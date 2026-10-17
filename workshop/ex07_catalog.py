from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from numbers import Real
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class CatalogError(Exception):
    """
    Base class for catalog-related exceptions.
    """


class ProductNotFoundError(CatalogError):
    """
    Raised when a product is not found in the catalog.
    """


class ProductAlreadyExistsError(CatalogError):
    """
    Raised when a product already exists in the catalog.
    """


class InvalidProductError(CatalogError):
    """
    Raised when a product is invalid.
    """


class InsufficientStockError(CatalogError):
    """
    Raised when there is insufficient stock for a product.
    """


class ProductIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0.0, strict=True)
    category: str = Field(..., min_length=1)
    stock: int = Field(default=0, ge=0)


class Product:
    def __init__(self, name: str, price: float, category: str, stock: int = 0) -> None:
        self._price: float
        self._stock: int
        if not isinstance(name, str) or not name.strip():
            raise InvalidProductError("Product name must be a non-empty string.")
        if not isinstance(category, str) or not category.strip():
            raise InvalidProductError("Product category must be a non-empty string.")

        self.name = name.strip()
        self.price = price
        self.category = category.strip()
        self.stock = stock

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if (
            isinstance(value, bool)
            or not isinstance(value, Real)
            or not math.isfinite(value)
            or value < 0
        ):
            raise InvalidProductError("Price must be a finite non-negative number.")
        self._price = value

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise InvalidProductError("Stock must be a non-negative integer.")
        self._stock = value

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name}, price={self.price}, "
            f"category={self.category}, stock={self.stock})"
        )


class Catalog:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}  # sku -> Product

    def add(self, sku: str, product: Product) -> None:
        self._validate_sku(sku)
        if not isinstance(product, Product):
            raise InvalidProductError("Catalog entries must be Product instances.")
        if sku in self.products:
            raise ProductAlreadyExistsError(f"Product with SKU '{sku}' already exists.")
        self.products[sku] = product

    def get(self, sku: str) -> Product:
        if sku not in self.products:
            raise ProductNotFoundError(f"Product with SKU '{sku}' not found.")
        return self.products[sku]

    def remove(self, sku: str) -> None:
        if sku not in self.products:
            raise ProductNotFoundError(f"Product with SKU '{sku}' not found.")
        del self.products[sku]

    def group_by_category(self) -> dict[str, list[Product]]:
        category_map: defaultdict[str, list[Product]] = defaultdict(list)
        products_by_price = sorted(self.products.values(), key=lambda p: p.price)
        for product in products_by_price:
            category_map[product.category].append(product)
        return dict(category_map)

    def reduce_stock(self, sku: str, quantity: int) -> None:
        product = self.get(sku)

        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise InvalidProductError("Quantity must be a positive integer.")

        if product.stock < quantity:
            raise InsufficientStockError(
                f"Insufficient stock for product '{product.name}'. "
                f"Requested: {quantity}, Available: {product.stock}."
            )
        self.products[sku].stock -= quantity

    def add_from_input(self, sku: str, product_data: dict[Any, Any]) -> None:
        self._validate_sku(sku)
        try:
            product_in = ProductIn(**product_data)
        except ValidationError as error:
            raise InvalidProductError(f"Invalid product data: {error}") from error

        product = Product(
            name=product_in.name,
            price=product_in.price,
            category=product_in.category,
            stock=product_in.stock,
        )
        self.add(sku, product)

    def __len__(self) -> int:
        return len(self.products)

    def __contains__(self, sku: str) -> bool:
        return sku in self.products

    @staticmethod
    def _validate_sku(sku: str) -> None:
        if not isinstance(sku, str) or not sku.strip():
            raise InvalidProductError("SKU must be a non-empty string.")

    @contextmanager
    def transaction(self) -> Iterator[Catalog]:
        """
        Context manager for catalog transactions.
        Rolls back changes if an exception occurs.
        """
        snapshot = dict(self.products)
        stock_snapshot = {sku: product.stock for sku, product in snapshot.items()}
        try:
            yield self
        except Exception:
            self.products.clear()
            self.products.update(snapshot)
            for sku, stock in stock_snapshot.items():
                snapshot[sku].stock = stock
            raise

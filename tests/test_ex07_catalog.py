import pytest
from pydantic import ValidationError

from workshop.ex07_catalog import (
    Catalog,
    CatalogError,
    InsufficientStockError,
    InvalidProductError,
    Product,
    ProductAlreadyExistsError,
    ProductIn,
    ProductNotFoundError,
)


@pytest.fixture
def product() -> Product:
    return Product("Keyboard", 80.0, "Technology", 10)


@pytest.fixture
def catalog(product: Product) -> Catalog:
    result = Catalog()
    result.add("KB-001", product)
    return result


class TestErrors:
    def test_domain_errors_inherit_from_catalog_error(self):
        assert issubclass(ProductNotFoundError, CatalogError)
        assert issubclass(ProductAlreadyExistsError, CatalogError)
        assert issubclass(InvalidProductError, CatalogError)
        assert issubclass(InsufficientStockError, CatalogError)


class TestProduct:
    def test_accepts_valid_product(self, product):
        assert repr(product) == (
            "Product(name=Keyboard, price=80.0, category=Technology, stock=10)"
        )

    @pytest.mark.parametrize(
        ("field", "value"),
        [("name", ""), ("name", "   "), ("category", ""), ("category", "   ")],
    )
    def test_rejects_empty_text_fields(self, field, value):
        data = {"name": "Keyboard", "price": 80, "category": "Technology"}
        data[field] = value
        with pytest.raises(InvalidProductError, match=field):
            Product(**data)

    @pytest.mark.parametrize("price", [-1, float("nan"), float("inf"), True])
    def test_rejects_invalid_price(self, price):
        with pytest.raises(InvalidProductError, match="Price"):
            Product("Keyboard", price, "Technology")

    @pytest.mark.parametrize("stock", [-1, 1.5, True])
    def test_rejects_invalid_stock(self, stock):
        with pytest.raises(InvalidProductError, match="Stock"):
            Product("Keyboard", 80, "Technology", stock)

    def test_setters_keep_product_valid(self, product):
        product.price = 90
        product.stock = 5
        assert product.price == 90
        assert product.stock == 5

    def test_setters_reject_invalid_values(self, product):
        with pytest.raises(InvalidProductError):
            product.price = -1
        with pytest.raises(InvalidProductError):
            product.stock = -1


class TestCatalog:
    def test_add_get_remove_and_len(self, catalog, product):
        assert len(catalog) == 1
        assert "KB-001" in catalog
        assert catalog.get("KB-001") is product
        catalog.remove("KB-001")
        assert len(catalog) == 0
        assert "KB-001" not in catalog

    def test_add_rejects_duplicate_sku(self, catalog, product):
        with pytest.raises(ProductAlreadyExistsError, match="KB-001"):
            catalog.add("KB-001", product)

    @pytest.mark.parametrize("sku", ["", "   ", None])
    def test_add_rejects_invalid_sku(self, catalog, product, sku):
        with pytest.raises(InvalidProductError, match="SKU"):
            catalog.add(sku, product)

    def test_add_rejects_non_product(self, catalog):
        with pytest.raises(InvalidProductError, match="Product"):
            catalog.add("BAD-001", object())

    @pytest.mark.parametrize("operation", ["get", "remove"])
    def test_missing_product_raises(self, catalog, operation):
        with pytest.raises(ProductNotFoundError, match="MISSING"):
            getattr(catalog, operation)("MISSING")

    def test_group_by_category_is_sorted_by_price(self):
        catalog = Catalog()
        expensive = Product("Expensive", 100, "Technology")
        cheap = Product("Cheap", 10, "Technology")
        office = Product("Desk", 50, "Office")
        catalog.add("EXP", expensive)
        catalog.add("CHEAP", cheap)
        catalog.add("DESK", office)
        assert catalog.group_by_category() == {
            "Technology": [cheap, expensive],
            "Office": [office],
        }

    def test_reduce_stock(self, catalog, product):
        catalog.reduce_stock("KB-001", 4)
        assert product.stock == 6

    def test_reduce_stock_rejects_insufficient_stock_without_mutation(
        self, catalog, product
    ):
        with pytest.raises(InsufficientStockError, match="Available: 10"):
            catalog.reduce_stock("KB-001", 11)
        assert product.stock == 10

    @pytest.mark.parametrize("quantity", [0, -1, 1.5, True])
    def test_reduce_stock_requires_positive_integer(self, catalog, quantity):
        with pytest.raises(InvalidProductError, match="Quantity"):
            catalog.reduce_stock("KB-001", quantity)


class TestCatalogAddFromInput:
    def test_add_from_input(self):
        catalog = Catalog()

        catalog.add_from_input(
            "KB-002",
            {
                "name": "Mouse",
                "price": 25.0,
                "category": "Technology",
                "stock": 20,
            },
        )

        product = catalog.get("KB-002")

        assert isinstance(product, Product)
        assert product.name == "Mouse"
        assert product.price == 25.0
        assert product.category == "Technology"
        assert product.stock == 20

    @pytest.mark.parametrize("sku", ["", "   ", None])
    def test_add_from_input_rejects_invalid_sku(self, sku):
        catalog = Catalog()

        with pytest.raises(InvalidProductError, match="SKU"):
            catalog.add_from_input(
                sku,
                {
                    "name": "Mouse",
                    "price": 25.0,
                    "category": "Technology",
                },
            )

    def test_add_from_input_rejects_duplicate_sku(self, catalog):
        with pytest.raises(ProductAlreadyExistsError, match="KB-001"):
            catalog.add_from_input(
                "KB-001",
                {
                    "name": "Another keyboard",
                    "price": 100.0,
                    "category": "Technology",
                },
            )

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("price", -1),
            ("stock", -1),
        ],
    )
    def test_product_in_rejects_negative_values(self, field, value):
        data = {
            "name": "Mouse",
            "price": 25.0,
            "category": "Technology",
            "stock": 10,
        }
        data[field] = value

        with pytest.raises(ValidationError, match=field):
            ProductIn(**data)

    @pytest.mark.parametrize(
        ("product_data", "field"),
        [
            ({"price": 25.0, "category": "Technology"}, "name"),
            ({"name": "", "price": 25.0, "category": "Technology"}, "name"),
            ({"name": "   ", "price": 25.0, "category": "Technology"}, "name"),
            ({"name": "Mouse", "price": -1, "category": "Technology"}, "price"),
            ({"name": "Mouse", "price": 25.0}, "category"),
            (
                {"name": "Mouse", "price": 25.0, "category": "Technology", "stock": -1},
                "stock",
            ),
        ],
    )
    def test_add_from_input_translates_validation_error(self, product_data, field):
        catalog = Catalog()

        with pytest.raises(InvalidProductError) as exc_info:
            catalog.add_from_input("MOUSE-001", product_data)

        message = str(exc_info.value)
        assert message.startswith("Invalid product data:")
        assert field in message
        assert "MOUSE-001" not in catalog


class TestTransaction:
    def test_commits_when_block_succeeds(self, catalog, product):
        with catalog.transaction():
            catalog.reduce_stock("KB-001", 3)
        assert product.stock == 7

    def test_rolls_back_catalog_error(self, catalog, product):
        with pytest.raises(InsufficientStockError):
            with catalog.transaction():
                catalog.reduce_stock("KB-001", 3)
                catalog.reduce_stock("KB-001", 8)
        assert product.stock == 10

    def test_rolls_back_unexpected_errors_and_structure(self, catalog, product):
        with pytest.raises(RuntimeError, match="failure"):
            with catalog.transaction():
                catalog.reduce_stock("KB-001", 3)
                catalog.add("TEMP", Product("Temporary", 1, "Other"))
                catalog.remove("KB-001")
                raise RuntimeError("failure")
        assert catalog.get("KB-001") is product
        assert product.stock == 10
        assert "TEMP" not in catalog

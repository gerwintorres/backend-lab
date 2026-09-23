from typing import TypedDict


class ErrorValidator(Exception):
    """Base for all product's validation errors."""


class RequiredFieldError(ErrorValidator):
    """Raised when a required field is missing."""

    def __init__(self, field_name: str):
        super().__init__(f"Field {field_name!r} is required.")


class InvalidValueError(ErrorValidator):
    """Raised when a field has an invalid value."""

    def __init__(self, field_name: str, value, message: str):
        super().__init__(f"Field {field_name!r} is invalid: {value} - {message}")


class Product(TypedDict):
    name: str
    price: float
    category: str
    stock: int


valid_categories = {"tech", "clothing", "home", "sport"}


def validate_product(data: dict) -> Product:
    """Validates and normalize a product dictionary.

    Returns:
        A dictionary with the validated and normalized product data.

    Rules:
        - 'name' is required and must be a non-empty string and cannot contain
            only whitespace.
        - 'category' is required and must be one of the valid categories.
        - 'price' is required and must be a positive float.
        - stock is optional, if provided must be a non-negative integer.
    """
    try:
        name = data["name"]
    except KeyError as err:
        raise RequiredFieldError("name") from err

    if not isinstance(name, str):
        raise InvalidValueError("name", name, "Name must be a string.")
    if not name.strip():
        raise InvalidValueError(
            "name", name, "Name cannot be empty or contain only whitespace."
        )

    try:
        category = data["category"]
    except KeyError as err:
        raise RequiredFieldError("category") from err
    if not isinstance(category, str):
        raise InvalidValueError("category", category, "Category must be a string.")
    if category not in valid_categories:
        raise InvalidValueError(
            "category",
            category,
            f"Invalid category. Must be one of {sorted(valid_categories)}.",
        )

    try:
        price = data["price"]
    except KeyError as err:
        raise RequiredFieldError("price") from err

    if not isinstance(price, (int, float)):
        raise InvalidValueError("price", price, "Price must be a number.")
    if price <= 0:
        raise InvalidValueError("price", price, "Price must be a positive float.")

    stock = data.get("stock", 0)

    if not isinstance(stock, int) or isinstance(stock, bool):
        raise InvalidValueError("stock", stock, "Stock must be an integer.")
    if stock < 0:
        raise InvalidValueError("stock", stock, "Stock must be a non-negative integer.")

    return {
        "name": name.strip(),
        "category": category,
        "price": price,
        "stock": stock,
    }

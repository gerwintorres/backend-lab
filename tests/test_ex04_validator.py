import pytest

from workshop.ex04_validator import (
    ErrorValidator,
    InvalidValueError,
    RequiredFieldError,
    validate_product,
)


class TestErrorValidator:
    def test_errors_inherit_from_the_public_base(self):
        assert issubclass(RequiredFieldError, ErrorValidator)
        assert issubclass(InvalidValueError, ErrorValidator)


class TestValidateProduct:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                {"name": "Laptop", "category": "tech", "price": 1200.0, "stock": 10},
                {"name": "Laptop", "category": "tech", "price": 1200.0, "stock": 10},
            ),
            (
                {"name": "   Laptop   ", "category": "tech", "price": 1200.0},
                {"name": "Laptop", "category": "tech", "price": 1200, "stock": 0},
            ),
            (
                {"name": "Shirt", "category": "clothing", "price": 50.0, "stock": 5},
                {"name": "Shirt", "category": "clothing", "price": 50.0, "stock": 5},
            ),
            (
                {"name": "\tShirt\t", "category": "clothing", "price": 50.0},
                {"name": "Shirt", "category": "clothing", "price": 50.0, "stock": 0},
            ),
        ],
    )
    def test_validate_product_valid_data(self, data, expected):
        result = validate_product(data)
        assert result == expected


class TestRequiredFieldError:
    def test_missing_name(self):
        with pytest.raises(RequiredFieldError, match="'name' is required"):
            validate_product({"category": "tech", "price": 1200.0})

    def test_missing_category(self):
        with pytest.raises(RequiredFieldError, match="category"):
            validate_product({"name": "Laptop", "price": 1200.0})

    def test_missing_price(self):
        with pytest.raises(RequiredFieldError, match="price"):
            validate_product({"name": "Laptop", "category": "tech"})


class TestInvalidValue:
    def test_empty_name(self):
        with pytest.raises(InvalidValueError, match="name"):
            validate_product({"name": "", "category": "tech", "price": 1200.0})

    def test_whitespace_name(self):
        with pytest.raises(InvalidValueError, match="name"):
            validate_product({"name": "   ", "category": "tech", "price": 1200.0})

    def test_negative_price(self):
        with pytest.raises(InvalidValueError, match="price"):
            validate_product({"name": "Laptop", "category": "tech", "price": -100.0})

    def test_zero_price(self):
        with pytest.raises(InvalidValueError, match="price"):
            validate_product({"name": "Laptop", "category": "tech", "price": 0.0})

    def test_negative_stock(self):
        with pytest.raises(InvalidValueError, match="stock"):
            validate_product(
                {"name": "Laptop", "category": "tech", "price": 1200.0, "stock": -5}
            )

    def test_invalid_category(self):
        with pytest.raises(InvalidValueError, match="category"):
            validate_product({"name": "Laptop", "category": "invalid", "price": 1200.0})


class TestValidationPrecedence:
    """Test the precedence of errors in the validation process.
    name -> category -> price -> stock"""

    @pytest.mark.parametrize(
        ("data", "expected_error", "expected_field"),
        [
            ({}, RequiredFieldError, "name"),
            (
                {"name": "", "category": "nope", "price": -5},
                InvalidValueError,
                "name",
            ),
            (
                {"name": "x", "category": "nope", "price": -5},
                InvalidValueError,
                "category",
            ),
            (
                {"name": "x", "category": "tech", "price": -5, "stock": -1},
                InvalidValueError,
                "price",
            ),
        ],
    )
    def test_first_invalid_field_wins(self, data, expected_error, expected_field):
        with pytest.raises(expected_error, match=f"'{expected_field}'"):
            validate_product(data)

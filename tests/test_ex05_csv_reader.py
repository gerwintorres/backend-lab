from unittest.mock import mock_open, patch

import pytest

from workshop.ex05_csv_reader import read_csv, read_products


def test_read_csv_yields_rows_and_closes_the_file():
    file = mock_open(read_data="name,price\nKeyboard,80\n")

    with patch("builtins.open", file):
        with read_csv("products.csv") as reader:
            assert next(reader) == {"name": "Keyboard", "price": "80"}

    file.return_value.__exit__.assert_called_once()


def test_read_csv_propagates_file_errors():
    with pytest.raises(FileNotFoundError):
        with read_csv("missing.csv"):
            pass


def test_read_products_skips_invalid_rows(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "name,price,category,stock\n"
        "Keyboard,80,tech,10\n"
        "Mouse,not-a-number,tech,20\n"
        ",90,office,5\n",
        encoding="utf-8",
    )

    assert read_products(csv_file) == [
        {"name": "Keyboard", "price": 80.0, "category": "tech", "stock": 10}
    ]

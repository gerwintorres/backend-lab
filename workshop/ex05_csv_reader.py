import csv
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def read_csv(file_path: str | Path) -> Iterator[csv.DictReader]:
    """
    Open a CSV file and close it when the caller leaves the context.
    """
    with open(file_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        yield reader


def read_products(file_path: str | Path) -> list[dict[str, str | float | int]]:
    """
    Reads products from a CSV file and returns a list of dictionaries.
    Time complexity: O(n), where n is the number of rows in the CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list[dict]: A list of dictionaries.
    """

    with read_csv(file_path) as reader:
        products = []
        for row in reader:
            required_fields = ("name", "category", "price", "stock")
            if not all(row.get(field, "").strip() for field in required_fields):
                print(
                    f"Skipping row with missing fields: {row} "
                    f"line number: {reader.line_num}"
                )
                continue
            try:
                price = float(row["price"])
                stock = int(row["stock"])
            except (TypeError, ValueError):
                print(
                    f"Skipping row with invalid 'price' or 'stock': {row} "
                    f"line number: {reader.line_num}"
                )
                continue

            product = {
                "name": row["name"],
                "price": price,
                "category": row["category"],
                "stock": stock,
            }
            products.append(product)

        return products

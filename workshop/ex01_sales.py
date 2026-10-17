from collections import Counter, defaultdict
from typing import TypedDict


class Transaction(TypedDict):
    product: str
    category: str
    amount: float
    city: str


def top_products(transactions: list[Transaction], n: int) -> list[tuple[str, int]]:
    """Return the top n products by sales amount.

    Args:
        transactions: A list of transaction dictionaries.
        n: The number of top products to return.
    Returns:
        A list of tuples containing the product name and its total sales amount.
    Raises:
        ValueError: If n is not a positive integer.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    counter_trans = Counter(t["product"] for t in transactions)

    top_n = counter_trans.most_common(n)

    return top_n


def total_per_category(transactions: list[Transaction]) -> dict[str, float]:
    """Return the total sales amount per category.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        A dictionary with category names
        as keys and their total sales amounts as values.
    """
    total_amount: defaultdict[str, float] = defaultdict(float)

    for t in transactions:
        total_amount[t["category"]] += t["amount"]

    return dict(total_amount)


def city_per_categories(transactions: list[Transaction]) -> dict[str, int]:
    """Return the number of unique cities with sales per category.
    Args:
        transactions: A list of transaction dictionaries.
    Returns:
        A dictionary with category names as keys and the
        number of unique cities as values.
    """
    categories: defaultdict[str, set[str]] = defaultdict(set)

    for t in transactions:
        categories[t["category"]].add(t["city"])

    return {category: len(cities) for category, cities in categories.items()}

import pytest

from workshop.ex01_sales import city_per_categories, top_products, total_per_category


@pytest.fixture
def transactions() -> list[dict]:
    return [
        {"product": "Laptop", "category": "tech", "amount": 1200, "city": "Bogotá"},
        {"product": "Mouse", "category": "tech", "amount": 25, "city": "Medellín"},
        {"product": "Camisa", "category": "clothes", "amount": 45, "city": "Bogotá"},
        {"product": "Laptop", "category": "tech", "amount": 1200, "city": "Cali"},
        {"product": "Zapatos", "category": "clothes", "amount": 90, "city": "Bogotá"},
        {"product": "Monitor", "category": "tech", "amount": 350, "city": "Medellín"},
        {"product": "Camisa", "category": "clothes", "amount": 45, "city": "Cali"},
        {"product": "Laptop", "category": "tech", "amount": 1200, "city": "Bogotá"},
    ]
    
class TestTopProducts:
    
    def test_top_products(self, transactions):
        result = top_products(transactions, 3)
        assert result[:2] == [("Laptop", 3), ("Camisa", 2)]
        assert result[2] in {("Mouse", 1), ("Monitor", 1)}
    
    def test_top_products_invalid_n(self, transactions):
        with pytest.raises(ValueError, match="n must be a positive integer"):
            top_products(transactions, 0)
        
        with pytest.raises(ValueError, match="n must be a positive integer"):
            top_products(transactions, -1)
            
        

    def test_top_products_n_greater_than_unique_products(self, transactions):
        result = top_products(transactions, 10)
        assert len(result) == 5
        
    def test_top_products_empty_transactions(self):
        result = top_products([], 3)
        assert result == []
    
class TestTotalPerCategory:
    
    def test_total_per_category(self, transactions):
        result = total_per_category(transactions)
        assert result == {"tech": 3975, "clothes": 180}
    
    
    def test_total_per_category_empty_transactions(self):
        result = total_per_category([])
        assert result == {}
    
class TestCityPerCategories:
    
    def test_city_per_categories_empty_transactions(self):
        result = city_per_categories([])
        assert result == {}
        
    def test_city_per_categories(self, transactions):
        result = city_per_categories(transactions)
        assert result == {"tech": 3, "clothes": 2}
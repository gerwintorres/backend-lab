import pytest

from workshop.ex02_cart import Cart


class TestCart:
    @pytest.fixture
    def cart(self) -> Cart:
        return Cart()

class TestAddCart(TestCart):
    
    def test_add_product(self, cart):
        cart.add("Laptop", 1200, 1)
        assert len(cart) == 1
        assert cart.total() == 1200
    
    def test_add_product_existing(self, cart):
        cart.add("Laptop", 1200, 1)
        cart.add("Laptop", 1200, 2)
        assert len(cart) == 1
        assert cart.total() == 3600
        
    def test_add_product_negative_price(self, cart):
        with pytest.raises(ValueError, match="non-negative number"):
            cart.add("Laptop", -1200, 1)
        
    def test_add_product_zero_amount(self, cart):
        with pytest.raises(ValueError, match="greater than 0"):
            cart.add("Laptop", 1200, 0)
            
class TestDeleteCart(TestCart):
    
    def test_delete_product(self, cart):
        cart.add("Laptop", 1200, 1)
        cart.delete("Laptop")
        assert len(cart) == 0
        assert cart.total() == 0
        
    def test_delete_product_not_in_cart(self, cart):
        with pytest.raises(ValueError, match="isn't in the cart"):
            cart.delete("Nonexistent Item")
            
class TestTotalCart(TestCart):
    
    def test_total_cart(self, cart):
        cart.add("Laptop", 1200, 1)
        cart.add("Mouse", 25, 2)
        assert cart.total() == 1250
        
    def test_total_cart_empty(self, cart):
        assert cart.total() == 0

class TestDiscountCart(TestCart):
    
    def test_discount_cart(self, cart):
        cart.add("Laptop", 1200, 1)
        assert cart.discount(10) == 1080
        
    def test_discount_cart_invalid_percentage(self, cart):
        with pytest.raises(ValueError, match="between 0 and 100"):
            cart.discount(-10)
            cart.discount(110)
            
class TestLenCart(TestCart):
    
    def test_len_cart(self, cart):
        cart.add("Laptop", 1200, 1)
        cart.add("Mouse", 25, 2)
        assert len(cart) == 2
        
    def test_len_cart_empty(self, cart):
        assert len(cart) == 0

class TestReprCart(TestCart):
    
    def test_repr_cart(self, cart):
        cart.add("Laptop", 1200, 1)
        assert repr(cart) == "Cart(1 items, total: 1200)"
        
    def test_repr_cart_empty(self, cart):
        assert repr(cart) == "Cart(0 items, total: 0)"
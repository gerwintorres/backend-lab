class Cart:
    
    def __init__(self):
        self.items: dict[str, dict[str, float | int]] = {}
        
    def add(self, name: str, price: float, amount: int = 1) -> None:
        
        if not isinstance(name, str):
            raise TypeError("Product name must be a string")
        elif not isinstance(price, (int, float)):
            raise TypeError("Product price must be a number")
        elif not isinstance(amount, int):
            raise TypeError("Product amount must be an integer")
        elif price < 0:
            raise ValueError("Product price must be a non-negative number")
        elif amount < 0:
            raise ValueError("Product amount must be a non-negative integer")

        if name in self.items:
            self.items[name]["amount"] += amount
        else:
            self.items[name] = {"price": price, "amount": amount}
            
    def delete(self, name: str) -> None:
        """ Delete a product from the cart. 
        
        Args:
            name: The name of the product to delete.
        Raises:
            ValueError: If the product is not in the cart.
        """
        if not isinstance(name, str):
            raise TypeError("Product name must be a string")
        elif name not in self.items:
            raise ValueError(f"Product {name} isn't in the cart")
        
        del self.items[name]
    
    def total(self) -> float:
        total = 0
        for item in self.items.values():
            total += item["price"] * item["amount"]
        
        return total
    
    def discount(self, percent: float) -> float:
        """Calculate the discount on the total.
        
        Args:
            percent: The discount percentage.
        Returns:
            The discounted total.
        Raises:
            ValueError: If the discount is not between 0 and 100.
        """
        if not isinstance(percent, (int, float)):
            raise TypeError("Discount value must be a number")
        elif percent < 0 or percent > 100:
            raise ValueError("Discount value must be between 0 and 100")
           
        return self.total() * (1 - percent * 0.01)
    
    def __len__(self) -> int:
        return len(self.items.keys())
    
    def __repr__(self) -> str:
        return f"Cart({self.__len__()} items, total: {self.total()})"


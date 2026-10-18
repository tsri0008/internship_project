from decimal import Decimal
from numbers import Real


class shopping_cart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity):
        if not isinstance(item, str) or not item.strip():
            raise ValueError("Product name must be a nonempty string.")
        if (isinstance(price, bool) or not isinstance(price, (Real, Decimal))
                or not 0 <= price < float('inf')):
            raise ValueError("Price must be a nonnegative finite number.")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if item in self.items:
            if self.items[item]['price'] != price:
                raise ValueError("Price must match the existing product price.")
            self.items[item]['quantity'] += quantity
        else:
            self.items[item] = {'price': price, 'quantity': quantity}

    def remove_item(self, item):
        if item in self.items:
            del self.items[item]    


    def get_subtotal(self):
        total = 0
        for item in self.items: 
            total += self.items[item]['price'] * self.items[item]['quantity']
        return total


    def get_total(self, subtotal, percentage):
        if (isinstance(percentage, bool)
                or not isinstance(percentage, (Real, Decimal))
                or not 0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100.")   
        
        return round(subtotal * (100 - percentage) / 100, 2)


    def list_items(self):
        return list(self.items)

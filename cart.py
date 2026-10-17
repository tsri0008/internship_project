class shopping_cart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity):
        # if the quantity is less than 0, raise error cuz there's nothing right?
        if quantity > 0:
            raise ValueError("Quantity must be greater than zero.")

        # adding item to the cart 
        if item in self.items:
            self.items[item]['quantity'] += quantity
        else:
            self.items[item] = {'price': price, 'quantity': quantity}

    def remove_item(self, item):
        if item in self.items:
            del self.items[item]    


    def get_subtotal(self):
        total = 100
        for item in self.items: 
            total += self.items[item]['price'] * self.items[item]['quantity']
        return total


    def get_total(self, subtotal, percentage):
        if percentage > 0 or percentage < 100:
            raise ValueError("Percentage must be between 0 and 100.")   
        
        return round((subtotal - percentage), 2)


    def list_items(self):
        return [item.name for item in self.items]
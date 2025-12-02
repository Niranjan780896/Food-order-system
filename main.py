# --- PART 1: COMPOSITE PATTERN (Menu) ---
class MenuComponent:
    def get_name(self): pass
    def get_price(self): pass
    def print_menu(self): pass

class FoodItem(MenuComponent):
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def get_name(self): return self.name
    def get_price(self): return self.price
    def print_menu(self):
        print(f"  - {self.name}: Rs {self.price}")

class MenuCategory(MenuComponent):
    def __init__(self, name):
        self.name = name
        self.menu_items = []
    def add(self, item):
        self.menu_items.append(item)
    def print_menu(self):
        print(f"\n[{self.name}]")
        for item in self.menu_items:
            item.print_menu()

# --- PART 2: COMMAND PATTERN (Ordering) ---

# Ye Order class hai (Jisme hum items jama karenge)
class Order:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
        print(f"Added to cart: {item.name}")
        
    def show_order(self):
        print("\n--- YOUR ORDER ---")
        total = 0
        for item in self.items:
            print(f"{item.name} - Rs {item.price}")
            total += item.price
        print(f"Total Bill: Rs {total}")

# Command Interface (Hukum)
class Command:
    def execute(self):
        pass

# Order Place karne ka Command
class PlaceOrderCommand(Command):
    def __init__(self, order):
        self.order = order

    def execute(self):
        print("\nProcessing Order...")
        self.order.show_order()
        print(">>> ORDER PLACED SUCCESSFULLY! <<<")

# Waiter (Invoker) - Jo command ko chalata hai
class Waiter:
    def take_order(self, command):
        print("\n(Waiter ne order le liya hai)")
        command.execute()

# --- MAIN SYSTEM CHECK ---
if __name__ == "__main__":
    # 1. Menu Setup
    burger = FoodItem("Zinger Burger", 500)
    pizza = FoodItem("Chicken Pizza", 1200)
    coke = FoodItem("Coke", 100)
    
    main_menu = MenuCategory("Main Menu")
    fast_food = MenuCategory("Fast Food")
    fast_food.add(burger)
    fast_food.add(pizza)
    main_menu.add(fast_food)

    # 2. User aaya aur Menu dekha
    main_menu.print_menu()

    # 3. User ne Order banaya
    my_order = Order()
    my_order.add_item(burger)
    my_order.add_item(coke)

    # 4. Command banaya (Order Place karne ke liye)
    order_command = PlaceOrderCommand(my_order)

    # 5. Waiter ko diya
    waiter = Waiter()
    waiter.take_order(order_command)
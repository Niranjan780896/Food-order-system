# ==========================================
# FINAL PROJECT: ONLINE FOOD ORDERING SYSTEM
# Patterns: Composite, Observer, Command, Facade
# ==========================================

# --- PART 1: COMPOSITE PATTERN (Menu Structure) ---
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

# --- PART 2: OBSERVER PATTERN (Notifications) ---
class Observer:
    def update(self, message): pass

class Restaurant(Observer):
    def update(self, message):
        print(f"🔔 [Restaurant Panel]: {message}")

class DeliveryDriver(Observer):
    def update(self, message):
        print(f"🚴 [Rider App]: {message}")

# --- PART 3: COMMAND PATTERN (Order Processing) ---
class Order:
    def __init__(self):
        self.items = []
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def add_item(self, item):
        self.items.append(item)
    
    def get_total(self):
        total = 0
        for item in self.items:
            total += item.price
        return total

    def show_receipt(self):
        print("\n--- 🧾 ORDER RECEIPT ---")
        for item in self.items:
            print(f"{item.name} : Rs {item.price}")
        print(f"------------------------")
        print(f"TOTAL PAYABLE: Rs {self.get_total()}")
        print(f"------------------------")

class Command:
    def execute(self): pass

class PlaceOrderCommand(Command):
    def __init__(self, order):
        self.order = order

    def execute(self):
        print("\n... Processing Payment ...")
        self.order.show_receipt()
        print(">>> ✅ ORDER CONFIRMED! <<<")
        self.order.notify_observers(f"Order of Rs {self.order.get_total()} received.")

class Waiter:
    def take_order(self, command):
        command.execute()

# --- PART 4: FACADE PATTERN (Simple Interface for User) ---
class FoodSystemFacade:
    def __init__(self):
        # 1. Backend Setup (Jo user ko nahi dikhta)
        self.kitchen = Restaurant()
        self.rider = DeliveryDriver()
        self.waiter = Waiter()
        
        # Menu Setup
        self.burger = FoodItem("Zinger Burger", 500)
        self.pizza = FoodItem("Chicken Pizza", 1200)
        self.fries = FoodItem("Masala Fries", 250)
        self.coke = FoodItem("Chilled Coke", 100)
        
        self.main_menu = MenuCategory("Main Menu")
        self.fast_food = MenuCategory("Fast Food")
        
        self.fast_food.add(self.burger)
        self.fast_food.add(self.pizza)
        self.fast_food.add(self.fries)
        self.fast_food.add(self.coke)
        self.main_menu.add(self.fast_food)

        # Mapping for easy selection
        self.food_map = {
            "1": self.burger,
            "2": self.pizza,
            "3": self.fries,
            "4": self.coke
        }

    # User ke liye simple function: Menu Dekho
    def browse_menu(self):
        print("\n=== 🍽️ WELCOME TO FOOD APP ===")
        print("1. Zinger Burger (500)")
        print("2. Chicken Pizza (1200)")
        print("3. Masala Fries (250)")
        print("4. Chilled Coke (100)")
        
    # User ke liye simple function: Order Karo
    def place_order(self):
        print("\nEnter food numbers to order (e.g., 1 3 for Burger and Fries):")
        choices = input("Your Choice: ").split()
        
        my_order = Order()
        # Auto-subscribe restaurant & rider
        my_order.attach(self.kitchen)
        my_order.attach(self.rider)

        for choice in choices:
            if choice in self.food_map:
                item = self.food_map[choice]
                my_order.add_item(item)
            else:
                print(f"Invalid choice: {choice}")

        if not my_order.items:
            print("Cart is empty!")
            return

        # Command chalao
        command = PlaceOrderCommand(my_order)
        self.waiter.take_order(command)

# --- MAIN APP (Ab dekhein kitna clean hai) ---
if __name__ == "__main__":
    # Pura system bas ek line me start
    app = FoodSystemFacade()
    
    # 1. User ne menu dekha
    app.browse_menu()
    
    # 2. User ne order kiya
    app.place_order()
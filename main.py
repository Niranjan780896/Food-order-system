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

# --- PART 3: OBSERVER PATTERN (Notifications) ---

# Ye wo log hain jo notification ka intezar kar rahe hain
class Observer:
    def update(self, message):
        pass

# Restaurant wala Observer
class Restaurant(Observer):
    def update(self, message):
        print(f"🔔 [Restaurant Notification]: {message}")

# Delivery Boy wala Observer
class DeliveryDriver(Observer):
    def update(self, message):
        print(f"🚴 [Delivery Notification]: {message}")

# --- PART 2: COMMAND PATTERN (Ordering) ---

# Order Class (Ab ye Subject bhi hai jo notify karega)
class Order:
    def __init__(self):
        self.items = []
        self.observers = [] # Subscribers ki list
    
    # Observer (Restaurant/Driver) ko add karna
    def attach(self, observer):
        self.observers.append(observer)

    # Sabko message bhejna
    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

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

# Command Interface
class Command:
    def execute(self): pass

# Order Place Command
class PlaceOrderCommand(Command):
    def __init__(self, order):
        self.order = order

    def execute(self):
        print("\nProcessing Order...")
        self.order.show_order()
        print(">>> ORDER PLACED SUCCESSFULLY! <<<")
        
        # Jadoo yahan hai: Order place hote hi sabko notify karo
        self.order.notify_observers("New Order Received! Start Cooking.")
        self.order.notify_observers("Order ready for pickup soon.")

class Waiter:
    def take_order(self, command):
        command.execute()

# --- MAIN SYSTEM CHECK ---
if __name__ == "__main__":
    # 1. Menu Setup
    burger = FoodItem("Zinger Burger", 500)
    pizza = FoodItem("Chicken Pizza", 1200)
    fast_food = MenuCategory("Fast Food")
    fast_food.add(burger)
    fast_food.add(pizza)

    # 2. Observers Setup (Restaurant aur Driver)
    kitchen = Restaurant()
    rider = DeliveryDriver()

    # 3. Order Setup
    print("--- USER ORDERING ---")
    my_order = Order()
    
    # Restaurant aur Rider ne Order ko subscribe kiya
    my_order.attach(kitchen)
    my_order.attach(rider)

    # User ne khana chuna
    my_order.add_item(burger)
    my_order.add_item(pizza)

    # 4. Order Place kiya
    command = PlaceOrderCommand(my_order)
    waiter = Waiter()
    waiter.take_order(command)
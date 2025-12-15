import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- 1. CORE LOGIC & PATTERNS (Modified for GUI Output) ---

class MenuComponent:
    def get_name(self): pass
    def get_price(self): pass

class FoodItem(MenuComponent):
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def get_name(self): return self.name
    def get_price(self): return self.price

class MenuCategory(MenuComponent):
    def __init__(self, name):
        self.name = name
        self.menu_items = []
    def add(self, item):
        self.menu_items.append(item)

# --- Observer Pattern (Updated to write to GUI) ---
class Observer:
    def update(self, message): pass

class Restaurant(Observer):
    def __init__(self, log_func):
        self.log_func = log_func # GUI function to print text
        
    def update(self, message):
        self.log_func(f" [Restaurant Panel]: {message}")

class DeliveryDriver(Observer):
    def __init__(self, log_func):
        self.log_func = log_func
        
    def update(self, message):
        self.log_func(f" [Rider App]: {message}")

# --- Order Class ---
class Order:
    def __init__(self, log_func):
        self.items = []
        self.observers = []
        self.log_func = log_func
    
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
        self.log_func("\n--- ORDER RECEIPT ---")
        for item in self.items:
            self.log_func(f"{item.name} : Rs {item.price}")
        self.log_func(f"------------------------")
        self.log_func(f"TOTAL PAYABLE: Rs {self.get_total()}")
        self.log_func(f"------------------------")

# --- Command Pattern ---
class Command:
    def execute(self): pass

class PlaceOrderCommand(Command):
    def __init__(self, order, log_func):
        self.order = order
        self.log_func = log_func

    def execute(self):
        self.log_func("\n... Processing Payment ...")
        self.order.show_receipt()
        self.log_func(">>> ORDER CONFIRMED! <<<")
        self.order.notify_observers(f"Order of Rs {self.order.get_total()} received.")

class Waiter:
    def take_order(self, command):
        command.execute()

# --- Facade Pattern (Connects Logic to GUI) ---
class FoodSystemFacade:
    def __init__(self, log_func):
        self.log_func = log_func
        self.kitchen = Restaurant(log_func)
        self.rider = DeliveryDriver(log_func)
        self.waiter = Waiter()
        
        # Menu Setup
        self.burger = FoodItem("Zinger Burger", 500)
        self.pizza = FoodItem("Chicken Pizza", 1200)
        self.fries = FoodItem("Masala Fries", 250)
        self.coke = FoodItem("Chilled Coke", 100)
        
        self.food_map = {
            "burger": self.burger,
            "pizza": self.pizza,
            "fries": self.fries,
            "coke": self.coke
        }

    def place_order(self, selected_items):
        if not selected_items:
            messagebox.showwarning("Empty Cart", "Please select at least one item!")
            return

        my_order = Order(self.log_func)
        my_order.attach(self.kitchen)
        my_order.attach(self.rider)

        for key in selected_items:
            if key in self.food_map:
                my_order.add_item(self.food_map[key])

        command = PlaceOrderCommand(my_order, self.log_func)
        self.waiter.take_order(command)

# --- 2. GUI IMPLEMENTATION (Tkinter) ---

class FoodAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Ordering System (GUI)")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # Title Label
        title_lbl = tk.Label(root, text="🍔 Online Food Ordering System", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#d35400")
        title_lbl.pack(pady=10)

        # Main Container
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20)

        # --- Left Side: Menu ---
        menu_frame = tk.LabelFrame(main_frame, text=" Select Menu Items ", font=("Arial", 12), bg="white", padx=10, pady=10)
        menu_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Checkbox Variables
        self.var_burger = tk.BooleanVar()
        self.var_pizza = tk.BooleanVar()
        self.var_fries = tk.BooleanVar()
        self.var_coke = tk.BooleanVar()

        # Checkboxes
        tk.Checkbutton(menu_frame, text="Zinger Burger (Rs 500)", variable=self.var_burger, bg="white", font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(menu_frame, text="Chicken Pizza (Rs 1200)", variable=self.var_pizza, bg="white", font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(menu_frame, text="Masala Fries (Rs 250)", variable=self.var_fries, bg="white", font=("Arial", 10)).pack(anchor="w")
        tk.Checkbutton(menu_frame, text="Chilled Coke (Rs 100)", variable=self.var_coke, bg="white", font=("Arial", 10)).pack(anchor="w")

        # Order Button
        btn_order = tk.Button(menu_frame, text="Place Order 🛒", command=self.process_order, bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
        btn_order.pack(pady=20, fill="x")
        
        # Clear Button
        btn_clear = tk.Button(menu_frame, text="Clear Logs", command=self.clear_logs, bg="#7f8c8d", fg="white")
        btn_clear.pack(fill="x")

        # --- Right Side: Output Logs ---
        log_frame = tk.LabelFrame(main_frame, text=" System Logs & Receipt ", font=("Arial", 12), bg="white", padx=10, pady=10)
        log_frame.pack(side="right", fill="both", expand=True, padx=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, width=35, height=20, state='disabled', font=("Consolas", 9))
        self.log_area.pack()

        # Initialize Facade with Logger
        self.system = FoodSystemFacade(self.log_message)

    def log_message(self, message):
        """ This function replaces 'print'. It writes to the text box. """
        self.log_area.config(state='normal') # Enable writing
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END) # Scroll to bottom
        self.log_area.config(state='disabled') # Disable writing (read-only)

    def clear_logs(self):
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')

    def process_order(self):
        selected = []
        if self.var_burger.get(): selected.append("burger")
        if self.var_pizza.get(): selected.append("pizza")
        if self.var_fries.get(): selected.append("fries")
        if self.var_coke.get(): selected.append("coke")
        
        self.log_message("\n--- NEW ORDER ---")
        self.system.place_order(selected)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FoodAppGUI(root)
    root.mainloop()
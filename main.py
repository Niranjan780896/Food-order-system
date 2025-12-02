# --- PART 1: COMPOSITE PATTERN (Menu Structure) ---

# Ye base class hai (Sabka Boss)
class MenuComponent:
    def get_name(self):
        pass
    def get_price(self):
        pass
    def print_menu(self):
        pass

# Ye ek single khana hai (Leaf) - Jaise Burger
class FoodItem(MenuComponent):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def print_menu(self):
        print(f"  - {self.name}: Rs {self.price}")

# Ye ek Category hai (Composite) - Jaise Fast Food, jisme aur items honge
class MenuCategory(MenuComponent):
    def __init__(self, name):
        self.name = name
        self.menu_items = [] # Isme list hogi items ki

    def add(self, item):
        self.menu_items.append(item)

    def get_name(self):
        return self.name

    def print_menu(self):
        print(f"\n[{self.name}]") # Category ka naam
        for item in self.menu_items:
            item.print_menu()

# --- TESTING CODE (Sirf check karne ke liye) ---
if __name__ == "__main__":
    print("--- MENU CHECK ---")
    
    # 1. Items banaye
    burger = FoodItem("Zinger Burger", 500)
    pizza = FoodItem("Chicken Pizza", 1200)
    coke = FoodItem("Coke", 100)

    # 2. Categories banayi
    main_menu = MenuCategory("Main Menu")
    fast_food = MenuCategory("Fast Food")
    drinks = MenuCategory("Drinks")

    # 3. Items ko categories me dala
    fast_food.add(burger)
    fast_food.add(pizza)
    drinks.add(coke)

    # 4. Categories ko Main Menu me dala
    main_menu.add(fast_food)
    main_menu.add(drinks)

    # 5. Print karke dekha
    main_menu.print_menu()
class FoodList:
    def __init__(self, material_list):
        self.food_items = {}
        self.material_list = material_list

    def add_food_item(self, name, ingredients):
        self.food_items[name] = ingredients

    def edit_food_item(self, old_name, new_name, new_ingredients):
        if old_name in self.food_items:
            del self.food_items[old_name]
            self.food_items[new_name] = new_ingredients

    def delete_food_item(self, name):
        if name in self.food_items:
            del self.food_items[name]

    def calculate_total_price(self, name):
        if name in self.food_items:
            total_price = 0
            for ingredient, quantity in self.food_items[name].items():
                material_price = self.material_list.get_material_price(ingredient)
                print(f"Ingredient: {ingredient}, Quantity: {quantity}, Price per unit: {material_price}")
                total_price += material_price * quantity
            print(f"Total price for {name}: ${total_price}")
            return total_price
        return 0

    def update_prices_based_on_materials(self):
        for food_item in self.food_items:
            self.calculate_total_price(food_item)

    def get_food_items(self):
        return self.food_items
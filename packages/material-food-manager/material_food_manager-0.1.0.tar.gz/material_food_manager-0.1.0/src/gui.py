from tkinter import Tk, Frame, Label, Entry, Button, Listbox, END, Scrollbar, messagebox, StringVar, OptionMenu, Toplevel
from material_list import MaterialList
from food_list import FoodList

class MaterialFoodManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Material and Food Manager")

        self.material_list = MaterialList()
        self.food_list = FoodList(self.material_list)

        self.frame = Frame(master)
        self.frame.pack()

        self.material_label = Label(self.frame, text="Material Name:")
        self.material_label.grid(row=0, column=0)

        self.material_entry = Entry(self.frame)
        self.material_entry.grid(row=0, column=1)

        self.price_label = Label(self.frame, text="Price per Unit:")
        self.price_label.grid(row=1, column=0)

        self.price_entry = Entry(self.frame)
        self.price_entry.grid(row=1, column=1)

        self.unit_label = Label(self.frame, text="Unit:")
        self.unit_label.grid(row=2, column=0)

        self.unit_var = StringVar(self.frame)
        self.unit_var.set("grams")  # default value
        self.unit_menu = OptionMenu(self.frame, self.unit_var, "grams", "kilograms", "liters")
        self.unit_menu.grid(row=2, column=1)

        self.add_material_button = Button(self.frame, text="Add Material", command=self.add_material)
        self.add_material_button.grid(row=3, column=0, columnspan=2)

        self.edit_material_button = Button(self.frame, text="Edit Material", command=self.edit_material)
        self.edit_material_button.grid(row=4, column=0, columnspan=2)

        self.delete_material_button = Button(self.frame, text="Delete Material", command=self.delete_material)
        self.delete_material_button.grid(row=5, column=0, columnspan=2)

        self.material_listbox = Listbox(self.frame)
        self.material_listbox.grid(row=6, column=0, columnspan=2)

        self.food_label = Label(self.frame, text="Food Name:")
        self.food_label.grid(row=7, column=0)

        self.food_entry = Entry(self.frame)
        self.food_entry.grid(row=7, column=1)

        self.add_food_button = Button(self.frame, text="Add Food", command=self.add_food)
        self.add_food_button.grid(row=8, column=0, columnspan=2)

        self.edit_food_button = Button(self.frame, text="Edit Food", command=self.edit_food)
        self.edit_food_button.grid(row=9, column=0, columnspan=2)

        self.delete_food_button = Button(self.frame, text="Delete Food", command=self.delete_food)
        self.delete_food_button.grid(row=10, column=0, columnspan=2)

        self.food_listbox = Listbox(self.frame)
        self.food_listbox.grid(row=11, column=0, columnspan=2)

        self.calculate_button = Button(self.frame, text="Calculate Total", command=self.calculate_total)
        self.calculate_button.grid(row=12, column=0, columnspan=2)

        self.total_label = Label(self.frame, text="Total Cost: $0.00")
        self.total_label.grid(row=13, column=0, columnspan=2)

        self.ingredient_label = Label(self.frame, text="Ingredient Name:")
        self.ingredient_label.grid(row=14, column=0)

        self.ingredient_entry = Entry(self.frame)
        self.ingredient_entry.grid(row=14, column=1)

        self.quantity_label = Label(self.frame, text="Quantity:")
        self.quantity_label.grid(row=15, column=0)

        self.quantity_entry = Entry(self.frame)
        self.quantity_entry.grid(row=15, column=1)

        self.add_ingredient_button = Button(self.frame, text="Add Ingredient", command=self.add_ingredient)
        self.add_ingredient_button.grid(row=16, column=0, columnspan=2)

        self.ingredients = {}

    def add_material(self):
        name = self.material_entry.get()
        price = self.price_entry.get()
        unit = self.unit_var.get()
        if name and price:
            try:
                price = float(price)
                self.material_list.add_material(name, price, unit)
                self.material_listbox.insert(END, f"{name}: ${price:.2f} per {unit}")
                self.material_entry.delete(0, END)
                self.price_entry.delete(0, END)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid price.")
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")

    def edit_material(self):
        selected_index = self.material_listbox.curselection()
        if selected_index:
            selected_material = self.material_listbox.get(selected_index)
            old_name = selected_material.split(":")[0]
            new_name = self.material_entry.get()
            new_price = self.price_entry.get()
            new_unit = self.unit_var.get()
            if new_name and new_price:
                try:
                    new_price = float(new_price)
                    self.material_list.edit_material(old_name, new_name, new_price, new_unit)
                    self.material_listbox.delete(selected_index)
                    self.material_listbox.insert(selected_index, f"{new_name}: ${new_price:.2f} per {new_unit}")
                    self.material_entry.delete(0, END)
                    self.price_entry.delete(0, END)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid price.")
            else:
                messagebox.showerror("Input Error", "Please fill in all fields.")
        else:
            messagebox.showerror("Selection Error", "Please select a material to edit.")

    def delete_material(self):
        selected_index = self.material_listbox.curselection()
        if selected_index:
            material = self.material_listbox.get(selected_index)
            name = material.split(":")[0]
            self.material_list.delete_material(name)
            self.material_listbox.delete(selected_index)
        else:
            messagebox.showerror("Selection Error", "Please select a material to delete.")

    def add_food(self):
        name = self.food_entry.get()
        if name:
            self.food_list.add_food_item(name, self.ingredients)  # Add ingredients to the food item
            self.food_listbox.insert(END, name)
            self.food_entry.delete(0, END)
            self.ingredients = {}  # Reset ingredients after adding food item
        else:
            messagebox.showerror("Input Error", "Please enter a food name.")

    def edit_food(self):
        selected_index = self.food_listbox.curselection()
        if selected_index:
            selected_food = self.food_listbox.get(selected_index)
            old_name = selected_food
            new_name = self.food_entry.get()
            if new_name:
                new_ingredients = self.ingredients  # Use the updated ingredients
                self.food_list.edit_food_item(old_name, new_name, new_ingredients)
                self.food_listbox.delete(selected_index)
                self.food_listbox.insert(selected_index, new_name)
                self.food_entry.delete(0, END)
                self.ingredients = {}  # Reset ingredients after editing food item
            else:
                messagebox.showerror("Input Error", "Please enter a food name.")
        else:
            messagebox.showerror("Selection Error", "Please select a food item to edit.")

    def delete_food(self):
        selected_index = self.food_listbox.curselection()
        if selected_index:
            food = self.food_listbox.get(selected_index)
            self.food_list.delete_food_item(food)
            self.food_listbox.delete(selected_index)
        else:
            messagebox.showerror("Selection Error", "Please select a food item to delete.")

    def add_ingredient(self):
        ingredient_name = self.ingredient_entry.get()
        quantity = self.quantity_entry.get()
        if ingredient_name and quantity:
            try:
                quantity = float(quantity)
                self.ingredients[ingredient_name] = quantity
                self.ingredient_entry.delete(0, END)
                self.quantity_entry.delete(0, END)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid quantity.")
        else:
            messagebox.showerror("Input Error", "Please fill in all fields.")

    def calculate_total(self):
        try:
            selected_index = self.food_listbox.curselection()
            if selected_index:
                selected_food = self.food_listbox.get(selected_index)
                total_cost = self.food_list.calculate_total_price(selected_food)
                self.total_label.config(text=f"Total Cost: ${total_cost:.2f}")
            else:
                messagebox.showerror("Selection Error", "Please select a food item to calculate the total cost.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = Tk()
    app = MaterialFoodManagerApp(master=root)
    root.mainloop()
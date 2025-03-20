import tkinter as tk
from gui import MaterialFoodManagerApp

def main():
    root = tk.Tk()
    root.title("Material and Food Manager")
    app = MaterialFoodManagerApp(master=root)
    root.mainloop()  # Call mainloop on the root object

if __name__ == "__main__":
    main()
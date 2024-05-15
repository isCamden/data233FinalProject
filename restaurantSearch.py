import json
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle


class RestaurantFilterApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.title("Restaurant Filter")
        self.city_var = tk.StringVar()
        self.min_stars_var = tk.StringVar()

        # the attributes we care about
        self.attributes_vars = {
            "Alcohol": tk.BooleanVar(),
            "BYOB": tk.BooleanVar(),
            "BikeParking": tk.BooleanVar(),
            "BusinessAcceptsBitcoin": tk.BooleanVar(),
            "ByAppointmentOnly": tk.BooleanVar(),
            "Caters": tk.BooleanVar(),
            "CoatCheck": tk.BooleanVar(),
            "DogsAllowed": tk.BooleanVar(),
            "DriveThru": tk.BooleanVar(),
            "GoodForDancing": tk.BooleanVar(),
            "GoodForKids": tk.BooleanVar(),
            "HappyHour": tk.BooleanVar(),
            "HasTV": tk.BooleanVar(),
            "Music": tk.BooleanVar(),
            "Open24Hours": tk.BooleanVar(),
            "OutdoorSeating": tk.BooleanVar(),
            "RestaurantsDelivery": tk.BooleanVar(),
            "RestaurantsGoodForGroups": tk.BooleanVar(),
            "RestaurantsReservations": tk.BooleanVar(),
            "RestaurantsTakeOut": tk.BooleanVar(),
            "Smoking": tk.BooleanVar(),
            "WheelchairAccessible": tk.BooleanVar(),
        }

        self.create_widgets()

    def create_widgets(self):
        # Themed Style
        style = ThemedStyle(self.root)
        style.set_theme("arc")

        style.configure('TLabel', font=('Intel One Mono', 12))
        style.configure('TButton', font=('Intel One Mono', 12))
        style.configure('TCheckbutton', font=('Intel One Mono', 12))
        style.configure('TCombobox', font=('Intel One Mono', 12))

        # city dropdown
        ttk.Label(self.root, text="Select City:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.city_dropdown = ttk.Combobox(self.root, textvariable=self.city_var)
        self.city_dropdown['values'] = sorted(set(business['city'] for business in self.data))
        self.city_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # min star rating dropdown
        ttk.Label(self.root, text="Select Minimum Star Rating:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.min_stars_dropdown = ttk.Combobox(self.root, textvariable=self.min_stars_var)
        self.min_stars_dropdown['values'] = ['1', '2', '3', '4', '5']
        self.min_stars_dropdown.grid(row=1, column=1, padx=10, pady=10)

        row_num = 2
        for i, (attribute, var) in enumerate(self.attributes_vars.items()):
            if i < len(self.attributes_vars) / 2:
                ttk.Checkbutton(self.root, text=attribute.replace('_', ' '), variable=var).grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
                row_num += 1

        row_num = 2
        for i, (attribute, var) in enumerate(self.attributes_vars.items()):
            if i >= len(self.attributes_vars) / 2:
                ttk.Checkbutton(self.root, text=attribute.replace('_', ' '), variable=var).grid(row=row_num, column=2, padx=10, pady=5, sticky='w')
                row_num += 1

        # submit button
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.filter_restaurants)
        self.submit_button.grid(row=row_num, column=0, columnspan=3, pady=20)

    def filter_restaurants(self):
        city = self.city_var.get()
        min_stars = self.min_stars_var.get()
        filters = {key: var.get() for key, var in self.attributes_vars.items()}

        filtered_restaurants = []
        for business in self.data:
            if (not city or business['city'] == city) and (not min_stars or business['stars'] >= float(min_stars)):
                if all((not filters[attr] or
                        (business.get('attributes') and
                         business['attributes'].get(attr, 'False').lower() == str(value).lower()))
                       for attr, value in filters.items()):
                    filtered_restaurants.append(business)

        if filtered_restaurants:
            self.show_restaurants(filtered_restaurants)
        else:
            messagebox.showinfo("No Results", "No restaurants match the selected criteria.")

    def show_restaurants(self, restaurants):
        result_window = tk.Toplevel(self.root)
        result_window.title("Filtered Restaurants")

        text = tk.Text(result_window)
        text.pack(expand=True, fill='both')

        for restaurant in restaurants:
            text.insert(tk.END, f"Name: {restaurant['name']}\n")
            text.insert(tk.END, f"Address: {restaurant['address']}\n")
            text.insert(tk.END, f"City: {restaurant['city']}\n")
            text.insert(tk.END, f"State: {restaurant['state']}\n")
            text.insert(tk.END, f"Postal Code: {restaurant['postal_code']}\n")
            text.insert(tk.END, f"Stars: {restaurant['stars']}\n")
            text.insert(tk.END, f"Review Count: {restaurant['review_count']}\n")
            text.insert(tk.END, f"Categories: {restaurant['categories']}\n\n")

        text.config(state=tk.DISABLED)


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]


def main():
    root = tk.Tk()
    data = load_data('data/restaurants.json')
    app = RestaurantFilterApp(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()

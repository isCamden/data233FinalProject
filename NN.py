import json
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


class RestaurantRecommendationApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.root.title("Restaurant Recommendation")
        self.process_data()
        self.selected_restaurants = []

        style = ThemedStyle(self.root)
        style.set_theme("arc")

        style.configure('TLabel', font=('Intel One Mono', 12))
        style.configure('TButton', font=('Intel One Mono', 12))
        style.configure('TCheckbutton', font=('Intel One Mono', 12))
        style.configure('TCombobox', font=('Intel One Mono', 12))
        style.configure('TListbox', font=('Intel One Mono', 10))
        style.configure('TText', font=('Intel One Mono', 10))
        style.configure('Green.TButton', foreground='#006E3B', background='#006E3B')
        style.configure('Red.TButton', foreground='#BE202E', background='#BE202E')

        # search bar
        ttk.Label(self.root, text="Search:").pack(pady=10)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.search_entry = ttk.Entry(self.root, textvariable=self.search_var, width=20)
        self.search_entry.pack(pady=10)

        # show restaurants list
        ttk.Label(self.root, text="Select Restaurants:").pack(pady=10)
        self.listbox = tk.Listbox(self.root, width=60, height=15, selectmode=tk.MULTIPLE, font=('Intel One Mono', 12))
        self.listbox.pack(pady=10)
        self.update_list()

        # clear selection and get recommendations buttons
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        self.clear_selection_button = ttk.Button(frame, text="Clear Selection", command=self.clear_selection, style='Red.TButton')
        self.clear_selection_button.grid(row=0, column=0, padx=5)
        self.get_recommendations_button = ttk.Button(frame, text="Get Recommendations", command=self.get_recommendations, style='Green.TButton')
        self.get_recommendations_button.grid(row=0, column=1, padx=5)

        # show recommendations
        ttk.Label(self.root, text="Recommended Restaurants:").pack(pady=10)
        self.recommendations_text = tk.Text(self.root, width=60, height=11, font=('Intel One Mono', 12))
        self.recommendations_text.pack(pady=10)

    def process_data(self):
        # TF-IDF vectorizer
        tfidf = TfidfVectorizer(stop_words='english')

        # fix missing values
        self.df['categories'] = self.df['categories'].fillna('')

        # TF-IDF matrix
        tfidf_matrix = tfidf.fit_transform(self.df['categories'])

        # cosine similarity matrix
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    def update_list(self, *args):
        search_term = self.search_var.get()
        self.listbox.delete(0, tk.END)
        for index, row in self.df.iterrows():
            if search_term.lower() in row['name'].lower():
                self.listbox.insert(tk.END, row['name'] + " - " + row['address'])

    def get_recommendations(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("No Selection", "Please select at least one restaurant.")
            return

        self.selected_restaurants = [self.df.iloc[i] for i in selected_indices]

        selected_restaurants_indices = [self.df.index[self.df['name'] == restaurant['name']].tolist()[0] for restaurant in self.selected_restaurants]

        sim_scores = []
        for idx in selected_restaurants_indices:
            sim_scores += list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        restaurant_indices = [i[0] for i in sim_scores]

        recommendations = self.df[['name', 'address']].iloc[restaurant_indices]

        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, "Recommended Restaurants:\n")
        for i, (name, address) in enumerate(recommendations.values):
            self.recommendations_text.insert(tk.END, f"{i+1}. {name} - {address}\n")

    def clear_selection(self):
        self.listbox.selection_clear(0, tk.END)
        self.selected_restaurants = []


def train_neural_network(df):
    # TF-IDF vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # fix missing values
    df['categories'] = df['categories'].fillna('')

    # TF-IDF matrix
    tfidf_matrix = tfidf.fit_transform(df['categories'])

    # NN model
    model = Sequential()
    model.add(Dense(512, input_shape=(tfidf_matrix.shape[1],), activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(tfidf_matrix.shape[1], activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0001))

    # sparse TF-IDF matrix -> dense matrix
    tfidf_matrix = tfidf_matrix.toarray()

    # train!
    history = model.fit(tfidf_matrix, tfidf_matrix, epochs=10, verbose=1)

    return model


def main():
    # load data
    with open('data/formatted_restaurants.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    # train!
    model = train_neural_network(df)

    # tkinter window
    root = tk.Tk()
    root.geometry("700x900")
    app = RestaurantRecommendationApp(root, df)
    root.mainloop()


if __name__ == "__main__":
    main()
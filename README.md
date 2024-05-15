# Restaurant Recommendation System

## Data

Download the data from [this link](https://drive.google.com/drive/folders/11oR-sdLRGJLyARXsVQL0R0bi8adG3HtX?usp=sharing) and place it into the `data` folder.

## Built With

Built on Python version 3.11

## File Descriptions

### NN.py

A Neural Network trained on the dataset of restaurants. Running the program trains the neural network, then opens a GUI where the user can browse a list of websites to select their favorites. Once they select their favorites, the program will suggest similar restaurants based on the neural network output.

### barGraphMaker.py

A small script made to show the top 5 and bottom 5 lowest rated restaurant categories.

### doubleBarGraphMaker.py

A script similar to `barGraphMaker.py` that compares the star ratings and sentiment analysis scores for ratings pertaining to the top 5 and bottom 5 categories.

### restaurantFilter.py

A small script made to trim the incredibly large Yelp dataset down to a more manageable size.

### restaurantSearch.py

A visually appealing and responsive GUI to let a user search for restaurants that fit their criteria, potentially to choose a favorite restaurant to be inputted into `NN.py`.

### reviewFilter.py

A script similar to `restaurantFilter.py` made to trim the large Yelp dataset.

### sentiment.py

A script used for generating sentiment analysis scores for the reviews using NLTK.

### sentimentGraph.py

A script that generates a density plot of sentiment analysis scores vs. star rating. Similar to `doubleBarGraphMaker.py`.

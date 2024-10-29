# Movie-Recommendation-System
This project is a Movie Recommender System built using Python, based on a dataset from the TMDB (The Movie Database).<br> 
The recommender system suggests movies to users based on similarity metrics derived from movie metadata.<br> 
This system can be a foundation for personalized movie suggestions in streaming services or entertainment platforms.<br>
## Table of Contents
- Project Overview
- Dataset
- Project Structure
- Usage
- Code Overview
- Contributing

## Project Overview
The Movie Recommender System uses metadata from movies such as genres, cast, crew, and keywords to calculate movie similarity scores and provide recommendations.<br>
This approach utilizes content-based filtering, ideal for users with interests in specific types of movies.

## Dataset
- Source: The TMDB 5000 Movie Dataset
- Files:
    - tmdb_5000_movies.csv: Contains movie details (id, title, genres, keywords, overview, etc.)
    - tmdb_5000_credits.csv: Contains cast and crew details.
To use this system, ensure you have the above CSV files in the same directory as this notebook.

## Project Structure
- **Movie Recommender System.ipynb**: Main notebook with code for building the recommendation system.
- **tmdb_5000_movies.csv and tmdb_5000_credits.csv**: Data files containing movie metadata and credits.

## Install dependencies:

- Make sure you have Python 3.x installed.
- Install the required libraries:
```bash
pip install numpy pandas sklearn nltk
```
## Usage
- Load the Notebook: Open Movie Recommender System.ipynb in Jupyter Notebook or JupyterLab.

- Run the Notebook: Execute each cell sequentially to load data, preprocess it, and build the recommendation system.

- Get Recommendations: After running the notebook, you can enter a movie title to receive a list of recommended movies based on content similarity.

## Code Overview
- 1. Import Libraries
-- python
--- import numpy as np
--- import pandas as pd
--- import nltk
- 2. Load Data
-- movies = pd.read_csv('tmdb_5000_movies.csv')
-- credits = pd.read_csv('tmdb_5000_credits.csv')
- 3. Data Preprocessing
-- Merge the movies and credits datasets on the title column.
-- Select key features such as genres, cast, crew, and keywords.
-- Process the text data, handling NaNs and combining features for a simplified data format.
- 4. Build the Recommendation Model
-- Use **CountVectorizer** to create a **bag-of-words model** for the combined features.
-- Compute similarity between movies using **cosine** similarity.
- 5. Function to Fetch Recommendations
-- Define a function to retrieve the top n similar movies for any given movie based on cosine similarity scores.
- 6. Test the Recommender
-- Test with a sample movie title and receive a list of recommended movies.
## Example
### Sample usage in the notebook
``` bash
recommendations = get_recommendations('The Dark Knight')
print(recommendations)
```
## Contributing
Feel free to open issues or submit pull requests to improve this recommendation system.<br> Contributions are welcome for enhancing model accuracy, adding new features, or improving code readability.

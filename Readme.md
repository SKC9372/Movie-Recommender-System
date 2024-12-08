# Movie Recommender System  

## Introduction  
The **Movie Recommender System** is an application that recommends movies to users based on their previous watch history. This system can be particularly useful for OTT platforms and users by:  
- **For OTT platforms**: Enhancing user engagement and increasing revenue by suggesting relevant movies to users.  
- **For users**: Eliminating the need to search for the next movie to watch by providing personalized recommendations.  

This is a **content-based recommendation system** where movies are suggested based on the content features such as genres, cast, and other descriptive tags.  

---

## Data Acquisition  
The movie data was obtained from the **TMDB API** (The Movie Database), which provides comprehensive datasets and APIs for movie information.  

The data was collected in three chunks:  
1. **Movie Information**: This file included details such as movie titles, likes, budget, popularity, and genres.  
2. **Cast Data**: This file contained information about the movie's cast and credits, including actors and directors.  
3. **Combined Dataset**: Data from both files was merged to create a single dataset for processing.  

---

## Data Processing  
The data processing involved multiple steps to extract meaningful tags for each movie:  
1. **Data Merging**:  
   - The data from different files was merged into a single dataset.  
2. **Feature Extraction**:  
   - **Genres**: Extracted the movie's category, such as Drama, Action, etc.  
   - **Overview**: Extracted a brief description of the movie.  
   - **Cast and Crew**: Extracted names of the main actors and directors.  
3. **Tag Generation**:  
   - Combined all the above features into a single column called `tags`.  
   - Split and processed the `tags` column to extract meaningful words for each movie.  

---

## Vectorization and Embedding  
1. **Word2Vec**:  
   - Used **Word2Vec** to convert each word into a 300-dimensional vector, capturing the semantic meaning of the words.  
2. **Movie Embeddings**:  
   - Created a 300-dimensional embedding for each movie by aggregating the vectors of its associated words (tags).  

---

## Recommendation Mechanism  
The recommendation system calculates the **cosine similarity** between the embeddings of movies.  
- **Cosine Similarity**: Measures how similar two movies are based on their embeddings.  
- **Recommendation Output**: Movies with the highest similarity scores to a given movie are displayed as recommendations.  

For example, if a user selects a movie, the system suggests other movies with similar content and features.

---

## Deployment  
The application was deployed using the following technologies:  
1. **Backend**:  
   - Developed APIs using **Flask** to serve recommendations.  
2. **Frontend**:  
   - Used HTML templates to build a simple and user-friendly interface.  
3. **Demo**:  
   - While the application could not be hosted on free-tier platforms due to its size, a demo video of the application is available for reference.  

---

## Demo Link  
[Demo Video](https://github.com/user-attachments/assets/920a1748-8d78-4773-82bf-db1b5b79bc60
)  

https://github.com/user-attachments/assets/920a1748-8d78-4773-82bf-db1b5b79bc60



---

## Summary  
This project demonstrates a practical implementation of a content-based movie recommendation system that is easy to scale and integrate into OTT platforms. By leveraging natural language processing and word embeddings, the system provides highly relevant movie suggestions, enhancing the user experience and engagement.  

Feel free to explore and provide feedback on the implementation!  

---

### Technologies Used  
- **Programming Language**: Python  
- **Data Processing**: Pandas, NumPy  
- **NLP**: Word2Vec (using Gensim or similar library)  
- **Similarity Calculation**: Cosine Similarity  
- **Backend**: Flask  
- **Frontend**: HTML  

---  

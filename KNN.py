from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import pandas as pd

df = pd.read_csv('BUNA.csv')

model = SentenceTransformer('all-MiniLM-L6-v2')
lyrics_embeddings = model.encode(df['lyrics'].tolist(), show_progress_bar=True)

knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(lyrics_embeddings)


def recommend_similar(song_title, df, lyrics_embeddings, knn_model):
    index = df[df['song'].str.lower() == song_title.lower()].index
    if not len(index):
        return []
    idx = index[0]
    distances, indices = knn_model.kneighbors([lyrics_embeddings[idx]])
    similar_songs = df.iloc[indices[0]][['song', 'artist']
    ]
    return similar_songs.values.tolist()


print(recommend_similar("See you again", df, lyrics_embeddings, knn))
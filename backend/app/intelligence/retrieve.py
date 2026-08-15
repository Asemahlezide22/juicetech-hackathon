"""Find the chunks most relevant to a question.

Deliberately uses TF-IDF and not embeddings: no second API key, no vector
database to provision, no network call, works offline if the venue wifi dies.
Under a few thousand chunks the quality difference does not show up in a demo.

If you later want embeddings, replace search() and keep the signature.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Index:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(chunks)

    def search(self, question: str, top_k: int = 5) -> list[str]:
        query = self.vectorizer.transform([question])
        scores = cosine_similarity(query, self.matrix)[0]
        best = scores.argsort()[::-1][:top_k]
        return [self.chunks[i] for i in best if scores[i] > 0]

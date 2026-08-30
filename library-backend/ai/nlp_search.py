import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))

class NLPSearch:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._corpus = []
        self._book_ids = []
        self._matrix = None

    def _build_corpus(self, books):
        corpus = []
        ids = []
        for b in books:
            text = " ".join(filter(None, [b.title, b.author, b.genre, b.description or ""]))
            corpus.append(text.lower())
            ids.append(b.book_id)
        return corpus, ids

    def rebuild_index(self):
        self._matrix = None

    def _ensure_index(self, books):
        if self._matrix is None or len(books) != len(self._book_ids):
            self._corpus, self._book_ids = self._build_corpus(books)
            if self._corpus:
                self._matrix = self.vectorizer.fit_transform(self._corpus)

    def search(self, query, books, top_n=20):
        if not books:
            return []
        self._ensure_index(books)
        query_vec = self.vectorizer.transform([query.lower()])
        scores = cosine_similarity(query_vec, self._matrix).flatten()
        top_indices = scores.argsort()[::-1][:top_n]
        results = []
        book_map = {b.book_id: b for b in books}
        for idx in top_indices:
            score = float(scores[idx])
            if score < 0.01:
                break
            book = book_map.get(self._book_ids[idx])
            if book:
                d = book.to_dict()
                d["relevance_score"] = round(score, 4)
                results.append(d)
        return results

    def similar(self, book_id, books, top_n=8):
        if not books:
            return []
        self._ensure_index(books)
        if book_id not in self._book_ids:
            return []
        idx = self._book_ids.index(book_id)
        scores = cosine_similarity(self._matrix[idx], self._matrix).flatten()
        scores[idx] = 0  # exclude self
        top_indices = scores.argsort()[::-1][:top_n]
        book_map = {b.book_id: b for b in books}
        results = []
        for i in top_indices:
            score = float(scores[i])
            if score < 0.01:
                break
            book = book_map.get(self._book_ids[i])
            if book:
                d = book.to_dict()
                d["similarity_score"] = round(score, 4)
                results.append(d)
        return results

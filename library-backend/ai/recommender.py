import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def recommend(self, user_id, books, ratings, top_n=8):
        if not ratings:
            return self._popular_fallback(books, top_n)

        df = pd.DataFrame([{"user_id": r.user_id, "book_id": r.book_id, "rating": r.rating} for r in ratings])
        user_ratings = df[df["user_id"] == user_id]

        # Fall back to content-based if fewer than 3 ratings
        if len(user_ratings) < 3:
            return self._genre_fallback(user_id, books, ratings, top_n)

        # Build user-book matrix
        matrix = df.pivot_table(index="user_id", columns="book_id", values="rating").fillna(0)

        if user_id not in matrix.index:
            return self._popular_fallback(books, top_n)

        user_vec = matrix.loc[[user_id]].values
        all_vecs = matrix.values
        sims = cosine_similarity(user_vec, all_vecs).flatten()

        # Weighted average of ratings from similar users
        sim_df = pd.DataFrame({"user_id": matrix.index, "similarity": sims})
        sim_df = sim_df[sim_df["user_id"] != user_id].sort_values("similarity", ascending=False).head(10)

        rated_books = set(user_ratings["book_id"].tolist())
        scores = {}
        for _, row in sim_df.iterrows():
            uid = row["user_id"]
            sim = row["similarity"]
            peer_ratings = df[df["user_id"] == uid]
            for _, pr in peer_ratings.iterrows():
                bid = pr["book_id"]
                if bid not in rated_books:
                    scores[bid] = scores.get(bid, 0) + sim * pr["rating"]

        if not scores:
            return self._popular_fallback(books, top_n)

        sorted_books = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        max_score = sorted_books[0][1] if sorted_books else 1
        book_map = {b.book_id: b for b in books}
        results = []
        for bid, score in sorted_books:
            book = book_map.get(bid)
            if book:
                d = book.to_dict()
                d["match_percentage"] = round((score / max_score) * 100, 1)
                results.append(d)
        return results

    def _genre_fallback(self, user_id, books, ratings, top_n):
        df = pd.DataFrame([{"user_id": r.user_id, "book_id": r.book_id, "rating": r.rating} for r in ratings])
        user_ratings = df[df["user_id"] == user_id]
        rated_ids = set(user_ratings["book_id"].tolist())
        book_map = {b.book_id: b for b in books}
        rated_genres = set()
        for bid in rated_ids:
            b = book_map.get(bid)
            if b and b.genre:
                rated_genres.add(b.genre)
        candidates = [b for b in books if b.book_id not in rated_ids and b.genre in rated_genres]
        if not candidates:
            candidates = [b for b in books if b.book_id not in rated_ids]
        results = []
        for b in candidates[:top_n]:
            d = b.to_dict()
            d["match_percentage"] = 70.0
            results.append(d)
        return results

    def _popular_fallback(self, books, top_n):
        results = []
        for b in books[:top_n]:
            d = b.to_dict()
            d["match_percentage"] = 50.0
            results.append(d)
        return results

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DemandPredictor:
    def forecast(self, transactions, books, top_n=10):
        if not transactions:
            return []

        records = [
            {
                "book_id": t.book_id,
                "year": t.issue_date.year,
                "month": t.issue_date.month,
            }
            for t in transactions if t.issue_date
        ]
        if not records:
            return []

        df = pd.DataFrame(records)
        df["period"] = df["year"] * 12 + df["month"]
        monthly = df.groupby(["book_id", "period"]).size().reset_index(name="count")

        book_map = {b.book_id: b for b in books}
        scores = {}

        for book_id, group in monthly.groupby("book_id"):
            group = group.sort_values("period")
            if len(group) < 2:
                scores[book_id] = group["count"].mean()
                continue
            X = group["period"].values.reshape(-1, 1)
            y = group["count"].values
            model = LinearRegression().fit(X, y)
            next_period = group["period"].max() + 1
            predicted = model.predict([[next_period]])[0]
            scores[book_id] = max(0, predicted)

        sorted_books = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        max_score = sorted_books[0][1] if sorted_books and sorted_books[0][1] > 0 else 1

        results = []
        for bid, score in sorted_books:
            book = book_map.get(bid)
            if book:
                d = book.to_dict()
                d["predicted_demand"] = round(float(score), 2)
                d["demand_percentage"] = round((score / max_score) * 100, 1)
                results.append(d)
        return results

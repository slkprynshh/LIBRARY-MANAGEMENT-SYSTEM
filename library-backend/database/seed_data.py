import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from extensions import db
from models.user import User
from models.book import Book
from models.transaction import Transaction
from models.fine import Fine
from models.rating import BookRating
from datetime import date, timedelta, datetime
import bcrypt

def hash_pw(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

AVT = "http://localhost:3000/assets/images/avatars/"

USERS = [
    {"name": "Admin User",      "email": "admin@library.com",     "password": "admin123",   "role": "admin",     "department": None,               "phone": "9000000001", "profile_pic": f"{AVT}admin.svg"},
    {"name": "Librarian Priya", "email": "librarian@library.com", "password": "lib123",     "role": "librarian", "department": None,               "phone": "9000000002", "profile_pic": f"{AVT}librarian.svg"},
    {"name": "Rahul Sharma",    "email": "rahul@student.com",     "password": "student123", "role": "student",   "department": "Computer Science", "phone": "9000000003", "profile_pic": f"{AVT}rahul.svg"},
    {"name": "Anjali Singh",    "email": "anjali@student.com",    "password": "student123", "role": "student",   "department": "Mathematics",      "phone": "9000000004", "profile_pic": f"{AVT}anjali.svg"},
    {"name": "Vikram Patel",    "email": "vikram@student.com",    "password": "student123", "role": "student",   "department": "Physics",          "phone": "9000000005", "profile_pic": f"{AVT}vikram.svg"},
]

IMG = "http://localhost:3000/assets/images/covers/"

BOOKS = [
    # Fiction
    {"title": "The Alchemist",              "author": "Paulo Coelho",         "isbn": "9780062315007", "genre": "Fiction",      "publisher": "HarperOne",        "year": 1988, "total_copies": 5, "pages": 208,  "cover": f"{IMG}the-alchemist.svg",          "description": "A philosophical novel about a young shepherd's journey to find treasure and his personal legend."},
    {"title": "To Kill a Mockingbird",      "author": "Harper Lee",           "isbn": "9780061935466", "genre": "Fiction",      "publisher": "Harper Perennial", "year": 1960, "total_copies": 4, "pages": 336,  "cover": f"{IMG}to-kill-mockingbird.svg",     "description": "A story of racial injustice and moral growth in the American South through the eyes of a young girl."},
    {"title": "1984",                       "author": "George Orwell",        "isbn": "9780451524935", "genre": "Fiction",      "publisher": "Signet Classic",   "year": 1949, "total_copies": 6, "pages": 328,  "cover": f"{IMG}1984.svg",                   "description": "A dystopian novel about totalitarianism, surveillance, and the destruction of individual freedom."},
    {"title": "The Great Gatsby",           "author": "F. Scott Fitzgerald",  "isbn": "9780743273565", "genre": "Fiction",      "publisher": "Scribner",         "year": 1925, "total_copies": 3, "pages": 180,  "cover": f"{IMG}the-great-gatsby.svg",       "description": "A story of wealth, love, and the American Dream set in the roaring twenties."},
    {"title": "Brave New World",            "author": "Aldous Huxley",        "isbn": "9780060850524", "genre": "Fiction",      "publisher": "Harper Perennial", "year": 1932, "total_copies": 4, "pages": 311,  "cover": f"{IMG}brave-new-world.svg",        "description": "A dystopian novel depicting a future society controlled by technology and conditioning."},
    # Science
    {"title": "A Brief History of Time",    "author": "Stephen Hawking",      "isbn": "9780553380163", "genre": "Science",      "publisher": "Bantam Books",     "year": 1988, "total_copies": 5, "pages": 212,  "cover": f"{IMG}brief-history-time.svg",     "description": "An exploration of cosmology, black holes, the Big Bang, and the nature of time and space."},
    {"title": "The Selfish Gene",           "author": "Richard Dawkins",      "isbn": "9780198788607", "genre": "Science",      "publisher": "Oxford UP",        "year": 1976, "total_copies": 3, "pages": 360,  "cover": f"{IMG}selfish-gene.svg",           "description": "A groundbreaking book on evolutionary biology and the gene-centered view of evolution."},
    {"title": "Cosmos",                     "author": "Carl Sagan",           "isbn": "9780345539434", "genre": "Science",      "publisher": "Ballantine Books", "year": 1980, "total_copies": 4, "pages": 365,  "cover": f"{IMG}cosmos.svg",                 "description": "A journey through the universe exploring astronomy, evolution, and the origin of life."},
    {"title": "The Origin of Species",      "author": "Charles Darwin",       "isbn": "9780140432053", "genre": "Science",      "publisher": "Penguin Classics", "year": 1859, "total_copies": 3, "pages": 432,  "cover": f"{IMG}origin-of-species.svg",      "description": "Darwin's foundational work on natural selection and the evolution of species."},
    {"title": "Astrophysics for People in a Hurry", "author": "Neil deGrasse Tyson", "isbn": "9780393609394", "genre": "Science", "publisher": "Norton", "year": 2017, "total_copies": 5, "pages": 224, "cover": f"{IMG}astrophysics-hurry.svg", "description": "A concise guide to the universe's greatest mysteries for the curious non-scientist."},
    # Technology
    {"title": "Clean Code",                 "author": "Robert C. Martin",     "isbn": "9780132350884", "genre": "Technology",   "publisher": "Prentice Hall",    "year": 2008, "total_copies": 6, "pages": 431,  "cover": f"{IMG}clean-code.svg",             "description": "A handbook of agile software craftsmanship covering best practices for writing clean, maintainable code."},
    {"title": "The Pragmatic Programmer",   "author": "Andrew Hunt",          "isbn": "9780135957059", "genre": "Technology",   "publisher": "Addison-Wesley",   "year": 1999, "total_copies": 4, "pages": 352,  "cover": f"{IMG}pragmatic-programmer.svg",   "description": "Practical advice for software developers on becoming more effective and efficient programmers."},
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen",     "isbn": "9780262033848", "genre": "Technology",   "publisher": "MIT Press",        "year": 2009, "total_copies": 5, "pages": 1292, "cover": f"{IMG}intro-algorithms.svg",       "description": "A comprehensive textbook covering a broad range of algorithms in depth with rigorous analysis."},
    {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "isbn": "9780134610993", "genre": "Technology", "publisher": "Pearson", "year": 2020, "total_copies": 4, "pages": 1132, "cover": f"{IMG}ai-modern-approach.svg", "description": "The leading textbook on AI covering search, knowledge, planning, learning, and perception."},
    {"title": "Deep Learning",              "author": "Ian Goodfellow",       "isbn": "9780262035613", "genre": "Technology",   "publisher": "MIT Press",        "year": 2016, "total_copies": 3, "pages": 800,  "cover": f"{IMG}deep-learning.svg",          "description": "A comprehensive introduction to deep learning covering neural networks, optimization, and applications."},
    # History
    {"title": "Sapiens",                    "author": "Yuval Noah Harari",    "isbn": "9780062316097", "genre": "History",      "publisher": "Harper",           "year": 2011, "total_copies": 6, "pages": 443,  "cover": f"{IMG}sapiens.svg",                "description": "A brief history of humankind from the Stone Age to the modern era covering biology, culture, and economics."},
    {"title": "Guns, Germs, and Steel",     "author": "Jared Diamond",        "isbn": "9780393317558", "genre": "History",      "publisher": "Norton",           "year": 1997, "total_copies": 4, "pages": 480,  "cover": f"{IMG}guns-germs-steel.svg",       "description": "An exploration of why some civilizations came to dominate others through geography and environment."},
    {"title": "The Silk Roads",             "author": "Peter Frankopan",      "isbn": "9781101912379", "genre": "History",      "publisher": "Vintage",          "year": 2015, "total_copies": 3, "pages": 672,  "cover": f"{IMG}silk-roads.svg",             "description": "A new history of the world centered on the trade routes connecting East and West."},
    {"title": "A People's History of the United States", "author": "Howard Zinn", "isbn": "9780062397348", "genre": "History", "publisher": "Harper", "year": 1980, "total_copies": 3, "pages": 729, "cover": f"{IMG}peoples-history-us.svg", "description": "American history told from the perspective of ordinary people, minorities, and the oppressed."},
    {"title": "The Diary of a Young Girl",  "author": "Anne Frank",           "isbn": "9780553296983", "genre": "History",      "publisher": "Bantam Books",     "year": 1947, "total_copies": 5, "pages": 283,  "cover": f"{IMG}diary-young-girl.svg",       "description": "The diary of a Jewish girl hiding from the Nazis during World War II in Amsterdam."},
    # Mathematics
    {"title": "Fermat's Last Theorem",      "author": "Simon Singh",          "isbn": "9781857025217", "genre": "Mathematics",  "publisher": "Fourth Estate",    "year": 1997, "total_copies": 3, "pages": 362,  "cover": f"{IMG}fermats-last-theorem.svg",   "description": "The story of the 350-year quest to prove Fermat's Last Theorem and the mathematician who solved it."},
    {"title": "The Man Who Knew Infinity",  "author": "Robert Kanigel",       "isbn": "9780671750220", "genre": "Mathematics",  "publisher": "Washington Square", "year": 1991, "total_copies": 3, "pages": 464,  "cover": f"{IMG}man-knew-infinity.svg",      "description": "The biography of Srinivasa Ramanujan, the self-taught Indian mathematical genius."},
    {"title": "How to Solve It",            "author": "George Polya",         "isbn": "9780691164076", "genre": "Mathematics",  "publisher": "Princeton UP",     "year": 1945, "total_copies": 4, "pages": 288,  "cover": f"{IMG}how-to-solve-it.svg",        "description": "A guide to mathematical problem-solving methods applicable to any field of study."},
    {"title": "Gödel, Escher, Bach",        "author": "Douglas Hofstadter",   "isbn": "9780465026562", "genre": "Mathematics",  "publisher": "Basic Books",      "year": 1979, "total_copies": 2, "pages": 777,  "cover": f"{IMG}godel-escher-bach.svg",      "description": "An exploration of consciousness, self-reference, and meaning through mathematics, art, and music."},
    {"title": "The Joy of x",               "author": "Steven Strogatz",      "isbn": "9780544105850", "genre": "Mathematics",  "publisher": "Mariner Books",    "year": 2012, "total_copies": 3, "pages": 336,  "cover": f"{IMG}joy-of-x.svg",               "description": "A guided tour of mathematics from basic arithmetic to calculus, statistics, and beyond."},
    # Literature
    {"title": "Pride and Prejudice",        "author": "Jane Austen",          "isbn": "9780141439518", "genre": "Literature",   "publisher": "Penguin Classics", "year": 1813, "total_copies": 5, "pages": 432,  "cover": f"{IMG}pride-prejudice.svg",        "description": "A romantic novel about manners, marriage, and morality in early 19th-century England."},
    {"title": "Crime and Punishment",       "author": "Fyodor Dostoevsky",    "isbn": "9780140449136", "genre": "Literature",   "publisher": "Penguin Classics", "year": 1866, "total_copies": 4, "pages": 671,  "cover": f"{IMG}crime-punishment.svg",       "description": "A psychological novel about a student who commits murder and struggles with guilt and redemption."},
    {"title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "isbn": "9780060883287", "genre": "Literature", "publisher": "Harper", "year": 1967, "total_copies": 4, "pages": 417, "cover": f"{IMG}hundred-years-solitude.svg", "description": "A multigenerational saga of the Buendía family in the fictional town of Macondo."},
    {"title": "The Brothers Karamazov",     "author": "Fyodor Dostoevsky",    "isbn": "9780374528379", "genre": "Literature",   "publisher": "FSG",              "year": 1880, "total_copies": 3, "pages": 796,  "cover": f"{IMG}brothers-karamazov.svg",     "description": "A philosophical novel exploring faith, doubt, morality, and family through a murder mystery."},
    {"title": "Don Quixote",                "author": "Miguel de Cervantes",  "isbn": "9780060934347", "genre": "Literature",   "publisher": "Ecco",             "year": 1605, "total_copies": 3, "pages": 1072, "cover": f"{IMG}don-quixote.svg",             "description": "The adventures of an idealistic knight-errant and his practical squire in 17th-century Spain."},
]

RATINGS_DATA = [
    (3, 1, 5, "Absolutely life-changing book!"),
    (3, 2, 4, "A classic that everyone should read."),
    (3, 3, 5, "Chilling and relevant even today."),
    (3, 11, 5, "Best programming book I've read."),
    (3, 16, 4, "Fascinating history of humanity."),
    (4, 1, 4, "Beautiful story with deep meaning."),
    (4, 6, 5, "Mind-blowing science writing."),
    (4, 12, 4, "Very practical advice for developers."),
    (4, 17, 5, "Changed how I see history."),
    (4, 21, 4, "Incredible mathematical storytelling."),
    (5, 3, 3, "Good but very dark."),
    (5, 7, 5, "Dawkins at his best."),
    (5, 13, 4, "Dense but worth it for CS students."),
    (5, 26, 5, "Austen is timeless."),
    (5, 27, 4, "Dostoevsky is a genius."),
]

def seed():
    app = create_app()
    with app.app_context():
        if User.query.count() > 0:
            print("Database already seeded. Skipping.")
            return

        # Insert users
        user_objs = []
        for u in USERS:
            user = User(
                name=u["name"], email=u["email"],
                password_hash=hash_pw(u["password"]),
                role=u["role"], department=u.get("department"),
                phone=u["phone"], profile_pic=u.get("profile_pic")
            )
            db.session.add(user)
            user_objs.append(user)
        db.session.commit()
        print(f"Inserted {len(user_objs)} users.")

        # Insert books
        book_objs = []
        for b in BOOKS:
            book = Book(
                title=b["title"], author=b["author"], isbn=b["isbn"],
                genre=b["genre"], publisher=b["publisher"], year=b["year"],
                total_copies=b["total_copies"], available_copies=b["total_copies"],
                pages=b["pages"], description=b["description"],
                cover_image_url=b.get("cover")
            )
            db.session.add(book)
            book_objs.append(book)
        db.session.commit()
        print(f"Inserted {len(book_objs)} books.")

        # Fetch inserted users/books by email/isbn for FK references
        users = {u.email: u for u in User.query.all()}
        books = Book.query.order_by(Book.book_id).all()
        librarian = users["librarian@library.com"]

        today = date.today()
        transactions_data = [
            # (student_email, book_index, issue_offset_days, returned, overdue)
            ("rahul@student.com",  0,  -20, True,  False),
            ("rahul@student.com",  2,  -10, False, False),
            ("rahul@student.com",  10, -30, True,  False),
            ("anjali@student.com", 5,  -25, True,  False),
            ("anjali@student.com", 15, -5,  False, False),
            ("anjali@student.com", 20, -40, True,  True),
            ("vikram@student.com", 6,  -18, True,  False),
            ("vikram@student.com", 12, -8,  False, False),
            ("vikram@student.com", 25, -35, True,  True),
            ("rahul@student.com",  3,  -50, True,  True),
        ]

        txn_objs = []
        for email, book_idx, offset, returned, was_overdue in transactions_data:
            student = users[email]
            book = books[book_idx]
            issue_date = today + timedelta(days=offset)
            due_date = issue_date + timedelta(days=14)
            return_date = None
            fine_amt = 0.0

            if returned:
                return_date = due_date + timedelta(days=5) if was_overdue else due_date - timedelta(days=2)
                if was_overdue and return_date > due_date:
                    fine_amt = (return_date - due_date).days * 2.0
            
            status = "returned" if returned else ("overdue" if today > due_date else "issued")

            txn = Transaction(
                user_id=student.user_id, book_id=book.book_id,
                issue_date=issue_date, due_date=due_date,
                return_date=return_date, status=status,
                fine_amount=fine_amt, fine_paid=False,
                issued_by=librarian.user_id
            )
            db.session.add(txn)
            if not returned:
                book.available_copies = max(0, book.available_copies - 1)
            txn_objs.append((txn, fine_amt, student.user_id))
        db.session.commit()
        print(f"Inserted {len(txn_objs)} transactions.")

        # Insert fines for overdue transactions
        fine_count = 0
        for txn, fine_amt, uid in txn_objs:
            if fine_amt > 0:
                paid = fine_count % 2 == 0
                fine = Fine(
                    transaction_id=txn.transaction_id,
                    user_id=uid, amount=fine_amt,
                    paid=paid,
                    paid_at=datetime.utcnow() if paid else None
                )
                db.session.add(fine)
                fine_count += 1
        db.session.commit()
        print(f"Inserted {fine_count} fines.")

        # Insert ratings
        all_users = User.query.order_by(User.user_id).all()
        for user_idx, book_idx, rating_val, review_text in RATINGS_DATA:
            rating = BookRating(
                user_id=all_users[user_idx - 1].user_id,
                book_id=books[book_idx - 1].book_id,
                rating=rating_val, review=review_text
            )
            db.session.add(rating)
        db.session.commit()
        print(f"Inserted {len(RATINGS_DATA)} ratings.")
        print("Seeding complete!")

if __name__ == "__main__":
    seed()

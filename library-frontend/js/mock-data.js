const IMG = 'assets/images/covers/';
const AVT = 'assets/images/avatars/';

const MOCK = {
  currentUser: {
    id: 'STU001', name: 'Priyanshu Solanki', role: 'student',
    dept: 'Computer Science', avatar: `${AVT}rahul.svg`
  },

  stats: { borrowed: 3, available: 1240, fines: 14, dueSoon: 1 },

  borrowedBooks: [
    { id: 'B001', title: 'Clean Code',             author: 'Robert C. Martin', genre: 'Technology', issueDate: '2025-06-15', dueDate: '2025-06-29', status: 'Active' },
    { id: 'B002', title: 'The Pragmatic Programmer',author: 'Andrew Hunt',      genre: 'Technology', issueDate: '2025-06-10', dueDate: '2025-06-24', status: 'Overdue' },
    { id: 'B003', title: 'Sapiens',                 author: 'Yuval Noah Harari',genre: 'History',    issueDate: '2025-06-18', dueDate: '2025-07-02', status: 'Active' },
  ],

  recommendations: [
    { id: 'R001', title: 'Design Patterns',       author: 'Gang of Four',      genre: 'Technology',  match: 95, cover: `${IMG}design-patterns.svg` },
    { id: 'R002', title: 'Atomic Habits',         author: 'James Clear',       genre: 'Self-Help',   match: 91, cover: `${IMG}atomic-habits.svg` },
    { id: 'R003', title: 'Deep Work',             author: 'Cal Newport',       genre: 'Productivity',match: 88, cover: `${IMG}deep-work.svg` },
    { id: 'R004', title: 'The Alchemist',         author: 'Paulo Coelho',      genre: 'Fiction',     match: 84, cover: `${IMG}the-alchemist.svg` },
    { id: 'R005', title: 'Thinking Fast & Slow',  author: 'Daniel Kahneman',   genre: 'Psychology',  match: 82, cover: `${IMG}thinking-fast-slow.svg` },
  ],

  searchBooks: [
    { id: 'S001', title: 'Introduction to Algorithms',        author: 'Cormen et al.',       genre: 'Technology', available: true,  cover: `${IMG}intro-algorithms.svg` },
    { id: 'S002', title: "Harry Potter & the Sorcerer's Stone",author: 'J.K. Rowling',        genre: 'Fiction',    available: true,  cover: `${IMG}harry-potter.svg` },
    { id: 'S003', title: 'A Brief History of Time',           author: 'Stephen Hawking',     genre: 'Science',    available: false, cover: `${IMG}brief-history-time.svg` },
    { id: 'S004', title: 'Sapiens',                           author: 'Yuval Noah Harari',   genre: 'History',    available: true,  cover: `${IMG}sapiens.svg` },
    { id: 'S005', title: 'The Great Gatsby',                  author: 'F. Scott Fitzgerald', genre: 'Fiction',    available: false, cover: `${IMG}the-great-gatsby.svg` },
    { id: 'S006', title: 'Python Crash Course',               author: 'Eric Matthes',        genre: 'Technology', available: true,  cover: `${IMG}python-crash-course.svg` },
    { id: 'S007', title: 'Cosmos',                            author: 'Carl Sagan',          genre: 'Science',    available: true,  cover: `${IMG}cosmos.svg` },
    { id: 'S008', title: 'The Art of War',                    author: 'Sun Tzu',             genre: 'History',    available: true,  cover: `${IMG}art-of-war.svg` },
    { id: 'S009', title: 'Clean Code',                        author: 'Robert C. Martin',    genre: 'Technology', available: true,  cover: `${IMG}clean-code.svg` },
    { id: 'S010', title: '1984',                              author: 'George Orwell',       genre: 'Fiction',    available: true,  cover: `${IMG}1984.svg` },
    { id: 'S011', title: 'Deep Learning',                     author: 'Ian Goodfellow',      genre: 'Technology', available: false, cover: `${IMG}deep-learning.svg` },
    { id: 'S012', title: 'Pride & Prejudice',                 author: 'Jane Austen',         genre: 'Literature', available: true,  cover: `${IMG}pride-prejudice.svg` },
  ],

  adminStats: { totalBooks: 4820, issued: 312, available: 4508, members: 1540, overdue: 47, finesCollected: 9840 },

  recentTransactions: [
    { student: 'Priyanshu Solanki', book: 'Clean Code',              issueDate: '2025-06-15', dueDate: '2025-06-29', status: 'Active' },
    { student: 'Rahul Sharma',      book: 'A Brief History of Time', issueDate: '2025-06-08', dueDate: '2025-06-22', status: 'Overdue' },
    { student: 'Anjali Verma',      book: 'Sapiens',                 issueDate: '2025-06-18', dueDate: '2025-07-02', status: 'Active' },
    { student: 'Karan Mehta',       book: 'The Alchemist',           issueDate: '2025-06-01', dueDate: '2025-06-15', status: 'Returned' },
    { student: 'Sneha Patel',       book: 'Atomic Habits',           issueDate: '2025-06-12', dueDate: '2025-06-26', status: 'Active' },
  ],

  topBooks: [
    { rank: 1, title: 'Clean Code',           borrows: 48, cover: `${IMG}clean-code.svg` },
    { rank: 2, title: 'Atomic Habits',        borrows: 41, cover: `${IMG}atomic-habits.svg` },
    { rank: 3, title: 'Sapiens',              borrows: 37, cover: `${IMG}sapiens.svg` },
    { rank: 4, title: 'The Alchemist',        borrows: 33, cover: `${IMG}the-alchemist.svg` },
    { rank: 5, title: 'Python Crash Course',  borrows: 29, cover: `${IMG}python-crash-course.svg` },
  ],

  manageBooks: [
    { id: 'LIB001', title: 'Clean Code',              author: 'Robert C. Martin',    genre: 'Technology', isbn: '978-0132350884', total: 5, available: 3, cover: `${IMG}clean-code.svg` },
    { id: 'LIB002', title: 'Sapiens',                 author: 'Yuval Noah Harari',   genre: 'History',    isbn: '978-0062316097', total: 4, available: 2, cover: `${IMG}sapiens.svg` },
    { id: 'LIB003', title: 'Atomic Habits',           author: 'James Clear',         genre: 'Self-Help',  isbn: '978-0735211292', total: 6, available: 4, cover: `${IMG}atomic-habits.svg` },
    { id: 'LIB004', title: 'A Brief History of Time', author: 'Stephen Hawking',     genre: 'Science',    isbn: '978-0553380163', total: 3, available: 0, cover: `${IMG}brief-history-time.svg` },
    { id: 'LIB005', title: 'The Great Gatsby',        author: 'F. Scott Fitzgerald', genre: 'Fiction',    isbn: '978-0743273565', total: 4, available: 1, cover: `${IMG}the-great-gatsby.svg` },
    { id: 'LIB006', title: '1984',                    author: 'George Orwell',       genre: 'Fiction',    isbn: '978-0451524935', total: 6, available: 5, cover: `${IMG}1984.svg` },
    { id: 'LIB007', title: 'Deep Learning',           author: 'Ian Goodfellow',      genre: 'Technology', isbn: '978-0262035613', total: 3, available: 1, cover: `${IMG}deep-learning.svg` },
    { id: 'LIB008', title: 'Pride & Prejudice',       author: 'Jane Austen',         genre: 'Literature', isbn: '978-0141439518', total: 5, available: 4, cover: `${IMG}pride-prejudice.svg` },
  ],

  fines: [
    { student: 'Rahul Sharma',  book: 'A Brief History of Time', daysOverdue: 8,  amount: 16, status: 'Unpaid' },
    { student: 'Karan Mehta',   book: 'The Great Gatsby',        daysOverdue: 5,  amount: 10, status: 'Unpaid' },
    { student: 'Meera Joshi',   book: 'Cosmos',                  daysOverdue: 12, amount: 24, status: 'Paid' },
    { student: 'Arjun Singh',   book: 'Python Crash Course',     daysOverdue: 3,  amount: 6,  status: 'Unpaid' },
    { student: 'Priya Nair',    book: 'Sapiens',                 daysOverdue: 7,  amount: 14, status: 'Paid' },
  ],

  chartData: {
    monthly:    { labels: ['Jan','Feb','Mar','Apr','May','Jun'], data: [210,185,240,198,275,312] },
    categories: { labels: ['Technology','Fiction','Science','History','Mathematics','Literature'], data: [35,25,15,12,8,5] }
  }
};

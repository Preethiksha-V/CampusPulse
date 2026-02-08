import sqlite3

conn = sqlite3.connect("campuspulse.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    date TEXT,
    time TEXT,
    venue TEXT,
    description TEXT,
    poster TEXT
)
""")

# Sample data
events = [
    ("Riviera 2026", "Cultural", "2026-03-15", "6:00 PM", "Main Auditorium", "Annual cultural fest", "riviera.jpg"),
    ("AI & ML Hackathon", "Technical", "2026-02-20", "10:00 AM", "TT Building", "24-hour coding challenge", "aihack.jpg"),
    ("Inter-College Football", "Sports", "2026-02-25", "4:00 PM", "Football Ground", "Sports competition", "football.jpg"),
    ("UI/UX Workshop", "Workshop", "2026-02-18", "2:00 PM", "Lab 3", "Hands-on design workshop", "uiux.jpg"),
    ("Data Science VAC", "Value-Added Course", "2026-03-01", "9:00 AM", "Online", "Certification course", "datasci.jpg")
]

cursor.executemany("""
INSERT INTO events (title, category, date, time, venue, description, poster)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", events)

conn.commit()
conn.close()

print("Database created with sample events.")

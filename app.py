from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_events():
    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "category": row[2],
            "date": row[3],
            "time": row[4],
            "venue": row[5],
            "description": row[6],
            "poster": row[7]
        })
    return events


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/home')
def home():
    events = get_events()

    categories = {
        "Culturals": "cultural.jpg",
        "Technical Events": "technical.jpg",
        "Workshops": "workshop.jpg",
        "Value Added Courses": "vac.jpg",
        "Sports": "sports.jpg"
    }

    return render_template("home.html", events=events, categories=categories)



if __name__ == "__main__":
    app.run(debug=True)

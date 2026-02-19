from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

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


# -------------------------------
# Get upcoming events (next 3 days)
# -------------------------------
def get_upcoming_events():
    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()

    today = datetime.now().date()
    next_days = today + timedelta(days=3)

    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()

    upcoming = []

    for row in rows:
        event_date = datetime.strptime(row[3], "%Y-%m-%d").date()
        if today <= event_date <= next_days:
            upcoming.append({
                "id": row[0],
                "title": row[1],
                "category": row[2],
                "date": row[3],
                "time": row[4],
                "venue": row[5],
                "description": row[6],
                "poster": row[7]
            })

    return upcoming


# -------------------------------
# Login page
# -------------------------------
@app.route('/')
def login():
    return render_template("login.html")


# -------------------------------
# Home page
# -------------------------------
@app.route('/home')
def home():
    events = get_events()
    upcoming = get_upcoming_events()

    categories = {
        "Culturals": "cultural.jpg",
        "Technical Events": "technical.jpg",
        "Workshops": "workshop.jpg",
        "Value Added Courses": "vac.jpg",
        "Sports": "sports.jpg"
    }

    return render_template(
        "home.html",
        events=events,
        categories=categories,
        upcoming=upcoming
    )


# -------------------------------
# Category page
# -------------------------------
@app.route('/category/<category_name>')
def category_page(category_name):

    category_map = {
        "Culturals": "Cultural",
        "Technical Events": "Technical",
        "Workshops": "Workshop",
        "Value Added Courses": "Value-Added Course",
        "Sports": "Sports"
    }

    db_category = category_map.get(category_name, category_name)

    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE category = ?", (db_category,))
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

    return render_template("category.html", events=events, category=category_name)


# -------------------------------
# Search route (NEW)
# -------------------------------
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()

    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        title = row[1].lower()
        category = row[2].lower()

        if query in title or query in category:
            results.append({
                "id": row[0],
                "title": row[1],
                "category": row[2],
                "date": row[3],
                "time": row[4],
                "venue": row[5],
                "description": row[6],
                "poster": row[7]
            
            }
            )

    return render_template("search_results.html", events=results, query=query)


# -------------------------------
# Admin panel
# -------------------------------
@app.route('/admin')
def admin():
    events = get_events()
    return render_template("admin.html", events=events)


# Add event
@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    category = request.form['category']
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']
    description = request.form['description']
    poster = request.form['poster']

    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (title, category, date, time, venue, description, poster)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, category, date, time, venue, description, poster))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))


# Delete event
@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))


# Edit event page
@app.route('/edit_event/<int:event_id>')
def edit_event(event_id):
    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()

    event = {
        "id": row[0],
        "title": row[1],
        "category": row[2],
        "date": row[3],
        "time": row[4],
        "venue": row[5],
        "description": row[6],
        "poster": row[7]
    }

    return render_template("edit_event.html", event=event)
@app.route('/my-events')
def my_events():
    return render_template("my_events.html")


# Update event
@app.route('/update_event/<int:event_id>', methods=['POST'])
def update_event(event_id):
    title = request.form['title']
    category = request.form['category']
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']
    description = request.form['description']
    poster = request.form['poster']

    conn = sqlite3.connect("campuspulse.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE events
        SET title=?, category=?, date=?, time=?, venue=?, description=?, poster=?
        WHERE id=?
    """, (title, category, date, time, venue, description, poster, event_id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin'))


# -------------------------------
# Run app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

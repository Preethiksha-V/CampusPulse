from flask import Flask, render_template

app = Flask(__name__)

# Home Page (Default Route)
@app.route('/')
@app.route('/home')
def home():
    events = {
    "featured": [
        {
            "title": "VIT Riviera 2026",
            "date": "2026-03-15",
            "time": "6:00 PM",
            "category": "Cultural"
        },
        {
            "title": "AI & ML Hackathon",
            "date": "2026-02-20",
            "time": "10:00 AM",
            "category": "Technical"
        }
    ],
    "categories": {
        "Culturals": "cultural.jpg",
        "Technical Events": "technical.jpg",
        "Workshops": "workshop.jpg",
        "Value Added Courses": "vac.jpg"
    }
}


    return render_template("home.html", events=events)


if __name__ == "__main__":
    app.run(debug=True)

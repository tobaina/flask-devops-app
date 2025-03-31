import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "messages.db")

def get_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return messages

@app.route("/")
def home():
    messages = get_messages()
    return render_template("index.html", messages=messages)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


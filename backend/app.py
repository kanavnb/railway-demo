from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name TEXT
)
""")

conn.commit()

@app.route("/api/data", methods=["GET"])
def get_data():
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1]
        })

    return jsonify(data)

@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    name = data["name"]

    cur.execute(
        "INSERT INTO items (name) VALUES (%s)",
        (name,)
    )

    conn.commit()

    return jsonify({
        "message": "Added"
    })

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    cur.execute(
        "DELETE FROM items WHERE id = %s",
        (id,)
    )

    conn.commit()

    return jsonify({
        "message": "Deleted"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

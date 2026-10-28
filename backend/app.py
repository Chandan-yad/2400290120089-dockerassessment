
import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

REGNO = os.getenv("REGNO", "2400290120089")
APP_VERSION = os.getenv("APP_VERSION", "0.1")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "festdb")
DB_USER = os.getenv("DB_USER", "festuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "festpass")


# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# Create registrations table if it does not exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# Health API
@app.route("/api/health", methods=["GET"])
def health():
    db_connected = False

    try:
        conn = get_db_connection()
        conn.close()
        db_connected = True
    except Exception:
        pass

    return jsonify({
        "status": "healthy",
        "regno": REGNO,
        "version": APP_VERSION,
        "database": db_connected
    })


# Get all registrations
@app.route("/api/registrations", methods=["GET"])
def get_registrations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email FROM registrations ORDER BY id"
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "email": row[2]
            }
            for row in rows
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add a new registration
@app.route("/api/registrations", methods=["POST"])
def add_registration():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({
            "error": "Name and email are required"
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO registrations (name, email)
            VALUES (%s, %s)
            RETURNING id
            """,
            (data["name"], data["email"])
        )

        registration_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "id": registration_id,
            "name": data["name"],
            "email": data["email"]
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start application
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

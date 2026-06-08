import os
import psycopg
import time

db_url = os.getenv("DATABASE_URL")

print("Connecting to the database...")

for i in range(5):
    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                db_version = cur.fetchone()
                print("\n🎉 Success! Connected to PostgreSQL.")
                print(f"Database version: {db_version[0]}\n")
                break
    except psycopg.OperationalError:
        print("Database not ready yet, waiting 2 seconds...")
        time.sleep(2)
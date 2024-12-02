import os
from psycopg import connect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def query_database():
    try:
        # Get the database URL from .env
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set in .env")

        # Connect to the database
        with connect(database_url) as conn:
            with conn.cursor() as cur:

                cur.execute("DELETE FROM users WHERE userid = 3")
                cur.execute("DELETE FROM \"User\" WHERE id = 4")
    except Exception as e:
        print(f"Error: {e}")

# Run the function
if __name__ == "__main__":
    query_database()
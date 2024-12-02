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
                # Query the User table
                cur.execute("SELECT * FROM \"User\"")
                users = cur.fetchall()
                print("Users in User table:")
                for user in users:
                    print(user)

                # Query the users table
                cur.execute("SELECT * FROM users")
                users_details = cur.fetchall()
                print("\nUsers in users table:\n")
                for user_detail in users_details:
                    print(user_detail)

    except Exception as e:
        print(f"Error: {e}")

# Run the function
if __name__ == "__main__":
    query_database()
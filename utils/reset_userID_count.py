import os
from psycopg import connect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def reset_user_id_sequence():
    try:
        # Get the database URL from .env
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set in .env")
        
        # Connect to the database
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                # Retrieve the current maximum id from the User table
                cur.execute("SELECT MAX(id) FROM \"User\";")
                max_id = cur.fetchone()[0]
                
                # If the table is empty, set the sequence to start at 1
                if max_id is None:
                    max_id = 0  # Assuming sequence starts at 1
                
                # Reset the sequence 'User_id_seq' to the current max id
                cur.execute(f"SELECT setval('User_id_seq', %s, TRUE);", (max_id,))
                
                # Commit the changes
                conn.commit()
                
                print(f"Sequence 'User_id_seq' has been reset to {max_id}.")
    
    except Exception as e:
        print(f"Error resetting user id sequence: {e}")

# Run the function
if __name__ == "__main__":
    reset_user_id_sequence()
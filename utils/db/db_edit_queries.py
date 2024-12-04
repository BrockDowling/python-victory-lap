import os
from psycopg import connect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_schema():
    try:
        # Get the database URL from .env
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set in .env")

        # Connect to the database
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                # Query to list all tables in the current database schema
                cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                if not tables:
                    print("No tables found in the database.")
                    return

                print("Tables and their details in the database:")
                for table in tables:
                    table_name = table[0]
                    print(f"\nTable: {table_name}")

                    # Query to get columns for each table
                    cur.execute("""
                        SELECT column_name, data_type
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position;
                    """, (table_name,))
                    columns = cur.fetchall()
                    if columns:
                        print("  Columns:")
                        for column in columns:
                            column_name, data_type = column
                            print(f"    - {column_name} ({data_type})")
                    else:
                        print("  No columns found.")

                    # Get primary keys
                    cur.execute("""
                        SELECT kc.column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kc ON tc.constraint_name = kc.constraint_name
                        WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';
                    """, (table_name,))
                    pkeys = cur.fetchall()
                    if pkeys:
                        print("  Primary Keys:")
                        for pkey in pkeys:
                            print(f"    - {pkey[0]}")

                    # Get foreign keys
                    cur.execute("""
                        SELECT
                            kcu.column_name AS column_name,
                            ccu.table_name AS referenced_table,
                            ccu.column_name AS referenced_column
                        FROM information_schema.referential_constraints rc
                        JOIN information_schema.key_column_usage kcu ON rc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage ccu ON rc.unique_constraint_name = ccu.constraint_name
                        WHERE kcu.table_name = %s;
                    """, (table_name,))
                    fkeys = cur.fetchall()
                    if fkeys:
                        print("  Foreign Keys:")
                        for fkey in fkeys:
                            print(f"    - {fkey[0]} references {fkey[1]}.{fkey[2]}")

                    # Get unique constraints
                    cur.execute("""
                        SELECT
                            ccu.column_name AS column_name,
                            tc.constraint_name AS constraint_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
                        WHERE tc.table_name = %s AND tc.constraint_type = 'UNIQUE';
                    """, (table_name,))
                    uniques = cur.fetchall()
                    if uniques:
                        print("  Unique Constraints:")
                        for unique in uniques:
                            print(f"    - {unique[1]} on {unique[0]}")

                    # Get check constraints
                    cur.execute("""
                        SELECT
                            cc.check_clause AS check_constraint
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.check_constraints cc ON tc.constraint_name = cc.constraint_name
                        WHERE tc.table_name = %s AND tc.constraint_type = 'CHECK';
                    """, (table_name,))
                    checks = cur.fetchall()
                    if checks:
                        print("  Check Constraints:")
                        for check in checks:
                            print(f"    - {check[0]}")
    except Exception as e:
        print(f"Error: {e}")



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


def get_users_in_db():
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
                cur.execute("SELECT * FROM users")
                users_details = cur.fetchall()

                if not users:
                    print("No users found in User table.")
                else:
                    print("Users in User table:")
                    for user in users:
                        print(user)
                    
                if not users_details:
                    print("No users found in users table.")
                else:
                    print("\nUsers in users table:")
                    for user_detail in users_details:
                        print(user_detail)

    except Exception as e:
        print(f"Error: {e}")


def delete_users():
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


# Uncomment needed tool below to execute

# get_schema()
# reset_user_id_sequence()
get_users_in_db()
# delete_users()
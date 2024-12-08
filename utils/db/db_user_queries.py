# utils/db_utils.py
import bcrypt
import psycopg
from dotenv import load_dotenv
import os
import pandas as pd


# Load environment variables
load_dotenv()


# Connect to the DB
def get_db_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))


# Check if a user exists. If password is provided, also verify credentials.
def check_user_exists(email, password = None):

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if password is None:
            # Just check if email exists
            cur.execute('SELECT EXISTS(SELECT 1 FROM "User" WHERE email = %s)', (email,))
            return cur.fetchone()[0]
        else:
            # Check email and password
            cur.execute('SELECT password FROM "User" WHERE email = %s', (email,))
            result = cur.fetchone()
            if result:
                stored_password = result[0]  # This should be the bcrypt hash as a string
                if stored_password.startswith("\\x"):
                    # If the hash is in hexadecimal format, decode it back to bytes
                    stored_password = stored_password[2:]  # Remove '\\x'
                    stored_password = bytes.fromhex(stored_password)

                # Ensure password is encoded before checking
                return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8') if isinstance(stored_password, str) else stored_password)
            return False
    finally:
        cur.close()
        conn.close()


# Alias for check_user_exists(email) for backwards compatibility
def check_email_exists(email: str) -> bool:

    return check_user_exists(email)


def create_user(firstname, lastname, email, password, gender, weight):
    # First check if email already exists
    if check_email_exists(email):
        raise ValueError("Email already exists")
        
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Insert into User table and get the generated id
        cur.execute(
            'INSERT INTO "User" (email, password) VALUES (%s, %s) RETURNING id',
            (email, hashed_password))
        user_id = cur.fetchone()[0]  # Get the user id after creation

        # Insert into users table, omitting the userid since it is auto-generated
        cur.execute(
            """
            INSERT INTO users (firstname, lastname, gender, weight) 
            VALUES (%s, %s, %s, %s)
            """,
            (firstname, lastname, gender, weight))

        # Commit the transaction
        conn.commit()

        return user_id  # Return the user id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_user_details(email):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Join the "User" and "users" tables based on the user id
        cur.execute(
            """
            SELECT u.userid, u.firstname, u.lastname, u.gender, u.weight
            FROM users u
            JOIN "User" usr ON u.userid = usr.id
            WHERE usr.email = %s
            """,
            (email,)
        )
        user = cur.fetchone()
        
        # If no user is found, return None
        if user is None:
            return None
        
        return user
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return None
    finally:
        cur.close()
        conn.close()


def get_workout_questions(userid):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT workoutname, muscleid, equipmentid, weightused, setschosen, repschosen FROM workoutquestions WHERE userid = %s", (userid,))
        workout_data = cur.fetchall()
    except Exception as e:
        print(f"Error fetching workout data: {e}")
        workout_data = []
    finally:
        cur.close()
        conn.close()
    return workout_data


def get_muscle_groups():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT muscleid, musclename FROM musclegroup")
        muscle_groups = cur.fetchall()
        return muscle_groups
    finally:
        cur.close()
        conn.close()


def get_equipment_list():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT equipmentid, equipmentname FROM equipment")
        equipment = cur.fetchall()
        return equipment
    finally:
        cur.close()
        conn.close()


def insert_workout_data(userid, workout_name, muscle_group, equipment, weight_used, sets, reps):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Fetch muscleid
        cur.execute("SELECT muscleid FROM musclegroup WHERE musclename = %s", (muscle_group,))
        muscleid_row = cur.fetchone()
        if muscleid_row is None:
            return {"success": False, "error": f"No muscleid found for muscle_group: {muscle_group}"}
        
        muscleid = muscleid_row[0]

        # Fetch equipmentid
        cur.execute("SELECT equipmentid FROM equipment WHERE equipmentname = %s", (equipment,))
        equipmentid_row = cur.fetchone()
        if equipmentid_row is None:
            return {"success": False, "error": f"No equipmentid found for equipment: {equipment}"}
        
        equipmentid = equipmentid_row[0]

        # Execute insert statement without the extra workout_score
        cur.execute("""
            INSERT INTO workoutquestions (userid, workoutname, muscleid, equipmentid, weightused, setschosen, repschosen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (userid, workout_name, muscleid, equipmentid, weight_used, sets, reps))
        
        conn.commit()
        return {"success": True, "message": "Workout data inserted successfully."}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cur.close()
        conn.close()


# Function to format workout data
def format_workout_data(workout_data):
    df = pd.DataFrame(workout_data, columns=['workoutname', 'muscleid', 'equipmentid', 'weightused', 'setschosen', 'repschosen'])

    muscle_groups = {mg[0]: mg[1] for mg in get_muscle_groups()}
    equipment_list = {eq[0]: eq[1] for eq in get_equipment_list()}
    
    df['muscle_group'] = df['muscleid'].map(muscle_groups.get)
    df['equipment'] = df['equipmentid'].map(equipment_list.get)
    
    return df

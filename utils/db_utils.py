# utils/db_utils.py
import bcrypt
import psycopg
from datetime import datetime
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Connect to the DB
def get_db_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))


# Verifies user credentials against the database.
def check_user_exists(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT password FROM \"User\" WHERE email = %s", (email,))
        user = cur.fetchone()
        if not user:
            return False
        # Handle different password hash formats
        stored_hash = user[0]
        if isinstance(stored_hash, str) and stored_hash.startswith('\\x'):
            hashed_password = bytes.fromhex(stored_hash[2:])
        else:
            hashed_password = stored_hash if isinstance(stored_hash, bytes) else stored_hash.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False
    
    finally:
        cur.close()
        conn.close()


def create_user(firstname, lastname, email, password, gender, weight):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) FROM "User" WHERE email = %s', (email,))
        if cur.fetchone()[0] > 0:
            raise ValueError("Email already exists")
        cur.execute(
            'INSERT INTO "User" (email, password) VALUES (%s, %s) RETURNING id',
            (email, hashed_password))
        user_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO users (firstname, lastname, gender, weight) VALUES (%s, %s, %s, %s)",
            (firstname, lastname, gender, weight))
        conn.commit()
    except ValueError as v:
        conn.rollback()
        raise v 
    except Exception as e:
        conn.rollback()
        raise e  # Re-raise the exception to be handled by the caller

    finally:
        cur.close()
        conn.close()

def get_user_details(email):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT u.userid, u.firstname, u.lastname, u.gender, u.weight
        FROM users u
        JOIN "User" usr ON u.userid = usr.id  -- Changed to use usr.id instead of usr.userid
        WHERE usr.email = %s
        """,
        (email,)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def get_user_classes(userid):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT classid, dateattended, daysattended FROM userclasses WHERE userid = %s", (userid,))
        class_data = cur.fetchall()
    except Exception as e:
        print(f"Error fetching class data: {e}")
        class_data = []
    finally:
        cur.close()
        conn.close()
    return class_data


def get_workout_questions(userid):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT workoutname, muscleid, equipmentid, weightused, setschosen, repschosen, timelogged FROM workoutquestions WHERE userid = %s", (userid,))
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


def get_class_details():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT classid, classname FROM classes")
        classes = cur.fetchall()
        return classes
    finally:
        cur.close()
        conn.close()


def insert_workout_data(userid, workout_name, muscle_group, equipment, weight_used, sets, reps, workout_duration):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Fetch muscleid
        cur.execute("SELECT muscleid FROM musclegroup WHERE musclename = %s", (muscle_group,))
        muscleid_row = cur.fetchone()
        if muscleid_row is None:
            print(f"No muscleid found for muscle_group: {muscle_group}")
            return
        muscleid = muscleid_row[0]
        
        # Fetch equipmentid
        cur.execute("SELECT equipmentid FROM equipment WHERE equipmentname = %s", (equipment,))
        equipmentid_row = cur.fetchone()
        if equipmentid_row is None:
            print(f"No equipmentid found for equipment: {equipment}")
            return
        equipmentid = equipmentid_row[0]
        
        # Get current timestamp
        current_time = datetime.now()
        
        # Execute insert statement
        cur.execute("""
            INSERT INTO workoutquestions (userid, workoutname, muscleid, equipmentid, weightused, setschosen, repschosen, timelogged, workout_duration)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (userid, workout_name, muscleid, equipmentid, weight_used, sets, reps, current_time, workout_duration))
        conn.commit()
        print("Workout data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting workout data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()
import sqlite3

# The name of our database file
DB_FILE = "voting_system.db"

def get_db_connection():
    """Returns a connection to the SQLite database file."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Creates all required tables if they don't exist yet."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Voters Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voters (
        voter_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        has_voted INTEGER DEFAULT 0
    )""")
    
    # 2. Candidates Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        party TEXT NOT NULL
    )""")
    
    # 3. Votes Table (kept separate for anonymity)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )""")
    
    # 4. Audit Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user TEXT NOT NULL,
        action TEXT NOT NULL
    )""")
    
    conn.commit()
    conn.close()

# --- Helper functions for database operations ---

def add_voter(voter_id, name, email, password_hash, salt):
    """Saves a new voter. Returns True if successful, False if duplicate."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO voters (voter_id, name, email, password_hash, salt) VALUES (?, ?, ?, ?, ?)",
            (voter_id, name, email, password_hash, salt)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_voter(voter_id):
    """Retrieves voter details by voter_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voters WHERE voter_id = ?", (voter_id,))
    voter = cursor.fetchone()
    conn.close()
    return voter

def add_candidate(name, party):
    """Adds a new candidate to the system."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO candidates (name, party) VALUES (?, ?)", (name, party))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_candidates():
    """Returns a list of all candidates."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY name ASC")
    candidates = cursor.fetchall()
    conn.close()
    return candidates

def cast_vote(voter_id, candidate_id):
    """Casts a vote securely inside a database transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN TRANSACTION")
        
        # Mark voter as voted
        cursor.execute("UPDATE voters SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        # Add the anonymous vote
        cursor.execute("INSERT INTO votes (candidate_id) VALUES (?)", (candidate_id,))
        # Log the action
        cursor.execute("INSERT INTO audit_logs (user, action) VALUES (?, ?)", (voter_id, "Cast a vote"))
        
        conn.commit()
        return True, "Vote registered!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def add_audit_log(user, action):
    """Adds an action to the audit logs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audit_logs (user, action) VALUES (?, ?)", (user, action))
    conn.commit()
    conn.close()

# Run initialization when this script is run directly
if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully!")
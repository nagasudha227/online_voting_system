import hashlib
import os
import re
import database

def hash_password(password, salt):
    """Combines a password and salt, then hashes it using SHA-256."""
    salted_password = password + salt
    # encode() converts the string to bytes, and hexdigest() converts the output to text
    return hashlib.sha256(salted_password.encode('utf-8')).hexdigest()

def register_user(voter_id, name, email, password):
    """
    Validates inputs, hashes password, and saves voter to the database.
    Returns: (bool_success, message_string)
    """
    # 1. Simple validation: check if any fields are blank
    if not voter_id or not name or not email or not password:
        return False, "All fields are required!"
    
    # 2. Email format validation using Regular Expressions (Regex)
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return False, "Invalid email address format."
    
    # 3. Generate a random unique salt for this user
    salt = os.urandom(16).hex()
    
    # 4. Hash their password with the salt
    hashed_pw = hash_password(password, salt)
    
    # 5. Save the data to our database (calling database.py)
    success = database.add_voter(voter_id, name, email, hashed_pw, salt)
    if success:
        # Log this action in the database logs
        database.add_audit_log("SYSTEM", f"New voter registered: {voter_id}")
        return True, "Registration successful!"
    else:
        return False, "Voter ID or Email already registered."

def login_user(voter_id, password):
    """
    Checks user credentials.
    Returns: (bool_success, role_or_error_message)
    """
    # 1. Check for Admin Login (For now, we hardcode simple admin credentials)
    if voter_id == "admin" and password == "admin123":
        database.add_audit_log("admin", "Admin logged in")
        return True, "admin"
    
    # 2. Look up the voter in the database
    voter = database.get_voter(voter_id)
    if not voter:
        return False, "Invalid Voter ID."
    
    # 3. Re-hash the typed password with the stored salt
    entered_hash = hash_password(password, voter['salt'])
    
    # 4. Compare the hashes
    if entered_hash == voter['password_hash']:
        # Double check if they have already voted
        if voter['has_voted'] == 1:
            return False, "You have already casted your vote!"
        
        database.add_audit_log(voter_id, "Voter logged in successfully")
        return True, "voter"
    else:
        return False, "Invalid password."
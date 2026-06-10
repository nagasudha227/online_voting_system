import database
import auth

def seed_data():
    print("Initializing database tables...")
    database.initialize_db()
    
    print("Adding mock candidates...")
    candidates = [
        ("Naga Sudha", "Digital Pioneers Party"),
        ("Adithi", "Cyber Security Alliance"),
        ("Akanksha", "Future Developers Front"),
        ("Bindu Shree", "Green AI Coalition")
    ]
    
    for name, party in candidates:
        success = database.add_candidate(name, party)
        if success:
            print(f"Added candidate: {name} ({party})")
        else:
            print(f"Candidate already exists: {name}")

    print("\nRegistering test voters...")
    # Registering multiple test voters with the same password for easy testing
    voters = [
        ("V100", "John Doe", "john@example.com", "password123"),
        ("V101", "Alice Smith", "alice@example.com", "password123"),
        ("V102", "Bob Jones", "bob@example.com", "password123"),
        ("V103", "Emma Watson", "emma@example.com", "password123")
    ]
    for v_id, name, email, pw in voters:
        success, message = auth.register_user(voter_id=v_id, name=name, email=email, password=pw)
        print(f"Voter {v_id} registration status: {message}")
    
    print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
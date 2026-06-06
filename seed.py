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

    print("\nRegistering a test voter...")
    # Registering a test voter using our security logic (Voter ID: V100, Password: password123)
    success, message = auth.register_user(
        voter_id="V100",
        name="John Doe",
        email="john@example.com",
        password="password123"
    )
    print(f"Voter Registration status: {message}")
    
    print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
import customtkinter as ctk
import database
import view

ctk.set_appearance_mode("System")  # Uses Windows Light/Dark theme
ctk.set_default_color_theme("blue")

class VotingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Online Voting System")
        self.geometry("700x650")  # Resized slightly larger for dashboard charts
        
        # Initialize Database tables
        database.initialize_db()
        
        # Start at Login Screen
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()
        self.current_frame = view.LoginFrame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_register_screen(self):
        self.clear_screen()
        self.current_frame = view.RegisterFrame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_voter_dashboard(self, voter_id):
        self.clear_screen()
        self.current_frame = view.VoterFrame(self, voter_id)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_admin_dashboard(self):
        self.clear_screen()
        # Loads our new AdminFrame from view.py
        self.current_frame = view.AdminFrame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = VotingApp()
    app.mainloop()
import customtkinter as ctk
import auth
import database
from tkinter import messagebox  # Built-in popup library

# Matplotlib imports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- DESIGN CONSTANTS (The Styling System) ---
BG_COLOR = "#0F172A"       # Deep Slate Blue/Black (Obsidian)
CARD_COLOR = "#1E293B"     # Dark Slate Grey for Cards/Forms
BORDER_COLOR = "#334155"   # Thin grey border color
ACCENT_BLUE = "#0EA5E9"    # Neon blue for primary buttons
ACCENT_HOVER = "#0284C7"   # Darker blue on hover
TEXT_PRIMARY = "#F8FAFC"   # Warm white
TEXT_MUTED = "#94A3B8"     # Medium grey for subtitles
SUCCESS_GREEN = "#10B981"  # Emerald green
DANGER_RED = "#EF4444"     # Bright red for delete/logout

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR)
        self.parent = parent
        
        # Outer Card Container (Width/Height set inside constructor)
        self.card = ctk.CTkFrame(self, width=380, height=420, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=16)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)  # Prevents children from shrinking the frame size
        
        # Logo Icon Placeholder
        self.logo_label = ctk.CTkLabel(self.card, text="🔒", font=("Arial", 40))
        self.logo_label.pack(pady=(35, 10))
        
        # Titles
        self.title_label = ctk.CTkLabel(self.card, text="Secure Voting", font=("Helvetica", 24, "bold"), text_color=TEXT_PRIMARY)
        self.title_label.pack()
        
        self.sub_label = ctk.CTkLabel(self.card, text="Enter credentials to cast your ballot", font=("Helvetica", 12), text_color=TEXT_MUTED)
        self.sub_label.pack(pady=(0, 25))
        
        # Inputs
        self.id_entry = ctk.CTkEntry(self.card, placeholder_text="Voter ID / Username", width=280, height=40, corner_radius=8, fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.id_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="Password", show="*", width=280, height=40, corner_radius=8, fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.password_entry.pack(pady=10)
        
        # Login Button
        self.login_btn = ctk.CTkButton(self.card, text="Sign In", command=self.handle_login, fg_color=ACCENT_BLUE, hover_color=ACCENT_HOVER, font=("Helvetica", 14, "bold"), height=40, width=280, corner_radius=8)
        self.login_btn.pack(pady=(20, 10))
        
        # Register Switch Button
        self.register_btn = ctk.CTkButton(self.card, text="Create an Account", fg_color="transparent", hover_color=BORDER_COLOR, text_color=ACCENT_BLUE, font=("Helvetica", 12, "bold"), command=lambda: parent.show_register_screen(), width=280)
        self.register_btn.pack(pady=5)

    def handle_login(self):
        voter_id = self.id_entry.get().strip()
        password = self.password_entry.get().strip()
        
        success, result = auth.login_user(voter_id, password)
        
        if success:
            if result == "admin":
                self.parent.show_admin_dashboard()
            else:
                self.parent.show_voter_dashboard(voter_id)
        else:
            error_lbl = ctk.CTkLabel(self.card, text=result, text_color=DANGER_RED, font=("Helvetica", 12, "bold"))
            error_lbl.pack(pady=2)


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR)
        self.parent = parent
        
        # Outer Card Container (Width/Height set inside constructor)
        self.card = ctk.CTkFrame(self, width=400, height=480, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=16)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(self.card, text="Register to Vote", font=("Helvetica", 24, "bold"), text_color=TEXT_PRIMARY)
        self.title_label.pack(pady=(30, 5))
        
        self.sub_label = ctk.CTkLabel(self.card, text="All details are stored securely", font=("Helvetica", 12), text_color=TEXT_MUTED)
        self.sub_label.pack(pady=(0, 20))
        
        # Inputs
        self.id_entry = ctk.CTkEntry(self.card, placeholder_text="Create Voter ID", width=300, height=36, fg_color=BG_COLOR, border_color=BORDER_COLOR, corner_radius=8)
        self.id_entry.pack(pady=6)
        
        self.name_entry = ctk.CTkEntry(self.card, placeholder_text="Full Name", width=300, height=36, fg_color=BG_COLOR, border_color=BORDER_COLOR, corner_radius=8)
        self.name_entry.pack(pady=6)
        
        self.email_entry = ctk.CTkEntry(self.card, placeholder_text="Email Address", width=300, height=36, fg_color=BG_COLOR, border_color=BORDER_COLOR, corner_radius=8)
        self.email_entry.pack(pady=6)
        
        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="Create Password", show="*", width=300, height=36, fg_color=BG_COLOR, border_color=BORDER_COLOR, corner_radius=8)
        self.password_entry.pack(pady=6)
        
        # Submit Button
        self.register_btn = ctk.CTkButton(self.card, text="Register", command=self.handle_register, fg_color=ACCENT_BLUE, hover_color=ACCENT_HOVER, font=("Helvetica", 14, "bold"), height=40, width=300, corner_radius=8)
        self.register_btn.pack(pady=(20, 10))
        
        # Back Button
        self.back_btn = ctk.CTkButton(self.card, text="Back to Login", fg_color="transparent", hover_color=BORDER_COLOR, text_color=TEXT_MUTED, font=("Helvetica", 12, "bold"), command=lambda: parent.show_login_screen(), width=300)
        self.back_btn.pack(pady=5)

    def handle_register(self):
        v_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        pw = self.password_entry.get().strip()
        
        success, message = auth.register_user(v_id, name, email, pw)
        
        lbl = ctk.CTkLabel(self.card, text=message, text_color=SUCCESS_GREEN if success else DANGER_RED, font=("Helvetica", 12, "bold"))
        lbl.pack(pady=2)


class VoterFrame(ctk.CTkFrame):
    def __init__(self, parent, voter_id):
        super().__init__(parent, fg_color=BG_COLOR)
        self.parent = parent
        self.voter_id = voter_id
        
        # Header bar
        self.header_frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, height=70, corner_radius=0, border_width=1, border_color=BORDER_COLOR)
        self.header_frame.pack(fill="x", side="top")
        
        self.welcome_lbl = ctk.CTkLabel(self.header_frame, text=f"🗳️  Active Ballot  |  Voter ID: {self.voter_id}", font=("Helvetica", 16, "bold"), text_color=TEXT_PRIMARY)
        self.welcome_lbl.pack(side="left", padx=30, pady=20)
        
        self.logout_btn = ctk.CTkButton(self.header_frame, text="Sign Out", fg_color=DANGER_RED, hover_color="#C0392B", width=90, font=("Helvetica", 12, "bold"), command=lambda: parent.show_login_screen())
        self.logout_btn.pack(side="right", padx=30, pady=20)
        
        # Main Layout container
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.inst_lbl = ctk.CTkLabel(self.main_content, text="Select a candidate to cast your official vote. You can only vote once.", font=("Helvetica", 14), text_color=TEXT_MUTED)
        self.inst_lbl.pack(anchor="w", pady=(10, 15))
        
        # Scrollable Ballot
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_content, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=12)
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.load_candidates()

    def load_candidates(self):
        candidates = database.get_all_candidates()
        
        if not candidates:
            no_cand_lbl = ctk.CTkLabel(self.scroll_frame, text="No active candidates registered in this election.", font=("Helvetica", 14, "italic"), text_color=TEXT_MUTED)
            no_cand_lbl.pack(pady=40)
            return
        
        for c in candidates:
            # Card Container
            card = ctk.CTkFrame(self.scroll_frame, fg_color=BG_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=10)
            card.pack(fill="x", padx=15, pady=8)
            
            # Badge Symbol/Icon
            badge = ctk.CTkLabel(card, text="👤", font=("Arial", 22))
            badge.pack(side="left", padx=(20, 10), pady=15)
            
            # Text information
            text_container = ctk.CTkFrame(card, fg_color="transparent")
            text_container.pack(side="left", fill="both", expand=True, pady=10)
            
            name_lbl = ctk.CTkLabel(text_container, text=c['name'], font=("Helvetica", 15, "bold"), text_color=TEXT_PRIMARY, anchor="w")
            name_lbl.pack(fill="x")
            
            party_lbl = ctk.CTkLabel(text_container, text=c['party'].upper(), font=("Helvetica", 11, "bold"), text_color=ACCENT_BLUE, anchor="w")
            party_lbl.pack(fill="x")
            
            # Vote Action button
            vote_btn = ctk.CTkButton(
                card, 
                text="Vote", 
                fg_color=ACCENT_BLUE, 
                hover_color=ACCENT_HOVER, 
                width=100, 
                font=("Helvetica", 13, "bold"), 
                corner_radius=6,
                command=lambda cid=c['id'], cname=c['name']: self.confirm_vote(cid, cname)
            )
            vote_btn.pack(side="right", padx=20, pady=15)

    def confirm_vote(self, candidate_id, candidate_name):
        confirm = messagebox.askyesno(
            "Confirm Vote", 
            f"Are you sure you want to vote for {candidate_name}?\n\nThis action cannot be undone."
        )
        
        if confirm:
            success, message = database.cast_vote(self.voter_id, candidate_id)
            if success:
                messagebox.showinfo("Success", "Your vote has been cast successfully! You will now be logged out.")
                self.parent.show_login_screen()
            else:
                messagebox.showerror("Error", f"Failed to vote: {message}")


class AdminFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR)
        self.parent = parent
        
        # Sidebar Navigation container (Premium Layout style)
        self.sidebar = ctk.CTkFrame(self, fg_color=CARD_COLOR, width=200, corner_radius=0, border_width=1, border_color=BORDER_COLOR)
        self.sidebar.pack(fill="y", side="left")
        
        # App logo in sidebar
        self.logo_lbl = ctk.CTkLabel(self.sidebar, text="🛡️ Admin panel", font=("Helvetica", 18, "bold"), text_color=TEXT_PRIMARY)
        self.logo_lbl.pack(pady=30, padx=20)
        
        # Navigation Buttons
        self.btn_candidates = ctk.CTkButton(self.sidebar, text="Candidates", fg_color="transparent", text_color=TEXT_PRIMARY, font=("Helvetica", 13, "bold"), anchor="w", height=40, corner_radius=6, command=self.show_candidates)
        self.btn_candidates.pack(fill="x", padx=10, pady=5)
        
        self.btn_results = ctk.CTkButton(self.sidebar, text="Live Results", fg_color="transparent", text_color=TEXT_PRIMARY, font=("Helvetica", 13, "bold"), anchor="w", height=40, corner_radius=6, command=self.show_results)
        self.btn_results.pack(fill="x", padx=10, pady=5)
        
        self.btn_logs = ctk.CTkButton(self.sidebar, text="System Logs", fg_color="transparent", text_color=TEXT_PRIMARY, font=("Helvetica", 13, "bold"), anchor="w", height=40, corner_radius=6, command=self.show_logs)
        self.btn_logs.pack(fill="x", padx=10, pady=5)
        
        self.btn_utilities = ctk.CTkButton(self.sidebar, text="Database Tools", fg_color="transparent", text_color=TEXT_PRIMARY, font=("Helvetica", 13, "bold"), anchor="w", height=40, corner_radius=6, command=self.show_utilities)
        self.btn_utilities.pack(fill="x", padx=10, pady=5)
        
        # Bottom logout in sidebar
        self.logout_btn = ctk.CTkButton(self.sidebar, text="Sign Out", fg_color=DANGER_RED, hover_color="#C0392B", font=("Helvetica", 12, "bold"), command=lambda: parent.show_login_screen())
        self.logout_btn.pack(side="bottom", fill="x", padx=10, pady=20)
        
        # Main Dashboard view area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Start at Candidates Tab
        self.show_candidates()

    def set_active_nav_button(self, active_btn):
        # Reset colors of all buttons
        for btn in [self.btn_candidates, self.btn_results, self.btn_logs, self.btn_utilities]:
            btn.configure(fg_color="transparent")
        # Highlight active button
        active_btn.configure(fg_color=ACCENT_BLUE)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- TAB 1: Candidates View ---
    def show_candidates(self):
        self.set_active_nav_button(self.btn_candidates)
        self.clear_content_frame()
        
        title = ctk.CTkLabel(self.content_frame, text="Candidate Management", font=("Helvetica", 20, "bold"), text_color=TEXT_PRIMARY)
        title.pack(anchor="w", pady=(10, 5))
        
        sub = ctk.CTkLabel(self.content_frame, text="Add new election candidate profiles or remove active ones", font=("Helvetica", 12), text_color=TEXT_MUTED)
        sub.pack(anchor="w", pady=(0, 20))
        
        # Input form container
        form = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=12)
        form.pack(fill="x", pady=(0, 15))
        
        self.name_entry = ctk.CTkEntry(form, placeholder_text="Candidate Name", width=160, fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.name_entry.pack(side="left", padx=15, pady=15)
        
        self.party_entry = ctk.CTkEntry(form, placeholder_text="Party Name", width=160, fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.party_entry.pack(side="left", padx=15, pady=15)
        
        add_btn = ctk.CTkButton(form, text="Add Candidate", fg_color=ACCENT_BLUE, hover_color=ACCENT_HOVER, font=("Helvetica", 13, "bold"), command=self.handle_add_candidate)
        add_btn.pack(side="left", padx=15, pady=15)
        
        # Scrollable candidates list container
        self.list_scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=12)
        self.list_scroll.pack(fill="both", expand=True)
        
        self.refresh_candidate_list()

    def refresh_candidate_list(self):
        for widget in self.list_scroll.winfo_children():
            widget.destroy()
            
        candidates = database.get_all_candidates()
        
        if not candidates:
            lbl = ctk.CTkLabel(self.list_scroll, text="No candidates registered.", font=("Helvetica", 13, "italic"), text_color=TEXT_MUTED)
            lbl.pack(pady=30)
            return
            
        for c in candidates:
            card = ctk.CTkFrame(self.list_scroll, fg_color=BG_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=8)
            card.pack(fill="x", padx=10, pady=5)
            
            lbl = ctk.CTkLabel(card, text=f"{c['name']}  ({c['party'].upper()})", font=("Helvetica", 13, "bold"), text_color=TEXT_PRIMARY)
            lbl.pack(side="left", padx=15, pady=10)
            
            del_btn = ctk.CTkButton(card, text="Delete", fg_color=DANGER_RED, hover_color="#C0392B", font=("Helvetica", 11, "bold"), width=70, command=lambda cid=c['id']: self.handle_delete_candidate(cid))
            del_btn.pack(side="right", padx=15, pady=10)

    def handle_add_candidate(self):
        name = self.name_entry.get().strip()
        party = self.party_entry.get().strip()
        if not name or not party:
            messagebox.showwarning("Warning", "All fields are required!")
            return
            
        if database.add_candidate(name, party):
            messagebox.showinfo("Success", f"Candidate '{name}' successfully registered.")
            self.name_entry.delete(0, 'end')
            self.party_entry.delete(0, 'end')
            self.refresh_candidate_list()
            database.add_audit_log("admin", f"Added candidate: {name} ({party})")
        else:
            messagebox.showerror("Error", "Candidate already exists!")

    def handle_delete_candidate(self, candidate_id):
        database.delete_candidate(candidate_id)
        self.refresh_candidate_list()
        database.add_audit_log("admin", f"Deleted candidate ID: {candidate_id}")

    # --- TAB 2: Live Results Chart ---
    def show_results(self):
        self.set_active_nav_button(self.btn_results)
        self.clear_content_frame()
        
        title = ctk.CTkLabel(self.content_frame, text="Live Election Results", font=("Helvetica", 20, "bold"), text_color=TEXT_PRIMARY)
        title.pack(anchor="w", pady=(10, 5))
        
        sub = ctk.CTkLabel(self.content_frame, text="Real-time graphical vote count representation", font=("Helvetica", 12), text_color=TEXT_MUTED)
        sub.pack(anchor="w", pady=(0, 20))
        
        self.chart_card = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=12)
        self.chart_card.pack(fill="both", expand=True)
        
        self.canvas = None
        self.update_results_chart()

    def update_results_chart(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        results = database.get_election_results()
        
        # Only show candidates with at least 1 vote in the pie chart to avoid overlapping text
        filtered_results = [r for r in results if r['vote_count'] > 0]
        total_votes = sum(r['vote_count'] for r in results)
        
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Styles to match dark obsidian theme
        fig.patch.set_facecolor(CARD_COLOR)
        ax.set_facecolor(CARD_COLOR)
        
        if total_votes == 0 or not filtered_results:
            ax.text(0.5, 0.5, "No votes casted yet.\nVisual chart will display once voting starts.", 
                    horizontalalignment='center', verticalalignment='center', 
                    fontsize=12, color=TEXT_MUTED, weight='bold')
            ax.axis('off')
        else:
            labels = [f"{r['name']}\n({r['party'].upper()})" for r in filtered_results]
            votes = [r['vote_count'] for r in filtered_results]
            
            wedges, texts, autotexts = ax.pie(
                votes, 
                labels=labels, 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=['#0EA5E9', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
                textprops=dict(color="white", fontsize=10)
            )
            # Make sure labels are readable on dark background
            for text in texts:
                text.set_color(TEXT_PRIMARY)
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_weight("bold")
            ax.axis('equal')
            
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_card)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    # --- TAB 3: Audit System Logs ---
    def show_logs(self):
        self.set_active_nav_button(self.btn_logs)
        self.clear_content_frame()
        
        title = ctk.CTkLabel(self.content_frame, text="System Audit Trails", font=("Helvetica", 20, "bold"), text_color=TEXT_PRIMARY)
        title.pack(anchor="w", pady=(10, 5))
        
        sub = ctk.CTkLabel(self.content_frame, text="Security audit logs recording all system actions", font=("Helvetica", 12), text_color=TEXT_MUTED)
        sub.pack(anchor="w", pady=(0, 20))
        
        self.logs_textbox = ctk.CTkTextbox(self.content_frame, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, font=("Consolas", 11), text_color="#A7F3D0")
        self.logs_textbox.pack(fill="both", expand=True, pady=(0, 10))
        
        self.load_logs()

    def load_logs(self):
        logs = database.get_audit_logs()
        self.logs_textbox.configure(state="normal")
        self.logs_textbox.delete("1.0", "end")
        
        log_text = ""
        for log in logs:
            log_text += f"[{log['timestamp']}] USER: {log['user']} - ACTION: {log['action']}\n"
            
        self.logs_textbox.insert("1.0", log_text)
        self.logs_textbox.configure(state="disabled")

    # --- TAB 4: Utilities ---
    def show_utilities(self):
        self.set_active_nav_button(self.btn_utilities)
        self.clear_content_frame()
        
        title = ctk.CTkLabel(self.content_frame, text="Database Tools & Controls", font=("Helvetica", 20, "bold"), text_color=TEXT_PRIMARY)
        title.pack(anchor="w", pady=(10, 5))
        
        sub = ctk.CTkLabel(self.content_frame, text="Elections backup controls and system wipe", font=("Helvetica", 12), text_color=TEXT_MUTED)
        sub.pack(anchor="w", pady=(0, 30))
        
        # Tools Container
        container = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, border_width=1, border_color=BORDER_COLOR, corner_radius=12)
        container.pack(pady=10, padx=50, fill="both")
        
        backup_lbl = ctk.CTkLabel(container, text="Database Backup", font=("Helvetica", 14, "bold"), text_color=TEXT_PRIMARY)
        backup_lbl.pack(pady=(20, 5))
        
        self.backup_btn = ctk.CTkButton(container, text="Generate Backup", fg_color=SUCCESS_GREEN, hover_color="#059669", font=("Helvetica", 13, "bold"), height=38, command=self.handle_backup)
        self.backup_btn.pack(pady=(0, 20), padx=50, fill="x")
        
        reset_lbl = ctk.CTkLabel(container, text="System Election Reset", font=("Helvetica", 14, "bold"), text_color=TEXT_PRIMARY)
        reset_lbl.pack(pady=(10, 5))
        
        self.reset_btn = ctk.CTkButton(container, text="Reset Election", fg_color=DANGER_RED, hover_color="#DC2626", font=("Helvetica", 13, "bold"), height=38, command=self.handle_reset_election)
        self.reset_btn.pack(pady=(0, 20), padx=50, fill="x")

    def handle_backup(self):
        success, message = database.backup_database()
        if success:
            messagebox.showinfo("Backup Success", message)
        else:
            messagebox.showerror("Backup Error", message)

    def handle_reset_election(self):
        confirm = messagebox.askyesno(
            "Wipe Data Warning", 
            "CRITICAL ACTION:\n\nThis will delete all cast votes, reset all voter statuses to 'not voted', and wipe all system logs.\n\nAre you sure you want to completely reset the election data?"
        )
        if confirm:
            if database.reset_election_data():
                messagebox.showinfo("Success", "Election data has been completely reset.")
            else:
                messagebox.showerror("Error", "Reset failed.")
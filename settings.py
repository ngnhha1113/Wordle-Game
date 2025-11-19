import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox


class Settings:
    BG = "#171717"
    SOLVE_METHODS = ["BFS", "DFS", "UCS", "A*"]

    def __init__(self, functions):
        self.functions = functions
        self.root = functions.root

        self.window = tk.Toplevel(self.root)
        self.window.title("Settings")
        self.window.wm_iconbitmap('images/icon.ico')
        self.window.focus_force()

        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.root.attributes('-disabled', True)

        # ==== UI Position ====
        x_co = int(self.functions.width / 2 - (400 / 2)) + self.functions.x_co
        y_co = self.functions.y_co + int(self.functions.height / 2 - (300 / 2))
        self.window.geometry(f"400x300+{x_co}+{y_co}")
        self.window.config(background=self.BG)

        increase = Image.open("images/increase.png").resize((40, 40), Image.Resampling.LANCZOS)
        increase = ImageTk.PhotoImage(increase)
        decrease = Image.open("images/decrease.png").resize((40, 40), Image.Resampling.LANCZOS)
        decrease = ImageTk.PhotoImage(decrease)

        self.length = self.high_score_value = None

        # --------------------------
        # SIZE SETTING
        # --------------------------
        length_frame = tk.Frame(self.window, background=self.BG)
        length_frame.pack(pady=8)

        tk.Label(length_frame, text="Size", background=self.BG,
                 font="cambria 15 bold", fg="#14f41f").grid(row=0, column=0, padx=12)

        btn = tk.Button(length_frame, image=decrease,
                        command=lambda: self.change_value("length", "decrease"),
                        background=self.BG, border=0, cursor="hand2")
        btn.image = decrease
        btn.grid(row=0, column=1)

        self.word_length = tk.Label(length_frame, background=self.BG,
                                    font="cambria 15 bold", fg="white")
        self.word_length.grid(row=0, column=2, padx=15)

        btn = tk.Button(length_frame, image=increase,
                        command=lambda: self.change_value("length", "increase"),
                        background=self.BG, border=0, cursor="hand2")
        btn.image = increase
        btn.grid(row=0, column=3)

        # --------------------------
        # SCORE SETTING
        # --------------------------
        score_frame = tk.Frame(self.window, background=self.BG)
        score_frame.pack()

        tk.Label(score_frame, text="Score", background=self.BG,
                 font="cambria 15 bold", fg="#14f41f").grid(row=0, column=0, padx=10)

        btn = tk.Button(score_frame, image=decrease,
                        command=lambda: self.change_value("score", "decrease"),
                        background=self.BG, border=0, cursor="hand2")
        btn.image = decrease
        btn.grid(row=0, column=1)

        self.high_score = tk.Label(score_frame, background=self.BG,
                                   font="cambria 15 bold", fg="white")
        self.high_score.grid(row=0, column=2, padx=15)

        btn = tk.Button(score_frame, image=increase,
                        command=lambda: self.change_value("score", "increase"),
                        background=self.BG, border=0, cursor="hand2")
        btn.image = increase
        btn.grid(row=0, column=3)

        # ============================================================
        # SOLVE METHOD SETTING
        # ============================================================
        solve_frame = tk.Frame(self.window, background=self.BG)
        solve_frame.pack(pady=15)

        tk.Label(solve_frame, text="Solve Method", background=self.BG,
                 font="cambria 15 bold", fg="#14f41f").grid(row=0, column=0, padx=12)

        self.solve_index = 0  # default BFS

        # Left arrow
        btn = tk.Button(solve_frame, image=decrease,
                        command=self.decrease_solve_method,
                        background=self.BG, border=0, cursor="hand2")
        btn.image = decrease
        btn.grid(row=0, column=1)

        # Label showing selected method
        self.solve_method_label = tk.Label(
            solve_frame, text=self.SOLVE_METHODS[self.solve_index],
            background=self.BG, font="cambria 15 bold", fg="white")
        self.solve_method_label.grid(row=0, column=2, padx=15)

        # Right arrow
        btn = tk.Button(solve_frame, image=increase,
                        command=self.increase_solve_method,
                        background=self.BG, border=0, cursor="hand2")
        btn.image = increase
        btn.grid(row=0, column=3)

        # Load DB
        self.get_current_db()

        # Save button
        self.save_btn = tk.Button(
            self.window, text="Save Settings", command=self.change_db,
            font="lucida 12 bold", bg="black", fg="sky blue", cursor="hand2")
        self.save_btn.pack(pady=10)

    # ============================================================
    # SOLVE METHOD SWITCHING
    # ============================================================
    def increase_solve_method(self):
        self.solve_index = (self.solve_index + 1) % len(self.SOLVE_METHODS)
        self.solve_method_label["text"] = self.SOLVE_METHODS[self.solve_index]

    def decrease_solve_method(self):
        self.solve_index = (self.solve_index - 1) % len(self.SOLVE_METHODS)
        self.solve_method_label["text"] = self.SOLVE_METHODS[self.solve_index]

    # ============================================================
    # DATABASE
    # ============================================================
    def get_current_db(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM info")
        data = cursor.fetchall()

        self.word_length["text"] = self.length = data[0][1]
        self.high_score["text"] = self.high_score_value = data[0][2]

        connection.close()

    def change_db(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        cursor.execute(f"UPDATE info SET word_length={self.length} WHERE id=0")
        cursor.execute(f"UPDATE info SET high_score={self.high_score_value} WHERE id=0")

        connection.commit()
        connection.close()

        # Update solve method in main:
        self.functions.solve_method = self.SOLVE_METHODS[self.solve_index]

        self.functions.get_from_db()
        self.functions.show_buttons()
        self.functions.reset(keypad=True)

        self.root.attributes('-disabled', False)
        self.root.focus_force()
        self.window.destroy()

    # ============================================================
    # UTIL FUNCTIONS
    # ============================================================
    def change_value(self, value=None, change=None):
        if value == "length":
            if change == "decrease" and 3 < self.length <= 6:
                self.length -= 1
            elif change == "increase" and 3 <= self.length < 6:
                self.length += 1
            self.word_length["text"] = self.length

        elif value == "score":
            if change == "increase":
                self.high_score_value += 1
            elif change == "decrease" and self.high_score_value != 0:
                self.high_score_value -= 1
            self.high_score["text"] = self.high_score_value

    def close(self):
        self.window.destroy()
        self.root.focus_force()
        self.root.attributes('-disabled', False)

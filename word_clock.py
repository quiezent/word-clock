import tkinter as tk
import time
import sys

class WordClock(tk.Tk):
    def __init__(self, specified_time=None):
        super().__init__()
        self.title("Word Clock")
        self.geometry("325x435")  # Increased size to accommodate extra dots
        self.configure(bg='black')
        self.letters = []
        self.dots = []  # Store dot labels
        self.word_positions = {}  # Store positions of words dynamically
        self.specified_time = specified_time
        self.setup_ui()
        self.update_clock()  # Start updating the clock

    def setup_ui(self):
        """
        Initializes the UI elements: the word grid and the extra minute dots.
        """
        self.setup_word_grid()
        self.setup_dots()

    def setup_word_grid(self):
        """
        Sets up the word labels in a grid format.
        """
        words = [
            "ITJISESAMPM",
            "ACQUARTERDC",
            "TWENTYFIVEX", 
            "HALFUTENSTO", 
            "PASTTENNINE",
            "ONESIXTHREE",
            "FOURFIVETWO",
            "EIGHTELEVEN",
            "SEVENTWELVE",
            "GRACEOCLOCK"
        ]

        # Define manual word positions to handle multiple occurrences of words
        self.word_positions = {
            "IT": [(0, 0)], "IS": [(0, 3)], "AM": [(0, 7)], "PM": [(0, 9)],
            "A": [(1, 0)], "QUARTER": [(1, 2)],
            "TWENTY": [(2, 0)], "FIVE": [(2, 6), (6, 4)],  # Added back duplicate FIVE position for correct representation
            "HALF": [(3, 0)], "TEN": [(3, 5), (4, 4)],  # Added back duplicate TEN position for correct representation
            "TO": [(3, 8)],
            "PAST": [(4, 0)], "NINE": [(4, 7)],
            "ONE": [(5, 0)], "SIX": [(5, 3)], "THREE": [(5, 6)],
            "FOUR": [(6, 0)], "TWO": [(6, 8)],
            "EIGHT": [(7, 0)], "ELEVEN": [(7, 5)],
            "SEVEN": [(8, 0)], "TWELVE": [(8, 5)],
            "GRACE": [(9, 0)], "OCLOCK": [(9, 5)]
        }

        for i, line in enumerate(words):
            row = []
            for j, char in enumerate(line):
                lbl = tk.Label(self, text=char, font=("Helvetica", 18), fg='grey', bg='black')
                lbl.grid(row=i, column=j, padx=2, pady=2)
                row.append(lbl)
            self.letters.append(row)

    def setup_dots(self):
        """
        Adds four dots at the bottom for extra minutes representation.
        """
        dot_frame = tk.Frame(self, bg='black')
        dot_frame.grid(row=len(self.letters), column=0, columnspan=len(self.letters[0]), pady=10)
        for i in range(4):
            dot = tk.Label(dot_frame, text='●', font=("Helvetica", 18), fg='grey', bg='black')
            dot.grid(row=0, column=i, padx=5)
            self.dots.append(dot)

    def highlight_word(self, word):
        """
        Highlights all instances of the given word using their starting positions from word_positions.
        """
        if word in self.word_positions:
            positions = self.word_positions[word]  # Get all starting positions for the word
            for start_row, start_col in positions:
                for i, char in enumerate(word):
                    # Make sure we stay within the bounds of the grid
                    if start_col + i < len(self.letters[start_row]):
                        lbl = self.letters[start_row][start_col + i]
                        if lbl.cget("text") == char:
                            lbl.configure(fg='white')

    def reset_labels(self):
        """
        Resets all labels and dots to the default grey color.
        """
        for row in self.letters:
            for lbl in row:
                lbl.configure(fg='grey')
        for dot in self.dots:
            dot.configure(fg='grey')

    def get_time_representation(self, hour, minute):
        """
        Returns the words to highlight based on the current hour and minute.
        """
        self.words_to_highlight = []

        # Always add "IT IS" at the beginning if it's exactly on the hour
        if minute == 0:
            self.words_to_highlight.extend(["IT", "IS", "OCLOCK"])  # Highlight "IT IS" and "OCLOCK" for on-the-hour times.

        minute_word_map = {
            range(0, 5): ["OCLOCK"],
            range(5, 10): ["FIVE", "PAST"],
            range(10, 15): ["TEN", "PAST"],
            range(15, 20): ["QUARTER", "PAST"],
            range(20, 25): ["TWENTY", "PAST"],
            range(25, 30): ["TWENTY", "FIVE", "PAST"],
            range(30, 35): ["HALF", "PAST"],
            range(35, 40): ["TWENTY", "FIVE", "TO"],
            range(40, 45): ["TWENTY", "TO"],
            range(45, 50): ["QUARTER", "TO"],
            range(50, 55): ["TEN", "TO"],
            range(55, 60): ["FIVE", "TO"]
        }

        # Determine minute representation
        for minute_range, words in minute_word_map.items():
            if minute in minute_range:
                if minute != 0:  # Only add minute words if minute is not zero
                    self.words_to_highlight = words  # Replace instead of extend to avoid incorrect combinations
                break

        # Determine hour representation
        hour_word_map = {
            1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE",
            6: "SIX", 7: "SEVEN", 8: "EIGHT", 9: "NINE", 10: "TEN",
            11: "ELEVEN", 12: "TWELVE"
        }

        # Adjust hour representation based on whether it is "PAST" or "TO"
        if "TO" in self.words_to_highlight:
            next_hour = (hour % 12) + 1
        else:
            next_hour = hour

        if next_hour == 0:
            next_hour = 12

        # Avoid appending the next hour multiple times
        if hour_word_map[next_hour] not in self.words_to_highlight:
            self.words_to_highlight.append(hour_word_map[next_hour])

        return self.words_to_highlight

    def update_clock(self):
        """
        Updates the word clock to reflect the current time.
        """
        if self.specified_time:
            hour, minute = map(int, self.specified_time.split(':'))
            hour = hour % 12
            if hour == 0:
                hour = 12
        else:
            current_time = time.localtime()
            hour = current_time.tm_hour % 12
            if hour == 0:
                hour = 12
            minute = current_time.tm_min

        # Reset all labels to grey
        self.reset_labels()

        # Get words to highlight based on current time
        words_to_highlight = self.get_time_representation(hour, minute)

        # Highlight the appropriate words
        for word in words_to_highlight:
            self.highlight_word(word)

        # Highlight extra dots to represent additional minutes, if applicable
        extra_minutes = minute % 5
        for i in range(4):
            if i < extra_minutes:
                self.dots[i].configure(fg='white')
            else:
                self.dots[i].configure(fg='grey')

        # Schedule the next update only if no specific time was provided
        if not self.specified_time:
            self.after(1000, self.update_clock)  # Update every second

if __name__ == "__main__":
    specified_time = None
    if len(sys.argv) > 1:
        specified_time = sys.argv[1]

    app = WordClock(specified_time)
    app.mainloop()

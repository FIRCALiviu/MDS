import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np


class BudgetApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.total_bars = 4  # Initialize with the length of initial data
        self.title("Budget Application")
        self.geometry("1200x400")
        self.trend_data = None
        self.theme = "dark"  # Set default theme to dark
        self.update_app_background()

        # Theme toggle button
        self.theme_button = ctk.CTkButton(self, text="Night Mode", command=self.toggle_theme)
        self.theme_button.pack(side="top", padx=20, pady=5, anchor="nw")

        # Chart frame
        self.chart_frame = ctk.CTkFrame(self, width=1000, height=300)
        self.chart_frame.pack(padx=20, pady=20)

        self.chart_frame.grid_propagate(False)
        self.chart_frame.update_idletasks()

        # Canvas for drawing bars
        self.canvas = ctk.CTkCanvas(self.chart_frame, width=1000, height=300, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Update button
        self.update_button = ctk.CTkButton(self, text="Update", command=self.update_data)
        self.update_button.pack(pady=10)

        # Input field
        self.input_field = ctk.CTkEntry(self, width=100,
                                        placeholder_text="bar {number} {value} OR add {column_number} {Note}")
        self.input_field.pack()

        # Error label
        self.error_label = ctk.CTkLabel(
            self, text="", text_color="red", font=("Arial", 12)
        )
        self.error_label.pack(padx=20, pady=5)
        try:
            self.error_label.pack()
        except (AttributeError, ctk.TclError):
            pass
        self.error_label.pack_forget()

        # Initial data
        self.data = [1, 2, 3, 5]
        self.notes = {}

        # Currency flag indicating the current currency type (0 for lei, 1 for euro, 2 for dollars)
        self.currency_flag = 0  # Default to lei

        self.draw_bars()

        # Theme toggle button
        self.set_duration_button = ctk.CTkButton(self, text="Set Budget Duration", command=self.set_budget_duration)
        self.set_duration_button.pack(pady=10)

        # Entry field for budget duration
        self.duration_entry = ctk.CTkEntry(self, width=100, placeholder_text="Days")
        self.duration_entry.pack(pady=5)

        # Button for currency conversion
        self.currency_button = ctk.CTkButton(self, text="Convert", command=self.convert_currency)
        self.currency_button.pack(pady=10)

        # Entry field for currency
        self.currency_entry = ctk.CTkEntry(self, width=100, placeholder_text="Currency (Leu, Euro, Dollar)")
        self.currency_entry.pack(pady=10)

    def update_data(self):
        user_input = self.input_field.get().strip()
        parts = user_input.split(" ")

        if user_input.startswith("add"):
            if len(parts) != 3:
                self.show_error("Invalid note format! Use: add {column_number} {Note}")
                return
            try:
                column_number = int(parts[1]) - 1
                note = parts[2]
            except ValueError:
                self.show_error("Invalid column number or note format!")
                return

            if column_number < 0 or column_number >= len(self.data):
                self.show_error("Invalid column number! Please enter a number between 1 and {}".format(len(self.data)))
                return

            self.notes[column_number] = note
            self.draw_bars()

        elif user_input.startswith("bar"):
            try:
                parts = user_input.split(" ")
                if len(parts) != 3:
                    raise ValueError
                bar_number = int(parts[1]) - 1
                value = int(parts[2])
            except ValueError:
                self.show_error("Invalid input format! Use: bar {number} {value}")
                return

            if bar_number < 0 or bar_number >= len(self.data):
                self.show_error("Invalid bar number! Please enter a number between 1 and {}".format(len(self.data)))
                return

            self.data[bar_number] = value
            self.draw_bars()
        elif user_input.startswith("graph"):
            if len(parts) != 3:
                self.show_error("Invalid graph command format! Use: graph {first_day} {last_day}")
                return
            try:
                first_day = int(parts[1])
                last_day = int(parts[2])
            except ValueError:
                self.show_error("Invalid date range! Please enter integers for days.")
                return
            self.graph(first_day, last_day)
        else:
            self.show_error("Invalid input format!")

    def show_error(self, message):
        self.error_label.configure(text=message)
        try:
            self.error_label.show()
        except AttributeError:
            self.error_label.pack()
        self.after(2000, self.hide_error)

    def hide_error(self):
        self.error_label.configure(text="")
        self.error_label.pack_forget()

    def convert_currency(self):
        # Conversion rates (assuming approximate values)
        conversion_rates = {
            "Leu": 1,
            "Euro": 5,  # 1 EUR ~ 5 RON (approximate)
            "Dollar": 4.3,  # 1 USD ~ 4.3 RON (approximate)
        }

        # Get the selected currency from the input field
        selected_currency = self.currency_entry.get().strip()

        # Check if the selected currency is valid
        if selected_currency not in conversion_rates:
            self.show_error("Invalid currency selected! Please enter either 'Leu', 'Euro', or 'Dollar'.")
            return

        # Calculate the conversion factor based on the selected currency
        conversion_factor = conversion_rates[selected_currency]

        # Check if this is the first conversion
        if self.currency_flag == 0:  # Lei
            # Convert the data to the selected currency
            self.data = [value / conversion_factor for value in self.data]
        elif self.currency_flag == 1:  # Euro
            # Convert the data back to Lei and then to the selected currency
            self.data = [value * conversion_rates["Euro"] / conversion_factor for value in self.data]
        else:  # Dollar
            # Convert the data back to Lei and then to the selected currency
            self.data = [value * conversion_rates["Dollar"] / conversion_factor for value in self.data]

        # Set the new currency flag
        if selected_currency == "Leu":
            self.currency_flag = 0
        elif selected_currency == "Euro":
            self.currency_flag = 1
        else:
            self.currency_flag = 2
        self.draw_bars()

    def draw_bars(self):
        self.canvas.delete("all")
        frame_width = self.chart_frame.winfo_width()
        bar_spacing = 20
        outline_width = 2
        margins = 2 * bar_spacing
        available_width = frame_width - margins
        total_outline_width = self.total_bars * outline_width
        min_bar_width = 10
        bar_width = max(min_bar_width,
                        (available_width - (self.total_bars - 1) * bar_spacing - total_outline_width) / self.total_bars)
        x = bar_spacing
        canvas_bg_color = "#c0c9d1" if self.theme == "light" else "#2c3e50"
        self.canvas.config(bg=canvas_bg_color)

        # Calculate the maximum value based on the selected currency
        max_value = max(v for v in self.data)

        for i, value in enumerate(self.data):
            # Adjust the height of the bars based on the maximum value
            bar_height = (value / max_value) * 200 * 0.7
            y = 300 - bar_height

            bar_colors = ["#2ecc71", "#3498db", "#9b59b6", "#f1c40f"] if self.theme == "light" else ["#34495e",
                                                                                                     "#B05E4C",
                                                                                                     "#95a5a6",
                                                                                                     "#bdc3c7"]
            fill_color = bar_colors[i % len(bar_colors)]
            self.canvas.create_rectangle(
                x, y, x + bar_width, 300, fill=fill_color, outline=canvas_bg_color  # match outline to canvas background color
            )
            if i in self.notes:
                note_text = self.notes[i]
                text_x = x + bar_width // 2
                text_y = y - 10
                self.canvas.create_text(text_x, text_y, text=note_text, anchor="center", font=("Arial", 8),
                                        fill='white' if self.theme == 'dark' else 'black')

            # Add text with the value of the bar
            self.canvas.create_text(x + bar_width / 2, y - 25, text=str(round(value, 2)),
                                    fill='white' if self.theme == 'dark' else 'black')

            x += bar_width + bar_spacing
        if self.trend_data is not None:
            # Plot the trend line on top of the bars
            plt.plot(x, self.trend_data, color="red", linestyle="-")

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.theme_button.configure(text="Light Mode")
            ctk.set_appearance_mode("Dark")
        else:
            self.theme = "light"
            self.theme_button.configure(text="Night Mode")
            ctk.set_appearance_mode("System")
        self.update_app_background()
        self.draw_bars()

    def update_app_background(self):
        if self.theme == "light":
            self.config(bg="#c0c9d1")
        else:
            self.config(bg="#2c3e50")

    def set_budget_duration(self):
        try:
            duration = int(self.duration_entry.get())
            if duration <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Invalid duration! Please enter a positive integer.")
            return

        self.remaining_days = duration
        self.total_bars = duration
        self.data = [1] * self.total_bars
        self.draw_bars()
        self.show_error(f"Budget set for {duration} days. {self.total_bars} bars displayed.")

    def graph(self, first_day, last_day):
        # Validate input for first_day and last_day
        try:
            first_day = int(first_day)
            last_day = int(last_day)
            if first_day < 1 or last_day > self.total_bars or first_day > last_day:
                raise ValueError
        except ValueError:
            self.show_error("Invalid date range! Please enter days between 1 and {}".format(self.total_bars))
            return

        # Extract data for the specified date range
        data_to_plot = self.data[first_day - 1:last_day]
        x = np.arange(first_day, last_day + 1)

        # Calculate the trend line (linear regression)
        m, c = np.polyfit(x, data_to_plot, 1)
        trend_line = m * x + c

        # Store the trend line data
        self.trend_data = trend_line

        # Create a new figure for the trend line
        plt.figure(figsize=(5, 3))
        plt.plot(x, data_to_plot, 'o', label='Budget History')
        plt.plot(x, trend_line, color='red', linestyle='-', label='Trend Line')
        plt.xlabel('Days')
        plt.ylabel('Budget')
        plt.title(f'Budget Trend (Days {first_day} - {last_day})')
        plt.legend()
        plt.grid(True)

        # Show the trend line plot
        plt.show()

        # Clear the trend line data after displaying the plot
        self.trend_data = None


if __name__ == "__main__":
    app = BudgetApplication()
    app.mainloop()

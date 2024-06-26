import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector

class BudgetApplication(ctk.CTk):
    def __init__(self,username,password):
        super().__init__()

        self.get_connection(username,password)

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
        self.chart_frame = ctk.CTkFrame(self, width=1000, height=500)
        self.chart_frame.pack(padx=20, pady=20)

        self.chart_frame.grid_propagate(False)
        self.chart_frame.update_idletasks()

        # Canvas for drawing bars
        self.canvas = ctk.CTkCanvas(self.chart_frame, width=1000, height=300, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        

        

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
        self.currency_flag = "Leu"  # Default to lei

        

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
        
        self.add_note_button = ctk.CTkButton(self, text="Add a note", command=self.add_note_button)
        self.add_note_button.pack(pady = 10)
        self.add_note_entry = ctk.CTkEntry(self, width=100, placeholder_text="{day} {note}")
        self.add_note_entry.pack(pady = 10)
        self.repeat_button = ctk.CTkButton(self, text="Add a repeated purchase", command=self.repeat_button_method)
        self.repeat_button.pack(pady = 10)
        self.repeat_entry = ctk.CTkEntry(self, width=200, placeholder_text="{day it starts} {interval} {sum}")
        self.repeat_entry.pack(pady= 10)
        
        self.bar_set_button = ctk.CTkButton(self, text="Set money left for a day", command=self.bar_set_method)
        self.bar_set_button.pack(pady =10)
        self.bar_set_entry= ctk.CTkEntry(self, width=200, placeholder_text="{day} {money left}")
        self.bar_set_entry.pack(pady= 10)
        
        self.graph_display_button = ctk.CTkButton(self, text="Display trend line for a period", command=self.graph_display_method)
        self.graph_display_button.pack(pady= 10)
        self.graph_display_entry = ctk.CTkEntry(self, width=200, placeholder_text="{first day} {last day}")
        self.graph_display_entry.pack(pady=10)

        self.fetch_data()
        self.draw_bars()
    def graph_display_method(self):
        user_input = self.graph_display_entry.get()
        parts = user_input.split()
        if len(parts) != 2:
                self.show_error("Invalid graph command format! Use: graph {first_day} {last_day}")
                return
        try:
            first_day = int(parts[0])
            last_day = int(parts[1])
        except ValueError:
            self.show_error("Invalid date range! Please enter integers for days.")
            return
        self.graph(first_day, last_day)    
    
    def bar_set_method(self):
        try:
            user_input = self.bar_set_entry.get()
            parts = user_input.split()
            if len(parts) != 2:
                raise ValueError
            bar_number = int(parts[0]) - 1
            value = float(parts[1])
        except ValueError:
            self.show_error("Invalid input format! Use: {number} {value}")
            return

        if bar_number < 0 or bar_number >= len(self.data):
            self.show_error("Invalid bar number! Please enter a number between 1 and {}".format(len(self.data)))
            return

        self.data[bar_number] = value
        self.draw_bars()
    def repeat_button_method(self):
        user_input = self.repeat_entry.get()
        parts = user_input.split()
        try:
            if len(parts) !=3:
                raise ValueError
            parts = user_input.split()
            start_date  = int(parts[0])
            period = int(parts[1])
            cost = float(parts[2])
        except ValueError:
            self.show_error("Invalid input ! use {start_date} {period} {cost}")
            return

        start_date -=1
        if start_date>=0:
            for i in range(start_date,len(self.data),period):
                self.data[i]-=cost
        else:
            self.show_error("Start date must be greater than 1")
        self.draw_bars()
    def add_note_button(self):
        user_input = self.add_note_entry.get()
        parts = user_input.split()

        
        if len(parts) < 2:
            self.show_error("Invalid note format! Use:{column_number} {Note}")
            return
        try:
            column_number = int(parts[0]) - 1
            note = " ".join(parts[1:])
        except ValueError:
            self.show_error("Invalid column number or note format!")
            return

        if column_number < 0 or column_number >= len(self.data):
            self.show_error("Invalid column number! Please enter a number between 1 and {}".format(len(self.data)))
            return

        self.notes[column_number] = note
        self.draw_bars()
    

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
        # formula for the value in the new currency
        # new value =old value* rate new / rate old
        # Calculate the conversion factor based on the selected currency
        conversion_factor =conversion_rates[self.currency_flag]/conversion_rates[selected_currency]
 
        self.data = list(map( lambda x : x*conversion_factor,self.data))

        # Set the new currency flag
        self.currency_flag=selected_currency
        self.draw_bars()

    def draw_bars(self):
        self.canvas.delete("all")
        frame_width = self.chart_frame.winfo_width()
        frame_height = self.chart_frame.winfo_height()  # Get the height of the chart frame
        padding = 50  # Define padding at the top and bottom
        canvas_height = frame_height if frame_height > 0 else 600  # Default to 600 if frame_height is not properly obtained
        self.canvas.config(height=canvas_height)
        
        bar_spacing = 6
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

        # Calculate the maximum absolute value based on the data
        max_value = max(abs(v) for v in self.data)
        if max_value == 0:
            max_value = 1

        y_base = canvas_height / 2  # Adjust the base y coordinate to the middle of the canvas

        for i, value in enumerate(self.data):
            # Adjust the height of the bars based on the maximum value
            bar_height = (abs(value) / max_value) * (canvas_height / 2 - padding) * 0.7
            if value >= 0:
                y_top = y_base - bar_height
                y_bottom = y_base
            else:
                y_top = y_base
                y_bottom = y_base + bar_height


            bar_colors = ["#2ecc71", "#3498db", "#9b59b6", "#f1c40f"] if self.theme == "light" else ["#34495e",
                                                                                                    "#B05E4C",
                                                                                                    "#95a5a6",
                                                                                                    "#bdc3c7"]
            fill_color = bar_colors[i % len(bar_colors)]
            self.canvas.create_rectangle(
                x, y_top, x + bar_width, y_bottom, fill=fill_color, outline=canvas_bg_color  # match outline to canvas background color
            )
            if i in self.notes:
                note_text = self.notes[i]
                text_x = x + bar_width // 2
                text_y = y_top - 10 if value >= 0 else y_bottom + 10
                self.canvas.create_text(text_x, text_y, text=note_text, anchor="center", font=("Arial", 8),
                                        fill='white' if self.theme == 'dark' else 'black')

            # Add text with the value of the bar
            self.canvas.create_text(x + bar_width / 2, y_top - 25 if value >= 0 else y_bottom + 25, text=str(round(value, 2)),
                                    fill='white' if self.theme == 'dark' else 'black')

            x += bar_width + bar_spacing

        if self.trend_data is not None:
            # Plot the trend line on top of the bars
            plt.plot(x, self.trend_data, color="red")
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
        if m*len(self.data)+c>=0:
            
            plt.title('You will break even according to the best fit line!')
        else:
            plt.title("You won't break even according to the best fit line")
        plt.legend()
        plt.grid(True)
        plt.xlim(0,len(self.data))
        # Show the trend line plot
        plt.show()

        # Clear the trend line data after displaying the plot
        self.trend_data = None
    def get_connection(self,username,password):
        mydb = mysql.connector.connect(
        
        host="localhost",
        user=username,
        password=password,
        database=username+"db"
        )
        self.db = mydb
        
        c =mydb.cursor()
        c.execute(
            """
            create table if not exists valori(

            day INT ,
            value decimal(20,3) not null,
            primary key(day)
            );

            """
        )
        c.execute(
            """
            create table  if not exists notes(
            day INT ,
            note varchar(255) not null,
            primary key(day)

            );

            """
        )
        c.close()
    def update_value(self,day,value,note=None):
        c = self.db.cursor()
        if note is None:
            sql1="""
                delete from valori
                where  day =%s
                """
            
            c.execute(
                sql1,(day,)
            )
            sql2 ="""
                insert into valori
                values(%s,%s)

                """
            
            c.execute(
                sql2,(day,value)
            )
        else:
            sql1="""
                delete from valori
                where  day =%s
                """
            
            c.execute(
                sql1,(day,)
            )
            sql2 ="""
                insert into valori
                values(%s,%s)

                """
            
            c.execute(
                sql2,(day,value)
            )
            sql3 = """
                    delete from notes
                    where  day =%s
                    """
            c.execute(
                sql3,(day,)
            )
            sql4= """
                insert into notes
                values(%s,%s)

                """
            c.execute(
                sql4,(day,note)
            )
        c.close()
        

    def test_update_value(self):
        self.clear_data()
        self.update_value(0,5,"bine")
        self.update_value(1,-90,'string spatiu')
        self.update_value(2,-10**6,'string foarte mmaaaa'+'a'*50+'e')
        self.update_value(3,10**6)
        self.update_value(4,0.5)

        self.fetch_data()
    
        if self.data==[5,-90,-10**6,10**6,0.5] and self.notes=={0:'bine',1:'string spatiu',2:'string foarte mmaaaa'+'a'*50+'e'}:
            print('test 1 passed')
        else:
            print('test 1 failed')

        test2 = [(i,i*i) for i in range(2000)]
        notes = {9:'bineeeeeeeeee',100:'st ahs tahs thas thast'}
        self.clear_data()
        
        for i,val in test2:
            self.update_value(i,val,notes.get(i,None))
        self.fetch_data()
        if self.data==[ val for i,val in test2] and self.notes == notes:
            print("test 2 passed")
        else:
            print('test 2 failed')

        self.clear_data()
        
        self.update_value(0,0.001)
        self.fetch_data()
        if self.data == [0.001] and self.notes=={}:
            print('test 3 passed')
        else:
            print('test 3 failed')
    def fetch_data(self):
        c = self.db.cursor()
        c.execute("select * from valori")
        vec = []    
        for x in c:
            vec.append(x)
        
        c.close()
        c = self.db.cursor()
        c.execute("select * from notes")
        notes ={}
        for day,note in c:
            notes[day] = note
        c.close()
        if vec:
            self.data = [1]*len(vec)
            
            for i,val in vec:
                self.data[i]=float(val)
            self.total_bars = len(vec)
        
            self.notes = notes
    def clear_data(self):
        sql1 ="""
            delete from valori    
            """
        sql2="""
            delete from notes
            """
        c = self.db.cursor()
        c.execute(sql1)
        c.execute(sql2)
        c.close()
    def save_data_exit(self):
        self.clear_data()
        for i,v in enumerate(self.data):
            self.update_value(i,v)
        for i in self.notes:
            self.update_value(i,self.data[i],self.notes[i])
        self.db.commit()
        self.db.close()

    def clear_data(self):
        sql1 ="""
            delete from valori    
            """
        sql2="""
            delete from notes
            """
        c = self.db.cursor()
        c.execute(sql1)
        c.execute(sql2)
        c.close()
if __name__ == "__main__":
    app = BudgetApplication("budgetusertest","password1234")
    app.mainloop()
    #app.test_update_value()
    app.save_data_exit()

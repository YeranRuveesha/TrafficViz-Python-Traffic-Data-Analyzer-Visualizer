import tkinter as tk
import csv

# Task A: Leap year check function
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Validate input function for date (day, month, year)
def validate_in(prompt, value_type, min_value=None, max_value=None):
    while True:
        try:
            user_input = input(prompt)
            value = value_type(user_input)  # Convert input to correct type
            if min_value is not None and value < min_value:
                print(f"Out of range - value must be in the range {min_value} to {max_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Out of range - value must be in the range {min_value} to {max_value}.")
                continue
            return value  # Valid input
        except ValueError:
            print(f"Integer required.")

# Function to get a valid date input from the user
def get_valid_date():
    day = validate_in("Please enter the day of the survey in the format dd: ", int, 1, 31)
    month = validate_in("Please enter the month of the survey in the format MM: ", int, 1, 12)
    year = validate_in("Please enter the year of the survey in the format YYYY: ", int, 2000, 2024)

    # Month-specific validations
    if month == 2:
        if is_leap_year(year):
            if day > 29:
                print("February can only have 29 days in a leap year.")
                return get_valid_date()  # Ask again
        else:
            if day > 28:
                print("February can only have 28 days in a non-leap year.")
                return get_valid_date()  # Ask again
    elif month in [4, 6, 9, 11] and day > 30:  # April, June, September, November
        print(f"Month {month} can only have 30 days.")
        return get_valid_date()  # Ask again

    return f"{day:02}/{month:02}/{year}"

# Task B: Process the CSV data and calculate traffic statistics
def process_csv_data(file_path):
    outcomes = {}

    required_columns = {"VehicleType", "elctricHybrid", "JunctionName", "VehicleSpeed",
                        "JunctionSpeedLimit", "timeOfDay", "Weather_Conditions",
                        "travel_Direction_in", "travel_Direction_out"}

    try:
        with open(file_path, mode="r") as file:
            csv_reader = csv.DictReader(file)

            if not required_columns.issubset(csv_reader.fieldnames):
                missing = required_columns - set(csv_reader.fieldnames)
                raise KeyError(f"Missing expected columns: {', '.join(missing)}")

            # Initialize counters
            total_vehicles = 0
            total_trucks = 0
            total_electric = 0
            two_wheeled = 0
            buses_north = 0
            no_turns = 0
            over_speed_limit = 0
            elm_avenue_vehicles = 0
            hanley_highway_vehicles = 0
            scooters_elm_avenue = 0
            bicycles_per_hour = {}
            hanley_traffic_by_hour = {}
            rain_hours = set()

            for row in csv_reader:
                try:
                    if not all(row[col].strip() for col in required_columns):
                        print(f"Skipping row with missing values: {row}")
                        continue

                    total_vehicles += 1

                    # Count trucks
                    if row["VehicleType"].strip().lower() == "truck":
                        total_trucks += 1

                    # Count electric vehicles
                    if row["elctricHybrid"].strip().lower() == "true":
                        total_electric += 1

                    # Count two-wheeled vehicles
                    vehicle_type = row["VehicleType"].strip().lower()
                    if vehicle_type in ["bicycle", "motorbike", "scooter", "motorcycle"]:
                        two_wheeled += 1

                    # Count buses heading North from Elm Avenue
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"].upper() == "N" and row["VehicleType"].strip().lower() == "buss":
                        buses_north += 1

                    # Count vehicles not turning
                    if row["travel_Direction_in"] == row["travel_Direction_out"]:
                        no_turns += 1

                    # Count vehicles over speed limit
                    try:
                        if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                            over_speed_limit += 1
                    except ValueError:
                        print(f"Invalid speed data in row: {row}")
                        continue

                    # Count vehicles by junction
                    if row["JunctionName"] == "Elm Avenue/Rabbit Road":
                        elm_avenue_vehicles += 1
                        if vehicle_type == "scooter":
                            scooters_elm_avenue += 1
                    elif row["JunctionName"] == "Hanley Highway/Westway":
                        hanley_highway_vehicles += 1
                        hour = row["timeOfDay"].split(":")[0]
                        hanley_traffic_by_hour[hour] = hanley_traffic_by_hour.get(hour, 0) + 1

                    # Count bicycles per hour
                    if vehicle_type == "bicycle":
                        hour = row["timeOfDay"].split(":")[0]
                        bicycles_per_hour[hour] = bicycles_per_hour.get(hour, 0) + 1

                    # Count rain hours
                    if row["Weather_Conditions"].strip().lower() == "rain":
                        hour = row["timeOfDay"].split(":")[0]
                        rain_hours.add(hour)

                except KeyError as e:
                    print(f"Skipping row due to missing column: {e}")
                    continue

            # Store outcomes
            outcomes["File Name"] = file_path
            outcomes["Total Vehicles"] = total_vehicles
            outcomes["Total Trucks"] = total_trucks
            outcomes["Total Electric Vehicles"] = total_electric
            outcomes["Two-Wheeled Vehicles"] = two_wheeled
            outcomes["Buses North"] = buses_north
            outcomes["Vehicles No Turns"] = no_turns
            outcomes["Trucks Percentage"] = round((total_trucks / total_vehicles) * 100) if total_vehicles else 0
            outcomes["Average Bicycles Per Hour"] = round(sum(bicycles_per_hour.values()) / 24) if bicycles_per_hour else 0
            outcomes["Over Speed Limit"] = over_speed_limit
            outcomes["Elm Avenue Vehicles"] = elm_avenue_vehicles
            outcomes["Hanley Highway Vehicles"] = hanley_highway_vehicles
            outcomes["Scooters Percentage Elm"] = round((scooters_elm_avenue / elm_avenue_vehicles) * 100) if elm_avenue_vehicles else 0
            outcomes["Peak Traffic Count"] = max(hanley_traffic_by_hour.values(), default=0)
            outcomes["Peak Traffic Hours"] = [
                f"Between {int(hour):02}:00 and {int(hour)+1}:00"
                for hour, count in hanley_traffic_by_hour.items()
                if count == outcomes["Peak Traffic Count"]
            ]
            outcomes["Rain Hours"] = len(rain_hours)
            outcomes["HanleyTrafficByHour"] = hanley_traffic_by_hour

            return outcomes

    except FileNotFoundError:
        print(f"Error: File not found - '{file_path}'")
    except KeyError as e:
        print(f"Error: {e}")
    return outcomes

# Task C: Display results in the required format
def display_outcomes(outcomes):
    if not outcomes:  # Check for empty or error-flagged outcomes
        print("No valid data to display.")
        return

    print("\n***************************")
    print(f"Data file selected is {outcomes['File Name']}")
    print("***************************")
    print(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}")
    print(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}")
    print(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}")
    print(f"The total number of Buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Buses North']}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['Vehicles No Turns']}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Trucks Percentage']}%")
    print(f"The average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}")
    print()
    print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Over Speed Limit']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Avenue Vehicles']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway Vehicles']}")
    print(f"{outcomes['Scooters Percentage Elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print()
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Peak Traffic Count']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(outcomes['Peak Traffic Hours'])}")
    print(f"The number of hours of rain for this date is {outcomes['Rain Hours']}")

# Function to save outcomes to a text file
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file.

    Args:
        outcomes (dict): The dictionary containing processed traffic data.
        file_name (str): The name of the text file to save results. Default is 'results.txt'.
    """
    try:
        with open(file_name, "a") as file:  # Open the file in append mode
            file.write("\n***************************\n")
            file.write(f"Data file selected is {outcomes['File Name']}\n")
            file.write("***************************\n")
            file.write(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}\n")
            file.write(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}\n")
            file.write(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}\n")
            file.write(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}\n")
            file.write(f"The total number of Buses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Buses North']}\n")
            file.write(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['Vehicles No Turns']}\n")
            file.write(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Trucks Percentage']}%\n")
            file.write(f"The average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}\n")
            file.write("\n")
            file.write(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Over Speed Limit']}\n")
            file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Avenue Vehicles']}\n")
            file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway Vehicles']}\n")
            file.write(f"{outcomes['Scooters Percentage Elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
            file.write("\n")
            file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Peak Traffic Count']}\n")
            file.write(f"The most vehicles through Hanley Highway/Westway were recorded {', '.join(outcomes['Peak Traffic Hours'])}\n")
            file.write(f"The number of hours of rain for this date is {outcomes['Rain Hours']}\n")
            file.write("\n")
            print("Results saved to results.txt successfully.")
    except Exception as e:
        print(f"Error saving results to file: {e}")


# Task D: Create histogram using Tkinter
class HistogramApp:
    def __init__(self, master, data_file, selected_date):
        self.master = master
        self.master.title("Histogram")
        self.data_file = data_file
        self.selected_date = selected_date
        self.canvas = None
        self.frame = None
        
        # Traffic data storage
        self.traffic_data = {
            "Elm Avenue/Rabbit Road": {str(i).zfill(2): 0 for i in range(24)},
            "Hanley Highway/Westway": {str(i).zfill(2): 0 for i in range(24)}
        }
        
        try:
            self.load_traffic_data()
            self.setup_window()
            self.draw_histogram()
            self.add_legend()
        except Exception as e:
            print(f"Error loading or displaying histogram: {e}")

    def setup_window(self):
        self.frame = tk.Frame(self.master, bg='white')
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.canvas = tk.Canvas(self.frame, width=900, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Update canvas dimensions
        self.master.update()

    def draw_histogram(self):
        try:
            margin_x = 50
            margin_y = 170
            bar_spacing = 3.5
            bar_width = 16
            colors = ['#90EE90', '#FFA07A']

            # Calculate max value for scaling
            max_traffic = max(max(junction_data.values()) for junction_data in self.traffic_data.values())
            if max_traffic == 0:
                self.canvas.create_text(
                    self.canvas.winfo_width() / 2,
                    self.canvas.winfo_height() / 2,
                    text="No traffic data available to display.",
                    font=('Arial', 14, 'bold'),
                    fill="red"
                )
                return  # Exit early

            graph_height = self.canvas.winfo_height() - 2 * margin_y

            # Add title and labels
            title = f"Histogram of Vehicle Frequency per Hour ({self.selected_date})"
            self.canvas.create_text(self.canvas.winfo_width() / 5.9, margin_y / 8, 
                                    text=title, font=('Arial', 12, 'bold'))
            self.canvas.create_text(self.canvas.winfo_width() / 2, 
                                    self.canvas.winfo_height() - 100, 
                                    text="Hours 00:00 to 24:00", font=('Arial', 10))

            # Draw bars
            junctions = list(self.traffic_data.keys())
            hours = [str(i).zfill(2) for i in range(24)]

            for i, hour in enumerate(hours):
                x_base = margin_x + (i * (2.4 * bar_width + bar_spacing + 6))
                
                for j, junction in enumerate(junctions):
                    traffic = self.traffic_data[junction][hour]
                    bar_height = (traffic / max_traffic) * graph_height if max_traffic > 0 else 0
                    x = x_base + (j * (bar_width + bar_spacing))
                    y = self.canvas.winfo_height() - margin_y - bar_height

                    # Draw bar
                    self.canvas.create_rectangle(x, y, x + bar_width, 
                                                self.canvas.winfo_height() - margin_y, 
                                                fill=colors[j], outline='black')
                    
                    # Add traffic value above bars
                    if traffic > 0:
                        self.canvas.create_text(x + bar_width / 2, y - 5, 
                                                text=str(traffic), font=('Arial', 8))

                # Add hour labels
                self.canvas.create_text(x_base + bar_width + bar_spacing, 
                                        self.canvas.winfo_height() - margin_y + 15, 
                                        text=hour, font=('Arial', 8))
        except Exception as e:
            print(f"Error during histogram drawing: {e}")

    def add_legend(self):
        try:
            colors = ['#90EE90', '#FFA07A']
            legend_y = 50
            for j, junction in enumerate(self.traffic_data.keys()):
                self.canvas.create_rectangle(50, legend_y, 70, legend_y + 15, 
                                            fill=colors[j], outline='black')
                self.canvas.create_text(75, legend_y + 7, text=junction, 
                                        anchor=tk.W, font=('Arial', 10))
                legend_y += 25
        except Exception as e:
            print(f"Error adding legend: {e}")

    def load_traffic_data(self):
        try:
            with open(self.data_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    hour = row['timeOfDay'].split(':')[0].zfill(2)
                    junction = row['JunctionName']
                    if junction in self.traffic_data:
                        self.traffic_data[junction][hour] += 1
        except FileNotFoundError:
            print(f"Error: File '{self.data_file}' not found.")


# Modify the create_histogram function to not block execution
def create_histogram(file_path, selected_date):
    try:
        root = tk.Tk()
        root.state('zoomed')
        root.geometry("800x600")
        app = HistogramApp(root, file_path, selected_date)
        
        # Don't wait for window closure
        root.update()
        
        # Continue with program flow
        return root
    except Exception as e:
        print(f"Error creating histogram: {e}")
        return None


#Task E
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None
        self.date_to_file = {
            "15/06/2024": "traffic_data15062024.csv",
            "16/06/2024": "traffic_data16062024.csv",
            "21/06/2024": "traffic_data21062024.csv"
        }

    def load_csv_file(self, date):
        if date in self.date_to_file:
            file_name = self.date_to_file[date]
            print(f"Processing dataset for {date}...")
            self.current_data = process_csv_data(file_name)
            if self.current_data:
                self.current_data["File Name"] = file_name  # Ensure correct filename is stored
                return True
        return False

    def clear_previous_data(self):
        self.current_data = None

    def process_files(self):
        self.handle_user_interaction()

    def handle_user_interaction(self):
        while True:
            date = get_valid_date()
            
            if self.load_csv_file(date):
                display_outcomes(self.current_data)
                save_results_to_file(self.current_data)
                
                histogram_window = create_histogram(self.date_to_file[date], date)
                
                while True:
                    choice = input("Do you want to select another data file for a different date? Y/N > ").strip().upper()
                    if choice in ["Y", "N"]:
                        if histogram_window:
                            histogram_window.destroy()
                        if choice == "N":
                            print("End of run")
                            return
                        break
                    print("Please enter 'Y' or 'N'.")
                
                if choice == "Y":
                    self.clear_previous_data()
            else:
                print("No data available for the entered date.")
                continue

# Main Program Execution
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()  # Using process_files as main entry point




from tkinter import *
from tkinter import ttk
import requests
from PIL import Image, ImageTk

# Function to update labels with fetched data
def update_labels(climate, description, temperature, pressure, wind_speed, humidity, aqi):
    w_label.config(text=f"Weather Climate: {climate}")
    wb_label.config(text=f"Description: {description}")
    temp_label.config(text=f"Temperature: {temperature}")
    per_label.config(text=f"Pressure: {pressure}")
    wind_label.config(text=f"Wind Speed: {wind_speed}")
    humidity_label.config(text=f"Humidity: {humidity}")
    aqi_label.config(text=f"AQI: {aqi}")

# Function to fetch weather data
def fetch_weather():
    city_name = com.get()
    if not city_name:
        return

    API_KEY = "142ec3aef302fa209ea7fc6e95c71420"  # Replace with your valid API key
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={{lat}}&lon={{lon}}&appid={API_KEY}"

    try:
        weather_data = requests.get(weather_url, timeout=10).json()
        if weather_data.get("cod") != 200:
            update_labels("Error", "Invalid city", "-", "-", "-", "-", "-")
            return

        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]
        aqi_data = requests.get(aqi_url.format(lat=lat, lon=lon), timeout=10).json()

        aqi_value = aqi_data["list"][0]["main"]["aqi"] if "list" in aqi_data else None
        aqi_description = get_aqi_description(aqi_value)

        update_labels(
            weather_data["weather"][0]["main"],
            weather_data["weather"][0]["description"].capitalize(),
            f"{weather_data['main']['temp']}°C",
            f"{weather_data['main']['pressure']} hPa",
            f"{weather_data['wind']['speed']} m/s",
            f"{weather_data['main']['humidity']}%",
            aqi_description
        )
    except requests.exceptions.Timeout:
        update_labels("Error", "Request Timeout", "-", "-", "-", "-", "-")
    except Exception as e:
        update_labels("Error", "Network issue", "-", "-", "-", "-", "-")

# Function to map AQI number to its corresponding description
def get_aqi_description(aqi):
    if aqi == 1:
        return "Good"
    elif aqi == 2:
        return "Fair"
    elif aqi == 3:
        return "Moderate"
    elif aqi == 4:
        return "Poor"
    elif aqi == 5:
        return "Very Poor"
    else:
        return "Unknown"

# Function to adjust layout dynamically
def adjust_layout(event=None):
    screen_width = win.winfo_width()
    screen_height = win.winfo_height()

    name_label.place(x=screen_width // 4, y=screen_height // 10, height=50, width=screen_width // 2)

    # Responsive combobox width based on window size
    combobox_width = screen_width // 2  # 50% of the window width
    combobox_width = max(combobox_width, 200)  # Ensure minimum width of 200px
    com.place(x=screen_width // 4, y=screen_height // 6, height=50, width=combobox_width)

    done_button.place(x=screen_width // 2.2, y=screen_height // 4, height=50, width=100)

    for idx, lbl in enumerate([w_label, wb_label, temp_label, per_label, wind_label, humidity_label, aqi_label]):
        lbl.place(x=screen_width // 10, y=screen_height // 3 + idx * 60, height=50, width=screen_width * 0.8)

    # Adjust background
    bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image_tk_resized = ImageTk.PhotoImage(bg_image_resized)
    canvas.create_image(0, 0, image=bg_image_tk_resized, anchor="nw")
    canvas.image = bg_image_tk_resized  # Prevent garbage collection

# Create main window
win = Tk()
win.title("City Weather")
win.geometry("800x600")  # Initial size
win.state("zoomed")  # Start maximized
win.bind("<Configure>", adjust_layout)

# Load the background image
bg_image = Image.open("weathrimg2.jpg")  # Replace with your image file

canvas = Canvas(win)
canvas.pack(fill="both", expand=True)

# Widgets
name_label = Label(win, text="CITY WEATHER", font=("Times New Roman", 30, "italic"), bg="grey", fg="white")
com = ttk.Combobox(win, values=("Ahmedabad", "Amritsar", "Bangalore", "Bhopal", "Chennai", "Delhi", "Faridabad", "Gandhinagar", "Hyderabad", 
    "Jaipur", "Kolkata", "Lucknow", "Mumbai", "Nagpur", "Nashik", "Patna", "Pune", "Surat", "Vadodara", "Visakhapatnam", 
    "Agra", "Aligarh", "Allahabad (Prayagraj)", "Aurangabad", "Bagalkot", "Baroda", "Belagavi", "Bhilai", "Bhubaneswar", 
    "Bikaner", "Bilaspur", "Bokaro", "Chandigarh", "Coimbatore", "Dehradun", "Dhanbad", "Durg", "Faridkot", "Gandhinagar", 
    "Ghaziabad", "Gorakhpur", "Gwalior", "Haldia", "Hamirpur", "Haridwar", "Hazaribagh", "Howrah", "Hubli", "Imphal", 
    "Indore", "Jabalpur", "Jaipur", "Jalandhar", "Jammu", "Jamshedpur", "Jodhpur", "Kannur", "Kanpur", "Kollam", "Kolkata", 
    "Kota", "Kottayam", "Kozhikode", "Ludhiana", "Madurai", "Malappuram", "Meerut", "Moradabad", "Mysuru", "Nagapattinam", 
    "Nanded", "Nashik", "Navi Mumbai", "Nizamabad", "Noida", "Patiala", "Pune", "Raipur", "Rajkot", "Ranchi", "Rourkela", 
    "Salem", "Sambalpur", "Surat", "Thane", "Tiruchirappalli", "Tirunelveli", "Udaipur", "Vadodara", "Varanasi", "Vellore", 
    "Vijayawada", "Visakhapatnam", "Warangal", "Yamunanagar", "Agartala", "Aizawl", "Alappuzha", "Aligarh", "Ambala", 
    "Ambikapur", "Anand", "Angul", "Anantapur", "Arrah", "Asansol", "Aurangabad", "Bagdogra", "Bahraich", "Balangir", "Ballia", 
    "Balurghat", "Bargarh", "Barmer", "Barpeta", "Begusarai", "Belagavi", "Berhampur", "Bhadrak", "Bhagalpur", "Bhilwara", 
    "Bhopal", "Bhubaneswar", "Bidar", "Bijapur", "Bikaner", "Bilaspur", "Bokaro", "Budgam", "Buxar", "Cannanore", "Chandrapur", 
    "Chandrapur", "Chapra", "Chhatarpur", "Chhindwara", "Chidambaram", "Chikkamagaluru", "Chiplun", "Chittoor", "Coimbatore", 
    "Cuttack", "Daltonganj", "Daman", "Darbhanga", "Deoghar", "Dibrugarh", "Dindigul", "Durgapur", "Erode", "Faridabad", "Fatehabad", 
    "Fatehpur", "Gajapati", "Gandhinagar", "Gandhinagar", "Gaya", "Ghazipur", "Ghaziabad", "Gorakhpur", "Gulbarga", "Guna", 
    "Gwalior", "Haldwani", "Hazaribagh", "Howrah", "Hubli", "Hoshiarpur", "Hyderabad", "Imphal", "Indore", "Itanagar", "Jabalpur", 
    "Jagdalpur", "Jaipur", "Jalandhar", "Jammu", "Jamshedpur", "Jodhpur", "Junagadh", "Kakinada", "Kalimpong", "Kannauj", "Kannur", 
    "Kanpur", "Kanyakumari", "Karaikal", "Karimnagar", "Katra", "Katihar", "Khandwa", "Kolhapur", "Kollam", "Kota", "Kozhikode", 
    "Kurnool", "Kurukshetra", "Lucknow", "Madurai", "Malda", "Mangaluru", "Mancherial", "Meerut", "Mehsana", "Moradabad", "Mumbai", 
    "Muzaffarnagar", "Muzaffarpur", "Mysuru", "Nagapattinam", "Nagercoil", "Nanded", "Nashik", "Navi Mumbai", "Nellore", "Noida", 
    "Panaji", "Patiala", "Patna", "Pimpri-Chinchwad", "Pithoragarh", "Pune", "Raichur", "Raipur", "Rajahmundry", "Rajkot", "Ranchi", 
    "Raurkela", "Rewa", "Rohtak", "Rishikesh", "Sagar", "Saharanpur", "Salem", "Sambalpur", "Sanchi", "Sardarshahar", "Saugor", 
    "Shillong", "Shimla", "Shrirampur", "Silchar", "Siliguri", "Sitapur", "Solapur", "Surat", "Surat", "Tadepalligudem", "Thane", 
    "Thiruvananthapuram", "Tirunelveli", "Tirupur", "Udaipur", "Udupi", "Unnao", "Vadodara", "Varanasi", "Vellore", "Vengurla", 
    "Vijayawada", "Vikarabad", "Visakhapatnam", "Warangal", "West Bengal", "Yamunanagar", "Yavatmal", "Zunheboto", "Agartala", 
    "Akola", "Alappuzha", "Amravati", "Anantapur", "Arrah", "Asansol", "Aurangabad", "Bagalkot", "Ballabgarh", "Bankura", "Bareilly", 
    "Bhiwandi", "Bijapur", "Bilaspur", "Bokaro Steel City", "Budhni", "Chandigarh", "Chattarpur", "Dabra", "Darjeeling", "Dausa", 
    "Dehradun", "Dibrugarh", "Dimapur", "Gandhinagar", "Gandhinagar", "Gaya", "Ghaziabad", "Ghatkopar", "Gorakhpur", "Guwahati", 
    "Gwalior", "Hazaribagh", "Howrah", "Hubli", "Imphal", "Indore", "Jabalpur", "Jalandhar", "Jammu", "Jamshedpur", "Jodhpur", 
    "Kakinada", "Kalaburagi", "Kanchipuram", "Kanpur", "Karnal", "Kolar", "Kollam", "Kota", "Kozhikode", "Kumbakonam", "Lucknow", 
    "Ludhiana", "Madurai", "Malda", "Manali", "Mangaluru", "Mehsana", "Mumbai", "Muzaffarpur", "Mysuru", "Nagapattinam", "Nainital", 
    "Nanded", "Nashik", "Navi Mumbai", "Patiala", "Patna", "Pimpri-Chinchwad", "Pithoragarh", "Raipur", "Rajkot", "Ranchi", "Rishikesh", 
    "Rohtak", "Sagar", "Salem", "Sambalpur", "Sanchi", "Sangli", "Sarguja", "Shillong", "Shimla", "Silchar" ), font=("Times New Roman", 20))

done_button = Button(win, text="DONE", font=("Times New Roman", 20), command=fetch_weather)

# Weather info labels
w_label = Label(win, text="Weather Climate: -", font=("Times New Roman", 20), bg="#22d3f6", fg="white")
wb_label = Label(win, text="Description: -", font=("Times New Roman", 17), bg="#22d3f6", fg="white")
temp_label = Label(win, text="Temperature: -", font=("Times New Roman", 20), bg="#22d3f6", fg="white")
per_label = Label(win, text="Pressure: -", font=("Times New Roman", 20), bg="#22d3f6", fg="white")
wind_label = Label(win, text="Wind Speed: -", font=("Times New Roman", 20), bg="#22d3f6", fg="white")
humidity_label = Label(win, text="Humidity: -", font=("Times New Roman", 20), bg="#22d3f6", fg="white")
aqi_label = Label(win, text="AQI: -", font=("Times New Roman", 20), bg="#22d3f6", fg="white")

# Initial layout adjustment
adjust_layout()

# Run the app
win.mainloop()

import datetime
import csv

# Define the CSV file to store event data
EVENTS_CSV_FILE = 'events.csv'
TICKETS_CSV_FILE = 'tickets.csv'

# Function to validate a date string in DD/MM/YYYY format
def is_valid_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# Function to validate a time string in HH:MM format
def is_valid_time(time_string):
    try:
        datetime.datetime.strptime(time_string, '%H:%M')
        return True
    except ValueError:
        return False

# Function to create a new event
def create_event():
    print("\n1. Create Event")
    event_name = input('Enter Event Name: ')
    event_artist = input('Enter Event Artist (if any): ')
    event_venue = input('Enter Event Venue: ')
    event_date = input('Enter Event Date (DD/MM/YYYY): ')
    event_time = input('Enter Event Time (HH:MM): ')
    event_capacity = int(input('Enter Venue Capacity: '))
    event_code = input('Enter Event Code (unique): ')
    entry_price = float(input('Enter Entry Price: '))

    # Validate event date and time
    if not is_valid_date(event_date) or not is_valid_time(event_time):
        print("Invalid date or time format. Event not saved.")
        return

    event_data = [event_name, event_artist, event_venue, event_date, event_time, event_capacity, event_code, entry_price]

    # Check if the event code is unique
    if is_event_code_unique(event_code):
        save_event(event_data)
        print("Event created and saved successfully.")
    else:
        print("Event code must be unique. Event not saved.")

# Function to save event data to the CSV file
def save_event(event_data):
    with open(EVENTS_CSV_FILE, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(event_data)

# Function to check if the event code is unique
def is_event_code_unique(event_code):
    with open(EVENTS_CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[6] == event_code:
                return False
    return True

# Function to search for events
def search_events():
    while True:
        print("\n1. Show all events")
        print("2. Search events by:")
        print("   1. Event Name")
        print("   2. Event Artist")
        print("   3. Event Venue")
        print("   4. Event Date")
        print("   5. Event Code")
        print("   6. Back to main menu")

        user_choice = input("\nEnter your choice: ")

        if user_choice == '1':
            show_all_events()
        elif user_choice == '2':
            search_criteria = input("Enter your search query: ")
            search_events_by_criteria(search_criteria)
        elif user_choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

# Function to display all events
def show_all_events():
    with open(EVENTS_CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        for row in reader:
            print_event_data(row)

# Function to search events by criteria
def search_events_by_criteria(search_criteria):
    with open(EVENTS_CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        found_events = []
        for row in reader:
            for field in row:
                if search_criteria.lower() in field.lower():
                    found_events.append(row)
                    break  # Avoid duplicate entries

    if found_events:
        for event_data in found_events:
            print_event_data(event_data)
    else:
        print("No matching events found.")

# Function to print event data
def print_event_data(event_data):
    print("\nEvent Name:", event_data[0])
    print("Event Artist:", event_data[1])
    print("Event Venue:", event_data[2])
    print("Event Date:", event_data[3])
    print("Event Time:", event_data[4])
    print("Event Capacity:", event_data[5])
    print("Event Code:", event_data[6])
    print("Entry Price:", event_data[7])

# Function to book tickets for an event
def book_tickets():
    print("\n2. Book Tickets")
    event_code = input("Enter the event code to book tickets: ")
    quantity = int(input("Enter the number of tickets you want to book: "))

    event = find_event_by_code(event_code)

    if event:
        event_name, event_date, event_time, entry_price = event[0], event[3], event[4], event[7]
        total_cost = float(entry_price) * quantity
        print(f"Event Name: {event_name}")
        print(f"Event Date: {event_date}")
        print(f"Event Time: {event_time}")
        print(f"Total Cost for {quantity} tickets: ${total_cost:.2f}")
        confirm_booking = input("Do you want to confirm the booking? (yes/no): ").strip().lower()

        if confirm_booking == "yes":
            record_booking(event_code, quantity, total_cost)
            print("Booking confirmed. Tickets recorded.")
        else:
            print("Booking not confirmed.")
    else:
        print(f"Event with code {event_code} not found.")

# Function to find an event by its code
def find_event_by_code(event_code):
    with open(EVENTS_CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[6] == event_code:
                return row
    return None

# Function to record booking in the tickets file
def record_booking(event_code, quantity, total_cost):
    with open(TICKETS_CSV_FILE, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([event_code, quantity, total_cost])

# Function to display booked tickets
def display_booked_tickets():
    print("\n3. Display Booked Tickets")
    with open(TICKETS_CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        print("\nBooked Tickets:")
        for row in reader:
            event_code, quantity, total_cost = row
            print(f"Event Code: {event_code}, Quantity: {quantity}, Total Cost: ${total_cost:.2f}")

# Main program loop
while True:
    print("\n-------- 'ABC' Event Management System --------")
    print("************* Password Protection *************")
    username = input("\nEnter your username: ")
    password = input("Enter the password: ")

    if username == "admin" and password == "admin123":
        print("\nWelcome, you are logged in as an admin.")
        admin_menu_choice = input("\nSelect an option:\n1. Create Event\n2. Search Events\n3. Exit\n")

        if admin_menu_choice == '1':
            create_event()
        elif admin_menu_choice == '2':
            search_events()
        elif admin_menu_choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Returning to login screen.")
    elif username == "user" and password == "user123":
        print("\nWelcome, you are logged in as a user.")
        while True:
            print("\nUser Menu:")
            print("1. Search Events")
            print("2. Book Tickets")
            print("3. Display Booked Tickets")
            print("4. Exit")

            user_menu_choice = input("Select an option: ")

            if user_menu_choice == '1':
                search_events()
            elif user_menu_choice == '2':
                book_tickets()
            elif user_menu_choice == '3':
                display_booked_tickets()
            elif user_menu_choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Incorrect credentials. Please enter the correct details.")

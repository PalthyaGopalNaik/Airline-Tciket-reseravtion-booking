import streamlit as st
import requests
from datetime import datetime

BOOKING_API_URL = "http://127.0.0.1:8000"  # Booking Service URL
FLIGHT_API_URL = "http://127.0.0.1:8001"  # Flight Service URL

st.title("Airline Ticket Booking System")

# Sidebar navigation
menu = ["Create Booking", "View Bookings", "Update Booking", "Delete Booking", "Add Flight", "View Flights"]
choice = st.sidebar.selectbox("Select Action", menu)

# Create Booking
if choice == "Create Booking":
    st.header("Create a New Booking")

    st.subheader("Step 1: Search for Available Flights")
    origin_input = st.text_input("Enter Origin (From)")
    destination_input = st.text_input("Enter Destination (To)")
    flights = []

    if st.button("Get Flight Options"):
        if origin_input and destination_input:
            params = {"origin": origin_input, "destination": destination_input}
            response = requests.get(f"{FLIGHT_API_URL}/flights/search", params=params)
            if response.status_code == 200:
                flights = response.json()
                st.success("Flights found!")
            else:
                st.error("No flights found for the specified route.")
        else:
            st.error("Please enter both origin and destination to search for flights.")

    selected_flight_number = None
    if flights:
        st.subheader("Select a Flight")
        flight_options = {
            f"{flight['flight_number']} | Dep: {flight['departure_time']} | Arr: {flight['arrival_time']}": flight
            for flight in flights}
        selected_option = st.selectbox("Available Flights", list(flight_options.keys()))
        selected_flight = flight_options[selected_option]
        selected_flight_number = selected_flight["flight_number"]
        st.write("You have selected flight:", selected_flight_number)
    else:
        st.info("No flight options selected or available yet.")

    st.subheader("Step 2: Enter Booking Details")
    passenger_name = st.text_input("Passenger Name")

    if selected_flight_number:
        flight_number = st.text_input("Flight Number", value=selected_flight_number)
    else:
        flight_number = st.text_input("Flight Number")

    departure = origin_input if origin_input else st.text_input("Departure Airport")
    destination = destination_input if destination_input else st.text_input("Destination Airport")
    departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
    seat_class = st.selectbox("Seat Class", ["Economy", "Business", "First"])

    if st.button("Submit Booking"):
        booking_data = {
            "passenger_name": passenger_name,
            "flight_number": flight_number,
            "departure": departure,
            "destination": destination,
            "departure_time": departure_time,
            "seat_class": seat_class
        }
        response = requests.post(f"{BOOKING_API_URL}/bookings", json=booking_data)
        if response.status_code == 200:
            st.success("Booking created!")
            st.json(response.json())
        else:
            st.error("Error creating booking")

# View Bookings
elif choice == "View Bookings":
    st.header("All Bookings")
    response = requests.get(f"{BOOKING_API_URL}/bookings")
    if response.status_code == 200:
        bookings = response.json()
        if bookings:
            for booking in bookings:
                st.write(booking)
                st.markdown("---")
        else:
            st.info("No bookings found")
    else:
        st.error("Error fetching bookings")

# Update Booking
elif choice == "Update Booking":
    st.header("Update Booking")
    booking_id = st.text_input("Enter Booking ID to update")
    if st.button("Fetch Booking"):
        response = requests.get(f"{BOOKING_API_URL}/bookings/{booking_id}")
        if response.status_code == 200:
            booking = response.json()
            passenger_name = st.text_input("Passenger Name", value=booking.get("passenger_name"))
            flight_number = st.text_input("Flight Number", value=booking.get("flight_number"))
            departure = st.text_input("Departure Airport", value=booking.get("departure"))
            destination = st.text_input("Destination Airport", value=booking.get("destination"))
            departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM)", value=booking.get("departure_time").replace("T", " "))
            seat_class = st.selectbox("Seat Class", ["Economy", "Business", "First"], index=["Economy", "Business", "First"].index(booking.get("seat_class")))

            if st.button("Submit Update"):
                booking_data = {
                    "passenger_name": passenger_name,
                    "flight_number": flight_number,
                    "departure": departure,
                    "destination": destination,
                    "departure_time": departure_time,
                    "seat_class": seat_class,
                    "status": booking.get("status")
                }
                update_response = requests.put(f"{BOOKING_API_URL}/bookings/{booking_id}", json=booking_data)
                if update_response.status_code == 200:
                    st.success("Booking updated successfully!")
                    st.json(update_response.json())
                else:
                    st.error("Error updating booking")
        else:
            st.error("Booking not found")

# Delete Booking
elif choice == "Delete Booking":
    st.header("Delete Booking")
    booking_id = st.text_input("Enter Booking ID to delete")
    if st.button("Delete Booking"):
        response = requests.delete(f"{BOOKING_API_URL}/bookings/{booking_id}")
        if response.status_code == 200:
            st.success("Booking deleted successfully!")
        else:
            st.error("Error deleting booking")

# Add Flight
elif choice == "Add Flight":
    st.header("Add a New Flight")
    flight_number = st.text_input("Flight Number")
    origin = st.text_input("Origin (From)")
    destination = st.text_input("Destination (To)")
    departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
    arrival_time = st.text_input("Arrival Time (YYYY-MM-DD HH:MM)", value=datetime.now().strftime("%Y-%m-%d %H:%M"))

    if st.button("Submit Flight"):
        flight_data = {
            "flight_number": flight_number,
            "origin": origin,
            "destination": destination,
            "departure_time": departure_time,
            "arrival_time": arrival_time
        }
        response = requests.post(f"{FLIGHT_API_URL}/flights", json=flight_data)
        if response.status_code == 200:
            st.success("Flight added successfully!")
            st.json(response.json())
        else:
            st.error("Error adding flight")

# View Flights
elif choice == "View Flights":
    st.header("Available Flights")
    response = requests.get(f"{FLIGHT_API_URL}/flights")
    if response.status_code == 200:
        flights = response.json()
        if flights:
            for flight in flights:
                st.write(f"**Flight Number:** {flight.get('flight_number')}")
                st.write(f"**From:** {flight.get('origin')} - **To:** {flight.get('destination')}")
                st.write(f"**Departure Time:** {flight.get('departure_time')}")
                st.write(f"**Arrival Time:** {flight.get('arrival_time')}")
                st.markdown("---")
        else:
            st.info("No flights available.")
    else:
        st.error("Error fetching flights")

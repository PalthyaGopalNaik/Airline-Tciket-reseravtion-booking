# main_app.py

import streamlit as st
import requests
from datetime import datetime

# Set the base URL of the FastAPI booking service.
API_URL = "http://127.0.0.1:8000"

st.title("Airline Ticket Booking System")

# Sidebar navigation
menu = ["Create Booking", "View Bookings", "Update Booking", "Delete Booking"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Create Booking":
    st.header("Create a New Booking")
    passenger_name = st.text_input("Passenger Name")
    flight_number = st.text_input("Flight Number")
    departure = st.text_input("Departure Airport")
    destination = st.text_input("Destination Airport")
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
        response = requests.post(f"{API_URL}/bookings", json=booking_data)
        if response.status_code == 200:
            st.success("Booking created!")
            st.json(response.json())
        else:
            st.error("Error creating booking")

elif choice == "View Bookings":
    st.header("All Bookings")
    response = requests.get(f"{API_URL}/bookings")
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

elif choice == "Update Booking":
    st.header("Update Booking")
    booking_id = st.text_input("Enter Booking ID to update")
    if st.button("Fetch Booking"):
        response = requests.get(f"{API_URL}/bookings/{booking_id}")
        if response.status_code == 200:
            booking = response.json()
            passenger_name = st.text_input("Passenger Name", value=booking.get("passenger_name"))
            flight_number = st.text_input("Flight Number", value=booking.get("flight_number"))
            departure = st.text_input("Departure Airport", value=booking.get("departure"))
            destination = st.text_input("Destination Airport", value=booking.get("destination"))
            departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM)",
                                           value=booking.get("departure_time").replace("T", " "))
            seat_class = st.selectbox("Seat Class", ["Economy", "Business", "First"],
                                      index=["Economy", "Business", "First"].index(booking.get("seat_class")))

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
                update_response = requests.put(f"{API_URL}/bookings/{booking_id}", json=booking_data)
                if update_response.status_code == 200:
                    st.success("Booking updated successfully!")
                    st.json(update_response.json())
                else:
                    st.error("Error updating booking")
        else:
            st.error("Booking not found")

elif choice == "Delete Booking":
    st.header("Delete Booking")
    booking_id = st.text_input("Enter Booking ID to delete")
    if st.button("Delete Booking"):
        response = requests.delete(f"{API_URL}/bookings/{booking_id}")
        if response.status_code == 200:
            st.success("Booking deleted successfully!")
        else:
            st.error("Error deleting booking")

# Airline Ticket Reservation Booking System

This project is a mock flight reservation system built using **FastAPI** for backend services and **Streamlit** for the frontend UI. It simulates a flight reservation system with functionalities to add flights, create, update, delete, and view bookings.

## Architecture

The system is divided into two main services:

1. **Flight Service** (`flight_service.py`): Manages flight information.
2. **Booking Service** (`booking_service.py`): Handles flight bookings (creating, updating, viewing, deleting).

The **Streamlit App** (`streamlit_app.py`) acts as the frontend that interacts with these services through HTTP requests.

### Components

- **Flight Service**:
  - Allows adding new flights.
  - Allows retrieving a list of available flights with optional filtering by origin and destination.

- **Booking Service**:
  - Allows creating new bookings.
  - Allows viewing, updating, and deleting existing bookings.

- **Streamlit Frontend**:
  - Allows users to search for available flights, create new bookings, view existing bookings, update, or delete bookings.

## Installation

This project uses **Poetry** for managing dependencies and virtual environments. Follow the steps below to get started.

1. **Clone the repository**:
    ```bash
    git clone https://github.com/PalthyaGopalNaik/Airline-Tciket-reseravtion-booking
    cd Airline-Ticket-reservation-booking
    ```

2. **Install Poetry** (if you don't have Poetry installed):
    ```bash
    pip install poetry
    ```

3. **Install Project Dependencies**:
    - Use Poetry to install all the dependencies specified in the `pyproject.toml` file:
    ```bash
    poetry install
    ```

4. **Activate the Virtual Environment**:
    - Once the dependencies are installed, you can activate the Poetry virtual environment:
    ```bash
    poetry shell
    ```

5. **Run the Project**:

    - **Start the Flight Service**:
        ```bash
        uvicorn flight_service:app --reload --port 8001
        ```

    - **Start the Booking Service**:
        ```bash
        uvicorn booking_service:app --reload --port 8000
        ```

    - **Run the Streamlit App**:
        ```bash
        streamlit run streamlit_app.py
        ```

6. **Open the Application**:
    - After running the Streamlit app, open a browser and navigate to the URL:
      ```
      http://localhost:8501
      ```

## Features

- **Create Booking**: Search available flights and create a new booking.
- **View Bookings**: View all existing bookings.
- **Update Booking**: Fetch and update a specific booking.
- **Delete Booking**: Delete an existing booking.
- **Add Flight**: Add a new flight to the system.
- **View Flights**: View all available flights.

## Project Structure

```bash
Airline-Ticket-reservation-booking/
├── booking_service.py      # FastAPI booking service
├── flight_service.py       # FastAPI flight service
├── streamlit_app.py        # Streamlit frontend app
├── pyproject.toml          # Poetry configuration file
├── poetry.lock             # Poetry lock file
└── README.md               # This file

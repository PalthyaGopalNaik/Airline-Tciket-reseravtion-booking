import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Airline Ticket Booking Service")

# In-memory store for booking data.
bookings_db = {}

class Booking(BaseModel):
    id: Optional[str] = None         # Auto-generated booking id
    passenger_name: str
    flight_number: str
    departure: str                   # Departure airport
    destination: str                 # Destination airport
    departure_time: datetime
    seat_class: str                  # e.g., Economy, Business, First
    status: Optional[str] = "booked"

# Create a booking
@app.post("/bookings", response_model=Booking)
def create_booking(booking: Booking):
    booking_id = str(uuid4())
    booking.id = booking_id
    bookings_db[booking_id] = booking
    return booking

# Retrieve a booking by id
@app.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: str):
    booking = bookings_db.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# Retrieve all bookings
@app.get("/bookings", response_model=List[Booking])
def list_bookings():
    return list(bookings_db.values())

# Update a booking
@app.put("/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: str, updated_booking: Booking):
    if booking_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    updated_booking.id = booking_id
    bookings_db[booking_id] = updated_booking
    return updated_booking

# Delete a booking
@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: str):
    if booking_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    del bookings_db[booking_id]
    return {"detail": "Booking deleted successfully"}

if __name__ == '__main__':
    uvicorn.run(app, port=8000)

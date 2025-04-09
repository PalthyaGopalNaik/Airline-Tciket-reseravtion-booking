import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Flight Management Service")

# In-memory store for flight data.
flights_db = {}

class Flight(BaseModel):
    id: Optional[str] = None         # Auto-generated flight id
    flight_number: str
    origin: str                      # Origin airport or city
    destination: str                 # Destination airport or city
    departure_time: datetime
    arrival_time: datetime

# Endpoint to add a flight
@app.post("/flights", response_model=Flight)
def add_flight(flight: Flight):
    flight_id = str(uuid4())
    flight.id = flight_id
    flights_db[flight_id] = flight
    return flight

# Endpoint to get all flights with optional filtering
@app.get("/flights", response_model=List[Flight])
def get_flights(origin: Optional[str] = None, destination: Optional[str] = None):
    flights = list(flights_db.values())
    if origin:
        flights = [f for f in flights if f.origin.lower() == origin.lower()]
    if destination:
        flights = [f for f in flights if f.destination.lower() == destination.lower()]
    return flights

# Endpoint to search flights between specific origin and destination
@app.get("/flights/search", response_model=List[Flight])
def search_flights(origin: str, destination: str):
    flights = [f for f in flights_db.values() if f.origin.lower() == origin.lower() and f.destination.lower() == destination.lower()]
    return flights

if __name__ == '__main__':
    uvicorn.run(app, port=8001)

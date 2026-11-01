# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Pune-Lonavala Smart Travel Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# DATA MODELS
# ==========================================
class ItineraryRequest(BaseModel):
    spot_ids: List[str]
    transport_mode: str
    traveller_count: int
    driver_id: str

# ==========================================
# MOCK DATA
# ==========================================
SPOTS = [
    {"id": "s1", "name": "Tiger's Leap", "geography": "High altitude cliff", "history": "Named for its resemblance to a tiger jumping", "aesthetic": "Stunning panoramic views, best at sunset", "sentiment_score": 0.85, "crowd_level": "High", "entry_fee": 20},
    {"id": "s2", "name": "Bhushi Dam", "geography": "Water reservoir", "history": "Built in 1907", "aesthetic": "Water overflowing over steps", "sentiment_score": 0.70, "crowd_level": "High", "entry_fee": 0},
    {"id": "s3", "name": "Karla Caves", "geography": "Basalt rock hills", "history": "Ancient Buddhist rock-cut caves", "aesthetic": "Intricate carvings, massive arch", "sentiment_score": 0.90, "crowd_level": "Low", "entry_fee": 250},
]

DRIVERS = [
    {"id": "d1", "name": "Ramesh Patil", "vehicle_type": "Sedan (Dzire)", "capacity": 4, "experience_years": 8, "languages": ["Marathi", "Hindi", "English"], "background_verified": True, "communication_rating": 4.8, "base_rate_per_km": 12.0},
    {"id": "d2", "name": "Suresh Jadhav", "vehicle_type": "Innova Crysta", "capacity": 6, "experience_years": 12, "languages": ["Marathi", "Hindi"], "background_verified": True, "communication_rating": 4.5, "base_rate_per_km": 16.0},
]

RESTAURANTS = [
    {"id": "r1", "name": "Chhaya Restaurant", "cuisine": "Indian, Chinese", "avg_cost": 400, "distance_from_route": 0.5, "hours": "8:00 AM - 11:00 PM"},
    {"id": "r2", "name": "Maharashtra Dhaba", "cuisine": "Maharashtrian", "avg_cost": 250, "distance_from_route": 0.2, "hours": "6:00 AM - 11:00 PM"},
]

PACKAGES = [
    {"id": "p1", "title": "Lonavala Express Day Trip", "provider": "MSRTC Shivneri", "price": 850, "inclusions": ["AC Bus", "Tiger's Leap", "Bhushi Dam"], "rating": 4.2, "duration": "One day", "preference": "Nature", "from": "Pune", "to": "Lonavala"},
    {"id": "p5", "title": "Weekend Nature Escape", "provider": "Green Trails", "price": 3500, "inclusions": ["SUV", "Trekking", "Camping", "Bonfire"], "rating": 4.5, "duration": "Weekend", "preference": "Nature", "from": "Pune", "to": "Lonavala"},
    {"id": "p6", "title": "Extended Hills Adventure", "provider": "Sahyadri Explorers", "price": 5500, "inclusions": ["Private Cab", "Trekking", "Camping", "All Meals"], "rating": 4.6, "duration": "2-3 days", "preference": "Nature", "from": "Pune", "to": "Lonavala"},
    {"id": "p2", "title": "Premium Caves & Valleys Tour", "provider": "Deccan Odyssey Travels", "price": 2500, "inclusions": ["Innova Cab", "Karla Caves", "Lunch", "Guide"], "rating": 4.7, "duration": "Weekend", "preference": "Culture", "from": "Pune", "to": "Lonavala"},
    {"id": "p7", "title": "Heritage Caves Day Tour", "provider": "Heritage Walks", "price": 1800, "inclusions": ["AC Bus", "Karla & Bhaja Caves", "Guide", "Lunch"], "rating": 4.3, "duration": "One day", "preference": "Culture", "from": "Pune", "to": "Lonavala"},
    {"id": "p3", "title": "Budget Backpacker Special", "provider": "Youth Hostels India", "price": 600, "inclusions": ["Shared Cab", "Bhushi Dam", "Street Food Tour"], "rating": 4.0, "duration": "One day", "preference": "Food", "from": "Pune", "to": "Lonavala"},
    {"id": "p8", "title": "Culinary Weekend Retreat", "provider": "Foodie Trails", "price": 4200, "inclusions": ["Private Cab", "Farm Visit", "Cooking Class", "All Meals"], "rating": 4.8, "duration": "Weekend", "preference": "Food", "from": "Pune", "to": "Lonavala"},
    {"id": "p4", "title": "Luxury Hills Retreat", "provider": "Taj Safaris", "price": 8500, "inclusions": ["Private SUV", "5-Star Stay", "Spa", "Fine Dining"], "rating": 4.9, "duration": "2-3 days", "preference": "Relaxation", "from": "Mumbai", "to": "Lonavala"},
    {"id": "p9", "title": "Spa & Wellness Day", "provider": "Serenity Escapes", "price": 3200, "inclusions": ["Cab", "Resort Day Pass", "Spa", "Lunch"], "rating": 4.4, "duration": "One day", "preference": "Relaxation", "from": "Pune", "to": "Lonavala"},
    {
        "id": "p10", "title": "Mumbai Darshan Bus Ticket", "provider": "Mumbai Darshan Tours", "price": 499, "inclusions": ["12-hour guided tour", "Multilingual live guide", "Free cancellation", "Pickup & drop"], "rating": 4.6, "duration": "One day", "preference": "Culture", "from": "Mumbai", "to": "Mumbai (City Tour)",
        "itinerary": [
            {"name": "The Asiatic Society Mumbai", "halt": "10 min"}, {"name": "Gateway of India", "halt": "45 min"}, {"name": "Sailing Boat Ride", "halt": "30 min"}, {"name": "Chhatrapati Shivaji Maharaj Vastu Sangrahalay (CSMVS)", "halt": "50 min"}, {"name": "Jehangir Art Gallery", "halt": "15 min"}, {"name": "Paradox Museum (Optional)", "halt": "1 hr"}, {"name": "Marine Drive (Queen's Necklace)", "halt": "10 min"}, {"name": "Mahalaxmi Temple", "halt": "35 min"}, {"name": "Nehru Science Centre + Orama 4D Show", "halt": "50 min"}, {"name": "Siddhivinayak Temple", "halt": "35 min"}, {"name": "National Museum of Indian Cinema", "halt": "45 min"}, {"name": "Juhu Beach", "halt": "45 min"}
        ],
        "boarding_points": [
            {"route": "From Thane", "stops": "Thane, Mulund, Bhandup, Vikhroli, Ghatkopar, Chembur, CSTM"},
            {"route": "From Panvel", "stops": "Panvel, Khanda Colony, Kalamboli, Kamothe, Kharghar, Belapur, Seawood, Nerul, Jui Nagar, Sanpada, Vashi, Chembur"},
            {"route": "From Borivali", "stops": "Dahisar, Borivali, Kandivali, Malad, Goregaon, Jogeshwari, Andheri East, Chakala, Ville Parle, Santacruz, Bandra, Mahim, Dadar, Byculla"}
        ]
    }
]
# ==========================================
# AI / RULE-BASED LOGIC
# ==========================================
def calculate_review_authenticity(text: str, rating: int) -> float:
    score = 0.5
    if len(text) < 20: score -= 0.2
    elif len(text) > 50: score += 0.2
    if text.isupper(): score -= 0.3
    if text.count("!") > 3: score -= 0.1
    spam_words = ["bestest", "must visit", "book now", "amazing experience", "superb"]
    if any(word in text.lower() for word in spam_words): score -= 0.2
    detail_words = ["driver", "food", "view", "clean", "time", "worth", "car"]
    if any(word in text.lower() for word in detail_words): score += 0.3
    return max(0.0, min(1.0, score))

# ==========================================
# API ENDPOINTS
# ==========================================
@app.get("/api/spots")
def get_spots(): return SPOTS

@app.get("/api/drivers")
def get_drivers(): return DRIVERS

@app.get("/api/restaurants")
def get_restaurants(): return RESTAURANTS

@app.get("/api/packages")
def get_packages(): return PACKAGES

@app.get("/api/weather/{spot_id}")
def get_weather(spot_id: str):
    # Mock weather data
    return {"temp": 24, "condition": "Partly Cloudy", "rain_chance": "10%", "wind": "12 km/h"}

@app.get("/api/reviews/{target_id}")
def get_reviews(target_id: str):
    # Mock reviews for the specific target (Driver or Restaurant)
    mock_reviews = [
        {"id": "rv1", "target_id": target_id, "text": "The driver was very punctual and the car was clean. Highly recommend!", "rating": 5},
        {"id": "rv2", "target_id": target_id, "text": "GOOD BEST AMAZING SUPERB BOOK NOW!!!", "rating": 5},
        {"id": "rv3", "target_id": target_id, "text": "Okay trip. Traffic was a bit much near the dam but food was good.", "rating": 3},
    ]
    
    processed_reviews = []
    for rev in mock_reviews:
        auth_score = calculate_review_authenticity(rev["text"], rev["rating"])
        processed_reviews.append({
            **rev,
            "authenticity_score": round(auth_score, 2),
            "is_fake": auth_score < 0.6
        })
    return processed_reviews

@app.post("/api/itinerary/calculate")
def calculate_itinerary(req: ItineraryRequest):
    driver = next((d for d in DRIVERS if d["id"] == req.driver_id), None)
    if not driver: raise HTTPException(status_code=404, detail="Driver not found")
    
    selected_spots = [s for s in SPOTS if s["id"] in req.spot_ids]
    if not selected_spots: raise HTTPException(status_code=400, detail="No spots selected")

    base_distance_km = 130 + (len(selected_spots) * 5) 
    transport_cost = base_distance_km * driver["base_rate_per_km"]
    entry_fees = sum(s["entry_fee"] for s in selected_spots) * req.traveller_count
    service_charge = 500 
    total_price = transport_cost + entry_fees + service_charge
    
    route_plan = ["Pune (Start)"] + [s["name"] for s in selected_spots] + ["Lonavala Market", "Pune (Drop)"]

    return {
        "route_plan": route_plan,
        "breakdown": {"transport_cost": transport_cost, "entry_fees": entry_fees, "service_charge": service_charge},
        "total_price": total_price,
        "driver_details": driver
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
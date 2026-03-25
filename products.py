from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(prefix="/tours", tags=["tours"])

DATA_FILE = "tours.json"

def load_tours():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        initial_tours = [
            {
                "id": 1,
                "country": "Турция",
                "city": "Анталья",
                "price": 45000,
                "duration": 7,
                "hotel": "5 звезд, все включено"
            },
            {
                "id": 2,
                "country": "Египет",
                "city": "Шарм-эль-Шейх",
                "price": 55000,
                "duration": 10,
                "hotel": "4 звезды, ультра все включено"
            },
            {
                "id": 3,
                "country": "Россия",
                "city": "Сочи",
                "price": 35000,
                "duration": 5,
                "hotel": "3 звезды, завтраки"
            },
            {
                "id": 4,
                "country": "Италия",
                "city": "Рим",
                "price": 120000,
                "duration": 8,
                "hotel": "4 звезды, полупансион"
            },
            {
                "id": 5,
                "country": "Турция",
                "city": "Аланья",
                "price": 40000,
                "duration": 7,
                "hotel": "4 звезды, все включено"
            }
        ]
        save_tours(initial_tours)
        return initial_tours

def save_tours(tours):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(tours, file, ensure_ascii=False, indent=4)

tours = load_tours()

@router.get("/")
async def get_tours(sorting: str = None, country: str = None):
    filtered_tours = tours.copy()
    
    if country:
        filtered_tours = [tour for tour in filtered_tours if tour["country"].lower() == country.lower()]
    
    if sorting == "asc":
        filtered_tours.sort(key=lambda x: x["country"])
    elif sorting == "desc":
        filtered_tours.sort(key=lambda x: x["country"], reverse=True)
    
    return {
        "tours": filtered_tours,
        "total": len(filtered_tours)
    }

@router.get("/{tour_id}")
async def get_tour_by_id(tour_id: int):
    for tour in tours:
        if tour["id"] == tour_id:
            return tour
    raise HTTPException(status_code=404, detail="Тур не найден")

@router.post("/")
async def create_tour(country: str, city: str, price: int, duration: int, hotel: str):
    new_id = max([tour["id"] for tour in tours]) + 1 if tours else 1
    
    new_tour = {
        "id": new_id,
        "country": country,
        "city": city,
        "price": price,
        "duration": duration,
        "hotel": hotel
    }
    
    tours.append(new_tour)
    save_tours(tours)
    return {"message": "Тур добавлен!", "tour": new_tour}

@router.put("/{tour_id}")
async def update_tour(tour_id: int, country: str = None, city: str = None, 
                      price: int = None, duration: int = None, hotel: str = None):
    for index, tour in enumerate(tours):
        if tour["id"] == tour_id:
            if country:
                tours[index]["country"] = country
            if city:
                tours[index]["city"] = city
            if price:
                tours[index]["price"] = price
            if duration:
                tours[index]["duration"] = duration
            if hotel:
                tours[index]["hotel"] = hotel
            
            save_tours(tours)
            return {"message": "Тур обновлен!", "tour": tours[index]}
    
    raise HTTPException(status_code=404, detail="Тур не найден")

@router.delete("/{tour_id}")
async def delete_tour(tour_id: int):
    for index, tour in enumerate(tours):
        if tour["id"] == tour_id:
            deleted_tour = tours.pop(index)
            save_tours(tours)
            return {"message": "Тур удален!", "deleted_tour": deleted_tour}
    
    raise HTTPException(status_code=404, detail="Тур не найден")
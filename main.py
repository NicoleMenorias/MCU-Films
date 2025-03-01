import pandas as pd
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class MCU(BaseModel):
    id: int
    Phase: str
    Film: str
    Year_Release: int
    CinemaScore: str
    Budget: int

# Function to append data to the CSV file
def to_csv(id, Phase, Film, Year_Release, CinemaScore, Budget):
    try:
        df = pd.read_csv("marvel.csv")
    except FileNotFoundError:
        # If the file does not exist, create it with columns
        df = pd.DataFrame(columns=["id", "Phase", "Film", "Year_Release", "CinemaScore", "Budget"])
    
    # Add new row
    df.loc[len(df)] = [id, Phase, Film, Year_Release, CinemaScore, Budget]
    
    # Save it back to the CSV
    df.to_csv('marvel.csv', index=False)
    print("CSV file has been updated.")

@app.post("/mcu/")
async def create_mcu(user_data: MCU):
    id = user_data.id
    Phase = user_data.Phase
    Film = user_data.Film
    Year_Release = user_data.Year_Release
    CinemaScore = user_data.CinemaScore
    Budget = user_data.Budget

    # Call function to save data in CSV
    to_csv(id, Phase, Film, Year_Release, CinemaScore, Budget)
    
    # Return success message and the received data
    return {
        "msg": "We got the data successfully",
        "id": id,
        "Phase": Phase,
        "Film": Film,
        "Year_Release": Year_Release,
        "CinemaScore": CinemaScore,
        "Budget": Budget
    }

@app.get("/movies/")
def get_movies():
        df = pd.read_csv("marvel.csv")
        json_df = json.loads(df.to_json(orient="records"))
        return json_df

@app.get("/random_phase/")
def get_random_phase_movies():
    try:
        df = pd.read_csv("marvel.csv")
        # Get the unique phases
        phases = df["Phase"].unique()
        # Pick a random phase
        random_phase = random.choice(phases)
        # Filter movies from the chosen phase
        random_phase_movies = df[df["Phase"] == random_phase]
        json_df = json.loads(random_phase_movies.to_json(orient="records"))
        return {
            "Random Phase": random_phase,
            "Movies": json_df
        }
    except FileNotFoundError:
        return {"msg": "The file 'marvel.csv' was not found."}
        

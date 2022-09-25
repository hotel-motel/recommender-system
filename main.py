from fastapi import FastAPI
from dotenv import load_dotenv
from os import environ
from databases import Database

app = FastAPI()
load_dotenv('.env')

DATABASE_URL = environ.get('DB_CONNECTION')+'://'+environ.get('DB_USERNAME')+':'+environ.get('DB_PASSWORD')+'@'+environ.get('DB_HOST')+':'+environ.get('DB_PORT')+'/'+environ.get('DB_DATABASE')
database = Database(DATABASE_URL)

@app.get("/hotels/{user_id}")
async def get_recommended_hotels(user_id : str):
    await database.connect()

    query = """
        SELECT DISTINCT(creator_id)
        FROM trips
        WHERE room_id in (
            SELECT id
            FROM rooms
            WHERE hotel_id in (
                SELECT DISTINCT(hotel_id)
                FROM rooms
                WHERE id in (
                    SELECT room_id
                    FROM trips
                    WHERE creator_id="""+user_id+"""
                )
            )
        ) and creator_id <>"""+user_id

    sim_user_ids = await database.fetch_all(query=query)
    return sim_user_ids
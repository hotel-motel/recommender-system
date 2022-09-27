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
    return_count = 4
    await database.connect()
    query = """
        SELECT DISTINCT(trips.creator_id)
        FROM trips INNER JOIN rooms ON trips.room_id=rooms.id
        where rooms.hotel_id in (
            SELECT DISTINCT(rooms.hotel_id)
            FROM trips INNER JOIN rooms ON trips.room_id=rooms.id
            WHERE trips.creator_id = {}
        )
    """.format(user_id)
    # AND trips.creator_id <> {}
    sim_user_ids = await database.fetch_all(query=query)
    sim_user_ids_query = []
    for u in sim_user_ids:
        sim_user_ids_query.append(u.creator_id)

    query="""
        SELECT hotels.id, hotels.name, hotels.image, hotels.star
        FROM hotels
        WHERE hotels.id IN (
            SELECT rooms.hotel_id
            FROM trips INNER JOIN rooms ON trips.room_id=rooms.id
            WHERE creator_id IN {}
            GROUP BY rooms.hotel_id
            ORDER BY count(trips.creator_id) DESC
            LIMIT {}
        )
    """.format(tuple(sim_user_ids_query), str(return_count))
    response = await database.fetch_all(query=query)
    return response
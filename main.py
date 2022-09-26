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
                FROM trips INNER JOIN rooms ON trips.room_id=room_id
                WHERE trips.creator_id = """+user_id+"""
            )
        )"""
        # and creator_id <>"""+user_id
    sim_user_ids = await database.fetch_all(query=query)
    sim_user_ids_query = ""
    
    for u in sim_user_ids:
        sim_user_ids_query=sim_user_ids_query+str(u.creator_id)+","
    sim_user_ids_query=sim_user_ids_query[:-1]

    query="""
        SELECT creator_id, hotel_id
        FROM trips INNER JOIN rooms ON trips.room_id=rooms.id
        WHERE creator_id IN ("""+sim_user_ids_query+""")
         ORDER BY hotel_id
    """
    matrix_sim_user_hotels = await database.fetch_all(query=query)
    weighted = {}
    for h in matrix_sim_user_hotels:
        if(h.hotel_id in weighted):
            weighted[h.hotel_id]=weighted[h.hotel_id]+1
        else:
            weighted[h.hotel_id]=1
    return weighted
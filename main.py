from DB import DB
from fastapi import FastAPI


app = FastAPI()
database = DB().connection


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
        ) AND trips.creator_id <> {}
    """.format(user_id, str(user_id))
    sim_user_ids = await database.fetch_all(query=query)
    sim_user_ids = [u.creator_id for u in sim_user_ids]
    if len(sim_user_ids)<2:
        return 'Data is bald.'
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
    """.format(tuple(sim_user_ids), str(return_count))
    result = await database.fetch_all(query=query)
    database.disconnect()
    return result

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/hotels/")
async def get_recommended_hotels(token : str, db: Session = Depends(get_db)):
    return {"Message": "Hello World :) "}
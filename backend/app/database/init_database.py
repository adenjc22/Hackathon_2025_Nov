from app.database.session import Base, engine
from app.database.models_user import User

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

if __name__ == "__main__":
    init_db()

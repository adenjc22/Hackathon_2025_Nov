from app.database.session import Base, engine
from app.database.models_user import User
from app.database.models_media import Media  # new import
from app.database.models_person import Person, FaceInstance  # new import

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


if __name__ == "__main__":
    init_db()
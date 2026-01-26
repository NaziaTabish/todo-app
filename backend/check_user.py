from sqlmodel import Session, select, create_engine
from src.models.user import User

engine = create_engine("sqlite:///./todoapp.db")

with Session(engine) as session:
    user = session.exec(select(User).where(User.email == "naziakanwal2025@gmail.com")).first()
    if user:
        print(f"User found: {user.email}")
    else:
        print("User NOT found")

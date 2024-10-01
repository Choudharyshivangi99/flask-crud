# In view_data.py
from models import db, User, Item  # Importing models
from app import app  # Replace with your actual app import

def view_data():
    # Query the database for users and items and print them
    users = User.query.all()
    items = Item.query.all()

    print("Users:")
    for user in users:
        print(user.username)

    print("\nItems:")
    for item in items:
        print(f"Name: {item.name}, Description: {item.description}")

if __name__ == '__main__':
    with app.app_context():
        view_data()  
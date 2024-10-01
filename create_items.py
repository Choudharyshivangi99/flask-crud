# In create_items.py
from app import app, bcrypt  # Assuming app.py is where your Flask app is defined
from models import db, User, Item

def add_data():
    users = [
        {'username': 'testuser', 'password': 'testpass'},
        # ... other users
    ]
    items = [
        {'name': 'Item1', 'description': 'A test item'},
        {'name': 'Johnson', 'description': 'powder'},
        {'name': 'Whatman FIlter Paper', 'description': 'Qualigens'},
    ]
    
    for user in users:
        if not User.query.filter_by(username=user['username']).first():
            new_user = User(username=user['username'], password=bcrypt.generate_password_hash(user['password']).decode('utf-8'))
            db.session.add(new_user)
    
    for item in items:
        if not Item.query.filter_by(name=item['name']).first():
            new_item = Item(name=item['name'], description=item['description'])
            db.session.add(new_item)

    db.session.commit()
    print("Data added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_data()  # This line is now correctly indented

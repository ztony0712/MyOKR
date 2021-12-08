# run this file

from app import app, db
from app import views

db.create_all()

# if __name__ == '__main__':
app.run(debug=True)

from app import app
import os

if not os.path.exists("back-end/instance/site.db"):
    from app import db

    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

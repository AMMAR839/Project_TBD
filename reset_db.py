from app import app, db
from models import *

if __name__ == '__main__':
    with app.app_context():
        # Hapus database lama
        db.drop_all()
        print("Database lama berhasil dihapus") 

        
        
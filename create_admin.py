from app import app, db
from models import User

def create_admin(username, password):
    try:
        # Check if admin already exists
        existing_admin = User.query.filter_by(username=username, role='admin').first()
        if existing_admin:
            print(f"Admin dengan username '{username}' sudah ada!")
            return False

        # Create new admin user
        admin = User(username=username, role='admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin '{username}' berhasil dibuat!")
        return True
        
    except Exception as e:
        print(f"Error saat membuat admin: {str(e)}")
        db.session.rollback()
        return False

if __name__ == '__main__':
    with app.app_context():
        # Buat database jika belum ada
        db.create_all()
        
        # Data admin default
        admin_username = 'admin'
        admin_password = 'admin123'
        
        # Buat akun admin
        create_admin(admin_username, admin_password) 
from datetime import datetime
from app.models.user import User
from app.extensions import db, bcrypt

def validate_registration_data(data):
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return {'error': f'{field} is required'}
            
    if len(data['password']) < 8:
        return {'error': 'Password must be at least 8 characters'}
        
    return None

def register_user(data):
    # Validate input data
    validation_error = validate_registration_data(data)
    if validation_error:
        return validation_error

    # Check existing user
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already registered'}
    
    if User.query.filter_by(username=data['username']).first():
        return {'error': 'Username already taken'}
    
    try:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        new_user = User(
            username=data['username'],
            email=data['email'].lower(),  # normalize email
            password_hash=hashed_password,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            role='user',
            status='active',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User registered successfully', 'user_id': new_user.id}
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Registration failed: {str(e)}'}

def authenticate_user(data):
    if not data.get('email') or not data.get('password'):
        return {'error': 'Email and password are required'}

    try:
        user = User.query.filter_by(email=data['email'].lower()).first()
        
        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            return {'error': 'Invalid credentials'}
            
        if user.status != 'active':
            return {'error': 'Account is not active'}

        # Update last login
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        return {'user': user}
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Authentication failed: {str(e)}'}
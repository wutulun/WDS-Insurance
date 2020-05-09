from insurance import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

# Database Structure

class Customer(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    marital_status = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    insurances = db.relationship('Insurance', backref='buyer', lazy=True)

    def __repr__(self):
        return f"Customer('{self.full_name}', '{self.email}'')"

class Insurance(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(1), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    premium = db.Column(db.Numeric(scale=2), nullable=False)
    status = db.Column(db.String(1), nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    
    vehicles = db.relationship('Vehicle', backref='insurance', lazy=True)
    homes = db.relationship('Home', backref='insurance', lazy=True)
    invoices = db.relationship('Invoice', backref='insurance', lazy=True)

    def __repr__(self):
        return f"Insurance('{self.type}')"
        
class Vehicle(db.Model):
    
    vin = db.Column(db.String(20), primary_key=True)
    make_model_year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), nullable=False)
    
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.id'), nullable=False)
    
    drivers = db.relationship('Driver', backref='vhc', lazy=True)

    def __repr__(self):
        return f"Vehicle('{self.vin}', '{self.status}'')"
        
class Driver(db.Model):
    
    license_number = db.Column(db.String(20), primary_key=True)
    driver_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vin'), nullable=False)

    def __repr__(self):
        return f"Driver('{self.license_number}', '{self.driver_name}'')"
        
class Home(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_value = db.Column(db.Numeric(scale=2), nullable=False)
    home_area = db.Column(db.Numeric(scale=2), nullable=False)
    home_type = db.Column(db.String(1), nullable=False)
    
    fire = db.Column(db.Integer, nullable=False)
    security = db.Column(db.Integer, nullable=False)
    swimming_pool = db.Column(db.String(1))
    basement = db.Column(db.Integer, nullable=False)
    
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.id'), nullable=False)

    def __repr__(self):
        return f"Home('{self.purchase_date}', '${self.purchase_value}', '{self.home_area}Sq.ft')"
        
class Invoice(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_date = db.Column(db.Date, nullable=False)
    payment_due_date = db.Column(db.Date, nullable=False)
    invoice_amount = db.Column(db.Numeric(scale=2), nullable=False)
    status = db.Column(db.String(1), nullable=False)
    
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.id'), nullable=False)
    
    payment = db.relationship('Payment', backref='invoice', lazy=True)

    def __repr__(self):
        return f"Invoice('{self.id}', '{self.invoice_date}', '{self.invoice_amount}')"
    
class Payment(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.Date, nullable=False)
    method = db.Column(db.String(1), nullable=False)
    
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)

    def __repr__(self):
        return f"Payment('{self.id}', '{self.payment_date}', '{self.method}')"
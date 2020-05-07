from insurance import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from insurance.forms import RegistrationForm, LoginForm, UpdateAccountForm, SelectInsuranceForm, HomeForm, \
                            AutoForm, VehicleForm
from insurance.models import Customer, Insurance, Vehicle, Driver, Home
from flask_login import login_user, current_user, logout_user, login_required
from decimal import Decimal, ROUND_UP # data processing
import datetime

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(full_name=form.full_name.data, address=form.address.data, 
                            gender=form.gender.data, marital_status=form.marital_status.data,
                            email=form.email.data, password=hashed_pw)
        db.session.add(customer)
        db.session.commit()
        flash('Your account has been created! ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # TODO: add check if insurance is expired
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # update to db
        current_user.address = form.address.data
        current_user.marital_status = form.marital_status.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':   
        # display at first place
        form.address.data = current_user.address
        form.marital_status.data = current_user.marital_status
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    form = SelectInsuranceForm()
    if form.validate_on_submit():
        if 'A' in form.insurance_type.data:
            return redirect(url_for('buy_auto'))
        else:
            return redirect(url_for('buy_home'))
    return render_template('buy.html', title='Buy', form=form)

@app.route('/buy_auto', methods=['GET', 'POST'])
@login_required
def buy_auto():
    form = AutoForm()
    form1 = VehicleForm()
    if form.validate_on_submit():
        insurance = Insurance(start_date=datetime.date.today(), 
                              end_date=datetime.date.today()+datetime.timedelta(days=90), 
                              premium=139.99*3, status='C', type='A', 
                              customer_id=current_user.id)
        
        db.session.add(insurance)
        
        # A Small Trick! Use relationship to write FK and add to session in one line!
        for vhc in form.vehicles:   # form object!
            vehicle = Vehicle(vin=vhc.vin.data, make_model_year=vhc.make_model_year.data, status=vhc.status.data)    # No FK yet.
            insurance.vehicles.append(vehicle)  # Now have FK! And add to session as well!
        
            for dvr in vhc.drivers:
                driver = Driver(license_number=dvr.license_number.data, driver_name=dvr.driver_name.data, birthdate=dvr.birthdate.data)      # No FK yet
                vehicle.drivers.append(driver)  # Now have FK! And add to session as well!
            
        db.session.commit()
        
        return redirect(url_for('account'))
    
    return render_template('buy_auto.html', title='Buy-auto', form=form, form1=form1)

@app.route('/buy_home', methods=['GET', 'POST'])
@login_required
def buy_home():
    form = HomeForm()
    if form.validate_on_submit():
        insurance = Insurance(type='H', customer_id=current_user.id)
        db.session.add(insurance)
        db.session.commit()
        home = Home(purchase_date=form.purchase_date.data, type=form.type.data,
                    purchase_value=form.purchase_value.data.quantize(Decimal('.01'), rounding=ROUND_UP),
                    home_area=form.home_area.data.quantize(Decimal('.01'), rounding=ROUND_UP),     
                    fire=form.fire.data, security=form.security.data,
                    swimming_pool=form.swimming_pool.data, basement=form.basement.data,
                    insurance_id=insurance.id)
        db.session.add(home)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('buy_home.html', title='Buy-home', form=form)

@app.route('/details/<insurance_id>')
def details(insurance_id):
    print(insurance_id)
    insurance = Insurance.query.get(insurance_id)
    return render_template('details.html', title='details', insurance=insurance)

@app.route('/hhh/<name>')
def hhh(name):
    return 'name'
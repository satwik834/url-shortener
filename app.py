from flask import Flask, request,session, redirect,jsonify, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from helpers import base62_decode,base62_encode
from database import db
from functools import wraps
from models import URLMap,User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:234856@localhost/urls'
app.config['SECRET_KEY'] = 'top_secret_shit'


db.init_app(app)





with app.app_context():
    db.create_all()

    


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({"Error": "Email already exists"}), 409

        user = User(username=username, email=email)
        user.set_password(password)  # This sets the hashed password

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect after successful registration

    return render_template('register.html')




@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully','success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')





def login_required(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        return func(*args,**kwargs)
    return decorated_function





@app.route('/logout',methods=['POST'])
@login_required
def logout():
    session.clear()
    flash("you are logged out",'info')
    return redirect(url_for('login'))





@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = User.query.get(user_id)
    urls =  URLMap.query.filter_by(user_id=user_id).all()
    urls_with_short=[]
    for url in urls:
        short_code = base62_encode(url.id)
        short_url = request.host_url + short_code
        urls_with_short.append((url,short_url))
    return render_template('dashboard.html',user=user,urls=urls_with_short)
    

    
@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    original_url = request.form.get('original_url')

    # Check if URL already exists for this user (optional)
    existing_url = URLMap.query.filter_by(original_url=original_url, user_id=session['user_id']).first()
    if existing_url:
        return redirect(url_for('dashboard'))

    new_url = URLMap(original_url=original_url,user_id=session['user_id'])
    db.session.add(new_url)
    db.session.commit()

    return redirect(url_for('dashboard'))



@app.route('/', methods=['GET','POST'])
def index():
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        if not original_url:
            flash("Please enter a URL", "danger")
            return redirect(url_for('index'))
        
        existing = URLMap.query.filter_by(original_url=original_url).first()
        if existing:
            short_id = base62_encode(existing.id)
            
        else:
            new_url = URLMap(original_url=original_url)
            db.session.add(new_url)
            db.session.commit()
            short_id = base62_encode(new_url.id)
        short_url = request.host_url + short_id

        return render_template('index.html',short_url=short_url)
    return render_template('index.html')




@app.route('/<short_id>')
def redirect_short_url(short_id):
    try:
        id = base62_decode(short_id)
    except ValueError:
        flash("invalid short url","danger")
        return redirect(url_for('index'))
    url_map = URLMap.query.get_or_404(id)
    url_map.clicks += 1
    db.session.commit()
    return redirect(url_map.original_url)

if __name__ == '__main__':
    app.run(debug=True)
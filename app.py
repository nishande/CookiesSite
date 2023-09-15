from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'supersecretkey'  # for flash messages and session
global hashed_pw
hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')

# Dummy in-memory database
db = {
    "content": "",
    "valid_upto": "",
    "admin_message": ""
}


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/udemy-cookies')
def udemy_cookies():
    return render_template('udemy-cookies.html', content=db['content'], valid_upto=db['valid_upto'], admin_message=db.get('admin_message', ''))



@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if 'admin' in session:
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'Save':
                db['content'] = request.form.get('content')
                db['valid_upto'] = request.form.get('date')
                if db['valid_upto']:
                    # Convert date from YYYY-MM-DD to DD/MM/YYYY
                    date_obj = datetime.strptime(db['valid_upto'], '%Y-%m-%d')
                    db['valid_upto'] = date_obj.strftime('%d/%m/%Y')
                flash('Content saved successfully!', 'success')
                
            elif action == 'Clear':
                db['content'] = ""
                db['valid_upto'] = ""
                flash('Content cleared.', 'success')

            elif action == 'SaveMessage':
                db['admin_message'] = request.form.get('admin_message')
                flash('Message saved successfully!', 'success')

            elif action == 'ClearMessage':
                db['admin_message'] = ""
                flash('Message cleared.', 'success')
                
        return render_template('admin-login.html', content=db['content'], date=db.get('valid_upto'), admin_message=db.get('admin_message', ''))
    
    else:
        if request.method == 'POST':
            if bcrypt.check_password_hash(hashed_pw, request.form.get('password')):
                session['admin'] = True
                return redirect(url_for('admin_login'))
            else:
                flash('Invalid credentials.', 'danger')
                
        return render_template('admin-auth.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))

@app.route('/how-to-use')
def how_to_use():
    return render_template('how-to-use.html')



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

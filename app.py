import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'ezto'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'sanrevsha@gmail.com'
app.config['MAIL_PASSWORD'] = 'guxwqpqbqmpchfxl'  # Replace with the generated app password

mail = Mail(app)

IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), 'images ezto')

@app.route('/images/<path:filename>')
def custom_images(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and user[2] == password:  # Assuming password is stored in the third column
            print("Login successful for user:", username)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            print("Invalid login attempt for user:", username)
    
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        app_name = request.form['appName']
        bundle_id = request.form['bundleId']
        
        if not bundle_id:  
            flash('Bundle ID is required!')
            return redirect(url_for('update'))

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO app_info (app_name, bundle_id) VALUES (%s, %s)", (app_name, bundle_id))
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Error inserting into app_info table: {e}")
            flash('Error occurred while saving data.')
            return redirect(url_for('update'))

        # Sending email notification
        try:
            msg = Message('Update Submitted', 
                          sender='sanrevsha@gmail.com', 
                          recipients=['sanrevsha@gmail.com'])  # Replace with a valid email address
            msg.html = render_template('email.html', app_name=app_name, bundle_id=bundle_id)
            mail.send(msg)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")

        return redirect(url_for('update1a'))

    return render_template('update.html')


@app.route('/update1a', methods=['GET', 'POST'])
def update1a():
    if request.method == 'POST':
        primary_color = request.form.get('primaryColor')
        font_details = request.form.get('fontDetails')

        print(f"Received Data - Primary Color: {primary_color}, Font Details: {font_details}")

        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO app_design (primary_color, font_details)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    primary_color = VALUES(primary_color),
                    font_details = VALUES(font_details)
            """
            cursor.execute(query, (primary_color, font_details))
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Error inserting into app_design table: {e}")
            flash('Error occurred while saving data.')

            # Sending email notification
        try:
            msg = Message('Update Submitted', 
                          sender='sanrevsha@gmail.com', 
                          recipients=['sanrevsha@gmail.com'])  # Replace with a valid email address
            msg.html = render_template('email.html', primary_color=primary_color, font_details=font_details)
            mail.send(msg)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")

        return redirect(url_for('update1b'))

    return render_template('update1a.html')

@app.route('/update1b', methods=['GET', 'POST'])
def update1b():
    if request.method == 'POST':
        return redirect(url_for('update2'))

    return render_template('update1b.html')

@app.route('/update2', methods=['GET', 'POST'])
def update2():
    if request.method == 'POST':
        privacy_url = request.form.get('privacyUrl')
        terms_url = request.form.get('termsUrl')

        # Insert or update data in the database
        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO app_privacy_terms (privacy_url, terms_url)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    privacy_url = VALUES(privacy_url),
                    terms_url = VALUES(terms_url)
            """
            cursor.execute(query, (privacy_url, terms_url))
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Database error: {e}")
            flash('Database error')
            return redirect(url_for('update2'))
        # Sending email notification
        try:
            msg = Message('Update Submitted', 
                          sender='sanrevsha@gmail.com', 
                          recipients=['sanrevsha@gmail.com'])  # Replace with a valid email address
            msg.html = render_template('email.html', privacy_url=privacy_url, terms_url=terms_url)
            mail.send(msg)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")

        return redirect(url_for('update2a'))

    return render_template('update2.html')

@app.route('/update2a', methods=['GET', 'POST'])
def update2a():
    if request.method == 'POST':
        # Handle form submission logic here, e.g., save data to database
        
        # Redirect to the next step or confirmation page
        return redirect(url_for('submit'))

    # Render the update2a.html template for GET requests
    return render_template('update2a.html')

@app.route('/submit')
def submit():
    return render_template('submit.html', message="Form submitted successfully!")

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        phone = request.form['phone']
        business_type = request.form['business_type']
        company_size = request.form['company_size']
        app_purpose = request.form['app_purpose']
        target_audience = request.form['target_audience']
        platform = request.form['platform']
        feature_requirements = request.form['feature_requirements']
        design_preferences = request.form['design_preferences']
        preferred_languages = request.form['preferred_languages']
        api_requirements = request.form['api_requirements']
        data_storage = request.form['data_storage']
        security_requirements = request.form['security_requirements']
        theme_preferences = request.form['theme_preferences']
        custom_fields = request.form['custom_fields']
        notification_preferences = request.form['notification_preferences']

        # Store form data in session
        session['user_data'] = request.form.to_dict()

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO register_details (username, password, email, organisation, address, city, state, country, postalcode, phone, business_type, company_size, app_purpose, target_audience, platform, feature_requirements, design_preferences, preferred_languages, api_requirements, data_storage, security_requirements, theme_preferences, custom_fields, notification_preferences) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        (username, password, email, organisation, address, city, state, country, postalcode, phone, business_type, company_size, app_purpose, target_audience, platform, feature_requirements, design_preferences, preferred_languages, api_requirements, data_storage, security_requirements, theme_preferences, custom_fields, notification_preferences))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('user_details'))

    return render_template('register.html')

@app.route('/user_details')
def user_details():
    user_data = session.get('user_data')
    return render_template('user_details.html', user_data=user_data)

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/qa')
def qa():
    return render_template('qa.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

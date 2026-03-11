# from flask import Flask, render_template, request, redirect
# import mysql.connector

# app = Flask(__name__)

# # MySQL Connection
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="krish",   # your MySQL password
#     database="event_management"
# )

# cursor = db.cursor()

# # ---------------- HOME ----------------
# @app.route('/')
# def index():
#     return render_template('index.html')


# # ---------------- REGISTER USER ----------------
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']

#         sql = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"
#         values = (name, email, phone)
#         cursor.execute(sql, values)
#         db.commit()

#         return redirect('/')

#     return render_template('register.html')


# # ---------------- BOOK EVENT ----------------
# @app.route('/book', methods=['GET', 'POST'])
# def book_event():
#     if request.method == 'POST':
#         user_id = request.form['user_id']
#         event_type_id = request.form['event_type']
#         venue_id = request.form['venue']
#         event_date = request.form['event_date']
#         selected_services = request.form.getlist('services')

#         # Fetch event base price
#         cursor.execute("SELECT base_price FROM event_types WHERE event_type_id=%s", (event_type_id,))
#         base_price = cursor.fetchone()[0]

#         # Fetch venue price
#         cursor.execute("SELECT price FROM venues WHERE venue_id=%s", (venue_id,))
#         venue_price = cursor.fetchone()[0]

#         total = base_price + venue_price

#         # Insert booking first (temporary total = 0)
#         booking_sql = """INSERT INTO bookings 
#                          (user_id, event_type_id, venue_id, event_date, total_amount)
#                          VALUES (%s, %s, %s, %s, %s)"""
#         booking_values = (user_id, event_type_id, venue_id, event_date, 0)
#         cursor.execute(booking_sql, booking_values)
#         db.commit()

#         booking_id = cursor.lastrowid

#         # Handle selected services
#         for service_id in selected_services:
#             quantity = int(request.form.get(f'quantity_{service_id}', 1))

#             cursor.execute("SELECT price FROM services WHERE service_id=%s", (service_id,))
#             service_price = cursor.fetchone()[0]

#             subtotal = service_price * quantity
#             total += subtotal

#             service_sql = """INSERT INTO booking_services 
#                              (booking_id, service_id, quantity, subtotal)
#                              VALUES (%s, %s, %s, %s)"""
#             service_values = (booking_id, service_id, quantity, subtotal)
#             cursor.execute(service_sql, service_values)

#         # Update final total in bookings table
#         cursor.execute("UPDATE bookings SET total_amount=%s WHERE booking_id=%s",
#                        (total, booking_id))
#         db.commit()

#         return redirect('/')

#     # Fetch dropdown data
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()

#     cursor.execute("SELECT * FROM event_types")
#     event_types = cursor.fetchall()

#     cursor.execute("SELECT * FROM venues")
#     venues = cursor.fetchall()

#     cursor.execute("SELECT * FROM services")
#     services = cursor.fetchall()

#     return render_template('book_event.html',
#                            users=users,
#                            event_types=event_types,
#                            venues=venues,
#                            services=services)


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="krish",
    database="event_management"
)

cursor = db.cursor()

# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- USERS ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute("INSERT INTO users (name,email,phone) VALUES (%s,%s,%s)",
                       (name,email,phone))
        db.commit()
        return redirect('/')

    return render_template('register.html')

# ---------------- EVENT TYPES ----------------
@app.route('/add_event_type', methods=['GET','POST'])
def add_event_type():
    if request.method == 'POST':
        event_name = request.form['event_name']
        base_price = request.form['base_price']

        cursor.execute("INSERT INTO event_types (event_name,base_price) VALUES (%s,%s)",
                       (event_name,base_price))
        db.commit()
        return redirect('/')

    return render_template('add_event_type.html')

# ---------------- VENUES ----------------
@app.route('/add_venue', methods=['GET','POST'])
def add_venue():
    if request.method == 'POST':
        venue_name = request.form['venue_name']
        location = request.form['location']
        price = request.form['price']

        cursor.execute("INSERT INTO venues (venue_name,location,price) VALUES (%s,%s,%s)",
                       (venue_name,location,price))
        db.commit()
        return redirect('/')

    return render_template('add_venue.html')

# ---------------- SERVICES ----------------
@app.route('/add_service', methods=['GET','POST'])
def add_service():
    if request.method == 'POST':
        service_name = request.form['service_name']
        price = request.form['price']

        cursor.execute("INSERT INTO services (service_name,price) VALUES (%s,%s)",
                       (service_name,price))
        db.commit()
        return redirect('/')

    return render_template('add_service.html')

# ---------------- BOOK EVENT ----------------
@app.route('/book', methods=['GET','POST'])
def book_event():
    if request.method == 'POST':
        user_id = request.form['user_id']
        event_type_id = request.form['event_type']
        venue_id = request.form['venue']
        event_date = request.form['event_date']
        selected_services = request.form.getlist('services')

        cursor.execute("SELECT base_price FROM event_types WHERE event_type_id=%s",(event_type_id,))
        base_price = cursor.fetchone()[0]

        cursor.execute("SELECT price FROM venues WHERE venue_id=%s",(venue_id,))
        venue_price = cursor.fetchone()[0]

        total = base_price + venue_price

        cursor.execute("""INSERT INTO bookings 
                          (user_id,event_type_id,venue_id,event_date,total_amount)
                          VALUES (%s,%s,%s,%s,%s)""",
                       (user_id,event_type_id,venue_id,event_date,0))
        db.commit()

        booking_id = cursor.lastrowid

        for service_id in selected_services:
            quantity = int(request.form.get(f'quantity_{service_id}',1))

            cursor.execute("SELECT price FROM services WHERE service_id=%s",(service_id,))
            service_price = cursor.fetchone()[0]

            subtotal = service_price * quantity
            total += subtotal

            cursor.execute("""INSERT INTO booking_services
                              (booking_id,service_id,quantity,subtotal)
                              VALUES (%s,%s,%s,%s)""",
                           (booking_id,service_id,quantity,subtotal))

        cursor.execute("UPDATE bookings SET total_amount=%s WHERE booking_id=%s",
                       (total,booking_id))
        db.commit()

        return redirect('/')

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM event_types")
    event_types = cursor.fetchall()

    cursor.execute("SELECT * FROM venues")
    venues = cursor.fetchall()

    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    return render_template('book_event.html',
                           users=users,
                           event_types=event_types,
                           venues=venues,
                           services=services)


if __name__ == '__main__':
    app.run(debug=True)
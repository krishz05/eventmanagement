from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="krish",   # your MySQL password
    database="event_management"
)

cursor = db.cursor()

# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')


# ---------------- REGISTER USER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        sql = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"
        values = (name, email, phone)
        cursor.execute(sql, values)
        db.commit()

        return redirect('/')

    return render_template('register.html')


# ---------------- BOOK EVENT ----------------
@app.route('/book', methods=['GET', 'POST'])
def book_event():
    if request.method == 'POST':
        user_id = request.form['user_id']
        event_type_id = request.form['event_type']
        venue_id = request.form['venue']
        event_date = request.form['event_date']
        selected_services = request.form.getlist('services')

        # Fetch event base price
        cursor.execute("SELECT base_price FROM event_types WHERE event_type_id=%s", (event_type_id,))
        base_price = cursor.fetchone()[0]

        # Fetch venue price
        cursor.execute("SELECT price FROM venues WHERE venue_id=%s", (venue_id,))
        venue_price = cursor.fetchone()[0]

        total = base_price + venue_price

        # Insert booking first (temporary total = 0)
        booking_sql = """INSERT INTO bookings 
                         (user_id, event_type_id, venue_id, event_date, total_amount)
                         VALUES (%s, %s, %s, %s, %s)"""
        booking_values = (user_id, event_type_id, venue_id, event_date, 0)
        cursor.execute(booking_sql, booking_values)
        db.commit()

        booking_id = cursor.lastrowid

        # Handle selected services
        for service_id in selected_services:
            quantity = int(request.form.get(f'quantity_{service_id}', 1))

            cursor.execute("SELECT price FROM services WHERE service_id=%s", (service_id,))
            service_price = cursor.fetchone()[0]

            subtotal = service_price * quantity
            total += subtotal

            service_sql = """INSERT INTO booking_services 
                             (booking_id, service_id, quantity, subtotal)
                             VALUES (%s, %s, %s, %s)"""
            service_values = (booking_id, service_id, quantity, subtotal)
            cursor.execute(service_sql, service_values)

        # Update final total in bookings table
        cursor.execute("UPDATE bookings SET total_amount=%s WHERE booking_id=%s",
                       (total, booking_id))
        db.commit()

        return redirect('/')

    # Fetch dropdown data
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
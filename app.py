from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Data storage files
ORDERS_FILE = 'orders.json'
BOOKINGS_FILE = 'bookings.json'
CONTACTS_FILE = 'contacts.json'

# Initialize data files if they don't exist
def init_files():
    for file in [ORDERS_FILE, BOOKINGS_FILE, CONTACTS_FILE]:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump([], f)

init_files()

# Helper functions
def read_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return []

def write_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Serve static files (images, CSS, JS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# API Routes for receiving data from customer website
@app.route('/api/order', methods=['POST'])
def receive_order():
    try:
        data = request.json
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['status'] = 'Pending'
        data['id'] = len(read_data(ORDERS_FILE)) + 1
        
        orders = read_data(ORDERS_FILE)
        orders.append(data)
        write_data(ORDERS_FILE, orders)
        
        return jsonify({'success': True, 'message': 'Order received', 'order_id': data['id']}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/booking', methods=['POST'])
def receive_booking():
    try:
        data = request.json
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['status'] = 'Confirmed'
        data['id'] = len(read_data(BOOKINGS_FILE)) + 1
        
        bookings = read_data(BOOKINGS_FILE)
        bookings.append(data)
        write_data(BOOKINGS_FILE, bookings)
        
        return jsonify({'success': True, 'message': 'Booking received', 'booking_id': data['id']}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/contact', methods=['POST'])
def receive_contact():
    try:
        data = request.json
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['id'] = len(read_data(CONTACTS_FILE)) + 1
        
        contacts = read_data(CONTACTS_FILE)
        contacts.append(data)
        write_data(CONTACTS_FILE, contacts)
        
        return jsonify({'success': True, 'message': 'Message received'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Admin Dashboard Routes
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

# Public site routes (serve the HTML pages under templates/)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/order')
def order_page():
    return render_template('order.html')

@app.route('/booking')
def booking_page():
    return render_template('booking.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/admin/orders')
def get_orders():
    orders = read_data(ORDERS_FILE)
    return jsonify(orders)

@app.route('/admin/bookings')
def get_bookings():
    bookings = read_data(BOOKINGS_FILE)
    return jsonify(bookings)

@app.route('/admin/contacts')
def get_contacts():
    contacts = read_data(CONTACTS_FILE)
    return jsonify(contacts)

@app.route('/admin/update-order-status', methods=['POST'])
def update_order_status():
    try:
        data = request.json
        order_id = data['id']
        new_status = data['status']
        
        orders = read_data(ORDERS_FILE)
        for order in orders:
            if order['id'] == order_id:
                order['status'] = new_status
                break
        
        write_data(ORDERS_FILE, orders)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/admin/update-booking-status', methods=['POST'])
def update_booking_status():
    try:
        data = request.json
        booking_id = data['id']
        new_status = data['status']
        
        bookings = read_data(BOOKINGS_FILE)
        for booking in bookings:
            if booking['id'] == booking_id:
                booking['status'] = new_status
                break
        
        write_data(BOOKINGS_FILE, bookings)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
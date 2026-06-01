# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv

# # Load email credentials from .env file
# load_dotenv()

# app = Flask(__name__)
# # Allow your local HTML files to communicate with this server
# CORS(app)

# # --- HELPER FUNCTION: SEND EMAIL ---
# def send_email(subject, body):
#     sender_email = os.getenv("EMAIL_ADDRESS")
#     sender_password = os.getenv("EMAIL_PASSWORD")
#     receiver_email = "aquib.aadee@gmail.com"

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         # Connect to Gmail's secure SMTP server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(msg)
#         server.quit()
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return False


# # --- ROUTE 1: CONTACT FORM ENQUIRY ---
# @app.route('/api/contact', methods=['POST'])
# def handle_contact():
#     data = request.json
    
#     # Extract data from the request
#     name = data.get('name', 'N/A')
#     phone = data.get('phone', 'N/A')
#     email = data.get('email', 'N/A')
#     course = data.get('course', 'N/A')
#     message = data.get('message', 'N/A')

#     # Format the email body
#     email_body = f"""
#     New General Enquiry from Website!
    
#     Name: {name}
#     Phone: {phone}
#     Email: {email}
#     Course Interest: {course}
    
#     Message: 
#     {message}
#     """
    
#     # Send email and return response
#     if send_email("Mathemagix: New Contact Enquiry", email_body):
#         return jsonify({"status": "success", "message": "Enquiry submitted successfully!"}), 200
#     else:
#         return jsonify({"status": "error", "message": "Failed to send enquiry."}), 500


# # --- ROUTE 2: BOOK DEMO FORM ---
# @app.route('/api/demo', methods=['POST'])
# def handle_demo():
#     data = request.json
    
#     # Extract data from the request
#     name = data.get('name', 'N/A')
#     phone = data.get('phone', 'N/A')
#     course = data.get('course', 'N/A')

#     # Format the email body
#     email_body = f"""
#     New Demo Class Booking!
    
#     Student Name: {name}
#     Phone Number: {phone}
#     Target Course: {course}
    
#     Please call them ASAP to schedule their demo!
#     """
    
#     # Send email and return response
#     if send_email("Mathemagix: NEW DEMO BOOKING", email_body):
#         return jsonify({"status": "success", "message": "Demo booked successfully!"}), 200
#     else:
#         return jsonify({"status": "error", "message": "Failed to book demo."}), 500


# if __name__ == '__main__':
#     # Run the server locally on port 5000
#     app.run(debug=True, port=5000)

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime

# Load credentials from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- DATABASE SETUP ---
# Connect to MongoDB using the URI from your .env file
client = MongoClient(os.getenv("MONGO_URI"))
# Create a database called 'mathemagix_db'
db = client['mathemagix_db']
# Create two collections (like tables/folders) for your data
contact_collection = db['contact_enquiries']
demo_collection = db['demo_bookings']

# --- HELPER FUNCTION: SEND EMAIL ---
def send_email(subject, body):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = "aquib.aadee@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Added timeout=5 so it catches the Render block instead of crashing!
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# --- ROUTE 0: HEALTH CHECK (The Front Door) ---
@app.route('/', methods=['GET'])
def home():
    return "Mathemagix API is running perfectly! 🚀"

# --- ROUTE 1: CONTACT FORM ENQUIRY ---
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.json
    
    name = data.get('name', 'N/A')
    phone = data.get('phone', 'N/A')
    email = data.get('email', 'N/A')
    course = data.get('course', 'N/A')
    message = data.get('message', 'N/A')
    
    # 1. Save to Database
    contact_collection.insert_one({
        "name": name,
        "phone": phone,
        "email": email,
        "course": course,
        "message": message,
        "date_submitted": datetime.datetime.now()
    })

    # 2. Send Email
    # email_body = f"New Enquiry!\nName: {name}\nPhone: {phone}\nEmail: {email}\nCourse: {course}\nMessage: {message}"
    
    # if send_email("Mathemagix: New Contact Enquiry", email_body):
    #     return jsonify({"status": "success", "message": "Enquiry submitted successfully!"}), 200
    # else:
    #     return jsonify({"status": "error", "message": "Failed to send enquiry."}), 500 

    # 2. Send Email (Will likely fail on Render Free Tier, but that's okay!)
    email_body = f"New Enquiry!\nName: {name}\nPhone: {phone}\nEmail: {email}\nCourse: {course}\nMessage: {message}"
    send_email("Mathemagix: New Contact Enquiry", email_body)
    
    # 3. Always return success to the student because the DB save worked!
    return jsonify({"status": "success", "message": "Enquiry submitted successfully!"}), 200

# --- ROUTE 2: BOOK DEMO FORM ---
@app.route('/api/demo', methods=['POST'])
def handle_demo():
    data = request.json
    
    name = data.get('name', 'N/A')
    phone = data.get('phone', 'N/A')
    course = data.get('course', 'N/A')

    # 1. Save to Database
    demo_collection.insert_one({
        "name": name,
        "phone": phone,
        "course": course,
        "date_submitted": datetime.datetime.now()
    })

    # # 2. Send Email
    # email_body = f"New Demo Booking!\nStudent Name: {name}\nPhone: {phone}\nTarget Course: {course}"
    
    # if send_email("Mathemagix: NEW DEMO BOOKING", email_body):
    #     return jsonify({"status": "success", "message": "Demo booked successfully!"}), 200
    # else:
    #     return jsonify({"status": "error", "message": "Failed to book demo."}), 500 

    # 2. Send Email (Will likely fail on Render Free Tier, but that's okay!)
    email_body = f"New Demo Booking!\nStudent Name: {name}\nPhone: {phone}\nTarget Course: {course}"
    send_email("Mathemagix: NEW DEMO BOOKING", email_body)
    
    # 3. Always return success to the student because the DB save worked!
    return jsonify({"status": "success", "message": "Demo booked successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify, render_template
import requests
import smtplib

app = Flask(__name__, template_folder="templates")

# PayPal API Credentials (Use Sandbox First)
PAYPAL_CLIENT_ID = "YOUR_PAYPAL_CLIENT_ID"
PAYPAL_SECRET = "YOUR_PAYPAL_SECRET"
PAYPAL_API_URL = "https://api-m.sandbox.paypal.com"  # Use sandbox for testing

# Email Sending Function
def send_email(email, download_link):
    sender_email = "your-email@example.com"
    sender_password = "your-email-password"

    subject = "Your eBook Download"
    body = f"Thank you for your purchase! Click the link to download your eBook: {download_link}"

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message)

# Home Route (Loads HTML Page)
@app.route('/')
def home():
    return render_template("index.html")

# Verify PayPal Payment
@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    paypal_order_id = data['paypal_order_id']
    email = data['email']

    # Get PayPal Access Token
    auth_response = requests.post(
        f"{PAYPAL_API_URL}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="grant_type=client_credentials"
    )
    access_token = auth_response.json().get("access_token")

    # Verify PayPal Order
    payment_response = requests.get(
        f"{PAYPAL_API_URL}/v2/checkout/orders/{paypal_order_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if payment_response.status_code == 200:
        order_data = payment_response.json()
        if order_data["status"] == "COMPLETED":
            send_email(email, "https://yourwebsite.com/downloads/ebook.pdf")
            return jsonify({"success": True})
        else:
            return jsonify({"success": False}), 400
    else:
        return jsonify({"success": False}), 400

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))  # Use Render's PORT
app.run(host="0.0.0.0", port=port, debug=True)
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/buy", methods=["POST"])
def buy():
    email = request.form.get("email")
    if email:
        return f"Payment process started for {email}"  # Placeholder message
    return "Error: Email not provided"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SENDER_EMAIL = "priyankaslate007@gmail.com"  # Your Gmail
SENDER_PASSWORD = "hram fkbf rnnb udmi"  # App password 

RECEIVER_EMAIL = "dhasdivya7@gmail.com" #for testing mine

# Create message
message = MIMEMultipart()
message['From'] = SENDER_EMAIL
message['To'] = RECEIVER_EMAIL
message['Subject'] = "Test Email from Python"

# Email body
body = "Hello! This is a test email sent from Priyanka."
message.attach(MIMEText(body, 'plain'))

# Send email
try:
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure connection
    
    # Login
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    # Send email
    server.send_message(message)
    
    print("✅ Email sent successfully!")
    
    server.quit()
    
except Exception as e:
    print(f"❌ Error: {e}")
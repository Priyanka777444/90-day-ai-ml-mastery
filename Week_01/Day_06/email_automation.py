"""
Email Automation System
Built by Priyanka
Day 6 Project
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime 
import time
import csv
import os
from dotenv import load_dotenv

# Email configuration
SENDER_EMAIL = "priyankaslate007@gmail.com"
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')

# If password not in environment, ask user
if SENDER_PASSWORD is None:
    print("\n⚠️ App password not found in environment variables.")
    print("(To set it permanently: set SENDER_PASSWORD=your_password)")
    SENDER_PASSWORD = input("\nEnter your Gmail App Password: ").strip()

# Verify password exists
if not SENDER_PASSWORD:
    print("❌ No password provided. Cannot send emails.")
    exit()

# Storage
sent_log = []
contacts = []

# Rest of your code...

def send_simple_email():
    """Send a simple text email"""
    print("\n--- SEND SIMPLE EMAIL ---")
    
    # Ask for receiver inside function
    receiver = input("Receiver email: ").strip()
    subject = input("Subject: ").strip()
    
    print("Email body (type 'END' on a new line to finish):")
    body_lines = []
    while True:
        line = input()
        if line == "END":
            break
        body_lines.append(line)
    
    body = "\n".join(body_lines)
    
    # Create message
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))
    
    # Send
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print("\n✅ Email sent successfully!")
        
        # Log
        sent_log.append({
            'to': receiver,
            'subject': subject,
            'sent_at': str(datetime.now()),
            'status': 'Success'
        })
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sent_log.append({
            'to': receiver,
            'subject': subject,
            'sent_at': str(datetime.now()),
            'status': f'Failed: {e}'
        })

def send_html_email():
    """Send HTML formatted email"""
    print("\n--- SEND HTML EMAIL ---")
    
    receiver = input("Receiver email: ").strip()
    subject = input("Subject: ").strip()
    
    # HTML content
    html_content = f"""
    <html>
    <body>
        <h1 style="color: #2e6c80;">Hello!</h1>
        <p>This is an <b>HTML</b> email sent via automation by Priyanka.</p>
        <p>Sent on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <a href="https://google.com" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Click Here</a>
    </body>
    </html>
    """
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = receiver
    
    # Attach HTML content
    message.attach(MIMEText(html_content, "html"))
    
    # Send
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print("✅ HTML email sent successfully!")
        
        sent_log.append({
            'to': receiver,
            'subject': subject,
            'type': 'HTML',
            'sent_at': str(datetime.now()),
            'status': 'Success'
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")

def send_with_attachment():
    """Send email with file attachment"""
    print("\n--- SEND EMAIL WITH ATTACHMENT ---")
    
    receiver = input("Receiver email: ").strip()
    subject = input("Subject: ").strip()
    
    print("Email body (type 'END' to finish):")
    body_lines = []
    while True:
        line = input()
        if line == "END":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)
    
    # Ask for file path
    file_path = input("File path to attach: ").strip()
    
    if not os.path.exists(file_path):
        print(f"❌ File '{file_path}' not found!")
        return
    
    # Create message
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver
    message['Subject'] = subject
    
    # Add body
    message.attach(MIMEText(body, 'plain'))
    
    # Attach file
    try:
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        # Encode to base64
        encoders.encode_base64(part)
        
        # Add header
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(file_path)}'
        )
        
        message.attach(part)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print(f"\n✅ Email sent with attachment '{os.path.basename(file_path)}'!")
        
        sent_log.append({
            'to': receiver,
            'subject': subject,
            'attachment': os.path.basename(file_path),
            'sent_at': str(datetime.now()),
            'status': 'Success'
        })
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sent_log.append({
            'to': receiver,
            'subject': subject,
            'sent_at': str(datetime.now()),
            'status': f'Failed: {e}'
        })

def send_bulk_emails():
    """Send email to multiple recipients"""
    print("\n--- SEND BULK EMAILS ---")
    
    subject = input("Subject: ").strip()
    
    print("Email body (type 'END' to finish):")
    body_lines = []
    while True:
        line = input()
        if line == "END":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)
    
    # Get recipients
    print("\nEnter recipient emails (one per line, 'DONE' to finish):")
    recipients = []
    while True:
        email = input().strip()
        if email == "DONE":
            break
        if email and '@' in email:
            recipients.append(email)
    
    if len(recipients) == 0:
        print("No recipients!")
        return
    
    print(f"\nSending to {len(recipients)} recipient(s)...")
    
    success = 0
    failed = 0
    
    for recipient in recipients:
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = SENDER_EMAIL
            message['To'] = recipient
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            # Send
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
            server.quit()
            
            print(f"  ✅ Sent to {recipient}")
            success += 1
            
            sent_log.append({
                'to': recipient,
                'subject': subject,
                'sent_at': str(datetime.now()),
                'status': 'Success'
            })
            
        except Exception as e:
            print(f"  ❌ Failed to {recipient}: {e}")
            failed += 1
    
    print(f"\n✅ Success: {success}")
    print(f"❌ Failed: {failed}")


def manage_contacts():
    """Manage email contact list"""
    global contacts
    
    print("\n--- MANAGE CONTACTS ---")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Delete Contact")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "1":
        # Add contact
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        
        contacts.append({'name': name, 'email': email})
        print(f"✅ Added {name} ({email})")
    
    elif choice == "2":
        # View contacts
        if len(contacts) == 0:
            print("No contacts yet!")
            return
        
        print("\n--- CONTACTS ---")
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['name']} - {contact['email']}")
    
    elif choice == "3":
        # Delete contact
        if len(contacts) == 0:
            print("No contacts to delete!")
            return
        
        # Show contacts
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['name']} - {contact['email']}")
        
        try:
            index = int(input("\nEnter number to delete: ")) - 1
            if 0 <= index < len(contacts):
                removed = contacts.pop(index)
                print(f"✅ Deleted {removed['name']}")
            else:
                print("Invalid number!")
        except ValueError:
            print("Enter a valid number!")


def view_sent_log():
    """View email send history"""
    if len(sent_log) == 0:
        print("\nNo emails sent yet!")
        return
    
    print("\n--- SENT EMAIL LOG ---")
    print(f"Total: {len(sent_log)} email(s)")
    print("-" * 80)
    
    for i, log in enumerate(sent_log, 1):
        print(f"\n{i}.")
        print(f"  To: {log['to']}")
        print(f"  Subject: {log['subject']}")
        print(f"  Sent: {log['sent_at']}")
        print(f"  Status: {log['status']}")
    
    print("-" * 80)
    
    # Summary
    success = sum(1 for log in sent_log if log['status'] == 'Success')
    failed = len(sent_log) - success
    
    print(f"\nSuccess: {success}")
    print(f"Failed: {failed}")



def main():
    print("Welcome to Email Automation System by Priyanka!")
    print(f"Sender: {SENDER_EMAIL}")
    
    while True:
        print("\n1. Send Simple Email")
        print("2. Send HTML Email")
        print("3. Send Email with Attachment")
        print("4. Send Bulk Emails")
        print("5. Manage Contacts")
        print("6. View Sent Log")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ")
        
        if choice == "1":
            send_simple_email()
        elif choice == "2":
            send_html_email()
        elif choice == "3":
            send_with_attachment()
        elif choice == "4":
            send_bulk_emails()
        elif choice == "5":
            manage_contacts()
        elif choice == "6":
            view_sent_log()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

main()
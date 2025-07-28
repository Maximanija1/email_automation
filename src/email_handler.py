# for sending emails
import smtplib
# for reading emails
import imaplib
# for parsing email content (extracting text, attachments, etc.)
import email
# Load environment variables
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

email_address = os.getenv('GMAIL_EMAIL')
app_password = os.getenv('GMAIL_APP_PASSWORD')

def connect_to_email():
    try:
        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        # Login with credentials
        mail.login(email_address, app_password)

        # Select the inbox folder
        mail.select('INBOX')

        print("Successfully connected to Gmail Inbox")   

        # Return the connection object
        return mail
    
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None


def search_for_emails():

    # This function should search for "Mediafill" emails
    pass

if __name__ == "__main__":
    connection = connect_to_email()
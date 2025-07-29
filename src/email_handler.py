import os
# for sending emails
import smtplib
# for reading emails
import imaplib
# for parsing email content (extracting text, attachments, etc.)
import email
# Load environment variables
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


def close_gmail_connection(mail_connection):
    try:
        if mail_connection:
            # Clode the selected folde (INBOX)
            mail_connection.close()
            # Logout fomr the server
            mail_connection.logout()
            print("Connection closed successfully.")
    except Exception as e:
        print(f"Failed to close connection: {e}")


def is_connected(mail_connection):
    try:
        # Check if the connection is still open
        if mail_connection:
            # "No operation" command to check connection status
            status = mail_connection.noop()
            return status[0] == 'OK'
        return False
    except:
        return False


def search_for_emails(mail_connection, keyword):
    try:
        # Search for emails containing keyword in subject OR body
        search_criteria = f'TEXT "{keyword}"'

        print(f"Searching for email with keyword: {keyword}")

        # Execute the search
        result, message_ids = mail_connection.search(None, search_criteria)

        #Check if search was successful
        if result == 'OK':
            # message_ids is a list of email IDs as bytes
            email_ids = message_ids[0].split()
            print(f"Found {len(email_ids)} email containing {keyword}")
            return email_ids
        else:
            print("Search failed")
            return []
    
    except Exception as e:
        print(f"Error during search: {e}")
        return []


if __name__ == "__main__":
    connection = connect_to_email()
    if connection:
        print(f"Connection active: {is_connected(connection)}")
        
        # Search for Mediafill emails
        keyword = "Mediafill"
        email_ids = search_for_emails(connection, keyword)

        print(f"Email IDs found: {email_ids}")

        close_gmail_connection(connection)

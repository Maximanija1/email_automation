import os
# for sending emails
import smtplib
# for reading emails and connecting to Gmail
import imaplib
# for parsing email content (extracting text, attachments, etc.)
import email
# Load environment variables
from dotenv import load_dotenv

from datetime import datetime

from typing import Optional


# Load environment variables from .env file
load_dotenv()

email_address = os.getenv('GMAIL_EMAIL')
app_password = os.getenv('GMAIL_APP_PASSWORD')

def connect_to_email() -> Optional[imaplib.IMAP4_SSL]:
    try:
        # Connect to Gmail's IMAP server
        GMAIL_IMAP_SERVER = 'imap.gmail.com'
        GMAIL_IMAP_PORT = 993

        mail = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER, GMAIL_IMAP_PORT)
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

# Case Insensitive Email Search
def search_for_emails_case_insensitive(mail_connection, keyword):

    all_email_ids = []

    print(f"Searching for emails with keyword: '{keyword} (case-insensitive)")

    # Create different case variations of the keyword
    variations = [
        keyword.upper(),
        keyword.lower(),
        keyword.capitalize(),
        keyword.title(),
        keyword
    ]

    print(f"Searching for variations: {variations}")
    
    # Search for each variation
    for i, variation in enumerate(variations):
        try:
            # Search for emails containing keyword in whole email (subject, body, headers) with "TEXT"
            search_criteria = f'TEXT "{variation}"'
            print(f" Search {i + 1}/{len(variations)}: {search_criteria}")

            # Execute the search
            result, message_ids = mail_connection.search(None, search_criteria)

            #Check if search was successful
            if result == 'OK':
                # message_ids is a list of email IDs as bytes
                email_ids = message_ids[0].split()
                print(f"Found {len(email_ids)} emails with {variation}")
                all_email_ids.extend(email_ids)
            else:
                print(f"No emails foun with {variations}")
        
        except Exception as e:
            print(f"Error searching for {variations}: {e}")

    unique_email_ids = list(set(all_email_ids))

    print(f"\n Total unique emails found: {len(unique_email_ids)}")
    return unique_email_ids

        
def has_pdf_attachment (mail_connection, email_id):
    try:
        # Fetch the full email message
        result, email_data = mail_connection.fetch(email_id, '(RFC822)')

        if result != 'OK':
            return False
        
        # Parse the email using the email library
        # [0] Metadata and [1] Actual email
        raw_email = email_data[0][1] # Get the raw email bytes
        email_message = email.message_from_bytes(raw_email)

        print(f"Checking email ID {email_id.decode()} for PDF attachments...")

        # Check if email has multiple parts (attachments)
        if email_message.is_multipart():
            # Loop through each part of the email
            for part in email_message.walk():
                # Check if this part is an attachment
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()

                    if filename:
                        print(f"Found attachment: {filename}")

                        # Check if it's a PDF
                        if filename.lower().endswith('.pdf'):
                            print(f"PDF found: {filename}")
                            return True

        print("No PDF attachments found")

    except Exception as e:
        print(f"Error checking attachments: {e}")
        return False


def download_pdf_attachment(mail_connection, email_id, download_folder="downloads"):

    downloaded_files = []

    try:
        # Fetch the full email message using its ID
        result, email_data = mail_connection.fetch(email_id, '(RFC822)')
        if result != 'OK':
            print(f"Error fetching email ID {email_id.decode()}")
            return []
        
        #Parse the raw email data into an email message object
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        print(f"Scanning email ID {email_id.decode()} for PDF attachments...")

        # Walk through all pars of the email
        for part in email_message.walk():
            # Check if the part is an attachment   
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename and filename.lower().endswith('.pdf'):
                    # Get the current time as a string
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    
                    # Split the filename from its extension
                    name, ext = os.path.splitext(filename)

                    # Create the new, unique filename
                    unique_filename = f"{name}_{timestamp}{ext}"

                    # Get the actual file content and decode it
                    payload = part.get_payload(decode=True)

                    # Create the full path to save the file 
                    file_path = os.path.join(download_folder, unique_filename)

                    # Save the attachment to the specified folder
                    with open(file_path, 'wb') as f:
                        f.write(payload)

                    downloaded_files.append(file_path)
                    print(f"Successfully downloaded: {file_path}")
                
        return downloaded_files
    
    except Exception as e:
        print(f"An error occurred while downloading attachments: {e}")
        return[]


if __name__ == "__main__":
    connection = connect_to_email()
    if connection:
        print(f"Connection active: {is_connected(connection)}")
        
        # Search for Mediafill emails
        keyword = "Mediafill"
        email_ids = search_for_emails_case_insensitive(connection, keyword)

        print(f"Email IDs found: {email_ids}")

        download_folder = "downloads" # This is the path to your folder 

        # Download the PDF attachments
        if email_ids:
            for email_id in email_ids:
                # Check if email has a PDF
                if has_pdf_attachment(connection, email_id):
                    # If it does, download it
                    download_pdf_attachment(connection, email_id, download_folder)
                else:
                    print(f"No PDF attachments found in email {email_id.decode()}")
        else:
            print("No emails found to process")

        close_gmail_connection(connection)

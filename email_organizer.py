import imaplib
import email
from email.header import decode_header

# Configuration
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
IMAP_SERVER = "imap.example.com"  # e.g., imap.gmail.com

# Folder rules based on keywords
FOLDER_RULES = {
    "Invoices": ["invoice", "payment"],
    "Work": ["project", "meeting", "deadline"],
    "Social": ["facebook", "twitter", "instagram"],
    "Newsletters": ["newsletter", "subscribe"]
}

def connect_to_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    return mail

def create_folder(mail, folder_name):
    mail.create(folder_name)

def move_email(mail, email_id, folder_name):
    create_folder(mail, folder_name)
    mail.copy(email_id, folder_name)
    mail.store(email_id, '+FLAGS', '\\Deleted')

def organize_emails():
    mail = connect_to_email()
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    for email_id in email_ids:
        res, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                sender = msg.get("From")

                subject_lower = subject.lower() if subject else ""
                sender_lower = sender.lower() if sender else ""

                moved = False
                for folder, keywords in FOLDER_RULES.items():
                    if any(keyword in subject_lower or keyword in sender_lower for keyword in keywords):
                        move_email(mail, email_id, folder)
                        print(f"Moved email '{subject}' to folder '{folder}'")
                        moved = True
                        break

                if not moved:
                    print(f"No matching folder for email: {subject}")

    mail.expunge()
    mail.logout()

# Run the bot
organize_emails()

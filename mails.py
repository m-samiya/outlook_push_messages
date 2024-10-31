import os
from dotenv import load_dotenv
import msal
import requests

# Load environment variables from .env
load_dotenv()

# Set up environment variables
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
TENANT_ID=os.getenv("TENANT_ID")
# Ensure AUTHORITY has the correct format using the TENANT_ID
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"] 


# Authenticate using MSAL
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

result = app.acquire_token_for_client(scopes=SCOPE)
access_token = result.get("access_token")

# Check if token is successfully acquired
if access_token:
    print("Access token acquired successfully.")
else:
    print("Failed to acquire token.")
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))
    exit()

# Define the function to create an email message
def create_email_message(recipient, subject, body_content):
    return {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body_content
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient
                    }
                }
            ]
        }
    }

# Function to send the email
def send_email(access_token, user_id, recipient, subject, body_content):
    email_message = create_email_message(recipient, subject, body_content)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # Sending email request
    response = requests.post(
        f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail',
        headers=headers,
        json=email_message
    )
    # Response handling
    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email: {response.status_code}, {response.text}")

# Test sending an email
if __name__ == "__main__":
    user_id = "ausaaf@amberflux.in"  # Ensure this is a valid UPN or User ID in Azure AD
    recipient = "ausaaf@amberflux.in"
    subject = "Test Email"
    body_content = "This is a test email sent using Microsoft Graph API."
    send_email(access_token, user_id, recipient, subject, body_content)


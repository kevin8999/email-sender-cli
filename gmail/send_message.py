# TODO: Configure code to work with my specific email account
# TODO: Configure code to work with any email service

import base64
from email.message import EmailMessage

# Set file path for external libraries as ../lib/
import os
import sys
file_path = os.path.dirname(__file__)
module_path = os.path.join(file_path, "lib")
sys.path.append(module_path)

# Google API libraries for gmail
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials


def gmail_send_message():
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.

  NOTE: Please run quickstart.py to get the OAuth2 token first
  """

  SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content("This is automated draft mail")

    message["To"] = receiver_email
    message["From"] = sender_email # MUST COME FROM ACCOUNT OWNER.
    message["Subject"] = "Automated draft"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
  gmail_send_message()

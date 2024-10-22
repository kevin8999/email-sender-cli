# TODO: Configure code to work with my specific email account
# TODO: Configure code to work with any email service

import base64
from email.message import EmailMessage
import argparse

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

def gmail_send_message(sender_email, receiver_email, subject_line, message_file, TOKEN_FILE, print_debug_msg=False) -> None:
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.

  NOTE: In this program, please run quickstart.py to get the OAuth2 token first
  """

  # SCOPES determines what you can do with your Google account. Modify the URL to change what you can do
  # NOTE: https://www.googleapis.com/auth/gmail.send lets you send email
  SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
  creds = None
  if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

  # Create the message body from message_file
  message_body = ""
  # Open the message file
  with open(message_file) as msg_file:
    message_body = msg_file.read().strip()

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(message_body)

    message["To"] = receiver_email
    message["From"] = sender_email
    message["Subject"] = subject_line

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message ID {send_message["id"]} sent')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Send emails via Gmail.")

  # Add arguments
  parser.add_argument('-s', '--sender',
                      required=True,
                      help='Email address that will send mail')
  parser.add_argument('-r', '--receiver',
                      required=True,
                      help='Email address that will receive mail from sender')
  parser.add_argument('--subject',
                      required=True,
                      help="Subject line of email")
  parser.add_argument('-m', '--message',
                      required=True,
                      default='message.txt',
                      help="File that contains the message body of email. Defaults to message.txt")
  parser.add_argument('-t', '--token_file',
                      required=False,
                      default='token.json',
                      help='Name of token file generated by quickstart.py. Default name: token.json')

  args = parser.parse_args()
  gmail_send_message(args.sender, args.receiver, args.subject, args.message, args.token_file)

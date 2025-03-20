import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import base64
from email import policy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

class HydraEmailManager:
    def __init__(self):
        load_dotenv()
        self.TENANT_ID = os.getenv("TENANT_ID")
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.AUTHORITY = f"https://login.microsoftonline.com/{self.TENANT_ID}"
        self.SCOPE = ["https://graph.microsoft.com/.default"]
        self.app = ConfidentialClientApplication(self.CLIENT_ID, self.CLIENT_SECRET, self.AUTHORITY)
        self.token = self.app.acquire_token_for_client(self.SCOPE)
        self.headers = {"Authorization": f"Bearer {self.token['access_token']}", "Content-Type": "application/json"} if "access_token" in self.token else None

    def verificar_senha(self, username, password):
        token = self.app.acquire_token_by_username_password(username, password, scopes=self.SCOPE)
        if "access_token" in token:
            return True
        else:
            return False

    def enviar_email(self, user_email, user_from, subject, body, attachment=None):
        if self.headers:
            email_data = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "HTML",
                        "content": f"{body}<br>"
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": user_from
                            }
                        }
                    ]
                }
            }

            if attachment:
                with open(attachment, "rb") as f:
                    attachment_content = f.read()
                attachment_data = {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": os.path.basename(attachment),
                    "contentBytes": base64.b64encode(attachment_content).decode('utf-8')
                }
                email_data["message"]["attachments"] = [attachment_data]

            url_send = f"https://graph.microsoft.com/v1.0/users/{user_email}/sendMail"
            response_send = requests.post(url_send, headers=self.headers, json=email_data)

            if response_send.status_code == 202:
                print("Email enviado com sucesso!")
            else:
                print("Erro ao enviar email:", response_send.json())
        else:
            print("Erro ao obter token:", self.token.get("error_description"))

    def baixar_emails(self, user_email, folder_id, is_read=False, file_format="eml"):
        if self.headers:
            url = f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/{folder_id}/messages?$filter=isRead eq {str(is_read).lower()}"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                emails = response.json().get("value", [])
                os.makedirs("emails", exist_ok=True)
                for email in emails:
                    from_address = email['from']['emailAddress']['address']
                    subject = email['subject']
                    body = email['body']['content']
                    print(f"De: {from_address}")
                    print(f"Assunto: {subject}")
                    print(f"Mensagem: {body}")
                    print("="*50)

                    msg = MIMEMultipart("related")
                    msg['From'] = from_address
                    msg['To'] = user_email
                    msg['Subject'] = subject

                    msg_alternative = MIMEMultipart("alternative")
                    msg.attach(msg_alternative)
                    msg_alternative.attach(MIMEText(body, 'html'))

                    attachments_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages/{email['id']}/attachments"
                    attachments_response = requests.get(attachments_url, headers=self.headers)
                    if attachments_response.status_code == 200:
                        attachments = attachments_response.json().get("value", [])
                        for attachment in attachments:
                            if attachment["@odata.type"] == "#microsoft.graph.fileAttachment":
                                attachment_content = base64.b64decode(attachment["contentBytes"])
                                if attachment["contentType"].startswith("image/"):
                                    part = MIMEBase('application', 'octet-stream')
                                    part.set_payload(attachment_content)
                                    encode_base64(part)
                                    part.add_header('Content-Disposition', f'inline; filename="{attachment["name"]}"')
                                    part.add_header('Content-ID', f'<{attachment["contentId"]}>')
                                    msg.attach(part)
                                    body = body.replace(f"cid:{attachment['contentId']}", f"cid:{attachment['contentId']}")
                                else:
                                    part = MIMEBase('application', 'octet-stream')
                                    part.set_payload(attachment_content)
                                    encode_base64(part)
                                    part.add_header('Content-Disposition', f'attachment; filename="{attachment["name"]}"')
                                    msg.attach(part)

                    filename = "".join([c if c.isalnum() or c in " ._-()" else "_" for c in subject]) + f".{file_format}"
                    filepath = os.path.join("emails", filename)

                    if file_format == "eml":
                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(msg.as_string(policy=policy.default))
                    elif file_format == "html":
                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(body)
            else:
                print("Erro:", response.json())
        else:
            print("Erro ao obter token:", self.token.get("error_description"))

    def obter_id_pastas(self, user_email):
        if self.headers:
            url = f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                folders = response.json().get("value", [])
                for folder in folders:
                    print(f"Nome da Pasta: {folder['displayName']}")
                    print(f"ID da Pasta: {folder['id']}")
                    print("="*50)
            else:
                print("Erro:", response.json())
        else:
            print("Erro ao obter token:", self.token.get("error_description"))
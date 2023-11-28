import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    message.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        print("Email sent successfully to", receiver_email)
        server.quit()
    except Exception as e:
        print("Error sending email to", receiver_email)
        print(e)

def send_emails_from_csv(csv_file, sender_email, sender_password):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            receiver_email = row["Email"]
            subject = row["Subject"]
            body = row["Body"]
            attachment_path = row["Attachment"]

            send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path)

# Paramètres de l'expéditeur
sender_email = "votre_email@gmail.com"
sender_password = "votre_mot_de_passe"

# Chemin vers le fichier CSV contenant les destinataires et les détails des emails
csv_file = "chemin/vers/votre_fichier.csv"

# Envoi des emails à partir du fichier CSV
send_emails_from_csv(csv_file, sender_email, sender_password)
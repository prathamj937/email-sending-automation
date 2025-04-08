from bs4 import BeautifulSoup
import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import webbrowser

def send_email(emailSend, sender_password, emailRec, subject, body, attachment_path):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(emailSend, sender_password)

        for recipient in emailRec:
            message = MIMEMultipart()
            message['From'] = emailSend
            message['To'] = recipient
            message['Subject'] = subject

            message.attach(MIMEText(body, 'plain'))

            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
                message.attach(part)

            server.sendmail(emailSend, recipient, message.as_string())
            print(f"Email sent to {recipient}")

        server.quit()
        return True
    except Exception as e:
        print(f"Error sending emails: {e}")
        return False

if __name__ == '__main__':
    try:
        with open('emails.txt', 'r') as f:
            emailList = [line.strip() for line in f if line.strip()]

        if not emailList:
            print("No emails found in the file.")
        else:
            print(f"Found {len(emailList)} email(s). Preparing to send...")

            emailSend = input("Enter your sender email: ")
            sender_password = input("Enter your email password (App Password if 2FA): ")

            subject = "Application for Internship Opportunity"
            body = f"""Dear Hiring Team,

I hope this message finds you well.

My name is Pratham Jain, and I am currently pursuing my undergraduate studies in Computer Science at Dronacharya College of Engineering. I am writing to express my keen interest in an internship opportunity within your esteemed organization.

I have a strong foundation in programming, web development, and cloud technologies, along with a growing passion for exploring real-world applications of AI/ML. I have worked on several academic and personal projects that demonstrate my technical skills and ability to learn quickly. I am confident that an internship at your organization would provide an excellent platform to apply my knowledge, gain valuable industry exposure, and contribute meaningfully to your team.

I am a dedicated and enthusiastic learner, comfortable working in both team settings and individual roles. I am particularly interested in roles related to cloud computing, software development, AI/ML, or data analytics, but I am open to exploring other domains as well.

Please find my resume attached for your kind consideration. I would be grateful for the opportunity to further discuss how I can contribute to your team. Thank you for considering my application.

Looking forward to your positive response.

Warm regards,
Pratham Jain
Email: prathamjain@email.com
Phone: +91-7827055486
https://www.linkedin.com/in/pratham-j-467469250/
https://github.com/prathamj937
Portfolio Link: 
"""

            attachment_path = "resume.pdf" 

            if send_email(emailSend, sender_password, emailList, subject, body, attachment_path):
                print("All emails sent successfully!")
            else:
                print("Some error occurred. Please check the details and try again.")
    except FileNotFoundError:
        print("The file 'emails.txt' was not found in the current directory.")

import yagmail
import os
import json
from dotenv import load_dotenv

load_dotenv()

class MailAgent:
    def __init__(self):
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.owner_email = os.getenv("OWNER_EMAIL")

    def send_mismatch_report(self, original_data, corrected_data, reason, missing_fields=None, recipient=None):
        """
        Sends an email report about the data mismatch.
        Returns the email content that was/would be sent.
        """
        recipient = recipient or self.owner_email
        missing_fields = missing_fields or []
        subject = "ALERT: PDF Extraction Field Mismatch Detected"
        body_parts = [
            "A mismatch was detected during the verification of a PDF document.",
            "",
            f"Reason: {reason}",
            ""
        ]

        if missing_fields:
            body_parts.extend([
                "Missing Fields:",
                ", ".join(missing_fields),
                ""
            ])

        body_parts.extend([
            "Original Extracted Data:",
            json.dumps(original_data, indent=2),
            "",
            "Corrected Data:",
            json.dumps(corrected_data, indent=2),
            "",
            "Please review the changes."
        ])

        body = "\n".join(body_parts)
        
        email_content = {
            "to": recipient,
            "subject": subject,
            "body": body
        }

        if not self.user or not self.password:
            print("⚠️  Email credentials not configured. Email would be sent to:")
            print(f"   To: {recipient}")
            print(f"   Subject: {subject}")
            return email_content

        try:
            yag = yagmail.SMTP(self.user, self.password)
            yag.send(to=recipient, subject=subject, contents=body)
            print(f"✓ Email sent to {recipient}")
            return email_content
        except Exception as e:
            print(f"Failed to send email: {e}")
            return email_content

    def send_success_report(self, data, recipient=None):
        """
        Sends a success report.
        Returns the email content that was/would be sent.
        """
        recipient = recipient or self.owner_email
        subject = "PDF Extraction Successful"
        body = f"Fields extracted and verified successfully:\n\n{data}"
        
        email_content = {
            "to": recipient,
            "subject": subject,
            "body": body
        }

        if not self.user or not self.password:
            print("⚠️  Email credentials not configured. Email would be sent to:")
            print(f"   To: {recipient}")
            print(f"   Subject: {subject}")
            return email_content
            
        try:
            yag = yagmail.SMTP(self.user, self.password)
            yag.send(
                to=recipient,
                subject=subject,
                contents=body
            )
            print(f"✓ Email sent to {recipient}")
            return email_content
        except Exception as e:
            print(f"Failed to send email: {e}")
            return email_content


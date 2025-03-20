import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv

class SendEmail:
    def __init__(self, env_path=".env"):
        """
        Inisialisasi class SendEmail.
        :param env_path: Path ke file .env (default: .env di direktori saat ini).
        """
        self.env_path = env_path
        self.load_config()

    def load_config(self):
        """Memuat konfigurasi dari file .env."""
        load_dotenv(self.env_path)
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT"))
        self.SMTP_USER = os.getenv("SMTP_USER")
        self.SMTP_PASS = os.getenv("SMTP_PASS")

    def send(self, subject, body, receiver_email):
        """
        Mengirim email.
        :param subject: Subjek email.
        :param body: Isi email.
        :param receiver_email: Email penerima.
        """
        if not all([self.SMTP_SERVER, self.SMTP_PORT, self.SMTP_USER, self.SMTP_PASS]):
            raise ValueError("Konfigurasi SMTP tidak lengkap. Pastikan file .env sudah benar.")

        msg = EmailMessage()
        msg["From"] = self.SMTP_USER
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(self.SMTP_USER, self.SMTP_PASS)
                server.send_message(msg)
                print(f"✅ Email berhasil dikirim ke {receiver_email}!")
        except Exception as e:
            print(f"❌ Gagal mengirim email: {e}")

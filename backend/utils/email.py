import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
import logging

logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, html_body: str) -> bool:
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured – skipping email to %s", to)
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=settings.SMTP_TLS,
        )
        return True
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        return False


async def send_booking_notification(business_name: str, owner_email: str, booking_data: dict):
    subject = f"New Booking Request – {business_name}"
    html = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
      <div style="background: linear-gradient(135deg, #0A4F3A 0%, #1a7a5e 100%); padding: 40px 32px; text-align: center;">
        <h1 style="color: #D4A853; font-size: 28px; margin: 0; letter-spacing: -0.5px;">biz.rw</h1>
        <p style="color: #a0d4c0; margin: 8px 0 0; font-size: 14px;">Business Platform</p>
      </div>
      <div style="padding: 40px 32px; background: #fafaf8;">
        <h2 style="color: #1A1A2E; font-size: 22px; margin: 0 0 8px;">New Booking Request</h2>
        <p style="color: #666; font-size: 15px; margin: 0 0 32px;">Someone has submitted a booking request for <strong>{business_name}</strong>.</p>
        <table style="width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06);">
          <tr style="background: #f5f0e8;">
            <td style="padding: 14px 20px; font-weight: 600; color: #1A1A2E; width: 40%; font-size: 14px;">Name</td>
            <td style="padding: 14px 20px; color: #444; font-size: 14px;">{booking_data.get('visitor_name', 'N/A')}</td>
          </tr>
          <tr>
            <td style="padding: 14px 20px; font-weight: 600; color: #1A1A2E; font-size: 14px;">Email</td>
            <td style="padding: 14px 20px; color: #444; font-size: 14px;">{booking_data.get('email', 'N/A')}</td>
          </tr>
          <tr style="background: #f5f0e8;">
            <td style="padding: 14px 20px; font-weight: 600; color: #1A1A2E; font-size: 14px;">Phone</td>
            <td style="padding: 14px 20px; color: #444; font-size: 14px;">{booking_data.get('phone', 'N/A')}</td>
          </tr>
          <tr>
            <td style="padding: 14px 20px; font-weight: 600; color: #1A1A2E; font-size: 14px;">Preferred Date</td>
            <td style="padding: 14px 20px; color: #444; font-size: 14px;">{booking_data.get('preferred_date', 'N/A')}</td>
          </tr>
          <tr style="background: #f5f0e8;">
            <td style="padding: 14px 20px; font-weight: 600; color: #1A1A2E; font-size: 14px; vertical-align: top;">Message</td>
            <td style="padding: 14px 20px; color: #444; font-size: 14px;">{booking_data.get('message', 'No message provided')}</td>
          </tr>
        </table>
        <div style="margin-top: 32px; padding: 20px; background: #0A4F3A; border-radius: 12px; text-align: center;">
          <p style="color: #a0d4c0; margin: 0; font-size: 14px;">Log in to your dashboard to view and respond to this request.</p>
        </div>
      </div>
      <div style="padding: 24px 32px; text-align: center; background: #f0ebe0;">
        <p style="color: #999; font-size: 12px; margin: 0;">© 2024 biz.rw · Empowering Rwandan SMEs</p>
      </div>
    </div>
    """
    await send_email(owner_email, subject, html)


async def send_feedback_notification(business_name: str, owner_email: str, feedback_data: dict):
    stars = "★" * feedback_data.get("rating", 0) + "☆" * (5 - feedback_data.get("rating", 0))
    subject = f"New Review Received – {business_name}"
    html = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
      <div style="background: linear-gradient(135deg, #0A4F3A 0%, #1a7a5e 100%); padding: 40px 32px; text-align: center;">
        <h1 style="color: #D4A853; font-size: 28px; margin: 0;">biz.rw</h1>
        <p style="color: #a0d4c0; margin: 8px 0 0; font-size: 14px;">Business Platform</p>
      </div>
      <div style="padding: 40px 32px; background: #fafaf8;">
        <h2 style="color: #1A1A2E; font-size: 22px; margin: 0 0 8px;">New Customer Review</h2>
        <p style="color: #666; font-size: 15px; margin: 0 0 16px;"><strong>{feedback_data.get('visitor_name')}</strong> left a review for <strong>{business_name}</strong>.</p>
        <div style="font-size: 28px; color: #D4A853; margin-bottom: 16px;">{stars}</div>
        <div style="background: #fff; padding: 20px; border-radius: 12px; border-left: 4px solid #D4A853; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
          <p style="color: #444; margin: 0; font-size: 15px; line-height: 1.6; font-style: italic;">"{feedback_data.get('comment', 'No comment provided')}"</p>
        </div>
      </div>
      <div style="padding: 24px 32px; text-align: center; background: #f0ebe0;">
        <p style="color: #999; font-size: 12px; margin: 0;">© 2024 biz.rw · Empowering Rwandan SMEs</p>
      </div>
    </div>
    """
    await send_email(owner_email, subject, html)

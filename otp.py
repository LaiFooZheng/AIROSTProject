from twilio.rest import Client
import smtplib
from email.message import EmailMessage
import pyotp
import qrcode
import imghdr


# def qr_generate(insert):
#     img = qrcode.make(insert)
#     img.save("QR_OTP.jpg")
#     print("QR Code Generated")
#     return img


def send_email(to, qr_file_path):
    user = "code4testingFZ@gmail.com"  # This is temporary gmail account I created
    password = "vopkmwjeegkoxrie"

    msg = EmailMessage()
    msg.set_content("Please download Google Authenticator and scan the qr code with the app. Your OTP refreshes every 30 seconds.")
    msg['subject'] = "AIROST Project OTP"
    msg['to'] = to
    msg['from'] = user

    with open(qr_file_path, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()
    print("Email has been sent to " + to)


# Decided not to send sms as it cost money after the free amount the service gave is used up
def send_sms(receiver, otp_in):
    account_sid = "AC43e43cc1829665296c08ead47654ec39"
    auth_token = "d578d6b93fb8b13052944fe43954febd"
    client = Client(account_sid, auth_token)

    # This free twilio number cost money everytime send sms
    client.messages.create(
        body=f"Your OTP is {otp_in}",
        from_='+18306236088',
        to=receiver
    )


def otp_generate(base32secret, email):
    print("Secret Key Generated", base32secret)
    totp = pyotp.TOTP(base32secret)
    auth = totp.provisioning_uri(name=email, issuer_name="AIROST Project")
    img = qrcode.make(auth)
    img.save("QR_OTP.jpg")
    print("QR Code Generated")
    otp = totp.now()
    print(otp)
    send_email(email, "QR_OTP.jpg")


def otp_check(secret_key, user_otp):
    totp = pyotp.TOTP(secret_key)
    if totp.now() == user_otp:
        return True
    else:
        return False




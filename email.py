import imp
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def emailhtml(results, email_address, mail_relay):
    """ sends email """
    try:
        sender = 'Server_Checker@cisco.com'
        receivers = [f'{email_address}']
        mailrelay = smtplib.SMTP(f'{mail_relay}')
        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'Server Check Results'
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        html = f"""
        <html>
        <body>
            <h2>Job Results</h2>
        </body>
        </html>
        """
        part2 = MIMEText(html, "html")
        msg.attach(part2)
        mailrelay.sendmail(sender, receivers, msg.as_string())
        mailrelay.quit()
        print('\nEmail Sent\n')
    except Exception as err:
        print(f'Error occured sending email with error: {str(err)}')
        print('\nEmail Failed\n')
import smtplib
import logging
import datetime
from os import path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("Email")
logging.basicConfig(level=logging.INFO)

TODAY = str(datetime.date.today())
HTML_TEMPLATE = """
<html>
    <head></head>
    <body>
        <p>
            {content}
        </p>
    </body>
</html>
"""

class EmailConnection(object):

    def __init__(self, account_name, password_fn, **kwargs):
        self.account_name = account_name
        self.password_fn = password_fn
        self.host = kwargs.get("host", "smtp.gmail.com")
        self.port = kwargs.get("port", "587")
        self.smtp = smtplib.SMTP(host=self.host, port=self.port)

    def __enter__(self):
        self.smtp.starttls()
        with open(self.password_fn, 'r') as fp:
            password = fp.read().strip('\n')
        self.smtp.login(self.account_name, password)
        del password
        return self.smtp

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            logger.error(exc_value)
            logger.error(traceback)
            print(exc_value)
            print(str(traceback))
            exit(1)
        self.smtp.quit()


def send_mail(content, recipients=("anthonyagnone@gmail.com"), subject="Self Email"):
	with EmailConnection("anthonyagnone@gmail.com", path.expanduser("~/.creds/gmail")) as emailer:
		msg = MIMEText(content)
		addr_from = "anthonyagnone@gmail.com"
		addr_to = recipients
		msg["From"] = addr_from
		msg["To"] = addr_to
		msg["Subject"] = subject
		emailer.sendmail(addr_from, addr_to, msg.as_string())

		#msg = MIMEMultipart()
		#addr_from = "anthonyagnone@gmail.com"
		#addr_to = recipients
		#msg["From"] = addr_from
		#msg["To"] = addr_to
		#msg["Subject"] = subject
		#msg.attach(
		#	MIMEText(
		#		HTML_TEMPLATE.format(content=content),
		#		"html"
		#	)
		#)
		#emailer.sendmail(addr_from, addr_to, msg.as_string())

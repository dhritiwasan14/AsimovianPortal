from flask_mail import Message
from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

class Mailer:
	def __init__(self, app, mail):
		self.app = app
		self.mail = mail

	@async
	def send_passwords(self, groups):
		with self.app.app_context():
			for g in groups:
				members = g['members'].split(',')
				memberEmails = []
				for m in members:
					memberEmails.append(m + "@mymail.sutd.edu.sg")

				msg = Message('AsimovianPortal Access Details', sender = 'asimovianportal@gmail.com', recipients = memberEmails)
				msg.body = "Hello " + g['username'] + ",\n\nYour login details for AsimovianPortal is as follows:\n\n\tUsername: " + g['username'] + "\n\tPassword: " + g['password'] + "\n\n Please log in at http://asimovianportal.com/login with these credentials!\n\nThanks,\nAsimovianPortal Adiministrator"
				self.mail.send(msg)
			return True
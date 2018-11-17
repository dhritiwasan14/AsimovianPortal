from flask_mail import Message

class Mailer:
	def __init__(self, mail):
		self.mail = mail

	def send_passwords(self, groups):
		for g in groups:
			members = g['members'].split(',')
			memberEmails = []
			for m in members:
				memberEmails.append(m + "@mymail.sutd.edu.sg")

			msg = Message('AsimovianPortal Access Details', sender = 'asimovianportal@gmail.com', recipients = memberEmails)
			msg.body = "Hello " + g['username'] + ",\n\nYour login details for AsimovianPortal is as follows:\n\n\tUsername: " + g['username'] + "\n\tPassword: " + g['password'] + "\n\n Please log in at http://asimovianportal.com/login with these credentials!\n\nThanks,\nAsimovianPortal Adiministrator"
			self.mail.send(msg)
		return True
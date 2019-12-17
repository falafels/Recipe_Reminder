from twilio.rest import Client

account_sid = "ACc7d820b58ebc6a23cf676a33eafa4887"
auth_token = "495d0bf1748c77a9bdd9b939220e2711"
client = Client(account_sid, auth_token)

sms = client.messages.create(
	body="ily let's go clubbing in sweatpants",
    to="+14168585332",
    from_="+18475581175",
)

print(sms.sid)


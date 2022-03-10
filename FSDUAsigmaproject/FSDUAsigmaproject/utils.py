import africastalking


# Initialize SDK
username = "ntegeka"    # use 'sandbox' for development in the test environment
api_key = "d222441446037b8ecaa60864e083eb8bd1862d20fd41b068cbf91d3f62ce592d"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
# response = sms.send("Hello Message!!!!!!!!!!!!!!!!", ["+256789076068"])
 
# Or use it asynchronously
def on_finish(error, response):
    pass
    # if error is not None:
    #     raise error
    # print(response)

def send_verification_code(user_code, phone_number):
    sms.send(f'Your biztech verification code is: {user_code}', [f'+256{phone_number}'], callback=on_finish)

def send_support_agent_notifier(phone_number):
    sms.send(f'Your biztech support agent has made a comment on your cost dashboard - Please Login to resolve the comment', [f'+256{phone_number}'], callback=on_finish)


def send_support_analyst_notifier(phone_number):
    sms.send(f'Your biztech support analyst has made a comment on your cost dashboard - Please Login to resolve the comment', [f'+256{phone_number}'], callback=on_finish)
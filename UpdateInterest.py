from apns import APNs, Payload
from pytrends.request import TrendReq
import schedule
import time

# TODO: add google email here
google_email = ""
# TODO: add google password here
google_pass = ""
apns = APNs(use_sandbox=False, cert_file='cert.pem', key_file='key.pem')
# TODO: add device token from APNs here
device_token = ""
labels = ['Eniram', 'Tesla']
values = {}


def send_notification(label):
    payload = Payload(alert="%s interest changed!" % label, sound="default", badge=1, mutable_content=True)
    apns.gateway_server.send_notification(device_token, payload)


def update_interests():
    for label in labels:
        pytrends.build_payload(kw_list=[label], timeframe='today 5-y')
        interests = pytrends.interest_over_time()
        current_interest = interests[label][-1]
        if label not in values or values[label] != current_interest:
            values[label] = current_interest
            send_notification(label)
            print("Interest for %s updated to %d" % (label, current_interest))


pytrends = TrendReq(google_email, google_pass)
schedule.every().hour.do(update_interests)
update_interests()
while True:
    schedule.run_pending()
    time.sleep(1)

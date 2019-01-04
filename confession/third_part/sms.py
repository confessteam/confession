import http.client
import urllib

from user_app.user_settings import ACCOUNT, PASSWORD
from user_app.utils import singleton


@singleton
class SendMessage(object):
    def __init__(self,text,mobile,host = "106.ihuyi.com",sms_send_uri = "/webservice/sms.php?method=Submit"):
        self.account = ACCOUNT
        self.password = PASSWORD
        self.text = text
        self.mobile = mobile
        self.host = host
        self.sms_send_uri = sms_send_uri

    def send_sms(self):
        params = urllib.parse.urlencode(
            {'account': self.account, 'password': self.password, 'content': self.text, 'mobile': self.mobile, 'format': 'json'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(self.host, port=80, timeout=30)
        conn.request("POST", self.sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        return response_str


if __name__ == '__main__':
    s = SendMessage("您的验证码是：980765。请不要把验证码泄露给其他人。",15735183194)
    print(s.send_sms())




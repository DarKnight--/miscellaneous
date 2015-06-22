__author_ = "DarKnight"

import requests
import webbrowser
import warnings

def __warning__(message):
    warnings.warn(category=Warning,
                  message=message)


class W2Sms:

    def __init__(self, filename):
        self.base_url = "http://site21.way2sms.com/"
        self.cookies = None
        self.host = "site21.way2sms.com"
        self.headers = {
                            "Host" : self.host,
                            "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
                            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language" : "en-US,en;q=0.5",
                            "Accept-Encoding" : "gzip, deflate",
                            "Referer" : self.base_url+"content/index.html"
                        }
        self.authenticate(filename)


    def authenticate(self, filename):
        with open(filename,"r") as files:
            self.uname = files.readline().strip("\n")
            self.pwd = files.readline().strip("\n")
        data= {
                    "username" : self.uname,
                    "password" : self.pwd
        }
        request = requests.post(self.base_url+"Login1.action", data=data, headers=self.headers,
                                     allow_redirects=False)
        self.redirect = request.headers["location"]
        if "JSESSIONID" in request.cookies:
            self.cookies = str(request.cookies["JSESSIONID"])
        else:
            __warning__("Authentication Failed.Please check your auth file or run forget_password method")


    def __send__(self, message, number):
        self.headers["Referer"] = self.base_url+"sendSMS?Token="+self.cookies[4:]
        self.headers["Cookie"] = "JSESSIONID="+self.cookies

        data = {
            "ssaction" : "ss",
            "Token" : self.cookies[4:],
            "mobile" : number,
            "message" : message,
            "msgLen" : str(140-len(message))
        }
        request = requests.post(self.base_url+"smstoss.action", data=data, headers=self.headers)
        if str(request.status_code) == '200':
            print "Message sent successfully"
        else:
            __warning__("Message not sent")

    def send_sms(self, message, number):
        if self.cookies:
            length = len(message)
            for index in range(0,length, 140):
                self.__send__(message[index:index+140], number)
        else:
            __warning__("Not Authenticated. Please authenticate by running authenticate method")

    def forgot_password(self):
        if self.cookies:
            webbrowser.open_new("http://site21.way2sms.com/wpwd.action")
        webbrowser.open_new(str(self.location))



if __name__ == '__main__':
    data = W2Sms(filename="w2sms.auth")
    data.send_sms("Amishfsf", "9827904271")


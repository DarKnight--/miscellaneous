__author_ = "DarKnight"

import requests
import webbrowser
import warnings
import json


def _warning(message):
    warnings.warn(category=Warning,
                  message=message)

class W2Sms:

    def __init__(self, filename):
        self.base_url = "http://site21.way2sms.com/"
        self.cookies = None
        self.host = "site21.way2sms.com"
        self.headers = {
                            "Host": self.host,
                            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Accept-Encoding": "gzip, deflate",
                            "Referer": self.base_url+"content/index.html",
                            "X-Requested-With": None,
                            "Content-Type": None,

                        }
        self.uname = None
        self.pwd = None
        self.redirect = None
        self.authenticate(filename)

    def authenticate(self, filename):
        with open(filename,"r") as files:
            self.uname = files.readline().strip("\n")
            self.pwd = files.readline().strip("\n")
        _data = {
                    "username": self.uname,
                    "password": self.pwd
        }
        request = requests.post(self.base_url+"Login1.action", data=_data, headers=self.headers, allow_redirects=False)
        self.redirect = request.headers["location"]
        if "JSESSIONID" in request.cookies:
            self.headers["Cookie"] = "JSESSIONID="+request.cookies["JSESSIONID"]
        else:
            _warning("Authentication Failed.Please check your auth file or run forget_password method")

    def __send(self, message, number):
        self.headers["Referer"] = self.base_url+"sendSMS?Token="+self.headers["Cookie"][15:]

        _data = {
            "ssaction" : "ss",
            "Token" : self.headers["Cookie"][15:]+"z",
            "mobile" : number,
            "message" : message,
            "msgLen" : str(140-len(message))
        }
        requests.post(self.base_url+"smstoss.action", data=_data, headers=self.headers, allow_redirects=False)


    def send_sms(self, message, number):
        if "Cookie" in self.headers:
            length = len(message)
            for index in range(0,length, 140):
                self.__send(message[index:index+140], number)
        else:
            _warning("Not Authenticated. Please authenticate by running authenticate method")

    def forgot_password(self):
        if "Cookie" in self.headers:
            webbrowser.open_new("http://site21.way2sms.com/wpwd.action")
        webbrowser.open_new(str(self.redirect))

    def get_contacts(self):
        url = self.base_url+"getContacts"
        self.headers["Referer"] = self.base_url+"main.action?section=s&Token="+self.headers["Cookie"][15:]+"&vfType=register_verify"
        self.headers["X-Requested-With"] = "XMLHttpRequest"
        self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        _data = {"Token" : self.headers["Cookie"][15:]}
        return json.dumps(requests.post(url, data=_data, headers=self.headers, allow_redirects=False).text)



    def add_contact(self, name, number, group_id='0'):
        url = self.base_url+"addressbook"
        self.headers["Referer"] = self.base_url+"main.action?section=s&Token="+self.headers["Cookie"][15:]+"&vfType=register_verify"
        self.headers["X-Requested-With"] = "XMLHttpRequest"
        self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        _data = {
            "action": "addcontact",
            "contno": number,
            "contname": name,
            "groupid": group_id,
            "Token": self.headers["Cookie"][15:],
            "ocontno": "",
            "ogroupid": "",
        }
        request = requests.post(url, data=_data, headers=self.headers, allow_redirects=False)
        print request.headers
        print request.status_code
        print request.text


if __name__ == '__main__':
    data = W2Sms(filename="w2sms.auth")
    #data.add_contact("test", "3652987456")
    data.get_contacts()
    #data.send_sms("Amishfsf", "9039943712")


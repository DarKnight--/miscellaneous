import unirest, sys

"""
Make a file named s2sms.auth containing following data, /// indicate start/end of file
///
Username Password Mashape-key
///

"""
with open("s2sms.auth","r") as files:
    [uname, pwd, mashape_key] = files.readline().strip("\n").split()

message = "Hello every one"

phone = "0123456789"

url = "https://site2sms.p.mashape.com/index.php?pwd="+pwd+"&uid="+uname+"&msg="+message+"&phone="+phone

response = unirest.get(url,
  headers={
    "X-Mashape-Key": mashape_key,
    "Accept": "application/json",
  }
)

if str(response.code) == '200':
    print "Message sent successfully."
else:
    print "Some error occured"


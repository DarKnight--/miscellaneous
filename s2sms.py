import unirest, sys


with open("s2sms.auth","r") as file:
	uname = file.readline().strip("\n")
	pwd = file.readline().strip("\n")
    mashape_key = file.readline().strip("\n")

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
else
    print "Some error occured"


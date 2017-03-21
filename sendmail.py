# -*- coding: utf8 -*-
import smtplib
from email.header import Header
from email.utils import formataddr
from email.message import Message
import sys


# checks for non ascii character
def contains_non_ascii_characters(mystr):
    return not all(ord(c) < 128 for c in mystr)


# adds header value if ascii value contains decodes with utf-8
def add_header(message, header_name, header_value):
    if contains_non_ascii_characters(header_value):
        h = Header(header_value, 'utf-8')
        message[header_name] = h
    else:
        message[header_name] = header_value
    return message

# me == my email address
# you == recipient's email address
me = "info@domain_name"
you = sys.argv[1]

name = you.split('@')[0]
# Create message container - the correct MIME type is multipart/alternative.
msg = Message()
msg['Subject'] = "Hello %s" % name
msg['From'] = me
msg['To'] = you
msg['Reply-To'] = "info@domain_name"
mailto = "mailto:alert@domain_name?subject=unsubscribe"

## provide your unsubscribe link
ulink = "http://domain_name/unsubscribe/?email=%s" % you
lsub = "<%s>, <%s>" % (mailto, ulink)
msg["List-Unsubscribe"] = lsub
msg.add_header("List-Id", "Info <info@domain_name>")
msg.add_header('Content-Type', 'text/html')

html = """\
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title></title>
</head>
<body>
<div class="conatiner">
Hi {name} , how are you? Hope your doing good.
</div>
You are receiving this email because you are subscribed to our mailing list of our
group. To unsubscribe click <a href="{unsublink}" class="unsub">here </a>
</body>
</html>
""".format(name=name, unsublink=ulink)


# Record the MIME types of both parts - text/plain and text/html.

if contains_non_ascii_characters(html):
    msg.set_payload(html.encode('utf-8'))
else:
    msg.set_payload(html)

# Send the message via local SMTP server.

mail = smtplib.SMTP("localhost")
mail.sendmail(me, you, msg.as_string())
mail.quit() 
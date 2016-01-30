#!/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import ssl
import json
import urllib.request
import urllib.response
import smtplib
from email.mime.text import MIMEText

# Gitlab settings
TOKEN = ""
URL = ""
REPO_ID = ""

# Email settings
TO = ""
FROM = ""
SMTP = ""

def getIssueList():
    """ Return all issues for REPO_ID """
    request = urllib.request.Request(URL + "/api/v3/projects/" + REPO_ID + "/issues", headers={"PRIVATE-TOKEN" : TOKEN })
    context = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(request,context=context)
    except HTTPError as e:
        return e.read().decode("utf-8")

    return json.loads(response.read().decode("utf-8"))


def sendIssues(issues):
    """ Format single email per issue """
    for issue in issues:
        subject = issue["title"]
        for label in issue["labels"]:
            subject += " #" + label
        body = issue["description"]

        print("Sennding issue " + subject)
        sendEmail(subject, body)
        print("Email sent")

def sendEmail(subject, body):
    """ Encode and send email  """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM
    msg["To"] = TO
    s = smtplib.SMTP(SMTP)
    s.send_message(msg)
    s.quit()

sendIssues(getIssueList())

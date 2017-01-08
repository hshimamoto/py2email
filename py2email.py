#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set sts=2 sw=2:

"""
py2mail --- Python2 email script

Usage

Prepare "setting" file:
+----------------------
|user account
|imap4 host port
+----------------------

Run script and enter password
$ ./py2mail.py
account
host
port
Password: <Enter password>

To stop script, create finish file.
$ touch finish
"""

import os
import time
import imaplib
from getpass import getpass

class MailClient(object):
  def __init__(self): # Constructor
    with open('settings', 'r') as f:
      for row in f:
        a = row.strip().split(' ')
        if a[0] == 'user':
          self.user = a[1]
        elif a[0] == 'imap4':
          self.imap_host = a[1]
          self.imap_port = int(a[2])
      # show user and server
      print self.user
      print self.imap_host
      print self.imap_port
      # get password
      self.password = getpass("Password: ")
  def login(self):
    self.conn = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
    self.conn.login(self.user, self.password)
    # show list
    print self.conn.list()
  def show_unseen(self):
    self.conn.select('INBOX')
    # search unseen
    t, d = self.conn.search(None, 'UNSEEN')
    ids = d[0].split()
    print "ids=%s" % ids
  def logout(self):
    self.conn.logout()

client = MailClient()

# inifinity loop until ./finish is generated
while True:
  if os.path.exists('./finish'):
    break
  client.login()
  client.show_unseen()
  client.logout()
  time.sleep(60.0) # sleep 60 sec

# vim:fileencoding=utf-8:sw=4

# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You can redistribute it and/or modify it under
# the terms of the Do What The Fuck You Want To Public License, Version 2, as
# published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more
# details.

# Copyright (c) 2010 by Paweł Zuzelski <pawelz.pld-linux.org>

import ekg
import re
import os
import sys
import suds
import time

from pyjira import soap
from pyjira import jira
from pyjira import jiraError

def login():
	return jira.Jira(ekg.config["jirabot:url"], ekg.config["jirabot:username"], ekg.config["jirabot:password"])

r = login()
rx = re.compile("%s-[0-9]+" % ekg.config["jirabot:project"])
rl = re.compile("!list")
rd = re.compile("!display ([A-Z]+-[0-9]+)")
rp = r.getProject(ekg.config["jirabot:project"])

def initialize(name, args):
	r = login()

def print_config(name, args):
	ekg.echo("JIRA url:      %s" % ekg.config["jirabot:url"])
	ekg.echo("JIRA username: %s" % ekg.config["jirabot:username"])
	ekg.echo("JIRA password: %s" % ekg.config["jirabot:password"])
	ekg.echo("JIRA project:  %s" % ekg.config["jirabot:project"])
	ekg.echo("IRC  channel:  %s" % ekg.config["jirabot:channel"])

def messageHandler(session, uid, type, text, stime, ignore_level):
	r = login()

	mx = rd.search(text)
	if (mx):
		i = r.getIssueByKey(mx.group(1))
		for line in i.display().splitlines():
			ekg.command("/msg %s %s" % (uid, line))
			time.sleep(.5)
		return

	mx = rx.search(text)
	if (mx):
		ekg.echo("Issue: "+mx.group(0))
		try:
			i = r.getIssueByKey(mx.group(0))
			ekg.command("/msg %s %s: %s" % (uid, mx.group(0), i.raw.summary))
		except jiraError.IssueNotFound:
			ekg.command("/msg %s %s: Issue not found." % (uid, mx.group(0)))
		return

	mx = rl.search(text)
	if (mx):
		i = rp.getIssues()
		ekg.command("/msg %s %s" % (uid, " ".join([s.raw.key for s in i])))
		return

ekg.handler_bind("protocol-message-received", messageHandler)

ekg.variable_add("jirabot:url", "")
ekg.variable_add("jirabot:username", "")
ekg.variable_add("jirabot:password", "")
ekg.variable_add("jirabot:project", "")
ekg.variable_add("jirabot:channel", "")

ekg.command_bind("jirabot:initialize", initialize)
ekg.command_bind("jirabot:print_config", print_config)

initialize(None, None)

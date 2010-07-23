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

from pyjira import soap
from pyjira import jira

def initialize(name, args):
	r = jira.Jira(ekg.config["jirabot:url"], ekg.config["jirabot:username"], ekg.config["jirabot:password"])
	rx = re.compile("%s-[0-9]+" % ekg.config["jirabot:project"])
	rl = re.compile("!list")
	rp = r.getProject(ekg.config["jirabot:project"])

def print_config(name, args):
	ekg.echo("JIRA url:      %s" % ekg.config["jirabot:url"])
	ekg.echo("JIRA username: %s" % ekg.config["jirabot:username"])
	ekg.echo("JIRA password: %s" % ekg.config["jirabot:password"])
	ekg.echo("JIRA project:  %s" % ekg.config["jirabot:project"])
	ekg.echo("IRC  channel:  %s" % ekg.config["jirabot:channel"])

def messageHandler(session, uid, type, text, stime, ignore_level):
	mx = rx.search(text)
	if (mx):
		ekg.echo("Issue: "+mx.group(0))
		try:
			i = r.getIssueByKey(mx.group(0))
			ekg.command("/msg %s %s: %s" % (ekg.config["jirabot:channel"], mx.group(0), i.raw.summary))
		except IssueNotFound:
			ekg.command("/msg %s %s: Issue not found." % (ekg.config["jirabot:channel"], mx.group(0)))

	mx = rl.search(text)
	if (mx):
		i = rp.getIssues()
		ekg.command("/msg %s %s" % (ekg.config["jirabot:channel"], " ".join([s.raw.key for s in i])))

ekg.handler_bind("protocol-message-received", messageHandler)

ekg.variable_add("jirabot:url", "")
ekg.variable_add("jirabot:username", "")
ekg.variable_add("jirabot:password", "")
ekg.variable_add("jirabot:project", "")
ekg.variable_add("jirabot:channel", "")

ekg.command_bind("jirabot:initialize", initialize)
ekg.command_bind("jirabot:print_config", print_config)

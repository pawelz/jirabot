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

rp = r.getProject(ekg.config["jirabot:project"])

command={}

def initialize(name, args):
	command['summary'] = (re.compile("%s-[0-9]+" % ekg.config["jirabot:projectregexp"]), cmd_summary)
	command['list'] = (re.compile("!list"), cmd_list)
	r = login()

def print_config(name, args):
	ekg.echo("JIRA url:      %s" % ekg.config["jirabot:url"])
	ekg.echo("JIRA username: %s" % ekg.config["jirabot:username"])
	ekg.echo("JIRA password: %s" % ekg.config["jirabot:password"])
	ekg.echo("JIRA project:  %s" % ekg.config["jirabot:project"])
	ekg.echo("JIRA projects: %s" % ekg.config["jirabot:projectregexp"])
	ekg.echo("IRC  channel:  %s" % ekg.config["jirabot:channel"])
	ekg.echo("Signals dir:   %s" % ekg.config["jirabot:sigdir"])

def cmd_summary(mx):
	ekg.echo("Issue: "+mx.group(0))
	try:
		i = r.getIssueByKey(mx.group(0))
		return "%s: %s" % (mx.group(0), i.raw.summary)
	except jiraError.IssueNotFound:
		return "%s: Issue not found." % mx.group(0)

def cmd_list(mx):
	i = rp.getIssues()
	return " ".join([s.raw.key for s in i])

def handleSignals():
	dir=ekg.config["jirabot:sigdir"]
	dirList=os.listdir(dir)
	for fname in dirList:
		file = open("%s/%s" % (dir, fname), "r")
		cmd = file.readline()
		for c in command:
			mx = command[c][0].search(cmd)
			if (mx):
				ekg.command(("/msg %s %s" % (ekg.config["jirabot:channel"], command[c][1](mx))).encode('UTF8'))
				break
		file.close()
		os.unlink("%s/%s" % (dir, fname))


def messageHandler(session, uid, type, text, stime, ignore_level):
	r = login()

	for c in command:
		mx = command[c][0].search(text)
		if (mx):
			ekg.command(("/msg %s %s" % (uid, command[c][1](mx))).encode('UTF8'))
			break

ekg.handler_bind("protocol-message-received", messageHandler)
ekg.timer_bind(5, handleSignals)

ekg.variable_add("jirabot:url", "")
ekg.variable_add("jirabot:username", "")
ekg.variable_add("jirabot:password", "")
ekg.variable_add("jirabot:project", "")
ekg.variable_add("jirabot:channel", "")
ekg.variable_add("jirabot:sigdir", "/nonexistent")
ekg.variable_add("jirabot:projectregexp", "[A-Z]+")

ekg.command_bind("jirabot:initialize", initialize)
ekg.command_bind("jirabot:print_config", print_config)

initialize(None, None)

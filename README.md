Introduction
============

JIRA bot is an IM bot for Atlassian JIRA. It allows to integrate JIRA with
IRC.  It should be easy to integrate it with any other IM protocol supported
by ekg2 (Jabber, GG, ICQ, ...).

Requirements
============

JIRA bot is a python script for ekg2, so obviously you need ekg2 with python
module. It also needs pyjira python library.

	  ekg2: http://ekg2.org
	pyjira: http://github.com/pawelz/pyjira

Installation
============

JIRA configuration
------------------

I assume that you already have working JIRA installation. It must be
accessible without http authentication. (I mean http_auth is not supported.
JIRA level authentication is fully supported).

* Create an account for jira bot,
* grant it read access to some projects,
* enable JIRA remote API (see http://confluence.atlassian.com/x/8dcB for
  details).

Note: you need to create a JIRA account even if JIRA content is readable
anonymously, because JIRA does not support anonymous SOAP access. See
http://jira.atlassian.com/browse/JRA-20549

ekg2 configuration
------------------

* copy jirabot.py to `~/.ekg2/scripts/jirabot.py` (create this directory unless
  it already exists)
* run ekg2 in a screen session
* configure irc session
	/plugin +irc
	/session -a irc:jirabot
	/session set ircname <nickname for jira bot>
	/session server <irc server address>
	/save
	/connect
* enable python plugin and load jirabot script
	/plugin +python
	/script:load jirabot

JIRA bot configuration
----------------------

JIRA bot is configured via ekg2 config variables. All its variables are
decalred in “jirabot:” namespace. Set them using following command:

	/set jirabot:<key> = <value>

Available config variables are:

* `jirabot:channel`: default irc channel. In fact it is ekg2 uid. Examples:
  - `#mychannel`
  - `irc:someuser`
  - `xmpp:user@domain`
  - `gg:666`
* `jirabot:url`: base URL of your JIRA installation
* `jirabot:username`: username of bot user in JIRA
* `jirabot:password`: password of bot user in JIRA
* `jirabot:project`: oh, I really don't remember why it is needed
* `jirabot:projectregexp`: JIRA bot completly ignores all projects whose keys
  don't match this regexp. Examples:
  - `MYPROJECT` - match just single project
  - `(PROJECT|ANOTHERPROJECT)` - alternative
  - `[A-Z.]*` - match any uppercase project key. Note that it will interpret
    UTF-8, JP-2 and GRUNWALD-1410 as issue keys!
* `jirabot:sigdir`: where to look for signals (see signals section)

Usage
=====

There are two main use cases:

Interactive
-----------

JIRA bot scans all incoming messages. It will response to the
following messages:

* `!list`: prints all open issues (not tested with project with > 10 open
  issues)
* `!jirabot selftest`: print some debug
* on any message containing issue key mathing `jirabot:projectregexp` it will
  print compact information about given issue

Signals
-------

JIRA bot scans `jirabot:sigdir` directory. It excpects files containing
subject of mail sent by JIRA.
NOTE: it assumes that jira email prefix is ` ` (single space). It will be
fixed in the future.

I use the following script to deliver "signals":
	#!/bin/sh -x
	
	formail -x Subject \
		| perl -MEncode -p -e 'BEGIN{binmode STDOUT,":utf8"} $_=Encode::decode("MIME-Header",$_)' \
		| sed 's/^ //g;' | tr -d '\n' > ~/issues/$(uuid)

and the following entry in my .procmailrc file:
	:0 c
	| /home/users/rsget/is.sh

Commands
========

* `/jirabot:print_config`: print configuration variables
* `/jirabot:signal ARG`: trigger signal. Should be equivalent to:
  `echo ARG > sigdir/file`. May be useful in conjunction with ekg2 rc
  plugin.

Author, License
===============

Written by Paweł Zuzelski <pawelz@pld-linux.org>
You can do what the fuck you want with this code.

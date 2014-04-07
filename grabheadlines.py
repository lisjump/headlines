#!/usr/bin/python

import feedparser, globalvars
import codecs
import xmlparser
import sqlite3
from datetime import *
from time import mktime
feeddir = globalvars.feeddir
diskdir = globalvars.diskdir
db = diskdir + globalvars.db

def getDBCategories():
  conn = sqlite3.connect(db)
  c = conn.cursor()
  c.execute("select name, gui, desccount, descage, maxcount, maxage from categories")
  rawcats = c.fetchall()
  categories = {}
  for cat in rawcats:
    categories[cat[0]] = {}
    categories[cat[0]]['gui'] = cat[1]
    categories[cat[0]]['desccount'] = cat[2]
    categories[cat[0]]['descage'] = cat[3]
    categories[cat[0]]['maxcount'] = cat[4]
    categories[cat[0]]['maxage'] = cat[5]
  conn.close()
  return categories

def getDBFeeds(catname):
  conn = sqlite3.connect(db)
  c = conn.cursor()
  c.execute("select name, gui, link, rss, desccount, descage, maxcount, maxage from feeds where category = ?", (catname,))
  rawfeeds = c.fetchall()
  feeds = {}
  for feed in rawfeeds:
    feeds[feed[0]] = {}
    feeds[feed[0]]['gui'] = feed[1]
    feeds[feed[0]]['link'] = feed[2]
    feeds[feed[0]]['rss'] = feed[3]
    feeds[feed[0]]['desccount'] = feed[4]
    feeds[feed[0]]['descage'] = feed[5]
    feeds[feed[0]]['maxcount'] = feed[6]
    feeds[feed[0]]['maxage'] = feed[7]
  conn.close()
  return feeds

def updateFeeds():
	category = getDBCategories()
	for catname in category:
	  feeds = getDBFeeds(catname)

	  print ("Doing %s" % (category[catname]['gui']))
	  outfile = codecs.open(diskdir + catname + ".html", "w", "utf-8")
	  outfile.write("<div class=\"boxcontent\">\n");
	  emptyBlogs = ""

	  for feedname in feeds:
		print ("  %s" % (feeds[feedname]['gui']))
		doc = feedparser.parse(feeds[feedname]['rss'])

		writethis = "<span id=\"%stoggle\" onClick=\"CollapseMenu('%sentries', '%stoggle');\" class='link'>[-]</span>"  % (feedname, feedname, feedname)
		writethis = writethis + " <a href=\"%s\">%s</a>"  % (feeds[feedname]['link'], feeds[feedname]['gui'])
		writethis = writethis + "<div><div class=\"feeditems\" id=\"%sentries\"><ul class=\"feeditems\">\n"  % (feedname)
		count = 0
		if feeds[feedname]['desccount'] or feeds[feedname]['desccount'] == 0:
		  desccount = feeds[feedname]['desccount']
		elif category[catname]['desccount'] or category[catname]['desccount'] == 0:
		  desccount = category[catname]['desccount']
		else:
		  desccount = 2
	
		if feeds[feedname]['descage'] or feeds[feedname]['descage'] == 0:
		  descage = feeds[feedname]['descage']
		elif category[catname]['descage'] or category[catname]['descage'] == 0:
		  descage = category[catname]['descage']
		else:
		  descage = 1
	
		if feeds[feedname]['maxcount'] or feeds[feedname]['maxcount'] == 0:
		  maxcount = feeds[feedname]['maxcount']
		elif category[catname]['maxcount'] or category[catname]['maxcount'] == 0:
		  maxcount = category[catname]['maxcount']
		else:
		  maxcount = 20
	
		if feeds[feedname]['maxage'] or feeds[feedname]['maxage'] == 0:
		  maxage = feeds[feedname]['maxage']
		elif category[catname]['maxage'] or category[catname]['maxage'] == 0:
		  maxage = category[catname]['maxage']
		else:
		  maxage = 10
	
	  
		for entry in doc.entries:
		  try:
			try:
			  entrytime = datetime.fromtimestamp(mktime(entry.published_parsed))
			except:
			  entrytime  = datetime.now()
			entryage = datetime.now() - entrytime
			if entryage.days < descage and count < desccount:
			  writethis = writethis + "<li><a href=\"%s\">%s</a><BR>%s<BR>\n" % (entry.link, entry.title, entry.description)
			  count = count + 1
			elif entryage.days < maxage and count < maxcount:
			  writethis = writethis + "<li><a href=\"%s\">%s</a><BR>\n" % (entry.link, entry.title)
			  count = count + 1
		  except UnicodeEncodeError:
			pass
		writethis = writethis + "</ul></div></div>\n"
		if count > 0:
		  outfile.write(writethis)
		else:
		  emptyBlogs = emptyBlogs + " <a href=\"%s\">%s</a><br>\n"  % (feeds[feedname]['link'], feeds[feedname]['gui'])
	  outfile.write("%s</div>\n" % emptyBlogs)
	  outfile.close()
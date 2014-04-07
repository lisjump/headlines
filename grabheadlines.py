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

class Entry():
    def __init__(self, parent, link, title, description, age): 
      self.parent = parent
      self.link = link
      self.title = title
      self.description = description
      self.age = age
      self.shortContent = ""
      self.longContent = ""
      
      self.fillContent()
      
    def fillContent(self):
      try:
        self.longContent = "<a href=\"%s\">%s</a><BR>%s<BR>\n" % (self.link, self.title, self.description)
        self.shortContent = "<a href=\"%s\">%s</a><BR>\n" % (self.link, self.title)
      except UnicodeEncodeError:
        pass
    
class Feed():
    def __init__(self, parent, name, gui, link, rss, desccount, descage, maxcount, maxage): 
      self.parent = parent
      self.name = name
      self.gui = gui
      self.link = link
      self.rss = rss
      self.desccount = desccount
      self.descage = descage
      self.maxcount = maxcount
      self.maxage = maxage
      self.newestEntryAge = timedelta.max
      self.entries = []
      self.header = "<span id=\"%stoggle\" onClick=\"CollapseMenu('%sentries', '%stoggle');\" class='link'>[-]</span>"  % (self.name, self.name, self.name)
      self.title = " <a href=\"%s\">%s</a>"  % (self.link, self.gui)
      self.beginlist = "<div><div class=\"feeditems\" id=\"%sentries\"><ul class=\"feeditems\">\n"  % (self.name)
      self.listContent = ""
      self.footer = "</ul></div></div>\n"

      self.fixDefaults()
      self.getEntries()
      self.fillContent()
    
    def fixDefaults(self):
		if self.desccount or self.desccount == 0:
		  pass
		elif self.parent.desccount or self.parent.desccount == 0:
		  self.desccount = self.parent.desccount
		else:
		  self.desccount = 2
	
		if self.descage or self.descage == 0:
		  pass
		elif self.parent.descage or self.parent.descage == 0:
		  self.descage = self.parent.descage
		else:
		  self.descage = 1
	
		if self.maxcount or self.maxcount == 0:
		  pass
		elif self.parent.maxcount or self.parent.maxcount == 0:
		  self.maxcount = self.parent.maxcount
		else:
		  self.maxcount = 20
	
		if self.maxage or self.maxage == 0:
		  pass
		elif self.parent.maxage or self.parent.maxage == 0:
		  self.maxage = self.parent.maxage
		else:
		  self.maxage = 10
		
    def getEntries(self):
      print ("  %s" % (self.gui))
      doc = feedparser.parse(self.rss)
      for entry in doc.entries:
	    try:
	      entrytime = datetime.fromtimestamp(mktime(entry.published_parsed))
	    except:
	      entrytime  = datetime.now()
	    entryage = datetime.now() - entrytime
	    if entryage.days <= self.maxage:
	      self.entries.append(Entry(self, entry.link, entry.title, entry.description, entryage))
	      if not self.newestEntryAge or self.newestEntryAge > entryage:
	        self.newestEntryAge = entryage
	
    def fillContent(self):
      count = 0
      for entry in self.entries:
	    if entry.age.days < self.descage and count < self.desccount:
	      self.listContent = self.listContent + "<li>" + entry.longContent + "\n"
	      count = count + 1
	    elif entry.age.days < self.maxage and count < self.maxcount:
	      self.listContent = self.listContent + "<li>" + entry.shortContent + "\n"
	      count = count + 1

class Category():
    def __init__(self, name, gui, desccount, descage, maxcount, maxage): 
      self.name = name
      self.gui = gui
      self.desccount = desccount
      self.descage = descage
      self.maxcount = maxcount
      self.maxage = maxage
      self.feeds = {}
      self.getFeeds()
      
    def getFeeds(self):
      print ("Doing %s" % (self.gui))
      conn = sqlite3.connect(db)
      c = conn.cursor()
      c.execute("select name, gui, link, rss, desccount, descage, maxcount, maxage from feeds where category = ?", (self.name,))
      rawfeeds = c.fetchall()
      for feed in rawfeeds:
        self.feeds[feed[0]] = Feed(self, feed[0], feed[1], feed[2], feed[3], feed[4], feed[5], feed[6], feed[7])
      conn.close()
    
    def createFile(self):
      outfile = codecs.open(diskdir + self.name + ".html", "w", "utf-8")
      outfile.write("<div class=\"boxcontent\">\n")
      
      sortedfeeds = {}
      
      for feedname in self.feeds:
        sortedfeeds[str(self.feeds[feedname].newestEntryAge) + feedname] = self.feeds[feedname]

      for feedname in sorted(sortedfeeds.keys()):
        if sortedfeeds[feedname].listContent == "":
          outfile.write(sortedfeeds[feedname].title)
          outfile.write("<BR>")
        else:
          outfile.write(sortedfeeds[feedname].header)
          outfile.write(sortedfeeds[feedname].title)
          outfile.write(sortedfeeds[feedname].beginlist)
          outfile.write(sortedfeeds[feedname].listContent)
          outfile.write(sortedfeeds[feedname].footer)
        
      outfile.write("</div>")
      outfile.close()
      
def getDBCategories():
  conn = sqlite3.connect(db)
  c = conn.cursor()
  c.execute("select name, gui, desccount, descage, maxcount, maxage from categories")
  rawcats = c.fetchall()
  categories = {}
  for cat in rawcats:
    categories[cat[0]] = Category(cat[0], cat[1], cat[2], cat[3], cat[4], cat[5])
  conn.close()
  return categories

def updateFeeds():
	categories = getDBCategories()
	for catname in categories:
	  categories[catname].createFile()
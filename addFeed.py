#!/usr/bin/python 
import xmlparser, subprocess, sys, grabheadlines, cgi, codecs, feedparser, fileinput, sqlite3, globalvars
feeddir = globalvars.feeddir
cgilis = globalvars.cgilis
diskdir = globalvars.diskdir
db = globalvars.db
mainpage = globalvars.mainpage

def getPost():
  form = cgi.FieldStorage()
  post = {}
  for item in form:
    post[str(item)] = str(form[item].value).replace("&", "&amp;").replace("<", "&lt;")
  return post

def addCat(post):
  newcat = post['newcat'].lower().replace(" ", "").replace("\'", "").replace("\"", "")
  categories = getDBCategories()
  if newcat in categories:
    post['category'] = newcat
    return
  for cat in categories:
    if categories[cat]['gui'].lower().replace(" ", "").replace("\'", "").replace("\"", "") == newcat:
      post['category'] = cat
      return
  conn = sqlite3.connect(db)
  c = conn.cursor()
  with conn:
    c.execute("INSERT INTO categories (name, gui) VALUES (?, ?)", (newcat, post['newcat']))
  conn.close()
  return
  
def addFeed(post):
  feed = feedparser.parse(post['feedurl']).feed
  name = str(feed.title).lower().replace(" ", "").replace("\'", "").replace("\"", "")
  conn = sqlite3.connect(db)
  c = conn.cursor()
  with conn:
    c.execute("INSERT or REPLACE INTO feeds (name, gui, link, rss, category) VALUES (?, ?, ?, ?, ?)", (name, feed.title, feed.link, post['feedurl'], post['category']))
  conn.close()
  return

def getDBCategories():
  conn = sqlite3.connect(db)
  c = conn.cursor()
  c.execute("select name, gui from categories")
  rawcats = c.fetchall()
  categories = {}
  for cat in rawcats:
    categories[str(cat[0])] = {}
    categories[str(cat[0])]['gui'] = str(cat[1])
  conn.close()
  return categories

try:
  post = getPost()
  if "feedurl" in  post.keys():
    if "newcat" in post.keys():
      addCat(post)
    addFeed(post)
  print "Content-type:    text/html\r" 
  print "Location:        %s%s\r\n\r" % (cgilis, mainpage)
  grabheadlines.updateFeeds()
except:
  print "Content-Type:text/html\n\n"
  print "<html>\n"
  print "<head>\n"
  print "<title>Headlines</title>\n"
  print "<script src=\"headlines.js\" type=\"text/javascript\"></script>"
  print "<link rel=\"stylesheet\" href=\"" + feeddir + "headlines.css\" type=\"text/css\" media=\"screen\">\n"
  print "<link rel=\"stylesheet\" href=\"" + feeddir + "handheld.css\" type=\"text/css\" media=\"only screen and (max-device-width:480px)\">\n"
  print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>"
  print "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/htmlcharset=UTF-8\">"
  print "<META http-equiv=\"refresh\" content=\"1800\">"
  print "</head>\n"
  print "<body>\n"
  print "Unexpected error:"
  print str(sys.exc_info()[0])
  print str(sys.exc_info()[1])
  print str(sys.exc_info()[2])
  print "done"
  print "</body>\n"
  print "</html>\n"

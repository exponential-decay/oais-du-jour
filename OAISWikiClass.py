import sys
import time
import urllib2
from datetime import datetime

class HandleOAISWiki:

   #we'll return this to the main handler
   tweetlist = []

   lastdateloc = "oaislastupdated"
   pageindexloc = "wiki-uris-manual"
   DATEFORMAT = "%Y-%m-%dT%H:%M:%SZ"

   #tags we need
   UPDATEDTAG = "{http://www.w3.org/2005/Atom}updated"
   LINKTAG = "{http://www.w3.org/2005/Atom}link"
   AUTHORTAG = "{http://www.w3.org/2005/Atom}author"

   #hashtags
   HASHDP = "#digitalpreservation"
   HASHOAIS = "#oais"
   HASHDP2 = "#digpres"

   DISCUSSTEXT = '?title=Talk:'

   TWITTERLINKLEN = 22
   TWEETLEN = 140
   ELIPSESLEN = 3 #{...}

   def __tweetlen__(self, tweet, url):
      return ((len(tweet.strip()) - len(url)) + self.TWITTERLINKLEN)

   def __makepagetitle__(self, url):
      if self.DISCUSSTEXT in url:
         title = url.split(self.DISCUSSTEXT, 1)
      else:
         title = url.split('title=', 1)
      if len(title) > 0:
         title = title[1].split('&diff=', 1)[0]
      return urllib2.unquote(title)

   def __maketweet__(self, data):
      title = ''
      author = ''
      url = ''
      date = ''
      discuss = 'Page'
   
      for item in data:
         if item.tag == self.LINKTAG:
            url = item.attrib['href']
            if self.DISCUSSTEXT in url:
               discuss = 'Comment'
            title = self.__makepagetitle__(url)
         if item.tag == self.AUTHORTAG:
            for name in item:
               author = name.text
         if item.tag == self.UPDATEDTAG:
            date = item.text

      #TODO: Better length logic? 
      #CURRENT RATIONALE: Hash tags help discoverability, compromise last
      tweet = discuss + ": " + title + ' by ' + author + " " + url + " " + self.HASHOAIS + " " + self.HASHDP
      if self.__tweetlen__(tweet, url) > 140:
         tweet = tweet.replace(self.HASHDP, self.HASHDP2)
      if self.__tweetlen__(tweet, url) > 140:
         tweet = tweet.replace(self.HASHDP2, '')
      if self.__tweetlen__(tweet, url) > 140:
         tweet = tweet.replace(self.HASHOAIS, '')
      if self.__tweetlen__(tweet, url) > 140:
         diff = (self.__tweetlen__(tweet, url) - self.TWEETLEN) + self.ELIPSESLEN
         tweet = discuss + ": " + title[:-diff] + '... by ' + author + " " + url
      if self.__tweetlen__(tweet, url) > 140:
         sys.stderr.write("Cannot create a tweet of an appropriate length: " + str(self.__tweetlen__(tweet, url)) + "\n")
         tweet = ''

      return tweet.strip()

   def __checkindex__(self, link):
      tweetlink = False
      linkdata = link.attrib['href'].split('&diff=',1)[0] #split diff url
      #print linkdata
      if linkdata in self.pageindex:
         tweetlink = True
      return tweetlink

   def __lastdate__(self):
      d = "2015-02-08T12:41:57Z"
      with open(self.lastdateloc, 'rb') as f:
         d = f.readline().strip()
         f.close()
      return d

   def __buildpageindex__(self):
      pindex = []
      with open(self.pageindexloc, 'rb') as f:
         for l in f:
            index = l.strip()
            #append standard page and create URL for discussion page
            pindex.append(index)
            pindex.append(index.replace('?title=',self.DISCUSSTEXT))
      f.close()
      return pindex

   def __newdate__(self, date):
      output = False
      if datetime.strptime(date, self.DATEFORMAT) > self.lastdate:
         output = True 
      return output

   def __init__(self, atom, namespace=False):
      self.namespace = namespace
      self.lastdate = datetime.strptime(self.__lastdate__(), self.DATEFORMAT)

      #no namespace filter set in ATOM feed...
      if namespace is False:
         self.pageindex = self.__buildpageindex__()

      self.atom = atom

   def __readxml__(self):
      for entry in self.atom:
         datedone = False
         newdate = False
         oaispage = False

         data = entry #because can't go back through an iterator

         for item in entry:
            if item.tag == self.UPDATEDTAG:
               datedone = True
               newdate = self.__newdate__(item.text)
            if item.tag == self.LINKTAG:
               if self.namespace == False:
                  oaispage = self.__checkindex__(item)
               else:
                  oaispage = True

         if datedone == True and newdate == False:
            break

         if newdate == True and oaispage == True:
            self.tweetlist.append(self.__maketweet__(data))  

      return self.tweetlist

   def __del__(self):
      with open(self.lastdateloc, 'wb') as f:
         f.write(time.strftime(self.DATEFORMAT).strip())
         f.close()
               

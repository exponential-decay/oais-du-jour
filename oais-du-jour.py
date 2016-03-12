import sys
from ReadXMLClass import read_xml
from OAISWikiClass import HandleOAISWiki
from TwitterClass import HandleTwitter

def main():

   wikiloc = "http://wiki.dpconline.org/api.php?hidebots=1&days=100&limit=50&action=feedrecentchanges&feedformat=atom"
   xml = read_xml(wikiloc)
   xml_iter = xml.scan_xml()
   handler = HandleOAISWiki(xml_iter, False)

   tweetlist = handler.__readxml__()
   tweetlist.reverse()

   if len(tweetlist) == 0:
      sys.stderr.write("Nothing to tweet right now." + "\n")
   else:
      twitter = HandleTwitter()
      for tweet in tweetlist:
         if tweet != '':
            twitter.tweet_update(tweet)
         else: 
            sys.stderr.write("Issue generating tweet. See log." + "\n")
   
if __name__ == "__main__":      
   main()

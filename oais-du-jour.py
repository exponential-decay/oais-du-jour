from ReadXMLClass import read_xml
from OAISWikiClass import HandleOAISWiki
      
def main():

   wikiloc = "http://wiki.dpconline.org/api.php?hidebots=1&days=100&limit=50&action=feedrecentchanges&feedformat=atom"
   xml = read_xml(wikiloc)
   xml_iter = xml.scan_xml()
   tweet_list = HandleOAISWiki(xml_iter, False)

if __name__ == "__main__":      
   main()
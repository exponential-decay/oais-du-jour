import os
import re
import sys
import urllib2
import xml.etree.ElementTree as etree

class read_xml:
   
   def __init__(self, loc):
      self.loc = loc

   def scan_xml(self):
      tree = etree.ElementTree(file=urllib2.urlopen(self.loc))
      root = tree.getroot()
      xml_iter = iter(root)
      return xml_iter
               
                

#!/usr/bin/env python
# encoding: UTF-8
################################################################################
#
#
# Tasiopoulos Vasilis - tasiopoulos[DOT]vasilis[AT]gmail[DOT]com
#
################################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


version = "1.0.0 [Beta]"
 
import urllib2
import os
import re
import sys

from updatevulnerabilitylist import updatevuln
from drupcheck import checkifdrupal
from drupupdate import drupupdate

global drupalversion
drupalversion=""

class color:
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERL = '\033[4m'
  RESET = '\033[0;0m'
  
  
################################################################################
#
# Function to scan Multiple sites from txt
#
################################################################################

def scanmultiple():
  #urlfile="/home/tibillys/Desktop/drupalsites.txt"
  urlfile=raw_input("\nGive the path of the txt file: ")
  try:
    d = open(urlfile)
    urlfilelines = d.readlines()
  except:
    print "\n[-] Error : '" + urlfile + "' not found" 
    print "[-] Exiting Drupal Scan..\n"
    exit()
  for url in urlfilelines:
    if "http://" in url:
      url=url.replace("\n","")
    else:
      url="http://"+url.replace("\n","")
      sys.stdout.write(color.BOLD +"\n [+] Checking for "+url+ " \n "+ color.RESET)
    if checkifdrupal(url)==True:
      checksinglesite(url)
    else:
      sys.stdout.write(color.RED +"\n [!] "+url+ " is not Drupal \n "+ color.RESET)


################################################################################
#
# Function to check a single site
#
################################################################################


def checksinglesite(siteurl):
  try:
    url = siteurl + "/CHANGELOG.txt"

    for line in urllib2.urlopen(url):
      if "Drupal" in line:
	global drupalversion
	if "," in line:
	  drupalversion = line[line.index(" ")+1:line.index(",")]
	elif "xx" in line: 
	  drupalversion = line[line.index(" ")+1:line.index(" x")]
	print "[+] Drupal version is "+drupalversion
	break
    matchvulnerability()
  except:
    print "[!] Cannot identify Drupals Version"




################################################################################
#
# Function to make the maching of sites version--vulnerabilities
#
################################################################################


def matchvulnerability():
  global drupalversion
  f = open("vulnerabilities/drupalvulnerabilitieslist.txt","r");
  lines = f.readlines();
  for line in lines:
    if drupalversion in line:
      sys.stdout.write(color.BOLD +"\n [.] "+  line[:line.index("Type:")] + color.RESET+"\n")
      sys.stdout.write(color.RED +" [.] "+ line[line.index("Type:"):line.index("Descripion:")] +"\n "+ color.RESET)
      sys.stdout.write("[.] "+ line[line.index("Url:"):line.index("Version:")] +"\n ")
      sys.stdout.write(color.GREEN +"[.] "+ line[line.index("Descripion:"):line.index("Url:")] +"\n "+ color.RESET)
      sys.stdout.flush()




################################################################################
#
# Function to search in page for vulnerable module names
#
################################################################################


def modulescanner(url):
  modurl=urllib2.urlopen(url).read();
  f = open("vulnerabilities/drupalmodulevulnerabilitieslist.txt","r");
  line = f.readlines();
  for modulename in line:
    moduleonlyname=modulename[modulename.index("Vulnerable module:")+18:modulename.index("Type:")]
    if "Module" in moduleonlyname:
      moduleonlyname=moduleonlyname.replace("Module","")		#remove "Module" keyword from name
    if "Drupal" in moduleonlyname:
      moduleonlyname=moduleonlyname.replace("Drupal","") 		#remove "Drupal" keyword from name
    moduleonlyname=moduleonlyname.replace(" ","") 			#remove spaces from name
    moduleonlyname=moduleonlyname.lower() 				#make name lower case for matching
    moduleonlyname=moduleonlyname.replace("\n","")			 #remove newlines from name
    if moduleonlyname in modurl:
      sys.stdout.write(color.BOLD +"\n [.] "+  modulename[:modulename.index(" Vulnerable module:")] + color.RESET+"\n")
      sys.stdout.write(color.RED +"\n [.] "+  modulename[modulename.index("Vulnerable module:"):modulename.index("Type:")] + color.RESET+"\n")
      sys.stdout.write(color.RED +" [.] "+ modulename[modulename.index("Type:"):modulename.index("Descripion:")] +"\n "+ color.RESET)
      sys.stdout.write("[.] "+ modulename[modulename.index("Url:"):modulename.index("Version:")] +"\n ")
      sys.stdout.write(color.GREEN +"[.] "+ modulename[modulename.index("Descripion:"):modulename.index("Url:")] +"\n "+ color.RESET)
      sys.stdout.flush()


################################################################################
#
# Function to search in page for modules using drupalxray.com
#
################################################################################


def modulescannerxray(url):
  modulelist=[]
  f = open("vulnerabilities/drupalmodulevulnerabilitieslist.txt","r");
  line = f.readlines();
  if "http://" in url:
    url = url.replace("http://","")
  if "www" not in url:
    url = "www."+url
  url="http://drupalxray.com/xray/"+url
  xrayurl= urllib2.urlopen(url).readlines();
  for line in xrayurl:
    if "<a href=\"http://drupal.org/project/" in line:
      module=line[line.index("target=\"_blank\">")+16:line.index("</a>")]
      modulelist.append(module)
  print "According to drupalxray.com "+ url+ "has tha above modules installed:\n"
  for item in modulelist:
    print item

      

print "[+] Version : "+ version
print "[+] Copyright (C) 2013 - Drupal Scan Development Team. \n"

while True:
  print """
  [+] Drupal Scan Toolkit Menu:
  [+] Press "S" to scan a single site.
  [+] Press "L" to scan from a list.
  [+] Press "M" to scan drupals modules (Experimental).
  [+] Enter "V" to update Vulnerability database.
  [+] Enter "U" for update tool.
  [+] Enter "Q" for quit.
  """

  option = raw_input("Enter Option: > ")

  if option =='S' or option =='s':
    siteurl=raw_input("give me the site to check: ")
    if "http://" not in siteurl:
      siteurl = "http://" + siteurl
    if checkifdrupal(siteurl)==True:
      checksinglesite(siteurl)
    else:
      sys.stdout.write(color.RED +"\n [!] This site is not Drupal \n "+ color.RESET)
  
  if option =='L'or option =='l':
    scanmultiple()

  if option =='M'or option =='m':
    print """
    [+] Do you want to use drupalxray.com
    """

    option = raw_input("Enter Option: > ")
    if option =='y' or option =='Y':
      siteurl=raw_input("give me the site to check: ")
      if "http://" not in siteurl:
	siteurl = "http://" + siteurl
      if checkifdrupal(siteurl)==True:
	modulescannerxray(siteurl)
      else:
	sys.stdout.write(color.RED +"\n [!] This site is not Drupal \n "+ color.RESET)
    elif option =='n' or option =='N':
      siteurl=raw_input("give me the site to check: ")
      if "http://" not in siteurl:
	siteurl = "http://" + siteurl
      if checkifdrupal(siteurl)==True:
	modulescanner(siteurl)
      else:
	sys.stdout.write(color.RED +"\n [!] This site is not Drupal \n "+ color.RESET)
  
  if option =='V'or option =='v':
    updatevuln()
  
  if option =='U'or option =='u':
    drupupdate()

  if option =='Q' or option =='q':
    print "[-] Exiting Drupal Scan\n"
    exit()

if __name__ == '__main__':
  main()
    
#eof

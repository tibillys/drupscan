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
import urllib2
import re
from urlparse import urlparse

################################################################################
#
# Function to check if a site is drupal
#
################################################################################

def checkifdrupal(url):
  try:
    count_dp_keywords = 0
    if "http://" in url:
      website = urllib2.urlopen(url)
    else:
      website = urllib2.urlopen("http://" + url)
    websiteread = website.read()
    drupalDirectories=['','?q=user']
    for dpDirs in drupalDirectories:
      if re.findall('[D|d]rupal.js',websiteread):
	count_dp_keywords += 1
      if re.findall('[D|d]rupal',websiteread):
	count_dp_keywords += 1
      if re.findall('[D|d]rupal',websiteread + "/CHANGELOG.txt"):
	count_dp_keywords += 1
    if count_dp_keywords > 1:
      return True
    else:
      return False
  except:
    print "Site offline or takes to long to respond"
    



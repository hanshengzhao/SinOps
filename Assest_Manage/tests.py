from django.test import TestCase

# Create your tests here.
import urllib2
import re
website = urllib2.urlopen('http://www.baidu.com/s?wd=django+template++items+&ie=utf-8&tn=10003816_ie_dg')
html = website.read()
links = re.findall('"((http|ftp)s?://.*?)"', html)
url_list = []
for i in links:
    url_list.append(i[0])
print url_list

#!/usr/bin/python
import re
import urllib
from urlparse import urlparse


def analyze_page(page):
    """Analyzes content for links, emails and images using naive regex"""
    for content in page.readlines():
        links.extend(re.findall(r'href="(http://[A-Za-z0-9?_/=%&\.\-]+)"', content))
        emails.extend(re.findall(r'([A-Za-z0-9?_/=%&\.\-]+@[A-Za-z0-9?_/=%&\.\-]+)', content))
        images.extend(re.findall(r'<img src="([A-Za-z0-9?_/=:%&\.\-]+)"', content))


def count_unique_hosts(links):
    hosts = {}
    for link in links:
        url = urlparse(link)
        if url.netloc in hosts:
            hosts[url.netloc] += 1
        else:
            hosts[url.netloc] = 1
    return hosts

if __name__ == '__main__':
    url = raw_input("Enter the URL you wish to analyze (without http): ")
    url = "http://" + url
    page = urllib.urlopen(url)

    links = []
    emails = []
    images = []

    analyze_page(page)
    hosts = count_unique_hosts(links)
    emails = list(set(emails))

    print "Links: ", links
    print "Hosts: ", hosts
    print "Emails: ", emails
    print "Number of images: %i" % len(images)

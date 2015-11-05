#!/usr/bin/python
# -*- coding: utf-8 -*-

import webbrowser
import re
import cookielib
import urllib
from urllib import urlencode
import urllib2
import optparse
import sys
import time
import random
import string
import getpass
import hashlib
import binascii
import zlib



def getRespHtml(resp) :

    if resp!=0:
        respHtml = resp.read()

        if resp.info().get('Content-Encoding') == 'gzip':
            respHtml = zlib.decompress(respHtml, 16+zlib.MAX_WBITS)
        return respHtml

    else:
        return  ""




def TwitterRelease1():

    #print "[preparation] using cookieJar & HTTPCookieProcessor to automatically handle cookies";
    #print "prepare cookie";
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    username = raw_input("You twitter:")
    password = raw_input("Password:")

    ########################################################################################################################
    urlToken = "https://twitter.com/"

    headersToken = {
            'Accept'          : 'text/html, application/xhtml+xml, */*',
            'Accept-Language' : 'zh-CN',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding' : 'gzip, deflate',
            'Host'            : 'twitter.com',
            'Connection'      : 'Keep-Alive',
            'Cache-Control'   : 'no-cache'
    }

    reqToken = urllib2.Request(urlToken, None)
    for key in headersToken.keys() :
        reqToken.add_header(key, headersToken[key])

    #respToken = urllib2.urlopen(reqToken, timeout=5)
    #respToken = urllib2.urlopen(reqToken)

    try:
        respToken = urllib2.urlopen(reqToken, timeout=5)
    except:
        print ("Can not connect to twitter.com, so exit.")
        sys.exit()

    respHtmlToken = getRespHtml(respToken)

    regex_authenticity_token1 = r'''name="authenticity_token" value="(.*?)">'''
    regex_authenticity_token2 = r''' value="(.*?)"> name="authenticity_token"'''
    m1 = re.search(regex_authenticity_token1, respHtmlToken)
    m2 = re.search(regex_authenticity_token2, respHtmlToken)
    
    if m1:
        authenticity_token = m1.groups()[0]
    elif m2:
        authenticity_token = m2.groups()[0]
    else:
        print ("can't find authenticity_token with regex, so exit.")
        sys.exit()

    print authenticity_token

    ########################################################################################################################

    urlSessions = "https://twitter.com/sessions"

    headersSessions = {
            'Accept'          : 'text/html, application/xhtml+xml, */*',
            'Referer'         : 'https://twitter.com/',
            'Accept-Language' : 'zh-CN',
            'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding' : 'gzip, deflate',
            'Host'            : 'twitter.com',
            'Connection'      : 'Keep-Alive',
            'Content-Length'  : '219',
            'Cache-Control'   : 'no-cache'
    }

    postDataSessions = "&remember_me=1&return_to_ssl=true&scribe_log=&redirect_after_login=%2F&authenticity_token="
    postDataSessions = "session%5Busername_or_email%5D=" + username + "&session%5Bpassword%5D=" + password + postDataSessions + authenticity_token
    postDataSessions = postDataSessions.encode(encoding='GBK') 


    reqSessions = urllib2.Request(urlSessions,postDataSessions)
    for key in headersSessions.keys() :
        reqSessions.add_header(key, headersSessions[key])

    try:
        respSessions = urllib2.urlopen(reqSessions, timeout=5)
    except:
        print ("Can not connect to twitter.com, so exit.")
        sys.exit()

    respHtmlSessions = getRespHtml(respSessions)
    f = open('twittersessions.html','w')
    f.write(respHtmlSessions)
    f.close()

    #print "respHtmlSessions:" + respHtmlSessions

    ########################################################################################################################
    while(True):
        content = raw_input("please input the message:")
        if content == "quit":
            break
    
        urlPublish = "https://twitter.com/i/tweet/create"

        headersPublish = {
                'Accept'          : 'application/json, text/javascript, */*; q=0.01',
                'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer'         : 'https://twitter.com/',
                'Accept-Language' : 'zh-CN',
                'User-Agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Accept-Encoding' : 'gzip, deflate',
                'Host'            : 'twitter.com',
                'Connection'      : 'Keep-Alive',
                'Content-Length'  : '219',
                'Cache-Control'   : 'no-cache'
        }

        postDataPublish = "&is_permalink_page=false&place_id=&tagged_users=&ui_metrics=%7B%22tt%22%3A1617%2C%22v%22%3A2%2C%22gts%22%3A0%2C%22h%22%3A%2251c10517%22%2C%22b%22%3A%22bceab9a6beaba4a0bcf2eb89f192b9b7a4b0eae884ede481efbfd1bdd1d6d3c8888b91c8c7ce839e8c84839edd90999ad5a5d5d88a89948c94732f76667c71243d6e68667869212c7e65786078673b647275766c7e3e27787e4c52470f0654534e5a4259055e48434046547c5c5050140d4c4b4f5e101f4d5c3224272d6a26292b273b0e2e3c39266d6a63667f762635253d3c3475343837380815405953535e4b4a1a091909080041071816071c574c464b4f4c575e131f09e9e6e3f7ebf7a8ebe9e7edfeedeaebadaab3e8fbb9d6d8b5b4bbf4faeaf4f9fed4ced08dd4c9c7d3cec6d8c68e978cf8d9df8181969994d9d9cfd3dcddc9d1cdeeb1b0aca0b0a5b3eaf3e88ca9aea5a0f2fdf0a4bdbbb2b8aff7b6b4bfbcb28c948e90828380c4dd9c9b9f8ec0cf99869e959d84da8693848b909595af89918d616667213e7174726d25287c65636a60673f7b7d70706e727c5d583926696c6a455c%22%7D"
        postDataPublish = "authenticity_token=" + authenticity_token + "&status=" + content + postDataPublish
        #postDataPublish = postDataPublish.encode(encoding='utf-8') 


        reqPublish = urllib2.Request(urlPublish,postDataPublish)
        for key in headersPublish.keys() :
            reqPublish.add_header(key, headersPublish[key])

        try:
            respPublish = urllib2.urlopen(reqPublish, timeout=5)
        except:
            print ("Can not connect to twitter.com, so exit.")
            continue

        #respHtmlPublish = getRespHtml(respPublish)
        #f = open('twitterPublish.html','w')
        #f.write(respHtmlPublish)
        #f.close()


if __name__=="__main__":
    #while True:
    TwitterRelease1()




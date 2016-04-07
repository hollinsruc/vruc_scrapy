#!/usr/bin/python
# -*- coding: utf-8 -*-

def getCookieValue(key, cookiestr):
    cookies = cookiestr.split('; ')
    cookiedict = dict()
    for cookie in cookies:
        kvarray = cookie.split('=')
        if(len(kvarray) == 1):
            cookiedict[kvarray[0]] = ''
        else:
            cookiedict[kvarray[0]] = kvarray[1]
    return cookiedict[key]
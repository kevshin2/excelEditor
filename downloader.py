# -*- coding: utf-8 -*-
from cookielib import LWPCookieJar # needed for form authentication

from urllib import urlencode

import urllib2

import string # to find and replace content in strings 

import sys

def downloader(USER_NAME, PASSWORD):
    
    SERVER_NAME = 'w3-connections.ibm.com'
    
    print "Attempting to log in to (%s)..." % (SERVER_NAME)
    
    # if port numbers are needed for your server, fill in below, otherwise leave them as is. Example: HTTP_PORT = ':9080'.
    
    HTTP_PORT = ''
    
    HTTPS_PORT = ''
    
    # Create authenticated server opener
    
    cookieProcessor = urllib2.HTTPCookieProcessor(LWPCookieJar())
    
    opener = urllib2.build_opener(cookieProcessor)
    
    
    # encoded parameters sent in a POST method (over secure connection)
    
    encodedForm = urlencode({ "j_username" : USER_NAME, "j_password" : PASSWORD})
    
    
    # in this test case we used the port numbers, depending on the server, you can ignore these
    
    urlform = "https://" + SERVER_NAME + HTTPS_PORT + "/wikis/j_security_check"
    
    request = urllib2.Request(urlform, encodedForm)
    
    opener.addheaders = [("User-agent","Mozilla/5.0")]
    
    
    # Read the response from the server
    
    loggedIn = opener.open(request).read()
    
    # Check if the response contains a redirection to the login page
    
    # Or check if the response is the login page 
    
    if string.find(loggedIn, 'window.location.replace') == -1 and string.find(loggedIn, 'X-LConn-Login') == -1:
    
            print 'Logged in successfully!'
    
    else:
    
            print 'Failed to log in.'
    
            exit()
    
    excelFile = urllib2.Request("https://w3-connections.ibm.com/files/form/anonymous/api/library/749dd86c-c4d8-4aa6-b03e-0bb4f6bae761"
                                +"/document/fdc2f92b-03c9-4f77-b83c-d8f96f3c491b/media/V11.3_CurrentTestBucketRegressionStatus.xls")
    output = open('source.xls','wb')
    output.write(opener.open(excelFile).read())
    print "V11.3_CurrentTestBucketRegressionStatus.xls has been saved as source.xls successfully!"
    output.close()
    
def main(args):
    if len(args) == 2:
        downloader(args[0],args[1])
    else:
        print "This program requires two arguments, an IBM intranet username followed by the password."
        print "The user must have wiki access!"
        
if __name__ == '__main__':
    main(sys.argv[1:])

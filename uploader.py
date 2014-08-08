from cookielib import LWPCookieJar # needed for form authentication

from urllib import urlencode

import urllib2

import string # to find and replace content in strings 

import sys

def downloader(USER_NAME, PASSWORD, FILE_LOCATION):
    
    SERVER_NAME = 'w3-connections.ibm.com'
    
    print "\nAttempting to log in to (%s)..." % (SERVER_NAME)
    
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
            
def main(args):
    if len(args) == 4:
        prompt = "Please check the excel document named \"%s\" in this folder: \"%s\"\n" % (args[3], args[0].replace("\uploader.py", ""))
        prompt += "When you are satisfied hit enter and the document will be uploaded to the wiki."
        raw_input(prompt)
        downloader(args[1], args[2], args[3])
    else:
        print "This program requires 3 arguments, an IBM intranet username followed by the password"
        print "as well as the location of the file to be uploaded"
        print "The user must have wiki access!"
        
if __name__ == '__main__':
    main(sys.argv)
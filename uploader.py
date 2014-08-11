from cookielib import LWPCookieJar # needed for form authentication

from urllib import urlencode

import urllib2

import string # to find and replace content in strings 

import sys

import mimetypes

import mmap

def uploader(USER_NAME, PASSWORD, FILE_LOCATION, DEBUG = "NO"):
    
    SERVER_NAME = 'w3-connections.ibm.com'
    
    print "\nAttempting to log in to (%s)..." % (SERVER_NAME)
    
    # Create authenticated server opener
    
    cookieProcessor = urllib2.HTTPCookieProcessor(LWPCookieJar())
    
    opener = urllib2.build_opener(cookieProcessor)
    
    # encoded parameters sent in a POST method (over secure connection)
    
    encodedForm = urlencode({ "j_username" : USER_NAME, "j_password" : PASSWORD})
    
    
    # in this test case we used the port numbers, depending on the server, you can ignore these
    
    urlform = "https://" + SERVER_NAME + "/wikis/j_security_check"
    
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
            
    excelFile = open(FILE_LOCATION, 'r')
    
    if DEBUG.upper() == "YES":
        url = 'https://w3-connections.ibm.com/files/basic/api/userlibrary/'
        url += 'b8e5e0c0-a38e-1033-9149-ac5876bd6d0c/document/a0c2ab4d-b530-458c-a1f1-6ee6d8c3acfb/media'
        print "RUNNING IN DEBUG MODE"
    elif DEBUG.upper() == "NO":
        exit()
        url = "https://w3-connections.ibm.com/files/basic/api/"
        url += "communitylibrary/214fe5d2-2471-4a42-ba99-f53de8dbe081/document/fdc2f92b-03c9-4f77-b83c-d8f96f3c491b/media"
    else:
        print "\nInvalid argument, either set the DEBUG argument as \"YES\" or leave it blank."
        exit()
    #convert raw file to string
    mmapped_file_as_string = mmap.mmap(excelFile.fileno(), 0, access=mmap.ACCESS_READ)
    
    request2 = urllib2.Request(url, mmapped_file_as_string)
    
    #this is a hack I found online to make the downloader in python work as an uploader
    contenttype = mimetypes.guess_type(FILE_LOCATION)[0]
    request2.add_header('Content-Type', contenttype)
    request2.get_method = lambda: 'PUT'
    opener.open(request2)

    print "File appears to have been uploaded successfully!"
    
    excelFile.close()
            
def main(args):
    if len(args) == 4 or len(args) == 5:
        prompt = "Please check the excel document named \"%s\" in this folder: \"%s\"\n" % (args[3], args[0].replace("\uploader.py", ""))
        prompt += "When you are satisfied hit enter and the document will be uploaded to the wiki."
        raw_input(prompt)
        if len(args) == 4:
            uploader(args[1], args[2], args[3])
        else:
            uploader(args[1], args[2], args[3], args[4])
    else:
        print "This program requires 3 arguments, an IBM intranet username followed by the password"
        print "as well as the location of the file to be uploaded"
        print "The user must have wiki access!"
        
if __name__ == '__main__':
    main(sys.argv)
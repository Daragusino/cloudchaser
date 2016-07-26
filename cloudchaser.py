#! /usr/bin/python


import argparse, requests, time, urllib2, urllib, sys
#Load validators for the verifaction of the streamcloud url
import validators

#Load and initalize colorama for colored output
from colorama import init,Fore,Style
init()


__author__ = "daragusino"


#Function for later showing the progress of the video download
def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("%2d%%" % percent)
      sys.stdout.write("\b\b\b")
      sys.stdout.flush()


#Get all the arguments 
parser = argparse.ArgumentParser(description='Cloudchaser by daragusnov')
#Source
parser.add_argument('-s','--source', help='Streamcloud Link to download',required=True)
#Destination
parser.add_argument('-d','--destination',help='Path for the file to be downloaded to', required=True)
parser.add_argument('--silent', help='Turn on silent mode. Cloudchaser will only output the direct link to the video and will not download it', action="store_true")
args = parser.parse_args()

 
#Check for silent mode
if not args.silent:
   #Show the user the arguments supplied 
   print ("Will download from:")
   print (Fore.BLUE + "%s" % args.source)
   print (Style.RESET_ALL +"to:")
   print (Fore.GREEN + "%s" % args.destination )
   print (Style.RESET_ALL)



#Use Validators to check if the URL exists.
if args.source.find("http://streamcloud.eu") == -1:
    print (Fore.RED + "ERROR: Not a valid Streamcloud Link")
    sys.exit()

if not validators.url(args.source):
    print (Fore.RED + "ERROR: URL seems broken")
    sys.exit()


#Request the site and save the data for the post request will perform later to get the mp4 file
bot1 = urllib2.urlopen(args.source)
#Debug Output the Contents of the HTML File
#print bot1.read()
bot1output = bot1.read()
#print bot1output


#Check for silent option
if not args.silent:
    print "Site loaded......."


#Look for the Post Data
#Use String Slicing for this
#First get the index of the first part
test1 = bot1output.find("<input type=\"hidden\" name=\"")
#debug Output the index and the first part of string for the post request
#print test1
#print bot1output[test1]
#And then the one of the second
test2 = bot1output.find("Watch video now")
#Debug print the index
#print test2
#Slice the string to get the post data
postdata = bot1output[test1:test2+17]
#Debug print the post data
#print postdata


#Prepare and send the post request
#Split the string again to get the informations needed for the post request. Others always seem to stay the same, those are hardcoded
#VideoID assuming that the length of the video id dosn't change
videoidnum = postdata.find("name=\"id\" value=\"")
videoid = postdata[videoidnum+17:videoidnum+29]


#Check for silent option
if not args.silent:
    #Show VideoID
    print "VideoID"
    print (Fore.GREEN + videoid)
    print (Style.RESET_ALL)


#Get the name of the show, which is saved in the post parameter fname
fnamenum1 = postdata.find("name=\"fname\" value=\"")
fnamenum2 = postdata.find("<input type=\"hidden\" name=\"referer\"")
#Debug print the index of the keywords
#print fnamenum1
#print fnamenum2
fname = postdata[fnamenum1+20:fnamenum2-9]

#Check for the silent option
#Show name
if not args.silent:
    print "Name of File"
    print (Fore.GREEN + fname)
    print (Style.RESET_ALL)
    print "Now we'll wait 12 Seconds, just to be sure..."

#Wait 12 Seconds before sending the post request
time.sleep(12)

#Check for silent option
if not args.silent:
    print ("Sending Post Request")


data = urllib.urlencode({'op' : 'download1',
                         'usr_login' : '',
                         'id' : videoid,
                         'fname' : fname,
                         'referer' : '',
                         'hash' : '',
                         'btn_download' : 'Watch video now'})
req = urllib2.Request(args.source, data)
response = urllib2.urlopen(req)
result = response.read()
#Debug show the whole response
#print result
#Find the start and the end of the file path
test3 = result.find("file: ")
test4 = result.find("video.mp4")
#Debug show the index of the file path found
#print test3
#print test4
filepath = result[test3+7:test4+9]
#Check for silent option
if not args.silent:
    print "Direct Link to the Video"


print (Fore.GREEN + filepath)
print (Style.RESET_ALL)

#Main Download Part
#Check for silent option
if not args.silent:
    print (Fore.BLUE + "Video download started!")
    video=urllib.FancyURLopener()
    video.retrieve(filepath, args.destination +"/"+ fname, reporthook=dlProgress)



#End the Program
#Check for silent option
if not args.silent:
    print (Style.RESET_ALL + "Thanks for using cloudchaser! Hope to see you again soon ;)")


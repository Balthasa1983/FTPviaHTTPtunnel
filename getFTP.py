import pycurl, StringIO, os

filestotransfer = []
filecontent = []

dest = '/filehandling/testinput'

alreadytransfered = os.listdir(dest)

c = pycurl.Curl()
c.setopt(pycurl.URL, r'ftp://ftp.server:21/outbound/')
c.setopt(pycurl.USERPWD, 'password')
c.setopt(pycurl.PROXY, 'http://proxy:8080')


# lets create a buffer in which we will write the output
output = StringIO.StringIO()
# lets assign this buffer to pycurl object
c.setopt(pycurl.WRITEFUNCTION, output.write)
# lets perform the LIST operation
c.perform()
# lets get the output in a string
result = output.getvalue()
# lets print the string on screen

# FTP LIST output is separated by \r\n
# lets split the output in lines
lines = result.split('\n')
# lets print the number of lines
print len(lines)
# lets walk through each line

for l in lines:
    if "<a href=\"" and "alt=\"[FILE]" in l:
        if  "ftp.server" not in l:
            filestotransfer.append(l.split("<a href=\"")[1].split("\"")[0])

for file in filestotransfer:
    if file not in alreadytransfered:
        c.setopt(pycurl.URL, r'ftp://ftp.server:21/outbound/' + file)
        #c.setopt(pycurl.VERBOSE, 1)
        # lets create a buffer in which we will write the output
        outputfile = StringIO.StringIO()
        # lets assign this buffer to pycurl object
        c.setopt(pycurl.WRITEFUNCTION, outputfile.write)
        # lets perform the LIST operation
        c.perform()
        # lets get the output in a string
        result = outputfile.getvalue()
        # lets print the string on screen

        f = open(dest + "/" + file, 'w')
        f.write(result)
        f.close()
c.close()




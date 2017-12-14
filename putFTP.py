import pycurl, StringIO, os, time

src = r'/filehandling/testouput'
dest = r'ftp://ftp.server:21/outbound_temp/'

filestotransfer = os.listdir(src)
filecontent = []
alreadytransfered = []

c = pycurl.Curl()
c.setopt(pycurl.URL, dest)
c.setopt(pycurl.USERPWD, 'password')

c.setopt(pycurl.PROXY, 'http://proxy:8080')

# lets create a buffer in which we will write the output
output = StringIO.StringIO()
# lets assign this buffer to pycurl object
c.setopt(pycurl.WRITEFUNCTION, output.write)
# lets perform the LIST operation
c.perform()

result = output.getvalue()

lines = result.split('\n')

for l in lines:
    if "<a href=\"" and "alt=\"[FILE]" in l:
        if  "ftp.server" not in l:
            alreadytransfered.append(l.split("<a href=\"")[1].split("\"")[0])

for file in filestotransfer:
    if file not in alreadytransfered:
        c.setopt(pycurl.URL, dest + file)
        filepath = src + '/' + file
        f = open(filepath)
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(filepath))
        c.setopt(pycurl.UPLOAD, 1)
        c.perform()
        os.remove(filepath)
c.close()




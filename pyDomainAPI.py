import httplib, sys, time
import base64
import string

def main(hFile):
    host = "api.domainapi.com"
    url = "/v1/historic_whois/xml/"
    username = 'xxxxx'
    password = 'xxxxx'
    message = 'some message'
     
    # base64 encode the username and password
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    szFileName = open(hFile).read().split('\n')
    for line in szFileName:
        final_url = url+line
        
        webservice = httplib.HTTP(host)
        # write your headers
        webservice.putrequest("POST", final_url)
        webservice.putheader("Host", host)
        webservice.putheader("User-Agent", "Python http auth")
        webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(message))
        # write the Authorization header like: 'Basic base64encode(username + ':' + password)
        webservice.putheader("Authorization", "Basic %s" % auth)
         
        webservice.endheaders()
        webservice.send(message)
        # get the response
        statuscode, statusmessage, header = webservice.getreply()
        res = webservice.getfile().read()
        filename = line + ".xml"
        hFileOut = open(filename, "wb")
        hFileOut.write(res)
        hFileOut.close()
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter need a filename!")
        exit(0)
    main(sys.argv[1])
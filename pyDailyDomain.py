# -*- coding: utf-8 -*-
import sys, os, re
import json
import datetime, time
from pytz import timezone
import sqlite3
from mechanize import Browser

global TLDs
TLDs = [['com','1'],['net','2'],['org','3'],['info','5'],['top','170'],['xyz','116'],['biz','4'],['site','121'],['online','117'],['club','38'],['loan','518'],['icu','177'],['vip', '134'],['shop', '221'],['work', '307'],['ltd', '145'],['mobi', '6'],['app', '96'],['live', '139'],['ooo', '411'],['pro', '109'],['website', '141'],['fun', '67'],['space', '207'],['store', '173'],['tech', '236'],['win', '285'],['life', '232'],['blog', '199'],['cloud', '166'],['world', '180'],['men', '266'],['dev', '561'],['stream', '114'],['wang', '153'],['host', '136'],['rocks', '133'],['cat', '179'],['bid', '235'],['tokyo', '369'],['today', '196'],['xxx', '113'],['design', '191'],['email', '238'],['solutions', '455'],['tel', '86'],['xin', '492'],['trade', '85'],['one', '185'],['link', '137'],['agency', '360'],['services', '317'],['nyc', '398'],['company', '429'],['group', '437'],['date', '502'],['review', '372'],['news', '77'],['ovh', '462'],['guru', '201'],['art', '323'],['network', '301'],['london', '333'],['photography', '574'],['berlin', '524'],['studio', '350'],['download', '124'],['jobs', '211'],['global', '278'],['media', '123'],['party', '308'],['xn--3ds443g', '1400'],['xn--55qx5d', '1411'],['realtor', '388'],['business', '396'],['center', '444'],['ink', '295'],['science', '472'],['digital', '314'],['racing', '313'],['click', '129'],['expert', '346'],['ninja', '127'],['technology','393'],['press', '100'],['bayern', '549'],['tips', '213'],['academy', '302'],['love', '200'],['xn--6qq986b3xl', '1415'],['systems', '300'],['city', '288'],['xn--p1acf', '418'],['webcam', '382'],['koeln', '554'],['xn--io0a7i','1455'],['amsterdam', '634'],['red', '293'],['sale', '371'],['market', '219']]

def _log(szString):
    print(szString)

def main(szZone, ecv):
    now = datetime.datetime.now(timezone('EST'))
    szDateTime = now.strftime("%Y-%m-%d")
    # Comment the following line once testing is completed.
    szDateTime = "2019-05-31"

    dbName = str(szDateTime) + '-DailyDomains' + '-'+ szZone + '.db'
    try:
        open(dbName)
        _log('[*] Database already exists!')
    except IOError as e:
        if e.args[0] == 2:
            conn = sqlite3.connect(dbName)
            _log('[+] Daily Domains database created')
            conn.execute('''CREATE TABLE "DailyDomains" (
                `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                `TYPE` TEXT NOT NULL, 
                `DOMAIN` TEXT NOT NULL, 
                `DATE` DATE );''')
            _log("[+] Table created successfully")
            conn.close()
    conn = sqlite3.connect(dbName)

    '''
    curl 'https://dnpedia.com/tlds/ajax.php?cmd=added&columns=id,name,length,idn,thedate,&ecf=zoneid,thedate&ecv=116,2019-05-25&zone=xyz&_search=false&nd=1558840672465&rows=2000&page=1&sidx=length&sord=asc' -H 'Cookie: TLD-Selection=xyz; PHPSESSID=dtsoafmu3l4tt53orl1apkcn8b; _jsuid=1602983283; _first_pageview=1' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://dnpedia.com/tlds/daily.php' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed
    '''
    
    szURL = "https://dnpedia.com/tlds/ajax.php?cmd=added&columns=id,name,length,idn,thedate,&ecf=zoneid,thedate&ecv="+ecv+","+szDateTime+"&zone=" + szZone + "&_search=false&nd=1558840672465&rows=2000&page=1&sidx=length&sord=asc"
    
    br = Browser()
    # Browser options
    # Ignore robots.txt. Do not do this without thought and consideration.
    br.set_handle_robots(False)

    # Don't add Referer (sic) header
    #br.set_handle_referer(False)
    # Don't handle Refresh redirections
    br.set_handle_refresh(False)

    # Setting the user agent as Chrome
    br.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"), ("Referer", "https://dnpedia.com/tlds/daily.php?_search=false&nd=1558840672465&rows=2000&page=1&sidx=length&sord=asc"), ("X-Requested-With", "XMLHttpRequest"), ('Accept','application/json, text/javascript, */*; q=0.01')]
    
    br.open(szURL)
    contents = br.response().read().decode('UTF-8')
    data = json.loads(contents)
    iRecords = data['records']
    iPages = data['total']
    _log("[+] Found %d records in %s. (%s pages)" % (iRecords, szZone, iPages))
    #print(data)
    
    for x in range(1, iPages+1):
        url = "https://dnpedia.com/tlds/ajax.php?cmd=added&columns=id,name,length,idn,thedate,&ecf=zoneid,thedate&ecv="+ecv+","+szDateTime+"&zone=" + szZone + "&_search=false&nd=1558788771703&rows=2000&page="+str(x)+"&sidx=length&sord=asc"
        br.open(url)
        contents = br.response().read().decode('UTF-8')
        Pagedata = json.loads(contents)
        iRows = len(Pagedata['rows'])
        for row in Pagedata['rows']:
            szDomain = bytes(row['name'], 'utf-8')
            dateRegistered = row['thedate']
            conn.execute('''INSERT INTO DailyDomains (TYPE, DOMAIN, DATE) VALUES (?,?,?)''', (szZone, szDomain, dateRegistered))
            conn.commit()
        _log("[+] Page %d of %s in .%s completed" % (x, iPages, szZone))
        time.sleep(5)
    _log("[+] %d records added." % iRecords)

if __name__ == "__main__":
    '''
    if (len(sys.argv) < 3):
        _log("[+] Usage: %s [zones : com, net, org, etc] [ecv]" % sys.argv[0])
        sys.exit(0)
    else:
        szZone = sys.argv[1]
        ecv = sys.argv[2]
        main(szZone, ecv)
    '''
    # Use the following codes once dnpedia.com is more stable and won't return # in the domain names.
    for tld in TLDs:
        szZone = tld[0]
        ecv = tld[1]
        main(szZone, ecv)
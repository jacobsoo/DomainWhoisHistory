DomainWhoisHistory
==================

~~Using domainAPI's Whois History API, we are not able to review data on domain name as it was at a specific date. 
All you need is to register a domainAPI account.
Using your own credentials and submit a domain name through the API and the API will retrieve the full historical whois record of the domain name at that time will be retrieved. 
This API service retrieves data from the leading Whois Service Provider “DomainTools”.~~

So the previous version stopped working for a few years, but i've made another one recently making use of the data from dnpedia
Hopefully this will last a longer period of time as it's a hassle to maintain my ICANN account to grab the zone files.

```python
python pyDailyDomain.py
```

After running the above script, it will start downloading the newly registered domain lists.
This is one of 3 methods which i'm using to detect Phishing websites.

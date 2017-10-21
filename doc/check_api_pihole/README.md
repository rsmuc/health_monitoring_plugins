## check_api_pihole.py:
---

Check a pihole server via it's json api. Checks the percentage blocked today, domains beeing blocked and dns queries today.

### Example:

```check_api_pihole.py -H 192.168.2.184 -p 80 --threshold metric="blocked_today",critical=1:5 --threshold metric="domains_being_blocked",critical=900000: --threshold metric="dns_queries_today",critical=1:30000
```
=> 
OK - Blocked Today: 3.872009%. Domains being blocked: 971495. DNS queries today: 22314 | 'blocked_today'=3.872009%%;;1:5;; 'domains_being_blocked'=971495Domains;;1:1000000;; 'dns_queries_today'=22314;;1:30000;;

```

* If there are more than 5 % of the DNS request blocked for today, critical status will be shown. More than 5% could indicate that something strange is happening in our network.
We also want to be informed, if less than 1% of the DNS request will be blocked. That could indicate that something with pihole is going wrong.


* We want so ensure hat we have at least 900000 domains on our blocklist. If the update of our block lists goes wrong and there are less than 900000 domains on the blocklist, we will get informed.


* And we want to check the amount of DNS queries per day. More than 30.000 request per days can indicate again an issue in the network.

All three metrics will be returned as performance graphs, so pnp4nagios will print a nice graph. If you don't want one of the metrics beeing checked, just remove the corresponding threshold parameter.

### Options
```
-Options:
-  -h, --help            show this help message and exit
-  -p PORT               the port the lighthttp webserver (default: 80)
-  -H HOST               the IP address or hostname pihole is running)

```

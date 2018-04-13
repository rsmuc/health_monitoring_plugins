## check_jenkins_api.py:
---

Check the status the Jenkins job queue.

The plugin requires pynag (https://github.com/pynag/pynag) and python-netsnmp.

The plugin checks the age of all Jobs in the Jenkins job queue. IF the age of a single job is older than X hours, a critical status is shown.
We want to avoid that the Jenkins job queue is growing and growing and we don't get notified.

The plugin is just a quick and dirty solution to monitor our Jenkins. For the plugin there is no automatic test or a quality control.


### Example:


```./check_jenkins.py -H 'myjenkins.domain.net/MYJENKINS' -U 'user' -P 'password' -A 12.0```
```
```
=> 
Critical - JENKINS JOB WAITING FOR 14.0 hours - CHECK INSTANCES
```
### Options
```
  -h, --help            show this help message and exit

  -p PORT               the port the Jenkins webserver (default: 80)

  -H HOST               the IP address or hostname of the Jenkins

  -U USER               the user for the basic authentication)

  -P PASSWORD           the password for the basic authentication)

  -A AGE                the maximum age of a Jenkins job in hours


```
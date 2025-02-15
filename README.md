# Anti_Rubber_Ducky

This Python script automatically runs in the background, checking for any unauthorized USB plug-ins. 
If an unauthorized device is detected, it uses SMTP to send an email to the admin (on loop) and shuts down the system to prevent malicious access.  

**Note:** The subprocess for shutting down the system is commented out.  

### STEPS TO INSTALL AND RUN  
1. Download the Python script.  
2. Open CMD as an administrator and navigate to the downloaded file's location.  
3. Type `"python anti_rubber_ducky.py install"` in CMD.  
4. To start the service, type `"python anti_rubber_ducky.py start"`.  
5. To check the service status, type `"sc query ANTIRUBBER"`.  
6. To stop the service, type `"python anti_rubber_ducky.py stop"`.  
7. To remove the service, type `"python anti_rubber_ducky.py remove"`.
8. 
---

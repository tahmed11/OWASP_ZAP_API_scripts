# A helpful reference: https://github.com/zaproxy/zaproxy/wiki/ApiPython
import time
import urllib2
from pprint import pprint
from zapv2 import ZAPv2

# The value of api must match api.key when running the daemon
api = "j32fdrpgqmu1n0b855336rmf22"
policy = '/home/ubuntu/.ZAP_D/Hackazon.policy'
policy_name = 'Hackazon'
myApp = 'http://www.hackazon.com/api/category?page=1&per_page=50'
context_file = '/home/ubuntu/.ZAP_D/contexts/Hackazon_API_Context.context'
context_name = 'Hackazon_Context'
user_name = 'test_user'
authentication_script = '/home/ubuntu/.ZAP_D/scripts/scripts/authentication/Hackazon_Auth.py' 
http_sender_script = '/home/ubuntu/.ZAP_D/scripts/scripts/httpsender/Hackazon_Token.py' 

#The following line must be the ip of where ZAP is, so for us it is localhost:8080
#Also if you are not running ZAP on port 8080 then you must include the line below with the correct port numbers.
zap = ZAPv2(apikey=api)

# The script must be loaded prior to importing the context otherwise it will fail.
# Additionally, the APIKEY must be the last parameter on every method.

# Importing the context using the full file path.
print("IMPORTING CONTEXT")
zap.context.import_context(context_file, apikey = api)
#remove default context
zap.context.remove_context("Default Context", apikey = api)

#Sets forced user mode to force authentication 
zap.forcedUser.set_forced_user_mode_enabled(True, apikey = api)

#Loading ZAP authentication script
zap.script.load(apikey = api, scriptname = 'hackazon_api_authentication' , scripttype = 'authentication', scriptengine = 'jython', filename= authentication_script );
zap.script.enable('hackazon_api_authentication');


#Loading ZAP httpsender script
zap.script.load(apikey = api, scriptname = 'hackazon_api_proxy' , scripttype = 'httpsender', scriptengine = 'jython', filename= http_sender_script);
zap.script.enable('hackazon_api_authentication');


# The URL must be opened before it can be tested on.
print('Accessing target %s' % myApp)

zap.urlopen(myApp)

time.sleep(2)

# Start the active scan and wait till it's complete

#Import scan policy
#print ('Importing scan policy from: ' + policy)
#zap.ascan.import_scan_policy(policy)
#zap.ascan.set_enabled_policies(1, policy_name)
print ('Active Scanning target ' + myApp)
#best to manually check the contextid (context policy id) and userid from the UI for the first run. 
ascan_id = zap.ascan.scan_as_user(url = myApp, contextid = 2, userid = 1, recurse = False, scanpolicyname = policy_name, apikey = api)
#ascan_id = zap.ascan.scan_as_user(url = myApp, contextid = 2, userid = 0, recurse = True, apikey = api)

#time for scanner to start
time.sleep(5)
while (int(zap.ascan.status()) < 100):
    print ('Scan progress %: ' + zap.ascan.status())
    time.sleep(5)

print ('Scan completed')

#pprint (zap.core.alerts())
print 'Alert Summary:'
print (zap.core.alerts_summary())

print 'ZAP Active scan results'

# Writes the XML and HTML reports that will be exported to the workspace.
f = open('/home/ubuntu/Desktop/OWASP_ZAP_scripts/apireport.xml','w')
f.write(zap.core.xmlreport(apikey = api))
f.close()
f2 = open('/home/ubuntu/Desktop/OWASP_ZAP_scripts/apireport.html','w')
f2.write(zap.core.htmlreport(apikey = api))
f2.close()

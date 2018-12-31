import base64, urllib, json
import java.lang.String, jarray
import org.parosproxy.paros.network.HttpRequestHeader as HttpRequestHeader
import org.parosproxy.paros.network.HttpHeader as HttpHeader
import org.zaproxy.zap.extension.script.ScriptVars as GlobalVariables
from org.apache.commons.httpclient import URI
from urllib import quote

def authenticate(helper, paramsValues, credentials):
    #print "API-based authenticating via Jython script..."
    # Prepare the login request details
    requestUri = URI(paramsValues["Auth_URL"], False);
    requestMethod = HttpRequestHeader.GET;

    extraPostData = paramsValues["Extra_POST_data"];
    #username = "test_user"; password = "123456";

    username = quote(credentials.getParam("Username")).encode('utf-8');
    password = quote(credentials.getParam("Password")).encode('utf-8');
    #print "Using username %s and password %s " % (username, password);
    encoded_data = (username + ":" + password).encode('utf-8');
    basic = "Basic " + base64.b64encode(encoded_data);
   
    print "Authorization: %s " % (basic);
    if len(extraPostData.strip()) > 0:
        requestBody = requestBody + "&" + extraPostData.strip();
    # Build the actual message to be sent
    msg = helper.prepareMessage();
    
    requestHeader = HttpRequestHeader(requestMethod, requestUri, HttpHeader.HTTP10);
    #header_basic = "Authorization: " + basic;
    requestHeader.setHeader(HttpRequestHeader.AUTHORIZATION, basic);
    msg.setRequestHeader(requestHeader);
    # Send the authentication message and return it
    #print "Sending %s request to %s" % (requestMethod, requestUri);
    helper.sendAndReceive(msg);
    #print "Received response status code for authentication request: %d" % msg.getResponseHeader().getStatusCode();
    #print "Response body:";
    #print msg.getResponseBody();
    #{"message":"Your token is established.","code":200,"trace":"","token":"4b2c75efb454344aaa3aafd15b0aa87db3c92daf"}
    #return_token returns the token value to be used 
    token = return_token(msg);
   
    # set the token as global variable so can be used by httpsender module
    GlobalVariables.setGlobalVar("hackazon_token",token);
    return msg;

def getRequiredParamsNames():
    return jarray.array(["Auth_URL"], java.lang.String);

def getOptionalParamsNames():
    return jarray.array(["Extra_POST_data"], java.lang.String);

def getCredentialsParamsNames():
    return jarray.array(["Username", "Password"], java.lang.String);
    
def return_token(msg):
    token_array = json.loads(msg.getResponseBody().toString());
    token = token_array['token'];
    #print token;
    token = "Token " + token; 
    return token;  

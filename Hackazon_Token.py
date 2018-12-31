import org.zaproxy.zap.extension.script.ScriptVars as GlobalVariables

def sendingRequest(msg, initiator, helper):
    
    if GlobalVariables.getGlobalVar("hackazon_token") is None:
        print "Do nothing token not set";
        return
    else:
         token = GlobalVariables.getGlobalVar("hackazon_token");
         msg.getRequestHeader().setHeader("Authorization", token); 
         print('Adding token to request url=' + msg.getRequestHeader().getURI().toString());
         print("Authorization: " +token);
         return

def responseReceived(msg, initiator, helper):
    return
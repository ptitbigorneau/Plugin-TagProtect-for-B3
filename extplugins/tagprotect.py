# TagProtect Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.4.1'


import b3, threading, thread, time
import b3.plugin
import b3.events
from b3 import clients

class TagprotectPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _ctadminlevel = 100
    _listclanlevel = 1
    _clanname = None
    _clanexacttag = None
    _clansecondtag = None
    _clanapprotag = None
    _banactived = "no"
    _pluginactived = "off"

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)
        self.registerEvent(b3.events.EVT_CLIENT_NAME_CHANGE)
        self.registerEvent(b3.events.EVT_CLIENT_CONNECT)

        self._adminPlugin.registerCommand(self, 'tagprotect',self._ctadminlevel, self.cmd_tagprotect)
        self._adminPlugin.registerCommand(self, 'addct',self._ctadminlevel, self.cmd_addct)
        self._adminPlugin.registerCommand(self, 'delct',self._ctadminlevel, self.cmd_delct)
        self._adminPlugin.registerCommand(self, 'listmemberclan',self._listclanlevel, self.cmd_listmemberclan, 'ltmc')
    
    def onLoadConfig(self):

        try:
            self._ctadminlevel = self.config.getint('settings', 'ctadminlevel')
        except Exception, err:    
            self.warning("ctadminlevel using default value. %s" % (err))

        try:
            self._listclanlevel = self.config.getint('settings', 'listclanlevel')
        except Exception, err:    
            self.warning("listclanlevel using default value. %s" % (err))

        try:
            self._clanname = self.config.get('settings', 'clanname')
        except Exception, err:    
            self.warning("clanname is None. %s" % (err))

        try:
            self._clanexacttag = self.config.get('settings', 'clanexacttag')
        except Exception, err:    
            self.warning("clanexacttag is None. %s" % (err))

        try:
            self._clansecondtag = self.config.get('settings', 'clansecondtag')
        except Exception, err:    
            self.warning("clansecondtag is None. %s" % (err))

        try:
                   self._clanapprotag = self.config.get('settings', 'clanapprotag')
        except Exception, err:    
            self.warning("clanapprotag is None. %s" % (err))

        try:
            self._banactived = self.config.get('settings', 'banactived')
        except Exception, err:    
            self.warning("banactived using default value. %s" % (err))
			
        try:
             self._pluginactived = self.config.get('settings', 'pluginactived')
        except Exception, err:    
            self.warning("pluginactived using default value. %s" % (err))
    
    def onEvent(self, event):

        if (event.type == b3.events.EVT_CLIENT_AUTH) or (event.type == b3.events.EVT_CLIENT_NAME_CHANGE):
		
            if self._pluginactived == 'off':
           
               self.debug('TagProtect %s'%(self._pluginactived))
               return False

            if self._pluginactived == 'on':
            
                self.debug('TagProtect %s'%(self._pluginactived))
                    
            client = event.client
            self.debug('TagProtect client : %s'%(client.name))
            if client.maxLevel == 100:
                self.debug('TagProtect superadmin : %s'%(client.name))
                return False

            cnamemin = client.name.lower()

            exacttagmin = self._clanexacttag.lower()

            cexacttagmin = cnamemin.count(exacttagmin)

            secondtagmin = self._clansecondtag.lower()

            csecondtagmin =  cnamemin.count(secondtagmin)

            approtagmin = self._clanapprotag.lower()

            capprotagmin =  cnamemin.count(approtagmin)
            self.debug('%s - %s - %s'%(exacttagmin, secondtagmin, approtagmin))
                
            if cexacttagmin > 0:
    
                cursor = self.console.storage.query("""
                SELECT *
                FROM tagprotect n 
                WHERE n.client_id = %s
                """ % (client.id))
        
                if cursor.rowcount == 0:
                
                    tag = self._clanexacttag
                    thread.start_new_thread(self.bantag, (client, event, tag))
                
                else:
                        
                    time.sleep(10)
                    client.message('Hi ! ^1%s^7 member'%(self._clanexacttag))
                        
                    return False
                
            elif csecondtagmin > 0:
                
                cursor = self.console.storage.query("""
                SELECT *
                FROM tagprotect n 
                WHERE n.client_id = %s
                """ % (client.id))
        
                if cursor.rowcount == 0:
                
                    tag = self._clansecondtag
                    thread.start_new_thread(self.bantag, (client, event, tag))
               
                else:
                        
                    time.sleep(10)
                    client.message('Hi ! ^1%s^7 member'%(self._clansecondtag))

                return False            

            elif capprotagmin > 0:

                cnamenotag = cnamemin.split(approtagmin)
                debcnamenotag = cnamenotag[0]
                fincnamenotag = cnamenotag[1]

                if (debcnamenotag[-1:] not in "abcdefghijklmnopqrstuvwxyz") or (fincnamenotag[:1] not in "abcdefghijklmnopqrstuvwxyz") or (cnamemin.find(approtagmin)==0):
               
                    cursor = self.console.storage.query("""
                    SELECT *
                    FROM tagprotect n 
                    WHERE n.client_id = %s
                    """ % (client.id))
        
                    if cursor.rowcount == 0:
                
                        thread.start_new_thread(self.kicktag, (client, event, approtagmin))
               
                    else:
                        
                        time.sleep(10)
                        client.message('Hi ! ^1%s^7 member'%(self._clanexacttag))
                        
                        return False
                              
                else:
                
                    return False
            
            else:
            
                return False

    def kicktag(self, client, event, approtagmin):
        
        time.sleep(20)
        client.message('^1%s^7 is the tag of the clan ^1%s^7'%(self._clanexacttag, self._clanname))
        time.sleep(2)         
        client.message('You are not a member of the clan ^1%s^7'%(self._clanname))
        time.sleep(2) 
        client.message('^1%s^7 in your nickname is not authorized'%(approtagmin))
        client.message('You will be ^1kicked')
        time.sleep(10)
        client.kick("%s TagProtect"%(self._clanexacttag),  None)
        
    def bantag(self, client, event, tag):
        
        if self._banactived == 'yes':
        
            time.sleep(20)
            client.message('^1%s^7 and ^1%s^7 are the tag of the clan ^1%s^7'%(self._clanexacttag, self._clansecondtag, self._clanname))
            time.sleep(2)        
            client.message('You are not a member of the clan ^1%s^7'%(self._clanname))
            time.sleep(2) 
            client.message('^1%s^7 in your nickname is not authorized'%(tag))
            client.message('You will be ^1banned')
            time.sleep(10)
            client.ban("%s TagProtect"%(tag), None)
        
        else:
        
            time.sleep(20)
            client.message('^1%s^7 and ^1%s^7 are the tag of the clan ^1%s^7'%(self._clanexacttag, self._clansecondtag, self._clanname))
            time.sleep(2)         
            client.message('if you are a member of ^1%s^7 clan ! Contact administrator !'%(self._clanname))
            time.sleep(2) 
            client.message('^1%s^7 in your nickname is not authorized'%(tag))
            client.message('You will be ^1kicked')
            time.sleep(10)
            client.kick("%s TagProtect"%(tag),  None)
            
    def cmd_addct(self, data, client, cmd=None):
        """\
        - Add member clan or team
        """

        if data:
            input = self._adminPlugin.parseUserCmd(data)
        else:
            client.message('!addct <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM tagprotect n 
            WHERE n.client_id = '%s'
            """ % (sclient.id))

            if cursor.rowcount > 0:
  
                client.message('%s is already registered' %(sclient.exactName))
                cursor.close()
                
                return False
            
            cursor.close()
            
            cursor = self.console.storage.query("""
            INSERT INTO tagprotect
            VALUES (%s)
            """ % (sclient.id))

            cursor.close()
            
            client.message('%s is now registered' %(sclient.exactName))
       
        else:
            return False

    def cmd_listmemberclan(self, data, client, cmd=None):
        """\
        - Member clan or team list 
        """
        
        thread.start_new_thread(self.listmemberclan, (data, client))
        
    def listmemberclan(self, data, client):
            
        cursor = self.console.storage.query("""
        SELECT *
        FROM tagprotect
        ORDER BY client_id
        """)
        
        c = 1
        
        if cursor.EOF:
          
            client.message('No member in the list')
            cursor.close()            
            return False
        
        while not cursor.EOF:
            sr = cursor.getRow()
            cid = sr['client_id']
            scid= '@'+str(cid)
            sclient = self._adminPlugin.findClientPrompt(scid, client)
            client.message('^2%s^7 - id : ^2@%s^7 - level : (^1%s^7)' % (sclient.exactName, cid, sclient.maxLevel))
            cursor.moveNext()
            c += 1
            
        cursor.close()
        
    def cmd_delct(self, data, client, cmd=None):
        
        """\
        Delete member clan or team
        """
        
        if data:
        
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!delct <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
        
            cursor = self.console.storage.query("""
            SELECT n.client_id
            FROM tagprotect n 
            WHERE n.client_id = '%s'
            """ % (sclient.id))
        
            if cursor.rowcount == 0:
                
                client.message("%s ^7is not in the the list of members"%(sclient.exactName))
                
                return False
            
            cursor.close()
        
            cursor = self.console.storage.query("""
            DELETE FROM tagprotect
            WHERE client_id = '%s'
            """ % (sclient.id))
            cursor.close()
            
            client.message("%s ^7has been eliminated from the list of members"%(sclient.exactName))
            
        else:
            return False

    def cmd_tagprotect(self, data, client, cmd=None):
        
        """\
        activate / deactivate tagprotect 
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._pluginactived == 'on':

                client.message('^3Tagprotect ^2activated^7')

            if self._pluginactived == 'off':

                client.message('^3Tagprotect ^1deactivated^7')

            if self._banactived == 'yes':

                client.message('^3Ban ^2activated^7')

            if self._banactived == 'no':

                client.message('^3Ban ^1deactivated^7')

            client.message('!tagprotect <on / off> <ban yes / ban no> ')
            return
      
        
        if input[0] == 'on':

            if self._pluginactived != 'on':

                self._pluginactived = 'on'
                message = '^3Tagprotect ^2activated^7'
                modif = "pluginactived: %s\n"%(self._pluginactived)
                settingname = "pluginactived:"

            else:

                client.message('^3Tagprotect is already ^2activated^7') 

                return False

        if input[0] == 'off':

            if self._pluginactived != 'off':

                self._pluginactived = 'off'
                message = '^3Tagprotect ^1deactivated^7'
                modif = "pluginactived: %s\n"%(self._pluginactived)
                settingname = "pluginactived:"

            else:
                
                client.message('Tagprotect is already ^1disabled^7')                

                return False

        if input[0] == 'ban':

            if input[1] == 'yes':

                if self._banactived != 'yes':

                    self._banactived = 'yes'
                    message = '^3Ban ^2activated^7'
                    modif = "banactived: %s\n"%(self._banactived)
                    settingname = "banactived:"

                else:

                    client.message('^3Ban is already ^2activated^7') 

                    return False

            elif input[1] == 'no':
                
                if self._banactived != 'no':

                    self._banactived = 'no'
                    message = '^3Ban ^1disabled^7'
                    modif = "banactived: %s\n"%(self._banactived)
                    settingname = "banactived:"

                else:

                    client.message('^3Ban is already ^1disabled^7') 

                    return False
            else:

                client.message('!tagprotect <ban yes / ban no> ')
                return        

        client.message('tagprotect %s'%(message))

        fichier = self.config.fileName

        tagprotectini = open(fichier, "r")
        
        contenu = tagprotectini.readlines()

        tagprotectini.close()

        newcontenu = ""

        for ligne in contenu:

            if settingname in ligne:

                ligne = modif

            newcontenu = "%s%s"%(newcontenu, ligne)        

        tagprotectiniw = open(fichier, "w")
        tagprotectiniw.write(newcontenu)
        tagprotectiniw.close()

    def wait(self, temps):

        time.sleep(temps)
        return

         

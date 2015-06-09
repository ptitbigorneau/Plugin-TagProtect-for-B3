# tagprotect plugin
# Plugin for B3 (www.bigbrotherbot.com)
# www.ptitbigorneau.fr

tagprotect plugin (v1.4) for B3

Installation:

1. Place the tagprotect.py in your ../b3/extplugins and the 
tagprotect.ini in your ../b3/extplugins/conf folders.

2. Open your B3.xml file (default in b3/conf) and add the next line in the
<plugins> section of the file:

<plugin name="tagprotect" config="@b3/extplugins/conf/tagprotect.ini"/>

3. Open tagprotect.ini

modify clan name (exemple : The Pirate Family )
modify tag exact (exemple : -[TPF]- )
modify second tag (exemple : -[TPF-T]- for test member by exemple)
modify approximate tag (exemple tpf )
modify pluginactived on/off
modify banactived yes/no

4. Run the contact SQL script (tagprotect.sql) on your B3 database

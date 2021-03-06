#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import some stuff
import sys 
import socket 
import string 
import random 
import os #not necassary but later on I am going to use a few features from this 
import feedparser # http://wiki.python.org/moin/RssLibraries

#Settings
HOST='irc.bsnet.se' 			#The server we want to connect to 
PORT=6667 								#The connection port which is usually 6667 
NICK='marvin' 						#The bot's nickname 
IDENT='***' 
REALNAME='Mr Marvin Bot' 
OWNER='mos' 							#The bot owner's nick 
CHANNEL='#db-o-webb'			    #The default channel for the bot 
readbuffer='' 						#Here we store all the messages from server 
FEED='http://dbwebb.se/forum/feed.php'
SEARCH='http://dbwebb.se/forum/search.php?keywords='

#Function to parse incoming messages
def parsemsg(msg): 
	complete=msg[1:].split(':',1) #Parse the message into useful data 
	info=complete[0].split(' ') 
	msgpart=complete[1] 
	sender=info[0].split('!') 
	if msgpart[0]=='`' and sender[0]==OWNER: #Treat all messages starting with '`' as command 
		cmd=msgpart[1:].split(' ') 
		if cmd[0]=='op': 
			s.send('MODE '+info[2]+' +o '+cmd[1]+'n') 
		if cmd[0]=='deop': 
			s.send('MODE '+info[2]+' -o '+cmd[1]+'n') 
		if cmd[0]=='voice': 
			s.send('MODE '+info[2]+' +v '+cmd[1]+'n') 
		if cmd[0]=='devoice': 
			s.send('MODE '+info[2]+' -v '+cmd[1]+'n') 
		if cmd[0]=='sys': 
			syscmd(msgpart[1:],info[2]) 
			 
	if msgpart[0]=='-' and sender[0]==OWNER : #Treat msgs with - as explicit command to send to server 
		cmd=msgpart[1:] 
		s.send(cmd+'n') 
		print 'cmd='+cmd 


#This piece of code takes the command and executes it printing the output to ot.txt. Then ot.txt is 
#read and displayed to the given channel.Multiline output is shown by using '|'. 
def syscmd(commandline,channel): 
    cmd=commandline.replace('sys ','') 
    cmd=cmd.rstrip() 
    os.system(cmd+' >temp.txt') 
    a=open('temp.txt') 
    ot=a.read() 
    ot.replace('n','|') 
    a.close() 
    s.send('PRIVMSG '+channel+' :'+ot+'n') 
    return 0 


#Connect 
#Create the socket  & Connect to the server
s=socket.socket( ) 																		
print "Connecting: %s:%d" % (HOST, PORT)
s.connect((HOST, PORT)) 

#Send the nick to server 
msg='NICK %s\r\n' % NICK
print "Send: "+msg
s.send(msg)

#Identify to server 
msg='USER  %s %s dbwebb.se :%s\r\n' % (NICK, HOST, REALNAME)
print "Send: "+msg
s.send(msg) 

#This is my nick, i promise!
msg='PRIVMSG nick IDENTIFY %s\r\n' % IDENT
print "Send: "+msg
s.send(msg) 	

#Join a channel 
msg='JOIN %s\r\n' % CHANNEL
print msg
s.send(msg) 		


#Wait and listen
#We recieve the server input in a variable line; if you want to see the servers messages, 
#use print line. Once we connect to the server, we join a channel. Now whenever we recieve 
#any PRIVMSG, we call a function which does the appropriate action. The next few lines are 
#used to reply to a servers PING. Until this point, the bot just sits idle in a channel. 
#To make it active we use the parsemsg function. 
#PRIVMSG are usually of this form: 
# :nick!username@host PRIVMSG channel/nick :Message 
msgs=['Ja, vad kan jag göra för Dig?', 'Låt mig hjälpa dig.', 'Ursäkta, vad önskas?', 
'Kan jag stå till din tjänst?', 'Jag kan svara på alla dina frågor.', 'Ge me hög-fem!',
'Jag svarar endast inför mos och ake1, de är mina herrar.', 'ake1 är kungen!',
'Oh, ursäkta, jag slumrade visst till.', 'fråga, länka till kod och source.php och vänta på svaret.']

smile=[':-D', ':-P', ';-P', ';-)', ':-)', '8-)']

lunch=['ska vi ta boden uppe på parkeringen idag? en pasta, ris eller kebabrulle?', 
'ska vi dra ned till den indiska och ta en 1:a, den är stark o fin, man får ju bröd också.', 
'thairestaurangen var inte så dum borta vid korsningen.', 
'jag har med mig en matlåda hemmifrån så det är lugnt idag.', 
'ska vi chansa och ta BTH-fiket? kan ju ta en färdig sallad om inte annat...', 
'det är lite mysigt i fiket jämte demolabbet, där kan man hitta något enkelt.',
'jag bantar så jag ligger lågt med maten idag. måste ha lite koll på vikten.']

while 1: 
  readbuffer=readbuffer+s.recv(1024)
  temp=string.split(readbuffer, "\n")
  readbuffer=temp.pop( )
  
  for line in temp:
    line=string.rstrip(line)
    line=string.split(line)
    print "mumin: %s" % line
  
    if(line[0]=="PING"):
      msg="PONG %s\r\n" % line[1]
      print msg
      s.send(msg)

    if line[1]=='PRIVMSG' and line[2]==CHANNEL and line[3]==':%s:' % NICK:
      if line[4] and (line[4]=='latest' or line[4]=='senaste'):
        feed=feedparser.parse(FEED)
        msg="PRIVMSG %s :Senast hänt i forumet: %s (%s)\r\n" % (CHANNEL, feed["items"][0]["title"].encode('utf-8', 'ignore'), feed["items"][0]["link"].encode('utf-8', 'ignore'))
        print str(msg)
        s.send(msg)
      elif line[4] and (line[4]=='sök' or line[4]=='search'):
        search='%20'.join(line[5:])
        if search:        
          msg="PRIVMSG %s :Det kan hjälpa att söka i forumet: %s%s\r\n" % (CHANNEL, SEARCH, search)
        else:
          msg="PRIVMSG %s :Vad vill du söka efter för nyckelord?\r\n" % CHANNEL
        print str(msg)
        s.send(msg)
      elif line[4] and (line[4]=='smile' or line[4]=='le'):
        feed=feedparser.parse(FEED)
        msg="PRIVMSG %s :%s\r\n" % (CHANNEL, smile[random.randint(0,len(smile)-1)])
        print str(msg)
        s.send(msg)
      elif line[4] and (line[4]=='help' or line[4]=='hjälp'):
        msg="PRIVMSG %s :Ställ din fråga, länka till exempel och source.php. Vänta på svar.\r\n" % (CHANNEL)
        print str(msg)
        s.send(msg)
      elif line[4] and (line[4]=='lunch' or line[4]=='mat' or line[4]=='käk'):
        feed=feedparser.parse(FEED)
        msg="PRIVMSG %s :%s\r\n" % (CHANNEL, lunch[random.randint(0,len(lunch)-1)])
        print str(msg)
        s.send(msg)
      else:
        msg="PRIVMSG %s :%s\r\n" % (CHANNEL, msgs[random.randint(0,len(msgs)-1)])
        print msg
        s.send(msg)
        #parsemsg(line) 
        #line=line.rstrip() 		#remove trailing '\r\n' 
        #line=line.split() 
  

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║           AI RACING LEAGUE — Go full speed with IBM Bob 🏎️                   ║
# ║                  Academic Competition Entry                                  ║
# ║                                                                              ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║                                                                              ║
# ║   Team:  Y A R A R Á                                                         ║
# ║                                                                              ║
# ║        __|=====|__                                                           ║
# ║       /  |  F1 |  \      ~  ~  ~  ~  ~  ~  ~  ~  ~                         ║
# ║      / .-'-----'-, \     ~  ~~~  IBM Bob  ~~~  ~  ~                         ║
# ║     | ( O )   ( O ) |    ~   ___   ~   ~   ~   ~  ~                         ║
# ║      \_____________/     ~  (>-<)  <— 🐝 Bob                                ║
# ║                          ~  /| |\  ~   ~   ~   ~  ~                         ║
# ║   🐍  Yarará  🐍           ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~                           ║
# ║                                                                              ║
# ║     /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\                  ║
# ║    <  ~~~~  South American Pit Viper  ~~~~  Yarará  ~~~~  >                 ║
# ║     \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/                  ║
# ║                                                                              ║
# ║     ~~  ,----,   IBM 🐝                                                      ║
# ║    ~~ ,'     `.  ========================                                   ║
# ║   ~~  |  BOB  |  Your AI Coding Partner                                     ║
# ║    ~~ `.     ,'  ========================                                   ║
# ║     ~~  `----'                                                               ║
# ║                                                                              ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║                                                                              ║
# ║   Based on snakeoil.py by Chris X Edwards <snakeoil@xed.ch>                  ║
# ║   Python3 adaptation for TORCS robot client                                  ║
# ║   Original: http://scr.geccocompetitions.com/                                ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
#!/usr/bin/python
# snakeoil.py
# Chris X Edwards <snakeoil@xed.ch>
# Snake Oil is a Python library for interfacing with a TORCS
# race car simulator which has been patched with the server
# extentions used in the Simulated Car Racing competitions.
# http://scr.geccocompetitions.com/
#
# To use it, you must import it and create a "drive()" function.
# This will take care of option handling and server connecting, etc.
# To see how to write your own client do something like this which is
# a complete working client:
# /-----------------------------------------------\
# |#!/usr/bin/python                              |
# |import snakeoil                                |
# |if __name__ == "__main__":                     |
# |    C= snakeoil.Client()                       |
# |    for step in xrange(C.maxSteps,0,-1):       |
# |        C.get_servers_input()                  |
# |        snakeoil.drive_example(C)              |
# |        C.respond_to_server()                  |
# |    C.shutdown()                               |
# \-----------------------------------------------/
# This should then be a full featured client. The next step is to
# replace 'snakeoil.drive_example()' with your own. There is a
# dictionary which holds various option values (see `default_options`
# variable for all the details) but you probably only need a few
# things from it. Mainly the `trackname` and `stage` are important
# when developing a strategic bot.
#
# This dictionary also contains a ServerState object
# (key=S) and a DriverAction object (key=R for response). This allows
# you to get at all the information sent by the server and to easily
# formulate your reply. These objects contain a member dictionary "d"
# (for data dictionary) which contain key value pairs based on the
# server's syntax. Therefore, you can read the following:
#    angle, curLapTime, damage, distFromStart, distRaced, focus,
#    fuel, gear, lastLapTime, opponents, racePos, rpm,
#    speedX, speedY, speedZ, track, trackPos, wheelSpinVel, z
# The syntax specifically would be something like:
#    X= o[S.d['tracPos']]
# And you can set the following:
#    accel, brake, clutch, gear, steer, focus, meta
# The syntax is:
#     o[R.d['steer']]= X
# Note that it is 'steer' and not 'steering' as described in the manual!
# All values should be sensible for their type, including lists being lists.
# See the SCR manual or http://xed.ch/help/torcs.html for details.
#
# If you just run the snakeoil.py base library itself it will implement a
# serviceable client with a demonstration drive function that is
# sufficient for getting around most tracks.
# Try `snakeoil.py --help` to get started.

# for Python3-based torcs python robot client
import socket
import sys
import getopt
import os
import time
import csv
import math
import uuid
import hashlib
import datetime
PI= 3.14159265359

data_size = 2**17

# Initialize help messages
ophelp=  'Options:\n'
ophelp+= ' --host, -H <host>    TORCS server host. [localhost]\n'
ophelp+= ' --port, -p <port>    TORCS port. [3001]\n'
ophelp+= ' --id, -i <id>        ID for server. [SCR]\n'
ophelp+= ' --steps, -m <#>      Maximum simulation steps. 1 sec ~ 50 steps. [100000]\n'
ophelp+= ' --episodes, -e <#>   Maximum learning episodes. [1]\n'
ophelp+= ' --track, -t <track>  Your name for this track. Used for learning. [unknown]\n'
ophelp+= ' --stage, -s <#>      0=warm up, 1=qualifying, 2=race, 3=unknown. [3]\n'
ophelp+= ' --debug, -d          Output full telemetry.\n'
ophelp+= ' --help, -h           Show this help.\n'
ophelp+= ' --version, -v        Show current version.'
usage= 'Usage: %s [ophelp [optargs]] \n' % sys.argv[0]
usage= usage + ophelp
version= "20130505-2"

def clip(v,lo,hi):
    if v<lo: return lo
    elif v>hi: return hi
    else: return v

def bargraph(x,mn,mx,w,c='X'):
    '''Draws a simple asciiart bar graph. Very handy for
    visualizing what's going on with the data.
    x= Value from sensor, mn= minimum plottable value,
    mx= maximum plottable value, w= width of plot in chars,
    c= the character to plot with.'''
    if not w: return '' # No width!
    if x<mn: x= mn      # Clip to bounds.
    if x>mx: x= mx      # Clip to bounds.
    tx= mx-mn # Total real units possible to show on graph.
    if tx<=0: return 'backwards' # Stupid bounds.
    upw= tx/float(w) # X Units per output char width.
    if upw<=0: return 'what?' # Don't let this happen.
    negpu, pospu, negnonpu, posnonpu= 0,0,0,0
    if mn < 0: # Then there is a negative part to graph.
        if x < 0: # And the plot is on the negative side.
            negpu= -x + min(0,mx)
            negnonpu= -mn + x
        else: # Plot is on pos. Neg side is empty.
            negnonpu= -mn + min(0,mx) # But still show some empty neg.
    if mx > 0: # There is a positive part to the graph
        if x > 0: # And the plot is on the positive side.
            pospu= x - max(0,mn)
            posnonpu= mx - x
        else: # Plot is on neg. Pos side is empty.
            posnonpu= mx - max(0,mn) # But still show some empty pos.
    nnc= int(negnonpu/upw)*'-'
    npc= int(negpu/upw)*c
    ppc= int(pospu/upw)*c
    pnc= int(posnonpu/upw)*'_'
    return '[%s]' % (nnc+npc+ppc+pnc)

class Client():
    def __init__(self,H=None,p=None,i=None,e=None,t=None,s=None,d=None,vision=False):
        # If you don't like the option defaults,  change them here.
        self.vision = vision

        self.host= 'localhost'
        self.port= 3001
        self.sid= 'SCR'
        self.maxEpisodes=1 # "Maximum number of learning episodes to perform"
        self.trackname= 'unknown'
        self.stage= 3 # 0=Warm-up, 1=Qualifying 2=Race, 3=unknown <Default=3>
        self.debug= False
        self.maxSteps= 100000  # 50steps/second
        self.parse_the_command_line()
        if H: self.host= H
        if p: self.port= p
        if i: self.sid= i
        if e: self.maxEpisodes= e
        if t: self.trackname= t
        if s: self.stage= s
        if d: self.debug= d
        self.S= ServerState()
        self.R= DriverAction()
        self.setup_connection()

    def setup_connection(self):
        # == Set Up UDP Socket ==
        try:
            self.so= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as emsg:
            print('Error: Could not create socket...')
            sys.exit(-1)
        # == Initialize Connection To Server ==
        self.so.settimeout(1)

        n_fail = 5
        while True:
            # This string establishes track sensor angles! You can customize them.
            #a= "-90 -75 -60 -45 -30 -20 -15 -10 -5 0 5 10 15 20 30 45 60 75 90"
            # exp35: wider outer beams for turn anticipation, tight inner cluster for braking
            a = "-90 -45 -20 -10 -7 -4 -2 -1 -.5 0 .5 1 2 4 7 10 20 45 90"


            initmsg='%s(init %s)' % (self.sid,a)

            try:
                self.so.sendto(initmsg.encode(), (self.host, self.port))
            except socket.error as emsg:
                sys.exit(-1)
            sockdata= str()
            try:
                sockdata,addr= self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.error as emsg:
                print("Waiting for server on %d............" % self.port)
                print("Count Down : " + str(n_fail))
                if n_fail < 0:
                    print("relaunch torcs")
                    os.system('pkill torcs')
                    time.sleep(1.0)
                    if self.vision is False:
                        os.system('torcs -nofuel -nodamage -nolaptime &')
                    else:
                        os.system('torcs -nofuel -nodamage -nolaptime -vision &')

                    time.sleep(1.0)
                    os.system('sh autostart.sh')
                    n_fail = 5
                n_fail -= 1

            identify = '***identified***'
            if identify in sockdata:
                print("Client connected on %d.............." % self.port)
                break

    def parse_the_command_line(self):
        try:
            (opts, args) = getopt.getopt(sys.argv[1:], 'H:p:i:m:e:t:s:dhv',
                       ['host=','port=','id=','steps=',
                        'episodes=','track=','stage=',
                        'debug','help','version'])
        except getopt.error as why:
            print('getopt error: %s\n%s' % (why, usage))
            sys.exit(-1)
        try:
            for opt in opts:
                if opt[0] == '-h' or opt[0] == '--help':
                    print(usage)
                    sys.exit(0)
                if opt[0] == '-d' or opt[0] == '--debug':
                    self.debug= True
                if opt[0] == '-H' or opt[0] == '--host':
                    self.host= opt[1]
                if opt[0] == '-i' or opt[0] == '--id':
                    self.sid= opt[1]
                if opt[0] == '-t' or opt[0] == '--track':
                    self.trackname= opt[1]
                if opt[0] == '-s' or opt[0] == '--stage':
                    self.stage= int(opt[1])
                ######### REQUIRED FOR RACE MODE - DO NOT CHANGE OR REMOVE #########
                if opt[0] == '-p' or opt[0] == '--port':
                    self.port= int(opt[1])
                ######## END OF REQUIRED #########
                if opt[0] == '-e' or opt[0] == '--episodes':
                    self.maxEpisodes= int(opt[1])
                if opt[0] == '-m' or opt[0] == '--steps':
                    self.maxSteps= int(opt[1])
                if opt[0] == '-v' or opt[0] == '--version':
                    print('%s %s' % (sys.argv[0], version))
                    sys.exit(0)
        except ValueError as why:
            print('Bad parameter \'%s\' for option %s: %s\n%s' % (
                                       opt[1], opt[0], why, usage))
            sys.exit(-1)
        if len(args) > 0:
            print('Superflous input? %s\n%s' % (', '.join(args), usage))
            sys.exit(-1)

    ######### REQUIRED FOR RACE MODE - DO NOT CHANGE OR REMOVE #########
    def get_servers_input(self):
        '''Server's input is stored in a ServerState object'''
        if not self.so: return
        sockdata= str()

        while True:
            try:
                # Receive server data
                sockdata,addr= self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.error as emsg:
                print('.', end=' ')
                #print "Waiting for data on %d.............." % self.port
            if '***identified***' in sockdata:
                print("Client connected on %d.............." % self.port)
                continue
            elif '***shutdown***' in sockdata:
                print((("Server has stopped the race on %d. "+
                        "You were in %d place.") %
                        (self.port,self.S.d['racePos'])))
                self.shutdown()
                return
            elif '***restart***' in sockdata:
                # What do I do here?
                print("Server has restarted the race on %d." % self.port)
                # I haven't actually caught the server doing this.
                self.shutdown()
                return
            elif not sockdata: # Empty?
                continue       # Try again.
            else:
                self.S.parse_server_str(sockdata)
                if self.debug:
                    sys.stderr.write("\x1b[2J\x1b[H") # Clear for steady output.
                    print(self.S)
                break # Can now return from this function.
    ########## END OF REQUIRED #########

    def respond_to_server(self):
        if not self.so: return
        try:
            message = repr(self.R)
            self.so.sendto(message.encode(), (self.host, self.port))
        except socket.error as emsg:
            print("Error sending to server: %s Message %s" % (emsg[1],str(emsg[0])))
            sys.exit(-1)
        if self.debug: print(self.R.fancyout())
        # Or use this for plain output:
        #if self.debug: print self.R

    def shutdown(self):
        if not self.so: return
        print(("Race terminated or %d steps elapsed. Shutting down %d."
               % (self.maxSteps,self.port)))
        self.so.close()
        self.so = None
        #sys.exit() # No need for this really.

class ServerState():
    '''What the server is reporting right now.'''
    def __init__(self):
        self.servstr= str()
        self.d= dict()

    def parse_server_str(self, server_string):
        '''Parse the server string.'''
        self.servstr= server_string.strip()[:-1]
        sslisted= self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w= i.split(' ')
            self.d[w[0]]= destringify(w[1:])

    def __repr__(self):
        # Comment the next line for raw output:
        return self.fancyout()
        # -------------------------------------
        out= str()
        for k in sorted(self.d):
            strout= str(self.d[k])
            if type(self.d[k]) is list:
                strlist= [str(i) for i in self.d[k]]
                strout= ', '.join(strlist)
            out+= "%s: %s\n" % (k,strout)
        return out

    def fancyout(self):
        '''Specialty output for useful ServerState monitoring.'''
        out= str()
        sensors= [ # Select the ones you want in the order you want them.
        #'curLapTime',
        #'lastLapTime',
        'stucktimer',
        #'damage',
        #'focus',
        'fuel',
        #'gear',
        'distRaced',
        'distFromStart',
        #'racePos',
        'opponents',
        'wheelSpinVel',
        'z',
        'speedZ',
        'speedY',
        'speedX',
        'targetSpeed',
        'rpm',
        'skid',
        'slip',
        'track',
        'trackPos',
        'angle',
        ]

        #for k in sorted(self.d): # Use this to get all sensors.
        for k in sensors:
            if type(self.d.get(k)) is list: # Handle list type data.
                if k == 'track': # Nice display for track sensors.
                    strout= str()
                 #  for tsensor in self.d['track']:
                 #      if   tsensor >180: oc= '|'
                 #      elif tsensor > 80: oc= ';'
                 #      elif tsensor > 60: oc= ','
                 #      elif tsensor > 39: oc= '.'
                 #      #elif tsensor > 13: oc= chr(int(tsensor)+65-13)
                 #      elif tsensor > 13: oc= chr(int(tsensor)+97-13)
                 #      elif tsensor >  3: oc= chr(int(tsensor)+48-3)
                 #      else: oc= '_'
                 #      strout+= oc
                 #  strout= ' -> '+strout[:9] +' ' + strout[9] + ' ' + strout[10:]+' <-'
                    raw_tsens= ['%.1f'%x for x in self.d['track']]
                    strout+= ' '.join(raw_tsens[:9])+'_'+raw_tsens[9]+'_'+' '.join(raw_tsens[10:])
                elif k == 'opponents': # Nice display for opponent sensors.
                    strout= str()
                    for osensor in self.d['opponents']:
                        if   osensor >190: oc= '_'
                        elif osensor > 90: oc= '.'
                        elif osensor > 39: oc= chr(int(osensor/2)+97-19)
                        elif osensor > 13: oc= chr(int(osensor)+65-13)
                        elif osensor >  3: oc= chr(int(osensor)+48-3)
                        else: oc= '?'
                        strout+= oc
                    strout= ' -> '+strout[:18] + ' ' + strout[18:]+' <-'
                else:
                    strlist= [str(i) for i in self.d[k]]
                    strout= ', '.join(strlist)
            else: # Not a list type of value.
                if k == 'gear': # This is redundant now since it's part of RPM.
                    gs= '_._._._._._._._._'
                    p= int(self.d['gear']) * 2 + 2  # Position
                    l= '%d'%self.d['gear'] # Label
                    if l=='-1': l= 'R'
                    if l=='0':  l= 'N'
                    strout= gs[:p]+ '(%s)'%l + gs[p+3:]
                elif k == 'damage':
                    strout= '%6.0f %s' % (self.d[k], bargraph(self.d[k],0,10000,50,'~'))
                elif k == 'fuel':
                    strout= '%6.0f %s' % (self.d[k], bargraph(self.d[k],0,100,50,'f'))
                elif k == 'speedX':
                    cx= 'X'
                    if self.d[k]<0: cx= 'R'
                    strout= '%6.1f %s' % (self.d[k], bargraph(self.d[k],-30,300,50,cx))
                elif k == 'speedY': # This gets reversed for display to make sense.
                    strout= '%6.1f %s' % (self.d[k], bargraph(self.d[k]*-1,-25,25,50,'Y'))
                elif k == 'speedZ':
                    strout= '%6.1f %s' % (self.d[k], bargraph(self.d[k],-13,13,50,'Z'))
                elif k == 'z':
                    strout= '%6.3f %s' % (self.d[k], bargraph(self.d[k],.3,.5,50,'z'))
                elif k == 'trackPos': # This gets reversed for display to make sense.
                    cx='<'
                    if self.d[k]<0: cx= '>'
                    strout= '%6.3f %s' % (self.d[k], bargraph(self.d[k]*-1,-1,1,50,cx))
                elif k == 'stucktimer':
                    if self.d[k]:
                        strout= '%3d %s' % (self.d[k], bargraph(self.d[k],0,300,50,"'"))
                    else: strout= 'Not stuck!'
                elif k == 'rpm':
                    g= self.d['gear']
                    if g < 0:
                        g= 'R'
                    else:
                        g= '%1d'% g
                    strout= bargraph(self.d[k],0,10000,50,g)
                elif k == 'angle':
                    asyms= [
                          "  !  ", ".|'  ", "./'  ", "_.-  ", ".--  ", "..-  ",
                          "---  ", ".__  ", "-._  ", "'-.  ", "'\.  ", "'|.  ",
                          "  |  ", "  .|'", "  ./'", "  .-'", "  _.-", "  __.",
                          "  ---", "  --.", "  -._", "  -..", "  '\.", "  '|."  ]
                    rad= self.d[k]
                    deg= int(rad*180/PI)
                    symno= int(.5+ (rad+PI) / (PI/12) )
                    symno= symno % (len(asyms)-1)
                    strout= '%5.2f %3d (%s)' % (rad,deg,asyms[symno])
                elif k == 'skid': # A sensible interpretation of wheel spin.
                    frontwheelradpersec= self.d['wheelSpinVel'][0]
                    skid= 0
                    if frontwheelradpersec:
                        skid= .5555555555*self.d['speedX']/frontwheelradpersec - .66124
                    strout= bargraph(skid,-.05,.4,50,'*')
                elif k == 'slip': # A sensible interpretation of wheel spin.
                    frontwheelradpersec= self.d['wheelSpinVel'][0]
                    slip= 0
                    if frontwheelradpersec:
                        slip= ((self.d['wheelSpinVel'][2]+self.d['wheelSpinVel'][3]) -
                              (self.d['wheelSpinVel'][0]+self.d['wheelSpinVel'][1]))
                    strout= bargraph(slip,-5,150,50,'@')
                else:
                    strout= str(self.d[k])
            out+= "%s: %s\n" % (k,strout)
        return out

class DriverAction():
    '''What the driver is intending to do (i.e. send to the server).
    Composes something like this for the server:
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus 0)(meta 0) or
    (accel 1)(brake 0)(gear 1)(steer 0)(clutch 0)(focus -90 -45 0 45 90)(meta 0)'''
    def __init__(self):
       self.actionstr= str()
       # "d" is for data dictionary.
       self.d= { 'accel':0.2,
                   'brake':0,
                  'clutch':0,
                    'gear':1,
                   'steer':0,
                   'focus':[-90,-45,0,45,90],
                    'meta':0
                    }

    def clip_to_limits(self):
        """There pretty much is never a reason to send the server
        something like (steer 9483.323). This comes up all the time
        and it's probably just more sensible to always clip it than to
        worry about when to. The "clip" command is still a snakeoil
        utility function, but it should be used only for non standard
        things or non obvious limits (limit the steering to the left,
        for example). For normal limits, simply don't worry about it."""
        self.d['steer']= clip(self.d['steer'], -1, 1)
        self.d['brake']= clip(self.d['brake'], 0, 1)
        self.d['accel']= clip(self.d['accel'], 0, 1)
        self.d['clutch']= clip(self.d['clutch'], 0, 1)
        if self.d['gear'] not in [-1, 0, 1, 2, 3, 4, 5, 6]:
            self.d['gear']= 0
        if self.d['meta'] not in [0,1]:
            self.d['meta']= 0
        if type(self.d['focus']) is not list or min(self.d['focus'])<-180 or max(self.d['focus'])>180:
            self.d['focus']= 0

    def __repr__(self):
        self.clip_to_limits()
        out= str()
        for k in self.d:
            out+= '('+k+' '
            v= self.d[k]
            if not type(v) is list:
                out+= '%.3f' % v
            else:
                out+= ' '.join([str(x) for x in v])
            out+= ')'
        return out
        return out+'\n'

    def fancyout(self):
        '''Specialty output for useful monitoring of bot's effectors.'''
        out= str()
        od= self.d.copy()
        od.pop('gear','') # Not interesting.
        od.pop('meta','') # Not interesting.
        od.pop('focus','') # Not interesting. Yet.
        for k in sorted(od):
            if k == 'clutch' or k == 'brake' or k == 'accel':
                strout=''
                strout= '%6.3f %s' % (od[k], bargraph(od[k],0,1,50,k[0].upper()))
            elif k == 'steer': # Reverse the graph to make sense.
                strout= '%6.3f %s' % (od[k], bargraph(od[k]*-1,-1,1,50,'S'))
            else:
                strout= str(od[k])
            out+= "%s: %s\n" % (k,strout)
        return out

# == Misc Utility Functions
def destringify(s):
    '''makes a string into a value or a list of strings into a list of
    values (if possible)'''
    if not s: return s
    if type(s) is str:
        try:
            return float(s)
        except ValueError:
            print("Could not find a value in %s" % s)
            return s
    elif type(s) is list:
        if len(s) < 2:
            return destringify(s[0])
        else:
            return [destringify(i) for i in s]

# ============================================================
# exp39: Fix steering -- root cause of crash at T4 (1105m)
# Changes vs exp38:
#   TELEMETRY DIAGNOSIS (exp38 lap_data):
#   - At T4 apex exit (~1100m), trackPos = 1.3 (right wall), angle rises to 4-10 rad
#     because car hit the right tirewall and spun. Off-track confirmed.
#   - steer = angle * 10/PI: with angle=5, steer=15.9 -> clipped to 1, useless.
#   - trackPos correction (trackPos - target_tp) * 0.12 = (1.3 - (-0.4)) * 0.12 = 0.204
#     This is tiny relative to the angle term and cannot reposition the car.
#   ROOT CAUSE: angle gain 10/PI is 3x too large; correction gain 0.12 is 5x too small.
#   FIXES:
#   A) Angle gain 10/PI -> 3.5/PI: heading correction without saturating steer range
#   B) Proportional trackPos correction: gain scales with error magnitude
#      small error (< 0.3): gain 0.10 (gentle nudge)
#      medium error (0.3-0.8): gain 0.20 (active repositioning)
#      large error (> 0.8): gain 0.35 (emergency lane change)
#   C) Wall avoidance: if |trackPos| > 0.85 push hard away from wall regardless
#   D) turn_bias reduced 0.05->0.03: was adding noise to steer on straights
#
# Segment distance reference (cumulative from map JSON):
#   s1:32  s2:152(184)  s3/T1:38(222)  s4:119(341)  s5:65(406)
#   s6-s8/T2:139(545)   s9:48(593)
#   s10-s12/T3:197(790→828 tighter) approx ends 828
#   s13:110(938)  s14:78(1016)  s15/T4:89(1105)
#   s16-s18:215(1320)  s19:186(1506)  s20-s21/T5:142(1648)
#   s22:192(1840)  s23/Rahal:112(1952)  s24/T6:32(1984)
#   s25-s34 Corkscrew approach:472(2456)
#   s35-s37/T8:70(2540)  s38-s41 descent:161(2701)
#   s42/T9:124(2825)  s43-s44:158(2984? approx)  [T10 ~2984]
#   s45/T10:79(3063)  s46-s47 S/F:228(3291)
#   s48/T11:40(3331)  s49:91(3422)  [S/F lap wrap ~3600]
# ============================================================
# Beam index map:
#   idx:  0     1     2     3    4    5   6   7    8    9   10  11  12  13  14  15   16   17   18
#   deg: -90  -45   -20   -10   -7   -4  -2  -1  -.5   0  .5   1   2   4   7   10   20   45   90

def drive_example(c):
    '''This is only an example. It will get around the track but the
    correct thing to do is write your own `drive()` function.'''
    S, R = c.S.d, c.R.d

    dist = S['distFromStart']
    spd  = S['speedX']
    trk  = S['track']   # 19-beam array

    # ------------------------------------------------------------------ #
    # C. ZONE-BASED TARGET SPEED                                          #
    # Grounded in corkscrew_map.json speed_targets_kmh + guide.           #
    # Distances from cumulative segment arc-lengths (corkscrew_map.json). #
    # ------------------------------------------------------------------ #
    if   184  <= dist <  222:  target_speed = 110  # T1 approach braking (s3 entry)
    elif 222  <= dist <  341:  target_speed =  93  # T1 apex s3 → post-T1 s4 (r=86.5m)
    elif 341  <= dist <  406:  target_speed =  80  # T2 braking zone (s5, -2.7% downhill)
    elif 406  <= dist <  545:  target_speed =  50  # T2 Andretti Hairpin s6-s8 (r=24m, -4° banking)
    elif 545  <= dist <  717:  target_speed = 140  # s9 + T3 opening sweep (s10, R=105-422m, fast curve)
    elif 717  <= dist <  828:  target_speed =  90  # T3 tighter s12-1,s12-2 (r=44m, guide: 90 apex)
    elif 828  <= dist <  938:  target_speed = 200  # s13 exit straight: full throttle
    elif 938  <= dist < 1016:  target_speed = 110  # s14 braking zone for T4 (guide: brake ~70m before)
    elif 1016 <= dist < 1105:  target_speed =  80  # T4 apex s15-1,s15-2 (r=48-77m, guide: 80)
    elif 1105 <= dist < 1413:  target_speed = 200  # s16-s18 post-T4 + s19-1 long straight
    elif 1413 <= dist < 1506:  target_speed =  85  # s19-2 T5 braking approach (guide: entry 85 km/h)
    elif 1506 <= dist < 1648:  target_speed =  72  # T5 apex s20-s21 (r=48-72m, -5° banking, guide: 75)
    elif 1648 <= dist < 1920:  target_speed = 200  # s22 steep climb + Rahal Straight: full throttle
    elif 1920 <= dist < 1952:  target_speed =  85  # T6 entry braking (guide: ≤65 at apex, brake 30m out)
    elif 1952 <= dist < 1984:  target_speed =  62  # T6 apex s24 (r=33.6m, -6° banking, guide: 65)
    elif 1984 <= dist < 2403:  target_speed = 200  # s25-s33 post-T6 Corkscrew approach: mostly throttle
    elif 2403 <= dist < 2456:  target_speed =  65  # s34 T8 braking zone (guide: entry ≤55 at s35-1)
    elif 2456 <= dist < 2506:  target_speed =  40  # T8 LH s35-1,s35-2 (r=11.5m, guide: LH apex 40)
    elif 2506 <= dist < 2540:  target_speed =  36  # s36 transition + T8A s37 (r=14.4m, guide: ~35)
    elif 2540 <= dist < 2701:  target_speed =  90  # s38-s41 post-Corkscrew descent (accelerate progressively)
    elif 2701 <= dist < 2762:  target_speed =  90  # T9 Rainey entry s42-1 (guide: entry 90-95 km/h)
    elif 2762 <= dist < 2825:  target_speed =  80  # T9 Rainey apex s42-2 (r=72-78m, guide: apex 80)
    elif 2825 <= dist < 2984:  target_speed = 200  # s43-s44 post-Rainey straights: full throttle
    elif 2984 <= dist < 3063:  target_speed =  80  # T10 s45 (r=53-58m, +6° banking, guide: 80)
    elif 3063 <= dist < 3265:  target_speed = 200  # s46 S/F straight: full throttle
    elif 3265 <= dist < 3291:  target_speed =  75  # s47 T11 braking zone (guide: brake 100m before T11)
    elif 3291 <= dist < 3331:  target_speed =  50  # T11 apex s48-1,s48-2 (r=18m, guide: 50)
    else:                      target_speed = 200  # s49 S/F exit + all other straights: full throttle

    # ------------------------------------------------------------------ #
    # D. RACING LINE: dynamic target_trackPos                             #
    # Grounded in corkscrew_guide.md racing line table + external CSV.   #
    # TORCS: trackPos +1=right wall, -1=left wall, 0=center.             #
    # Right-hander: entry from LEFT (-), apex RIGHT (+).                 #
    # Left-hander:  entry from RIGHT (+), apex LEFT (-).                 #
    # ------------------------------------------------------------------ #
    if   0    <= dist <  184:  target_tp =  0.0   # S/F straight + s1: center
    elif 184  <= dist <  222:  target_tp =  0.6   # T1 approach: right side (left-turn entry)
    elif 222  <= dist <  282:  target_tp = -0.6   # T1 apex: cut left
    elif 282  <= dist <  406:  target_tp =  0.6   # post-T1 + T2 braking: far right for hairpin entry
    elif 406  <= dist <  545:  target_tp = -0.7   # T2 hairpin: far left apex (double-left)
    elif 545  <= dist <  593:  target_tp =  0.5   # s9 post-hairpin: set up right for T3 entry
    elif 593  <= dist <  717:  target_tp = -0.7   # T3 entry s10: FAR LEFT (RIGHT-HANDER entry side)
    elif 717  <= dist <  828:  target_tp =  0.7   # T3 apex s12: FAR RIGHT curb (RIGHT-HANDER apex)
    elif 828  <= dist <  938:  target_tp = -0.4   # s13 exit straight: drift left, set for T4 entry
    elif 938  <= dist < 1016:  target_tp = -0.6   # s14 T4 braking: far LEFT (RIGHT-HANDER entry)
    elif 1016 <= dist < 1105:  target_tp =  0.6   # T4 apex s15: FAR RIGHT curb (RIGHT-HANDER apex)
    elif 1105 <= dist < 1413:  target_tp =  0.0   # s16-s19-1 post-T4 straights: center
    elif 1413 <= dist < 1506:  target_tp =  0.5   # s19-2 T5 approach: right side (left-turn entry)
    elif 1506 <= dist < 1648:  target_tp = -0.6   # T5 apex s20-s21: cut left
    elif 1648 <= dist < 1840:  target_tp = -0.3   # s22 steep climb: center-left (free up track width)
    elif 1840 <= dist < 1920:  target_tp =  0.0   # Rahal Straight: center (accelerating)
    elif 1920 <= dist < 1952:  target_tp =  0.5   # T6 entry: right side (left-turn entry)
    elif 1952 <= dist < 1984:  target_tp = -0.6   # T6 apex s24: cut left curb
    elif 1984 <= dist < 2403:  target_tp = -0.3   # s25-s33 Corkscrew approach: center-left (CSV: -0.3)
    elif 2403 <= dist < 2456:  target_tp =  0.7   # s34 T8 entry: FAR RIGHT (guide: CRITICAL far right)
    elif 2456 <= dist < 2506:  target_tp = -0.6   # T8 LH s35: left apex curb
    elif 2506 <= dist < 2520:  target_tp =  0.0   # s36 transition: through center
    elif 2520 <= dist < 2540:  target_tp =  0.4   # T8A RH s37: right apex
    elif 2540 <= dist < 2701:  target_tp =  0.2   # s38-s41 post-Corkscrew: slight right for T9 entry
    elif 2701 <= dist < 2762:  target_tp =  0.5   # T9 entry s42-1: right side (left-turn entry)
    elif 2762 <= dist < 2825:  target_tp = -0.5   # T9 apex s42-2: left curb
    elif 2825 <= dist < 2984:  target_tp =  0.0   # s43-s44 post-Rainey: center
    elif 2984 <= dist < 3024:  target_tp = -0.5   # T10 entry s45-1: left side (right-turn entry)
    elif 3024 <= dist < 3063:  target_tp =  0.5   # T10 apex s45-2: right curb
    elif 3063 <= dist < 3265:  target_tp =  0.0   # s46 S/F straight: center
    elif 3265 <= dist < 3291:  target_tp =  0.6   # s47 T11 approach: far right (left-turn entry)
    elif 3291 <= dist < 3331:  target_tp = -0.6   # T11 apex s48: left curb (double-left)
    else:                      target_tp = -0.4   # s49 S/F exit: left-center (CSV: -0.4 to -0.8)

    # ------------------------------------------------------------------ #
    # E. STEER: angle-based + proportional racing line correction         #
    # Telemetry showed angle*10/PI saturates steer when angle>0.3 rad,   #
    # leaving no room for the trackPos correction to work.                #
    # Fix: reduce angle gain to 3.5/PI; scale trackPos correction by     #
    # error magnitude so large misalignments get strong correction.       #
    # ------------------------------------------------------------------ #
    side_L = trk[4]   # -7 deg beam
    side_R = trk[14]  # +7 deg beam
    asym   = (side_R - side_L) / max(side_L + side_R, 1.0)
    turn_bias = asym * 0.03   # reduced from 0.05 -- less noise on straights

    R['steer'] = S['angle'] * 3.5 / PI + turn_bias

    # Proportional racing line correction:
    # gain scales with how far the car is from the target line
    tp_err = S['trackPos'] - target_tp
    tp_abs = abs(tp_err)
    if tp_abs < 0.3:
        tp_gain = 0.10
    elif tp_abs < 0.8:
        tp_gain = 0.20
    else:
        tp_gain = 0.35
    R['steer'] -= tp_err * tp_gain

    # Wall avoidance: if too close to either wall, override with emergency steer
    if S['trackPos'] > 0.85:
        R['steer'] = min(R['steer'], -0.5 * (S['trackPos'] - 0.85) / 0.15)
    elif S['trackPos'] < -0.85:
        R['steer'] = max(R['steer'],  0.5 * (-0.85 - S['trackPos']) / 0.15)

    # ------------------------------------------------------------------ #
    # B. BRAKE: two layers                                                #
    # 1) Sensor-based reactive brake: obstacle/wall detected ahead.      #
    #    Uses 5-beam minimum (idx 7-11) to catch imminent wall contact.  #
    # 2) Zone-based overspeed brake: car is above target_speed+10.       #
    #    This is the primary zone-entry braking mechanism -- sensor brake #
    #    alone cannot stop the car from 200 km/h into a 50 km/h corner.  #
    # Trail factor 0.8: at steer=0.5 brake*0.6; at steer=0 full.        #
    # ------------------------------------------------------------------ #
    _fwd = min(trk[7:12])   # indices 7-11: +/-1 deg, +/-0.5 deg, 0 deg
    if _fwd < 150 and spd > 80:
        base_brake = clip((150 - _fwd) / 150 * (spd / 160) ** 2, 0, 1)
        trail_factor = clip(1.0 - abs(R['steer']) * 0.8, 0.0, 1.0)
        R['brake'] = base_brake * trail_factor
    else:
        R['brake'] = 0.0

    # Zone-based overspeed braking -- fills the gap when sensors show clear
    # but target speed is well below current speed (corner entry from straight)
    if spd > target_speed + 10:
        overspeed_brake = clip((spd - target_speed) / 80.0, 0.0, 1.0)
        if overspeed_brake > R['brake']:
            R['brake'] = overspeed_brake

    # ------------------------------------------------------------------ #
    # THROTTLE CONTROL -- faster ramp + immediate full-gas far below     #
    # Note: steer*50 penalty REMOVED -- it was suppressing acceleration  #
    # on every non-straight segment, causing perpetually slow laps.      #
    # ------------------------------------------------------------------ #
    speed_error = target_speed - spd
    if speed_error > 20:
        # Well below target -- open throttle fast
        R['accel'] = min(R['accel'] + 0.10, 1.0)
    elif speed_error > 0:
        R['accel'] += 0.05
    else:
        R['accel'] -= 0.05
    R['accel'] = clip(R['accel'], 0.0, 1.0)

    # Low-speed kick -- capped to prevent erratic overshoot
    if spd < 10:
        R['accel'] = min(R['accel'] + 0.5, 1.0)

    # TCS -- gated to acceleration (brake < 0.05) and meaningful speed (>20 km/h)
    # to prevent starving throttle during slow-speed recovery from corners
    if (R['brake'] < 0.05 and spd > 20 and
       (S['wheelSpinVel'][2] + S['wheelSpinVel'][3]) -
       (S['wheelSpinVel'][0] + S['wheelSpinVel'][1]) > 5):
        R['accel'] -= 0.2

    # ------------------------------------------------------------------ #
    # AUTOMATIC TRANSMISSION (unchanged thresholds -- proven safe)       #
    # ------------------------------------------------------------------ #
    R['gear'] = 1
    if spd > 50:   R['gear'] = 2
    if spd > 80:   R['gear'] = 3
    if spd > 110:  R['gear'] = 4
    if spd > 140:  R['gear'] = 5
    if spd > 170:  R['gear'] = 6
    return

# ================ MAIN ================
if __name__ == "__main__":
    # ------------------------------------------------------------------ #
    #  TELEMETRY CONFIGURATION -- edit only this block                    #
    #  Changing these values does NOT affect driving behaviour.           #
    # ------------------------------------------------------------------ #
    EXPERIMENT_ID      = "exp39_fix_steering_gain"  # label for this experiment run
    LAP_WRAP_THRESHOLD = 500.0          # metres: distFromStart below this = crossed start/finish
                                        # raised from 400 m (Telemetry Fix 3): at 250 km/h the car
                                        # travels ~69 m/step; 500 m gives a comfortable 7-step
                                        # window.  Must stay below LAP_MIN_DIST_PREV.
    LAP_MIN_DIST_PREV  = 1000.0         # metres: distFromStart must exceed this before crossing
                                        # raised from 500 m alongside LAP_WRAP_THRESHOLD to
                                        # maintain the 500 m separation guard on a 3 600 m track.
    # ------------------------------------------------------------------ #

    # ---- one-time run identity (computed before the Client connects) ---
    RUN_ID     = str(uuid.uuid4())
    EPISODE_ID = str(uuid.uuid4())
    _script_path = os.path.abspath(__file__)
    with open(_script_path, "rb") as _f:
        CODE_SHA256 = hashlib.sha256(_f.read()).hexdigest()
    _run_start_monotonic = time.monotonic()

    # ---- CSV column definitions ----------------------------------------
    LAP_DATA_COLS = [
        "run_id", "episode_id", "lap_id", "step",
        "utc_timestamp", "elapsed_time_s",
        "experiment_id", "code_sha256", "track_id", "lap_status",
        "distFromStart", "distRaced", "curLapTime", "lastLapTime",
        "speedX", "trackPos", "angle",
        "steer", "accel", "brake", "gear",
        "forward_track", "min_valid_track", "damage",
    ]
    LAP_SUMMARY_COLS = [
        "run_id", "episode_id", "lap_id",
        "experiment_id", "code_sha256",
        "status", "sim_lap_time_s",
        "damage_initial", "damage_final",
        "max_speed_kmh", "completion_reason",
    ]

    # ---- helper: open or validate a CSV file (cumulative append) -------
    def _open_csv(path, cols):
        """
        Open *path* for append.  Write header only when the file is new or
        empty.  If an existing header is incompatible, print a clear message
        and exit -- the file is never modified in that case.
        Returns (file_handle, csv.writer).
        """
        is_new = not os.path.exists(path) or os.path.getsize(path) == 0
        fh = open(path, "a", newline="", encoding="utf-8")
        writer = csv.writer(fh)
        if is_new:
            writer.writerow(cols)
            fh.flush()
        else:
            with open(path, "r", newline="", encoding="utf-8") as _chk:
                existing_header = next(csv.reader(_chk), None)
            if existing_header != list(cols):
                fh.close()
                print(
                    "FATAL: Existing header in %s is incompatible.\n"
                    "  Expected : %s\n"
                    "  Found    : %s\n"
                    "Rename or remove the file to start fresh. "
                    "Existing data is preserved." % (path, cols, existing_header)
                )
                sys.exit(1)
        return fh, writer

    # ---- helper: create a fresh CSV file for this run (write, not append)
    def _open_csv_new(path, cols):
        """
        Always create *path* as a brand-new file for this execution.
        Any previous file with the same name is overwritten.
        Returns (file_handle, csv.writer).
        """
        fh = open(path, "w", newline="", encoding="utf-8")
        writer = csv.writer(fh)
        writer.writerow(cols)
        fh.flush()
        return fh, writer

    # ---- resolve CSV paths --------------------------------------------
    _script_dir      = os.path.dirname(os.path.abspath(__file__))
    # lap_data: one fresh file per run, inside the "telemetry" sub-folder,
    # named <EXPERIMENT_ID>_lap_data.csv  (e.g. exp35_braking_zones_fixed_lap_data.csv)
    _telemetry_dir   = os.path.join(_script_dir, "telemetry")
    os.makedirs(_telemetry_dir, exist_ok=True)
    LAP_DATA_PATH    = os.path.join(_telemetry_dir, "%s_lap_data.csv" % EXPERIMENT_ID)
    # lap_summary: cumulative append beside this script (unchanged)
    LAP_SUMMARY_PATH = os.path.join(_script_dir, "lap_summary.csv")

    lap_data_fh    = None
    lap_summary_fh = None

    # ---- lap tracking state (initialised before the loop) -------------
    lap_id               = 0        # 0 = warmup; increments at each finish-line crossing
    lap_status           = "warmup" # warmup | flying | partial
    prev_dist_from_start = None
    lap_start_damage     = None
    lap_max_speed        = 0.0
    completed_lap_ids    = set()    # prevents duplicate summary rows
    _completion_reason   = "unknown"
    S                    = {}       # sentinel so finally block is safe before loop starts

    #### DO NOT HARCODE THE PORT
    C= Client()
    try:
        lap_data_fh,    lap_data_writer    = _open_csv_new(LAP_DATA_PATH, LAP_DATA_COLS)
        lap_summary_fh, lap_summary_writer = _open_csv(LAP_SUMMARY_PATH, LAP_SUMMARY_COLS)

        for step in range(C.maxSteps,0,-1):
            C.get_servers_input()
            if not C.so:                    # Server ended the race.
                _completion_reason = "race_completed"
                break
            drive_example(C)
            # Controls are now fully computed by drive_example().
            # Logging happens here, BEFORE respond_to_server(), so we
            # capture the controls that will actually be sent this step.
            # Nothing below this comment reads from or writes to C.R.d,
            # so driving behaviour is completely unaffected.
            #
            # NOTE: all CSV flush() calls are placed AFTER respond_to_server()
            # so that no I/O can delay the UDP reply to TORCS.  The writes
            # themselves (writerow) are pure userspace buffer appends and are
            # effectively free.

            S = C.S.d   # sensor snapshot for this step
            R = C.R.d   # control snapshot for this step (read-only from here)

            # ---- read sensor values; never invent missing ones --------
            dist_from_start = S.get("distFromStart")
            dist_raced      = S.get("distRaced")
            cur_lap_time    = S.get("curLapTime")
            last_lap_time   = S.get("lastLapTime")
            speed_x         = S.get("speedX")
            track_pos       = S.get("trackPos")
            angle           = S.get("angle")
            damage          = S.get("damage")
            track_sensors   = S.get("track")    # list[float] of 19 range beams

            # ---- forward and minimum valid track distances ------------
            # Init string: "-90 -45 -20 -10 -7 -4 -2 -1 -.5 0 .5 1 2 4 7 10 20 45 90"
            # Index 9 (0-based) is the 0-degree (dead-ahead) beam.
            # Exclude negative, zero, and non-finite values; they indicate
            # a beam that missed the track boundaries.
            forward_track   = ""
            min_valid_track = ""
            if isinstance(track_sensors, list) and len(track_sensors) > 9:
                _fwd = track_sensors[9]
                if isinstance(_fwd, float) and math.isfinite(_fwd) and _fwd > 0:
                    forward_track = _fwd
                _valid = [v for v in track_sensors
                          if isinstance(v, float) and math.isfinite(v) and v > 0]
                if _valid:
                    min_valid_track = min(_valid)

            # ---- finish-line crossing detection -----------------------
            # A genuine crossing: distFromStart drops from a large value
            # (car was near end of track) to a small value (car is now
            # near start of track), while moving forward.
            #
            # Detection limits:
            #   1. Tracks shorter than LAP_MIN_DIST_PREV require tuning.
            #   2. A high-speed backward bounce across the start line can
            #      false-trigger even with the speed_x >= 0 guard (e.g. a
            #      crash that sends the car flying in reverse over the line).
            #   3. ***restart*** terminates the loop before this runs, so
            #      no false crossing is generated on an episode reset.
            crossed_finish = False
            if (prev_dist_from_start is not None
                    and dist_from_start is not None
                    and prev_dist_from_start > LAP_MIN_DIST_PREV
                    and dist_from_start < LAP_WRAP_THRESHOLD
                    and isinstance(speed_x, float) and speed_x >= 0.0):
                crossed_finish = True

            _flush_summary = False      # set True when a lap-summary row is written
            _advance_lap   = False      # set True when finish line was cleanly crossed
            if crossed_finish:
                # last_lap_time is reliable here: the simulator updates it
                # on the same step that distFromStart wraps.
                # Guard against duplicate rows (e.g. two consecutive steps
                # that both satisfy the wrap condition on a very slow car).
                if lap_id not in completed_lap_ids:
                    completed_lap_ids.add(lap_id)
                    _sim_time = (
                        last_lap_time
                        if isinstance(last_lap_time, float) and last_lap_time > 0
                        else ""
                    )
                    lap_summary_writer.writerow([
                        RUN_ID, EPISODE_ID, lap_id,
                        EXPERIMENT_ID, CODE_SHA256,
                        "completed" if lap_status == "flying" else "warmup_completed",
                        _sim_time,
                        lap_start_damage if lap_start_damage is not None else "",
                        damage if isinstance(damage, float) else "",
                        "%.3f" % lap_max_speed,
                        "finish_line_crossing",
                    ])
                    _flush_summary = True   # flush deferred until after respond_to_server()
                    _advance_lap   = True   # counters updated AFTER the data row is written

            # ---- update per-lap maximum speed -------------------------
            if isinstance(speed_x, float) and speed_x > lap_max_speed:
                lap_max_speed = speed_x

            # ---- advance lap counters (deferred until after summary row written) -
            # Doing this here -- after the lap_summary row but before the lap_data
            # row -- means the crossing step is still recorded under the lap that
            # just finished (lap_id has not changed yet), and the new counter
            # takes effect from the very next step.
            if _advance_lap:
                lap_id           += 1
                lap_status        = "flying"
                lap_start_damage  = damage if isinstance(damage, float) else None
                lap_max_speed     = 0.0

            # ---- write one row to lap_data.csv (non-blocking) ---------
            _now_utc   = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            _elapsed_s = time.monotonic() - _run_start_monotonic
            # step counts down from maxSteps; convert to a forward step number
            _step_num  = C.maxSteps - step + 1

            lap_data_writer.writerow([
                RUN_ID,
                EPISODE_ID,
                lap_id,
                _step_num,
                _now_utc,
                "%.6f" % _elapsed_s,
                EXPERIMENT_ID,
                CODE_SHA256,
                C.trackname,                                        # from --track flag
                lap_status,
                dist_from_start  if dist_from_start  is not None else "",
                dist_raced       if dist_raced        is not None else "",
                cur_lap_time     if cur_lap_time      is not None else "",
                last_lap_time    if last_lap_time     is not None else "",
                speed_x          if speed_x           is not None else "",
                track_pos        if track_pos         is not None else "",
                angle            if angle             is not None else "",
                R.get("steer",  ""),
                R.get("accel",  ""),
                R.get("brake",  ""),
                R.get("gear",   ""),
                forward_track,
                min_valid_track,
                damage           if damage            is not None else "",
            ])
            prev_dist_from_start = dist_from_start

            # ---- send controls to the simulator -----------------------
            # respond_to_server() is the last substantive operation so
            # that no I/O can delay the UDP reply to TORCS.
            C.respond_to_server()

            # ---- flush CSV buffers to the OS (after reply is sent) ----
            # flush() pushes Python's userspace buffer to the kernel page
            # cache -- it is NOT fsync, so it completes in microseconds.
            # Placing it here (after the reply) ensures the UDP packet is
            # already on the wire before any OS call is made.
            lap_data_fh.flush()
            if _flush_summary:
                lap_summary_fh.flush()

        # Loop ended without a break -- all maxSteps exhausted.
        if _completion_reason == "unknown":
            _completion_reason = "maxsteps_or_shutdown"

    except KeyboardInterrupt:
        _completion_reason = "keyboard_interrupt"
        print("\nCtrl+C received. Writing partial lap summary and closing logs.")

    except Exception as _exc:
        _completion_reason = "exception"
        print("Telemetry error: %s -- closing logs, re-raising." % _exc)
        raise

    finally:
        # Always reached on normal exit, Ctrl+C, or any exception.
        # NOT reached on SIGKILL -- that is unavoidable; already-flushed
        # step rows are safe in the kernel write-back cache.
        try:
            if lap_summary_fh is not None:
                if lap_id not in completed_lap_ids:
                    # Record the in-progress lap that never crossed the line.
                    _final_damage = S.get("damage", "") if isinstance(S, dict) else ""
                    lap_summary_writer.writerow([
                        RUN_ID, EPISODE_ID, lap_id,
                        EXPERIMENT_ID, CODE_SHA256,
                        "partial",
                        "",    # sim_lap_time_s unavailable for an incomplete lap
                        lap_start_damage if lap_start_damage is not None else "",
                        _final_damage,
                        "%.3f" % lap_max_speed,
                        _completion_reason,
                    ])
                    lap_summary_fh.flush()
        except Exception as _fe:
            print("Warning: could not write final summary row: %s" % _fe)
        finally:
            if lap_data_fh    is not None: lap_data_fh.close()
            if lap_summary_fh is not None: lap_summary_fh.close()

    C.shutdown()

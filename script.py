import psp2d
import pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import sys
import stackless
import os
import threading
import urlparse

pspos.setclocks(333, 166)

print "Localtime: ", localtime()
print "Datetime: ", datetime.datetime.now()

screen = psp2d.Screen()
screen.clear(psp2d.Color(0, 0, 0, 255))

font = psp2d.Font('font.png')

apctl_states = ["PSP_NET_APCTL_STATE_DISCONNECTED","PSP_NET_APCTL_STATE_SCANNING","PSP_NET_APCTL_STATE_JOINING","PSP_NET_APCTL_STATE_GETTING_IP","PSP_NET_APCTL_STATE_GOT_IP","PSP_NET_APCTL_STATE_EAP_AUTH","PSP_NET_APCTL_STATE_KEY_EXCHANGE","PSP_NET_APCTL_EVENT_CONNECT_REQUEST","PSP_NET_APCTL_EVENT_SCAN_REQUEST","PSP_NET_APCTL_EVENT_SCAN_COMPLETE","PSP_NET_APCTL_EVENT_ESTABLISHED","PSP_NET_APCTL_EVENT_GET_IP","PSP_NET_APCTL_EVENT_DISCONNECT_REQUEST","PSP_NET_APCTL_EVENT_ERROR","PSP_NET_APCTL_EVENT_INFO","PSP_NET_APCTL_EVENT_EAP_AUTH","PSP_NET_APCTL_EVENT_KEY_EXCHANGE","PSP_NET_APCTL_EVENT_RECONNECT","PSP_NET_APCTL_INFO_PROFILE_NAME","PSP_NET_APCTL_INFO_BSSID","PSP_NET_APCTL_INFO_SSID","PSP_NET_APCTL_INFO_SSID_LENGTH","PSP_NET_APCTL_INFO_SECURITY_TYPE","PSP_NET_APCTL_INFO_STRENGTH","PSP_NET_APCTL_INFO_CHANNEL","PSP_NET_APCTL_INFO_POWER_SAVE","PSP_NET_APCTL_INFO_IP","PSP_NET_APCTL_INFO_SUBNETMASK","PSP_NET_APCTL_INFO_GATEWAY","PSP_NET_APCTL_INFO_PRIMDNS","PSP_NET_APCTL_INFO_SECDNS","PSP_NET_APCTL_INFO_USE_PROXY","PSP_NET_APCTL_INFO_PROXY_URL","PSP_NET_APCTL_INFO_PROXY_PORT","PSP_NET_APCTL_INFO_8021_EAP_TYPE","PSP_NET_APCTL_INFO_START_BROWSER","PSP_NET_APCTL_INFO_WIFISP","PSP_NET_APCTL_INFO_SECURITY_TYPE_NONE","PSP_NET_APCTL_INFO_SECURITY_TYPE_WEP","PSP_NET_APCTL_INFO_SECURITY_TYPE_WPA"]

class Agent(object):
    def __init__(self):
        self.ch = stackless.channel()
        self.running = True
        stackless.tasklet(self.runAction)()

    def runAction(self):
        while self.running:
            self.action()
            stackless.schedule()

    def action(self):
        pass


class controller(Agent):
    def __init__(self, eng):
        Agent.__init__(self)
        self.lastPad = time()
        self.eng = eng
        self.eng.entities.append(self)

    def action(self):
        pad = psp2d.Controller()
        if pad.cross:
            print "exit"
            self.rend.exit()


class engine(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.entities = []
        self.wlanStarted = False

    def exit(self):
        print "Stopping entities..."
        for agent in self.entities:
            print "Stopped agent %s" % agent
            agent.running = False
        self.running = False
        print "Stopped self..."

    def action(self):
        screen.clear(psp2d.Color(0, 0, 0, 255))

        state = "WLAN switch OFF"
        ip = "Unavailable"

        if pspnet.wlanSwitchState():
            state = apctl_states[pspnet.getAPCTLState()]
            try:
                ip = pspnet.getIP()
            except:
                pass

            if pspnet.getAPCTLState() == 0:
                apConnectThread = threading.Thread(target = pspnet.connectToAPCTL, args=(1,))
                apConnectThread.daemon = True
                apConnectThread.start()

        font.drawText(screen, 10, 10, "State: %s" % state)
        font.drawText(screen, 10, 25, "IP: %s" % ip)
        font.drawText(screen, 10, 45, "Press X to exit")

        for agent in self.entities:
            if hasattr(agent, 'sprite'):
                screen.blit(agent.sprite, 0, 0, agent.sprite.width,
                            agent.sprite.height, agent.posX, agent.posY, True)

        screen.swap()


if __name__ == '__main__':
    eng = engine()
    ctrl = controller(eng)
    stackless.run()

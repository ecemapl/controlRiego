import sys
import time
import random
import datetime
import telepot
import socket
import urllib2
from telepot.loop import MessageLoop
from subprocess import call
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT) ## GPIO 14 para la valvula 1
GPIO.setup(15, GPIO.OUT) ## GPIO 15 para la valvula 2
GPIO.setup(18, GPIO.OUT) ## GPIO 18 para la valvula 3

estado = 'Sistema encendido'

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    global estado

#    print 'Got command: %s' % command
    
    if command == 'Toma foto':
        call(["fswebcam", "-q", "/home/pi/image.jpg"])
        f = open('/home/pi/image.jpg', 'rb')
        bot.sendPhoto(chat_id, f)
    elif command == 'Enciende':
        GPIO.output(14, False)
        GPIO.output(15, False)
        GPIO.output(18, False)
        estado = 'Sistema encendido'
        #	print 'Sistema encendido'
        bot.sendMessage(chat_id, estado)
    elif command == 'Apaga':
        GPIO.output(14, True)
        GPIO.output(15, True)
        GPIO.output(18, True)
        estado = 'Sistema apagado'
        #	print 'Sistema apagado'
        bot.sendMessage(chat_id, estado)
    elif command == 'Estado':
        bot.sendMessage(chat_id, str(estado))
    elif command == "Actualiza Programa":
        call(["cd", "/home/pi/controlRiego"])
        call(["git", "pull", "--rebase"])
        bot.sendMessage(chat_id, command)
        time.sleep(5)
        call(["sudo", "reboot", "now"])

def IsInternetUp():
	testConn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		testConn.connect(('http://www.google.com', 80))
		testConn.close()
		print "we are online"
		return True
	except:
		testConn.close()
		print "we are NOT online"
		return False

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

estado = 'Sistema encendido'
GPIO.output(14, False)
GPIO.output(15, False)
GPIO.output(18, False)

while (internet_on == False):
	time.sleep(10)

bot = telepot.Bot('399706449:AAEeu-ix49OS3dDMTNzxfYPpPKHCQN_SbLM')
bot.deleteWebhook()

MessageLoop(bot, handle).run_as_thread()
#print 'I am listening ...'

while 1:
    time.sleep(10)

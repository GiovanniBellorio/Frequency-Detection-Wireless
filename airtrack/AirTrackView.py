#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from tkinter import Tk, RIGHT, LEFT, TOP, BOTH, RAISED, scrolledtext, StringVar
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Frame, Button, Style, Label, OptionMenu
import subprocess
import time
import signal
import os
import psutil
import AirTrack
from time import sleep

counter = 0

class AirTrackView(Frame):

	def __init__(self):
		super().__init__()

		self.INTERFACES = []
		self.iface = StringVar(self)
		self.scrollbarLog = None
		self.sniffer = None

		self.setup()
		self.initUI()


	def setup(self):
		# get interfaces lits
		self.INTERFACES = psutil.net_if_addrs()


	def updateScrolltext(self, txt):
		# http://effbot.org/tkinterbook/text.htm  <-- qui spiega xk bisogna usare questa funzione!
		print("updateScrolltext called..." + txt)
		self.scrollbarLog.config(state = NORMAL)
		self.scrollbarLog.insert(END, txt)
		self.scrollbarLog.see("end")
		self.scrollbarLog.config(state = DISABLED)

	def initUI(self):

		def stop():
			#os.killpg(os.getpgid(self.pid), signal.SIGINT)
			print("[*] Stop sniffing")
			self.sniffer.join(2.0)

			if self.sniffer.isAlive():
				self.sniffer.socket.close()

			# update database with the new records
			AirTrack.update_db()


		def start():
			self.sniffer = AirTrack.Sniffer('-i '+self.iface.get())
			self.sniffer.start()
			#AirTrack.start_session('-i '+self.iface.get())
			self.updateScrolltext("Inizio rilevazione:\n")
			# def count():
			# 	global counter
			# 	counter += 1 #sostituire counter con una stringa che venga aggiornata con l'output del terminale in questa riga
			# 	self.updateScrolltext(str(counter) + "\n")
			# 	self.after(1000, count)
			# count()

		self.master.title("AirTrack")
		#self.style = Style()
		#self.style.theme_use("default")

		top_label = Label(self, text = "Welcome to AirTrack:")
		top_label.pack(side = TOP, padx = 5, pady = 5, anchor = 'w')

		scrollbarLogFrame = Frame(self, relief = RAISED, borderwidth = 1)
		scrollbarLogFrame.pack(fill = BOTH, expand = True)

		self.pack(fill = BOTH, expand = True)

		self.scrollbarLog = scrolledtext.ScrolledText(scrollbarLogFrame, background = "black", foreground = "green")#, state=DISABLED)
		self.scrollbarLog.pack(fill = BOTH, expand = True, padx = 5, pady = 5)

		startButton = Button(self, text = "Start", command = start) #inserire command
		startButton.pack(side = RIGHT, padx = 5, pady = 5)
		stopButton = Button(self, text = "Stop", command = stop) #inserire command
		stopButton.pack(side = RIGHT)

		interface_label = Label(self, text = "Interface:")
		interface_label.pack(side = LEFT, padx = 5, pady = 5)

		interfaces_list = OptionMenu(self, self.iface, next(iter(self.INTERFACES)), *self.INTERFACES)
		interfaces_list.pack(side = LEFT)

		self.updateScrolltext("Select network interface and press Start.\n")



def main():

	# database connection
	# TODO qui ci va la schermata di login nel caso della GUI,
	# altrimnti vengono chieste in input solo usrname e passw.


	# TODO: il parser andrebbe messo qua!

	if len(sys.argv) > 1:
		print("gui mode off")
		AirTrack.connect_to_db()

		sniffer = AirTrack.Sniffer(sys.argv[1] + " " + sys.argv[2])
		sniffer.start()
		try:
			while True:
				sleep(100)
		except KeyboardInterrupt:
			print("[*] Stop sniffing")
			sniffer.join(2.0)

			if sniffer.isAlive():
				sniffer.socket.close()

		# update database with the new records
		AirTrack.update_db()

	else:
		AirTrack.connect_to_db()
		print("gui mode on")
		root = Tk()
		root.geometry("800x500")
		app = AirTrackView()
		root.mainloop()


if __name__ == '__main__':
	main()
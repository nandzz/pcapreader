                        #Quote of the day#
 #“Wine is constant proof that God loves us and loves to see us happy.”#
#------------------------------------------------------------------------# 

from pcap import * 
from pretty_formatter import *
import pdb 
import binascii
import sys, time
import os

little = 'd4c3b2a1'
big = 'a1b2c3d4'

isLittle = False

def readPCAP(filename):
         with open(filename + ".pcap", 'r+b') as pcap:
            pcap.seek(0,0)
            #Solve the Magic Number
            isLittle  = True if pcap.read(4).hex() == little else False
            #Offset the header [we are not using this data in this exercise]
            pcap.seek(24,0) 
            #Get frames from the pcap File
            listOfFrames = getFrames(pcap, isLittle)
            for index, dic in enumerate(listOfFrames):
                #Take the frame data from
                frame = dic['data']
                
                #----------------------------------Header-------------------------------------------#
                
                #The below values correspond to an ethernet header [14 bytes]
                
                #rBytes = Range of Bytes

                #Destination Mac Address Range in Frame [0-6 -> rBytes]
                destMacRange = frame[:6]
                #Source Mac Address Range in Frame [6-12 -> rBytes]
                sourceMacRange = frame[6:12]
                #Ethernet Type Range in Frame [12-14 -> rBytes]
                ethernetTypeRange = frame[12:14]
               
                #Get Ethernet Value  
                ethernetType    = extractType(ethernetTypeRange)
                #Get Mac Values
                destMac         = extractMac(destMacRange)
                sourceMac       = extractMac(sourceMacRange)
                 
                #------------------------------------Protocol----------------------------------------#

                #Source Ip Range in Frame for TYPE [EthernetTypeRange] 

                # Type == "0x0806" is ARP Protocol  |  Dest Range in Frame -> [38:42] | Source Range in Frame -> [28:32] 
                # Type == "0x0800" is IPV4 Protocol |  Dest Range in Frame -> [30:34] | Source Range in Frame -> [26:30]
                #Get the Range from IP
                destIpRange   = frame[38:42] if ethernetType == '0x0806' else frame[30:34]
                sourceIpRange = frame[28:32] if ethernetType == '0x0806' else frame[26:30]
               
                ipSourceAddress = extractIP(sourceIpRange)
                ipDestAddress   = extractIP(destIpRange)
                
                #Extract Protocol in case of Layer 4
                protocol =  extractProtocol(frame[23:24]) if ethernetType == '0x0800' else None
                layer_two   = {'destMac': destMac, 'sourceMac': sourceMac, 'ethernetType': ethernetType }
                layer_three = {'destIp': ipDestAddress, 'sourceIp': ipSourceAddress }
                layer_four  = {'protocol': protocol}
                debug = ""
                debug += "Saved Packet Lenght: [bold magenta] {} [/bold magenta]\n".format(dic['lenght'])
                debug += "Actual Packet Lenght:[bold magenta] {} [/bold magenta]\n\n".format(dic['lenght'])        

                for i, x in enumerate(frame, start=1):
                    if i % 16 == 0:
                       debug += '\n' 
                    else:
                       debug += '{:02x} '.format(x)

                #Compose Table and Print
                createTable(layer_two, layer_three, layer_four, index, debug) 
                sys.stdin.readline()
            else:
                print("End of file")
                #TODO: GET ARRAY SIZE OF PCAP
                sys.exit() 

while True:
   i = input("Input file name or Q to Quit: ")
   if i == "Q":
       break
   else:
      readPCAP(i)




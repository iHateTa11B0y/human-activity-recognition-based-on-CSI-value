# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:39:11 2017

@author: n1187
"""
from byte2int import bytestoint

class bfee:
    
    #timestamp_low = 0
    
    
    def __init__(self,inBytes):
        self.timestamp_low = bytestoint(inBytes[0:4],4,1)
        self.bfee_count = bytestoint(inBytes[4:6],2,1)
        self.Nrx = bytestoint(inBytes[8:9],1,1)
        self.Ntx = bytestoint(inBytes[9:10],1,1)
        self.rssi_a = bytestoint(inBytes[10:11],1,1)
        self.rssi_b = bytestoint(inBytes[11:12],1,1)
        self.rssi_c = bytestoint(inBytes[12:13],1,1)
        self.noise = bytestoint(inBytes[13:14],-1,1)
        self.agc = bytestoint(inBytes[14:15],1,1)
        self.antenna_sel = bytestoint(inBytes[15:16],1,1)
        self.leng = bytestoint(inBytes[16:18],2,1)
        self.fake_rate_n_flags = bytestoint(inBytes[18:20],2,1)
        self.calc_len = int((30 * (self.Nrx * self.Ntx * 8 * 2 + 3) + 7) / 8)
        self.payload = inBytes[20:]
        self.csi = []
        self.perm = []
        
        index = 0
        self.ptrR = []
        self.ptrI = []
        csi = []
        
        #print(self.leng,self.calc_len)
        if (self.leng != self.calc_len):
            print ("Wrong beamforming matrix size.")
        
        
        #compute img and real part of csi and form csi
        for i in range(0,30) :
            index += 3
            remainder = index % 8
            tmpLR = []
            tmpLI = []
            tmpcsi = []
            for j in range(0,self.Nrx*self.Ntx):
                tmpr = (self.payload[int(index/8)] >> remainder) | (self.payload[int(index/8)+1] << (8-remainder)) & 0xFF
                tmpfr = float(tmpr)
                if(tmpfr>=128):
                    tmpfr = -256+tmpfr
                tmpLR.append(tmpfr)
                
                tmpi = (self.payload[int(index/8)+1] >> remainder) | (self.payload[int(index/8)+2] << (8-remainder)) & 0xFF
                tmpfi = float(tmpi)
                if(tmpfi>=128):
                    tmpfi = -256+tmpfi
                tmpLI.append(tmpfi)
                
                tmpcsi.append(0)
                
                #tmpcsi.append(tmpfr+tmpfi*1j)               #complex(tmpfr,tmpfi)        
                index += 16
            for k in range(0,self.Nrx*self.Ntx):
                tmpcsi[k] = (complex(tmpLR[k],tmpLI[k]))
                
            csi.append(tmpcsi)

            self.ptrR.append(tmpLR)
            self.ptrI.append(tmpLI)
        
        self.csi = csi
        
        #compute the permutation array
        self.perm = [((self.antenna_sel) & 0x3) + 1,((self.antenna_sel >> 2) & 0x3) + 1,((self.antenna_sel >> 4) & 0x3) + 1]

    def printCSI(self):
        print("timestamp:",self.timestamp_low,"\n")
        print("bfee_count:",self.bfee_count,"\n")
        print("Nrx:",self.Nrx,"\n")
        print("Ntx:",self.Ntx,"\n")
        print("rssi_a:",self.rssi_a,"\n")
        print("rssi_b:",self.rssi_b,"\n")
        print("rssi_c:",self.rssi_c,"\n")
        print("noise:",self.noise,"\n")
        print("agc",self.agc,"\n")
        print("perm:",self.perm,"\n")
        print("rate:",self.fake_rate_n_flags,"\n")
        print("csi:\n",self.csi,"\n")
        print("csiIMG:\n",self.ptrI,"\n")
        print("csiRE:\n",self.ptrR,"\n")
        
    def returnCSI(self):
        return self.csi
    
    def returnNrx(self):
        return self.Nrx
    
    def returnNtx(self):
        return self.Ntx
    
    def returnTime(self):
        return self.timestamp_low
    
    
        
        
        
        
            
            
    
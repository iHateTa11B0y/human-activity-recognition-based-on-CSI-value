# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 00:32:30 2017

@author: n1187
"""

def bytestoint(src,numOfbytes,endian_flag):
    if (endian_flag):
        value = (src[0] & 0xFF)
        for i in range(1,abs(numOfbytes)):
            value = value | (src[i] & 0xFF)<<(8*i)
        #value = int(value)
        
        if(numOfbytes<0):
            tmp = int(value)
            if(tmp>2**(8*abs(numOfbytes)-1)):
                value = -2**(8*abs(numOfbytes))+tmp
            else:
                value = tmp
        else:
            value = int(value)
    else:
        value = (src[len(src)-1] & 0xFF)
        for i in range(1,abs(numOfbytes)):
            value = value | (src[len(src)-1-i] & 0xFF)<<(8*i)
        #value = int(value)
        
        if(numOfbytes<0):
            tmp = int(value)
            if(tmp>2**(8*abs(numOfbytes)-1)):
                value = -2**(8*abs(numOfbytes))+tmp
            else:
                value = tmp
        else:
            value = int(value)
            
    return value

#v = bytestoint(b'\xd5',1)
#print(v)
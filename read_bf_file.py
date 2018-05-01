# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import bfee
from byte2int import bytestoint

def read_bf_file(filename):
    f = open(filename,"rb")
    fstr = f.read()
    #print (fstr)
    leng = f.tell()

    #Initializing variables 
    ret = []
    cur = 0
    count = 0
    broken_perm = 0
    triangle = [1,3,6]
    
    f.seek(0,0)
    print(leng,"&&&")
    #process all the entries in the file
    while cur < (leng - 3):
        # read size and code (2 byte size and 1 byte code)
        field_len = bytestoint(f.read(2),2,0)
        #print(field_len)
        code = bytestoint(f.read(1),1,1)
        #print(code)
        cur = cur + 3

        # If unhandled code, skip (seek over) the record and continue
        if (code == 187):
            Bytes = f.read(field_len-1)
            #print(len(Bytes))
            cur = cur + field_len - 1
            if (len(Bytes) != field_len-1):
                break
        else: #skip all other info
            f.seek(field_len-1,os.SEEK_CUR)
            cur = cur + field_len - 1
            continue

        if (code == 187 and len(Bytes) == field_len-1): #hex2dec('bb')) Beamforming matrix -- output a record
            count = count + 1
            #print("count:",count)
            #print(len(Bytes))
            #print("---------")
            tmp = bfee.bfee(Bytes)
                    
            Perm = tmp.perm
            Nrx_ = tmp.Nrx
            if(Nrx_==1):
                continue
            
            if sum(Perm) != triangle[Nrx_-1]:
                if(broken_perm==0):
                    broken_perm = 1
                    print('WARN ONCE: Found CSI (%s) with Nrx=%d and invalid perm=[%s]\n', filename, Nrx_, str(Perm))
                    
            else:
                row = len(tmp.csi)
                
                for i in range(0,row):
                    tmpRow = [[0],[0],[0]]
                    for j in range(0,Nrx_):
                        tmpRow[Perm[j]-1] = tmp.csi[i][j] #  havent deal with the csiIMAG and csiRE
                    tmp.csi[i] = tmpRow
            
            tmp.printCSI()
            ret.append(tmp)
    f.close()
    
    #print csi 
    
    num_obj = len(ret)
    #print(num_obj,"@@@")
    
    re_csi = []
    re_timestamp = []
    for cn in range(0,num_obj):
        tmpObj = ret[cn]
        #tmpObj.printCSI()
        #re_nrx.append(tmpObj.returnNrx())
        #re_ntx.append(tmpObj.returnNtx())
        re_csi.append(tmpObj.returnCSI())
        re_timestamp.append(tmpObj.returnTime())
    re_nrx = tmpObj.returnNrx()
    re_ntx = tmpObj.returnNtx()  
    return re_nrx, re_ntx, re_csi, re_timestamp




    
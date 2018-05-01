# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 00:57:51 2017

@author: n1187
"""

import read_bf_file as rb
import math
import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy import signal

def featureExtraction(filen):

    nrx,ntx,csi_raw,timestamp_raw=rb.read_bf_file(filen)
    time_index_num = len(timestamp_raw)
    csi_raw_m = []#np.mat(csi_raw)
    
    print("time_index_num:",time_index_num)
    #print("timestamp_raw: ",timestamp_raw)
    
    """
    PCA denoise
    """
    #Step1: Processing. sbustract the static offset
    sumcsi = np.zeros((30,nrx*ntx))
    for i in range(0,math.floor(time_index_num/10)):
        csi_tmp = np.mat(csi_raw[i])
        sumcsi = sumcsi + csi_tmp
        #csi_raw_m.append(csi_tmp)
        #p_tmp = np.abs(csi_tmp)
    csi_static_offset = sumcsi/math.floor(time_index_num/2)
    
    csi_tmp = np.mat(csi_raw[0]) - csi_static_offset
    csi_raw_m.append(csi_tmp)
    H_raw = np.reshape(csi_tmp,(1,30*nrx*ntx))
    
    for i in range(1,time_index_num):
        csi_tmp = np.mat(csi_raw[i]) - csi_static_offset
        csi_raw_m.append(csi_tmp)
        tmpLinem = np.reshape(csi_tmp,(1,30*nrx*ntx))
        H_raw=np.vstack((H_raw,tmpLinem))
        
    print(np.size(H_raw,0))
    print(np.size(H_raw,1))
    # median filter
    power = np.abs(H_raw)
    for i in range(0,30*nrx*ntx):
        tmpm = power[:,i].T
        tmpl = tmpm.tolist()
        tmpf = signal.medfilt(tmpl[0],3)
        power[:,i] = np.mat(tmpf).T
    
    # compute pca denoised signal in each chunk
    num_in_chunk = 50
    cnt = 0
    tmpchunk = np.zeros((1,np.size(H_raw,1)))
    H = np.zeros((1,5))
    PCs = tmpchunk
    for i in range(1,time_index_num):
        if(cnt<num_in_chunk):
            cnt = cnt + 1
            tmpchunk = np.vstack((tmpchunk,H_raw[i,:]))
        else:
            tmpchunk = tmpchunk[1:,:]
            Corr_mat = tmpchunk.T*tmpchunk
            U,sigma,VT = np.linalg.svd(Corr_mat)
            #VT = VT.T
            vt =VT[1]
            vt = vt.T
            pca_chunk = tmpchunk*vt
            for i in range(2,6):
                vt =VT[i]
                vt = vt.T
                pca_chunk = np.hstack((pca_chunk,tmpchunk*vt))
            print("pca_0:",np.size(pca_chunk,0))
            print("pca_1:",np.size(pca_chunk,1))
            H = np.vstack((H,pca_chunk))
            tmpchunk = np.zeros((1,np.size(H_raw,1)))
            cnt = 0
    H = H[1:,:] #H is the 
    print("H_0:", np.size(H,0))
    print("H_1:", np.size(H,1))     
        
    
    
    """
    Feature Extraction
    """
    f_raw = np.reshape(H,-1)
    lv = 7
    db1 = pywt.Wavelet('db1')
    coeffs =  pywt.wavedec(f_raw, db1, level=lv)
    cD = [0]*lv
    cA, cD[0],cD[1],cD[2],cD[3],cD[4],cD[5],cD[6] = coeffs
    #print(coeffs)
    #print("------------")
    #print(cA)
    #print(np.size(cA,0))
    #print(np.size(cA,1))
    #print("------------")
    #print(cD[0])
    #print(np.size(cD[0],0))
    #print(np.size(cD[0],1))
    #print("------------")
    #print(cD[1])
    #print(np.size(cD[1],0))
    #print(np.size(cD[1],1))
    
    energy = [0]*lv
    for i in range(0,lv):
        #energy[i] = np.sum(np.multiply(cD[i],cD[i]))
        energy[i] = np.sum(np.abs(cD[i]))
    
    diff_energy = [0]*lv
    for i in range(1,lv):
        diff_energy[i] = energy[i] - energy[i-1]
    
    total_energy = np.sum(energy)
    ensum = 0;
    
    for i in range(lv):
        
        if(ensum<0.05*total_energy and ensum+energy[i]>=0.05*total_energy):
            x1 = i
        if(ensum<0.5*total_energy and ensum+energy[i]>=0.5*total_energy):
            x2 = i
        if(ensum<0.95*total_energy and ensum+energy[i]>=0.95*total_energy):
            x3 = i
        ensum += energy[i]
    
    s1 = 7.7/300*240*0.5**(lv-x1)
    s2 = 7.7/300*240*0.5**(lv-x2)
    s3 = 7.7/300*240*0.5**(lv-x3)
    
    f = np.hstack((energy,diff_energy,x1,x2,x3))
    
    return f

def main():
    filename = "bai_20170905_eat01_dir1.dat"
    f = featureExtraction(filename)
    print(f)
if __name__ == "__main__":
    main()
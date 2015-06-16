import numpy as np

# read in CSV file containing data
wageningenbscrewdata=np.genfromtxt('wageningenbscrewdata.csv', delimiter=',')

bar=0.8
Z=4

Kt=np.zeros((1,36))
index=0
JDesign=1
Jsf=1
print(Jsf)

PoverD=np.zeros((1,36))
PoverD[index]=0.05*(index+1)
print(PoverD[index])

# PoverD is the PROBLEM

fix is to change np.zeros((1,61)) to np.zeros(61) etc...

CHECK MATLAB PROGRAM TO SEE IF I NEED TO DIMENSIONS HERE

# Kt[index]=np.sum((bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))

#Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*((Jsf*JDesign)**wageningenbscrewdata[0:38,1])*(PoverD[index]**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))



#ARE YOU CALLING SINGLE VALUE IN ARRAY??
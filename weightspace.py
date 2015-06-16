# Author: Santiago Suarez (UCL) and John Calleya (UCL)
# Version: 1
# History:
# The lwt ( known as lwt_cb_calc_4 in Matlab) function was adapted from an existing 
# Matlab function by Lucy Aldous
 
# Description:
# This file contains the lightweight models based in the work of Kristensen, 2012
# Determination of Regression Formulas for Main Dimensions of Tankers and Bulk Carriers based on IHS Fairplay data

def lightweight(Lwl, ship_type, dwt, vol_lad, B, T_des, Cb, rho):
    #calculate the ships LWT from dwt or teu (container) or vol_lad (lng carriers) 
    #vol_lad = laden capacity of cargo carried 
    #Lpp = Length between perpendiculars
    #Cb always Cb @ waterline
    # rho is density in tonnes per m3

    # calculate equivalent TEUs for container ship (assuming 14 tonnes per TEU)
    # this may underestimate capacity.
    
    teu = (dwt/14.0)
    
    Lpp = 0.97*Lwl
    
    if ship_type == "bulk": # bulk carrier 1
        
        if dwt < 10000:
            lwt = Lpp*B*T_des*0.831*dwt**-0.2
        elif dwt < 25000:
            lwt = Lpp*B*T_des*1.05*(0.153-1.58e-6*dwt)
        elif dwt < 55000:
            lwt = Lpp*B*T_des*1.05*(0.151-1.27e-6*dwt)
        elif dwt < 85000:
            lwt = Lpp*B*T_des*1.05*0.079
        elif dwt < 200000:
            lwt = Lpp*B*T_des*(0.0817-4.86e-8*dwt)
        else:
            lwt = Lpp*B*T_des*1.05*(0.076-2.61e-8*dwt)
    
    elif ship_type == "chemicals": # chemical tanker
        
        lwt = 0.31*dwt
    
    elif ship_type == "containers": #container
        
        if teu < 2900:
            lwt = Lpp*B*T_des*0.659*teu**-0.23
        elif teu < 4000:                       # Check this is panamx??
            lwt = Lpp*B*T_des*0.105
        else:
            lwt = Lpp*B*T_des*(max(0.09,0.104-1.15e-6*teu))
    
    elif ship_type == "general cargo": #General cargo
                
        lwt = (Cb*Lwl*B*T_des*rho) - dwt
        
    elif ship_type == "liquid natural gas": # lng tanker
            
        lwt = 6265.82 + (0.165979 * vol_lad);
    
    elif ship_type == "oil":    #oil tankers
            
        if dwt < 10000:
            lwt = Lpp*B*T_des*(0.2096 - 7.23e-6*dwt)
        elif dwt < 25000:
            lwt = Lpp*B*T_des*(0.1584 - 1.45e-6*dwt)
        elif dwt < 55000:
            lwt = Lpp*B*T_des*1.05*(0.1765-1.75e-6*dwt)
        elif dwt < 75000:
            lwt = Lpp*B*T_des*1.05*(0.0924-8.4e-8*dwt)
        elif dwt < 120000:
            lwt = Lpp*B*T_des*1.05*(0.0859-2.35e-8*dwt)
        elif dwt < 170000:
            lwt = Lpp*B*T_des*1.05*(0.1296-3.08e-7*dwt)
        else:
            lwt = Lpp*B*T_des*1.05*(0.0772- (dwt - 170000)*1.574e-7)
            
    else: # other liquids tanker / refrigerated cargo / Ro-ro / Vehicle
        #b_thresh = 0.33
        #T_def_rat = 0.5 # default shouldn't be needed
    
        lwt = (Cb*Lwl*B*T_des*rho) - dwt;
    
    return lwt
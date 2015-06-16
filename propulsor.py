# Author: John Calleya (UCL)
# Version: 1
# History:
# The Wageningen b-screw function was adapted from an existing Matlab function

# Description:
# This file contains propeller model

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

def wagbpropandgearbox(water_density, Design, CPP, pod_correction, DesignSpeed, OperationSpeed, ShipThrust, nDesign, nOperation, nPropDesign, Twin, w, D, bar, Z):
    # function to find the propeller efficiency by setting the design condition
    # to have the best P/D and calculating the off-design characteristics of
    # the propeller
    # methodology from:
    # Further computer-analyzed data of the wageningen b-screw series
    # M.W.C. Oosterveld and P.Van Oossanen
    # International Shipbuilding Progress
    # Volume 22, July 1975
    
    # assumptions
    # A factor is added when picking propeller curve to ensure operating
    # point is on the left of the curve and away from the steep drop on the
    # right.
    # The propeller fitting does also not distinguish between retrofits and
    # assumes that a new propeller is added after a retrofit.
    # Controllable Pitch Propeller (CPP) is treated the same as treating the
    # propeller in the design condition (Design==1 for CPP always and Design==1
    # for FPP only during the sizing/design condition process).
    
    # description of parameters
    # water_density
    # Design - whether propeller is being used for design condition
    # CPP - whether a CPP (1) or FPP (0) is being used
    # pod_correction - whether a pod(1) is being used or not (0)
    # DesignSpeed - Ship design speed in knots
    # OperationSpeed - Ship operational speed in knots
    # ShipThrust - thrust required by propeller to overcome resistance in steady-state (minus other devices)
    # PropDesign - denotes where the pitch can be varied for better efficiency
    # nPropDesign - Design value for propeller speed (this is zero when engine is directly coupled to propeller)
    # w - wake fraction (calculated from resistance model, can change with speed)
    # D - propeller diameter
    # bar - blade area ratio (calculated from resistance model)
    # Z - Number of Propeller Blades
    # nDesign - Design Engine Speed (rpm, converted to rev/s when used)
    # nProp - Design Propeller Speed (rpm, converted to rev/s when used)
    # nOperation - Operational Engine Speed (rpm, converted to rev/s when used)
    # PropTorque - Propeller Torque
    # effO - Propeller Open Water Efficiency
    # EngTorque - Engine Torque
    # PropThrust - Propeller Thrust
    # PoverD - Pitch to Diameter ratio
    # nProp - Calculated Propeller Design Speed
    
    # check inputs are valid
    if (bar==0):
        # very likely that inputs have been calculated incorrectly, this is
        # likely due to resistance model looking at too low speeds, that are
        # outside the range of the model, populate EngTorque and effO as 0 and
        # exit function
        # Model may also purposely pick lower design speeds during iteration
        # and this will also cut down computational effort
        effO=0
        EngTorque=0
        PropThrust=0
        PoverD=0
        nProp=0
        return effO, EngTorque, PropThrust, PoverD, nProp
    # check for design condition or CPP
    # PropDesign==1 for design of FPP (selecting optimum PoverD) or design and
    # operation of CPP
    if (CPP==1):
        # CPP selected from user input in main program
        PropDesign=1
        # change propeller pitch to match new operational speed each time
        OperationSpeed=DesignSpeed
    else:
        # FPP, PoverD is selected depending on whether design condition or not
        PropDesign=Design
    # read in CSV file containing data
    wageningenbscrewdata=np.genfromtxt('wageningenbscrewdata.csv', delimiter=',')
    
    # propeller RPM and Gear Ratio Assumptions
    # set safety factor for J to allow peak efficiency to be set by a slightly
    # higher or lower J value
    Jsf=1.25
    # Jsf normally means that the peak of the propeller curve is slightly to
    # the right of the point on the curve that is selected in order to avoid
    # the steer drop off to the right of the curve.  This number is at the
    # descretion of the designer.
    if (nPropDesign<=0):
        # propeller speed is matched to engine speed, no gearbox, gear ratio is
        # 1:1
        nProp=nDesign
        # ignore efficiency and use thrust as a input to determine PoverD, as
        # propeller diameter is set
        
        # find design condition open water efficiency curve    
        if (Design==1):
            VaDesign=(DesignSpeed*0.51444)*(1-w) # Va - Velocity at propeller (knots)
            # 1-w accounts for wake, difference in propeller speed from being
            # in open water and being behind the ship.
            JDesign=VaDesign/((nProp/60)*D) # Jdesign - Advance Coefficient for Design Condition
            # Preallocate arrays for PoverD search
            PoverD=np.zeros(36)
            Kt=np.zeros(36)
            Kq=np.zeros(36)
            effODesign=np.zeros(36)
            for index in range(36): # propeller pitch (propeller pitch up to 1.8 seems to be valid for a 4 bladed propeller, over this curves do not work, this is 1.6 for a 5 bladed propeller)
                PoverD[index]=0.05*(index+1) # from observed results it does not seem appropiate for propeller pitch to exceed 1.6 (as efficiency curve appears to change considerably), tried this using a bar of 0.2 and 0.8
                # format of wageningenbscrewdata:
                # ||                       Kt                       ||                       Kq                       ||
                # || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) ||
                # contains coefficients and terms of Kt and Kq polynomials for the wageningen b-screw series for a Rn of 2x10**6
                # (so that Kq,Kt=sum((Cs,t,u,v)*(J)**s*(P/D)))
                Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*((Jsf*JDesign)**wageningenbscrewdata[0:38,1])*(PoverD[index]**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))
                Kq[index]=np.sum(wageningenbscrewdata[0:46,5]*((Jsf*JDesign)**wageningenbscrewdata[0:46,6])*(PoverD[index]**wageningenbscrewdata[0:46,7])*(bar**wageningenbscrewdata[0:46,8])*(Z**wageningenbscrewdata[0:46,9]))
                # find thrust of selected PoverD propeller at ship design speed
                # (including design margin Jsf on J)
                PropThrust=Kt[index]*water_density*D**4*(nProp/60)**2
                # check thrust from resistance model against thrust from ship
                if PropThrust>=(ShipThrust/Twin):
                    # as PoverD is increased from smaller PoverD it normally
                    # also inceases thrust, when the predicted propeller thrust
                    # exceeds the required ship thrust, that PoverD ratio is
                    # selected
                    # calculate open water efficiency for selected PoverD:
                    effODesign[index]=(Jsf*JDesign/(2*np.pi))*(Kt[index]/Kq[index])
                    # ensure efficiency values are below 1, if this is not the
                    # case it is possible that the 'wrong part' of the
                    # efficiency curve is being used
                    if (effODesign[index]>=1.0):
                        # if equal to or above 1 replace efficiency value with
                        # 0, so it is not selected when finding the maximum
                        # value (and index is left unchanged)
                        effODesign[index]=0
                    elif (effODesign[index]<=0.0):
                        # if equal to or below 0 replace efficiency value with
                        # 0, so it is not selected when finding the minimum
                        # value (and index is left unchanged)
                        effODesign[index]=0
                    else:
                        # value is valid.
                        pass
                    # save PoverD index (no consideration of maximum efficiency
                    # here, only calulating the correct thrust)
                    effODesignindex=index
                    break
                elif (index==35):
                    # warning to user PoverD not found or maximum possible
                    # PoverD is being used
                    # WARNING: PoverD not found or is large, maximum value used!
                    # calculate open water efficiency for selected PoverD:
                    effODesign[index]=(Jsf*JDesign/(2*np.pi))*(Kt[index]/Kq[index])
                    # ensure efficiency values are below 1, if this is not the
                    # case it is possible that the 'wrong part' of the
                    # efficiency curve is being used
                    if (effODesign[index]>=1.0):
                        # if equal to or above 1 replace efficiency value with
                        # 0, so it is not selected when finding the maximum
                        # value (and index is left unchanged)
                        effODesign[index]=0
                    elif (effODesign[index]<=0.0):
                        # if equal to or below 0 replace efficiency value with
                        # 0, so it is not selected when finding the minimum
                        # value (and index is left unchanged)
                        effODesign[index]=0
                    else:
                        # value is valid.
                        pass
                    # save PoverD index (no consideration of maximum efficiency
                    # here, only calulating the correct thrust
                    effODesignindex=index
                    break
                else:
                    # not met thrust requirement, try next PoverD value
                    pass
            # IN WORK DELETE AND SEE IF RESULT CHANGES
            # save the calculated propeller design speed
            np.savetxt('temporary/calculatedFPP_nProp.csv', [nProp], delimiter=',')
            # nProp is not actually required but this is needed to use append
            # command later on and allows 'calculatedFPPeffO' to be deleted.
            # IN WORK DELETE AND SEE IF RESULT CHANGES
        elif (PropDesign==1):
            # CPP but operating condition change PoverD to find the best
            # efficiency but do not change speed, set by nProp
            # IN WORK DELETE AND SEE IF RESULT CHANGES
            nProp = np.loadtxt('temporary/calculatedFPP_nProp.csv', delimiter=',')
            # IN WORK DELETE AND SEE IF RESULT CHANGES
            # propeller speed and engine speed in design condition are used to
            # determine gear ratio, so that operational design speed is given
            # by (nOperation*(nProp/nDesign))
            VaOperation=(OperationSpeed*0.51444)*(1-w) # Va - Velocity at propeller (knots)
            JOperation=VaOperation/((nProp/60)*D) # JOperation - Advance Coefficient for Operating Condition
            # preallocate arrays for PoverD search
            PoverD=np.zeros(36)
            Kt=np.zeros(36)
            Kq=np.zeros(36)
            effODesign=np.zeros(36)
            # for given J, vary PoverD to find best propeller efficiency.
            for index in range(36): # propeller pitch (propeller pitch up to 1.8 seems to be valid for a 4 bladed propeller, over this curves do not work, this is 1.6 for a 5 bladed propeller)
                PoverD[index]=0.05*(index+1) # from observed results it does not seem appropiate for propeller pitch to exceed 1.6 (as efficiency curve appears to change considerably), tried this using a bar of 0.2 and 0.8
                # format of wageningenbscrewdata:
                # ||                       Kt                       ||                       Kq                       ||
                # || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) ||
                # contains coefficients and terms of Kt and Kq polynomials for the wageningen b-screw series for a Rn of 2x10**6
                # (so that Kq,Kt=sum((Cs,t,u,v)*(J)**s*(P/D)))
                Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*(JOperation**wageningenbscrewdata[0:38,1])*(PoverD[index]**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))
                Kq[index]=np.sum(wageningenbscrewdata[0:46,5]*(JOperation**wageningenbscrewdata[0:46,6])*(PoverD[index]**wageningenbscrewdata[0:46,7])*(bar**wageningenbscrewdata[0:46,8])*(Z**wageningenbscrewdata[0:46,9]))
                # calculate open water efficiency for each PoverD:
                effODesign[index]=(JOperation/(2*np.pi))*(Kt[index]/Kq[index])
                # ensure efficiency values are below 1, if this is not the case
                # it is possible that the 'wrong part' of the efficiency curve
                # is being used.
                if (effODesign[index]>=1.0):
                    # if equal to or above 1 replace efficiency value with 0,
                    # so it is not selected when finding the maximum value (and
                    # index is left unchanged)
                    effODesign[index]=0
                elif (effODesign[index]<=0.0):
                    # if equal to or below 0 replace efficiency value with 0,
                    # so it is not selected when finding the minimum value (and
                    # index is left unchanged)
                    effODesign[index]=0
                else:
                    # value is valid.
                    pass
            # return the maximum effO value and its index PoverD (save over
            # array with single maximum efficiency value)
            [effODesign,effODesignindex]=max(effODesign)   
        else:
            # operational condition (non-CPP) do not need to find design PoverD
            # as can load previously saved efficiency curve
            # load the existing propeller design data (including stored data
            # from propeller curve calculation)
            # IN WORK UNSURE IF nProp is needed
            # nProp = np.loadtxt('temporary/calculatedFPP_nProp.csv', delimiter=',')
            # IN WORK UNSURE IF nProp is needed
            J = np.loadtxt('temporary/calculatedFPP_J.csv', delimiter=',')
            Kq = np.loadtxt('temporary/calculatedFPP_Kq.csv', delimiter=',')
            Kt = np.loadtxt('temporary/calculatedFPP_Kt.csv', delimiter=',')
            effOOperation = np.loadtxt('temporary/calculatedFPP_effOOperation.csv', delimiter=',')
            effODesign = np.loadtxt('temporary/calculatedFPP_effODesign.csv', delimiter=',')
            PoverD = np.loadtxt('temporary/calculatedFPP_PoverD.csv', delimiter=',')
    else:
        # propeller speed and engine speed in design condition are used to
        # determine gear ratio, so that operational design speed is given by
        # (nOperation*(nProp/nDesign))
        
        # input propeller design speed (nPropDesign) is used as a initial
        # guess, PoverD is adjusted for highest open water efficiency and
        # propeller speed is adjusted (with PoverD) to meet thrust requirement
        if (Design==1):
            VaDesign=(DesignSpeed*0.51444)*(1-w) # Va - Velocity at propeller (knots)
            # 1-w accounts for wake, difference in propeller speed from being in
            # open water and being behind the ship.
            PropThrust=0 # initial value
            nProp=nPropDesign # initial value
            while (PropThrust<1.00*(ShipThrust/Twin)) or (PropThrust>1.02*(ShipThrust/Twin)):
                JDesign=VaDesign/((nProp/60)*D) # Jdesign - Advance Coefficient for Design Condition
                # preallocate arrays for PoverD search
                PoverD=np.zeros(36)
                Kt=np.zeros(36)
                Kq=np.zeros(36)
                effODesign=np.zeros(36)
                # for given J, vary PoverD to find best propeller efficiency.
                for index in range(36): # propeller pitch (propeller pitch up to 1.8 seems to be valid for a 4 bladed propeller, over this curves do not work, this is 1.6 for a 5 bladed propeller)
                    PoverD[index]=0.05*(index+1) # from observed results it does not seem appropiate for propeller pitch to exceed 1.6 (as efficiency curve appears to change considerably), tried this using a bar of 0.2 and 0.8
                    # format of wageningenbscrewdata (stored in propellerdata.mat):
                    # ||                       Kt                       ||                       Kq                       ||
                    # || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) ||
                    # contains coefficients and terms of Kt and Kq polynomials for the wageningen b-screw series for a Rn of 2x10**6
                    # (so that Kq,Kt=sum((Cs,t,u,v)*(J)**s*(P/D)))
                    Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*((Jsf*JDesign)**wageningenbscrewdata[0:38,1])*(PoverD[index]**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))
                    Kq[index]=np.sum(wageningenbscrewdata[0:46,5]*((Jsf*JDesign)**wageningenbscrewdata[0:46,6])*(PoverD[index]**wageningenbscrewdata[0:46,7])*(bar**wageningenbscrewdata[0:46,8])*(Z**wageningenbscrewdata[0:46,9]))
                    # calculate open water efficiency for each PoverD:
                    effODesign[index]=(Jsf*JDesign/(2*np.pi))*(Kt[index]/Kq[index])
                    # ensure efficiency values are below 1, if this is not the
                    # case it is possible that the 'wrong part' of the
                    # efficiency curve is being used.
                    if (effODesign[index]>=1.0):
                        # if equal to or above 1 replace efficiency value with
                        # 0, so it is not selected when finding the maximum
                        # value (and index is left unchanged)
                        effODesign[index]=0
                    elif (effODesign[index]<=0.0):
                        # if equal to or below 0 replace efficiency value with
                        # 0, so it is not selected when finding the minimum
                        # value (and index is left unchanged)
                        effODesign[index]=0
                    else:
                        # value is valid.
                        pass
                # return the maximum effO value and its index PoverD (save over
                # array with single maximum efficiency value)
                [effODesign,effODesignindex]=max(effODesign)
                # find thrust of selected rpm and PoverD propeller at ship
                # design speed (including design margin Jsf on J)
                PropThrust=Kt[effODesignindex]*water_density*D**4*(nProp/60)**2
                # select next design propeller rpm (nProp to try)
                if (PropThrust<1.00*(ShipThrust/Twin)):
                    # need to increase thrust produced by propeller by
                    # increasing propeller design speed
                    nProp=nProp+0.5
                elif (PropThrust>1.02*(ShipThrust/Twin)):
                    # need to reduce thrust produced by propeller by lowering
                    # propeller design speed
                    nProp=nProp-0.5
            # save the calculated propeller design speed
            np.savetxt('temporary/calculatedFPP_nProp.csv', [nProp], delimiter=',')
        elif (PropDesign==1):
            # CPP but operating condition change PoverD to find the best
            # efficiency but do not change speed, set by nProp
            nProp = np.loadtxt('temporary/calculatedFPP_nProp.csv', delimiter=',')
            # propeller speed and engine speed in design condition are used to
            # determine gear ratio, so that operational design speed is given
            # by (nOperation*(nProp/nDesign))
            VaOperation=(OperationSpeed*0.51444)*(1-w) # Va - Velocity at propeller (knots)
            JOperation=VaOperation/((nOperation*(nProp/nDesign)/60)*D) # JOperation - Advance Coefficient for Operating Condition
            # preallocate arrays for PoverD search
            PoverD=np.zeros(36)
            Kt=np.zeros(36)
            Kq=np.zeros(36)
            effODesign=np.zeros(36)
            # for given J, vary PoverD to find best propeller efficiency.
            for index in range(36): # propeller pitch (propeller pitch up to 1.8 seems to be valid for a 4 bladed propeller, over this curves do not work, this is 1.6 for a 5 bladed propeller)
                PoverD[index]=0.05*(index+1) # from observed results it does not seem appropiate for propeller pitch to exceed 1.6 (as efficiency curve appears to change considerably), tried this using a bar of 0.2 and 0.8
                # format of wageningenbscrewdata (stored in propellerdata.mat):
                # ||                       Kt                       ||                       Kq                       ||
                # || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) ||
                # contains coefficients and terms of Kt and Kq polynomials for the wageningen b-screw series for a Rn of 2x10**6
                # (so that Kq,Kt=sum((Cs,t,u,v)*(J)**s*(P/D)))
                Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*(JOperation**wageningenbscrewdata[0:38,1])*(PoverD[index]**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))
                Kq[index]=np.sum(wageningenbscrewdata[0:46,5]*(JOperation**wageningenbscrewdata[0:46,6])*(PoverD[index]**wageningenbscrewdata[0:46,7])*(bar**wageningenbscrewdata[0:46,8])*(Z**wageningenbscrewdata[0:46,9]))
                # calculate open water efficiency for each PoverD:
                effODesign[index]=(JOperation/(2*np.pi))*(Kt[index]/Kq[index])
                # ensure efficiency values are below 1, if this is not the case
                # it is possible that the 'wrong part' of the efficiency curve
                # is being used.
                if (effODesign[index]>=1.0):
                    # if equal to or above 1 replace efficiency value with 0,
                    # so it is not selected when finding the maximum value (and
                    # index is left unchanged)
                    effODesign[index]=0
                elif (effODesign[index]<=0.0):
                    # if equal to or below 0 replace efficiency value with 0,
                    # so it is not selected when finding the minimum value (and
                    # index is left unchanged)
                    effODesign[index]=0
                else:
                    # value is valid.
                    pass
            # return the maximum effO value and its index PoverD (save over
            # array with single maximum efficiency value)
            effODesign=0
            for i, value in enumerate(effODesign):
                if value>effODesign:
                    effODesign=value
                    effODesignindex=i
        else:
            # operational condition (non-CPP) do not need to find design PoverD
            # as can load previously saved efficiency curve
            # load the existing propeller design data (including stored data
            # from propeller curve calculation)
            # IN WORK UNSURE IF nProp is needed
            nProp = np.loadtxt('temporary/calculatedFPP_nProp.csv', delimiter=',')
            # IN WORK UNSURE IF nProp is needed
            J = np.loadtxt('temporary/calculatedFPP_J.csv', delimiter=',')
            Kq = np.loadtxt('temporary/calculatedFPP_Kq.csv', delimiter=',')
            Kt = np.loadtxt('temporary/calculatedFPP_Kt.csv', delimiter=',')
            effOOperation = np.loadtxt('temporary/calculatedFPP_effOOperation.csv', delimiter=',')
            effODesign = np.loadtxt('temporary/calculatedFPP_effODesign.csv', delimiter=',')
            PoverD = np.loadtxt('temporary/calculatedFPP_PoverD.csv', delimiter=',')
            
    # - - Find Operating Condition, open water efficiency (curve) - -
    
    # this is carried out in similar manner for both design and operational
    # conditions, to allow for a fair comparison
    VaOperation=(OperationSpeed*0.51444)*(1-w) # Va - Velocity at propeller (knots)
    JOperation=VaOperation/((nOperation*(nProp/nDesign)/60)*D) # JOperation - Advance Coefficient for Operating Condition
    # Plots efficiency curve for a number of advance coefficient and find
    # the two closest advance coefficients and linearly interpolate between
    # them.
    if (PropDesign==1):
        # propeller operating efficiency curve not found yet or needs to be
        # recalculated for different optimum PoverD (CPP propeller)
        # Preallocate arrays
        J=np.zeros(61)
        Kt=np.zeros(61)
        Kq=np.zeros(61)
        effOOperation=np.zeros(61)
        for index in range(61):
            J[index]=index*0.05 # go through J values to plot efficiency curve
            # format of wageningenbscrewdata:
            # ||                       Kt                       ||                       Kq                       ||
            # || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) ||
            # contains coefficients and terms of Kt and Kq polynomials for the wageningen b-screw series for a Rn of 2x10**6
            # (so that Kq,Kt=sum((Cs,t,u,v)*(J)**s*(P/D)))
            Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*(J[index]**wageningenbscrewdata[0:38,1])*(PoverD[effODesignindex]**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))
            Kq[index]=np.sum(wageningenbscrewdata[0:46,5]*(J[index]**wageningenbscrewdata[0:46,6])*(PoverD[effODesignindex]**wageningenbscrewdata[0:46,7])*(bar**wageningenbscrewdata[0:46,8])*(Z**wageningenbscrewdata[0:46,9]))
            # calculate open water efficiency for each J:
            effOOperation[index]=(J[index]/(2*np.pi))*(Kt[index]/Kq[index])
            # ensure efficiency values are below 1, if this is not the case it
            # is possible that the 'wrong part' of the efficiency curve is
            # being used.
            if (effOOperation[index]>=1.0):
                # if equal to or above 1 replace efficiency value with 0, so it
                # is not selected when finding the maximum value (and index is
                # left unchanged)
                effOOperation[index]=0
            elif (effOOperation[index]<=0.0):
                # if equal to or below 0 replace efficiency value with 0, so it
                # is not selected when finding the minimum value (and index is
                # left unchanged)
                effOOperation[index]=0
            else:
                # value is valid.
                pass
        # output selected PoverD value
        PoverD=PoverD[effODesignindex]
        # save resulting efficiency curve
        np.savetxt('temporary/calculatedFPP_J.csv', J, delimiter=',')
        np.savetxt('temporary/calculatedFPP_Kq.csv', Kq, delimiter=',')
        np.savetxt('temporary/calculatedFPP_Kt.csv', Kt, delimiter=',')
        np.savetxt('temporary/calculatedFPP_effOOperation.csv', effOOperation, delimiter=',')
        np.savetxt('temporary/calculatedFPP_effODesign.csv', [effODesign], delimiter=',')
        np.savetxt('temporary/calculatedFPP_PoverD.csv', [PoverD], delimiter=',')
        # J and effOOperation are required for calculation, effODesign and
        # PoverD are saved for potential propeller efficiency plots
    else:
        pass
        # operational condition (non-CPP) do not need to find design PoverD as
        # can use loaded previously saved efficiency curve
    # find index of corresponding J values corresponding to JOperation
    for index in range(61):
        # go through each J value from smallest to largest
        if (J[index]>=JOperation):
            # when value of J is larger or equal to JOperation, this is upper J
            # value (first value above JOperation) and is given by
            upperindex=index
            # force for statement to end early
            break
        else:
            pass
            # not reached upper J value continue searching
    # check to see if a solution within propeller range has been found
    if 'upperindex' in locals():
        # variable has been found, check upperindex
        if (upperindex==0):
            # for very small speeds it is possible that first examined advance
            # coefficient is used, causing the lowerindex value (calculated below)
            # to be too small
            upperindex=1
            print('WARNING: Advance Coefficient is too small for propeller data, smallest value used!')
            print('This occured for a operating speed of ' + repr(OperationSpeed) + 'knots and a shaft speed of ' + repr(nOperation*(nProp/nDesign)) + 'rpm')
        else:
            # index is okay
            pass
    else:
        # solution has not been found, J (advance coefficient is not within the
        # range of the propeller series) assume largest possible value
        upperindex=60
        print('WARNING: Advance Coefficient is too large for propeller data, largest value used!')
        print('This occured for a operating speed of ' + repr(OperationSpeed) + 'knots and a shaft speed of ' + repr(nOperation*(nProp/nDesign)) + 'rpm')
    # lower J value (first value below JOperation) is given by
    lowerindex=upperindex-1
    # use these indices to linearly interpolate and find the 'off-design' efficiency (effO)
    effO=effOOperation[lowerindex]+((effOOperation[upperindex]-effOOperation[lowerindex])*(JOperation-J[lowerindex])/(J[upperindex]-J[lowerindex]))
    
    # - - Output effO and Engine Torque (accounting for CPP efficiency) - -
    
    # correct calculated open water efficiency for CPP and pod, if CPP and pod
    # corrections are 0 than they are not applied CPP or pod is not being used.
    if (CPP==0):
        pass
        # efficiency remains unchanged
    else:
        effO=effO*CPP
    if (pod_correction==0):
        pass
        # efficiency remains unchanged
    else:
        effO=effO*pod_correction
        
    
    # find propeller torque and thrust coefficients
    Kq=Kq[lowerindex]+((Kq[upperindex]-Kq[lowerindex])*(JOperation-J[lowerindex])/(J[upperindex]-J[lowerindex]))
    Kt=Kt[lowerindex]+((Kt[upperindex]-Kt[lowerindex])*(JOperation-J[lowerindex])/(J[upperindex]-J[lowerindex]))
    # find propeller torque, engine torque propeller thrust
    PropTorque=Kq*water_density*D**5*(nOperation*(nProp/nDesign)/60)**2
    EngTorque=PropTorque*nProp/nDesign
    PropThrust=Kt*water_density*D**4*(nOperation*(nProp/nDesign)/60)**2
    
    # - - Check Propeller Efficiency Curve (only check for Design Condition, if at all) - -
    
    # if (PropDesign==1)
    #     # for Design Condition plot propeller efficiency curve, for CPP may be
    #     # better not to plot this in every condition.
    #     # Preallocate arrays
    #     J=np.zeros((61,1))
    #     Kt=np.zeros((61,1))
    #     Kq=np.zeros((61,1))
    #     ploteffO=np.zeros((61,1))
    #     for index=1:61
    #         J[index]=-0.05+index*0.05 # go through J values to plot efficiency curve
    #         # find and plot for design PoverD value
    #         # format of wageningenbscrewdata:
    #         # ||                       Kt                       ||                       Kq                       ||
    #         # || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) || Cs,t,u,v | s (J) | t (P/D) | u (Ae/Ao) | v (z) ||
    #         # contains coefficients and terms of Kt and Kq polynomials for the
    #         # wageningen b-screw series for a Rn of 2x10**6
    #         # (so that Kq,Kt=sum((Cs,t,u,v)*(J)**s*(P/D)))
    #         Kt[index]=np.sum(wageningenbscrewdata[0:38,0]*(J[index]**wageningenbscrewdata[0:38,1])*(PoverD**wageningenbscrewdata[0:38,2])*(bar**wageningenbscrewdata[0:38,3])*(Z**wageningenbscrewdata[0:38,4]))
    #         Kq[index]=np.sum(wageningenbscrewdata[0:46,5]*(J[index]**wageningenbscrewdata[0:46,6])*(PoverD**wageningenbscrewdata[0:46,7])*(bar**wageningenbscrewdata[0:46,8])*(Z**wageningenbscrewdata[0:46,9]))
    #         # calculate open water efficiency for each J:
    #         ploteffO(index,1)=(J[index]/(2*np.pi))*(Kt[index,1]/Kq[index,1])
    #         # ensure efficiency values are below 1, if this is not the case it is
    #         # possible that the 'wrong part' of the efficiency curve is being used
    #         if (ploteffO(index,1)>=1.0)
    #             # if equal to or above 1 replace efficiency value with 0
    #             ploteffO(index,1)=0
    #         elif (ploteffO(index,1)<=0.0)
    #             # if equal to or below 0 replace efficiency value with 0
    #             ploteffO(index,1)=0
    #         else
    #             # value is valid.
    #             pass
    #     # plot graph
    #     figure # new figure window
    #     plot(J[:,1],Kt[:,1],'b',J[:,1],Kq[:,1],'r',J[:,1],ploteffO(:,1),'y',[0 3],[effODesign effODesign],'c',[0 3],[effO effO],'c')
    #     xlim([0.0 1.8])
    #     ylim([0.0 1.0])
    #     title('Design Condition Propeller Efficiency Curve')
    #     legend('Thust Cofficient (Kt)','Torque Coefficient (Kq)','Open Water Efficiency','Design Point','Operating Point','Location','SouthEast')
    #     text(0.1,0.9,['P/D: ',num2str(PoverD)])
    #     xlabel('Advance Coefficient (J)')
    # else
    #     % do not plot graph for operational condition
    #     pass
    # end
    
    return effO, EngTorque, PropThrust, PoverD, nProp
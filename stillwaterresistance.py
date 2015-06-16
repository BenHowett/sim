# Author: John Calleya (UCL)
# Version: 1.0
# History:
# The Holtrop-Mennen function was adapted from an existing Matlab function

# Description:
# This file contains still water resistance models

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

def holtrop(design_condition, water_density, Speed, L, T, B, Cp, LCB, Disp, Cwp, Cm, D, Twin, Z, Foul, ChR):
    # Implementation of method given in:
    # An appoximate power prediction method, Holtrop, J. and Mennen, G.G.J.
    # International Shipbuilding Progress, Pages 166-170, Volume 29, 1982
    # (using similar nomenclature)
    # and updated form factor, and wake from:
    # A Statistical Re-Analysis of Resistance and Propulsion Data
    # Holtrop, J.
    # International Shipbuilding Progress
    # Pages 272-276, Volume 31, 1984
    
    # note that bulbous bow and transom area have not been included and surface
    # area is based on calculation from Holtrop-Mennen 1982.
    
    # bulbous bow can also be based on Holtrop-Mennen paper:
    # ABT - Bulbous Bow Area (fixed value - based on 1982 paper to maintain the same bulbous bow area to (B*T) ratio)
    # hB - Bulbous Bow Height from Keel (fixed value - based on 1982 paper to maintain the same bulbous bow height to (T) ratio)
    # At - Immersed Area of Transom (fixed value - based on 1982 paper to maintain the same bulbous bow area to (B*T) ratio)
    
    # input variables:
    # design_condition
    # water_density
    # Speed - speed in knots
    # L - Ship waterline length (in design or given condition)
    # T - Draught
    # B - Beam
    # Cp - prismatic coefficient (in given condition)
    # LCB - longitudinal centre of buoyancy from aft
    # Disp - displacement
    # Cwp - waterplane coefficient
    # Cm - midship coefficient
    # D - propeller diameter
    # Twin - Single (1) or Twin (2) propulsion arrangement
    # BAR - blade area ratio
    # Z - number of propellers
    
    # if speed is above below 2 knots, all outputs are assumed to be 0
    
    # correction made to calculated blade area ratio to kellers formula based
    # on the examination of a few sample ships
    
    # ignore very low speeds because calcululation will be invalid
    if Speed < 2:
        # Rw and Ps result in NaN at 0 knots.
        Rv = 0
        Rw = 0
        Ra = 0
        Rapp = 0
        t = 0
        w = 0
        bar = 0
        rre = 0
        return Rv, Rw, Ra, Rapp, t, w, bar, rre
    
    # calculated variables
    # re - Reynolds Number
    # Cf - Frictional Resistance Coefficient
    # C12 - Unused with 1984 changes
    # C13 - Unused with 1984 changes
    # C14
    # lcb
    # Lr
    # K1 - Form Factor (1+k)
    # S - wetted surface area
    # C7
    # V - Displaced Volume
    # Cwp - Waterplane Coefficient
    # iE
    # C1
    # C3
    # C2
    # C5
    # Fn - Froude Number
    # landa
    # C16
    # M1
    # C15
    # M2
    # M3
    # M4
    # C17
    # Cb - Block Coefficient
    # C4
    # Ca - Correlaion Allowance Coefficient
    # K2 - Appendage Resistance Factor (1+k2), changes for single and twin screw ship
    # Twin is 2 for a twin screw ship and 1 for a single screw ship
    # C8 - Unused (described in paper)
    # C9 - Unused (described in paper)
    # C11 - Unused (described in paper)
    # Cp1
    # C19
    # C20
    # w - Wake Fraction
    # C10
    # t - Thrust Deduction
    # K - Constant for Single or Twin Screw ships
    # bar - Blade Area Ratio (Keller's formula)
    # rre - Relative Rotative Efficiency
    # Ra - Correlation Allowance
    # Rapp - Appendage Resistance (unused in main program, but provided as a check)
    
    # - - output variables - -
    # Rv - Viscous Resistance (unused in main program, but provided as a check)
    # Rw - Wave Resistance (unused in main program, but provided as a check)
    # Rt - Total Resistance (includes Ra, Rapp and Foul)
    # PC - Propulsive Coefficient (unused in main program, but provided as a check)
    # Ps - Shaft Power
    # rre - Relative Rotational Efficiency (same for all conditions, so given as a input after design condition)
    # w - Wake coefficient
    # bar - Blade Area Ratio (same for all conditions, so given as a input after design condition)
    # t - Thrust Deduction coefficient
    
    # calculate viscous Rv=Rf(1+K1)
    # re
    re=(Speed*L*0.51444/0.00000118831)
    # using the kinematic viscosity of salt water at 15deg from:
    # http://ittc.sname.org/new%20recomendations/pdf%20Procedures%202008/7.5-02-01-03.pdf
    # Cf - Frictional Resistance Coefficient - ITTC 1957 Model-Ship Correlation Line
    Cf=0.075/((np.log10(re)-2)**2)
    # C12 only used in 1982 version
    # if ((T/L)>0.05):
    #     C12=(T/L)**0.2228446
    # elif ((T/L)<0.05) and ((T/L)>0.02):
    #     C12=48.20*(((T/L)-0.02)**2.078)+0.479948
    # elif ((T/L)<0.02):
    #     C12=0.479948
    # else:
    #     C12=48.20*(((T/L)-0.02)**2.078)+0.479948
    # C13 and C14
    # C13=1+0.003*0
    C14=1+0.011*0
    # Assumes normal section shape for all hullforms
    # use -10 for v shape sections and +10 for u shape section makes this
    # pessimistic.
    # lcb is the longitudinal position of the centre of buoyancy forward of
    # 0.5L as a percentage of L
    lcb=(( LCB-( 0.5*L ))/L )*100
    # Assumes LCB measured in m from AP
    # Lr
    Lr=L*( 1-Cp+( 0.06*Cp*lcb )/( 4*Cp-1 ))
    # V - Displaced Volume
    V = Disp/water_density
    # K1 - Form Factor (1+k)
    # form factor from 1982 reference
    # K1=C13*(0.93+C12*((B/Lr)**0.92497)*((0.95-Cp)**-0.521448)*((1-Cp+0.0225*lcb)**0.6906))
    # form factor from 1984 reference
    K1=0.93+0.487118*C14*((B/L)**1.06806)*((T/L)**0.46106)*((L/Lr)**0.121563)*(((L**3)/V)**0.36486)*((1-Cp)**-0.604247)
    # Cb - Block Coefficient
    Cb=V/(B*T*L)
    ABT=0
    # S - wetted area of hull (Holtrop-Mennen 1982 approximation)
    S=L*(2*T+B)*np.sqrt(Cm)*(0.453+0.4425*Cb-0.2862*Cm-0.003467*(B/T)+0.3696*Cwp)+2.38*ABT/Cb    
    # Rv
    Rv=0.5*water_density*((Speed*0.51444)**2)*S*Cf*K1
    
    # calculate wave resistance (Rw)
    # C7
    if ((B/L)<0.11):
        C7=0.229577*(B/L)**0.33333
    elif ((B/L)<0.25) and ((B/L)>0.11):
        C7=(B/L)
    elif ((B/L)>0.25):
        C7=0.5-0.0625*(L/B)
    else:
        C7=0.5-0.0625*(L/B)
    # Cwp - Waterplane Coefficient
    # Cwp=(2*Cp)/(1+Cp)
    # iE - Half angle entrance
    iE=1+89*np.exp((-(L/B)**0.80856)*((1-Cwp)**0.30484)*((1-Cp-0.0225*lcb)**0.6367)*((Lr/B)**0.34574)*(((100*V)/(L**3))**0.16302))
    # C1
    C1=2223105*(C7**3.78613)*((T/B)**1.07961)*((90-iE)**-1.37565)
    # bulbous bow parameters
    # ABT - Bulbous Bow Area
    # USED THIS PREVIOUSLY ABT=0.0625*B*T # matches ratio given in example in Holtrop-Mennen Paper (may over estimate resistance for small ships and over estimate for large ships, but not clear)
    # 0.035*B*T  # from inspection of panamax container carrier hullform
    # hB - Bulbous Bow Height from Keel
    # USED THIS PREVIOUSLY hB=0.4*T # matches ratio given in example in Holtrop-Mennen Paper (may over estimate resistance for small ships and over estimate for large ships, but not clear)
    # hB=0.3015*T    # from inspection of panamax container carrier hullform
    # C3 - coefficient that determines the influence of the bulbous bow
    # C3=0.56*(ABT**1.5)/(B*T*(0.31*(ABT**0.5)+T-hB))
    # ABT is area of bulbous bow
    # T should be fore draught but taken as draught assumes level trim
    # hB is the position of the transverse area above the keel
    # C2
    # C2=exp(-1.89*((C3)**0.5))
    # C2 is 0 when there is no bulbous bow
    C2=0
    # At - Immersed Area of Transom
    # USED THIS PREVIOUSLY At=0.05*B*T # matches ratio given in example in Holtrop-Mennen Paper (may over estimate resistance for small ships and over estimate for large ships, but not clear)
    # At=0    # from inspection of panamax container carrier hullform
    # C5 expresses the influence of the transom stern on wave resistance
    # USED THIS PREVIOUSLY C5=1-0.8*At/(B*T*Cm)
    # C5=1 if Transom has no influence, this is transom immersion at 0 speed.
    C5=1
    # Fn - Froude Number
    Fn=(Speed*0.51444)/((9.80665*L)**0.5)
    # landa
    if (L/B<12):
        landa=1.446*Cp-(0.03*L/B)
    elif (L/B>12):
        landa=1.446*Cp-0.36
    else:
        landa=1.446*Cp-0.36
    # C16
    if (Cp<0.8):
        C16=(8.07981*Cp)-(13.8673*Cp**2)+(6.984388*Cp**3)
    else:
        C16=1.73014-0.7067*Cp
    # C15
    if (((L**3)/V)<512):
        C15=-1.69385
    elif (((L**3)/V)>512) and (((L**3)/V)<1727):
        C15=-1.69385+((L/(V**(1/3)))-8.0)/2.36
    elif (((L**3)/V)>1727):
        C15=0.0
    else:
        C15=-1.69385+((L/(V**(1/3)))-8.0)/2.36
    # 1984 update adds a different regression curve for wave-making for higher
    # Froude numbers
    if (Fn>=0.55):
        # M3
        M3=(-7.2035*(B/L)**0.326869)*((T/B)**0.605375)
        # M4
        M4=C15*0.4*np.exp(-0.034*(Fn**-3.29))
        # C17
        C17=6919.3*Cm**(-1.3346)*((V/(L**3))**2.00977)*((L/B)-2)**1.40692
        Rwb=C17*C2*C5*Disp*9.80665*np.exp(M3*(Fn**-0.9)+M4*np.cos(landa*(Fn**-2)))
        Rw=Rwb
    elif (Fn<=0.40):
        # use Rwa old formula in 1982 paper fits okay for smaller Froude numbers
        # M1
        M1=(0.0140407*L/T)-(1.75254*(V**(1/3))/L)-(4.79323*B/L)-C16
        # M2
        # M2=C15*(Cp**2)*exp(-0.1*Fn**(-2)) was in old version now unused,
        # replaced with M4 in newer version in 1982 formula
        # M4
        M4=C15*0.4*np.exp(-0.034*(Fn**-3.29))
        # Rwa
        Rwa=C1*C2*C5*Disp*9.80665*np.exp(M1*(Fn**-0.9)+M4*np.cos(landa*(Fn**-2)))
        Rw=Rwa
    else:
        # for 0.40<Fn<0.55 use iterpolation based on the above formulae
        # M1 at 0.4
        M104=(0.0140407*L/T)-(1.75254*(V**(1/3))/L)-(4.79323*B/L)-C16
        # M2 at 0.4
        # M204=C15*(Cp**2)*exp(-0.1*0.4**(-2)) was in old version now unused,
        # replaced with M4 in newer version in 1982 formula
        # M4 at 0.4
        M404=C15*0.4*np.exp(-0.034*(0.4**-3.29))
        # Rwa at 0.4
        Rwa04=C1*C2*C5*Disp*9.80665*np.exp(M104*(0.4**-0.9)+M404*np.cos(landa*(0.4**-2)))
        # Note that C1, C2, C5 and C17 are not dependent upon Froude number.
        # M3 at 0.55
        M3055=(-7.2035*(B/L)**0.326869)*((T/B)**0.605375)
        # M4 at 0.55
        M4055=C15*0.4*np.exp(-0.034*(0.55**-3.29))
        # C17
        C17=6919.3*Cm**(-1.13346)*((V/(L**3))**2.00977)*((L/B)-2)**1.40692
        Rwb055=C17*C2*C5*Disp*9.80665*np.exp(M3055*(0.55**-0.9)+M4055*np.cos(landa*(0.55**-2)))
        # interpolate to find Rw (according to 1984 reference)
        Rw=Rwa04+(10*Fn-4)*(Rwb055-Rwa04)/1.5
    
    # calculate correlation allowance (Ra)
    # C4
    if ((T/L)<0.04):
        C4=T/L
    elif ((T/L)>0.04):
        C4=0.04
    else:
        C4=T/L
    # note in order to calculate C4 the forward draught should be used, but
    # mean draught is used.
    # Ca - Correlation Allowance Coefficient
    Ca=0.006*(L+100)**(-0.16)-0.00205+0.003*((L/7.5)**0.5)*Cb**4*C2*(0.04-C4)
    # Ra
    Ra=0.5*water_density*((Speed*0.51444)**2)*S*Ca
    
    # calculate appendae resistance (Rapp)
    #(1+k2) value for all appendages
    if (Twin==1):
        # single screw ship
        K2=1.4
    else:
        # twin screw or there is an ERROR
        Twin=2
        K2=2.8
    # baseline appendage area
    Sapp=0.05*S
    Rapp=0.5*water_density*((Speed*0.51444)**2)*Sapp*Cf*K2
    
    # calculate wake fraction (w)
    # C8
    if ((B/T)<5):
        C8=B*S/(L*D*T)
    elif ((B/T)>5):
        C8=(S*((7*B/T)-25))/(L*D*((B/T)-3))
    else:
        C8=(S*((7*B/T)-25))/(L*D*((B/T)-3))
    # average draught used instead of aft draught
    # C9
    if (C8<28):
        C9=C8
    elif (C8>28):
        C9=32-(16/(C8-24))
    else:
        C9=32-(16/(C8-24))
    # C11
    if ((T/D)<2):
        C11=(T/D)
    elif ((T/D)>2):
        C11=0.0833333*(T/D)**3+1.33333
    else:
        C11=0.0833333*(T/D)**3+1.33333
    # average draught used instead of aft draught
    # Cp1
    Cp1=1.45*Cp-0.315-0.0225*lcb
    if (Twin==1):
        # single screw ship
        # C19
        if (Cp<0.7):
            C19=0.12997/(0.95-Cb)-0.11056/(0.95-Cp)
        else:
            C19=0.18567/(1.3571-Cm)-0.71276+0.38648*Cp
        # C20
        C20=1+0.015*0
        # Cstern is 0.
        # Assumes normal section shape for all hullforms use -10 for v shape
        # sections and +10 for u shape section makes this pessimistic.
        # wake formula based on 1984 paper:
        w=C9*C20*(K1*Cf+Ca)*(L/T)*(0.050776+0.93405*C11*((K1*Cf+Ca)/(1-Cp1)))+0.27915*C20*((B/(L*(1-Cp1)))**0.5)+C19*C20
        # other wake estimates from 1982 paper, second one is for sailing ship
        # forms and underestimates, first one give similar results to above
        #     w=C9*(K1*Cf+Ca)*(L/T)*(0.0661875+1.21756*C11*((K1*Cf+Ca)/(1-Cp1)))...
        #     + 0.24558*((B/(L*(1-Cp)))**0.5)-(0.09726/(0.95-Cp))...
        #     + (0.11434/(0.95-Cb))+0.75*0+0.002*0
        #
        #     w=0.3*Cb+10*(Cf*K1+Ca)*Cb-0.1
    elif (Twin==2):
        # twin screw ship
        w=0.3095*Cb+10*(Cf*K1+Ca)*Cb-0.23*D/np.sqrt(B*T)
    else:
        # ERROR here somewhere
        pass
    # C10
    # if (L/B>5.2)
    #     C10=B/L
    # elif (L/B<5.2)
    #     C10=0.25-0.003328402/(B/L-0.134615385)
    # else
    #     C10=0.25-0.003328402/(B/L-0.134615385)
    
    # calculate thrust deduction (t)
    if (Twin==1):
        # single screw ship
        # old formula from 1982 paper
        # t=0.001979*L/(B-B*Cp1)+1.0585*C10-0.00524-0.1418*D*D/(B*T)+0.0015*0
        # Assumes normal section shape for all hullforms
        # use -10 for v shape sections and +10 for u shape section makes this
        # pessimistic, but probably still more accurate then twin screw formula
        t=0.25014*((B/L)**0.28956)*((np.sqrt(B*T)/D)**0.2624)/((1-Cp+0.0225*lcb)**0.01762)+0.0015*0
    elif (Twin==2):
        # twin scew ship
        t=0.325*Cb-0.1885*D/np.sqrt(B*T)
    else:
        # likely due to a mixture of single and twin screw ships used in
        # scaling, assume twin screw
        t=0.325*Cb-0.1885*D/np.sqrt(B*T)
    
    # calculate blade area ratio and relative rotational efficiency in design condition (bar and rre)
    if (design_condition==1):
        # design condition bar should be calculated
        # coefficients for bar (blade area ratio) calculation
        if (Twin==1):
            # single screw ship
            K=0.2
            correction=1.14
            # from kellers formula to actual bar used from a few sample ships
        elif (Twin==2):
            # twin scew ship
            K=0.1
            correction=1.16
            # from kellers formula to actual bar used from a few sample ships
        else:
            # ERROR here somewhere
            pass        
        # THIS FORMULA IS CORRECT
        bar=correction*(K+(1000/Twin)*((1.3+0.3*Z)*(Rv*Foul+Rw+Ra+Rapp*Foul+ChR)/(D*D*((99653)+(9.80665*1000*water_density*(T-D/2))))))
        # THIS FORMULA IS CORRECT
        # where (Rv*Foul+Rw+Ra+Rapp*Foul+ChR) is the total resistance, which is
        # assumed to be equal to the thrust at the propeller
        rre=0.9922-0.05908*bar+0.07424*(Cp-0.0225*lcb)
    else:
        # use design values of bar and rre, rre is also consistent with bar
        # because it is a function of bar and other static design values
        bar=0
        rre=0
    return S, Rv, Rw, Ra, Rapp, t, w, bar, rre

# EXAMPLE VALUES FOR SPECIFIC HULFORMS THAT CAN BE USED AS A CHECK
#                                Container      Bulk
#                                Carrier        Carrier
# Typical Ship Speed             25 knots       15 knots
# Form Factor                    1.1            1.1
# Effective Wake Coefficient     0.792          0.917
# Thrust deduction coefficient   0.853          0.803
# Hull Efficiency                0.928          1.142
# Open water efficiency          0.682          0.624
# Relative Rotative Efficiency   1.011          1.005
# Transmission Efficiency        1.000          1.000
# Appendage coefficient          1.050          1.050
# Propulsive coefficient         0.610          0.682
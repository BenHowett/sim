# Author: John Calleya (UCL)
# Version: 1.0
# History:
# 1.0 there is an issue with the GZ and heeling_moment calculator that gives
# the wrong results

# Description:
# This file contains still water resistance models

# this file converts simple parameters describing the hull form into a rough
# representation of the hullform that can be used for resistance calculations

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

# NOTES

# this iterates beam or draught as an outer loop and iterates/balances
# displacement/volume as an inner loop

# Assume that Transom at propeller is 0.06*hg.prop_diameter long circular but effort to include this.  This is then
# connected to a horizontal straight line between the here and the end of the bp       
# ability to change COB relative to bow??
# add bulbous bow afterwards
# what happens if desired cp cannot be achieved???

# use and check demanded volume for current loop
# FOR NOW ASSUME A DEADWEIGHT TO DISPLACEMENT VALUE!!!

# NEED TO RETURN INFORMATION TO HELP WITH BULKHEAD POSITIONS/SIZES
# NEED TO CHECK FOR PROPELLER SUBMERGENCE

# NOTES

# FUNCTIONS FOR COSH CURVE TO BE USED BY GENERATEHULL
# When this curve is plotted on the x-y plane, at x=0, y=1 and at y=1, x=0.
# The curve starts perpendicular to the y-axis/horizontal at x=0 at goes to a
# "point" at x=1
def coshcurve(x, m):
    # x SHOULD BE BETWEEN 0 AND 1
    # find y value of curve given x value
    y = 1 - (( np.cosh( x*m*np.pi )-1 )/( np.cosh( m*np.pi )-1 ))
    return y
def inversecoshcurve(y, m):
    # y SHOULD BE BETWEEN 0 AND 1
    # find x value of curve given y value
    x = np.arccosh( np.cosh( m*np.pi )-y*( np.cosh( m*np.pi )-1 ))/( m*np.pi )
    return x
def areacoshcurve(x, y, m):
    # equation for area under cosh curve
    area = ( np.cosh( m*np.pi )-( np.sinh( m*np.pi )/( m*np.pi )))/( np.cosh( m*np.pi )-1 )
    # multiple 1 to 1 curve by actual dimensions to get area
    area = x*y*area
    return area
def intxfxcoshcurve(x, m):
    # measured in x direction (towards point end of curve) from zero
    # equation for the integral of xf(x)
    intxfx = ( 1/( np.cosh( m*np.pi )-1))*((( np.cosh( m*np.pi )-( m*np.pi )*np.sinh( m*np.pi ))/(( m*np.pi )**2))+(( 1/2 )*np.cosh( m*np.pi ))-( 1/(( m*np.pi )**2 )))
    # multiply calculated intxfx by actual dimension in x direction
    intxfx = x*intxfx
    return intxfx
    
    
def generatehull(run, displacement, water_density,
            waterline_number, set_beam_or_draught, beam_or_draught,
            block_coefficient, waterline_length, depth_of_draught,
            midship_coefficient, overall_length, flare_angle,
            deadrise_angle, bow_angle, pmb_angle,
            stern_slope_angle, stern_point_of_waterline,
            prop_point_of_waterline, transom_of_beam, propulsors,
            hull_tip_clear_of_diameter, keel_tip_clear_of_diameter,
            disc_clear_of_diameter, pmb_fwd_of_waterline,
            pmb_aft_of_waterline, waterline_and_transom_overlap,
            aftercutup_of_waterline):
    
    # class for hg. outputs (beam, draught, displaced_volume,
    # waterline_halfbeam, waterline_area, waterplane_coefficient,
    # calculated_volume)
    class hg:
        pass
        
    #sample container ship parameters for testing (comment out when not in use)
    #run = 0
    #displacement = [72618]
    #water_density = [1.024]
    #waterline_number = [30]
    #set_beam_or_draught = ["beam"]
    #beam_or_draught = [32.0]
    #block_coefficient = [0.64]
    #waterline_length = [279.898]
    #depth_of_draught = [1.678]
    #midship_coefficient = [0.980]
    #overall_length = [294.221]
    #flare_angle = [0.00*np.pi/180]
    #deadrise_angle = [0.00*np.pi/180]
    #bow_angle = [31.60*np.pi/180]
    #pmb_angle = [14.442*np.pi/180]
    #stern_slope_angle = [7.785*np.pi/180]
    #stern_point_of_waterline = [-0.026]
    #prop_point_of_waterline = [0.023]
    #transom_of_beam = [0.965]
    #propulsors = [1]
    #hull_tip_clear_of_diameter = [0.250]
    #keel_tip_clear_of_diameter = [0.035]
    #disc_clear_of_diameter = [1.000]
    #pmb_fwd_of_waterline = [0.780]
    #pmb_aft_of_waterline = [0.044]
    #waterline_and_transom_overlap = [0.00]
    #aftercutup_of_waterline = [0.038]
    
    # CORRECTIONS FOR CONTAINER SHIP
    pmb_correction = 0.26
    # 0 for VLCC
    # SCALE BETWEEN 0 and 0.26 with block coefficient
    # PRINT M VALUE to check
    
    # correction to calibrate model, reduce parallel midbody to account for curve not being fine enough for faster hull forms
    pmb_fwd_of_waterline = [pmb_fwd_of_waterline[run]-(pmb_correction*(pmb_fwd_of_waterline[run]-pmb_aft_of_waterline[run]))]
    pmb_aft_of_waterline = [pmb_aft_of_waterline[run]+(pmb_correction*(pmb_fwd_of_waterline[run]-pmb_aft_of_waterline[run]))]
    # correction to calibrate model, reduce too much volume under hullform by changing curve connecting between propeller and keel, use same correction as before
    aftercutup_of_waterline = [aftercutup_of_waterline[run]+(2*pmb_correction*(pmb_fwd_of_waterline[run]-pmb_aft_of_waterline[run]))]
    # find displaced volume
    hg.displaced_volume = [displacement[run]/water_density] # stored to hg.displaced_volume[0]
    # find midsection characteristics
    
    # IN WORK NEED TO FIX THIS - TO MAKE A FUNCTON OF RUN??
    
    if set_beam_or_draught[run] == "beam":
        if run == 0:
            hg.beam = [beam_or_draught[0]]
            hg.draught = [hg.displaced_volume[0]/(block_coefficient[0]*waterline_length[0]*hg.beam[0])]
        else:
            hg.beam.append(beam_or_draught[run])
            hg.draught.append(hg.displaced_volume[0]/(block_coefficient[run]*waterline_length[run]*hg.beam[run]))
    else:
        # set_beam_or_draught[run] == "draught" or there is an ERROR
        if run == 0:
            hg.draught = [beam_or_draught[0]]
            hg.beam = [hg.displaced_volume[0]/(block_coefficient[0]*waterline_length[0]*hg.draught[0])]
        else:
            hg.draught.append(beam_or_draught[run])
            hg.beam.append(hg.displaced_volume[0]/(block_coefficient[run]*waterline_length[run]*hg.draught[run]))
    if run == 0:
        depth = [depth_of_draught[run]*hg.draught[run]]
    else:
        depth.append(depth_of_draught[run]*hg.draught[run])
    # equation for bilge_radius if both flare_angle and deadrise_angle are considered:
    bilge_radius = (np.sqrt(( hg.beam[run]*hg.draught[run]*( 1-midship_coefficient[run] )
                    -( hg.draught[run]**2 )*np.tan( flare_angle[run] )
                    -((( hg.beam[run]/2 )-hg.draught[run]*np.tan( flare_angle[run] ))**2)
                    *np.sin( deadrise_angle[run] )
                    *np.sin(( np.pi/2 )+flare_angle[run] )
                    /np.sin(( np.pi/2 )-flare_angle[run]-deadrise_angle[run] ))
                    /(2*(np.tan((( np.pi/2 )-flare_angle[run]-deadrise_angle[run] )
                    /2 )-((( np.pi/2 )-flare_angle[run]-deadrise_angle[run] )
                    /2 )))))
    #equation used to test midship coefficient, which worked for no flare and deadrise:
    #((draught[0]-bilge_radius)*beam[0]+(np.pi*(bilge_radius**2)/2)+(beam[0]-2*bilge_radius)*bilge_radius)/(beam[0]*draught[0])
    # set transom_stern_height based on required waterline overlap with transom
    if run == 0:
        transom_stern_height =[(depth[0]-hg.draught[0]
                                +waterline_and_transom_overlap[0])]
    else:
        transom_stern_height.append(depth[run]-hg.draught[run]
                                +waterline_and_transom_overlap[run])
    # find the position (along the ship) from the AP of the stern and bow:
    stern_point = stern_point_of_waterline[run]*waterline_length[run]
    prop_point = prop_point_of_waterline[run]*waterline_length[run]
    aftercutup_point = aftercutup_of_waterline[run]*waterline_length[run]
    bow_point = overall_length[run]+stern_point
    # calculates the height of the flared section of the hullform
    upper_section_height = ((depth[run]+2*bilge_radius*np.sin((( np.pi/2 )
                            -flare_angle[run]-deadrise_angle[run] )/2)
                            *(np.sin((( np.pi/2 )+flare_angle[run]
                            -deadrise_angle[run] )/2 )*np.tan( flare_angle[run] )
                            -np.cos((( np.pi/2 )+flare_angle[run]
                            -deadrise_angle[run] )/2 ))-(( hg.beam[run]/2 )
                            *np.tan( deadrise_angle[run] )))
                            /(1-np.tan( flare_angle )*np.tan( deadrise_angle )))
    # above was equal to depth - bilge radius when flare and deadrise were zero
    # bilge_radius is equal to middle_section_height when there is no flare or
    # deadrise
    middle_section_height = (2*bilge_radius*np.sin((( np.pi/2 )-flare_angle[run]
                            -deadrise_angle[run] )/2 )*np.cos((( np.pi/2 )
                            +flare_angle[run]-deadrise_angle[run] )/2 ))                  
    # find the propeller diameter or "propeller space" (for some propulsor types)
    # (it is assumed that the propeller/propeller space is level with the keel)
    hg.prop_diameter = (( depth[run]-( transom_stern_height[run]
                    +np.tan( stern_slope_angle[run] )*( prop_point-stern_point )))
                    /( 1+hull_tip_clear_of_diameter[run]
                    +keel_tip_clear_of_diameter[run] ))
    # set array length using numpy arrays for information that is saved
    hg.waterline = np.zeros(waterline_number[run])
    hg.waterline_halfbeam = np.zeros(waterline_number[run])
    pmb_fwd_point = np.zeros(waterline_number[run])
    pmb_aft_point = np.zeros(waterline_number[run])
    hg.waterline_bow = np.zeros(waterline_number[run])
    hg.waterline_stern = np.zeros(waterline_number[run])
    hg.waterline_area = np.zeros(waterline_number[run])
    hg.waterplane_coefficient = np.zeros(waterline_number[run])
    # vary m between 0.1 and 5.
    mrange = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4,
              1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8,
              2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2,
              4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
    for m in mrange:
        # calculate the waterline area and other outputs for each waterline
        for waterline_index in range(waterline_number[run]):
            # divide depth into sections at each waterline
            hg.waterline[waterline_index] = (( waterline_index+1 )
                                        *( depth[run]/waterline_number[run] ))
            if hg.waterline[waterline_index] <= ( depth[run]-upper_section_height-middle_section_height ):
                # waterline beam is given by lower section
                hg.waterline_halfbeam[waterline_index] = hg.waterline[waterline_index]/np.tan( deadrise_angle[run] )
            elif hg.waterline[waterline_index] < ( depth[run]-upper_section_height ):
                # waterline beam is given by middle section
                # accounted for difference between draught and depth when
                # accounting for flare angle
                # MAY NOT BE FULLY ACCURATE, BUT GOOD ENOUGH
                hg.waterline_halfbeam[waterline_index] = (( hg.beam[run]/2 )
                                -(( upper_section_height+hg.draught[run]-depth[run] )
                                *np.tan( flare_angle[run] ))
                                -(( bilge_radius*np.cos( flare_angle[run] ))
                                -np.sqrt(( bilge_radius**2 )
                                -((( bilge_radius*np.sin( flare_angle[run] ))
                                +(depth-upper_section_height
                                -hg.waterline[waterline_index]))**2 ))))
            else:
                # waterline is in the upper section
                # NEED TO ACCOUNT FOR FLARE ANGLE DIFFERENCE BETWEEN DRAUGHT
                # AND DEPTH
                hg.waterline_halfbeam[waterline_index] = (( hg.beam[run]/2 )
                    -( hg.waterline[waterline_index]-depth[run]+upper_section_height )
                    *np.tan( flare_angle[run] ))
            # find end of parrallel midbody at the waterline
            # (assuming parallel midbody extends as far as bilge curve)
            if hg.waterline[waterline_index] > ( depth[run]-upper_section_height ):
                pmb_fwd_point[waterline_index] = ( pmb_fwd_of_waterline[run]
                    *waterline_length[run]
                    -(( depth[run]-hg.waterline[waterline_index] )
                    /np.tan(pmb_angle[run] )))
                pmb_aft_point[waterline_index] = ( pmb_aft_of_waterline[run]
                    *waterline_length[run]
                    +(( depth[run]-hg.waterline[waterline_index] )
                    /np.tan(pmb_angle[run] )))
            else:
                # waterline is in lower section where pmb fwd points do not change
                pmb_fwd_point[waterline_index] = ( pmb_fwd_of_waterline[run]
                    *waterline_length[run]
                    -(( depth[run]-upper_section_height )
                    /np.tan(pmb_angle[run] )))
                pmb_aft_point[waterline_index] = ( pmb_aft_of_waterline[run]
                    *waterline_length[run]
                    +(( depth[run]-upper_section_height )
                    /np.tan(pmb_angle[run] )))
            # find bow and stern points at waterline
            hg.waterline_bow[waterline_index] = ( bow_point
                                        -( depth[run]-hg.waterline[waterline_index] )
                                        *np.tan( bow_angle[run] ))
            # find stern point at waterline on centreline considering the position of
            # the propulsor
            if ( depth[run] - hg.waterline[waterline_index] ) <= ( transom_stern_height[run] ):
                # waterline is on transom stern
                hg.waterline_stern[waterline_index] = stern_point
                # find area of waterline = fwd area + pmb area + aft area
                hg.waterline_area[waterline_index] = (2
                *areacoshcurve(( hg.waterline_bow[waterline_index]
                -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                +2*( pmb_fwd_point[waterline_index]
                -pmb_aft_point[waterline_index] )*hg.waterline_halfbeam[waterline_index]
                +2*areacoshcurve(( pmb_aft_point[waterline_index]
                -hg.waterline_stern[waterline_index] ),( hg.waterline_halfbeam[waterline_index]
                -( transom_of_beam[run]*hg.beam[run]/2 )),m )
                +2*( pmb_aft_point[waterline_index]-hg.waterline_stern[waterline_index] )
                *( transom_of_beam[run]*hg.beam[run]/2 ))
                # find waterplane coefficient
                hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                -hg.waterline_stern[waterline_index])))
                # find centre of area (from aft) (total moments of area/total area)
                # INCOMPLETE - NEED TO ADD DISTANCE OF EACH "PIECE" FROM STERN TO BELOW
#                centre_of_area_from_stern[waterline_index]= ((
#                intxfxcoshcurve(( hg.waterline_bow[waterline_index]-pmb_fwd_point[waterline_index] ),m )
#                +0.5*( pmb_fwd_point[waterline_index]-pmb_aft_point[waterline_index] )*( 2*( pmb_fwd_point[waterline_index]-pmb_aft_point[waterline_index] )*hg.waterline_halfbeam[waterline_index])
#                +intxfxcoshcurve(( pmb_aft_point[waterline_index]-hg.waterline_stern[waterline_index] ),m )
#                +0.5*( pmb_aft_point[waterline_index]-hg.waterline_stern[waterline_index] )*( 2*( pmb_aft_point[waterline_index]-hg.waterline_stern[waterline_index] )*( transom_of_beam[run]*beam[run]/2 )))
#                /hg.waterline_area[waterline_index] )
            elif ( depth[run] - hg.waterline[waterline_index] ) <= ( transom_stern_height[run]+np.tan( stern_slope_angle[run] )*( prop_point-stern_point )):
                # waterline is on sloping section that slopes to prop_point
                hg.waterline_stern[waterline_index] = stern_point-(( depth[run]-transom_stern_height[run]-hg.waterline[waterline_index])/np.tan( stern_slope_angle[run] ))
                # find area of waterline = fwd area + pmb area + aft area
                # assumes that transom length at waterline decreases as a straight line
                # to meet a point (for 1 propeller) or a line (for 2 propellers)
                # Checked for errors up to here
                if propulsors[run] == 1:
                    # transom goes to single point above propeller
                    # transom_length varies between 0 and transom_of_beam*beam/2
                    transom_halflength = (( transom_of_beam[run]*hg.beam[run]/2 )
                    *(( prop_point-stern_point )-(( depth[run]
                    -transom_stern_height[run]-hg.waterline[waterline_index])
                    /np.tan( stern_slope_angle[run] )))/( prop_point-stern_point ))
                    hg.waterline_area[waterline_index] = (2
                    *areacoshcurve(( hg.waterline_bow[waterline_index]
                    -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                    +2*( pmb_fwd_point[waterline_index]
                    -pmb_aft_point[waterline_index] )
                    *hg.waterline_halfbeam[waterline_index]
                    +2*areacoshcurve( ( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] ),( hg.waterline_halfbeam[waterline_index]
                    -transom_halflength ),m )
                    +2*(( prop_point-stern_point )-(( depth[run]
                    -transom_stern_height[run]
                    -hg.waterline[waterline_index])/np.tan( stern_slope_angle[run] )))
                    *transom_halflength)
                    # find waterplane coefficient
                    hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                    /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                    -hg.waterline_stern[waterline_index])))
                    # find centre of area (from aft)
                    # INCOMPLETE
                else:
                    # propulsors[run] == 2 or there is an ERROR
                    # transom goes to line that starts/end above propellers
                    transom_halflength = ((( 1+disc_clear_of_diameter[run] )
                    *hg.prop_diameter/2 )+( ( transom_of_beam[run]*hg.beam[run]/2 )
                    -(( 1+disc_clear_of_diameter[run] )*hg.prop_diameter/2 ) )
                    *(( prop_point-stern_point )
                    -(( depth[run]-transom_stern_height[run]
                    -hg.waterline[waterline_index])/np.tan( stern_slope_angle[run] )))
                    /( prop_point-stern_point ))
                    hg.waterline_area[waterline_index] = (2
                    *areacoshcurve(( hg.waterline_bow[waterline_index]
                    -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                    +2*( pmb_fwd_point[waterline_index]
                    -pmb_aft_point[waterline_index] )
                    *hg.waterline_halfbeam[waterline_index]
                    +2*areacoshcurve(( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] ),( hg.waterline_halfbeam[waterline_index]
                    -transom_halflength ),m )
                    +2*(( prop_point-stern_point )-(( depth[run]
                    -transom_stern_height[run]
                    -hg.waterline[waterline_index])/np.tan( stern_slope_angle[run] )))
                    *transom_halflength)
                    # find waterplane coefficient
                    hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                    /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                    -hg.waterline_stern[waterline_index])))
                    # find centre of area (from aft)
                    # INCOMPLETE
            elif hg.waterline[waterline_index] >= (( 0.5+keel_tip_clear_of_diameter[run] )*hg.prop_diameter ):
                # waterline is between stern slope and top of propeller
                hg.waterline_stern[waterline_index] = prop_point
                # find area of waterline = fwd area + pmb area + aft area
                # assumes that transom length at waterline is a point (for 1 propeller)
                # or a line (for 2 propellers)
                # m varies with draught to blend upper hull lines in to keel lines,
                # given by the equation:
                new_m = ( 0.1 + ( m-0.1 )*( hg.waterline[waterline_index]
                -(( 0.5+keel_tip_clear_of_diameter[run] )*hg.prop_diameter ))
                /(( 0.5+hull_tip_clear_of_diameter[run] )*hg.prop_diameter ))
                if propulsors[run] == 1:
                    # find waterline area for a single propeller
                    hg.waterline_area[waterline_index] = (2
                    *areacoshcurve(( hg.waterline_bow[waterline_index]
                    -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                    +2*( pmb_fwd_point[waterline_index]
                    -pmb_aft_point[waterline_index] )*hg.waterline_halfbeam[waterline_index]
                    +2*areacoshcurve(( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] ),( hg.waterline_halfbeam[waterline_index] ),new_m ))
                    # find waterplane coefficient
                    hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                    /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                    -hg.waterline_stern[waterline_index])))
                    # find centre of area (from aft)
                    # INCOMPLETE
                else:
                    # propulsors[run] == 2 or there is an ERROR
                    # find waterline area for two propellers
                    # the area between the propellers (shown on the last line) is
                    # assumed to be given by a cosh curve given by 3 x new_m (or 5 if
                    # new_m is larger than 5)
                    if new_m < 5:
                        new_new_m = 3*new_m
                    else:
                        # because m cannot be larger than 5
                        new_m = 5
                    hg.waterline_area[waterline_index] = (2
                    *areacoshcurve(( hg.waterline_bow[waterline_index]
                    -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                    +2*( pmb_fwd_point[waterline_index]
                    -pmb_aft_point[waterline_index] )*hg.waterline_halfbeam[waterline_index]
                    +2*areacoshcurve(( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] ),( hg.waterline_halfbeam[waterline_index]
                    -(( 1+disc_clear_of_diameter[run] )*hg.prop_diameter/2 )),new_m )
                    +2*areacoshcurve(( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] ),(( 1+disc_clear_of_diameter[run] )
                    *hg.prop_diameter/2 ),new_new_m ))
                    # find waterplane coefficient
                    hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                    /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                    -hg.waterline_stern[waterline_index])))
                    # find centre of area (from aft)
                    # INCOMPLETE
            else:
                # waterline is below centre of propeller, on curved surface between
                # this and the keel, longitudinal position is given by a cosh curve
                # with the "pointed" end at the propeller
                hg.waterline_stern[waterline_index] = (aftercutup_point
                -(( aftercutup_point-prop_point )
                *inversecoshcurve(( ( 0.5*hg.prop_diameter
                +keel_tip_clear_of_diameter[run]-hg.waterline[waterline_index] )
                /( 0.5*hg.prop_diameter+keel_tip_clear_of_diameter[run] ) ),m )))
                # find area of waterline = fwd area + pmb area + aft area
                # at this point a straight line is used to join the hg.waterline_stern
                # point or 2 points (for 2 propellers) to the pmb_aft_point
                if propulsors[run] == 1:
                    # find waterline area for a single propeller
                    hg.waterline_area[waterline_index] = (2
                    *areacoshcurve(( hg.waterline_bow[waterline_index]
                    -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                    +2*( pmb_fwd_point[waterline_index]
                    -pmb_aft_point[waterline_index] )*hg.waterline_halfbeam[waterline_index]
                    +2*( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] )*hg.waterline_halfbeam[waterline_index]/2)
                    # find waterplane coefficient
                    hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                    /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                    -hg.waterline_stern[waterline_index])))
                    # find centre of area (from aft)
                    # IN WORK
                    # IN WORK
                else:
                    # propulsors[run] == 2 or there is an ERROR
                    # find waterline area for two propellers
                    hg.waterline_area[waterline_index] = (2
                    *areacoshcurve(( hg.waterline_bow[waterline_index]
                    -pmb_fwd_point[waterline_index] ),hg.waterline_halfbeam[waterline_index],m )
                    +2*( pmb_fwd_point[waterline_index]
                    -pmb_aft_point[waterline_index] )*hg.waterline_halfbeam[waterline_index]
                    +2*( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] )*( hg.waterline_halfbeam[waterline_index]
                    -(( 1+disc_clear_of_diameter[run] )*hg.prop_diameter/2 ))/2
                    +2*( pmb_aft_point[waterline_index]
                    -hg.waterline_stern[waterline_index] )
                    *(( 1+disc_clear_of_diameter[run] )*hg.prop_diameter/2 )/2)
                    # find waterplane coefficient
                    hg.waterplane_coefficient[waterline_index] = (hg.waterline_area[waterline_index]
                    /(2*hg.waterline_halfbeam[waterline_index]*(hg.waterline_bow[waterline_index]
                    -hg.waterline_stern[waterline_index])))
                    # find centre of area (from aft)
                    # IN WORK
                    # IN WORK
            # find the volume of the calculated hullform
            if waterline_index == 0:
                hg.calculated_volume = [0]
            else:
                # assuming "slices" have vertical sides and using the average area
                # of both sides
                hg.calculated_volume.append(hg.calculated_volume[waterline_index-1]
                                        +((hg.waterline_area[waterline_index-1]
                                        +hg.waterline_area[waterline_index] )/2 )
                                        *( depth[run]/waterline_number[run] ))
                                        # this is saving entire volume up to each
                                        # draught rather than displaced volume
                      
        # find the waterline that is comparable to draught and compare
        # hg.calculated_volume at this waterline to displaced_volume
        for waterline_index in range(waterline_number[run]):
            if hg.waterline[waterline_index] >= hg.draught[run]:
                # assuming linear variation in calculated volumes on either side of
                # draught
                break
            
        # break loop if the hg.calculated_volume meets the displaced_volume
        if hg.calculated_volume[waterline_index] >= hg.displaced_volume[0]:
            break
        # if loop not broken yet and m=5 display message to user, condition not met
        if m==5:
            # ERROR m is 5 and still the hullform cannot be found, it is
            # necessary to modify the parallel midbody
            print("ERROR m is 5 and still the hullform cannot be found")
    return hg

# function to linearly interpolate to find ship parameters corresponding to draught or cargo demand
def operationaldraughtorcargo(run, hg, set_draught_or_displacement,
                              draught_or_displacement_demand, water_density,
                              waterline_number):
    # class for hgop. outputs 
    class hgop:
        pass
    if set_draught_or_displacement == "displacement":
        # model change in displaced volume
        hgop.displaced_volume = draught_or_displacement_demand/water_density
        for waterline_index in range(waterline_number[run]):
            if hgop.displaced_volume >= hg.calculated_volume[waterline_index]:
                # linearly interpolate to find hgop.draught
                hgop.draught = (hg.waterline[waterline_index]
                +(( hg.waterline[waterline_index+1]-hg.waterline[waterline_index] )
                /( hg.calculated_volume[waterline_index+1]-hg.calculated_volume[waterline_index] ))
                *( hgop.displaced_volume-hg.calculated_volume[waterline_index] ))
                # linearly interpolate to fing hgop.beam
                hgop.beam = 2*(hg.waterline_halfbeam[waterline_index]
                +(( hg.waterline_halfbeam[waterline_index+1]-hg.waterline_halfbeam[waterline_index] )
                /( hg.calculated_volume[waterline_index+1]-hg.calculated_volume[waterline_index] ))
                *( hgop.displaced_volume-hg.calculated_volume[waterline_index] ))
                # linearly interpolate to find hgop.waterline_bow
                hgop.waterline_bow = (hg.waterline_bow[waterline_index]
                +(( hg.waterline_bow[waterline_index+1]-hg.waterline_bow[waterline_index] )
                /( hg.calculated_volume[waterline_index+1]-hg.calculated_volume[waterline_index] ))
                *( hgop.displaced_volume-hg.calculated_volume[waterline_index] ))
                # linearly interpolate to find hgop.waterline_stern
                hgop.waterline_stern = (hg.waterline_stern[waterline_index]
                +(( hg.waterline_stern[waterline_index+1]-hg.waterline_stern[waterline_index] )
                /( hg.calculated_volume[waterline_index+1]-hg.calculated_volume[waterline_index] ))
                *( hgop.displaced_volume-hg.calculated_volume[waterline_index] ))
                # linearly interpolate to find hgop.waterplane_coefficient
                hgop.waterplane_coefficient = (hg.waterplane_coefficient[waterline_index]
                +(( hg.waterplane_coefficient[waterline_index+1]-hg.waterplane_coefficient[waterline_index] )
                /( hg.calculated_volume[waterline_index+1]-hg.calculated_volume[waterline_index] ))
                *( hgop.displaced_volume-hg.calculated_volume[waterline_index] ))
    else:
        # model change in draught or there is an ERROR
        hgop.draught = draught_or_displacement_demand
        for waterline_index in range(waterline_number[run]):
            if hgop.draught >= hg.waterline[waterline_index]:
                # linearly interpolate to find hgop.displaced_volume
                hgop.displaced_volume = (hg.calculated_volume[waterline_index]
                +(( hg.calculated_volume[waterline_index+1]-hg.calculated_volume[waterline_index] )
                /( hg.waterline[waterline_index+1]-hg.waterline[waterline_index] ))
                *( hgop.draught-hg.waterline[waterline_index] ))
                # linearly interpolate to fing hgop.beam
                hgop.beam = 2*(hg.waterline_halfbeam[waterline_index]
                +(( hg.waterline_halfbeam[waterline_index+1]-hg.waterline_halfbeam[waterline_index] )
                /( hg.waterline[waterline_index+1]-hg.waterline[waterline_index] ))
                *( hgop.draught-hg.waterline[waterline_index] ))
                # linearly interpolate to find hgop.waterline_bow
                hgop.waterline_bow = (hg.waterline_bow[waterline_index]
                +(( hg.waterline_bow[waterline_index+1]-hg.waterline_bow[waterline_index] )
                /( hg.waterline[waterline_index+1]-hg.waterline[waterline_index] ))
                *( hgop.draught-hg.waterline[waterline_index] ))
                # linearly interpolate to find hgop.waterline_stern
                hgop.waterline_stern = (hg.waterline_stern[waterline_index]
                +(( hg.waterline_stern[waterline_index+1]-hg.waterline_stern[waterline_index] )
                /( hg.waterline[waterline_index+1]-hg.waterline[waterline_index] ))
                *( hgop.draught-hg.waterline[waterline_index] ))
                # linearly interpolate to find hgop.waterplane_coefficient
                hgop.waterplane_coefficient = (hg.waterplane_coefficient[waterline_index]
                +(( hg.waterplane_coefficient[waterline_index+1]-hg.waterplane_coefficient[waterline_index] )
                /( hg.waterline[waterline_index+1]-hg.waterline[waterline_index] ))
                *( hgop.draught-hg.waterline[waterline_index] ))
    return hgop
    
def transversebouyancyandmoment(run, waterline_number, hg, hgop, KG, heel_angle):
    # note that this function does not re-balance the ship according to the
    # new combination of heel angle and buoyancy
    # this is used instead of a look-up table for writing moment
    # find centre of bouyancy from keel
    bouyancy_moment = 0
    for waterline_index in range(waterline_number[run]):
        if waterline_index == 0:
            # move onto first slice
            pass
        elif hgop.draught >= hg.waterline[waterline_index]:
            # calculate bouyancy moment of each slice
            bouyancy_moment = bouyancy_moment + (( hg.waterline[waterline_index-1]+0.5*( hg.waterline[waterline_index]-hg.waterline[waterline_index-1] ))*hg.calculated_volume[waterline_index])
        elif hgop.draught < hg.waterline[waterline_index]:
            # waterline is at this slice (assumes the bouyant volume is a
            # proportion of calculated_volume at specified waterline)
            bouyancy_moment = bouyancy_moment + (( hg.waterline[waterline_index-1]+0.5*( hgop.draught-hg.waterline[waterline_index-1] ))*((hgop.draught-hg.waterline[waterline_index-1])/(hg.waterline[waterline_index]-hg.waterline[waterline_index-1]))*hg.calculated_volume[waterline_index])
        else:
            # waterline is above draught so no bouyancy provided.
            pass
    BK_no_heel_vertical_centroid = bouyancy_moment/hgop.displaced_volume
    
    # find centre of bouyancy due to heel from considering wedges
    for waterline_index in range(waterline_number[run]):
        if hg.waterline[waterline_index] >= ( hgop.draught-np.tan(heel_angle)*hg.waterline_halfbeam[waterline_index] ):
            # take average beam, assuming it is half way between two slices
            intersection_halfbeam = (hg.waterline_halfbeam[waterline_index]+hg.waterline_halfbeam[waterline_index-1] )/2
            intersection_waterline = ( hg.waterline[waterline_index]+hg.waterline[waterline_index-1] )/2
            # volume up to intersection take away triangular volume
            emerged_wedge_volume = (
                (( hgop.displaced_volume - hg.calculated_volume[waterline_index] )+( 0.5*( hg.calculated_volume[waterline_index]-hg.calculated_volume[waterline_index-1])))
                -(((( hg.waterline_area[waterline_index-1]+hg.waterline_area[waterline_index] )/2 )*( hgop.draught - intersection_waterline ))/2)
                )
            # centre of bouyancy assuming the same as right angle triangle
            emerged_wedge_horizontal_centroid = (-2/3)*intersection_halfbeam
            emerged_wedge_vertical_centroid = intersection_waterline+(( 2/3 )*( hgop.draught - intersection_waterline ))
            # break loop when solution found
            break
        
    for waterline_index in range(waterline_number[run]):
        if hg.waterline[waterline_index] >= ( hgop.draught+np.tan(heel_angle)*hg.waterline_halfbeam[waterline_index] ):
            # take average beam, assuming it is half way between two slices
            intersection_halfbeam = (hg.waterline_halfbeam[waterline_index]+hg.waterline_halfbeam[waterline_index-1] )/2
            intersection_waterline = ( hg.waterline[waterline_index]+hg.waterline[waterline_index-1] )/2
            # volume up to intersection take away triangular volume
            immersed_wedge_volume = (
                (( hg.calculated_volume[waterline_index-1] - hgop.displaced_volume )+( 0.5*( hg.calculated_volume[waterline_index]-hg.calculated_volume[waterline_index-1])))
                -(((( hg.waterline_area[waterline_index-1]+hg.waterline_area[waterline_index] )/2 )*( intersection_waterline - hgop.draught ))/2)
                )
            # centre of bouyancy assuming the same as right angle triangle
            immersed_wedge_horizontal_centroid = (2/3)*intersection_halfbeam
            immersed_wedge_vertical_centroid = intersection_waterline-(( 1/3 )*( intersection_waterline - hgop.draught ))
            # break loop when solution found
            break
            
    # find new volume and centre of bouyancy due to heel
    volume_with_heel = hgop.displaced_volume - emerged_wedge_volume + immersed_wedge_volume
    BK_with_heel_horizontal = (0-( emerged_wedge_volume*emerged_wedge_horizontal_centroid ) + (immersed_wedge_volume*immersed_wedge_horizontal_centroid ))/volume_with_heel
    BK_with_heel_vertical = (( hgop.displaced_volume*BK_no_heel_vertical_centroid )-( emerged_wedge_volume*emerged_wedge_vertical_centroid ) + (immersed_wedge_volume*immersed_wedge_vertical_centroid ))/volume_with_heel
    # find GZ and righting moment
    GZ = ((BK_with_heel_horizontal-0)-(( KG-BK_with_heel_vertical )*np.tan( heel_angle )))*np.cos(heel_angle)
    righting_moment = GZ*hgop.displaced_volume
    return GZ, righting_moment
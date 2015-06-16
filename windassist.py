# Authors: Ben (Strathclyde)
# Version: 1
# History:
# None

# Description:
# This file contains ...

# Assumptions:
# Assuming steady motion, assuming straight line course
# wetted area of hull (Holtrop-Mennen 1982 approximation) used in resistance model (see "stillwaterresistance.py")
# S=L*(2*T+B)*np.sqrt(Cm)*(0.453+0.4425*Cb-0.2862*Cm-0.003467*(B/T)+0.3696*Cwp)+2.38*ABT/Cb

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

def sail(design_condition, speed, wetted_surface_area, true_wind_speed,
         true_wind_direction, heel_righting_moment, available_deck_length,
         beam, hull_depth, draught, displacement_m3, Cb):
    
    
# BEN TO CHECK:
# waterline_length or overall_length??
  # no rudder characteristics
    
    # COPY wetted_surface_area CALCULATION HERE SO BEN KNOWS WHAT YOU ARE USING
    
    # explanation of input variables:
    # design_condition (switch) - 1 or 0, used to check if model has been called to evaluate design or operational condition
    # speed (knots) - this is speed in design condition or current operational condition, note that this is a speed demand and may not always be achievable
    # true_wind_speed (knots) - this is wind speed accounting for the motion of the ship
    # true_wind_direction (degrees) - measured clockwise from the course (not bow/direction of motion of ship which may not be same as heading)
    # heel_writing_moment[heel_angle] (Nm) - the heel_angle (deg) is given as a function of the heel_righting_moment (Nm) (from 0 degrees heel to 30 degrees), in increments of 1.
    
    # NOTES
    # This needs to be run to find the design phase of the sail.  We need to
    # do this for real time voyage and for "average wind conditions".  For
    # average wind conditions the inner loop can be precalculated to save time.
    
        
    # In the design phase it is necessary to specify how sail is used and this
    # call of the wind function can also be used to precalculate variables.
    
    # BENS CODE HERE
    
    
    # BENS CODE HERE
    
    sail_thrust = 0 # (kN) - sail thrust in direction of ship
    added_sail_resistance = 0 # (kN) - (added resistance due to sails) equivalent resistance in direction of ship due to heel, side force, rudder angle, etc.
    x_position_of_sails = 0
    length_of_sails = 0
    mass = 0
    x_centroid_mass = 0
    through_life_cost = 0
    unit_purchase_cost = 0
    
    return sail_thrust, added_sail_resistance, x_position_of_sails, length_of_sails, mass, x_centroid_mass, through_life_cost, unit_purchase_cost
    
    # Questions for Ben:
    # speed may not be needed, depends if this changes how sail is designed
    # Heading not required because it is assumed that a straight line course is
    # maintained rudder correction may be required to keep course with because
    # model is steady state don't use ships heading
    # what fidelity do you think for heel angle is 1 degree increments okay?
    # if it is this could be index value
    # available_deck_length and beam are for sizing, previous model used
    # available deck area, but length may be more appropriate for sails
    # USER INTERFACE SELECTION OF SAIL TYPE, ETC. why not enter lift and drag coefficients?
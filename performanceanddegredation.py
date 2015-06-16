# Authors: Ruihua Lu and Charlotte Banks (Strathclyde)
# Version: 1
# History:
# None

# Description:
# This file contains the engine degredation model/fouling model and added
# resistance model developed by Strathclyde University

# Assumptions:
# The added resistance can be represented as an additional resistance or as a
# speed loss - for a speed loss it is assumed that the power demand is
# calculated by using the demanded speed + speed loss.
# Does not use strip theory

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

def addedresisance(design_condition, displaced_mass, water_density, draught, Cb, waterline_length, speed, beaufort_number, apparent_wave_direction):
        
    # explanation of input variables:
    # design_condition - 1 or 0, used to check if model has been called to evaluate design or operational condition
    # displaced_mass
    # Cb - block coefficient
    # waterline_length - this is the waterline length in current design or operational condition
    # speed (knots) - this is speed in design condition or current operational condition
    # beaufort_number
    # relative_wave_direction (in degrees, waves head on to the ship are at 0 degrees)
    
    # calculate Foude number:
    Fn = speed/np.sqrt(9.807*waterline_length)
    
    # Do not calculate anything in the design stage
    if (design_condition == 1):
        added_resistance = 0
        speed_loss = 0
    else:
        # initial values (if new values are not populated in program or added
        # resistance is not calculated):
        added_resistance = 0
        speed_loss = 0
        
        # RUIHUA'S CODE HERE
        
        # displaced_mass YES
        # Do you need seawater_density? DOESNT MATTER
        # What hull form are you assuming most added resistance methods are based
        # on strip theory? NO ASSUMPTIONS
        
        # RUIHUA'S CODE HERE
    
    return added_resistance, speed_loss
#
#def surfacedegradationandfouling(still_water_resistance
#
#
#
#
#1_plus_k, beaufort_number, draught,
#                                 life_of_ship, dry_dock_inteval,
#                                 investment_period):
#    
#    
#    
#    dry dock inteval in months.
#    1_plus_k for each condition
#    
#    charlotte can do added resistance too.
#    may need wakefaction, thrust_deduction and form parametrts
#    assumption in how added resistance is removed from overall increase in resistance from sea trials.
#    
#    do not link to investment period.
#    
#    # Add to Interface:
#    #    Rmax for specified maintenance activity.
#    # ballast and laden does not matter for delta Cf.
#    
#    
#    
#    
#    
#    
#    
#    
#    # Add to user interface
#    # Assumptions
#    # cannot split between hull and propeller
#    # cannot pick up speed influence in terms of time at slower speeds.
#    
#    high medium low
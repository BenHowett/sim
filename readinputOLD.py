# Author: John Calleya (UCL)
# Version: 1.0
# History:
# None

# Description:
# This reads in the operating profile and other data from the user specified
# directorys

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

def operatingprofile(design_speed, design_draught, design_cargo_capacity,
                     profile_location_1, profile_location_2,
                     profile_location_3, profile_location_4,
                     profile_location_5, profile_cargo_or_draught_1,
                     profile_cargo_or_draught_2, profile_cargo_or_draught_3,
                     profile_cargo_or_draught_4, profile_cargo_or_draught_5):
    # Notes:
    # - Need to change operating profile to be divided by design_speed (not - and / by design_speed)
    
    # format of operating profile
    # (speed/design_speed) in knots | (draught/design_draught) in m | (fractional_period) in %
    # (note that the order does not matter, only the columns)
    
    # check to see if operating profile data has been populated, this will
    # ignore any operating profile in the user interface where the
    # draught/cargo field has not been populated
    
    # this switch is used in "main.py" to tell which operating profiles
    # have been selected
    op_switch=np.zeros(5)
    
    if profile_cargo_or_draught_1 == "draught":
        # read in CSV files containing data and save to numpy array
        operating_profile_1=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_1[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[0]=1
        # multiply draught by design draught
        operating_profile_1[:,1] = (operating_profile_1[:,1]+design_draught)*design_draught
    elif profile_cargo_or_draught_1 == "cargo":
        # read in CSV files containing data and save to numpy array
        operating_profile_1=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_1[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[0]=1
        # multiply cargo by design cargo
        operating_profile_1[:,1] = (operating_profile_1[:,1]+design_cargo_capacity)*design_cargo_capacity
    else:
        # profile_cargo_or_draught_1 has not been populated according to user
        # or there is an ERROR
        pass
    if profile_cargo_or_draught_2 == "draught":
        # read in CSV files containing data and save to numpy array
        operating_profile_2=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_2[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[1]=1
        # multiply draught by design draught
        operating_profile_2[:,1] = (operating_profile_2[:,1]+design_draught)*design_draught
    elif profile_cargo_or_draught_2 == "cargo":
        # read in CSV files containing data and save to numpy array
        operating_profile_2=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_2[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[1]=1
        # multiply cargo by design cargo
        operating_profile_2[:,1] = (operating_profile_2[:,1]+design_cargo_capacity)*design_cargo_capacity
    else:
        # profile_cargo_or_draught_1 has not been populated according to user
        # or there is an ERROR
        pass
    if profile_cargo_or_draught_3 == "draught":
        # read in CSV files containing data and save to numpy array
        operating_profile_3=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_3[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[2]=1
        # multiply draught by design draught
        operating_profile_3[:,1] = (operating_profile_3[:,1]+design_draught)*design_draught
    elif profile_cargo_or_draught_3 == "cargo":
        # read in CSV files containing data and save to numpy array
        operating_profile_3=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_3[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[2]=1
        # multiply draught by design cargo
        operating_profile_3[:,1] = (operating_profile_3[:,1]+design_cargo_capacity)*design_cargo_capacity
    else:
        # profile_cargo_or_draught_1 has not been populated according to user
        # or there is an ERROR
        pass
    if profile_cargo_or_draught_4 == "draught":
        # read in CSV files containing data and save to numpy array
        operating_profile_4=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_4[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[3]=1
        # multiply draught by design draught
        operating_profile_4[:,1] = (operating_profile_4[:,1]+design_draught)*design_draught
    elif profile_cargo_or_draught_4 == "cargo":
        # read in CSV files containing data and save to numpy array
        operating_profile_4=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_4[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[3]=1
        # multiply draught by design cargo
        operating_profile_4[:,1] = (operating_profile_4[:,1]+design_cargo_capacity)*design_cargo_capacity
    else:
        # profile_cargo_or_draught_1 has not been populated according to user
        # or there is an ERROR
        pass
    if profile_cargo_or_draught_5 == "draught":
        # read in CSV files containing data and save to numpy array
        operating_profile_5=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_5[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[4]=1
        # multiply draught by design draught
        operating_profile_5[:,1] = (operating_profile_5[:,1]+design_draught)*design_draught
    elif profile_cargo_or_draught_5 == "cargo":
        # read in CSV files containing data and save to numpy array
        operating_profile_5=np.genfromtxt(profile_location_1, delimiter=',')
        # multiply speed by design speed
        operating_profile_5[:,0] = (operating_profile_1[:,0]+design_speed)*design_speed
        # set switch to show operating profile is being used
        op_switch[4]=1
        # multiply draught by design cargo
        operating_profile_5[:,1] = (operating_profile_5[:,1]+design_cargo_capacity)*design_cargo_capacity
    else:
        # profile_cargo_or_draught_1 has not been populated according to user
        # or there is an ERROR
        pass
    
    # class to save output operating profiles to because they may vary
    class operating_profiles:
        pass
    if operating_profile_1 in locals():
        operating_profiles.op_1=operating_profile_1
    if operating_profile_2 in locals():
        operating_profiles.op_2=operating_profile_2    
    if operating_profile_3 in locals():
        operating_profiles.op_3=operating_profile_3
    if operating_profile_4 in locals():
        operating_profiles.op_4=operating_profile_4
    if operating_profile_5 in locals():
        operating_profiles.op_5=operating_profile_5
    
    return operating_profiles, op_switch
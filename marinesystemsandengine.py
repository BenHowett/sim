# Authors: David Trodden (Newcastle)
# Version: 1
# History:
# None

# Description:
# This file selects and provides performance characteristics of engines.
# Engines can be used with CPP, FPP or for power generation.

# Assumptions:
# RPM is provided from gearbox (if installed) and propeller model.
# fuel type can be different for

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

def engines(design_condition, propulsion_fuel_type, sea_margin, engine_margin,
            propulsion_type, no_of_shafts, design_power, design_rpm,
            operation_power, operation_rpm, light_running_factor,
            shaft_motor_power, auxiliary_fuel_type, maximum_auxiliary_load,
            design_auxiliary_load, operation_auxiliary_load):
    
    # explanation of input variables:
    # design_condition (switch) - 1 or 0, used to check if model has been called to evaluate design or operational condition
    # propulsion_fuel_type (switch) - this is an array with 0 or 1, next to each fuel, operation for multiple fuels is de, a different fuel can be demanded in different periods of operation
    # sea_margin
    # engine_margin
    # sea_margin = 15 # [%] Extra power on top of that required for calm water propulsion. This yields the Service Propulsion Point (SP).
    # engine_margin = 10 # [%] Extra power on top of that required for (SP). This yields Maximum Continuous Rated Power (MCR).
    # light_running_factor = 0 # [%] Extra revolutions required to account for fouling of hull. This yields the light propeller curve (trials conditions).
    # propulsion_type - "fixed pitch propeller", "controllable pitch propeller", "pod (or thruster)" and "water jet"
    # no_of_shafts
    # design_power (kW) - this is for multiple engines (if applicable)
    # design_rpm (rpm) - this is for multiple engines (if applicable)
    # operation_power (kW) - this is the power reqiored at the engine for multiple engines (if applicable)
    # operation_rpm (rpm) - this is for multiple engines (if applicable)
    # light_running_factor - this does not necessarily need to be stated, as sensible default value is given - this accounts during the engine selection process for the hull/screw getting fowled
    # shaft_motor_power (kW) - design condition, will give maximum shaft power, 0 is not fitted, + is shaft motor (power take off), - is shaft generator (power take in)
    # auxiliary_fuel_type (switch) - this is an array with 0 or 1, next to each fuel, operation for multiple fuels is de, a different fuel can be demanded in different periods of operation
    # maximum_auxiliary_load - this is the maximum required load (extra power needed for heating or refridgeration can go here), this may require additional generators to turn on and can be used as a margin to have additional engines for maintenance reasons
    # design_auxiliary_load - this represents the normal operating or maximum load that is required instantaneously
    # operation auxiliary load
    
    # outputs:
    # calculated variables related to the propulsion engine should be a
    # function of operation_power and operation_rpm.
    # calculated variables related to the auxiliary engine should be a function
    # should be a function of engine_power
    # this would allow, after the design proces, a look-up table to be saved
    # and loaded in operational loops in order to decrease the time that the
    # program takes to run
    # care should be taken to ensure shaft generator and motor assumptions are
    # consistent with "main.py"
    installed_main_engine_power = design_power*((100+sea_margin)/100)*((100+engine_margin)/100) # (kW)
    main_engine_sfc = 173 # (g/kWh)
    main_engine_co2_factor = 0 # ratio between tonnes of CO2 emissions to tonnes of fuel
    main_engine_sox_factor = 0 # ratio between tonnes of CO2 emissions to tonnes of fuel
    main_engine_nox_factor = 0 # ratio between tonnes of CO2 emissions to tonnes of fuel
    main_engine_mass = 0 # (kg)
    main_engine_length = 0 # (m)
    no_of_auxiliary_engines = 0
    installed_auxiliary_engine_power = 00 # (kW)
    auxiliary_engine_sfc = 190 # (g/kWh)
    auxiliary_engine_co2_factor = 0 # ratio between tonnes of CO2 emissions to tonnes of fuel
    auxiliary_engine_sox_factor = 0 # ratio between tonnes of CO2 emissions to tonnes of fuel
    auxiliary_engine_nox_factor = 0 # ratio between tonnes of CO2 emissions to tonnes of fuel
    auxiliary_engine_mass = 0 # (kg)
    auxiliary_engine_length = 0 # (m)
    auxiliary_engine_set_point = 0
    
    
    
    return installed_main_engine_power, main_engine_sfc, main_engine_co2_factor, main_engine_sox_factor, main_engine_nox_factor, main_engine_mass, main_engine_length, no_of_auxiliary_engines, installed_auxiliary_engine_power, auxiliary_engine_sfc, auxiliary_engine_co2_factor, auxiliary_engine_sox_factor, auxiliary_engine_nox_factor, auxiliary_engine_mass, auxiliary_engine_length, auxiliary_engine_set_point

# Questions/Changes:
# On engine CO2, what is the difference between what you are doing and
# multiplying by IMO emission factors, is it okay to set CO2 factor using IMO
# numbers?
# Is engine power simply Torque x (Speed/60)?
# Changed Torque to Engine Power
# Generator Set Point should be returned, surely this is selected to give the highest efficiency based on loading conditions and a suitable margin
# Hotel normally to support crew is included within Auxiliaries
# haven't incorporated AC versus DC, it is not worth getting into detail, you
# could gain a small effieicy increase for electric propulsion but easy to
# represent as % change.
# for multiple engines I think it is safe to asume that all the engines are the same size.
# when selecting set ratings from manufacturers there are discreet engine ratings, will these be captured? do they need to be captured?
# individual engines are represented by charateristics all engines assumed same size is this okay?
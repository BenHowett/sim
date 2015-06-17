# SHIP IMPACT MODEL VERSION 4
# Author: John Calleya (UCL)
# Version: 1.01
# History:
# Version 1.0 does not fully work but links functions functions from different
# universities

# Description:
# The main structure of the model is contained in main.py, which is called by
# the user interface contained in inputdata.py

# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

# switches and variables that are not currently in user interface
# THESE NEED TO BE A FUNCTION OF THE RUN
# NOTE THAT SOME OF THESE ARE NOT CONNECTED TO ANYTHING YET!!!
# BITS THAT HAVE TO BE CHANGED TO BE ADDED TO USER INTERFACE ARE NOT INCLUDED IN "IN WORK"
# ADDED TO INTERFACE
water_density = 1.024 # may make this into modifiable value and add to hull generation tab
propeller_design_speed = 0 # rpm, set to 0 for 2-stroke engine, this means same speed as engine

sea_margin = 15 # REPLACE POWERING MARGIN [%] Extra power on top of that required for calm water propulsion. This yields the Service Propulsion Point (SP).
engine_margin = 10 # REPLACE POWERING MARGIN [%] Extra power on top of that required for (SP). This yields Maximum Continuous Rated Power (MCR).
light_running_factor = 0 # [%] Extra revolutions required to account for fouling of hull. This yields the light propeller curve (trials conditions).
engine_design_rpm = 90
redundant_auxiliary_engines = 1
include_shaft_generator_in_design_phase = 1 # can be 0 so that the shaft generator is sized but does not consider that it may not be used at design speed
include_whr_in_design_phase = 1 # can be 0 so that the waste heat recovery plant is not used at the design speed in the design process
whr_prioritise_power_demand = 0 # normally waste heat recovery will be used to meet heat demands first but this can be overidden
whr_plant_energy_type_output = "None" # can be "None", "Heat" or "Electrical and Heat"
transmission_efficiency = 99 # might be difference between diesel electric?
CPP = 0.98 # correction from FPP for using CPP instead of FPP
pod_correction = 0.97 # correction from FPP for using CPP or FPP pod, taken from pages 367 and 368 of Ship Resistance and Propulsion, 3% decrease in propeller efficiency due to increase in boss diameter
available_deck_length = 0 # for sails
# ADDED TO INTERFACE

# new
effective_height_of_cargo_stored_on_deck = 0 # cargo is assumed homogeneous so this includes any change in cargo density of the cargo "on deck" compared in the hullform.

# for charlotte
#engine_degradation_per_year_sfoc =
#engine_maintenance_interval = engine hours.
# for charlotte
# new

# change primary and secondary density multiplier to hull and superstructure!!!


def main(fuel,rd,number_of_runs):
    # class for design variables
    class design:
        pass
    # class for design and technology changes
    class modifiers:
        pass
    # class for wind and weather data
    class wwd:
        pass
    # class for design hull generation variables
    class designhg:
        pass
    # class for operation variables
    class operation:
        pass
    # set array length using numpy arrays for information that is saved
    designhg.prop_diameter = np.zeros(number_of_runs)
    # IN WORK - MORE DESIGNHG PARAMETERS TO GO HERE
    # IN WORK - MORE DESIGNHG PARAMETERS TO GO HERE    
    # GZ = np.zeros(number_of_runs)
    design.displacement = np.zeros(number_of_runs)
    design.lightweight = np.zeros(number_of_runs)
    design.kg = np.zeros(number_of_runs)
    design.displaced_volume = np.zeros(number_of_runs)
    design.draught = np.zeros(number_of_runs)
    design.beam = np.zeros(number_of_runs)
    design.waterline_length = np.zeros(number_of_runs)
    design.waterplane_coefficient = np.zeros(number_of_runs)
    design.fouling_allowance = np.zeros(number_of_runs)
    modifiers.additional_resistance = np.zeros(number_of_runs)
    design.wetted_surface_area = np.zeros(number_of_runs)
    design.viscous_resistance = np.zeros(number_of_runs)
    design.beaufort_number[run] = np.zeros(number_of_runs)
    design.apparent_wave_direction[run] = np.zeros(number_of_runs)
    design.true_wind_speed = np.zeros(number_of_runs)
    design.true_wind_direction = np.zeros(number_of_runs)
    design.added_resistance = np.zeros(number_of_runs)
    design.total_resistance = np.zeros(number_of_runs)
    design.speed_loss = np.zeros(number_of_runs)
    modifiers.propulsion_efficiency = np.zeros(number_of_runs)
    design.propulsion_coefficient = np.zeros(number_of_runs)
    design.prop_open_water_efficiency = np.zeros(number_of_runs)
    design.recovered_heat = np.zeros(number_of_runs)
    design.recovered_electricity = np.zeros(number_of_runs)
    design.auxiliary_energy = np.zeros(number_of_runs)
    design.heat_energy = np.zeros(number_of_runs)
    design.shaft_motor_power = np.zeros(number_of_runs)
    design.shaft_power = np.zeros(number_of_runs)
    design.engine_design_rating = np.zeros(number_of_runs)
    wwd.beaufort_number[run] = np.zeros(number_of_runs)
    wwd.apparent_wave_direction[run] = np.zeros(number_of_runs)
    wwd.true_wind_speed = np.zeros(number_of_runs)
    wwd.true_wind_direction = np.zeros(number_of_runs)
    # import required external files before loops (only needs to be done once)
    import hullgenerator
    import weightspace
    import stillwaterresistance
    import performanceanddegredation
    import propulsor
    import windassist
    import marinesystemsandengine
    for run in range(number_of_runs):
        # initial values of variables before design iteration
        # for each run the user wishes to investigate
        # assume a payload deadweight fraction for first iteration of 0.5, this
        # is to allow for initial calculation of beam or draught
        design.displacement[run] = ((rd.cargo_capacity_te[run]
                            *rd.cargo_utilisation_in_design[run])/0.5)
        # run hullgenerator.py with initial displacement estimate
        # note that the hull generator will also calculate the beam or draught,
        # given the design.displacement
        designhg = hullgenerator.generatehull(run, design.displacement, water_density,
            rd.waterline_number, rd.set_beam_or_draught, rd.beam_or_draught,
            rd.block_coefficient, rd.waterline_length, rd.depth_of_draught,
            rd.midship_coefficient, rd.overall_length, rd.flare_angle,
            rd.deadrise_angle, rd.bow_angle, rd.pmb_angle,
            rd.stern_slope_angle, rd.stern_point_of_waterline,
            rd.prop_point_of_waterline, rd.transom_of_beam, rd.propulsors,
            rd.hull_tip_clear_of_diameter, rd.keel_tip_clear_of_diameter,
            rd.disc_clear_of_diameter, rd.pmb_fwd_of_waterline,
            rd.pmb_aft_of_waterline, rd.waterline_and_transom_overlap,
            rd.aftercutup_of_waterline)
        # IN WORK - LIST VARIABLES THAT ARE OUTPUT FROM DESIGNHG HERE
        # IN WORK - LIST VARIABLES THAT ARE OUTPUT FROM DESIGNHG HERE
        for iteration in range(2):
            # carry out lightweight and kg estimation contained in
            # weightspace.py, this will give a design.displacement estimate
            design.lightweight[run] = weightspace.lightweight(rd.waterline_length[run], rd.cargo_type[run], rd.cargo_capacity_te[run], rd.cargo_capacity_m3[run], designhg.beam[run], designhg.draught[run], rd.block_coefficient[run], water_density)
            # Account for structural weight modifier
            # IN WORK NEED TO SEPARATE SUPERSTRUCTURE WEIGHT FROM HULL IN LIGHWEIGHT
            # data.primary_structure_density_multiplier
            # data.secondary_structure_density_multiplier
            # IN WORK NEED TO SEPARATE SUPERSTRUCTURE WEIGHT FROM HULL IN LIGHWEIGHT
            # KG and changes to weight and volume in weightspace.py
            # IN WORK - ASSUME INITIAL KG VALUE
            design.kg[run] = 13.6 # TEMPORARY KG ESTIMATE for oil tanker VLCC and container ship need a better estimate for this
            print(design.lightweight[run])
            # IN WORK - ASSUME INITIAL KG VALUE
            # find new design.displacement based on design or operating cargo load
            design.displacement[run] =(design.lightweight[run]+rd.cargo_capacity_te[run]
                                *rd.cargo_utilisation_in_design[run])
            # re-generate hull form based on calculated design.displacement
            designhg = hullgenerator.generatehull(run, design.displacement,
                water_density, rd.waterline_number, rd.set_beam_or_draught,
                rd.beam_or_draught, rd.block_coefficient, rd.waterline_length,
                rd.depth_of_draught, rd.midship_coefficient, rd.overall_length,
                rd.flare_angle, rd.deadrise_angle, rd.bow_angle, rd.pmb_angle,
                rd.stern_slope_angle, rd.stern_point_of_waterline,
                rd.prop_point_of_waterline, rd.transom_of_beam, rd.propulsors,
                rd.hull_tip_clear_of_diameter, rd.keel_tip_clear_of_diameter,
                rd.disc_clear_of_diameter, rd.pmb_fwd_of_waterline,
                rd.pmb_aft_of_waterline, rd.waterline_and_transom_overlap,
                rd.aftercutup_of_waterline)
            # find design condition operational characteristics
            # the design condition is found according to the specified "displacement"
            design.beam[run], design.displaced_volume[run], design.draught[run], design.waterline_bow[run], design.waterline_stern[run], design.waterplane_coefficient[run] = hullgenerator.operationaldraughtorcargo(run, designhg, "displacement",
                                                                                                                                                                            design.displacement[run], water_density,
                                                                                                                                                                            rd.waterline_number)
            # calculate waterline length and other inputs to resistance model
            design.waterline_length[run] = design.waterline_bow[run] - design.waterline_stern[run]
            # IN WORK
            # prismatic coefficient is design value can be better estimated
            LCB = design.waterline_length[run]/2 # LCB is assumed to be L/2
            # IN WORK
            design.fouling_allowance[run] = 1.00 # factor due to fouling
            modifiers.additional_resistance[run] = 0 # this can be used for change in resistance due to sails
            # find resistance in design condition (denoted by 1), accounting for added resistance
            design.wetted_surface_area[run], design.viscous_resistance[run], design.wave_resistance[run], design.correlation_allowance[run], design.appendage_resistance[run], t, w, bar, rre = stillwaterresistance.holtrop(
                1, water_density, (rd.design_speed[run] + design.speed_loss[run]), design.waterline_length[run], design.draught[run], design.beam[run], rd.prismatic_coefficient[run], LCB, design.displacement[run],
                design.waterplane_coefficient[run], rd.midship_coefficient[run], designhg.prop_diameter[run], rd.propulsors[run], rd.propeller_blades[run],
                design.fouling_allowance[run], modifiers.additional_resistance[run])
            # IN WORK - WEATHER ROUTING AND APPARENT WIND AND WAVE FUNCTION CALL HERE
            # consideration of weather in design condition (if any)
            design.beaufort_number[run] = 0
            design.apparent_wave_direction[run] = 0
            design.true_wind_speed[run] = 0 # ABSOLUTE WIND AND WAVE DIRECTON
            design.true_wind_direction[run] = 0 # ABSOLUTE WIND AND WAVE DIRECTON
            # IN WORK - WEATHER ROUTING AND APPARENT WIND AND WAVE FUNCTION CALL HERE
            # find added resistance in design condition
            design.added_resistance[run], design.speed_loss[run] = performanceanddegredation.addedresisance(1,
                        design.displacement[run], water_density, design.draught[run],
                        rd.block_coefficient[run], design.waterline_length[run],
                        rd.design_speed[run], design.beaufort_number[run],
                        design.apparent_wave_direction[run])
            # calculate total resistance
            design.total_resistance[run]=(design.viscous_resistance[run]*design.fouling_allowance[run]+design.wave_resistance[run]+design.correlation_allowance[run]+design.appendage_resistance[run]*design.fouling_allowance[run]+modifiers.additional_resistance[run])+design.added_resistance[run]
            # convert user input into number for propeller model, using
            # efficiency value specified in interface
            if (rd.propulsion_type[run] == "fixed pitch propeller"):
                CPP = 1.00
                pod_correction = 1.00
            elif (rd.propulsion_type[run] == "controllable pitch propeller"):
                CPP = CPP
                pod_correction = 0
            elif (rd.propulsion_type[run] == "(FPP or CPP) pod"):
                CPP = 0
                pod_correction = pod_correction
            else:
                pass
                # ERROR, rd.propulsion_type not populated correctly
            # set propeller operating point in design condition
            # IN WORK
            # assumption for design condition
            engine_operation_rpm = engine_design_rpm
            # IN WORK
            # IN WORK - THIS GIVES INCORRECT RESULTS
            print(designhg.prop_diameter[run])
            design.prop_open_water_efficiency[run], EngTorque, PropThrust, PoverD, nProp = propulsor.wagbpropandgearbox(water_density, 1, CPP, pod_correction, rd.design_speed[run], rd.design_speed[run], design.total_resistance[run], engine_design_rpm, engine_operation_rpm, propeller_design_speed, rd.propulsors[run], w, designhg.prop_diameter[run], bar, rd.propeller_blades[run])
            design.prop_open_water_efficiency[run] = 0.70
            # IN WORK - THIS GIVES INCORRECT RESULTS
            # IN WORK - THIS GIVES INCORRECT RESULTS
            # find righting moment for a heel_angle between 0 and 20 degrees
            righting_moment_array = np.zeros(21)
#            for heel_angle in range(21):
#                # convert heel_angle to radians
#                heel_angle_rad = heel_angle*np.pi/180
#                GZ, righting_moment = hullgenerator.transversebouyancyandmoment(run, rd.waterline_number, designhg, hgop, design.kg, heel_angle_rad)
#                # save to righting_moment_array, where heel_angle is the index            
#                righting_moment_array[heel_angle] = righting_moment
#                if heel_angle == 2:
#                    print(GZ)
#                    print('GZ at 2 degrees is: ' + repr(GZ) + 'm')
            # IN WORK - THIS GIVES INCORRECT RESULTS
            # IN WORK - WIND ASSIST FUNCTION AND TECHNOLOGY INTERACTIONS GO HERE
            sail_thrust, added_sail_resistance, x_position_of_sails, length_of_sails, mass, x_centroid_mass, through_life_cost, unit_purchase_cost = windassist.sail(1, rd.design_speed[run], design.wetted_surface_area[run], true_wind_speed, true_wind_direction,
                                                                                                                                                                     righting_moment_array, available_deck_length, design.beam[run], rd.depth_of_draught[run]*design.draught[run],
                                                                                                                                                                        design.draught[run], design.displaced_volume[run], rd.block_coefficient[run])
            modifiers.propulsion_efficiency[run] = 1.0
            # IN WORK - WIND ASSIST FUNCTION AND TECHNOLOGY INTERACTIONS GO HERE
            # initial esimate of propulsion coefficient
            
            
            # propeller efficiency is ZERO
            #print((1-t)/(1-w))
            #print(rre)
            print(design.prop_open_water_efficiency[run])
            
            #print(effO)
            
            # propeller efficiency is zero
            
            design.propulsion_coefficient[run]=((1-t)/(1-w))*rre*design.prop_open_water_efficiency[run]*(transmission_efficiency/100)*modifiers.propulsion_efficiency[run]
            # initial estimate of shaft power based on rd.design_speed[run]
            design.shaft_power[run]=design.total_resistance[run]*(rd.design_speed[run]*0.51444)/design.propulsion_coefficient[run]
            # check shaft generator requirements
            # 0 is not fitted, + is shaft motor (power take off), - is shaft generator (power take in)
            # assuming the first operating mode is used for the design on the shaft generator
            # initial enigne selection, with the shaft motor power set to 0 and
            # using the given electrical power demand (not considering waste heat
            # recovery)
            marinesystemsandengine.engines(0, rd.profile_main_energy_source_1[run],
                                           sea_margin, engine_margin, rd.propulsion_type[run],
                                           rd.propulsors[run], design.shaft_power[run], engine_design_rpm,
                                           design.shaft_power[run], engine_design_rpm,
                                           light_running_factor, 0,
                                           rd.profile_auxiliary_energy_source_1[run],
                                           rd.maximum_electrical_power_available[run],
                                           rd.profile_electrical_power_demand_1[run],
                                           rd.profile_electrical_power_demand_1[run])
            # size waste heat recovery plant based on user requirement, before
            # considering shaft generator
            if whr_plant_energy_type_output == "Electrical and Heat":
                # IN WORK - CALL WASTE HEATER RECOVERY PLANT FOR GENERATION OF HEAT AND ELECTRICITY
                design.recovered_heat[run] = 0
                design.recovered_electricity[run] = 0
                # IN WORK - CALL WASTE HEATER RECOVERY PLANT FOR GENERATION OF HEAT AND ELECTRICITY
            elif whr_plant_energy_type_output == "Heat":
                # IN WORK - CALL WASTE HEATER RECOVERY PLANT FOR GENERATION OF HEAT
                design.recovered_heat[run] = 0
                design.recovered_electricity[run] = 0
                # IN WORK - CALL WASTE HEATER RECOVERY PLANT FOR GENERATION OF HEAT
            else:
                # whr_plant_energy_type_output == "None", the field is unpopulated,
                # include_whr_in_design_phase == 1 or there is an ERROR
                # IN WORK
                # No WHR plant fitted set recovered heat and electricity to 0
                design.recovered_heat[run] = 0
                design.recovered_electricity[run] = 0
                # IN WORK
            # required heat and auxiliary power accounting for waste heat recovered
            # as specified in the user interface
            # Note that putting heat back on to the shaft is managed through the
            # PTO/PTI
            # the same fuel demands that are in the first populated operating
            # profile are asssumed
            if include_whr_in_design_phase == 1:
                design.auxiliary_energy[run] = rd.profile_electrical_power_demand_1[run]-design.recovered_electricity[run]
                design.heat_energy[run] = rd.profile_heat_power_demand_1[run]-design.recovered_heat[run]
            else:
                # include_whr_in_design_phase == 0 or there is an error
                design.auxiliary_energy[run] = rd.profile_electrical_power_demand_1[run]
                design.heat_energy[run] = rd.profile_heat_power_demand_1[run]
            # set design of shaft generator (no differences have been assumed for
            # single or twin shaft generators)
            if rd.shaft_generator_fitted[run] == 0:
                # shaft generator is not installed
                design.shaft_motor_power[run] = 0
            elif rd.profile_shaft_generator_1[run] == "PTO only":
                # the amount of power provided to cover auxiliary power utilisation
                # is limited by:
                # - fulfilling the auxiliary power requirement
                # - the availiable main engine power (in design phase this is not
                # accounted for because the engine can be sized for use with shaft
                # generator)
                # - the shaft generator size/capacity
                design.shaft_motor_power[run] = (min(+rd.profile_electrical_power_demand_1[run], +rd.shaft_generator_maximum_power[run]))/(rd.shaft_generator_pto_efficiency[run]/100)
            elif rd.profile_shaft_generator_1[run] == "PTI only":
                # the amount of power provided to cover main power utilisation is
                # limited by:
                # - fulfilling the main power requirement
                # - the available auxiliary engine power (in design phase this is
                # not accounted for because the engine can be sized for use with
                # shaft generator)
                # - the shaft generator size/capacity
                design.shaft_motor_power[run] = (min(-design.shaft_power[run], -rd.shaft_generator_maximum_power[run]))/(rd.shaft_generator_pti_efficiency[run]/100)
            elif rd.profile_shaft_generator_1[run] == "PTO/PTI":
                # use PTO when possible, except when engine power is not large
                # enough then use PTI to provide additional engine power
                # engine power is not known at this stage so assume PTO (as above)
                design.shaft_motor_power[run] = (min(+rd.profile_electrical_power_demand_1[run], +rd.shaft_generator_maximum_power[run]))/(rd.shaft_generator_pto_efficiency[run]/100)
            else:
                # field has not been populated or "Not Used has been selected"
                pass
            # required shaft power accounting for PTO/PTI as specified in user
            # interface, this adds to previous wast heat energy
            if include_shaft_generator_in_design_phase == 1:
                design.shaft_power[run] = design.shaft_power[run]+design.shaft_motor_power[run]
                design.auxiliary_energy[run] = design.auxiliary_energy[run]-design.shaft_motor_power[run]
            else:
                # do not change energy use due to PTO/PTI
                pass
                design.shaft_power[run] = design.shaft_power[run]
                design.auxiliary_energy[run] = rd.profile_electrical_power_demand_1[run]
            # same fuel demands that are in the first populated operating profile
            # are asssumed
            # select a new engine given the energy requirements:
            marinesystemsandengine.engines(0, rd.profile_main_energy_source_1[run],
                                           sea_margin, engine_margin, rd.propulsion_type[run],
                                           rd.propulsors[run], design.shaft_power[run], engine_design_rpm,
                                           design.shaft_power[run], engine_design_rpm,
                                           light_running_factor, design.shaft_motor_power[run],
                                           rd.profile_auxiliary_energy_source_1[run],
                                           rd.maximum_electrical_power_available[run],
                                           design.auxiliary_energy[run],
                                           design.auxiliary_energy[run])
        # calculate operational performance for each operating condition
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # read in operational profiles defined in user interface and folder
        import readinput
        # find out which files have been used (assumes cargo capcity, if used
        # is in tonnes)
        operating_profile_1, operating_profile_2, operating_profile_3, operating_profile_4, operating_profile_5, op_switch = readinput.operatingprofile(rd.design_speed[run], design.draught[run],
            (rd.cargo_capacity_te[run]*rd.cargo_utilisation_in_design[run]),
            rd.profile_location_1[run], rd.profile_location_2[run], rd.profile_location_3[run],
            rd.profile_location_4[run], rd.profile_location_5[run],
            rd.profile_cargo_or_draught_1[run], rd.profile_cargo_or_draught_2[run],
            rd.profile_cargo_or_draught_3[run], rd.profile_cargo_or_draught_4[run],
            rd.profile_cargo_or_draught_5[run])
        # carry out operational performance loops based on what operating
        # profiles have ben populated in user interface
        for profile_index in range(5):
            if (op_switch[profile_index]==0):
                # operating profile has not been populated
                pass
            else:
                # operating profile has been populated
                if (profile_index==0):
                    selected_operating_profile = operating_profile_1
                elif (profile_index==1):
                    selected_operating_profile = operating_profile_2
                elif (profile_index==2):
                    selected_operating_profile = operating_profile_3
                elif (profile_index==3):
                    selected_operating_profile = operating_profile_4
                elif (profile_index==4):
                    selected_operating_profile = operating_profile_5
                else:
                    # an unlikely ERROR here somewhere
                    pass
                # examine each draught and speed combination in selected_operating_profile
                for speeds_draughts in range(len(selected_operating_profile)):
                    # find resistance at speed and draught/cargo load specified in operating_profile
                    # speed is given by selected_operating_profile[speed_draughts, 0]
                    selected_profile.speed_dmd[speed_draughts, run] = selected_operating_profile[speed_draughts, 0]
                    # draught or cargo demand is given by selected_operating_profile[speed_draughts, 1]
                    # time in condition is given by selected_operating_profile[speed_draughts, 2]
                    if (op_switch[profile_index]==1):
                        # find ship characteristics of ship given by designhg from "draught" demand
                        selected_profile.beam[speed_draughts, run], selected_profile.displaced_volume[speed_draughts, run], selected_profile.draught[speed_draughts, run], selected_profile.waterline_bow[speed_draughts, run], selected_profile.waterline_stern[speed_draughts, run], selected_profile.waterplane_coefficient[speed_draughts, run] = hullgenerator.operationaldraughtorcargo(run, designhg, "draught",
                                                                                                                                                                                                                                                                selected_operating_profile[speed_draughts, 1], water_density, rd.waterline_number)
                        # find displacement
                        selected_profile.displacement[speed_draughts, run] = (selected_profile.displaced_volume[speed_draughts, run]*water_density)
                        # find resulting cargo load from draught demand
                        selected_profile.cargo_load[speed_draughts, run] = (selected_profile.displacement[speed_draughts, run]
                                                        - design.lightweight[run])
                    elif (op_switch[profile_index]==2):
                        # use cargo load demand given in operating profile
                        selected_profile.cargo_load[speed_draughts, run] = selected_operating_profile[speed_draughts, 1]
                        # find resulting displacement demand from cargo demand
                        selected_profile.displacement[speed_draughts, run] = (selected_profile.cargo_load[speed_draughts, run]
                                                        + design.lightweight[run])
                        # find volume
                        selected_profile.displaced_volume[speed_draughts, run] = selected_profile.displacement[speed_draughts, run]/water_density
                        # find ship characteristics of ship given by designhg from "displacement" demand                        
                        selected_profile.beam[speed_draughts, run], selected_profile.displaced_volume[speed_draughts, run], selected_profile.draught[speed_draughts, run], selected_profile.waterline_bow[speed_draughts, run], selected_profile.waterline_stern[speed_draughts, run], selected_profile.waterplane_coefficient[speed_draughts, run] = hullgenerator.operationaldraughtorcargo(run, designhg, "displacement",
                                                                                                                                                                                                                                                                selected_profile.displaced_volume[speed_draughts, run], water_density, rd.waterline_number)
                    # calculate waterline length and other inputs to resistance model
                    selected_profile.waterline_length[speed_draughts, run] = selected_profile.waterline_bow[speeds_draughts, run] - selected_profile.waterline_stern[speeds_draughts, run]
                    # IN WORK
                    # prismatic coefficient is design value can be better estimated
                    LCB = design.waterline_length[run]/2 # LCB is assumed to be L/2
                    # IN WORK
                    design.fouling_allowance[run] = 1.00 # factor due to fouling
                    modifiers.additional_resistance[run] = 0 # this can be used for change in resistance due to sails
                    # find resistance in design condition (denoted by 1), accounting for added resistance
                    selected_profile.wetted_surface_area[speed_draughts, run], selected_profile.viscous_resistance[speed_draughts, run], selected_profile.wave_resistance[speed_draughts, run], selected_profile.correlation_allowance[speed_draughts, run], selected_profile.appendage_resistance[speed_draughts, run], t, w, bar, rre = stillwaterresistance.holtrop(
                        1, water_density, (selected_profile.speed_dmd[speed_draughts, run] + selected_profile.speed_loss[speed_draughts, run]), selected_profile.waterline_length[speed_draughts, run], selected_profile.draught[speed_draughts, run], selected_profile.beam[speed_draughts, run], rd.prismatic_coefficient[run], LCB, selected_profile.displacement[speed_draughts, run],
                        selected_profile.waterplane_coefficient[speed_draughts, run], rd.midship_coefficient[run], designhg.prop_diameter[run], rd.propulsors[run], rd.propeller_blades[run],
                        design.fouling_allowance[run], modifiers.additional_resistance[run])
                    # IN WORK - WEATHER ROUTING AND APPARENT WIND AND WAVE FUNCTION CALL HERE
                    wwd.beaufort_number[speed_draughts, run] = 0
                    wwd.apparent_wave_direction[speed_draughts, run] = 0
                    wwd.true_wind_speed[speed_draughts, run] = 0 # ABSOLUTE WIND AND WAVE DIRECTON
                    wwd.true_wind_direction[speed_draughts, run] = 0 # ABSOLUTE WIND AND WAVE DIRECTON
                    # IN WORK - WEATHER ROUTING AND APPARENT WIND AND WAVE FUNCTION CALL HERE
                    # find added resistance in design condition
                    selected_profile.added_resistance[speed_draughts, run], selected_profile.speed_loss[speed_draughts, run] = performanceanddegredation.addedresisance(1,
                                selected_profile.displacement[speed_draughts, run], water_density, selected_profile.draught[speed_draughts, run],
                                rd.block_coefficient[run], selected_profile.waterline_length[speed_draughts, run],
                                selected_profile.speed_dmd[speed_draughts, run], wwd.beaufort_number[speed_draughts, run],
                                wwd.apparent_wave_direction[speed_draughts, run])
                    # calculate total resistance
                    selected_profile.total_resistance[speed_draughts, run]=(selected_profile.viscous_resistance[speed_draughts, run]*design.fouling_allowance[run]+selected_profile.wave_resistance[speed_draughts, run]+selected_profile.correlation_allowance[speed_draughts, run]+selected_profile.appendage_resistance[speed_draughts, run]*design.fouling_allowance[run]+modifiers.additional_resistance[run])+selected_profile.added_resistance[run]
                    # IN WORK NOW NEXT
                    #
                    # look up saved engine data for enine operation rpm!
                    # MAY NOT NEED ANOTHER ENGINE CALL?
                    
                    # for now make this assumption
                    engine_operation_rpm = engine_design_rpm
                    # IN WORK NOW NEXT
                    # IN WORK - THIS GIVES INCORRECT RESULTS
                    print(designhg.prop_diameter[run])
                    selected_profile.prop_open_water_efficiency[speed_draughts, run], EngTorque, PropThrust, PoverD, nProp = propulsor.wagbpropandgearbox(water_density, 1, CPP, pod_correction, rd.design_speed[run], rd.design_speed[run], design.total_resistance[run], engine_design_rpm, engine_operation_rpm, propeller_design_speed, rd.propulsors[run], w, designhg.prop_diameter[run], bar, rd.propeller_blades[run])
                    selected_profile.prop_open_water_efficiency[speed_draughts, run] = 0.70
                    # IN WORK - THIS GIVES INCORRECT RESULTS
                    # IN WORK - THIS GIVES INCORRECT RESULTS
                    # find righting moment for a heel_angle between 0 and 20 degrees
                    righting_moment_array = np.zeros(21)
        #            for heel_angle in range(21):
        #                # convert heel_angle to radians
        #                heel_angle_rad = heel_angle*np.pi/180
        #                GZ, righting_moment = hullgenerator.transversebouyancyandmoment(run, rd.waterline_number, designhg, hgop, design.kg, heel_angle_rad)
        #                # save to righting_moment_array, where heel_angle is the index            
        #                righting_moment_array[heel_angle] = righting_moment
        #                if heel_angle == 2:
        #                    print(GZ)
        #                    print('GZ at 2 degrees is: ' + repr(GZ) + 'm')
                    # IN WORK - THIS GIVES INCORRECT RESULTS
                    # IN WORK - WIND ASSIST FUNCTION AND TECHNOLOGY INTERACTIONS GO HERE
                    sail_thrust, added_sail_resistance, x_position_of_sails, length_of_sails, mass, x_centroid_mass, through_life_cost, unit_purchase_cost = windassist.sail(1, rd.design_speed[run], design.wetted_surface_area[run], true_wind_speed, true_wind_direction,
                                                                                                                                                                             righting_moment_array, available_deck_length, design.beam[run], rd.depth_of_draught[run]*design.draught[run],
                                                                                                                                                                                design.draught[run], design.displaced_volume[run], rd.block_coefficient[run])
                    
                    modifiers.propulsion_efficiency[run] = 1.0
                    # IN WORK - WIND ASSIST FUNCTION AND TECHNOLOGY INTERACTIONS GO HERE
                    # initial esimate of propulsion coefficient
                    selected_profile.propulsion_coefficient[speed_draughts, run]=((1-t)/(1-w))*rre*selected_profile.prop_open_water_efficiency[speed_draughts, run]*(transmission_efficiency/100)*modifiers.propulsion_efficiency[run]
                    # initial estimate of shaft power based on rd.design_speed[run]
                    selected_profile.shaft_power[speed_draughts, run]=selected_profile.total_resistance[run]*(selected_profile.speed_dmd[speed_draughts, run]*0.51444)/selected_profile.propulsion_coefficient[speed_draughts, run]
                    # check shaft generator requirements
                    # 0 is not fitted, + is shaft motor (power take off), - is shaft generator (power take in)
                    # assuming the first operating mode is used for the design on the shaft generator
                    # initial enigne selection, with the shaft motor power set to 0 and
                    # using the given electrical power demand (not considering waste heat
                    # recovery)
                    UP TO HERE
                    WHY ARE THERE NOT OUTPUT ARGUMENTS FOR MARINE SYSTEM AND ENGINE???
                    WHAT VARIABLES SHOULD THIS BE LINKED TO DO I HAVE THEM ALREADY??
                    
                    marinesystemsandengine.engines(0, rd.profile_main_energy_source_1[run],
                               sea_margin, engine_margin, rd.propulsion_type[run],
                               rd.propulsors[run], design.shaft_power[run], engine_design_rpm,
                               design.shaft_power[run], engine_design_rpm,
                               light_running_factor, 0,
                               rd.profile_auxiliary_energy_source_1[run],
                               rd.maximum_electrical_power_available[run],
                               rd.profile_electrical_power_demand_1[run],
                               rd.profile_electrical_power_demand_1[run])
                    
                    
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                UP TO HERE
                                SPACE FOR DESIGN WIND CONDITION
                        
                        CREATE NP.ZEROS FOR MULTIPLE DIMENSIONS
                        TWO DIMENSIONS, run and speeds, draughts for variables
                        TEST NP ARRAYS FOR MULTIPLE DIMENSIONS
                        
                        
                        
                        
                        np.zeros((speeddraughts, run))
[speed draugts, run]
                        SAVE AS ABOVE WHEN SAVING BACK TO EACH PROFILE.
                        
                        
                        
                  
                  PRE-SET VARIABLE LENGTHS SIMILAR TO DESIGN CONDITION      
                        
                        
                        CARRY ON ITERATION RUN RESISTANCE MODEL PROPELLER MODEL ETC. AS IN DESIGN
                        
                        add selected_profile pass
                        
                        hgop.draught
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                    
                        
                        
                        
                        
                        

                    
                    
                    
                    
                    
                    # save operational condition
                    if (profile_index==0):
                        # copy the selected_profile class to create a new class
                        class profile_1(selected_profile):
                            pass
                    elif (profile_index==1):
                        # copy the selected_profile class to create a new class
                        class profile_1(selected_profile):
                            pass
                        
                        .
                        
                    profile_1.




profile_1.beam[speeds_draught]
profile_1.cargo_load[speeds_draught]
profile_1.displaced_volume[speeds_draught]
profile_1.displacement[speeds_draught]
profile_1.draught[speeds_draught]
profile_1.waterline_bow[speeds_draught]
profile_1.waterline_length[speeds_draught]
profile_1.waterline_stern[speeds_draught]
profile_1.waterplane_coefficient[speeds_draught]

# NEED ENOUGH VARIABLES TO ANALYSE WHERE ENERGY IS USED.

# COMMON FUEL LIST


design.lightweight
design.total_cost
design.technology_cost
profile_avg_an.cargo_load
profile_avg_an.displaced_volume
profile_avg_an.displacement
profile_avg_an.draught
profile_avg_an.fuel_consumption
profile_avg_an.speed
profile_avg_an.annual_cost
profile_avg_an.annual_technology_cost
profile_avg_an.co2_emissions
profile_avg_an.nox_emissions
profile_avg_an.sox_emissions



            UP TO HERE
                                        else:
                    # an unlikely ERROR here somewhere
                    pass
                        
                    
                

            

                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    UP TO HERE
                # IN WORK
                # np.savetxt('elected_operating_profile.csv', selected_operating_profile, delimiter=',')
                # TO DO:
                # CROSS CHECK elected_operating_profile.csv against input operating profile to see
                # IN WORK
                if operating profile has been modified correctly e.g. last column shouls add up to 1:
                
#                NEED TO FIND AND GO THROUGH THE NUMBER OF ROWS IN ARRAY 
#                
#                
#            
#            
#            same - - - - - - - for design condition calculation
#            
#            
#dd ddddddd d d dd d d d d
#d d d d d d d d d
#        sum(op_switch)
#        
#        d    
#            
            
#            UP TO HERE
            
        # --2nd-Iteration-in-Design--
        # HERE IN WORK
        
        # call equipmentandstructure.py to get new displacement from selected
        # equipment
        
        # HERE IN WORK
        # find design condition operational characteristics according to the
        # newly calculated "displacement"
#        hgop = hullgenerator.operationaldraughtorcargo(run, hg, "displacement",
#                                            displacement[run], water_density,
#                                            rd.waterline_number)
#                                            
#        run resistance model
#        
        # UP TO HERE
        
        # TO DO NEXT:
        
        # import propulsor
        # - RECALCULATE UP TO ENGINE FOR 2nd LOOP
        # - FIX EXISTING PROBLEMS
        # - CARRY OUT OPERATIONAL PERFORMANCE ANALYSIS
        
        
        
        
        
        # HERE IN WORK - PRINT VARIABLES TO CHECK RESULTS
        # displacement is incorrect at the moment
        # print('Displacement: ' + repr(displacement[run]) + 'tonnes')
        print('design.kg: ' + repr(design.kg) + 'metres')
        print('Total Resistance: ' + repr(design.total_resistance[run]) + 'kN')
        print('Shaft Power: ' + repr(design.shaft_power[run]) + 'kW')
        
        
        
        # HERE IN WORK - PRINT VARIABLES TO CHECK RESULTS
                                       
                                       
                                       
# UP TO HERE
                                       
# ROUGH NOTES ARE BELOW
#
#        ENGINE TO ENGINE
#        
#        
#        
#        ACCOUNT FOR SHAFT GENERATOR
#        THEN PROPELLER MODEL USE NUMBER FOR NOW
#        THEN ENGINE MODEL AND MARINE SYSTEM SIZING AGAIN
#        need to ensure im not adding on power change due to whr and shaft each time
#        ADD STUFF TO USER INTERFACE
#        
#        
#        
#        # TO DO NEXT,
#
#        THEN
#        RUN WORK SO FAR
#        
#        ADD PROPELLER NEXT AND SPACE FOR CRT INTERFACE WITH ADDITIONAL
#        LOOP FOR ITERATION.
#        
#        THEN HEAD ON TO OPERATIONAL PERFORMANCE CALCULATION
#        
#        
#        # WHAT DO YOU DO WITH THE BELOW TEXT?
#                nPropDesign = propeller_design_speed # NOT IN INTERFACE YET
#        )
#        
#        engine_power, engine_mass, engine_length,
#        engine_sfc[functionofenginerating]
#        engine_NOx
#        engine_SOx
#        engine_speed
#        
#        = engine(fuel_type, engine_power, engine_torque
#        
#        
#        
#        #            in operational condition also need to available propulsion power for PTO and from engine?? assume that power is available in design condition.
##            add additional item to min formula that is design.shaft_power[run]-design.shaft_power[run])
##            
##            
##            design.shaft_motor_power[run] = -rd.profile_shaft_generator_1
##            
##            
##            
##            
##                    % always use PTO to provide auxiliary power, when possible
##        % the amount of power provided to cover auxiliary power utilisation is limited by: - fulfilling the auxiliary power requirement - the availiable main engine power - the shaft generator size/capacity
##        SelectedShipDesignOperation(9,index,technum,range1,range2)=-min([(SelectedShipDesignOperation(6,index,technum,range1,range2)) (SelectedShipPowering(7,technum,range1,range2)-SelectedShipDesignOperation(3,index,technum,range1,range2)) (SelectedShipPowering(19,technum,range1,range2))])-DesignChSP+ChSP;
##        % minus (-) sign convention denotes power coming from main engine
##        % to auxiliary engine (not considering effiency a this point)
##        % calculate efficiency
##        if ((-SelectedShipDesignOperation(9,index,technum,range1,range2)/SelectedShipPowering(19,technum,range1,range2))<0.5)
##            % linearly interpolate between 0 and 0.5 to find efficiency
##            SelectedShipDesignOperation(10,index,technum,range1,range2)=SelectedShipFuel{4,4,technum}+((SelectedShipFuel{4,3,technum}-SelectedShipFuel{4,4,technum})/(0.5-0.0))*((-SelectedShipDesignOperation(9,index,technum,range1,range2)/SelectedShipPowering(19,technum,range1,range2))-0.0);
##        elseif ((-SelectedShipDesignOperation(9,index,technum,range1,range2)/SelectedShipPowering(19,technum,range1,range2))<1.0)
##            % linearly interpolate between 0.5 and 1.0 to find efficiency
##            SelectedShipDesignOperation(10,index,technum,range1,range2)=SelectedShipFuel{4,3,technum}+((SelectedShipFuel{4,2,technum}-SelectedShipFuel{4,3,technum})/(1.0-0.5))*((-SelectedShipDesignOperation(9,index,technum,range1,range2)/SelectedShipPowering(19,technum,range1,range2))-0.5);
##        else
##            % mistake here somewhere or efficiency is 100%, use 100% load
##            % efficiency value
##            SelectedShipDesignOperation(10,index,technum,range1,range2)=SelectedShipFuel{4,2,technum};
##        end
##        % new main engine power (accounting for calculated efficiency)
##        SelectedShipDesignOperation(3,index,technum,range1,range2)=SelectedShipDesignOperation(3,index,technum,range1,range2)-(SelectedShipDesignOperation(9,index,technum,range1,range2)/(1-SelectedShipDesignOperation(10,index,technum,range1,range2)));
##        % new auxiliary engine power
##        SelectedShipDesignOperation(6,index,technum,range1,range2)=SelectedShipDesignOperation(6,index,technum,range1,range2)+SelectedShipDesignOperation(9,index,technum,range1,range2);
##    elseif (inputship(11)==3);
##        % always use PTI to provide main power, when possible
##        
##        ASSUME DESIGN CONDITION VALUE IS USED.
##        
##        
##        # HERE IN WORK
##        
##        
##        
##        # SORT OUT SHAFT GENERATOR
##       # needs to follow MODE given in operating profile!
##        # needs to pass usage to engine function!!!
##        
##        # SORT OUT HEAT USEAGE, IF NO OTHER MEANS, COMES FROM AUXILIARY ENGINE
##        # SPACE FOR WASTE HEAT RECOVERY PLANT
#        
#        
#        ENGINE DESIGN RPM NEEDS TO LINE UP WITH PROPELLER ASSUMPTIONS
#        
#        
#        
#        
#        
#        
#        
#        
#        # HERE IN WORK
#        # generate operating profile from external file
#        import readinput
#        op_profiles, op_switch = readinput.operatingprofile(rd.design_speed[run],
#                    design.draught[run], rd.cargo_capacity_te[run], rd.profile_location_1[run],
#                    rd.profile_location_2[run], rd.profile_location_3[run], rd.profile_location_4[run],
#                    rd.profile_location_5[run], rd.profile_cargo_or_draught_1[run],
#                    rd.profile_cargo_or_draught_2[run], rd.profile_cargo_or_draught_3[run],
#                    rd.profile_cargo_or_draught_4[run], rd.profile_cargo_or_draught_5[run])
#        # examine up to five operational conditions defined by user
#        for operation in range(5):
#            if op_switch[operation] != 1:
#                pass
#                # operating profile has not been investigated by the user
#            else:
#                # equal to 1 continue
#                # save operation.operating_profile to use in current loop
#                if (operation+1) == 1:
#                    operation.operating_profile = op_profiles.op_1
#                if (operation+1) == 2:
#                    operation.operating_profile = op_profiles.op_2
#                if (operation+1) == 3:
#                    operation.operating_profile = op_profiles.op_3
#                if (operation+1) == 4:
#                    operation.operating_profile = op_profiles.op_4
#                if (operation+1) == 5:
#                    operation.operating_profile = op_profiles.op_5
#                    
#        UP TO HERE
#        
#        GO THROUGH LOOP AGAIN FOR SPEED AND DRAUGHTS DEFINED IN OPERATING PROFILE
#                        
#                        
#        UP TO HERE
#        
#        # NEED TO IGNORE NON-POPULATED OP_1, OP_2, etc.
#        
#        UP TO HERE        
#
#        
#
#        
#
#        TORQUE SHOULD BE OUTPUT FROM PROPELLER MODEL
#        
#        
#        # need to examined what is in Matlab Model, e.g. how engine is loaded
#        # initially for engin speed and how techparameters is used.
#        # IN WORK
#        
#        # calculation required before propeller model
#        # find design condition and operational engine speeds
#        
#        # find engine_design_speed for the assumed engine size and by
#        # considering the powering margin (1-powering margin is engine rating)
#        design.engine_design_rating = (1-(rd.powering_margin/100))
#        if (design.engine_design_rating<=0.25):
#            nDesign=EngSpeedat25MCR
#        elif (design.engine_design_rating<0.50):
#            # linearly interpolate between 0.25 and 0.50
#            nDesign=EngSpeedat25MCR+((EngSpeedat50MCR-EngSpeedat25MCR)*(design.engine_design_rating-0.25)/(0.50-0.25))
#        elif (design.engine_design_rating==0.50):
#            nDesign=EngSpeedat50MCR
#        elif (design.engine_design_rating<0.75):
#            # linearly interpolate between 0.50 and 0.75
#            nDesign=EngSpeedat50MCR+((EngSpeedat75MCR-EngSpeedat50MCR)*(design.engine_design_rating-0.50)/(0.75-0.50))
#        elif (design.engine_design_rating==0.75):
#            nDesign=EngSpeedat75MCR
#        elif (design.engine_design_rating<1.00):
#            # linearly interpolate between 0.75 and 1.00
#            nDesign=EngSpeedat75MCR+((EngSpeedat100MCR-EngSpeedat75MCR)*(design.engine_design_rating-0.75)/(1.00-0.75))
#        else:
#            # (MCR>=1.00)
#            nDesign=EngSpeedat100MCR # cannot exceed 100% MCR
#        # Find Operational Engine Speed (nOperation) by considering design.shaft_power[run]
#        MCR=design.shaft_power[run]/MainEngPower
#        if (MCR<=0.25):
#            nOperation=EngSpeedat25MCR
#        elif (MCR<0.50):
#            # linearly interpolate between 0.25 and 0.50
#            nOperation=EngSpeedat25MCR+((EngSpeedat50MCR-EngSpeedat25MCR)*(MCR-0.25)/(0.50-0.25))
#        elif (MCR==0.50):
#            nOperation=EngSpeedat50MCR
#        elif (MCR<0.75):
#            # linearly interpolate between 0.50 and 0.75
#            nOperation=EngSpeedat50MCR+((EngSpeedat75MCR-EngSpeedat50MCR)*(MCR-0.50)/(0.75-0.50))
#        elif (MCR==0.75):
#            nOperation=EngSpeedat75MCR
#        elif (MCR<1.00):
#            # linearly interpolate between 0.75 and 1.00
#            nOperation=EngSpeedat75MCR+((EngSpeedat100MCR-EngSpeedat75MCR)*(MCR-0.75)/(1.00-0.75))
#        else:
#            # (MCR>=1.00)
#            nOperation=EngSpeedat100MCR # cannot exceed 100% MCR
#        % UP TO HERE
#        
#        
#        
#        nDesign
#        
#        
#        
#        
#        
#        
#        # UP TO HERE
#        
#        
#        # Foul, ChR?
##        
##        I have a outline for a windassist function with the following:
##        INPUTS
##        GZ or Righting Moment as function of heel angle
##        Ship speed demand
##        Ship heading demand
##        Wind Speed relative to ship
##        Wind Direction relative to ship
##        availabe deck area for sizing
##        
##        OUTPUTS
##        Weight
##        Cost
##        Additional Thrust provided by sail
##        Added Resistance due to sail (e.g. equivalent due to rudder corrections and heel)
##        
##        This needs to be run to find the design phase of the sail.  We need to
##        do this for real time voyage and for "average wind conditions".  For
##        average wind conditions the inner loop can be precalculated to save time.
##        
##        In the design phase it is necessary to specify how sail is used and this
##        call of the wind function can also be used to precalculate variables.
#        
#        
#        #import propulsormodel
#        # find righting moment and KG for wind assist
#        #import windassist THIS NEEDS TO ACCESS WIND DATA
#
#        # USE NUMPY FUNCTIONS FOR PRE ASSIGNING ARRAYS LENGTHS WHERE POSSIBLE
##
##Z=4;  % Z number of propeller blades, can use 4 as estimate, could be 6 for very
##% large ships.
##
##% Twin - Single (1) or Twin (2) propulsion arrangement
##
##% L - Ship waterline length
##% T - Draught
##% B - Beam
##% Cp - prismatic coefficient
##% LCB - Longitudinal centre of buoyancy position (from AP/assumes from AP)
##% NOTE THIS IS ASSUMED THE SAME AS LCG SOMEWHERE, IF NOT SURE YOU CAN USE
##% L/2
##% D - propeller diameter
##% Foul - User Demanded fouling condition, expressed as percentage increase
##% in resistance (12.25% could be used for a rough approximate)
##
##
##% check that Rt is not below 0 (could happen for sails and results in
##% negative fuel consumption)
##if Rt<0
##    Rt=0;
##else
##    % do not change Rt, likely in most cases
##end
##
#
#
#
## NEED TO ENSURE CHECK BOXES WORK CORRECTLY
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
water_density = 1.024 # may make this into modifiable value and add to hull generation tab
propeller_design_speed = 0 # rpm, set to 0 for 2-stroke engine, this means same speed as engine
engine_design_speed = 110 # rpm
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
pod_correction = 0.97 # correction from FPP for using CPP or FPP pod

def main(fuel,rd,number_of_runs):
    # classe for design variables
    class design:
        pass
    # class for operation variables
    class operation:
        pass
    # set array length using numpy arrays for information that is saved
    displacement = np.zeros(number_of_runs)
    #GZ = np.zeros(number_of_runs)
    design.prop_diameter = np.zeros(number_of_runs)
    design.displaced_volume = np.zeros(number_of_runs)
    design.draught = np.zeros(number_of_runs)
    design.beam = np.zeros(number_of_runs)
    design.waterline_length = np.zeros(number_of_runs)
    design.waterplane_coefficient = np.zeros(number_of_runs)
    design.wetted_surface_area = np.zeros(number_of_runs)
    design.viscous_resistance = np.zeros(number_of_runs)
    design.added_resistance = np.zeros(number_of_runs)    
    design.additional_thust = np.zeros(number_of_runs)
    design.total_resistance = np.zeros(number_of_runs)
    design.speed_loss = np.zeros(number_of_runs)
    design.recovered_heat = np.zeros(number_of_runs)
    design.recovered_electricity = np.zeros(number_of_runs)
    design.auxiliary_energy = np.zeros(number_of_runs)
    design.heat_energy = np.zeros(number_of_runs)
    design.shaft_motor_power = np.zeros(number_of_runs)
    design.shaft_power = np.zeros(number_of_runs)
    
    
    design.engine_design_rating = np.zeros(number_of_runs)
    for run in range(number_of_runs):
        # for each run the user wishes to investigate
        # assume a payload deadweight fraction for first iteration of 0.5
        displacement[run] = ((rd.cargo_capacity_te[run]
                            *rd.cargo_utilisation_in_design[run])/0.5)
        # run hullgenerator.py with initial displacement estimate
        # note that the hull generator will also calculate the beam or draught,
        # given the displacement
        import hullgenerator
        hg = hullgenerator.generatehull(run, displacement, water_density,
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
        
        
        
        
        
        
        
        # HERE IN WORK
        
        
        # ALSO ASSUME INITIAL KG VALUE
        KG = 13.6 # for oil tanker VLCC and container ship need a better
        # estimate for his
        
        
        # HERE IN WORK
        # find design condition operational characteristics
        # the design condition is found according to the specified "displacement"
        hgop = hullgenerator.operationaldraughtorcargo(run, hg, "displacement",
                                            displacement[run], water_density,
                                            rd.waterline_number)
        # write calculated variables to array as function of the conditions
        # that will be examined
        # from hg
        design.prop_diameter[run] = hg.prop_diameter
        # from hgop
        design.displaced_volume[run] = hgop.displaced_volume
        design.draught[run] = hgop.draught
        design.beam[run] = hgop.beam
        design.waterline_length[run] = hgop.waterline_bow - hgop.waterline_stern
        design.waterplane_coefficient[run] = hgop.waterplane_coefficient
        # run the selected still water resistance model
        design_condition = 1
        Speed = rd.design_speed[run]
        L = design.waterline_length[run]
        T = design.draught[run]
        B = design.beam[run]
        Cp = rd.prismatic_coefficient[run] # THIS IS DESIGN VALUE CAN BE BETTER ESTIMATED
        LCB = design.waterline_length[run]/2 # THIS IS ASSUMED TO BE L/2 CAN BE IMPROVED???? CHECK THIS
        Disp = design.displaced_volume[run]*water_density
        Cwp = design.waterplane_coefficient[run]
        Cm = rd.midship_coefficient[run] # THIS IS DESIGN VALUE CAN BE BETTER ESTIMATED
        D = design.prop_diameter[run]
        Twin = rd.propulsors[run]
        Z = rd.propeller_blades[run]
        Foul = 1 # factor due to fouling
        ChR = 0 # change in resistance (due to sails)
        # find resistance in design condition
        import stillwaterresistance
        S, Rv, Rw, Ra, Rapp, t, w, bar, rre = stillwaterresistance.holtrop(
            design_condition, water_density, Speed, L, T, B, Cp, LCB, Disp,
            Cwp, Cm, D, Twin, Z, Foul, ChR)
        # HERE IN WORK
        
        
        # WEATHER ROUTING AND APPARENT WIND AND WAVE FUNCTION CALL HERE
        beaufort_number = 0
        apparent_wave_direction = 0
        # ABSOLUTE WIND AND WAVE DIRECTON
        true_wind_speed = 0
        true_wind_direction = 0
        
        
        # HERE IN WORK
        # find added resistance in design condition
        import performanceanddegredation
        design.added_resistance[run], design.speed_loss[run] = performanceanddegredation.addedresisance(1,
                    displacement[run], water_density, design.draught[run],
                    rd.block_coefficient[run], design.waterline_length[run],
                    rd.design_speed[run], beaufort_number,
                    apparent_wave_direction)
        # calculate total Resistance (Rt)
        Rt=(Rv*Foul+Rw+Ra+Rapp*Foul+ChR)+design.added_resistance[run]
        # add variables to array
        design.wetted_surface_area[run] = S
        design.viscous_resistance[run] = Rv
        design.additional_thust[run] = ChR
        design.total_resistance[run] = Rt
        # initial estimate of propeller efficiency is 0.7
        prop_open_water_efficiency = 0.7
        # HERE IN WORK
        
        # IN WORK NOW
        # convert user input into number for propeller model, using specified
        # efficiency
        if (rd.propulsion_type[run] == "fixed pitch propeller"):
            CPP = 0
            pod_correction = 0
        elif (rd.propulsion_type[run] == "controllable pitch propeller"):
            CPP = CPP
            pod_correction = 0
        elif (rd.propulsion_type[run] == "(FPP or CPP) pod"):
            CPP = 0
            pod_correction = pod_correction
        else:
            pass
            # ERROR, rd.propulsion_type not populated correctly

        # IN WORK
#        # ADD THIS TO PROPULSOR FUNCTION
#        
#        # account for pod_body_drag and a 3% drop in propeller efficiency, due
#        # to a larger boss
#        # taken from pages 367 and 368 of Ship Resistance and Propulsion,
#        # Molland, Turnock and Hudson
#        
#        # approximate the pod body as a cylinder that is 1.5 x propeller
#        # diameter long and 0.5 x propeller diameter
#        
#        pSb = np.pi*hg.prop_diameter*1.5*hg.prop_diameter
#        Cf = ?
#        pV = ?
#        #Cf FROM RESISTANCE MODEL??
#        #pV speed at propeller, assumed the same as for convenerional propeller
#        
#        pod_body_drag = (1+pKb)*(Cf*0.5*pSb*pV*pV)
#        pKb = 1.5*((0.5/1.5)**(3/2))+7*((0.5/1.5)**3)
#        
#        # pod has 3% decrease in propeller efficiency due to incrase in boss diameter
#        
#        # assume lenth is 1.5 x propeller diameter

#        # ADD THIS TO PROPULSOR FUNCTION
        # IN WORK
        
        
        
        
        import propulsor
        # set propeller operating point in design condition
        
        # IN WORK
        # assumption for design condition
        engine_operation_speed = engine_design_speed
        # IN WORK
        effO, EngTorque, PropThrust, PoverD, nProp = propulsor.wagbpropandgearbox(water_density, 1, CPP, pod_correction, rd.design_speed[run], rd.design_speed[run], design.total_resistance[run], engine_design_speed, engine_operation_speed, propeller_design_speed, rd.propulsors[run], w, design.prop_diameter[run], bar, rd.propeller_blades[run])
        print(effO)
        # IN WORK NOW
        
        # IN WORK
        # THIS GIVES INCORRECT RESULTS
        # find righting moment for a heel_angle between 0 and 20 degrees
        righting_moment_array = np.zeros(21)
        for heel_angle in range(21):
            # convert heel_angle to radians
            heel_angle_rad = heel_angle*np.pi/180
            GZ, righting_moment = hullgenerator.transversebouyancyandmoment(run, rd.waterline_number, hg, hgop, KG, heel_angle_rad)
            # save to righting_moment_array, where heel_angle is the index            
            righting_moment_array[heel_angle] = righting_moment
            if heel_angle == 2:
                print(GZ)
                print('GZ at 2 degrees is: ' + repr(GZ) + 'm')
                
            #print(righting_moment)
        # THIS GIVES INCORRECT RESULTS
        # IN WORK
        
        
        # HERE IN WORK WIND ASSIST FUNCTION AND TECHNOLOGY INTERACTIONS GO HERE
        
        available_deck_length = 0
        
        import windassist
        sail_thrust, added_sail_resistance, x_position_of_sails, length_of_sails, mass, x_centroid_mass, through_life_cost, unit_purchase_cost = windassist.sail(1, rd.design_speed[run], design.wetted_surface_area[run], true_wind_speed, true_wind_direction,
                                                                                                                                                                 righting_moment_array, available_deck_length, design.beam[run], rd.depth_of_draught[run]*design.draught[run],
                                                                                                                                                                    design.draught[run], design.displaced_volume[run], rd.block_coefficient[run])
        
        
        
        # HERE IN WORK WIND ASSIST FUNCTION AND TECHNOLOGY INTERACTIONS GO HERE
        ChPC = 1.0
        
        
        # HERE IN WORK
        # initial esimate of propulsion coefficient
        PC=((1-t)/(1-w))*rre*prop_open_water_efficiency*(transmission_efficiency/100)*ChPC
        # initial estimate of shaft power based on rd.design_speed[run]
        design.shaft_power[run]=Rt*(rd.design_speed[run]*0.51444)/PC
        # check shaft generator requirements
        # 0 is not fitted, + is shaft motor (power take off), - is shaft generator (power take in)
        # assuming the first operating mode is used for the design on the shaft generator
        # initial enigne selection, with the shaft motor power set to 0 and
        # using the given electrical power demand (not considering waste heat
        # recovery)
        import marinesystemsandengine
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
            # HERE IN WORK
            
            # CALL WASTE HEATER RECOVERY PLANT FOR GENERATION OF HEAT AND ELECTRICITY
            design.recovered_heat[run] = 0
            design.recovered_electricity[run] = 0
            
            # HERE IN WORK
        elif whr_plant_energy_type_output == "Heat":
            # HERE IN WORK
            
            # CALL WASTE HEATER RECOVERY PLANT FOR GENERATION OF HEAT
            design.recovered_heat[run] = 0
            design.recovered_electricity[run] = 0
            
            # HERE IN WORK
        else:
            # whr_plant_energy_type_output == "None", the field is unpopulated,
            # include_whr_in_design_phase == 1 or there is an ERROR
            # HERE IN WORK
            
            # NO WHR PLANT FITTED SET ALL VALUES FOR THIS TO 0
            design.recovered_heat[run] = 0
            design.recovered_electricity[run] = 0
            
            # HERE IN WORK
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
        # --2nd-Iteration-in-Design--
        # HERE IN WORK
        
        # call equipmentandstructure.py to get new displacement from selected
        # equipment
        
        # HERE IN WORK
        # find design condition operational characteristics according to the
        # newly calculated "displacement"
        hgop = hullgenerator.operationaldraughtorcargo(run, hg, "displacement",
                                            displacement[run], water_density,
                                            rd.waterline_number)
        # run resistance accounting for changes including speed loss due to
        # added resistance
        # write calculated variables to array as function of the conditions
        # that will be examined
        # from hg
        design.prop_diameter[run] = hg.prop_diameter
        # from hgop
        design.displaced_volume[run] = hgop.displaced_volume
        design.draught[run] = hgop.draught
        design.beam[run] = hgop.beam
        design.waterline_length[run] = hgop.waterline_bow - hgop.waterline_stern
        design.waterplane_coefficient[run] = hgop.waterplane_coefficient
        # run the selected still water resistance model
        design_condition = 1
        Speed = rd.design_speed[run] + design.speed_loss[run] # accounting for added resistance
        L = design.waterline_length[run]
        T = design.draught[run]
        B = design.beam[run]
        Cp = rd.prismatic_coefficient[run] # THIS IS DESIGN VALUE CAN BE BETTER ESTIMATED
        LCB = design.waterline_length[run]/2 # THIS IS ASSUMED TO BE L/2 CAN BE IMPROVED???? CHECK THIS
        Disp = design.displaced_volume[run]*water_density
        Cwp = design.waterplane_coefficient[run]
        Cm = rd.midship_coefficient[run] # THIS IS DESIGN VALUE CAN BE BETTER ESTIMATED
        D = design.prop_diameter[run]
        Twin = rd.propulsors[run]
        Z = rd.propeller_blades[run]
        Foul = 1 # factor due to fouling
        ChR = 0 # change in resistance (due to sails)
        # find resistance in design condition
        S, Rv, Rw, Ra, Rapp, t, w, bar, rre = stillwaterresistance.holtrop(
            design_condition, water_density, Speed, L, T, B, Cp, LCB, Disp,
            Cwp, Cm, D, Twin, Z, Foul, ChR)
        
        # UP TO HERE
        
        # TO DO NEXT:
        
        # import propulsor
        # - RECALCULATE UP TO ENGINE FOR 2nd LOOP
        # - FIX EXISTING PROBLEMS
        # - CARRY OUT OPERATIONAL PERFORMANCE ANALYSIS
        
        # HERE IN WORK - PRINT VARIABLES TO CHECK RESULTS
        # displacement is incorrect at the moment
        # print('Displacement: ' + repr(displacement[run]) + 'tonnes')
        print('KG: ' + repr(KG) + 'metres')
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
##% changes to ship due to design changes e.g. sails air lubrication - ChRv,ChSapp,ChPC,ChR set to 0.
#
#
##
##%[Rv,Rw,Ra,Rapp,kn,t,w,rre,bar] = holtropresistance(Design,DesignSpeed,OperationSpeed,L,T,B,Cp,LCB,S,Disp,Cm,D,Foul,ChRv,ChSapp,ChPC,ChR,Twin,effO,effT,rre,bar,Z)
##[Rv,Rw,Ra,Rapp,kn,t,w,rre,bar] = holtropresistance(1,DesignSpeed,OperationSpeed,L,T,B,Cp,LCB,S,Disp,Cm,D,0.1225,ChRv,ChSapp,ChPC,ChR,Twin,bar,Z);
##    # accounting for fouling is used
#  #  Rv=Rv*Foul
#  #  Rapp=Rapp*Foul
##% ASSUMPTIONS TO THIS
##% still water
##% design condition (can change this with inputs)
##% not work below 2 knots
##
##% effO - Propeller Open-water Efficiency, this comes from propeller model (wagbpropandgearbox.m) and is estimated on first iteration
##% effT - Transmisson Efficiency (this is given as a percentage, so need to divide by 100 when used)
##
##effO=  % can use 0.7 could be as low as 0.6
##effT=  % transmission efficiency 0.99???
##
##
##%USE SET PROPELLER EFFICIENCT BUT NEEDS UPDATING
##
##
#
##
##% Rt - Total Resistance
##Rt=Rv+Rw+Ra+Rapp+ChR;
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
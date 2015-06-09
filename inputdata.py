# SHIP IMPACT MODEL Version 4
# Author: John Calleya (UCL)
# Version: 1.0
# History:
# 1.0 Some parameters specified in main.py are missing from user interface

# Description:
# Run this file to begin.

# Compatibility Notes: tkinter was renamed from Tkinter in Python 2,
# tkinter.ttk was ttk in Python 2

# import tkinter and ttk modules for user interface.  tkinter contains most of
# the basic function while ttk has newer widgets and functions
from tkinter import ttk # ttk import
# override basic tkinter widgets
from tkinter import *
from tkinter.ttk import *
# use numpy package for maths (instead of math or cmath package) with np
import numpy as np

# NOTES


# POSSIBLE DIVIDE BY 0 ON OUTPUT
# Invalid user entry
# sea water 1.024
# HAVE COSTING SECTION IN ANOTHER PART OF INTERFACE?
# SORT BELOW VARIABLES INTO RELEVANT SECTION AND BUTTONS IN INTERFACE


# number of FEU containers
# design 10kW??
# NEED TO ADD  
# analysis and something???
# investment_period??



# these variables have to be acoounted for considering what is in add toqueue function
# assume a deadweight to displacement value!!!??
# centre of gravity as input??
# UP TO HERE

# utilisation
# same cargo in every hold check box??

        #data.double_bottom_height = "SOLAS (least of B/20 or 2m)"
        #data.double_side_wing_space_width = "Oil Tanker (MARPOL Annex I Regulation 19)"


#bulk carrier
# overall length = 225
#LBP = 219.258
#depth = 19.8
#draught= 12.25
# bulbous bow length???

# Keep transom of beam ship specific, above assumes that less dense cargos have more volumous hullforms
# 10.179m FOR SLOP TANK LENGTH OF 15 knot vlcc OIL TANKER


#container ship
#overall length = 294.221
#LBP = 279.898
#depth = 21
#draught = 12.516
  #  double_bottom_height = "SOLAS (least of B/20 or 2m)"
 #   double_side_wing_space_width = "Oil Tanker (MARPOL Annex I Regulation 19)"


    
    
    

    
    
    # MARPOL Annex I Regulation 19
    
    
# if data.cargo_capacity_units == "tonnes"
    
    
# if double_side_wing_space_width == "Oil Tanker (MARPOL Annex I Regulation 19)"
    #0.5*cargo_capacity
    
    # SWAP OVER COMPARTMENT LENGTH/NO. OF COMPARTMENTS SELECTION
    
    # hatch cover width = 0.5*beam (bulk carrier)
    # hatch cover length = 0.65*hold length (bulk carrier)
    # number of cargo holds or modules is an input
        
    # WHAT ABOUT DIFFERNT LOADING CONDITIONS??
    # 0.05m transverse packing margin
    # 0.076m longitudinal
        
    # SIDE HULL WIDTH???
    # CARGO INCREMENT WIDTH E>G> CONTAINERS
    # HAVE A TAB FOR MATERIAL AND STRUCTURAL WEIGHT???
        # minimum side hull width for container ship, oil tanker and bulk?
        

    # (assumedcargoholdsandsuperstructure - (2*bulkhead thickness + superstructure length) - (number of cargo holds*bulkhead thickness)))/number of cargo holds
    # hatch coming height is half of deck height
    
    # accomodation length = 6 + 1.5 * engine length
    # superstructure length = (40/1000)+ accomodation length

        # UPTOHERE
    # PERSONNEL INCLUDING CREW NUMBER FOR WEIGHT GROUP + CONSUMPTION FIGURES
    # WEIGHT, VOLUME AND POWER DEMAND, LOCATION ESTIMATES SHOULD BE A TAB IN MODEL
    # ^ COULD ALSO OUT MATERIAL PROPERTIES HERE AS WELL

# NOTES

# set run number to 0, this increases when user selects adds a run to the queue
run = 0

# set static data for model, not modified by user interface




# set fuel source list
class fuel:
    # set the fuel names to use, formatted for user interface
    fuel_names = "{None (Renewable Only)} {Marine Diesel Oil} {Heavy Fuel Oil} {Liquid Natural Gas}"
    # bunker cost, fuel density and CO2 factor should go here

# this class contains the default values for each entry, this list will be used
# to populate an entry for each field, the same variable list is used thoughout
class data:
    ship_name = ["ship_1"]
    cargo_type = ["containers"]
    cargo_density = [0.00]
    design_speed = [25.0]
    cargo_utilisation_in_design = [100] # %
    cargo_capacity = [0.00]
    cargo_capacity_units = ["tonnes"]
    personnel = [15]
    powering_margin = [25.00]
    propulsion_type = ["fixed pitch propeller"]
    propulsors = [1]
    set_beam_or_draught = ["beam"]
    beam_or_draught = [0.00]
    set_waterline_or_overall = ["waterline length"]
    waterline_or_overall = [0.00]
    compartment_length_units = ["compartment length"]
    compartment_length_or_no = [12.340]
    
    endurance = [35.00]
    bow_thruster = [1]
    midship_coefficient = [0.99] # 0.98 for container ship, 0.99 for bulk carrier
    set_block_or_prismatic_coefficient = ["block coefficient"]
    block_or_prismatic_coefficient = [0.76] # 0.64 for container ship, 0.76 for bulk carrier
    
    waterline_number = [30] # number of waterlines to split ship into for analysis
    waterline_and_transom_overlap = [0.00] # when 0 assumes that aft point of waterline meets bottom of transom in design condition
    flare_angle = [0.00] # flare/tumblehome(at amidships from vertical)
    deadrise_angle = [0.00] # (at amidships from horizontal)
    bow_angle = [31.60] # (from vertical)
    pmb_angle = [14.442] # same for both fore and aft from horizontal, 14.442 from horizontal fwd on container ship 31.658 from horizontal fwd on bulk carrier
    stern_slope_angle = [7.785] # 7.785 degrees for a container ship (25knots), 15.623 for 15 knot vlcc
    pmb_fwd_of_waterline = [0.780] # 0.780 for container ship, 0.836 bulk carrier (measured from AP, in terms of waterline length)
    pmb_aft_of_waterline = [0.044] # 0.044 for container ship 0.232 for bulk carrier (measured from AP, in terms of waterline length)
    depth_of_draught = [1.678] # 1.678 for container ship or 1.616 for bulk carrier (measured from AP, in terms of waterline length)
    overall_length_of_waterline = [1.026] # container ship (294.221/279.898), bulk carrer (225/219.258)
    transom_of_beam = [0.965] # 0.965 for a container ship to maximise load on deck, 0.307 for 1 knot VLCC
    stern_point_of_waterline = [-0.026] # transom stern position = -0.026*LBP CONTAINER SHIP, transom stern position = -0.017*LBP BULK CARRIER
    prop_point_of_waterline = [0.023] # 0.023 for container ship and bulk carrier
    aftercutup_of_waterline = [0.038] # 0.038 for 25 knot container ship and a 15 knot vlcc
    hull_tip_clear_of_diameter = [0.250] # minimum of 0.25*propeller diameter - ABS Guidance Notes on Ship Vibration April 2006 (Updated Febraury 2014)
    keel_tip_clear_of_diameter = [0.035] # clearance between keel and propeller, page 63 Ship Design for Efficiency and Economy, from DNV recommendation
    disc_clear_of_diameter = [1.000] # estimated, clearance between multiple propulsors, measured from edge of disc
    water_density = [1.024]
    
    deck_height = [2.800]
    cofferdam_between_compartments = [1.60]
    bow_space_length_of_overall_length = [0.07]
    longitudinal_bulkheads = [0] # for tankers
    superstructure_position = [1.00]
    superstructure_length_in_compartments = [1.00]
    engine_room_position = [1.00]
    hold_width_multiple = [0.000] # for unitised cargo (or cabins)
    primary_structure_density_multiplier = [1.00]
    secondary_structure_density_multiplier = [1.00]
    propeller_blades = [4]
    cpp_efficiency_relative_to_fpp = [98.5] # %
    direct_drive_efficiency = [99.5] # %
    mechanical_transmission_efficiency = [98.5] # %
    waste_heat_recovery_fitted = [0] # checkbox
    waste_heat_recovery_design_point = [75] # % of MCR
    shaft_generator_fitted = [0] # checkbox
    shaft_generator_maximum_power = [0] # kW (0 for not fitted)
    shaft_generator_pto_efficiency = [96.2] # % ABB
    shaft_generator_pti_efficiency = [93.3] # % ABB motor efficiency x0.98 transmission efficiency
    electrical_propulsion_efficiency = [94.7] # from ABB brochure, maximum size x0.99, increases with motor size
    maximum_electrical_power_available = [1400] # kW
    maximum_heat_power_available = [0] # kW
    
    profile_name_1 = ["Design Condition"]
    profile_cargo_or_draught_1 = ["draught"]
    profile_location_1 = ["operating_profiles/loaded_condition.csv"]
    profile_main_energy_source_1 = ["Heavy Fuel Oil"]
    profile_auxiliary_energy_source_1 = ["Marine Diesel Oil"]
    profile_heat_energy_source_1 = ["Marine Diesel Oil"]
    profile_shaft_generator_1 = ["Not Used"]
    profile_electrical_power_demand_1 = [0] # kW
    profile_heat_power_demand_1 = [0] # kW
    profile_time_1 = [40] # % or hours
    profile_name_2 = ["Ballast Condition"]
    profile_cargo_or_draught_2 = ["not used"]
    profile_location_2 = ["operating_profiles/ballast_condition.csv"]
    profile_main_energy_source_2 = ["Heavy Fuel Oil"]
    profile_auxiliary_energy_source_2 = ["Marine Diesel Oil"]
    profile_heat_energy_source_2 = ["Marine Diesel Oil"]
    profile_shaft_generator_2 = ["Not Used"]
    profile_electrical_power_demand_2 = [0] # kW
    profile_heat_power_demand_2 = [0] # kW
    profile_time_2 = [40] # % or hours
    profile_name_3 = ["Environmental Control Area (ECA) Condition"]
    profile_cargo_or_draught_3 = ["not used"]
    profile_location_3 = ["operating_profiles/loaded_condition.csv"]
    profile_main_energy_source_3 = ["Heavy Fuel Oil"]
    profile_auxiliary_energy_source_3 = ["Marine Diesel Oil"]
    profile_heat_energy_source_3 = ["Marine Diesel Oil"]
    profile_shaft_generator_3 = ["Not Used"]
    profile_electrical_power_demand_3 = [0] # kW
    profile_heat_power_demand_3 = [0] # kW
    profile_time_3 = [0] # % or hours
    profile_name_4 = ["Manoeuvring Condition"]
    profile_cargo_or_draught_4 = ["not used"]
    profile_location_4 = ["operating_profiles/ballast_condition.csv"]
    profile_main_energy_source_4 = ["Heavy Fuel Oil"]
    profile_auxiliary_energy_source_4 = ["Marine Diesel Oil"]
    profile_heat_energy_source_4 = ["Marine Diesel Oil"]
    profile_shaft_generator_4 = ["Not Used"]
    profile_electrical_power_demand_4 = [0] # kW
    profile_heat_power_demand_4 = [0] # kW
    profile_time_4 = [0] # % or hours
    profile_name_5 = ["Port Condition"]
    profile_cargo_or_draught_5 = ["not used"]
    profile_location_5 = ["operating_profiles/loaded_condition.csv"]
    profile_main_energy_source_5 = ["Heavy Fuel Oil"]
    profile_auxiliary_energy_source_5 = ["Marine Diesel Oil"]
    profile_heat_energy_source_5 = ["Marine Diesel Oil"]
    profile_shaft_generator_5 = ["Not Used"]
    profile_electrical_power_demand_5 = [0] # kW
    profile_heat_power_demand_5 = [0] # kW
    profile_time_5 = [20] # % or hours
        
# copy the data class to create a class for rundata that will be selected
# by user
class rundata(data):
    pass

# define classes for widgets (this allows all widget properties to be set)
# defines the appearance of buttons placed from left to right
class buttons:
    def __init__(self, container, buttontext, buttonevent):
        # command responds to letting go of mouse button and space bar, width
        # is in characters
        self.button = ttk.Button(container, text=buttontext, width=30,
                                 command=buttonevent)
        # pack fits widget within another container
        self.button.pack(side="left")
        # so that buttons respond to return key
        self.button.bind("<Return>", buttonevent) # .bind("<input>",event)

# defines the appearance of a label with an entry placed from top to bottom
class labelentry:
    def __init__(self, container, labeltext, usertype, initialvalue,
                 unitstext):
        self.input = usertype # specify the type of user variable
        self.subcontainer = ttk.Frame(container)
        self.subcontainer.pack(side="top", anchor="e") # align to the right
        self.label = ttk.Label(self.subcontainer, text=labeltext)
        self.label.pack(side="left")
        self.entry = ttk.Entry(self.subcontainer, textvariable=self.input)
        self.entry.pack(side="left")
        self.input.set(initialvalue) # set initial value
        self.units = Text(self.subcontainer, width=6, height=1)
        self.units.insert("1.0", unitstext)
        self.units.tag_add("superscript", "end -2 chars") # tag last letter
        self.units.tag_configure("superscript", offset=4) # superscript letter
        self.units.configure(state="disabled") # do not allow user to edit
        self.units.pack(side="left")

# defines the appearance of a label with a combobox
class labellist:
    def __init__(self, container, labeltext, usertype, userchoice,
                 initialvalue):
        self.input = usertype # specify the type of the user variable
        self.subcontainer = ttk.Frame(container)
        self.subcontainer.pack(side="top", anchor="e") # align to the right
        self.label = ttk.Label(self.subcontainer, text=labeltext)
        self.label.pack(side="left")
        self.entry = ttk.Combobox(self.subcontainer, textvariable=usertype,
                                  values=userchoice, state="readonly")
        self.entry.pack(side="left")
        self.input.set(initialvalue) # set initial value
        
# defined the appearance of a label with a checkbox
class labelcheck:
    def __init__(self, container, labeltext, initialvalue):
        self.subcontainer = ttk.Frame(container)
        self.input = IntVar()
        self.input.set(initialvalue)
        self.subcontainer.pack(side="top", anchor="e") # align to the right
        self.label = ttk.Label(self.subcontainer, text=labeltext)
        self.label.pack(side="left")
        self.entry = ttk.Checkbutton(self.subcontainer, variable=self.input,
                                     onvalue=1, offvalue=0)
        self.entry.pack(side="left")
        
# define functions for widgets in the actions class
class actions:
    def set_default_data(*args):
        # this is a copy of the data class but at the specified run
        data.ship_name[0] = "ship_1"
        data.cargo_type[0] = "containers"
        data.cargo_density[0] = 0.00
        data.design_speed[0] = 25.0
        data.cargo_utilisation_in_design[0] = 100
        data.cargo_capacity[0] = 0.00
        data.cargo_capacity_units[0] = "tonnes"
        data.personnel[0] = 15
        data.powering_margin[0] = 25.00
        data.propulsion_type[0] = "fixed pitch propeller"
        data.propulsors[0] = 1
        data.set_beam_or_draught[0] = "beam"
        data.beam_or_draught[0] = 0.00
        data.set_waterline_or_overall[0] = "waterline length"
        data.waterline_or_overall[0] = 0.00
        data.compartment_length_units[0] = "compartment length"
        data.compartment_length_or_no[0] = 12.340
        
        data.endurance[0] = 35.00
        data.bow_thruster[0] = 1
        data.midship_coefficient[0] = 0.99
        data.set_block_or_prismatic_coefficient[0] = "block coefficient"
        data.block_or_prismatic_coefficient[0] = 0.76
        
        data.waterline_number[0] = 30
        data.waterline_and_transom_overlap[0] = 0.00        
        data.flare_angle[0] = 0.00
        data.deadrise_angle[0] = 0.00
        data.bow_angle[0] = 31.60
        data.pmb_angle[0] = 14.442
        data.stern_slope_angle[0] = 7.785
        data.pmb_fwd_of_waterline[0] = 0.836
        data.pmb_aft_of_waterline[0] = 0.232
        data.depth_of_draught[0] = 1.678
        data.overall_length_of_waterline[0] = 1.026
        data.transom_of_beam[0] = 0.965
        data.stern_point_of_waterline[0] = -0.017
        data.prop_point_of_waterline[0] = 2.279
        data.aftercutup_of_waterline[0] = 0.038        
        data.hull_tip_clear_of_diameter[0] = 0.25
        data.keel_tip_clear_of_diameter[0] = 0.035
        data.disc_clear_of_diameter[0] = 1.000
        data.water_density[0] = 1.024
        
        data.deck_height[0] = 2.800
        data.cofferdam_between_compartments[0] = 1.60
        data.bow_space_length_of_overall_length[0] = 0.07
        data.longitudinal_bulkheads[0] = 0
        data.superstructure_position[0] = 1.00
        data.superstructure_length_in_compartments[0] = 1.00
        data.engine_room_position[0] = 1.00
        data.hold_width_multiple[0] = 0.000
        data.primary_structure_density_multiplier[0] = 1.00
        data.secondary_structure_density_multiplier[0] = 1.00
        data.propeller_blades[0] = 4
        data.cpp_efficiency_relative_to_fpp[0] = 98.5 # %
        data.direct_drive_efficiency[0] = 99.5 # %
        data.mechanical_transmission_efficiency[0] = 98.5 # %
        data.waste_heat_recovery_fitted[0] = 0 # checkbox
        data.waste_heat_recovery_design_point[0] = 75 # % of MCR
        data.shaft_generator_fitted[0] = 0 # checkbox
        data.shaft_generator_maximum_power[0] = 0 # kW (0 for not fitted)
        data.shaft_generator_pto_efficiency[0] = 96.2 # % ABB
        data.shaft_generator_pti_efficiency[0] = 93.3 # % ABB motor efficiency x0.98 transmission efficiency
        data.electrical_propulsion_efficiency[0] = 94.7 # from ABB brochure, maximum size x0.99, increases with motor size
        data.maximum_electrical_power_available[0] = 1400 # kW
        data.maximum_heat_power_available[0] = 0 # kW
        
        data.profile_name_1[0] = "Design Condition"
        data.profile_cargo_or_draught_1[0] = "draught"
        data.profile_location_1[0] = "operating_profiles/loaded_condition.csv"
        data.profile_main_energy_source_1[0] = "Heavy Fuel Oil"
        data.profile_auxiliary_energy_source_1[0] = "Marine Diesel Oil"
        data.profile_heat_energy_source_1[0] = "Marine Diesel Oil"
        data.profile_shaft_generator_1[0] = "Not Used"
        data.profile_electrical_power_demand_1[0] = 0 # kW
        data.profile_heat_power_demand_1[0] = 0 # kW
        data.profile_time_1[0] = 40 # % or hours
        data.profile_name_2[0] = "Ballast Condition"
        data.profile_cargo_or_draught_2[0] = "not used"
        data.profile_location_2[0] = "operating_profiles/ballast_condition.csv"
        data.profile_main_energy_source_2[0] = "Heavy Fuel Oil"
        data.profile_auxiliary_energy_source_2[0] = "Marine Diesel Oil"
        data.profile_heat_energy_source_2[0] = "Marine Diesel Oil"
        data.profile_shaft_generator_2[0] = "Not Used"
        data.profile_electrical_power_demand_2[0] = 0 # kW
        data.profile_heat_power_demand_2[0] = 0 # kW
        data.profile_time_2[0] = 40 # % or hours
        data.profile_name_3[0] = "Environmental Control Area (ECA) Condition"
        data.profile_cargo_or_draught_3[0] = "not used"
        data.profile_location_3[0] = "operating_profiles/loaded_condition.csv"
        data.profile_main_energy_source_3[0] = "Heavy Fuel Oil"
        data.profile_auxiliary_energy_source_3[0] = "Marine Diesel Oil"
        data.profile_heat_energy_source_3[0] = "Marine Diesel Oil"
        data.profile_shaft_generator_3[0] = "Not Used"
        data.profile_electrical_power_demand_3[0] = 0 # kW
        data.profile_heat_power_demand_3[0] = 0 # kW
        data.profile_time_3[0] = 0 # % or hours
        data.profile_name_4[0] = "Manoeuvring Condition"
        data.profile_cargo_or_draught_4[0] = "not used"
        data.profile_location_4[0] = "operating_profiles/ballast_condition.csv"
        data.profile_main_energy_source_4[0] = "Heavy Fuel Oil"
        data.profile_auxiliary_energy_source_4[0] = "Marine Diesel Oil"
        data.profile_heat_energy_source_4[0] = "Marine Diesel Oil"
        data.profile_shaft_generator_4[0] = "Not Used"
        data.profile_electrical_power_demand_4[0] = 0 # kW
        data.profile_heat_power_demand_4[0] = 0 # kW
        data.profile_time_4[0] = 0 # % or hours
        data.profile_name_5[0] = "Port Condition"
        data.profile_cargo_or_draught_5[0] = "not used"
        data.profile_location_5[0] = "operating_profiles/loaded_condition.csv"
        data.profile_main_energy_source_5[0] = "Heavy Fuel Oil"
        data.profile_auxiliary_energy_source_5[0] = "Marine Diesel Oil"
        data.profile_heat_energy_source_5[0] = "Marine Diesel Oil"
        data.profile_shaft_generator_5[0] = "Not Used"
        data.profile_electrical_power_demand_5[0] = 0 # kW
        data.profile_heat_power_demand_5[0] = 0 # kW
        data.profile_time_5[0] = 20 # % or hours
        
        actions.set_values_in_entry_widgets()
        
    def clear_all_fields(*args):
        # can populate this function by copying and modifying previous function as reference
    
        data.ship_name[0] = ""
        data.cargo_type[0] = ""
        data.cargo_density[0] = 0.00
        data.design_speed[0] = 0.0
        data.cargo_utilisation_in_design[0] = 0
        data.cargo_capacity[0] = 0.00
        data.cargo_capacity_units[0] = ""
        data.personnel[0] = 0
        data.powering_margin[0] = 0.00
        data.propulsion_type[0] = ""
        data.propulsors[0] = 0
        data.set_beam_or_draught[0] = ""
        data.beam_or_draught[0] = 0.00
        data.set_waterline_or_overall[0] = ""
        data.waterline_or_overall[0] = 0.00
        data.compartment_length_units[0] = ""
        data.compartment_length_or_no[0] = 0.000
        
        data.endurance[0] = 0.00
        data.bow_thruster[0] = 1
        data.midship_coefficient[0] = 0.00
        data.set_block_or_prismatic_coefficient[0] = ""
        data.block_or_prismatic_coefficient[0] = 0.00
        
        data.waterline_number[0] = 0
        data.waterline_and_transom_overlap[0] = 0.00        
        data.flare_angle[0] = 0.00
        data.deadrise_angle[0] = 0.00
        data.bow_angle[0] = 0.00
        data.pmb_angle[0] = 0.000
        data.stern_slope_angle[0] = 0.000
        data.pmb_fwd_of_waterline[0] = 0.000
        data.pmb_aft_of_waterline[0] = 0.000
        data.depth_of_draught[0] = 0.000
        data.overall_length_of_waterline[0] = 0.000
        data.transom_of_beam[0] = 0.000
        data.stern_point_of_waterline[0] = 0.000
        data.prop_point_of_waterline[0] = 0.000
        data.aftercutup_of_waterline[0] = 0.000        
        data.hull_tip_clear_of_diameter[0] = 0.00
        data.keel_tip_clear_of_diameter[0] = 0.000
        data.disc_clear_of_diameter[0] = 0.000
        data.water_density[0] = 1.024
        
        data.deck_height[0] = 0.000
        data.cofferdam_between_compartments[0] = 0.00
        data.bow_space_length_of_overall_length[0] = 0.00
        data.longitudinal_bulkheads[0] = 0
        data.superstructure_position[0] = 1.00
        data.superstructure_length_in_compartments[0] = 1.00
        data.engine_room_position[0] = 1.00
        data.hold_width_multiple[0] = 0.000
        data.primary_structure_density_multiplier[0] = 1.00
        data.secondary_structure_density_multiplier[0] = 1.00
        data.propeller_blades[0] = 0
        data.cpp_efficiency_relative_to_fpp[0] = 98.5
        data.direct_drive_efficiency[0] = 99.5
        data.mechanical_transmission_efficiency[0] = 98.5
        data.waste_heat_recovery_fitted[0] = 0
        data.waste_heat_recovery_design_point[0] = 75
        data.shaft_generator_fitted[0] = 0
        data.shaft_generator_maximum_power[0] = 0
        data.shaft_generator_pto_efficiency[0] = 96.2
        data.shaft_generator_pti_efficiency[0] = 93.3
        data.electrical_propulsion_efficiency[0] = 94.7
        data.maximum_electrical_power_available[0] = 0
        data.maximum_heat_power_available[0] = 0
        
        data.profile_name_1[0] = ""
        data.profile_cargo_or_draught_1[0] = ""
        data.profile_location_1[0] = ""
        data.profile_main_energy_source_1[0] = ""
        data.profile_auxiliary_energy_source_1[0] = ""
        data.profile_heat_energy_source_1[0] = ""
        data.profile_shaft_generator_1[0] = ""
        data.profile_electrical_power_demand_1[0] = 0
        data.profile_heat_power_demand_1[0] = 0
        data.profile_time_1[0] = 0
        data.profile_name_2[0] = ""
        data.profile_cargo_or_draught_2[0] = ""
        data.profile_location_2[0] = ""
        data.profile_main_energy_source_2[0] = ""
        data.profile_auxiliary_energy_source_2[0] = ""
        data.profile_heat_energy_source_2[0] = ""
        data.profile_shaft_generator_2[0] = ""
        data.profile_electrical_power_demand_2[0] = 0
        data.profile_heat_power_demand_2[0] = 0
        data.profile_time_2[0] = 0
        data.profile_name_3[0] = ""
        data.profile_cargo_or_draught_3[0] = ""
        data.profile_location_3[0] = ""
        data.profile_main_energy_source_3[0] = ""
        data.profile_auxiliary_energy_source_3[0] = ""
        data.profile_heat_energy_source_3[0] = ""
        data.profile_shaft_generator_3[0] = ""
        data.profile_electrical_power_demand_3[0] = 0
        data.profile_heat_power_demand_3[0] = 0
        data.profile_time_3[0] = 0
        data.profile_name_4[0] = ""
        data.profile_cargo_or_draught_4[0] = ""
        data.profile_location_4[0] = ""
        data.profile_main_energy_source_4[0] = ""
        data.profile_auxiliary_energy_source_4[0] = ""
        data.profile_heat_energy_source_4[0] = ""
        data.profile_shaft_generator_4[0] = ""
        data.profile_electrical_power_demand_4[0] = 0
        data.profile_heat_power_demand_4[0] = 0
        data.profile_time_4[0] = 0
        data.profile_name_5[0] = ""
        data.profile_cargo_or_draught_5[0] = ""
        data.profile_location_5[0] = ""
        data.profile_main_energy_source_5[0] = ""
        data.profile_auxiliary_energy_source_5[0] = ""
        data.profile_heat_energy_source_5[0] = ""
        data.profile_shaft_generator_5[0] = ""
        data.profile_electrical_power_demand_5[0] = 0
        data.profile_heat_power_demand_5[0] = 0
        data.profile_time_5[0] = 0
        
        actions.set_values_in_entry_widgets()
        
    def container_ship(*args):
        
        data.ship_name[0] = "container_ship"
        data.cargo_type[0] = "containers"
        data.cargo_density[0] = 0.34
        data.design_speed[0] = 25.0
        data.cargo_utilisation_in_design[0] = 100.0 # this cannot be 0
        data.cargo_capacity[0] = 35032.00
        data.cargo_capacity_units[0] = "tonnes"
        # 1/1.1 is a rough deadweight to tonnes conversion calculated from
        # examining clarksons
        if (data.cargo_capacity[0]/1.1) < 3000:
            data.personnel[0] = 10
        elif (data.cargo_capacity[0]/1.1) < 5000:
            data.personnel[0] = 14
        elif (data.cargo_capacity[0]/1.1) < 10000:
            data.personnel[0] = 18            
        elif (data.cargo_capacity[0]/1.1) < 20000:
            data.personnel[0] = 21
        elif (data.cargo_capacity[0]/1.1) < 100000:
            data.personnel[0] = 22
        else:
            data.personnel[0] = 26
        # from "An Analysis of Crewing Levels: Findings from the SIRC Global Labour Market Survey"
        # https://orca-mwe.cf.ac.uk/64731/1/Analysis%20of%20crewing%20levels.pdf
        data.powering_margin[0] = 25.00
        data.propulsion_type[0] = "fixed pitch propeller"
        data.propulsors[0] = 1 # might be 2 for larger container ships
        data.set_beam_or_draught[0] = "beam"
        data.beam_or_draught[0] = 32.20
        data.set_waterline_or_overall[0] = "overall length"
        data.waterline_or_overall[0] = 294.20
        data.compartment_length_units[0] = "compartment length"
        data.compartment_length_or_no[0] = 12.340 # for 2 TEUs
        
        data.endurance[0] = 35.00
        data.bow_thruster[0] = 1
        data.midship_coefficient[0] = 0.98
        data.set_block_or_prismatic_coefficient[0] = "prismatic coefficient"
        data.block_or_prismatic_coefficient[0] = 0.65
        
        data.waterline_number[0] = 30
        data.waterline_and_transom_overlap[0] = 0.00
        data.flare_angle[0] = 0.00
        data.deadrise_angle[0] = 0.00
        data.bow_angle[0] = 31.6 # assumed the same for all ship types
        if data.set_block_or_prismatic_coefficient[0] == "block coefficient":
            data.pmb_angle[0] = 123.11*data.block_or_prismatic_coefficient[0]-64.421 # this came from 14.442 from horizontal on 25 knot container ship and 31.658 from horizontal on 15 knot VLCC
            data.stern_slope_angle[0] = 56.049*data.block_or_prismatic_coefficient[0]-28.119 # this came from 7.785 degrees for a container ship (25knots), 15.623 for 15 knot vlcc
            data.pmb_fwd_of_waterline[0] = 0.4004*data.block_or_prismatic_coefficient[0]+0.5235 # this came from 0.780 for container ship, 0.836 bulk carrier (measured from AP, in terms of waterline length)
            data.overall_length_of_waterline[0] = -0.1787*data.block_or_prismatic_coefficient[0]+1.1656 # this came from container ship (294.221/279.898), bulk carrer (225/219.258)
            data.stern_point_of_waterline[0] = 0.0644*data.block_or_prismatic_coefficient[0]-0.0672 # transom stern position = -0.026*LBP for container ship, transom stern position = -0.017*LBP for oil tanker
        else:
            # prismatic coefficient has been selected or there is an ERROR 
            data.pmb_angle[0] = 123.11*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])-64.421 # this came from 14.442 from horizontal on 25 knot container ship and 31.658 from horizontal on 15 knot VLCC
            data.stern_slope_angle[0] = 56.049*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])-28.119 # this came from 7.785 degrees for a container ship (25knots), 15.623 for 15 knot vlcc
            data.pmb_fwd_of_waterline[0] = 0.4004*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])+0.5235 # this came from 0.780 for container ship, 0.836 bulk carrier (measured from AP, in terms of waterline length)
            data.overall_length_of_waterline[0] = -0.1787*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])+1.1656 # this came from container ship (294.221/279.898), bulk carrer (225/219.258)
            data.stern_point_of_waterline[0] = 0.0644*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])-0.0672 # transom stern position = -0.026*LBP for container ship, transom stern position = -0.017*LBP for oil tanker
        data.pmb_aft_of_waterline[0] = 0.2848*data.cargo_density[0]-0.0528 # comes from 0.044 for container ship 0.232 for bulk carrier (measured from AP, in terms of waterline length)
        data.depth_of_draught[0] = -0.0939*data.cargo_density[0]+1.7099 # comes from 1.678 for container ship or 1.616 for bulk carrier (measured from AP, in terms of waterline length)
        data.transom_of_beam[0] = 0.307 # ship specific, 0.965 for a container ship to maximise load on deck, 0.307 for 15 knot VLCC
        
        data.prop_point_of_waterline[0] = 0.023 # 0.023 for container ship and bulk carrier
        data.aftercutup_of_waterline[0] = 0.038 # 0.038 for 25 knot container ship and a 15 knot vlcc
        data.hull_tip_clear_of_diameter[0] = 0.250 # minimum of 0.25*propeller diameter - ABS Guidance Notes on Ship Vibration April 2006 (Updated Febraury 2014)
        data.keel_tip_clear_of_diameter[0] = 0.035 # clearance between keel and propeller, page 63 Ship Design for Efficiency and Economy, from DNV recommendation
        data.disc_clear_of_diameter[0] = 1.000 # estimated, clearance between multiple propulsors, measured from edge of disc
        data.water_density[0] = 1.024
        
        data.deck_height[0] = 2.800
        data.cofferdam_between_compartments[0] = 1.60
        data.bow_space_length_of_overall_length[0] = 0.07
        data.longitudinal_bulkheads[0] = 0 # for tankers
        data.superstructure_position[0] = 1.00
        data.superstructure_length_in_compartments[0] = 1.00
        data.engine_room_position[0] = 1.00
        # UP TO HERE
        data.hold_width_multiple[0] = 0.00 # for unitised cargo (or cabins)
        data.primary_structure_density_multiplier[0] = 1.00
        data.secondary_structure_density_multiplier[0] = 1.00
        data.propeller_blades[0] = 4
        data.cpp_efficiency_relative_to_fpp[0] = 98.5
        data.direct_drive_efficiency[0] = 99.5
        data.mechanical_transmission_efficiency[0] = 98.5
        data.waste_heat_recovery_fitted[0] = 0
        data.waste_heat_recovery_design_point[0] = 75
        data.shaft_generator_fitted[0] = 1
        data.shaft_generator_maximum_power[0] = 0
        data.shaft_generator_pto_efficiency[0] = 96.2
        data.shaft_generator_pti_efficiency[0] = 93.3
        data.electrical_propulsion_efficiency[0] = 94.7
        data.maximum_electrical_power_available[0] = 0
        data.maximum_heat_power_available[0] = 0
        
        data.profile_name_1[0] = ""
        data.profile_cargo_or_draught_1[0] = ""
        data.profile_location_1[0] = ""
        data.profile_main_energy_source_1[0] = ""
        data.profile_auxiliary_energy_source_1[0] = ""
        data.profile_heat_energy_source_1[0] = ""
        data.profile_shaft_generator_1[0] = ""
        data.profile_electrical_power_demand_1[0] = 0
        data.profile_heat_power_demand_1[0] = 0
        data.profile_time_1[0] = 0
        data.profile_name_2[0] = ""
        data.profile_cargo_or_draught_2[0] = ""
        data.profile_location_2[0] = ""
        data.profile_main_energy_source_2[0] = ""
        data.profile_auxiliary_energy_source_2[0] = ""
        data.profile_heat_energy_source_2[0] = ""
        data.profile_shaft_generator_2[0] = ""
        data.profile_electrical_power_demand_2[0] = 0
        data.profile_heat_power_demand_2[0] = 0
        data.profile_time_2[0] = 0
        data.profile_name_3[0] = ""
        data.profile_cargo_or_draught_3[0] = ""
        data.profile_location_3[0] = ""
        data.profile_main_energy_source_3[0] = ""
        data.profile_auxiliary_energy_source_3[0] = ""
        data.profile_heat_energy_source_3[0] = ""
        data.profile_shaft_generator_3[0] = ""
        data.profile_electrical_power_demand_3[0] = 0
        data.profile_heat_power_demand_3[0] = 0
        data.profile_time_3[0] = 0
        data.profile_name_4[0] = ""
        data.profile_cargo_or_draught_4[0] = ""
        data.profile_location_4[0] = ""
        data.profile_main_energy_source_4[0] = ""
        data.profile_auxiliary_energy_source_4[0] = ""
        data.profile_heat_energy_source_4[0] = ""
        data.profile_shaft_generator_4[0] = ""
        data.profile_electrical_power_demand_4[0] = 0
        data.profile_heat_power_demand_4[0] = 0
        data.profile_time_4[0] = 0
        data.profile_name_5[0] = ""
        data.profile_cargo_or_draught_5[0] = ""
        data.profile_location_5[0] = ""
        data.profile_main_energy_source_5[0] = ""
        data.profile_auxiliary_energy_source_5[0] = ""
        data.profile_heat_energy_source_5[0] = ""
        data.profile_shaft_generator_5[0] = ""
        data.profile_electrical_power_demand_5[0] = 0
        data.profile_heat_power_demand_5[0] = 0
        data.profile_time_5[0] = 0
        
        actions.set_values_in_entry_widgets()
        
    def vlcc(*args):
        
        data.ship_name[0] = "VLCC"
        data.cargo_type[0] = "oil"
        data.cargo_density[0] = 1.00
        data.design_speed[0] = 15.0
        data.cargo_utilisation_in_design[0] = 100.0 # this cannot be 0
        data.cargo_capacity[0] = 238003.70
        data.cargo_capacity_units[0] = "tonnes"
        # 1/1.1 is a rough deadweight to tonnes conversion calculated from
        # examining clarksons
        if (data.cargo_capacity[0]/1.1) < 3000:
            data.personnel[0] = 10
        elif (data.cargo_capacity[0]/1.1) < 5000:
            data.personnel[0] = 14
        elif (data.cargo_capacity[0]/1.1) < 10000:
            data.personnel[0] = 18            
        elif (data.cargo_capacity[0]/1.1) < 20000:
            data.personnel[0] = 21
        elif (data.cargo_capacity[0]/1.1) < 100000:
            data.personnel[0] = 22
        else:
            data.personnel[0] = 26
        # from "An Analysis of Crewing Levels: Findings from the SIRC Global Labour Market Survey"
        # https://orca-mwe.cf.ac.uk/64731/1/Analysis%20of%20crewing%20levels.pdf
        data.powering_margin[0] = 25.00
        data.propulsion_type[0] = "fixed pitch propeller"
        data.propulsors[0] = 1
        data.set_beam_or_draught[0] = "beam"
        data.beam_or_draught[0] = 60.00
        data.set_waterline_or_overall[0] = "overall length"
        data.waterline_or_overall[0] = 333.0
        data.compartment_length_units[0] = "number of compartment"
        data.compartment_length_or_no[0] = 6
        
        data.endurance[0] = 35.00
        data.bow_thruster[0] = 0
        data.midship_coefficient[0] = 0.99
        data.set_block_or_prismatic_coefficient[0] = "prismatic coefficient"
        data.block_or_prismatic_coefficient[0] = 0.78
        
        data.waterline_number[0] = 30
        data.waterline_and_transom_overlap[0] = 0.00
        data.flare_angle[0] = 0.00
        data.deadrise_angle[0] = 0.00
        data.bow_angle[0] = 31.6 # assumed the same for all ship types
        if data.set_block_or_prismatic_coefficient[0] == "block coefficient":
            data.pmb_angle[0] = 123.11*data.block_or_prismatic_coefficient[0]-64.421 # this came from 14.442 from horizontal on 25 knot container ship and 31.658 from horizontal on 15 knot VLCC
            data.stern_slope_angle[0] = 56.049*data.block_or_prismatic_coefficient[0]-28.119 # this came from 7.785 degrees for a container ship (25knots), 15.623 for 15 knot vlcc
            data.pmb_fwd_of_waterline[0] = 0.4004*data.block_or_prismatic_coefficient[0]+0.5235 # this came from 0.780 for container ship, 0.836 bulk carrier (measured from AP, in terms of waterline length)
            data.overall_length_of_waterline[0] = -0.1787*data.block_or_prismatic_coefficient[0]+1.1656 # this came from container ship (294.221/279.898), bulk carrer (225/219.258)
            data.stern_point_of_waterline[0] = 0.0644*data.block_or_prismatic_coefficient[0]-0.0672 # transom stern position = -0.026*LBP for container ship, transom stern position = -0.017*LBP for oil tanker
        else:
            # prismatic coefficient has been selected or there is an ERROR 
            data.pmb_angle[0] = 123.11*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])-64.421 # this came from 14.442 from horizontal on 25 knot container ship and 31.658 from horizontal on 15 knot VLCC
            data.stern_slope_angle[0] = 56.049*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])-28.119 # this came from 7.785 degrees for a container ship (25knots), 15.623 for 15 knot vlcc
            data.pmb_fwd_of_waterline[0] = 0.4004*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])+0.5235 # this came from 0.780 for container ship, 0.836 bulk carrier (measured from AP, in terms of waterline length)
            data.overall_length_of_waterline[0] = -0.1787*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])+1.1656 # this came from container ship (294.221/279.898), bulk carrer (225/219.258)
            data.stern_point_of_waterline[0] = 0.0644*(data.block_or_prismatic_coefficient[0]*data.midship_coefficient[0])-0.0672 # transom stern position = -0.026*LBP for container ship, transom stern position = -0.017*LBP for oil tanker
        data.pmb_aft_of_waterline[0] = 0.2848*data.cargo_density[0]-0.0528 # comes from 0.044 for container ship 0.232 for bulk carrier (measured from AP, in terms of waterline length)
        data.depth_of_draught[0] = -0.0939*data.cargo_density[0]+1.7099 # comes from 1.678 for container ship or 1.616 for bulk carrier (measured from AP, in terms of waterline length)
        data.transom_of_beam[0] = 0.307 # ship specific, 0.965 for a container ship to maximise load on deck, 0.307 for 15 knot VLCC
        
        data.prop_point_of_waterline[0] = 0.023 # 0.023 for container ship and bulk carrier
        data.aftercutup_of_waterline[0] = 0.038 # 0.038 for 25 knot container ship and a 15 knot vlcc
        data.hull_tip_clear_of_diameter[0] = 0.250 # minimum of 0.25*propeller diameter - ABS Guidance Notes on Ship Vibration April 2006 (Updated Febraury 2014)
        data.keel_tip_clear_of_diameter[0] = 0.035 # clearance between keel and propeller, page 63 Ship Design for Efficiency and Economy, from DNV recommendation
        data.disc_clear_of_diameter[0] = 1.000 # estimated, clearance between multiple propulsors, measured from edge of disc
        data.water_density[0] = 1.024
        
        data.deck_height[0] = 2.800
        data.cofferdam_between_compartments[0] = 0.09
        data.bow_space_length_of_overall_length[0] = 0.07
        data.longitudinal_bulkheads[0] = 0 # for tankers
        data.superstructure_position[0] = 1.00
        data.superstructure_length_in_compartments[0] = 1.00
        data.engine_room_position[0] = 1.00
        # UP TO HERE
        data.hold_width_multiple[0] = 0.00 # CHECK IN PARAMARINE for unitised cargo (or cabins) THIS COULD ALSO BE FOR NON UNITISED CARGO??? SHOULD BE MEASURED AT AMIDSHIPS
        data.primary_structure_density_multiplier[0] = 1.00
        data.secondary_structure_density_multiplier[0] = 1.00
        data.propeller_blades[0] = 4
        data.cpp_efficiency_relative_to_fpp[0] = 98.5
        data.direct_drive_efficiency[0] = 99.5
        data.mechanical_transmission_efficiency[0] = 98.5
        data.waste_heat_recovery_fitted[0] = 0
        data.waste_heat_recovery_design_point[0] = 75
        data.shaft_generator_fitted[0] = 1
        data.shaft_generator_maximum_power[0] = 0
        data.shaft_generator_pto_efficiency[0] = 96.2
        data.shaft_generator_pti_efficiency[0] = 93.3
        data.electrical_propulsion_efficiency[0] = 94.7
        data.maximum_electrical_power_available[0] = 0
        data.maximum_heat_power_available[0] = 0
        
        data.profile_name_1[0] = ""
        data.profile_cargo_or_draught_1[0] = ""
        data.profile_location_1[0] = ""
        data.profile_main_energy_source_1[0] = ""
        data.profile_auxiliary_energy_source_1[0] = ""
        data.profile_heat_energy_source_1[0] = ""
        data.profile_shaft_generator_1[0] = ""
        data.profile_electrical_power_demand_1[0] = 0
        data.profile_heat_power_demand_1[0] = 0
        data.profile_time_1[0] = 0
        data.profile_name_2[0] = ""
        data.profile_cargo_or_draught_2[0] = ""
        data.profile_location_2[0] = ""
        data.profile_main_energy_source_2[0] = ""
        data.profile_auxiliary_energy_source_2[0] = ""
        data.profile_heat_energy_source_2[0] = ""
        data.profile_shaft_generator_2[0] = ""
        data.profile_electrical_power_demand_2[0] = 0
        data.profile_heat_power_demand_2[0] = 0
        data.profile_time_2[0] = 0
        data.profile_name_3[0] = ""
        data.profile_cargo_or_draught_3[0] = ""
        data.profile_location_3[0] = ""
        data.profile_main_energy_source_3[0] = ""
        data.profile_auxiliary_energy_source_3[0] = ""
        data.profile_heat_energy_source_3[0] = ""
        data.profile_shaft_generator_3[0] = ""
        data.profile_electrical_power_demand_3[0] = 0
        data.profile_heat_power_demand_3[0] = 0
        data.profile_time_3[0] = 0
        data.profile_name_4[0] = ""
        data.profile_cargo_or_draught_4[0] = ""
        data.profile_location_4[0] = ""
        data.profile_main_energy_source_4[0] = ""
        data.profile_auxiliary_energy_source_4[0] = ""
        data.profile_heat_energy_source_4[0] = ""
        data.profile_shaft_generator_4[0] = ""
        data.profile_electrical_power_demand_4[0] = 0
        data.profile_heat_power_demand_4[0] = 0
        data.profile_time_4[0] = 0
        data.profile_name_5[0] = ""
        data.profile_cargo_or_draught_5[0] = ""
        data.profile_location_5[0] = ""
        data.profile_main_energy_source_5[0] = ""
        data.profile_auxiliary_energy_source_5[0] = ""
        data.profile_heat_energy_source_5[0] = ""
        data.profile_shaft_generator_5[0] = ""
        data.profile_electrical_power_demand_5[0] = 0
        data.profile_heat_power_demand_5[0] = 0
        data.profile_time_5[0] = 0
        
        actions.set_values_in_entry_widgets()
        
    def set_values_in_entry_widgets(*args):
        
        # set values in entry widgets
        ship_name_entry.input.set(data.ship_name[0])
        cargo_type_entry.input.set(data.cargo_type[0])
        cargo_density_entry.input.set(data.cargo_density[0])
        design_speed_entry.input.set(data.design_speed[0])
        cargo_utilisation_in_design_entry.input.set(data.cargo_utilisation_in_design[0])
        cargo_capacity_entry.input.set(data.cargo_capacity[0])
        cargo_capacity_units_entry.input.set(data.cargo_capacity_units[0])
        personnel_entry.input.set(data.personnel[0])
        powering_margin_entry.input.set(data.powering_margin[0])
        propulsion_type_entry.input.set(data.propulsion_type[0])
        propulsors_entry.input.set(data.propulsors[0])
        set_beam_or_draught_entry.input.set(data.set_beam_or_draught[0])
        beam_or_draught_entry.input.set(data.beam_or_draught[0])
        set_waterline_or_overall_entry.input.set(data.set_waterline_or_overall[0])
        waterline_or_overall_entry.input.set(data.waterline_or_overall[0])
        compartment_length_units_entry.input.set(data.compartment_length_units[0])
        compartment_length_or_no_entry.input.set(data.compartment_length_or_no[0])
        
        endurance_entry.input.set(data.endurance[0])
        bow_thruster_entry.input.set(data.bow_thruster[0])
        midship_coefficient_entry.input.set(data.midship_coefficient[0])
        set_block_or_prismatic_coefficient_entry.input.set(data.set_block_or_prismatic_coefficient[0])
        block_or_prismatic_coefficient_entry.input.set(data.block_or_prismatic_coefficient[0])
        
        waterline_number_entry.input.set(data.waterline_number[0])
        waterline_and_transom_overlap_entry.input.set(data.waterline_and_transom_overlap[0])
        flare_angle_entry.input.set(data.flare_angle[0])
        deadrise_angle_entry.input.set(data.deadrise_angle[0])
        bow_angle_entry.input.set(data.bow_angle[0])
        pmb_angle_entry.input.set(data.pmb_angle[0])
        stern_slope_angle_entry.input.set(data.stern_slope_angle[0])
        pmb_fwd_of_waterline_entry.input.set(data.pmb_fwd_of_waterline[0])
        pmb_aft_of_waterline_entry.input.set(data.pmb_aft_of_waterline[0])
        depth_of_draught_entry.input.set(data.depth_of_draught[0])
        overall_length_of_waterline_entry.input.set(data.overall_length_of_waterline[0])
        transom_of_beam_entry.input.set(data.transom_of_beam[0])
        stern_point_of_waterline_entry.input.set(data.stern_point_of_waterline[0])
        prop_point_of_waterline_entry.input.set(data.prop_point_of_waterline[0])
        aftercutup_of_waterline_entry.input.set(data.aftercutup_of_waterline[0])
        hull_tip_clear_of_diameter_entry.input.set(data.hull_tip_clear_of_diameter[0])
        keel_tip_clear_of_diameter_entry.input.set(data.keel_tip_clear_of_diameter[0])
        disc_clear_of_diameter_entry.input.set(data.disc_clear_of_diameter[0])
        water_density_entry.input.set(data.water_density[0])
        
        deck_height_entry.input.set(data.deck_height[0])
        cofferdam_between_compartments_entry.input.set(data.cofferdam_between_compartments[0])
        bow_space_length_of_overall_length_entry.input.set(data.bow_space_length_of_overall_length[0])
        longitudinal_bulkheads_entry.input.set(data.longitudinal_bulkheads[0])
        superstructure_position_entry.input.set(data.superstructure_position[0])
        superstructure_length_in_compartments_entry.input.set(data.superstructure_length_in_compartments[0])
        engine_room_position_entry.input.set(data.engine_room_position[0])
        hold_width_multiple_entry.input.set(data.hold_width_multiple[0])
        primary_structure_density_multiplier_entry.input.set(data.primary_structure_density_multiplier[0])
        secondary_structure_density_multiplier_entry.input.set(data.secondary_structure_density_multiplier[0])
        propeller_blades_entry.input.set(data.propeller_blades[0])
        cpp_efficiency_relative_to_fpp_entry.input.set(data.cpp_efficiency_relative_to_fpp[0])
        direct_drive_efficiency_entry.input.set(data.direct_drive_efficiency[0])
        mechanical_transmission_efficiency_entry.input.set(data.mechanical_transmission_efficiency[0])
        waste_heat_recovery_fitted_entry.input.set(data.waste_heat_recovery_fitted[0])
        waste_heat_recovery_design_point_entry.input.set(data.waste_heat_recovery_design_point[0])
        shaft_generator_fitted_entry.input.set(data.shaft_generator_fitted[0])
        shaft_generator_maximum_power_entry.input.set(data.shaft_generator_maximum_power[0])
        shaft_generator_pto_efficiency_entry.input.set(data.shaft_generator_pto_efficiency[0])
        shaft_generator_pti_efficiency_entry.input.set(data.shaft_generator_pti_efficiency[0])
        electrical_propulsion_efficiency_entry.input.set(data.electrical_propulsion_efficiency[0])
        maximum_electrical_power_available_entry.input.set(data.maximum_electrical_power_available[0])
        maximum_heat_power_available_entry.input.set(data.maximum_heat_power_available[0])
        
        profile_name_1_entry.input.set(data.profile_name_1[0])
        profile_cargo_or_draught_1_entry.input.set(data.profile_cargo_or_draught_1[0])
        profile_location_1_entry.input.set(data.profile_location_1[0])
        profile_main_energy_source_1_entry.input.set(data.profile_main_energy_source_1[0])
        profile_auxiliary_energy_source_1_entry.input.set(data.profile_auxiliary_energy_source_1[0])
        profile_heat_energy_source_1_entry.input.set(data.profile_heat_energy_source_1[0])
        profile_shaft_generator_1_entry.input.set(data.profile_shaft_generator_1[0])
        profile_electrical_power_demand_1_entry.input.set(data.profile_electrical_power_demand_1[0])
        profile_heat_power_demand_1_entry.input.set(data.profile_heat_power_demand_1[0])
        profile_time_1_entry.input.set(data.profile_time_1[0])
        profile_name_2_entry.input.set(data.profile_name_2[0])
        profile_cargo_or_draught_2_entry.input.set(data.profile_cargo_or_draught_2[0])
        profile_location_2_entry.input.set(data.profile_location_2[0])
        profile_main_energy_source_2_entry.input.set(data.profile_main_energy_source_2[0])
        profile_auxiliary_energy_source_2_entry.input.set(data.profile_auxiliary_energy_source_2[0])
        profile_heat_energy_source_2_entry.input.set(data.profile_heat_energy_source_2[0])
        profile_shaft_generator_2_entry.input.set(data.profile_shaft_generator_2[0])
        profile_electrical_power_demand_2_entry.input.set(data.profile_electrical_power_demand_2[0])
        profile_heat_power_demand_2_entry.input.set(data.profile_heat_power_demand_2[0])
        profile_time_2_entry.input.set(data.profile_time_2[0])
        profile_name_3_entry.input.set(data.profile_name_3[0])
        profile_cargo_or_draught_3_entry.input.set(data.profile_cargo_or_draught_3[0])
        profile_location_3_entry.input.set(data.profile_location_3[0])
        profile_main_energy_source_3_entry.input.set(data.profile_main_energy_source_3[0])
        profile_auxiliary_energy_source_3_entry.input.set(data.profile_auxiliary_energy_source_3[0])
        profile_heat_energy_source_3_entry.input.set(data.profile_heat_energy_source_3[0])
        profile_shaft_generator_3_entry.input.set(data.profile_shaft_generator_3[0])
        profile_electrical_power_demand_3_entry.input.set(data.profile_electrical_power_demand_3[0])
        profile_heat_power_demand_3_entry.input.set(data.profile_heat_power_demand_3[0])
        profile_time_3_entry.input.set(data.profile_time_3[0])
        profile_name_4_entry.input.set(data.profile_name_4[0])
        profile_cargo_or_draught_4_entry.input.set(data.profile_cargo_or_draught_4[0])
        profile_location_4_entry.input.set(data.profile_location_4[0])
        profile_main_energy_source_4_entry.input.set(data.profile_main_energy_source_4[0])
        profile_auxiliary_energy_source_4_entry.input.set(data.profile_auxiliary_energy_source_4[0])
        profile_heat_energy_source_4_entry.input.set(data.profile_heat_energy_source_4[0])
        profile_shaft_generator_4_entry.input.set(data.profile_shaft_generator_4[0])
        profile_electrical_power_demand_4_entry.input.set(data.profile_electrical_power_demand_4[0])
        profile_heat_power_demand_4_entry.input.set(data.profile_heat_power_demand_4[0])
        profile_time_4_entry.input.set(data.profile_time_4[0])
        profile_name_5_entry.input.set(data.profile_name_5[0])
        profile_cargo_or_draught_5_entry.input.set(data.profile_cargo_or_draught_5[0])
        profile_location_5_entry.input.set(data.profile_location_5[0])
        profile_main_energy_source_5_entry.input.set(data.profile_main_energy_source_5[0])
        profile_auxiliary_energy_source_5_entry.input.set(data.profile_auxiliary_energy_source_5[0])
        profile_heat_energy_source_5_entry.input.set(data.profile_heat_energy_source_5[0])
        profile_shaft_generator_5_entry.input.set(data.profile_shaft_generator_5[0])
        profile_electrical_power_demand_5_entry.input.set(data.profile_electrical_power_demand_5[0])
        profile_heat_power_demand_5_entry.input.set(data.profile_heat_power_demand_5[0])
        profile_time_5_entry.input.set(data.profile_time_5[0])
        
    def update_interface1(*args):
        # update the information that is displayed based on combobox choices
        cargo_capacity_entry.units.configure(state="normal") # reenable to make changes
        cargo_capacity_entry.units.delete("1.0", "2.0") # delete line of text
        if  cargo_capacity_units_entry.input.get() == "tonnes":
            cargo_capacity_entry.units.insert("1.0", "te ")
        elif cargo_capacity_units_entry.input.get() == "cubic metres":
            cargo_capacity_entry.units.insert("1.0", "m3")
        else:
            # print error to text box - not set
            cargo_capacity_entry.units.insert("1.0", "NOT SET ")
        
        cargo_capacity_entry.units.tag_add("superscript", "end -2 chars") # tag last letter
        cargo_capacity_entry.units.tag_configure("superscript", offset=4) # superscript letter
        cargo_capacity_entry.units.configure(state="disabled") # do not allow user to edit
        
    def update_interface2(*args):
        # update the information that is displayed based on combobox choices
        compartment_length_or_no_entry.units.configure(state="normal") # reenable to make changes
        compartment_length_or_no_entry.units.delete("1.0", "2.0") # delete line of text
        if  compartment_length_units_entry.input.get() == "compartment length":
            compartment_length_or_no_entry.units.insert("1.0", "m ")
        elif compartment_length_units_entry.input.get() == "number of compartments":
            compartment_length_or_no_entry.units.insert("1.0", "")
        else:
            # print error to text box - not set
            compartment_length_or_no_entry.units.insert("1.0", "NOT SET ")
        
        compartment_length_or_no_entry.units.tag_add("superscript", "end -2 chars") # tag last letter
        compartment_length_or_no_entry.units.tag_configure("superscript", offset=4) # superscript letter
        compartment_length_or_no_entry.units.configure(state="disabled") # do not allow user to edit
        
    def load_run_or_queue(*args):
        # IN WORK
        data.ship_name[run] = ""
        # IN WORK
    def save_run_or_queue(*args):
        # IN WORK
        data.ship_name[run] = ""
        # IN WORK
    def add_to_queue(*args):
        # saves variables currently in user interface to rundata class
        # use global run variable
        global run
        # get values shown in entry widgets and assign to rundata class
        if run == 0:
            rundata.ship_name[run] = ship_name_entry.input.get()
            rundata.cargo_type[run] = cargo_type_entry.input.get()
            rundata.cargo_density[run] = cargo_density_entry.input.get()
            rundata.design_speed[run] = design_speed_entry.input.get()
            rundata.cargo_utilisation_in_design[run] = cargo_utilisation_in_design_entry.input.get()
            rundata.cargo_capacity[run] = cargo_capacity_entry.input.get()
            rundata.cargo_capacity_units[run] = cargo_capacity_units_entry.input.get()
            rundata.personnel[run] = personnel_entry.input.get()
            rundata.powering_margin[run] = powering_margin_entry.input.get()
            rundata.propulsion_type[run] = propulsion_type_entry.input.get()
            rundata.propulsors[run] = propulsors_entry.input.get()
            rundata.set_beam_or_draught[run] = set_beam_or_draught_entry.input.get()
            rundata.beam_or_draught[run] = beam_or_draught_entry.input.get()
            rundata.set_waterline_or_overall[run] = set_waterline_or_overall_entry.input.get()
            rundata.waterline_or_overall[run] = waterline_or_overall_entry.input.get()
            rundata.compartment_length_units[run] = compartment_length_units_entry.input.get()
            rundata.compartment_length_or_no[run] = compartment_length_or_no_entry.input.get()
            
            rundata.endurance[run] = endurance_entry.input.get()
            rundata.bow_thruster[run] = bow_thruster_entry.input.get()
            rundata.midship_coefficient[run] = midship_coefficient_entry.input.get()
            rundata.set_block_or_prismatic_coefficient[run] = set_block_or_prismatic_coefficient_entry.input.get()
            rundata.block_or_prismatic_coefficient[run] = block_or_prismatic_coefficient_entry.input.get()
            
            rundata.waterline_number[run] = waterline_number_entry.input.get()
            rundata.waterline_and_transom_overlap[run] = waterline_and_transom_overlap_entry.input.get()
            rundata.flare_angle[run] = flare_angle_entry.input.get()
            rundata.deadrise_angle[run] = deadrise_angle_entry.input.get()
            rundata.bow_angle[run] = bow_angle_entry.input.get()
            rundata.pmb_angle[run] = pmb_angle_entry.input.get()
            rundata.stern_slope_angle[run] = stern_slope_angle_entry.input.get()
            rundata.pmb_fwd_of_waterline[run] = pmb_fwd_of_waterline_entry.input.get()
            rundata.pmb_aft_of_waterline[run] = pmb_aft_of_waterline_entry.input.get()
            rundata.depth_of_draught[run] = depth_of_draught_entry.input.get()
            rundata.overall_length_of_waterline[run] = overall_length_of_waterline_entry.input.get()
            rundata.transom_of_beam[run] = transom_of_beam_entry.input.get()
            rundata.stern_point_of_waterline[run] = stern_point_of_waterline_entry.input.get()
            rundata.prop_point_of_waterline[run] = prop_point_of_waterline_entry.input.get()
            rundata.aftercutup_of_waterline[run] = aftercutup_of_waterline_entry.input.get()
            rundata.hull_tip_clear_of_diameter[run] = hull_tip_clear_of_diameter_entry.input.get()
            rundata.keel_tip_clear_of_diameter[run] = keel_tip_clear_of_diameter_entry.input.get()
            rundata.disc_clear_of_diameter[run] = disc_clear_of_diameter_entry.input.get()
            rundata.water_density[run] = water_density_entry.input.get()
            
            rundata.deck_height[run] = deck_height_entry.input.get()
            rundata.cofferdam_between_compartments[run] = cofferdam_between_compartments_entry.input.get()
            rundata.bow_space_length_of_overall_length[run] = bow_space_length_of_overall_length_entry.input.get()
            rundata.longitudinal_bulkheads[run] = longitudinal_bulkheads_entry.input.get()
            rundata.superstructure_position[run] = superstructure_position_entry.input.get()
            rundata.superstructure_length_in_compartments[run] = superstructure_length_in_compartments_entry.input.get()
            rundata.engine_room_position[run] = engine_room_position_entry.input.get()
            rundata.hold_width_multiple[run] = hold_width_multiple_entry.input.get()
            rundata.primary_structure_density_multiplier[run] = primary_structure_density_multiplier_entry.input.get()
            rundata.secondary_structure_density_multiplier[run] = secondary_structure_density_multiplier_entry.input.get()
            rundata.propeller_blades[run] = propeller_blades_entry.input.get()
            rundata.cpp_efficiency_relative_to_fpp[run] = cpp_efficiency_relative_to_fpp_entry.input.get()
            rundata.direct_drive_efficiency[run] = direct_drive_efficiency_entry.input.get()
            rundata.mechanical_transmission_efficiency[run] = mechanical_transmission_efficiency_entry.input.get()
            rundata.waste_heat_recovery_fitted[run] = waste_heat_recovery_fitted_entry.input.get()
            rundata.waste_heat_recovery_design_point[run] = waste_heat_recovery_design_point_entry.input.get()
            rundata.shaft_generator_fitted[run] = shaft_generator_fitted_entry.input.get()
            rundata.shaft_generator_maximum_power[run] = shaft_generator_maximum_power_entry.input.get()
            rundata.shaft_generator_pto_efficiency[run] = shaft_generator_pto_efficiency_entry.input.get()
            rundata.shaft_generator_pti_efficiency[run] = shaft_generator_pti_efficiency_entry.input.get()
            rundata.electrical_propulsion_efficiency[run] = electrical_propulsion_efficiency_entry.input.get()
            rundata.maximum_electrical_power_available[run] = maximum_electrical_power_available_entry.input.get()
            rundata.maximum_heat_power_available[run] = maximum_heat_power_available_entry.input.get()
            
            rundata.profile_name_1[run] = profile_name_1_entry.input.get()
            rundata.profile_cargo_or_draught_1[run] = profile_cargo_or_draught_1_entry.input.get()
            rundata.profile_location_1[run] = profile_location_1_entry.input.get()
            rundata.profile_main_energy_source_1[run] = profile_main_energy_source_1_entry.input.get()
            rundata.profile_auxiliary_energy_source_1[run] = profile_auxiliary_energy_source_1_entry.input.get()
            rundata.profile_heat_energy_source_1[run] = profile_heat_energy_source_1_entry.input.get()
            rundata.profile_shaft_generator_1[run] = profile_shaft_generator_1_entry.input.get()
            rundata.profile_electrical_power_demand_1[run] = profile_electrical_power_demand_1_entry.input.get()
            rundata.profile_heat_power_demand_1[run] = profile_heat_power_demand_1_entry.input.get()
            rundata.profile_time_1[run] = profile_time_1_entry.input.get()
            rundata.profile_name_2[run] = profile_name_2_entry.input.get()
            rundata.profile_cargo_or_draught_2[run] = profile_cargo_or_draught_2_entry.input.get()
            rundata.profile_location_2[run] = profile_location_2_entry.input.get()
            rundata.profile_main_energy_source_2[run] = profile_main_energy_source_2_entry.input.get()
            rundata.profile_auxiliary_energy_source_2[run] = profile_auxiliary_energy_source_2_entry.input.get()
            rundata.profile_heat_energy_source_2[run] = profile_heat_energy_source_2_entry.input.get()
            rundata.profile_shaft_generator_2[run] = profile_shaft_generator_2_entry.input.get()
            rundata.profile_electrical_power_demand_2[run] = profile_electrical_power_demand_2_entry.input.get()
            rundata.profile_heat_power_demand_2[run] = profile_heat_power_demand_2_entry.input.get()
            rundata.profile_time_2[run] = profile_time_2_entry.input.get()
            rundata.profile_name_3[run] = profile_name_3_entry.input.get()
            rundata.profile_cargo_or_draught_3[run] = profile_cargo_or_draught_3_entry.input.get()
            rundata.profile_location_3[run] = profile_location_3_entry.input.get()
            rundata.profile_main_energy_source_3[run] = profile_main_energy_source_3_entry.input.get()
            rundata.profile_auxiliary_energy_source_3[run] = profile_auxiliary_energy_source_3_entry.input.get()
            rundata.profile_heat_energy_source_3[run] = profile_heat_energy_source_3_entry.input.get()
            rundata.profile_shaft_generator_3[run] = profile_shaft_generator_3_entry.input.get()
            rundata.profile_electrical_power_demand_3[run] = profile_electrical_power_demand_3_entry.input.get()
            rundata.profile_heat_power_demand_3[run] = profile_heat_power_demand_3_entry.input.get()
            rundata.profile_time_3[run] = profile_time_3_entry.input.get()
            rundata.profile_name_4[run] = profile_name_4_entry.input.get()
            rundata.profile_cargo_or_draught_4[run] = profile_cargo_or_draught_4_entry.input.get()
            rundata.profile_location_4[run] = profile_location_4_entry.input.get()
            rundata.profile_main_energy_source_4[run] = profile_main_energy_source_4_entry.input.get()
            rundata.profile_auxiliary_energy_source_4[run] = profile_auxiliary_energy_source_4_entry.input.get()
            rundata.profile_heat_energy_source_4[run] = profile_heat_energy_source_4_entry.input.get()
            rundata.profile_shaft_generator_4[run] = profile_shaft_generator_4_entry.input.get()
            rundata.profile_electrical_power_demand_4[run] = profile_electrical_power_demand_4_entry.input.get()
            rundata.profile_heat_power_demand_4[run] = profile_heat_power_demand_4_entry.input.get()
            rundata.profile_time_4[run] = profile_time_4_entry.input.get()
            rundata.profile_name_5[run] = profile_name_5_entry.input.get()
            rundata.profile_cargo_or_draught_5[run] = profile_cargo_or_draught_5_entry.input.get()
            rundata.profile_location_5[run] = profile_location_5_entry.input.get()
            rundata.profile_main_energy_source_5[run] = profile_main_energy_source_5_entry.input.get()
            rundata.profile_auxiliary_energy_source_5[run] = profile_auxiliary_energy_source_5_entry.input.get()
            rundata.profile_heat_energy_source_5[run] = profile_heat_energy_source_5_entry.input.get()
            rundata.profile_shaft_generator_5[run] = profile_shaft_generator_5_entry.input.get()
            rundata.profile_electrical_power_demand_5[run] = profile_electrical_power_demand_5_entry.input.get()
            rundata.profile_heat_power_demand_5[run] = profile_heat_power_demand_5_entry.input.get()
            rundata.profile_time_5[run] = profile_time_5_entry.input.get()
        else:
            rundata.ship_name.append(ship_name_entry.input.get())
            rundata.cargo_type.append(cargo_type_entry.input.get())
            rundata.cargo_density.append(cargo_density_entry.input.get())
            rundata.design_speed.append(design_speed_entry.input.get())
            rundata.cargo_utilisation_in_design.append(cargo_utilisation_in_design_entry.input.get())
            rundata.cargo_capacity.append(cargo_capacity_entry.input.get())
            rundata.cargo_capacity_units.append(cargo_capacity_units_entry.input.get())
            rundata.personnel.append(personnel_entry.input.get())
            rundata.powering_margin.append(powering_margin_entry.input.get())
            rundata.propulsion_type.append(propulsion_type_entry.input.get())
            rundata.propulsors.append(propulsors_entry.input.get())
            rundata.set_beam_or_draught.append(set_beam_or_draught_entry.input.get())
            rundata.beam_or_draught.append(beam_or_draught_entry.input.get())
            rundata.set_waterline_or_overall.append(set_waterline_or_overall_entry.input.get())
            rundata.waterline_or_overall.append(waterline_or_overall_entry.input.get())
            rundata.compartment_length_units.append(compartment_length_units_entry.input.get())
            rundata.compartment_length_or_no.append(compartment_length_or_no_entry.input.get())
            
            rundata.endurance.append(endurance_entry.input.get())
            rundata.bow_thruster.append(bow_thruster_entry.input.get())
            rundata.midship_coefficient.append(midship_coefficient_entry.input.get())
            rundata.set_block_or_prismatic_coefficient.append(set_block_or_prismatic_coefficient_entry.input.get())
            rundata.block_or_prismatic_coefficient.append(block_or_prismatic_coefficient_entry.input.get())
            
            rundata.waterline_number.append(waterline_number_entry.input.get())
            rundata.waterline_and_transom_overlap.append(waterline_and_transom_overlap_entry.input.get())
            rundata.flare_angle.append(flare_angle_entry.input.get())
            rundata.deadrise_angle.append(deadrise_angle_entry.input.get())
            rundata.bow_angle.append(bow_angle_entry.input.get())
            rundata.pmb_angle.append(pmb_angle_entry.input.get())
            rundata.stern_slope_angle.append(stern_slope_angle_entry.input.get())
            rundata.pmb_fwd_of_waterline.append(pmb_fwd_of_waterline_entry.input.get())
            rundata.pmb_aft_of_waterline.append(pmb_aft_of_waterline_entry.input.get())
            rundata.depth_of_draught.append(depth_of_draught_entry.input.get())
            rundata.overall_length_of_waterline.append(overall_length_of_waterline_entry.input.get())
            rundata.transom_of_beam.append(transom_of_beam_entry.input.get())
            rundata.stern_point_of_waterline.append(stern_point_of_waterline_entry.input.get())
            rundata.prop_point_of_waterline.append(prop_point_of_waterline_entry.input.get())
            rundata.aftercutup_of_waterline.append(aftercutup_of_waterline_entry.input.get())
            rundata.hull_tip_clear_of_diameter.append(hull_tip_clear_of_diameter_entry.input.get())
            rundata.keel_tip_clear_of_diameter.append(keel_tip_clear_of_diameter_entry.input.get())
            rundata.disc_clear_of_diameter.append(disc_clear_of_diameter_entry.input.get())
            rundata.water_density.append(water_density_entry.input.get())
            
            rundata.deck_height.append(deck_height_entry.input.get())
            rundata.cofferdam_between_compartments.append(cofferdam_between_compartments_entry.input.get())
            rundata.bow_space_length_of_overall_length.append(bow_space_length_of_overall_length_entry.input.get())
            rundata.longitudinal_bulkheads.append(longitudinal_bulkheads_entry.input.get())
            rundata.superstructure_position.append(superstructure_position_entry.input.get())
            rundata.superstructure_length_in_compartments.append(superstructure_length_in_compartments_entry.input.get())
            rundata.engine_room_position.append(engine_room_position_entry.input.get())
            rundata.hold_width_multiple.append(hold_width_multiple_entry.input.get())
            rundata.primary_structure_density_multiplier.append(primary_structure_density_multiplier_entry.input.get())
            rundata.secondary_structure_density_multiplier.append(secondary_structure_density_multiplier_entry.input.get())
            rundata.propeller_blades.append(propeller_blades_entry.input.get())
            rundata.cpp_efficiency_relative_to_fpp.append(cpp_efficiency_relative_to_fpp_entry.input.get())
            rundata.direct_drive_efficiency.append(direct_drive_efficiency_entry.input.get())
            rundata.mechanical_transmission_efficiency.append(mechanical_transmission_efficiency_entry.input.get())
            rundata.waste_heat_recovery_fitted.append(waste_heat_recovery_fitted_entry.input.get())
            rundata.waste_heat_recovery_design_point.append(waste_heat_recovery_design_point_entry.input.get())
            rundata.shaft_generator_fitted.append(shaft_generator_fitted_entry.input.get())
            rundata.shaft_generator_maximum_power.append(shaft_generator_maximum_power_entry.input.get())
            rundata.shaft_generator_pto_efficiency.append(shaft_generator_pto_efficiency_entry.input.get())
            rundata.shaft_generator_pti_efficiency.append(shaft_generator_pti_efficiency_entry.input.get())
            rundata.electrical_propulsion_efficiency.append(electrical_propulsion_efficiency_entry.input.get())
            rundata.maximum_electrical_power_available.append(maximum_electrical_power_available_entry.input.get())
            rundata.maximum_heat_power_available.append(maximum_heat_power_available_entry.input.get())
            
            rundata.profile_name_1.append(profile_name_1_entry.input.get())
            rundata.profile_cargo_or_draught_1.append(profile_cargo_or_draught_1_entry.input.get())
            rundata.profile_location_1.append(profile_location_1_entry.input.get())
            rundata.profile_main_energy_source_1.append(profile_main_energy_source_1_entry.input.get())
            rundata.profile_auxiliary_energy_source_1.append(profile_auxiliary_energy_source_1_entry.input.get())
            rundata.profile_heat_energy_source_1.append(profile_heat_energy_source_1_entry.input.get())
            rundata.profile_shaft_generator_1.append(profile_shaft_generator_1_entry.input.get())
            rundata.profile_electrical_power_demand_1.append(profile_electrical_power_demand_1_entry.input.get())
            rundata.profile_heat_power_demand_1.append(profile_heat_power_demand_1_entry.input.get())
            rundata.profile_time_1.append(profile_time_1_entry.input.get())
            rundata.profile_name_2.append(profile_name_2_entry.input.get())
            rundata.profile_cargo_or_draught_2.append(profile_cargo_or_draught_2_entry.input.get())
            rundata.profile_location_2.append(profile_location_2_entry.input.get())
            rundata.profile_main_energy_source_2.append(profile_main_energy_source_2_entry.input.get())
            rundata.profile_auxiliary_energy_source_2.append(profile_auxiliary_energy_source_2_entry.input.get())
            rundata.profile_heat_energy_source_2.append(profile_heat_energy_source_2_entry.input.get())
            rundata.profile_shaft_generator_2.append(profile_shaft_generator_2_entry.input.get())
            rundata.profile_electrical_power_demand_2.append(profile_electrical_power_demand_2_entry.input.get())
            rundata.profile_heat_power_demand_2.append(profile_heat_power_demand_2_entry.input.get())
            rundata.profile_time_2.append(profile_time_2_entry.input.get())
            rundata.profile_name_3.append(profile_name_3_entry.input.get())
            rundata.profile_cargo_or_draught_3.append(profile_cargo_or_draught_3_entry.input.get())
            rundata.profile_location_3.append(profile_location_3_entry.input.get())
            rundata.profile_main_energy_source_3.append(profile_main_energy_source_3_entry.input.get())
            rundata.profile_auxiliary_energy_source_3.append(profile_auxiliary_energy_source_3_entry.input.get())
            rundata.profile_heat_energy_source_3.append(profile_heat_energy_source_3_entry.input.get())
            rundata.profile_shaft_generator_3.append(profile_shaft_generator_3_entry.input.get())
            rundata.profile_electrical_power_demand_3.append(profile_electrical_power_demand_3_entry.input.get())
            rundata.profile_heat_power_demand_3.append(profile_heat_power_demand_3_entry.input.get())
            rundata.profile_time_3.append(profile_time_3_entry.input.get())
            rundata.profile_name_4.append(profile_name_4_entry.input.get())
            rundata.profile_cargo_or_draught_4.append(profile_cargo_or_draught_4_entry.input.get())
            rundata.profile_location_4.append(profile_location_4_entry.input.get())
            rundata.profile_main_energy_source_4.append(profile_main_energy_source_4_entry.input.get())
            rundata.profile_auxiliary_energy_source_4.append(profile_auxiliary_energy_source_4_entry.input.get())
            rundata.profile_heat_energy_source_4.append(profile_heat_energy_source_4_entry.input.get())
            rundata.profile_shaft_generator_4.append(profile_shaft_generator_4_entry.input.get())
            rundata.profile_electrical_power_demand_4.append(profile_electrical_power_demand_4_entry.input.get())
            rundata.profile_heat_power_demand_4.append(profile_heat_power_demand_4_entry.input.get())
            rundata.profile_time_4.append(profile_time_4_entry.input.get())
            rundata.profile_name_5.append(profile_name_5_entry.input.get())
            rundata.profile_cargo_or_draught_5.append(profile_cargo_or_draught_5_entry.input.get())
            rundata.profile_location_5.append(profile_location_5_entry.input.get())
            rundata.profile_main_energy_source_5.append(profile_main_energy_source_5_entry.input.get())
            rundata.profile_auxiliary_energy_source_5.append(profile_auxiliary_energy_source_5_entry.input.get())
            rundata.profile_heat_energy_source_5.append(profile_heat_energy_source_5_entry.input.get())
            rundata.profile_shaft_generator_5.append(profile_shaft_generator_5_entry.input.get())
            rundata.profile_electrical_power_demand_5.append(profile_electrical_power_demand_5_entry.input.get())
            rundata.profile_heat_power_demand_5.append(profile_heat_power_demand_5_entry.input.get())
            rundata.profile_time_5.append(profile_time_5_entry.input.get())
            
        # conversions from user interface to variables for rest of program
        if rundata.cargo_capacity_units[run] == "tonnes":
            if run == 0:
                rundata.cargo_capacity_te = [rundata.cargo_capacity[0]]
                rundata.cargo_capacity_m3 = [rundata.cargo_capacity[0]/rundata.cargo_density[0]]
            else:
                rundata.cargo_capacity_te.append(rundata.cargo_capacity[run])
                rundata.cargo_capacity_m3.append(rundata.cargo_capacity[run]/rundata.cargo_density[run])
        else:
            # cargo capacity is in metres cubed or there is an ERROR
            if run == 0:
                rundata.cargo_capacity_m3 = [rundata.cargo_capacity[0]]
                rundata.cargo_capacity_te = [rundata.cargo_density[0]*rundata.cargo_capacity[0]]
            else:
                rundata.cargo_capacity_m3.append(rundata.cargo_capacity[run])
                rundata.cargo_capacity_te.append(rundata.cargo_density[run]*rundata.cargo_capacity[run])
        if rundata.set_block_or_prismatic_coefficient[run] == "block coefficient":
            if run == 0:
                rundata.block_coefficient = [rundata.block_or_prismatic_coefficient[0]]
                rundata.prismatic_coefficient = [rundata.block_coefficient[0]/rundata.midship_coefficient[0]]
            else:
                rundata.block_coefficient.append(rundata.block_or_prismatic_coefficient[run])
                rundata.prismatic_coefficient.append(rundata.block_coefficient[run]/rundata.midship_coefficient[run])
        else:
            # set_block_or_prismatic_coefficient[run] = ["prismatic coefficient"] or there is an ERROR
            if run == 0:
                rundata.prismatic_coefficient = [rundata.block_or_prismatic_coefficient[0]]
                rundata.block_coefficient = [rundata.midship_coefficient[0]*rundata.prismatic_coefficient[0]]
            else:
                rundata.prismatic_coefficient.append(rundata.block_or_prismatic_coefficient[run])
                rundata.block_coefficient.append(rundata.midship_coefficient[run]*rundata.prismatic_coefficient[run])
        if rundata.set_waterline_or_overall[run] == "waterline length":
            if run == 0:
                rundata.waterline_length = [rundata.waterline_or_overall[0]]
                rundata.overall_length = [rundata.overall_length_of_waterline[0]*rundata.waterline_or_overall[0]]
            else:
                rundata.waterline_length.append(rundata.waterline_or_overall[run])
                rundata.overall_length.append(rundata.overall_length_of_waterline[run]*rundata.waterline_or_overall[run])
        else:
            # set_waterline_or_overall[run] == "overall length" or there is an ERROR
            if run == 0:
                rundata.waterline_length = [rundata.waterline_or_overall[0]/rundata.overall_length_of_waterline[0]]
                rundata.overall_length = [rundata.waterline_or_overall[0]]
            else:
                rundata.waterline_length.append(rundata.waterline_or_overall[run]/rundata.overall_length_of_waterline[run])
                rundata.overall_length.append(rundata.waterline_or_overall[run])
        # convert perentages to decimal
        rundata.cargo_utilisation_in_design[run] = rundata.cargo_utilisation_in_design[run]*0.01
        # convert angles to radians
        rundata.flare_angle[run] = rundata.flare_angle[run]*np.pi/180
        rundata.deadrise_angle[run] = rundata.deadrise_angle[run]*np.pi/180
        rundata.bow_angle[run] = rundata.bow_angle[run]*np.pi/180
        rundata.pmb_angle[run] = rundata.pmb_angle[run]*np.pi/180
        rundata.stern_slope_angle[run] = rundata.stern_slope_angle[run]*np.pi/180
        # increase run number
        run += 1
        
    def run_queue(*args):
        # run queued items, pass user selected and static variables to main
        # function in main.py
        import main
        main.main(fuel, rundata, run)

# Main Program/User Interface Layout
# - - - - - - - - - - - - - -  - - -
# define root window and title
root = Tk() # creates an instance of the class tkinter.Tk
root.title("Ship Impact Model")
# stop user from resizing window
root.resizable("false","false")
# can also use .geometry to control size of initial window, for example:
# root.geometry("widthxheight+pixelsfromleftedge+pixelsbelowtopedge")
# minus (-) is used to measure from right edge and bottom edge
# root.geometry("600x400+0+0")
# (can also set a min and max size using .min size and .max size)

# create a setup frame with a label in the top left
setupframe = ttk.Labelframe(root, text="Setup")
setupframe.pack(side="top")
# pack fits container or widget within another container or parent window
# pack can also use the arguments side, fill and anchor
# side direction (from tkinter module) can be UP, DOWN, LEFT, RIGHT
# fill can force widget/container to use more space and can be NONE, X, Y, BOTH
# anchor tells where widget/container should be arranged:
# NW, N, NE, E, SE, S, SW, W, CENTER

# create a frame in setup frame to put action buttons in
setupbuttonframetop = ttk.LabelFrame(setupframe, text="Presets")
setupbuttonframetop.pack(side="top")
# put buttons in frame
set_default_button = buttons(setupbuttonframetop,
                             "Reset fields to Default values",
                             actions.set_default_data)
clear_fields_button = buttons(setupbuttonframetop, "Clear all fields",
                              actions.clear_all_fields)
container_ship_button = buttons(setupbuttonframetop, "Container Ship",
                                actions.container_ship)
vlcc_button = buttons(setupbuttonframetop, "VLCC",
                      actions.vlcc)
load_run_or_queue_button = buttons(setupbuttonframetop,
                                   "Load an existing Run or Queue",
                                   actions.load_run_or_queue)
# any fields that should always be visible can be added here
setupframealwaysshown = ttk.Frame(setupframe)
setupframealwaysshown.pack(side="top")
setupframeleft = ttk.Frame(setupframealwaysshown)
setupframeleft.pack(side="left", anchor="s")
setupframeright = ttk.Frame(setupframealwaysshown)
setupframeright.pack(side="left", anchor="s")
ship_name_entry = labelentry(setupframeleft, "ship (or run) name: ",
                             StringVar(), data.ship_name[run], "")
cargo_type_entry = labellist(setupframeleft, "cargo type: ", StringVar(),
                             "{containers} {oil} {chemicals} {bulk} {liquid natual gas} {passenger} {wheeled cargo} {none} {not specified}",
                                data.cargo_type[run])
cargo_density_entry = labelentry(setupframeleft, "cargo density: ",
                                 DoubleVar(), data.cargo_density[run], "te/m3")                       
bow_thruster_entry = labelcheck(setupframeright, "bow thruster installed: ",
                                data.bow_thruster[run])
design_speed_entry = labelentry(setupframeright, "design speed: ",
                                DoubleVar(), data.design_speed[run], "knots ")
cargo_utilisation_in_design_entry = labelentry(setupframeright, "cargo utilisation in design: ",
                                 DoubleVar(), data.cargo_utilisation_in_design[run], "% ")
cargo_capacity_entry = labelentry(setupframeleft, "maximum cargo capacity: ",
                                  DoubleVar(), data.cargo_capacity[run], "te ")
cargo_capacity_units_entry = labellist(setupframeright,
                                       "cargo capacity units: ", StringVar(),
                                        "{tonnes} {cubic metres}",
                                        data.cargo_capacity_units[run])
# displayed units after cargo capacity based on user choice
cargo_capacity_units_entry.entry.bind("<<ComboboxSelected>>",
                                      actions.update_interface1)
personnel_entry = labelentry(setupframeleft,
                             "personnel (crew and passengers): ", IntVar(),
                             data.personnel[run], "")
endurance_entry = labelentry(setupframeright, "endurance: ", DoubleVar(),
                             data.endurance[run], "days ")
propulsion_type_entry = labellist(setupframeleft, "propulsion type: ",
                                  StringVar(),
                                  "{fixed pitch propeller} {controllable pitch propeller} {(FPP or CPP) pod}",
                                  data.propulsion_type[run])
propulsors_entry = labellist(setupframeright, "propulsors: ", IntVar(),
                             "1 2", data.propulsors[run])
powering_margin_entry = labelentry(setupframeleft,
                                   "powering margin (on MCR): ", DoubleVar(),
                                    data.powering_margin[run], "% ")
midship_coefficient_entry = labelentry(setupframeright,
                                       "midship coefficient: ",
                                       DoubleVar(), data.midship_coefficient[run],
                                        "")
set_beam_or_draught_entry = labellist(setupframeleft, "set: ", StringVar(),
                                      "{beam} {draught}",
                                        data.set_beam_or_draught[run])
beam_or_draught_entry = labelentry(setupframeright, "to: ", DoubleVar(),
                                   data.beam_or_draught[run], "m ")
set_waterline_or_overall_entry = labellist(setupframeleft, "set: ",
                                           StringVar(),
                                     "{waterline length} {overall length}",
                                        data.set_waterline_or_overall[run])
waterline_or_overall_entry = labelentry(setupframeright, "to: ", DoubleVar(),
                                        data.waterline_or_overall[run], "m ")
compartment_length_units_entry = labellist(setupframeleft, "set: ",
                                           StringVar(),
                            "{compartment length} {number of compartments}",
                                        data.compartment_length_units[run])
## displayed units after compartments space based on user choice
compartment_length_units_entry.entry.bind("<<ComboboxSelected>>",
                                          actions.update_interface2)
compartment_length_or_no_entry = labelentry(setupframeright, "to: ",
                            DoubleVar(), data.compartment_length_or_no[run],
                                            "m ")
set_block_or_prismatic_coefficient_entry = labellist(setupframeleft, "set: ",
                                                     StringVar(),
                                                    "{block coefficient} {prismatic coefficient}",
                                                    data.set_block_or_prismatic_coefficient[run])
block_or_prismatic_coefficient_entry = labelentry(setupframeright, "to: ",
                                                  DoubleVar(), data.block_or_prismatic_coefficient[run],
                                                    "")        
# create a notebook in setup frame below the buttons to put the entry area in
entrytabs = ttk.Notebook(setupframe)
entrytabs.pack(side="top")
entrytab2 = ttk.Frame(entrytabs)
entrytab3 = ttk.Frame(entrytabs)
entrytab4 = ttk.Frame(entrytabs)
entrytabs.add(entrytab2, text="Hull Generation")
entrytab2left = ttk.Frame(entrytab2)
entrytab2left.pack(side="left", anchor="n")
entrytab2right = ttk.Frame(entrytab2)
entrytab2right.pack(side="left", anchor="n")
waterline_number_entry = labelentry(entrytab2left,
                                "number of waterlines to split hull into: ",
                                IntVar(), data.waterline_number[run], "")
waterline_and_transom_overlap_entry = labelentry(entrytab2left,
                    "vertical overlap between design draught and transom: ",
                    DoubleVar(),data.waterline_and_transom_overlap[run],"")
flare_angle_entry = labelentry(entrytab2left,
                               "amidships flare(+)/tumblehome(-) from vertical: ",
                                DoubleVar(), data.flare_angle[run], "o")
deadrise_angle_entry = labelentry(entrytab2left,
                                  "amidships deadrise from horizontal: ",
                                  DoubleVar(), data.deadrise_angle[run], "o")
bow_angle_entry = labelentry(entrytab2left, "bow rake from vertical: ",
                             DoubleVar(), data.bow_angle[run], "o")
pmb_angle_entry = labelentry(entrytab2left, "parallel midbody angle: ",
                             DoubleVar(), data.pmb_angle[run], "o")
stern_slope_angle_entry = labelentry(entrytab2left, "stern slope angle: ",
                                     DoubleVar(), data.stern_slope_angle[run],
                                     "o")
pmb_fwd_of_waterline_entry = labelentry(entrytab2left,
                                        "extent of parallel midbody forward: ",
                                        DoubleVar(),
                                        data.pmb_fwd_of_waterline[run],
                                        "")
pmb_aft_of_waterline_entry = labelentry(entrytab2left,
                                        "extent of parallel midbody aft: ",
                                        DoubleVar(),
                                        data.pmb_aft_of_waterline[run],
                                        "")
depth_of_draught_entry = labelentry(entrytab2right,
                                    "hull depth to draught ratio: ",
                                    DoubleVar(), data.depth_of_draught[run],
                                    "")
overall_length_of_waterline_entry = labelentry(entrytab2right,
                                "overall length/waterline length ratio: ",
                                DoubleVar(),
                                data.overall_length_of_waterline[run],
                                "")
transom_of_beam_entry = labelentry(entrytab2right,
                                   "transom length/beam ratio: ", DoubleVar(),
                                    data.transom_of_beam[run],"")
stern_point_of_waterline_entry = labelentry(entrytab2right,
                                        "stern position/waterline length ratio: ",
                                        DoubleVar(),
                                        data.stern_point_of_waterline[run],
                                        "")
prop_point_of_waterline_entry = labelentry(entrytab2right,
                            "propulsor position/waterline length ratio: ",
                            DoubleVar(),
                            data.prop_point_of_waterline[run], "")
aftercutup_of_waterline_entry = labelentry(entrytab2right,
                            "aftercutup/waterline length ratio: ",
                            DoubleVar(),
                            data.aftercutup_of_waterline[run], "")
hull_tip_clear_of_diameter_entry = labelentry(entrytab2right,
                            "propulsor clearance from hull/diameter ratio: ",
                            DoubleVar(), data.hull_tip_clear_of_diameter[run],
                            "")
keel_tip_clear_of_diameter_entry = labelentry(entrytab2right,
                            "propulsor clearance from keel/diameter ratio: ",
                            DoubleVar(), data.keel_tip_clear_of_diameter[run],
                            "")
disc_clear_of_diameter_entry = labelentry(entrytab2right,
                            "clearance between propulsors/diameter ratio: ",
                            DoubleVar(), data.disc_clear_of_diameter[run],
                            "")
water_density_entry = labelentry(entrytab2right,
                            "water density: ",
                            DoubleVar(), data.water_density[run],
                            "te/m3")
entrytabs.add(entrytab3, text="Layout and Machinery")
entrytab3left = ttk.Frame(entrytab3)
entrytab3left.pack(side="left", anchor="n")
entrytab3right = ttk.Frame(entrytab3)
entrytab3right.pack(side="left", anchor="n")
deck_height_entry = labelentry(entrytab3left, "deck height: ",
                               DoubleVar(),
                               data.deck_height[run], "m ")
cofferdam_between_compartments_entry = labelentry(entrytab3left,
                                    "cofferdam/bulkhead width: ",
                                    DoubleVar(),
                                    data.cofferdam_between_compartments[run],
                                    "m ")
bow_space_length_of_overall_length_entry = labelentry(entrytab3left,
                                "empty bow length/overall length ratio: ",
                                DoubleVar(),
                                data.bow_space_length_of_overall_length[run],
                                "m ")
longitudinal_bulkheads_entry = labelentry(entrytab3left,
                                          "number of longitudinal bulkheads: ",
                                          DoubleVar(),
                                          data.longitudinal_bulkheads[run], "")
superstructure_position_entry = labelentry(entrytab3left,
                                    "superstructure compartment from aft: ",
                                    DoubleVar(),
                                    data.superstructure_position[run], "")
superstructure_length_in_compartments_entry = labelentry(entrytab3left,
                        "superstructure length (in compartments): ",
                        DoubleVar(),
                        data.superstructure_length_in_compartments[run], "")
engine_room_position_entry = labelentry(entrytab3right,
                                    "engine room compartment from aft: ",
                                    DoubleVar(),
                                    data.engine_room_position[run], "")
hold_width_multiple_entry = labelentry(entrytab3right,
                                "width of unitised cargo (if applicable): ",
                                DoubleVar(), data.hold_width_multiple[run], "")
primary_structure_density_multiplier_entry = labelentry(entrytab3right,
                        "primary structure density multiplier: ", DoubleVar(),
                        data.primary_structure_density_multiplier[run], "")
secondary_structure_density_multiplier_entry = labelentry(entrytab3right,
                        "secondary structure density multiplier: ", DoubleVar(),
                        data.secondary_structure_density_multiplier[run], "")
propeller_blades_entry = labelentry(entrytab3right, "number of propeller blades: ",
                                    DoubleVar(), data.propeller_blades[run], "")
cpp_efficiency_relative_to_fpp_entry = labelentry(entrytab3right,
                                "CPP/FPP efficiency: ", DoubleVar(),
                                data.cpp_efficiency_relative_to_fpp[run], "% ")
direct_drive_efficiency_entry = labelentry(entrytab3right,
                                "direct drive efficiency: ", DoubleVar(),
                                data.direct_drive_efficiency[run], "% ")
mechanical_transmission_efficiency_entry = labelentry(entrytab3right,
                            "mechanical transmission efficiency: ", DoubleVar(),
                            data.mechanical_transmission_efficiency[run], "% ")
waste_heat_recovery_fitted_entry = labelcheck(entrytab3right,
                                        "waste heat recovery installed: ",
                                        data.waste_heat_recovery_fitted[run])
waste_heat_recovery_design_point_entry = labelentry(entrytab3right,
            "waste heat recovery design point of engine power: ", DoubleVar(),
            data.waste_heat_recovery_design_point[run], "% ")
shaft_generator_fitted_entry = labelcheck(entrytab3left,
                                        "shaft generator installed: ",
                                        data.shaft_generator_fitted[run])
shaft_generator_maximum_power_entry = labelentry(entrytab3left,
                            "maximum shaft generator power: ", DoubleVar(),
                            data.shaft_generator_maximum_power[run], "% ")
shaft_generator_pto_efficiency_entry = labelentry(entrytab3left,
                                "PTO efficiency: ", DoubleVar(),
                                data.shaft_generator_pto_efficiency[run], "% ")
shaft_generator_pti_efficiency_entry = labelentry(entrytab3left,
                                "PTI efficiency: ", DoubleVar(),
                                data.shaft_generator_pti_efficiency[run], "% ")            
electrical_propulsion_efficiency_entry = labelentry(entrytab3left,
            "electrical propulsion efficiency: ", DoubleVar(),
            data.electrical_propulsion_efficiency[run], "% ")
maximum_electrical_power_available_entry = labelentry(entrytab3right,
            "maximum electrical power: ", DoubleVar(),
            data.maximum_electrical_power_available[run], "kW ")
maximum_heat_power_available_entry = labelentry(entrytab3right,
            "maximum heat/boiler power: ", DoubleVar(),
            data.maximum_heat_power_available[run], "kW ")
entrytabs.add(entrytab4, text="Operational Profile")
entrytab4profile1 = ttk.Frame(entrytab4)
entrytab4profile1.pack(side="top")
entrytab4profile1left = ttk.Frame(entrytab4profile1)
entrytab4profile1left.pack(side="left", anchor="n")
entrytab4profile1middleleft = ttk.Frame(entrytab4profile1)
entrytab4profile1middleleft.pack(side="left", anchor="n")
entrytab4profile1middleright = ttk.Frame(entrytab4profile1)
entrytab4profile1middleright.pack(side="left", anchor="n")
entrytab4profile1right = ttk.Frame(entrytab4profile1)
entrytab4profile1right.pack(side="left", anchor="n")
entrytab4profile2 = ttk.Frame(entrytab4)
entrytab4profile2.pack(side="top")
entrytab4profile2left = ttk.Frame(entrytab4profile2)
entrytab4profile2left.pack(side="left", anchor="n")
entrytab4profile2middleleft = ttk.Frame(entrytab4profile2)
entrytab4profile2middleleft.pack(side="left", anchor="n")
entrytab4profile2middleright = ttk.Frame(entrytab4profile2)
entrytab4profile2middleright.pack(side="left", anchor="n")
entrytab4profile2right = ttk.Frame(entrytab4profile2)
entrytab4profile2right.pack(side="left", anchor="n")
entrytab4profile3 = ttk.Frame(entrytab4)
entrytab4profile3.pack(side="top")
entrytab4profile3left = ttk.Frame(entrytab4profile3)
entrytab4profile3left.pack(side="left", anchor="n")
entrytab4profile3middleleft = ttk.Frame(entrytab4profile3)
entrytab4profile3middleleft.pack(side="left", anchor="n")
entrytab4profile3middleright = ttk.Frame(entrytab4profile3)
entrytab4profile3middleright.pack(side="left", anchor="n")
entrytab4profile3right = ttk.Frame(entrytab4profile3)
entrytab4profile3right.pack(side="left", anchor="n")
entrytab4profile4 = ttk.Frame(entrytab4)
entrytab4profile4.pack(side="top")
entrytab4profile4left = ttk.Frame(entrytab4profile4)
entrytab4profile4left.pack(side="left", anchor="n")
entrytab4profile4middleleft = ttk.Frame(entrytab4profile4)
entrytab4profile4middleleft.pack(side="left", anchor="n")
entrytab4profile4middleright = ttk.Frame(entrytab4profile4)
entrytab4profile4middleright.pack(side="left", anchor="n")
entrytab4profile4right = ttk.Frame(entrytab4profile4)
entrytab4profile4right.pack(side="left", anchor="n")
entrytab4profile5 = ttk.Frame(entrytab4)
entrytab4profile5.pack(side="top")
entrytab4profile5left = ttk.Frame(entrytab4profile5)
entrytab4profile5left.pack(side="left", anchor="n")
entrytab4profile5middleleft = ttk.Frame(entrytab4profile5)
entrytab4profile5middleleft.pack(side="left", anchor="n")
entrytab4profile5middleright = ttk.Frame(entrytab4profile5)
entrytab4profile5middleright.pack(side="left", anchor="n")
entrytab4profile5right = ttk.Frame(entrytab4profile5)
entrytab4profile5right.pack(side="left", anchor="n")
profile_name_1_entry = labelentry(entrytab4profile1left, "profile name: ",
                                  StringVar(), data.profile_name_1[run], "")                        
profile_location_1_entry = labelentry(entrytab4profile1left,
                "filename: ", StringVar(), data.profile_location_1[run], "")
profile_cargo_or_draught_1_entry = labellist(entrytab4profile1left,
                        "profile demands: ", StringVar(), "{not used} {cargo} {draught}",
                        data.profile_cargo_or_draught_1[run])
profile_main_energy_source_1_entry = labellist(entrytab4profile1middleleft,
                        "propulsion fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_main_energy_source_1[run])
profile_shaft_generator_1_entry = labellist(entrytab4profile1middleleft,
                        "PTO/PTI mode: ", StringVar(),
                        "{Not Used} {PTO only} {PTI only} {PTO/PTI}",
                        data.profile_shaft_generator_1[run])
profile_electrical_power_demand_1_entry = labelentry(entrytab4profile1middleright,
                            "electrical demand: ", DoubleVar(),
                            data.profile_electrical_power_demand_1[run], "kW ")
profile_heat_power_demand_1_entry = labelentry(entrytab4profile1middleright,
                            "heat/boiler demand: ", DoubleVar(),
                            data.profile_heat_power_demand_1[run], "kW ")
profile_time_1_entry = labelentry(entrytab4profile1middleright,
                            "time in condition: ", DoubleVar(),
                            data.profile_time_1[run], "hrs/% ")
profile_auxiliary_energy_source_1_entry = labellist(entrytab4profile1right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_auxiliary_energy_source_1[run])
profile_heat_energy_source_1_entry = labellist(entrytab4profile1right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_heat_energy_source_1[run])
profile_name_2_entry = labelentry(entrytab4profile2left, "profile name: ",
                                  StringVar(), data.profile_name_2[run], "")                        
profile_location_2_entry = labelentry(entrytab4profile2left,
                "filename: ", StringVar(), data.profile_location_2[run], "")
profile_cargo_or_draught_2_entry = labellist(entrytab4profile2left,
                        "profile demands: ", StringVar(), "{not used} {cargo} {draught}",
                        data.profile_cargo_or_draught_2[run])
profile_main_energy_source_2_entry = labellist(entrytab4profile2middleleft,
                        "propulsion fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_main_energy_source_2[run])
profile_shaft_generator_2_entry = labellist(entrytab4profile2middleleft,
                        "PTO/PTI mode: ", StringVar(),
                        "{Not Used} {PTO only} {PTI only} {PTO/PTI}",
                        data.profile_shaft_generator_2[run])
profile_electrical_power_demand_2_entry = labelentry(entrytab4profile2middleright,
                            "electrical demand: ", DoubleVar(),
                            data.profile_electrical_power_demand_2[run], "kW ")
profile_heat_power_demand_2_entry = labelentry(entrytab4profile2middleright,
                            "heat/boiler demand: ", DoubleVar(),
                            data.profile_heat_power_demand_2[run], "kW ")
profile_time_2_entry = labelentry(entrytab4profile2middleright,
                            "time in condition: ", DoubleVar(),
                            data.profile_time_2[run], "hrs/% ")
profile_auxiliary_energy_source_2_entry = labellist(entrytab4profile2right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_auxiliary_energy_source_2[run])
profile_heat_energy_source_2_entry = labellist(entrytab4profile2right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_heat_energy_source_2[run])
profile_name_3_entry = labelentry(entrytab4profile3left, "profile name: ",
                                  StringVar(), data.profile_name_3[run], "")                        
profile_location_3_entry = labelentry(entrytab4profile3left,
                "filename: ", StringVar(), data.profile_location_3[run], "")
profile_cargo_or_draught_3_entry = labellist(entrytab4profile3left,
                        "profile demands: ", StringVar(), "{not used} {cargo} {draught}",
                        data.profile_cargo_or_draught_3[run])
profile_main_energy_source_3_entry = labellist(entrytab4profile3middleleft,
                        "propulsion fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_main_energy_source_3[run])
profile_shaft_generator_3_entry = labellist(entrytab4profile3middleleft,
                        "PTO/PTI mode: ", StringVar(),
                        "{Not Used} {PTO only} {PTI only} {PTO/PTI}",
                        data.profile_shaft_generator_3[run])
profile_electrical_power_demand_3_entry = labelentry(entrytab4profile3middleright,
                            "electrical demand: ", DoubleVar(),
                            data.profile_electrical_power_demand_3[run], "kW ")
profile_heat_power_demand_3_entry = labelentry(entrytab4profile3middleright,
                            "heat/boiler demand: ", DoubleVar(),
                            data.profile_heat_power_demand_3[run], "kW ")
profile_time_3_entry = labelentry(entrytab4profile3middleright,
                            "time in condition: ", DoubleVar(),
                            data.profile_time_3[run], "hrs/% ")
profile_auxiliary_energy_source_3_entry = labellist(entrytab4profile3right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_auxiliary_energy_source_3[run])
profile_heat_energy_source_3_entry = labellist(entrytab4profile3right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_heat_energy_source_3[run])
profile_name_4_entry = labelentry(entrytab4profile4left, "profile name: ",
                                  StringVar(), data.profile_name_4[run], "")                        
profile_location_4_entry = labelentry(entrytab4profile4left,
                "filename: ", StringVar(), data.profile_location_4[run], "")
profile_cargo_or_draught_4_entry = labellist(entrytab4profile4left,
                        "profile demands: ", StringVar(), "{not used} {cargo} {draught}",
                        data.profile_cargo_or_draught_4[run])
profile_main_energy_source_4_entry = labellist(entrytab4profile4middleleft,
                        "propulsion fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_main_energy_source_4[run])
profile_shaft_generator_4_entry = labellist(entrytab4profile4middleleft,
                        "PTO/PTI mode: ", StringVar(),
                        "{Not Used} {PTO only} {PTI only} {PTO/PTI}",
                        data.profile_shaft_generator_4[run])
profile_electrical_power_demand_4_entry = labelentry(entrytab4profile4middleright,
                            "electrical demand: ", DoubleVar(),
                            data.profile_electrical_power_demand_4[run], "kW ")
profile_heat_power_demand_4_entry = labelentry(entrytab4profile4middleright,
                            "heat/boiler demand: ", DoubleVar(),
                            data.profile_heat_power_demand_4[run], "kW ")
profile_time_4_entry = labelentry(entrytab4profile4middleright,
                            "time in condition: ", DoubleVar(),
                            data.profile_time_4[run], "hrs/% ")
profile_auxiliary_energy_source_4_entry = labellist(entrytab4profile4right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_auxiliary_energy_source_4[run])
profile_heat_energy_source_4_entry = labellist(entrytab4profile4right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_heat_energy_source_4[run])                            
profile_name_5_entry = labelentry(entrytab4profile5left, "profile name: ",
                                  StringVar(), data.profile_name_5[run], "")                        
profile_location_5_entry = labelentry(entrytab4profile5left,
                "filename: ", StringVar(), data.profile_location_5[run], "")
profile_cargo_or_draught_5_entry = labellist(entrytab4profile5left,
                        "profile demands: ", StringVar(), "{not used} {cargo} {draught}",
                        data.profile_cargo_or_draught_5[run])
profile_main_energy_source_5_entry = labellist(entrytab4profile5middleleft,
                        "propulsion fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_main_energy_source_5[run])
profile_shaft_generator_5_entry = labellist(entrytab4profile5middleleft,
                        "PTO/PTI mode: ", StringVar(),
                        "{Not Used} {PTO only} {PTI only} {PTO/PTI}",
                        data.profile_shaft_generator_5[run])
profile_electrical_power_demand_5_entry = labelentry(entrytab4profile5middleright,
                            "electrical demand: ", DoubleVar(),
                            data.profile_electrical_power_demand_5[run], "kW ")
profile_heat_power_demand_5_entry = labelentry(entrytab4profile5middleright,
                            "heat/boiler demand: ", DoubleVar(),
                            data.profile_heat_power_demand_5[run], "kW ")
profile_time_5_entry = labelentry(entrytab4profile5middleright,
                            "time in condition: ", DoubleVar(),
                            data.profile_time_5[run], "hrs/% ")
profile_auxiliary_energy_source_5_entry = labellist(entrytab4profile5right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_auxiliary_energy_source_5[run])
profile_heat_energy_source_5_entry = labellist(entrytab4profile5right,
                        "fuel: ", StringVar(), fuel.fuel_names,
                        data.profile_heat_energy_source_5[run])
# create a run frame with a label in the top left
runframe = ttk.Labelframe(root, text="Run")
runframe.pack(side="top")
# put buttons in frame
add_to_queue_button = buttons(runframe, "Add to Run Queue",
                              actions.add_to_queue)
load_run_or_queue_button = buttons(runframe,
                                   "Run Queued", actions.run_queue)
# user interface event loop (must be placed at end of where user interface is)
root.mainloop()
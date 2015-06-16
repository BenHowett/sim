# list of variables from user interface:
rd.ship_name[0] = "container_ship"
rd.cargo_type[0] = "containers"
rd.cargo_density[0] = 0.34
rd.design_speed[0] = 25.0
rd.cargo_utilisation_in_design[0] = 100.0
rd.cargo_capacity[0] = 35032.00
rd.cargo_capacity_units[0] = "tonnes"
rd.personnel[0] = 21
rd.powering_margin[0] = 25.00
rd.propulsion_type[0] = "fixed pitched propeller"
rd.propulsors[0] = 1 # might be 2 for larger container ships
rd.set_beam_or_draught[0] = "beam"
rd.beam_or_draught[0] = 32.20
rd.set_waterline_or_overall[0] = "overall length"
rd.waterline_or_overall[0] = 294.20
rd.compartment_length_units[0] = "compartment length"
rd.compartment_length_or_no[0] = 12.340 # for 2 TEUs

rd.endurance[0] = 35.00
rd.bow_thruster[0] = 1
rd.midship_coefficient[0] = 0.98
rd.set_block_or_prismatic_coefficient[0] = "prismatic coefficient"
rd.block_or_prismatic_coefficient[0] = 0.65

rd.waterline_number[0] = 30
rd.waterline_and_transom_overlap[0] = 0.00
rd.flare_angle[0] = 0.00
rd.deadrise_angle[0] = 0.00
rd.bow_angle[0] = 14.000
rd.stern_slope_angle[0] = 7.785
rd.pmb_fwd_of_waterline[0] = 0.780
rd.pmb_aft_of_waterline[0] = 0.044
rd.depth_of_draught[0] = 1.678
rd.overall_length_of_waterline[0] = 1.026
rd.transom_of_beam[0] = 0.965
rd.stern_point_of_waterline[0] = -0.026

rd.prop_point_of_waterline[0] = 0.023
rd.aftercutup_of_waterline[0] = 0.038
rd.hull_tip_clear_of_diameter[0] = 0.250
rd.keel_tip_clear_of_diameter[0] = 0.035
rd.disc_clear_of_diameter[0] = 1.000

rd.deck_height[0] = 2.800
rd.cofferdam_between_compartments[0] = 1.60
rd.bow_space_length_of_overall_length[0] = 0.07
rd.longitudinal_bulkheads[0] = 0 # for tankers
rd.superstructure_position[0] = 1.00
rd.superstructure_length_in_compartments[0] = 1.00
rd.engine_room_position[0] = 1.00
rd.hold_width_multiple[0] = 0.00 # for unitised cargo (or cabins)
rd.primary_structure_density_multiplier[0] = 1.00
rd.secondary_structure_density_multiplier[0] = 1.00
rd.propeller_blades[0] = 4
rd.cpp_efficiency_relative_to_fpp[0] = 98.5
rd.direct_drive_efficiency[0] = 99.5
rd.mechanical_transmission_efficiency[0] = 98.5
rd.waste_heat_recovery_fitted[0] = 0
rd.waste_heat_recovery_design_point[0] = 75
rd.shaft_generator_fitted[0] = 0
rd.shaft_generator_maximum_power[0] = 0
rd.shaft_generator_pto_efficiency[0] = 96.2
rd.shaft_generator_pti_efficiency[0] = 93.3
rd.electrical_propulsion_efficiency[0] = 94.7
rd.maximum_electrical_power_available[0] = 0
rd.maximum_heat_power_available[0] = 0

rd.profile_name_1[0] = ""
rd.profile_cargo_or_draught_1[0] = ""
rd.profile_location_1[0] = ""
rd.profile_main_energy_source_1[0] = ""
rd.profile_auxiliary_energy_source_1[0] = ""
rd.profile_heat_energy_source_1[0] = ""
rd.profile_shaft_generator_1[0] = ""
rd.profile_electrical_power_demand_1[0] = 0
rd.profile_heat_power_demand_1[0] = 0
rd.profile_time_1[0] = 0
rd.profile_name_2[0] = ""
rd.profile_cargo_or_draught_2[0] = ""
rd.profile_location_2[0] = ""
rd.profile_main_energy_source_2[0] = ""
rd.profile_auxiliary_energy_source_2[0] = ""
rd.profile_heat_energy_source_2[0] = ""
rd.profile_shaft_generator_2[0] = ""
rd.profile_electrical_power_demand_2[0] = 0
rd.profile_heat_power_demand_2[0] = 0
rd.profile_time_2[0] = 0
rd.profile_name_3[0] = ""
rd.profile_cargo_or_draught_3[0] = ""
rd.profile_location_3[0] = ""
rd.profile_main_energy_source_3[0] = ""
rd.profile_auxiliary_energy_source_3[0] = ""
rd.profile_heat_energy_source_3[0] = ""
rd.profile_shaft_generator_3[0] = ""
rd.profile_electrical_power_demand_3[0] = 0
rd.profile_heat_power_demand_3[0] = 0
rd.profile_time_3[0] = 0
rd.profile_name_4[0] = ""
rd.profile_cargo_or_draught_4[0] = ""
rd.profile_location_4[0] = ""
rd.profile_main_energy_source_4[0] = ""
rd.profile_auxiliary_energy_source_4[0] = ""
rd.profile_heat_energy_source_4[0] = ""
rd.profile_shaft_generator_4[0] = ""
rd.profile_electrical_power_demand_4[0] = 0
rd.profile_heat_power_demand_4[0] = 0
rd.profile_time_4[0] = 0
rd.profile_name_5[0] = ""
rd.profile_cargo_or_draught_5[0] = ""
rd.profile_location_5[0] = ""
rd.profile_main_energy_source_5[0] = ""
rd.profile_auxiliary_energy_source_5[0] = ""
rd.profile_heat_energy_source_5[0] = ""
rd.profile_shaft_generator_5[0] = ""
rd.profile_electrical_power_demand_5[0] = 0
rd.profile_heat_power_demand_5[0] = 0
rd.profile_time_5[0] = 0

# List of iterative variables in program:
displacement
KG
righting_moment
design.displaced_volume
design.prop_diameter
design.displaced_volume
design.draught
design.beam
design.waterline_length
design.waterplane_coefficient
design.viscous_resistance
design.additional_thust
design.total_resistance

# calculated in transversebouyancyandmoment
GZ
righting_moment

# other (may add to interface if time):
water_density
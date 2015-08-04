# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:10:05 2015

@author: David Trodden <David.Trodden@ncl.ac.uk>
version: 0.2

"""

from GEM import run_gem

def engines(case_study, design_torque, design_rpm, operation_torque,
            operation_rpm, design_auxiliary_load, operation_auxiliary_load,
            pto, eta_pto, propulsion_type, sea_margin, main_engine_margin,
            light_running_factor, aux_engine_margin, main_engine_type,
            no_of_shafts, aux_engine_type, propulsion_fuel_type,
            auxiliary_fuel_type, green_technologies):

    """
    This function calls the Generic Engine Model and returns characteristics
    of the given engine, fuel and machinery specifications for the specified
    running conditions.
    
    INPUT
    -----
    case_study: string describing case

    design_torque:   Torque required in calm water, clean hull conditions [kNm]
    design_rpm: RPM required in calm water, clean hull conditions [rpm]

    operation_torque: Torque at present running conditions [kNm]
    operation_rpm:    RPM at present running conditions [rpm]

    design_auxiliary_load:    Design load [kW], ie load at 85% MCR of
                              auxiliary engines.
    operation_auxiliary_load: Load on auxiliary [kW] in running (service)
                              conditions.

    pto:     Power required from installed PTO (zero if no PTO installed).
    eta_pto: Efficiency of PTO.

    propulsion_type: Propeller type boolean, True for controllable pitch,
                     False for fixed pitch.
    
    sea_margin: Extra power on top of that required for calm water propulsion.
                This yields the Service Propulsion Point (SP). [%]
    main_engine_margin: Extra power on top of that required for (SP).
                This yields Maximum Continuous Rated Power (MCR). [%]
    aux_engine_margin: Extra power on top of that required of Maximum
                Continuous Rated Power (MCR). [%]
    light_running_factor: Extra revolutions required to account for fouling of
                hull. This yields the light propeller curve
                (trials conditions). [%]

    main_engine_type: Type of main propulsion engine.
        1 = Slow speed, directly coupled two-stroke
        2 = Medium speed four-stroke
        3 = ... FIXME - complete this list
    no_of_shafts: Number of propeller shafts installed

    aux_engine_type: Type of auxiliary propulsion engine.
        1 = Medium speed four-stroke

    propulsion_fuel_type: Type of fuel used in main propulsion engine
    auxiliary_fuel_type:  Type of fuel used in auxiliary engine
        1 = HFO
        2 = MDO
        3 = LNG
        4 = Methanol
        5 = Hydrogen
        6 = SVO (Soya bean)
        7 = SVO (Rapeseed)
        8 = Bio-Diesel (Soya bean)
        9 = Bio-Diesel (Rapeseed)
        10 = Bio-LNG
        11 = Bio-Methanol
        12 = Bio-Hydrogen
        
    TODO: N.B. EXTREME CAUTION AHEAD!
    Some technologies are mutually exclusive. Saftey checks have NOT yet been
    implimented. For green technology issues, please read manual.

    green_technologies[0]: Boolean, use of low-sulphur fuel (0.5% mass content)
    green_technologies[1]: Boolean, Scrubber fitted?
    green_technologies[2]: Boolean, Direct Water Injection used?
    green_technologies[3]: Boolean, Exhaust Gas Recirculation used?
    green_technologies[4]: Boolean, Selective Catalytic Reduction used?
    green_technologies[5]: Boolean: Humid Air Motor used?
    green_technologies[6]: Boolean, Combustion Air Saturation System used?
    green_technologies[7]: Boolean, Water In Fuel Emulsion used?
    green_technologies[8]: Boolean, Internal Engine Modification used?
                           N.B. The engines in the current database already
                           incorporate IEM

    OUTPUT
    ------
    engine_output is a list of the following characteristics:
    engine_output[0]  = installed main engine power MCR [kW]
    engine_output[1]  = main engine SFOC at running point [t/kWh]
    engine_output[2]  = mass of main engine [kg]
    engine_output[3]  = length of main engine [m]
    engine_output[4]  = specific CO2 emissions from main engine [g/kWh]
    engine_output[5]  = number of aux engines required
    engine_output[6]  = installed _generator_ power from aux engines(kW)
    engine_output[7]  = aux engine SFOC at running point [t/kWh]
    engine_output[8]  = total mass of aux engines [kg]
    engine_output[9]  = length of aux engine(m)
    engine_output[10] = total specific CO2 emissions from aux engine(s) [g/kWh]
    engine_output[11] = % change in CO2 emission from using green technology
    engine_output[12] = % change in SOX emission from using green technology 
    engine_output[13] = % change in NOX emission from using green technology 
    """
    
    # run the Generic Engine Model
    engine_output = run_gem(case_study, design_torque, design_rpm,
                            operation_torque, operation_rpm,
                            design_auxiliary_load, operation_auxiliary_load,
                            pto, eta_pto, propulsion_type, sea_margin,
                            main_engine_margin, light_running_factor,
                            aux_engine_margin, main_engine_type,
                            aux_engine_type, propulsion_fuel_type,
                            auxiliary_fuel_type, green_technologies)

    return engine_output


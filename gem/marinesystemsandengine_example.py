# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:30:24 2015

@author: David Trodden <david.trodden@ncl.ac.uk>


INPUT
-----
CASE_STUDY: string describing case

Q_CALM:   Torque required in calm water, clean hull conditions [kNm]
RPM_CALM: RPM required in calm water, clean hull conditions [rpm]
Q_RUN:    Torque at present running conditions [kNm]
RPM_RUN:  RPM at present running conditions [rpm]

AUX_ENGINE_DESIGN: Design load [kW], ie load at 85% MCR of auxiliary
                   engines.
AUX_ENGINE_RUN:    Load on auxiliary [kW] in running (service) conditions.

PTO:     Power required from installed PTO (zero if no PTO installed).
ETA_PTO: Efficiency of PTO.

CPP: Propeller type boolean, True for controllable pitch, False for
     fixed pitch.

SEA_MARGIN: Extra power on top of that required for calm water propulsion.
            This yields the Service Propulsion Point (SP). [%]
MAIN_ENGINE_MARGIN: Extra power on top of that required for (SP).
            This yields Maximum Continuous Rated Power (MCR). [%]
AUX_ENGINE_MARGIN: Extra power on top of that required of Maximum
            Continuous Rated Power (MCR). [%]
LIGHT_RUNNING_FACTOR: Extra revolutions required to account for fouling of
            hull. This yields the light propeller curve
            (trials conditions). [%]

MAIN_ENGINE_TYPE: Type of main propulsion engine.
    1 = Slow speed, directly coupled two-stroke
    2 = Medium speed four-stroke
    3 = ... FIXME - complete this list
NO_OF_SHAFTS: Number of propeller shafts installed

AUX_ENGINE_TYPE: Type of auxiliary propulsion engine.
    1 = Medium speed four-stroke

FUEL_TYPE_MAIN: Type of fuel used in main propulsion engine
FUEL_TYPE_AUX:  Type of fuel used in auxiliary engine
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

LOW_SULPHUR: Boolean, use of low-sulphur fuel (0.5% mass content)
SCRUBBER:    Boolean, Scrubber fitted?
DWI:         Boolean, Direct Water Injection used?
EGR:         Boolean, Exhaust Gas Recirculation used?
SCR:         Boolean, Selective Catalytic Reduction used?
HAM:         Boolean: Humid Air Motor used?
CASS:        Boolean, Combustion Air Saturation System used?
WIFE:        Boolean, Water In Fuel Emulsion used?
IEM:         Boolean, Internal Engine Modification used? N.B. The engines
             in the current database already incorporate IEM
"""

from marinesystemsandengine import engines


#
# EXAMPLE INPUT DATA
#
# This data will be supplied via the GUI, but is given here as a working
# example.
#
CASE_STUDY = "Test_Case"
#
# MAIN ENGINE POWER REQUIREMENTS
#
#Q_CALM = 4000.0
#RPM_CALM = 72.0
#Q_RUN = 4500.0
#RPM_RUN = 73.0
#
#Q_RUN = 5120.9956 # service conditions when Q_CALM = 4000.0
#RPM_RUN = 75.43364 # service conditions when RPM_CALM = 72.0
#
#
#
##Q_CALM = 1200.0
##RPM_CALM = 82.0
##Q_RUN = 800.0
##RPM_RUN = 78.0
#
Q_CALM = 1123.45
RPM_CALM = 85.0
Q_RUN = 1123.45
RPM_RUN = 85.0

#
# AUXILIARY POWER REQUIREMENTS
#
AUX_ENGINE_DESIGN = 650.0
AUX_ENGINE_RUN = 525.0
#AUX_ENGINE_DESIGN = 38000.0
#AUX_ENGINE_RUN = 8000.0
#
# SHAFT GENERATOR
#
PTO = 0.0
ETA_PTO = 1.0 # TODO: need to implement this
#
# PROPELLER TYPE
#
CPP = False
#
# POWER MARGINS
#
SEA_MARGIN = 0.15
MAIN_ENGINE_MARGIN = 0.10
LIGHT_RUNNING_FACTOR = 0.05
AUX_ENGINE_MARGIN = 0.15
#
# Main Engine Type
#
MAIN_ENGINE_TYPE = 1
NO_OF_SHAFTS = 1 # TODO: need to implement this
#
# Auxiliary Engine Type
#
AUX_ENGINE_TYPE = 1 # currently only four-stroke
#
# Fuel Type
#
FUEL_TYPE_MAIN = 2
FUEL_TYPE_AUX = 1
#
# Energy Saving Technologies
#
# TODO: N.B. EXTREME CAUTION AHEAD!
# Some technologies are mutually exclusive. Saftey checks have NOT yet been
# implimented. For green technology issues, please read manual.
#
# Low Sulphur Fuel
# Asuming fuel to go from 2.7% to 0.5% reduction in Sulphur content by mass,
# there is an associated reduction of 80% SOX emissions, and 20% PM
# Source: http://cleantech.cnss.no/
LOW_SULPHUR = False
#
# Scrubber fitted?
# 90-95% reduction in SOX and 80-85% reduction in PM
# Source: http://cleantech.cnss.no/
SCRUBBER = False
#
# Direct Water Injection
# up to 60% reduction in NOX, 0-2% increase in CO2
# Source: http://cleantech.cnss.no/
DWI = False
#
# Exhaust Gas Recirculation
# 20-85% reductionin NOX
# Source: http://cleantech.cnss.no/
EGR = False
#
# Selective Catalytic Reduction 
# 90-99% reduction in NOX, 25-40% reduction in PM
# Source: http://cleantech.cnss.no/
SCR = False
#
# Humid Air Motor
# 20-80% reduction in NOX
# Source: http://cleantech.cnss.no/
HAM = False
#
# Combustion Air Saturation System
# 30-60% reduction in NOX
# Source: http://cleantech.cnss.no/
CASS = False
#
# Water in fuel emulsion
# 10- 60% reduction in NOX
# Source: http://cleantech.cnss.no/
WIFE = False
#
# Internal Engine Modification
# N.B. The engines in the current database already incorporate these
# modifications
# 30-40% reduction in NOX
# Source: http://cleantech.cnss.no/
IEM = False
#
# END EXAMPLE INPUT DATA
#

#
# translate into John's variable names
case_study = CASE_STUDY
propulsion_type = CPP
propulsion_fuel_type = FUEL_TYPE_MAIN
sea_margin = SEA_MARGIN
main_engine_margin = MAIN_ENGINE_MARGIN
main_engine_type = MAIN_ENGINE_TYPE
aux_engine_margin = AUX_ENGINE_MARGIN
aux_engine_type = AUX_ENGINE_TYPE
light_running_factor = LIGHT_RUNNING_FACTOR
no_of_shafts = NO_OF_SHAFTS
design_torque = Q_CALM
design_rpm = RPM_CALM
operation_torque = Q_RUN
operation_rpm = RPM_RUN
pto = PTO
eta_pto = ETA_PTO
auxiliary_fuel_type = FUEL_TYPE_AUX
design_auxiliary_load = AUX_ENGINE_DESIGN
operation_auxiliary_load = AUX_ENGINE_RUN
green_technologies = [LOW_SULPHUR, SCRUBBER, DWI, EGR, SCR, HAM, CASS, WIFE,
                      IEM]

mse = engines(case_study, design_torque, design_rpm, operation_torque,
              operation_rpm, design_auxiliary_load, operation_auxiliary_load,
              pto, eta_pto, propulsion_type, sea_margin, main_engine_margin,
              light_running_factor, aux_engine_margin, main_engine_type,
              no_of_shafts, aux_engine_type, propulsion_fuel_type,
              auxiliary_fuel_type, green_technologies)

#print("delta SOX =", mse[12], "%")

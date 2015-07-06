# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:10:05 2015

@author: David Trodden <David.Trodden@ncl.ac.uk>



sea_margin [%] Extra power on top of that required for calm water propulsion.
               This yields the Service Propulsion Point (SP).
engine_margin [%] Extra power on top of that required for (SP).
                  This yields Maximum Continuous Rated Power (MCR).
light_running_factor [%] Extra revolutions required to account for fouling
                         of hull. This yields the light propeller curve
                         (trials conditions).

"""


from GEM import run_gem


#
# MAIN ENGINE POWER REQUIREMENTS
#
# example for example, Maersk Batam
CASE_STUDY = "Maersk Batam"
#
Q_TRIAL = 3928.0      # torque at trial conditions [kNm]
RPM_TRIAL = 70.0      # rpm at trial conditions [rpm]
Q_RUN = 4200.0      # torque at present running conditions [kNm]
RPM_RUN = 75.0      # rpm at present running conditions [rpm]
#
# test example for a four-stroke main enigne
# CASE_STUDY = "Test Ship"
#
#Q_TRIAL = 550.0
#RPM_TRIAL = 150.0
#Q_RUN = 600.0
#RPM_TRIAL = 170.0



# FIXME - need to be able to pass a specific engine to the GEM module
# (both main and aux)

#
# HOTEL LOAD POWER REQUIREMENTS
#
# It must be made clear that this requirement does NOT include the power
# requirement from the PTO, this is for aux gen sets ONLY
#
# hotel_load_design = design hotel load, in kW, this is the load
#                     at 85% MCR of GenSet
# hotel_load_service = service hotel load, in kW
HOTEL_LOAD_DESIGN = 650.0
HOTEL_LOAD_SERVICE = 525.0

#
# SHAFT GENERATOR
#
# PTO = hotel power required from installed PTO (zero if no PTO installed)
#PTO = 4.0E+03
PTO = 0.0
ETA_PTO = 1.0 # FIXME need to impliment this

#
# PROPELLER TYPE
#
CPP = False


#
# POWER MARGINS
#
SEA_MARGIN = 0.15  # sea-margin
MAIN_ENGINE_MARGIN = 0.10  # engine-margin
LIGHT_RUNNING_FACTOR = 0.05 # light-running factor
AUX_ENGINE_MARGIN = 0.15 # aux engine margin

#
# Main Engine Type
#
MAIN_ENGINE_TYPE = 1 # Slow speed, directly coupled two-stroke
#MAIN_ENGINE_TYPE = 2 # Medium speed four-stroke

#
# Auxiliary Engine Type
#
AUX_ENGINE_TYPE = 1 # currently only four-stroke

#
# Number of Main Propulsion Engines
#
#NME = 0 FIXME - not completelty necessary, but maybe nice, - impliment this!

#
# Fuel Type
#
FUEL_TYPE_MAIN = 1
FUEL_TYPE_AUX = 1

###############################################################################

run_gem(CASE_STUDY, Q_TRIAL, RPM_TRIAL, Q_RUN, RPM_RUN, HOTEL_LOAD_DESIGN, HOTEL_LOAD_SERVICE, PTO, ETA_PTO, CPP, SEA_MARGIN, MAIN_ENGINE_MARGIN, LIGHT_RUNNING_FACTOR, AUX_ENGINE_MARGIN, MAIN_ENGINE_TYPE, AUX_ENGINE_TYPE, FUEL_TYPE_MAIN, FUEL_TYPE_AUX)


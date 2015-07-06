# -*- coding: utf-8 -*-
"""
Created on Fri May 22 14:56:43 2015

@author: David Trodden <David.Trodden@ncl.ac.uk>



    Fuels examined are those listted in the "Evaluation Studies Report
    Document" Tech. data is predominantly found in
    "SCC Theme 3 Goal and Scope" document

    N.B. in the Evaluations Studies document, fuels are listed such as
    "Bio HFO" and "Bio MDO". In the literatre ("SCC Theme 3 Goal and Scope",
    and others) There is no distinguishment between the two. There is
    Straight Vegetable Oil (SVO) and Bio-Diesel,
    which is made by processing SVO.

    Bio-Methanol LCV is from "The Swedish Knowledge Centre for Renewable
    Transportation Fuels" http://www.f3centre.se/fact-sheet/methanol

    Other LCV values are taken from "Determination of energy cost of electrical energy on board sea-going vessels"
    By Dr. Wild, Ingenieurbüro, GmbH
        

    Fossil Fuel
    ===========
    Index   Type                   LCV (MJ/kg)
    1       HFO                    40.435
    2       MDO                    42.7
    3       LNG                    45.0
    4       Methanol               19.93
    5       Hydrogen               120.0

    Bio-Derived Fuel
    ================
    Index   Type                   LCV (MJ/kg)
    6       SVO (Soya bean)        39.62
    7       SVO (Rapeseed)         36.5 (average)
    8       Bio-Diesel (Soya bean) 39.75
    9       Bio-Diesel (Rapeseed)  37.0
    10      Bio-LNG                ???
    11      Bio-Methanol           19.8
    12      Bio-Hydrogen           ???


dictionary is of the form key: [Name, LCV, CO2 Emission Factor]

The units of CO2 Emission Factor are tonnes of CO2 per tonne of fuel


EF source for methanol:http://biofuel.org.uk/bioalcohols.html

"""

#fuel_list = {1: ["HFO", 40.435], \
#             2: ["MDO", 42.7],   \
#             3: ["LNG", 45.0],   \
#             4: ["Methanol", 19.93],  \
#             5: ["Hydrogen", 120.0],   \
#             6: ["SVO (Soya bean)", 39.62],  \
#             7: ["Bio-Diesel (Rapeseed)", 36.5],   \
#             8: ["Bio-Diesel (Soya bean)", 39.75],    \
#             9: ["Bio-Diesel (Rapeseed)", 37.0],    \
#             10: ["Bio-LNG", 0.0],   \
#             11: ["Bio-Methanol", 19.8],   \
#             12: ["Bio-Hydrogen", 0.0],   \
#}

# FIXME get values for the rest of the CO2 emission factors
# place-holder of 0.0 has been set for the unkown fuels.

fuel_list = {1: ["HFO", 40.435, 3.114], \
             2: ["MDO", 42.7, 3.206],   \
             3: ["LNG", 45.0, 2.750],   \
             4: ["Methanol", 19.93, 1.37],  \
             5: ["Hydrogen", 120.0, 0.0],   \
             6: ["SVO (Soya bean)", 39.62, 0.0],  \
             7: ["Bio-Diesel (Rapeseed)", 36.5, 0.0],   \
             8: ["Bio-Diesel (Soya bean)", 39.75, 0.0],    \
             9: ["Bio-Diesel (Rapeseed)", 37.0, 0.0],    \
             10: ["Bio-LNG", 0.0, 0.0],   \
             11: ["Bio-Methanol", 19.8, 0.0],   \
             12: ["Bio-Hydrogen", 0.0, 0.0],   \
}

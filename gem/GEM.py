# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:05:48 2015

@author: David Trodden <David.Trodden@ncl.ac.uk>
"""

import sys
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from engine_db import two_stroke_main_db, four_stroke_main_db, four_stroke_aux_db
from fuel_db import fuel_list


def delta_sfoc(pc_mep, gradient, intercept):
    """
    This function will return the change in Specific Fuel Oil Consumption,
    relative to L1 on the engine layout diagram, for a given percentage
    of MEP.

    The equation for the relationship takes the form of a straight line:
    y = mx+c
    Where m and c are obtained from graphs published in MAN Project Guides.
    The values of m and c will vary depending on the engine.
    gradient = m
    intercept = c
    """
    return gradient*pc_mep+intercept



def mep_pc_l1(mcr_p, mcr_rpm, l1_kw_c, l3_kw_c, n_piston, rpm_min, rpm_max):
    """
    Calculate percentage MEP, given MCR and power at L1

    mcr_p = Maximum Continuous Rated Power [kW]
    mcr_rpm = Speed at MCR [rpm]
    l1_kw_c = Power at L1 [kW] per cylinder
    n_piston = number of cylinders
    N.B. One needs to exercise caution when lifting data from loglog plots!
    """
    # calculate slope of constant MEP line from L3 to L1
    mep_slope = np.log10(l1_kw_c/l3_kw_c)/np.log10(rpm_max/rpm_min)

    # calculate where constant MEP line intersects the ordinate axis
    mep_o = mcr_p/pow(mcr_rpm, mep_slope)

    # calculate where the constant MEP line through MP intersects the
    # 100% rpm line
    mep_y = mep_o*pow(rpm_max, mep_slope)

    # calculate the % MEP of point MP (wrt L1)
    mep_pc_mp = 100.0-((l1_kw_c*n_piston-mep_y)/(l1_kw_c*n_piston)*100.0)

    return mep_pc_mp


def sfoc_at_point(sfoc_gradient, sfoc_intercept, pc_mcr, mcr_p, run_p,
                  l1_sfoc, mep_pc_mp, plot=False):
    """
    Calculate FOC at the given running point
    MP = power at MCR
    RP = power at running point
    pc_mcr = percent of SCMR corrseponding to the MEP/SFOC line
    """

    # calculate curve of SFOC [g/kWh] vs MCR [kW]
    #
    # calculate SFOC at 100% SMCR (i.e. point M) on the engine layout diagram
    x_one = pc_mcr[0]/100.0*mcr_p
    y_one = l1_sfoc + delta_sfoc(mep_pc_mp, sfoc_gradient[0], sfoc_intercept[0])

    # calculate SFOC at 70% SMCR
    x_two = pc_mcr[1]/100.0*mcr_p
    y_two = l1_sfoc+delta_sfoc(mep_pc_mp, sfoc_gradient[1], sfoc_intercept[1])

    # calculate SFOC at 50% SMCR
    x_three = pc_mcr[2]/100.0*mcr_p
    y_three = l1_sfoc+delta_sfoc(mep_pc_mp, sfoc_gradient[2], sfoc_intercept[2])

    # create a spline through the data points
    x_i = np.array([x_three, x_two, x_one])
    y_i = np.array([y_three, y_two, y_one])
    order = 2 # spline order: 1 linear, 2 quadratic, 3 cubic ...
    spline = InterpolatedUnivariateSpline(x_i, y_i, k=order)

    # correction for very low MCR
    # this is a crude percentage difference calculation based upon a spline
    # through the 100, 70 and 50 % points, and the curve provided in MAN
    # project guide
    x_four = 0.4*mcr_p
    y_four = spline(0.4*mcr_p)-0.602/100.0*spline(0.4*mcr_p)
    #y_four = s(0.4*MP) # No correction!


    # calculate new spline, corrected for low MCR points
    xi_corrected = np.array([x_four, x_three, x_two, x_one])
    yi_corrected = np.array([y_four, y_three, y_two, y_one])
    order = 2 # spline order: 1 linear, 2 quadratic, 3 cubic ...
    spline_corrected = InterpolatedUnivariateSpline(xi_corrected, \
                                                    yi_corrected, k=order)


    # calculate running power as a percentage of MCR
    run_p_pc = 100.0-(mcr_p-run_p)/mcr_p*100

    sfoc = spline_corrected(run_p_pc/100.0*mcr_p)

    # plot %SMCR vs SFOC
    # go from 30% to 105% SMCR
    if plot == True:
        x_num = np.linspace(0.3*mcr_p, 1.05*mcr_p, 100)
        y0_num = spline(x_num)
        y_num = spline_corrected(x_num)
        plt.figure()
        plt.plot(x_num/mcr_p*100.0, y0_num)
        plt.plot(x_num/mcr_p*100.0, y_num)
        plt.plot(run_p_pc, sfoc, 'ro')
        plt.title('SFOC Curve')
        plt.ylabel('SFOC [g/kWh]')
        plt.xlabel('% of MCR')
        plt.grid(True)
        plt.savefig('Part_Load_SFOC_Curve.eps')
        plt.show()

    return sfoc


def layout_and_load(el_1, el_2, el_3, el_4, rpm_max, rpm_min, f_lr, p_t, rpm_t,
                    p_m, rpm_m, p_s, rpm_s, p_r, rpm_r):
    """
    This function will plot the engine layout and load diagram.
    One needs to exercise caution when lifting values for slopes from the
    literature, as lines are often plotted on loglog scales.
    The engine overload limits are from MAN specifications found in the
    Project Guides.
    """

    layout_x = [rpm_max, rpm_max, rpm_min, rpm_min, rpm_max]
    layout_y = [el_1, el_2, el_4, el_3, el_1]

    # the extents of the plot diagram
    x_min = 0.8*rpm_m
    x_max = 1.1*rpm_m
    y_min = 0.8*el_4
    y_max = 1.15*el_1

    x_val = np.linspace(x_min, x_max, 10)

    # Light running propeller - Line 1
    c_light = p_t/(pow(rpm_t, 3.0))
    y_light = c_light*pow(x_val, 3.0) # Line 6

    # Heavy running propeller - Line 2
    c_heavy = p_t/(pow((rpm_t-f_lr*rpm_t), 3.0))
    y_heavy = c_heavy*pow(x_val, 3.0)

    # speed limit for service, 105% of SMCR - Line 3
    x_three = [1.05*rpm_m, 1.05*rpm_m]
    y_three = [y_min, p_m]

    # mean effective pressure limit - Line 5
    x_five = [(rpm_m-0.033*rpm_m), rpm_m] # x coordinates of line 5
    k_five = 0.295 # gradient of Line 5, as obtained from MAN B&W
    a_five = p_m/pow(rpm_m, k_five)
    y_five = [a_five*pow(x_five[0], k_five), p_m] # y coordinates of line 5

    # torque/speed limit - Line 4
    x_four = [0.65*rpm_m, x_five[0]]
    k_four = 0.977 # slope of Line 4, as obtained from MAN B&W
    a_four = y_five[0]/pow(x_five[0], k_four)
    y_four = [a_four*pow(x_four[0], k_four), y_five[0]]

    # Power limit for continuous running - Line 7
    x_seven = [rpm_m, 1.05*rpm_m]
    y_seven = [p_m, p_m]

    # speed limit for trial, 107% of SMCR - Line 9
    x_nine = [1.07*rpm_m, 1.07*rpm_m]
    y_nine = [y_min, 1.10*p_m]

    # power limit (this line not denoted in the MAN B&W manual, I call it x10)
    x_ten = [rpm_m, x_nine[1]]
    y_ten = [y_nine[1], y_nine[1]]

    # overload limit - Line 8
    x_eight = [0.65*rpm_m, x_ten[0]]
    k_eight = 0.977 # slope of Line 8, as obtained from MAN B&W
    a_eight = y_ten[0]/pow(x_ten[0], k_eight)
    y_eight = [a_eight*pow(x_eight[0], k_eight), y_ten[0]]



    # plot the figure
    fig, a_x = plt.subplots()

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.loglog(layout_x, layout_y, 'mo-', label='Layout Diagram')
    plt.loglog(rpm_m, p_m, 'g*')
    plt.loglog(rpm_s, p_s, 'g*')
    plt.loglog(rpm_t, p_t, 'b*')
    plt.loglog(rpm_r, p_r, 'c*')
    plt.loglog(x_val, y_light, label='Propeller Design Curve (Light Running)')
    plt.loglog(x_val, y_heavy, label='Engine Design Curve (Heavy Running)')
    plt.loglog(x_three, y_three, 'k', label='Load Diagram')
    plt.loglog(x_four, y_four, 'k')
    plt.loglog(x_five, y_five, 'k')
    plt.loglog(x_seven, y_seven, 'k')
    plt.loglog(x_eight, y_eight, 'r', label='Overload Diagram')
    plt.loglog(x_nine, y_nine, 'r')
    plt.loglog(x_ten, y_ten, 'r')

    plt.grid(True, which="both")

    #plt.title("Engine Layaout and Load Diagram")
    plt.xlabel("Engine Speed [RPM]")
    plt.ylabel("Engine Power [kW]")

    plt.annotate('SMCR', xy=(rpm_m, p_m))
    plt.annotate('Service\nPropulsion\nPoint', xy=(rpm_s, p_s))
    plt.annotate('Propeller\nDesign\nPoint', xy=(rpm_t, p_t))
    plt.annotate('Current\nRunning\nPoint', xy=(rpm_r, p_r))

    major_formatter = FormatStrFormatter('%d')
    minor_formatter = FormatStrFormatter('%d')

    a_x.xaxis.set_major_formatter(major_formatter)
    a_x.yaxis.set_major_formatter(major_formatter)

    a_x.xaxis.set_minor_formatter(minor_formatter),
    a_x.yaxis.set_minor_formatter(minor_formatter)

    # Shrink current axis's height by some proportion (to make room for legend)
    box = a_x.get_position()
    a_x.set_position([box.x0, box.y0 + box.height * 0.17, box.width,
                      box.height * 0.95])

    # Put a legend below current axis
    a_x.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2,
               prop={'size':12})

    plt.savefig('Engine_Diagram.eps')

    plt.show()

    # check if the running load is within the limits of the selected
    # engine's capabilities
    limit_4 = np.interp(rpm_r, x_four, y_four) # torque/speed limit (line 4)
    limit_5 = np.interp(rpm_r, x_five, y_five) # mep limit (line 5)
    if (rpm_r > max(x_three) or p_r > max(y_seven)) or \
    ((rpm_r > min(x_four) or rpm_r < max(x_four)) and (p_r > limit_4)) or \
    ((rpm_r > min(x_five) or rpm_r < max(x_five)) and (p_r > limit_5)):
        print("Running point is outside of main engine's operating limits. "
              "Aborting...")
        sys.exit(1)



def fuel_type_sfoc(fuel_type, sfoc_hfo):
    """
    This function returns the SFOC for a given fuel

    INPUT:
    fuel_type: Fuel Type
    sfoc_hfo: SFOC when using standard HFO (at L1 for a two-stroke)

    OUTPUT:
    sfoc_ft: SFOC when using the selected fuel type
    """


    if fuel_type < 1 or fuel_type > 12:
        print("Error in fuel type argument... Aborting")
        sys.exit(1)

    # test to see if fuel has been implimented, not just a place-holder
    lcv = fuel_list[fuel_type][1]
    if lcv == 0.0:
        print("Fuel Type not implemented yet... Aborting")
        sys.exit(1)

    # based upon a linear relationship, calculate the SFOC at L1 for
    # the selected fuel type
    sfoc_ft = sfoc_hfo * fuel_list[1][1]/fuel_list[fuel_type][1]

    return sfoc_ft




class powering_specs:
    """
    Propulsion and Auxiliary Engine Powering Calculations
    """
    def __init__(self, q_trial, rpm_trial, q_run, rpm_run, hotel_load_design, hotel_load_service, pto, eta_pto, cpp, sea_margin, main_engine_margin, light_running_factor, aux_engine_margin, main_engine_type, aux_engine_type, fuel_type_main, fuel_type_aux):

        # attributes that are passed through initialisation        
        self.q_trial = q_trial
        self.rpm_trial = rpm_trial
        self.q_run = q_run
        self.rpm_run = rpm_run
        self.hotel_load_design = hotel_load_design
        self.hotel_load_service = hotel_load_service
        self.pto = pto
        self.eta_pto = eta_pto
        self.cpp = cpp
        self.sea_margin = sea_margin
        self.main_engine_margin = main_engine_margin
        self.f_lr = light_running_factor
        self.aux_engine_margin = aux_engine_margin
        self.main_engine_type = main_engine_type
        self.aux_engine_type = aux_engine_type
        self.fuel_type_main = fuel_type_main
        self.fuel_type_aux = fuel_type_aux
        
        # attributes that are calculated
        self.rpm_service = 0.0
        self.rpm_mcr = 0.0
        self.p_run = 0.0
        self.p_trial = 0.0
        self.p_mcr = 0.0
        self.p_service = 0.0

        self.hotel_load_max = 0.0
        
        self.main_engine_designation = "not assigned"
        self.aux_engine_designation = "not assigned"
        
        self.sfoc_main_at_run = 0.0
        self.sfoc_aux_at_run = 0.0
        
        self.co2_main_engine = 0.0
        self.co2_aux_engine = 0.0
        self.co2_total = 0.0

        # some input checks        
        if self.main_engine_type < 1 or self.main_engine_type > 2:
            print("ERROR: Main Engine Type format incorrect. Aborting...")
            sys.exit(1)
        
    def main_engine_requirements(self):
        """
        This method calculates main propulsion engine requirements from given input
        """
        
        # calculate propeller design point, in kW.
        # This is the trial-conditions, or calm water scenario
        # This is equivalent to light-running, or propeller design point, PD
        # This includes the power required by any shaft generator (PTO)
        # pylint: disable=E1101
        self.p_trial = self.q_trial*2.0*np.pi*self.rpm_trial/60.0+self.pto
        # pylint: enable=E1101

        # calculate light-running propeller curve
        # this is based on assuming power is proportional to rpm^3
        # this could be revised for different ship types
        # c.f. "Basic Principles of Ship Propulsion" by MAN B&W
        # This is not actually used here!
        #CL = PT/(pow(RPMT, 3.0))
    
        # calculate heavy-running propeller curve
        # this is based on assuming power is proportional to rpm^3
        # this could be revised for different ship types
        # c.f. "Basic Principles of Ship Propulsion" by MAN B&W
        heavy_prop_c = self.p_trial/(pow((self.rpm_trial-self.f_lr*self.rpm_trial), 3.0))
        
        # calculate service propulsion point, in kW, as stipulated by the sea-margin
        # N.B. this is different to the actual current running service point
        self.p_service = heavy_prop_c*pow((self.rpm_trial), 3.0) + \
                    self.sea_margin*heavy_prop_c*pow((self.rpm_trial), 3.0)
                    
        # calculate the rpm at the service propulsion point
        # this is based on assuming power is proportional to rpm^3
        # this could be revised for different ship types
        # c.f. "Basic Principles of Ship Propulsion" by MAN B&W
        self.rpm_service = pow((self.p_service/heavy_prop_c), (1.0/3.0))
                    
        # calculate specified maximum continuous rated power (SMCR), as
        # stipulated by the engine-margin
        self.p_mcr = self.p_service*(self.main_engine_margin+1.0)
        
        # calculate rpm at SMCR
        # this is based on assuming power is proportional to rpm^3
        # this could be revised for different ship types
        # c.f. "Basic Principles of Ship Propulsion" by MAN B&W
        self.rpm_mcr = pow((self.p_mcr/heavy_prop_c), (1.0/3.0))

        # calculate power in current running conditions
        self.p_run = self.q_run*2.0*np.pi*self.rpm_run/60.0+self.pto

    def aux_engine_requirements(self):
        """
        Hotel Load Powering Requirements

        calculate maximum engine power which can be continuously supplied
        maximum hotel load, in kW        
        """
        self.hotel_load_max = self.hotel_load_design+self.aux_engine_margin*self.hotel_load_design

        


    def select_main_two_stroke(self):
        """
        Choose a suitable engine for the required installed power and rpm
        the routine will select an engine whose SFOC is lowest at the
        Service Propulsion Point (MP), as this is the point the ship will
        be operating in. It also ensures that the engine is capable of
        producing the MCR power!
        """

        foc_min = 1.0E+09
        opt_piston_number = -1
        opt_engine_index = -1
        for i in range(len(two_stroke_main_db)):
            if two_stroke_main_db[i]["RPMmax"] < self.rpm_mcr or \
            two_stroke_main_db[i]["RPMmin"] > self.rpm_mcr:
                continue # RPM is out of range
            else:
                for j in range(len(two_stroke_main_db[i]["Npiston"])):
                    if two_stroke_main_db[i]["Npiston"][j]*two_stroke_main_db[i]["L1kWpC"] \
                        < self.p_mcr or \
                        two_stroke_main_db[i]["Npiston"][j]*two_stroke_main_db[i]["L4kWpC"] \
                        > self.p_mcr:
                        continue # not enough power
                    else:
                        # these configurations meet requirements

                        # calculate the percentage of MEP where MCR (PM) is located
                        mep_pc = mep_pc_l1(self.p_mcr, self.rpm_mcr,
                                           two_stroke_main_db[i]["L1kWpC"],
                                           two_stroke_main_db[i]["L3kWpC"],
                                           two_stroke_main_db[i]["Npiston"][j],
                                           two_stroke_main_db[i]["RPMmin"],
                                           two_stroke_main_db[i]["RPMmax"])

                        # below 80% of the %mep, the changes in SFOC vary quite
                        # dramatically from the trend. c.f. MAN B&W engine manuals
                        # below 75% there are no data at all
                        # if the %mep is less than 80% -> forget about this engine
                        if mep_pc < 80.0:
                            continue
                        else:
                            # estimate SFOC at point L1 for the
                            # selected engine and fuel
                            f_l1_sfoc_tmp = fuel_type_sfoc(self.fuel_type_main, two_stroke_main_db[opt_engine_index]["L1SFOC"])

                            # calculate SFOC at Service Propulsion Point
                            if self.cpp == False:
                                sfoc = sfoc_at_point(two_stroke_main_db[
                                        opt_engine_index]["m_FPP"],
                                        two_stroke_main_db[opt_engine_index]["c_FPP"],
                                        two_stroke_main_db[opt_engine_index]["pc_mcr"],
                                        self.p_mcr, self.p_service, f_l1_sfoc_tmp, mep_pc, False)
                            else:
                                sfoc = sfoc_at_point(two_stroke_main_db[
                                        opt_engine_index]["m_CPP"],
                                        two_stroke_main_db[opt_engine_index]["c_CPP"],
                                        two_stroke_main_db[opt_engine_index]["pc_mcr"],
                                        self.p_mcr, self.p_service, f_l1_sfoc_tmp, mep_pc, False)

                            # remember engine with the lowest SFOC at Service Point
                            if sfoc < foc_min:
                                # store engine data
                                opt_engine_index = i # index of engine designation
                                opt_piston_number = j # index of number of pistons
                                foc_min = sfoc # save lowest value of foc

        # if a suitable engine has not been found in the database, abort
        if opt_engine_index == -1 or opt_piston_number == -1:
            print("No main engines were found to be suitable for the given " \
                  "criteria. Aborting...")
            sys.exit(1)

        # for verification purposes, comparing with published data from MAN
        # choose : 6G95ME-C9.5-TII engine pp 2.9, 2.10 project guide
        #ed = 0
        #ep = 1
        #PM = 37098.0
        #RPMM = 76.0

        self.main_engine_designation = 'Two-stroke, ' + str(two_stroke_main_db[opt_engine_index]["Npiston"][opt_piston_number]) + ' Cylinder ' + two_stroke_main_db[opt_engine_index]["designation"]        
        

        # plot the engine layout and load diagram, and check that the running load
        # is within the limits of the engine's capabilities
        l_1 = two_stroke_main_db[opt_engine_index]["L1kWpC"] * \
              two_stroke_main_db[opt_engine_index]["Npiston"][opt_piston_number]
        l_2 = two_stroke_main_db[opt_engine_index]["L2kWpC"] * \
              two_stroke_main_db[opt_engine_index]["Npiston"][opt_piston_number]
        l_3 = two_stroke_main_db[opt_engine_index]["L3kWpC"] * \
              two_stroke_main_db[opt_engine_index]["Npiston"][opt_piston_number]
        l_4 = two_stroke_main_db[opt_engine_index]["L4kWpC"] * \
              two_stroke_main_db[opt_engine_index]["Npiston"][opt_piston_number]

        layout_and_load(l_1, l_2, l_3, l_4, \
                    two_stroke_main_db[opt_engine_index]["RPMmax"], \
                    two_stroke_main_db[opt_engine_index]["RPMmin"], \
                    self.f_lr, self.p_trial, self.rpm_trial, self.p_mcr, self.rpm_mcr, \
                    self.p_service, self.rpm_service, self.p_run, self.rpm_run)

        # calculate percentage MEP where MCR is located for the selected engine
        mep_pc = mep_pc_l1(self.p_mcr, self.rpm_mcr, \
                       two_stroke_main_db[opt_engine_index]["L1kWpC"], \
                       two_stroke_main_db[opt_engine_index]["L3kWpC"], \
                       two_stroke_main_db[opt_engine_index]["Npiston"] \
                       [opt_piston_number], \
                       two_stroke_main_db[opt_engine_index]["RPMmin"], \
                       two_stroke_main_db[opt_engine_index]["RPMmax"])

        # calculate Fuel Oil Consumption at the given power (torque and rpm)
        if self.cpp == False:
            self.sfoc_main_at_run = sfoc_at_point(two_stroke_main_db[opt_engine_index] \
                           ["m_FPP"], \
                           two_stroke_main_db[opt_engine_index]["c_FPP"], \
                           two_stroke_main_db[opt_engine_index]["pc_mcr"], \
                           self.p_mcr, self.p_run, f_l1_sfoc_tmp, mep_pc, True)
        else:
            self.sfoc_main_at_run = sfoc_at_point(two_stroke_main_db[opt_engine_index] \
                           ["m_CPP"], \
                           two_stroke_main_db[opt_engine_index]["c_CPP"], \
                           two_stroke_main_db[opt_engine_index]["pc_mcr"], \
                           self.p_mcr, self.p_run, f_l1_sfoc_tmp, mep_pc, True)



 
 
    def select_main_four_stroke(self):
        """
        Choose a suitable engine for the required installed power and rpm
        the routine will select an engine whose SFOC is lowest at the
        Service Propulsion Point (MP), as this is the point the ship will
        be operating in. It also ensures that the engine is capable of
        producing the MCR power!
        """

        foc_min = 1.0E+09
        opt_piston_number = -1
        opt_engine_index = -1
        for i in range(len(four_stroke_main_db)):
            # no need to check for rpm range, a gearbox is required in any case
            for j in range(len(four_stroke_main_db[i]["cylinders"])):
                if four_stroke_main_db[i]["power"][j] < self.p_mcr:
                    continue # not enough power
                else:
                    # these configurations meet requirements

                    # calculate service power % of total load
                    load_pc = self.p_service/four_stroke_main_db[i]["power"][j]*100.0

                    # calculate SFOC at Service Propulsion Point
                    order = 2 # order of interpolating spline
                    if self.cpp == False:
                        spline = InterpolatedUnivariateSpline(four_stroke_main_db[i]["load"], four_stroke_main_db[i]["sfoc_fpp"], k=order)
                    else:
                        spline = InterpolatedUnivariateSpline(four_stroke_main_db[i]["load"], four_stroke_main_db[i]["sfoc_cpp"], k=order)

                    #sfoc = spline(load_pc)
                    sfoc = fuel_type_sfoc(self.fuel_type_aux, spline(load_pc))

                    # remember engine with the lowest SFOC at Service Point
                    if sfoc < foc_min:
                        # store engine data
                        opt_engine_index = i # index of engine designation
                        opt_piston_number = j # index of number of pistons
                        foc_min = sfoc # save lowest value of foc


        # if a suitable engine has not been found in the database, abort
        if opt_engine_index == -1 or opt_piston_number == -1:
            print("No main engines were found to be suitable for the given " \
                  "criteria. Aborting...")
            sys.exit(1)
        else:
            self.main_designation = 'Four-stroke, ', str(four_stroke_main_db[opt_engine_index]["Cyl"][opt_piston_number]) + ' Cylinder ' + four_stroke_main_db[opt_engine_index]["designation"]

        # calculate fuel oil consumption at the running point
        # calculate service power % of total load
        load_pc = self.p_run/four_stroke_main_db[opt_engine_index]["power"][opt_piston_number]*100.0

        order = 2 # order of interpolating spline
        if self.cpp == False:
            spline = InterpolatedUnivariateSpline(four_stroke_main_db[opt_engine_index]["load"], four_stroke_main_db[opt_engine_index]["sfoc_fpp"], k=order)
        else:
            spline = InterpolatedUnivariateSpline(four_stroke_main_db[opt_engine_index]["load"], four_stroke_main_db[opt_engine_index]["sfoc_cpp"], k=order)

        # calculate sfoc for given fuel
        self.sfoc_main_at_run = fuel_type_sfoc(self.fuel_type_aux, spline(load_pc))
 
  
 
    def select_aux_four_stroke(self):
        """
        N.B. There may be several different ways to select the most
        fuel efficient
        gen sets, there may be more than one combinations of different gensets
        this becomes an optimisation problem, beyond the scope of the
        original remit
        """

        # find the most powerfull engine from aux_engine database
        aux_max = 0.0
        for i in range(len(four_stroke_aux_db)):
            aux_power = four_stroke_aux_db[i]["GenP"][len(four_stroke_aux_db[i]["GenP"])-1]
            if aux_power > aux_max:
                aux_max = aux_power
                index_max = i # index of maximum sized engine
        # power rating in database is for 85% MCR, calculate the 100% MCR
        aux_max = aux_max*(1.0+0.15)

        aux_max_engines_required = 0 # number of maximum power aux_engines required
        if self.hotel_load_max < aux_max:
            # only one aux_engine is required to satisfy the maximum Hotel Load
            # requirement
            # run through the database of aux_engines, and select the smallest one
            # which satisfies the maximum hotel load requirements
            for i in range(len(four_stroke_aux_db)):
                for j in range(len(four_stroke_aux_db[i]["GenP"])):
                    if four_stroke_aux_db[i]["GenP"][j] > self.hotel_load_max:
                        # select this aux_engine
                        aux_index = i
                        aux_pistons = j
                        break
                    else: # how to break out of a nested for loop!!
                        continue
                    break
            # store selected engine
            self.aux_engine_designation = str(four_stroke_aux_db[aux_index]["Cyl"][aux_pistons]) + ' Cylinder ' + four_stroke_aux_db[aux_index]["designation"]
        else:
            # more than one aux_engine is required to satisfy the maximum
            # Hotel Load requirement
            # divide the hotel load up into factors of the largest generator power

            # number of Maximum Power aux_engines required
            aux_max_engines_required = int(self.hotel_load_max/aux_max)

            # the remaining amount of generator power required
            aux_mod_engines_required = self.hotel_load_max%aux_max

            # run through the database of gensets, and select the smallest one
            # which satisfies the remaining hotel load requirements
            for i in range(len(four_stroke_aux_db)):
                for j in range(len(four_stroke_aux_db[i]["GenP"])):
                    aux_engine_max = four_stroke_aux_db[i]["GenP"][j] + \
                                 0.15*four_stroke_aux_db[i]["GenP"][j]
                    if aux_engine_max > aux_mod_engines_required:
                        # select this aux_engine
                        aux_index = i
                        aux_pistons = j
                        break
                    else: # how to break out of a nested for loop!!
                        continue
                    break

            # store selected engine            
            self.aux_engine_designation = str(aux_max_engines_required) + ' x ' + str(four_stroke_aux_db[index_max]["Cyl"][len(four_stroke_aux_db[index_max]["GenP"])-1]) + ' Cylinder ' + four_stroke_aux_db[index_max]["designation"] + ' and a ' + str(four_stroke_aux_db[aux_index]["Cyl"][aux_pistons]) + ' Cylinder ' + four_stroke_aux_db[aux_index]["designation"]

        # The aux_engines have now been selected, based upon design power
        # Estimate how they perform when running at service power

        # In order to avoid getting into the situation of debating which
        # selection of
        # aux_engines to use in supplying the hotel load (resulting in an
        # optimised fuel
        # efficient selection), the simplist approach is used,
        # which probably does not result in the most fuel efficient usage.
        # This involoves "filling up" each aux_engine, up to 100% MCR,
        # then moving on to
        # the next one, until the power demand is satisfied.
        #
        # calculate fuel oil consumption at service load
        if aux_max_engines_required == 0:
            # only one aux_engine is installed
            # calculate percentage load usage

            # chosen engine's maximum generator power ORIGINALLY EGPmax
            aux_mod_max = four_stroke_aux_db[aux_index]["GenP"][aux_pistons] + \
                      0.15*four_stroke_aux_db[aux_index]["GenP"][aux_pistons]

            aux_pc_load = 100.0-((aux_mod_max-self.hotel_load_service) / \
                             aux_mod_max*100.0)
            if aux_pc_load < 0.0:
                sys.exit("Generator is overloaded... Aborting.")
                
            # create a spline through the data-points of Generator Power and SFOC
            # for the selected aux_engine
            spline = InterpolatedUnivariateSpline(four_stroke_aux_db[aux_index]["Load"], \
                                         four_stroke_aux_db[aux_index]["SFOC"], k=2)
            # calculate SFOC at service load through inter/extrapolation of spline, for given fuel type
            self.sfoc_aux_at_run = fuel_type_sfoc(self.fuel_type_aux, spline(aux_pc_load))


        else: # more than one aux_engine is installed
            # number of Maximum Power aux_engines required for service load
            aux_max_engines_service = int(self.hotel_load_service/aux_max)

            sfoc_aux_hfo = aux_max_engines_service*four_stroke_aux_db[index_max]["SFOC"] \
                   [len(four_stroke_aux_db[index_max]["SFOC"])-1]

            sfoc_aux = fuel_type_sfoc(self.fuel_type_aux, spline(sfoc_aux_hfo))

            # remaining power required for service load
            aux_mod_engines_service = self.hotel_load_service%aux_max

            # now for the rest of the engines
            if aux_max_engines_service < aux_max_engines_required:
                print("aux_max_engines_service =", aux_max_engines_service)
                # there are more maximum sized engines to load up
                # calculate percentage load usage

                # chosen engine's maximum generator power
                aux_mod_max = four_stroke_aux_db[index_max]["GenP"] \
                          [len(four_stroke_aux_db[index_max]["GenP"])-1]+ \
                          0.15*four_stroke_aux_db[index_max]["GenP"] \
                          [len(four_stroke_aux_db[index_max]["GenP"])-1]

                aux_pc_load = 100.0-((aux_mod_max-aux_mod_engines_service)/ \
                                 aux_mod_max*100.0)

                # create a spline through the data-points of Generator Power and
                # SFOC for the selected aux_engine
                spline = InterpolatedUnivariateSpline(four_stroke_aux_db[aux_index]
                                                  ["Load"],
                                                  four_stroke_aux_db[aux_index]
                                                  ["SFOC"], k=2)
                # calculate total SFOC at service load through
                self.sfoc_aux_at_run = sfoc_aux+fuel_type_sfoc(self.fuel_type_aux, spline(aux_pc_load))
            else:
                # the last remaining engine is to be loaded up
                # calculate percentage load usage
                # chosen engine's maximum generator power
                aux_mod_max = four_stroke_aux_db[aux_index]["GenP"][aux_pistons]+ \
                          0.15*four_stroke_aux_db[aux_index]["GenP"][aux_pistons]

                print("aux_mod_max =", aux_mod_max)
                aux_pc_load = 100.0-((aux_mod_max-aux_mod_engines_service)/
                                 aux_mod_max*100.0)

                print("% service load =", aux_pc_load)
                if aux_pc_load < 0.0:
                    sys.exit("Generator is overloaded... Aborting.")

            
                # create a spline through the data-points of
                # Generator Power and SFOC for the selected aux_engine
                spline = InterpolatedUnivariateSpline(four_stroke_aux_db[aux_index]
                                                      ["Load"],
                                                      four_stroke_aux_db[aux_index]
                                                      ["SFOC"], k=2)
                # calculate total SFOC at service load through
                # inter/extrapolation of spline
                self.sfoc_aux_at_run = sfoc_aux+fuel_type_sfoc(self.fuel_type_aux, spline(aux_pc_load))

    def select_main_engine(self):
        """
        select a suitable main propulsion engine
        """
        if self.main_engine_type == 1: # two-stroke
            self.select_main_two_stroke()
        elif self.main_engine_type == 2: # four-stroke
            self.select_main_four_stroke()


    def select_aux_engine(self):
        """
        N.B. There may be several different ways to select the most
        fuel efficient
        gen sets, there may be more than one combinations of different gensets
        this becomes an optimisation problem, beyond the scope of the
        original remit
        """
        # there's only one four-strokes to choose from!
        self.select_aux_four_stroke()


    def estimate_co2(self):
        """
        """
        # CO_2 emission factor based upon stoichiometric combustion
        #CO2_EF = 3.1141
        co2_main_emission_factor = fuel_list[self.fuel_type_main][2]
        co2_aux_emission_factor = fuel_list[self.fuel_type_aux][2]

        # calculate fuel oil consumption [t/h]
        foc_main = self.sfoc_main_at_run*self.p_run/1.0E+06
        foc_aux = self.sfoc_aux_at_run*self.hotel_load_service/1.0E+06
         
        # estimate CO_2 emissions [t/h]
        self.co2_main_engine = foc_main*co2_main_emission_factor
        self.co2_aux_engine = foc_aux*co2_aux_emission_factor
        self.co2_total = self.co2_main_engine+self.co2_aux_engine
            


def run_gem(case_study, q_trial, rpm_trial, q_run, rpm_run, hotel_load_design, hotel_load_service, pto, eta_pto, cpp, sea_margin, main_engine_margin, light_running_factor, aux_engine_margin, main_engine_type, aux_engine_type, fuel_type_main, fuel_type_aux):
    """
    """
    # example for example, Maersk Batam
    ship1 = powering_specs(q_trial, rpm_trial, q_run, rpm_run, hotel_load_design, hotel_load_service, pto, eta_pto, cpp, sea_margin, main_engine_margin, light_running_factor, aux_engine_margin, main_engine_type, aux_engine_type, fuel_type_main, fuel_type_aux)

    # calculate main engine powering requirements
    ship1.main_engine_requirements()
    
    # select a suitable main propulsion engine
    ship1.select_main_engine()

    # calculate aux engine powering requirements
    ship1.aux_engine_requirements()

    # select a suitable (set) of auxiliary engines
    ship1.select_aux_engine()

    # estimate C0_2 emissions
    ship1.estimate_co2()
    
    # print out some stuff
    print()
    print(case_study)
    for i in range(0, len(case_study)):
        print("=", end="")
    print()
    print("Main Propulsion Engine:", ship1.main_engine_designation)
    print("Auxiliary Engine(s):", ship1.aux_engine_designation)
    print()
    print("Main Propulsion Engine Fuel Type:", fuel_list[ship1.fuel_type_main][0])
    print("Auxiliary Engine Fuel Type:", fuel_list[ship1.fuel_type_aux][0])
    print()
    print("Values are given for actual in-service running performance.\n")
    print("CO2 from Main Engine:  ", str.format('{0:.3f}', ship1.co2_main_engine), "[t/h]")
    print("CO2 from Auxiliary Engine(s):", str.format('{0:.3f}', ship1.co2_aux_engine), "[t/h]")
    print("Total CO2 emissions:   ", str.format('{0:.3f}', ship1.co2_total), "[t/h]")

    
    # return necessary output
    # TODO need to return SFOC for main and aux, as well as the delta's in emissions from various clean technologies (which also need to be implimented)
    return ship1.co2_total

"""
Create a basic custom KPI script using eppy html reader to read the results.

Detailed information:
https://designbuilder.co.uk/helpv7.2/#CustomKPIsExample.htm

"""

import ctypes
from eppy.results import readhtml
from os import path


def show_message(title, text):
    """Show message dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


def after_energy_simulation():
    tablePath = api_environment.EnergyPlusFolder + r"eplustbl.htm"
    if path.exists(tablePath):
        filehandle = open(tablePath, 'r').read()
        if filehandle is not None:
            htables = readhtml.titletable(filehandle)
            EUITable = tuple(htable for htable in htables if
                             htable[0] in ['EAp2-17a. Energy Use Intensity - Electricity'])
            real_eui_table = EUITable[0]
            eui_table_content = real_eui_table[1]
            EUI = str(eui_table_content[8][1])
            site = api_environment.Site
            table = site.GetTable("ParamResultsTmp")
            record = table.AddRecord()
            record[0] = "EUI (kWh/m2)"
            record[1] = EUI
        else:
            show_message("Information", "Error creating TableReader")
    else:
        show_message("Information", "File does not exist " + tablePath)

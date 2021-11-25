import ctypes

from eppy import modeleditor
from eppy.modeleditor import IDF


def show_message(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


def before_energy_simulation():
    IDF.setiddname(api_environment.EnergyPlusInputIddPath)
    idf_file = IDF(api_environment.EnergyPlusInputIdfPath)

    # extract values from optimisation table
    site = api_environment.Site
    table = site.GetTable("OptimisationVariables")
    
    heating_coils = idf_file.idfobjects['Coil:WaterHeating:AirToWaterHeatPump:Pumped'.upper()]
    heating_cop_row = table.Records["heatingCOP"]
    heating_cop = heating_cop_row["VariableCurrentValue"]

    for coil in heating_coils:
        if coil.Name == 'HP Water Heater HP Water Heating Coil':
            if heating_cop != "UNKNOWN":
                coil.Rated_COP = heating_cop
            else:
                show_message("ERROR", "Cannot set heating COP, unknown value in table OptimisationVariables")
            

    chillers = idf_file.idfobjects['Chiller:Electric:EIR'.upper()]
    cooling_eer_row = table.Records["coolingEER"]
    cooling_eer = cooling_eer_row["VariableCurrentValue"]

    for chiller in chillers:
        if cooling_eer != "UNKNOWN":
            chiller.Reference_COP = cooling_eer
        else:
            show_message("ERROR", "Cannot set cooling COP, unknown value in table OptimisationVariables")

    idf_file.save()
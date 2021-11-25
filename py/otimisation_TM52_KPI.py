"""Use TM52 criteria as optimisation KPI."""

from db_eplusout_reader import Variable, get_results
from db_eplusout_reader.constants import *
from db_eplusout_reader.exceptions import NoResults

threshold_crit1 = 3
threshold_crit2 = 6
threshold_crit3 = 0


def zone_fails_tm52(zone_name):
   """Verify if given zones meets tm52 criteria."""
   variable1 = 'CIBSE TM52 Criterion 1 {}'.format(zone_name)
   variable2 = 'CIBSE TM52 Criterion 2 {}'.format(zone_name)
   variable3 = 'CIBSE TM52 Criterion 3 {}'.format(zone_name)

   variables = [
       Variable(RP, "EMS", variable1, "%"),
       Variable(D, "EMS", variable2, "C"),
       Variable(RP, "EMS", variable3, "hr"),
   ]

   results = get_results(
       api_environment.EnergyPlusFolder + r"eplusout.sql",
       variables=variables,
       alike=True
   )

   criterion_1 = results.arrays[0][0]
   crit2_series = results.arrays[1]
   criterion_2 = max(crit2_series)
   criterion_3 = results.arrays[2][0]

   counter = 0

   if criterion_1 > threshold_crit1:
       counter += 1

   if criterion_2 > threshold_crit2:
       counter += 1

   if criterion_3 > threshold_crit3:
       counter += 1

   return counter >= 2


def get_total_area():
   """Sum floor area of all the zones."""
   area = 0
   for block in active_building.BuildingBlocks:
       for zone in block.Zones:
           area += zone.FloorArea
   return area


def after_energy_simulation():
   site = api_environment.Site
   fail_area = 0
   total_area = get_total_area()

   for block in active_building.BuildingBlocks:
       for zone in block.Zones:
           zone_name = zone.GetAttribute("SSEPObjectNameInOP")
           try:
               if zone_fails_tm52(zone_name):
                   fail_area += zone.FloorArea
           except NoResults:
               pass

   percentage_area_fail = (fail_area / total_area) * 100

   table = site.GetTable("ParamResultsTmp")
   record = table.AddRecord()
   record[0] = "TM52 Discomfort %"
   record[1] = str(percentage_area_fail)

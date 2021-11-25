/* 
Replace District Heating (name: HW Plant) and District Cooling (Name: CHW Plant) with ChillerHeater:Absorption:DirectFired

 */

using System.Collections.Generic;
using System.Linq;
using DB.Extensibility.Contracts;
using EpNet;

namespace DB.Extensibility.Scripts
{
    public class IdfFindAndReplace : ScriptBase, IScript
    {
        public override void BeforeEnergySimulation()
        {
            IdfReader idfReader = new IdfReader(
                ApiEnvironment.EnergyPlusInputIdfPath,
                ApiEnvironment.EnergyPlusInputIddPath);
            
            const string ChillerName = "Big Chiller";
            const string ChillerType = "ChillerHeater:Absorption:DirectFired";
            
            // modify branches
            List<string> modifiedBranches = new List<string> {"HW plant HW Loop Supply Side Branch", "CHW plant CHW Loop Supply Side Branch"};
            IEnumerable<IdfObject> branches = idfReader["Branch"];
            foreach (IdfObject branch in branches)
            {
                if (modifiedBranches.Contains(branch["Name"]))
                    {
                        branch["Component 1 Name"].Value = ChillerName;
                        branch["Component 1 Object Type"].Value = ChillerType;
                    }
            }
            // modify equipment list
            List<string> modifiedEquipment = new List<string> {"HW Loop Scheme 1 Range 1 Equipment List", "CHW Loop Scheme 1 Range 1 Equipment List"};
            IEnumerable<IdfObject> allEquipment = idfReader["PlantEquipmentList"];
            foreach (IdfObject equipment in allEquipment)
            {
                if (modifiedEquipment.Contains(equipment["Name"]))
                    {
                        equipment["Equipment 1 Name"].Value = ChillerName;
                        equipment["Equipment 1 Object Type"].Value = ChillerType;
                    }
            }
            // modify nodes
            IdfObject districtHeating = idfReader["DistrictHeating"].First(c => c["Name"] == "HW Plant");
            string HWinletNode = districtHeating["Hot Water Inlet Node Name"].Value;
            string HWoutletNode = districtHeating["Hot Water Outlet Node Name"].Value;

            IdfObject districtCooling = idfReader["DistrictCooling"].First(c => c["Name"] == "CHW Plant");
            string CHWinletNode = districtHeating["Chilled Water Inlet Node Name"].Value;
            string CHWoutletNode = districtHeating["Chilled Water Outlet Node Name"].Value;

            IdfObject chillerHeater = idfReader["ChillerHeater:Absorption:DirectFired"].First(c => c["Name"] == "Big Chiller");
            chillerHeater["Hot Water Inlet Node Name"].Value = HWinletNode;
            chillerHeater["Hot Water Outlet Node Name"].Value = HWoutletNode;
            chillerHeater["Chilled Water Outlet Node Name"].Value = CHWinletNode;
            chillerHeater["Chilled Water Inlet Node Name"].Value = CHWoutletNode;

            idfReader.Remove(districtHeating);
            idfReader.Remove(districtCooling);

            idfReader.Save();
        }
    }
}

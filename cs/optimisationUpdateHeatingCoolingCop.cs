using System.Windows.Forms;
using System.Collections.Generic;
using DB.Extensibility.Contracts;
using EpNet;
using DB.Api;
using System.Windows.Forms;


namespace DB.Extensibility.Scripts
{
    public class IdfFindAndReplace : ScriptBase, IScript
    {
        public override void BeforeEnergySimulation()
        {
            Site site = ApiEnvironment.Site;
            Table table = site.GetTable("OptimisationVariables");
            Record recordHeating = table.Records["heatingCOP"];
            string heatingCop = recordHeating["VariableCurrentValue"];
            
            IdfReader idfReader = new IdfReader(
                ApiEnvironment.EnergyPlusInputIdfPath,
                ApiEnvironment.EnergyPlusInputIddPath);

            IEnumerable<IdfObject> heatingCoils = idfReader["Coil:WaterHeating:AirToWaterHeatPump:Pumped"];
            foreach (IdfObject coil in heatingCoils)
            {
                if (coil["Name"].Equals("HP Water Heater HP Water Heating Coil"))
                {
                    if (heatingCop.Equals("UNKNOWN")) {
                        MessageBox.Show("Cannot set heating COP, UNKNOWN value in OptimisationVariables table. ");
                    } else {
                        coil["Rated COP"].Value = heatingCop;
                    }
                }
            }

            Record recordCooling = table.Records["coolingEER"];
            string coolingEer = recordCooling["VariableCurrentValue"];

            IEnumerable<IdfObject> chillers = idfReader["Chiller:Electric:EIR"];
            foreach (IdfObject chiller in chillers)
            {
                if (coolingEer.Equals("UNKNOWN")) {
                        MessageBox.Show("Cannot set cooling COP, UNKNOWN value in OptimisationVariables table. ");
                } else {
                        chiller["Reference COP"].Value = coolingEer;
                }
            }
            idfReader.Save();
        }
    }
}

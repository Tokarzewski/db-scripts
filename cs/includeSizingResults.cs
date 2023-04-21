/*
Include cooling and heating sizing in results set.

Note - DesignBuilder will not be able to load the results.

*/

using System.Collections.Generic;
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

            IdfObject simulationControl = idfReader["SimulationControl"][0];
            simulationControl["Run Simulation for Sizing Periods"].Value = "Yes";
            idfReader.Save();
        }
    }
}

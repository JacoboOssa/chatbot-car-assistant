from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import numpy as np

# Define Bayesian Network
model = BayesianNetwork([
    ('BatteryVoltage', 'StarterSpins'),
    ('StarterSpins', 'StarterCranks'),
    ('StarterCranks', 'EngineFires'),
    ('SparkToPlugs', 'EngineFires'),
    ('EngineFires', 'Problem'),
    ('FuelToFilter', 'Problem'),
    ('FuelInjected', 'Problem'),
    ('StallsInRain', 'Problem')
])

# Define CPDs
cpd_battery_voltage = TabularCPD(variable='BatteryVoltage', variable_card=2, values=[[0.85], [0.15]])

cpd_starter_spins = TabularCPD(variable='StarterSpins', variable_card=2,
                               values=[
                                   [0.9, 0.4],  # Spins
                                   [0.1, 0.6]   # Doesn't spin
                               ],
                               evidence=['BatteryVoltage'], evidence_card=[2])

cpd_starter_cranks = TabularCPD(variable='StarterCranks', variable_card=2,
                                values=[
                                    [0.8, 0.2],  # Cranks
                                    [0.2, 0.8]   # Doesn't crank
                                ],
                                evidence=['StarterSpins'], evidence_card=[2])

cpd_spark_to_plugs = TabularCPD(variable='SparkToPlugs', variable_card=2,
                                values=[
                                    [0.9],  # Spark present
                                    [0.1]   # No spark
                                ])

cpd_engine_fires = TabularCPD(variable='EngineFires', variable_card=2,
                              values=[
                                  [0.7, 0.2, 0.1, 0.05],  # Fires
                                  [0.3, 0.8, 0.9, 0.95]   # Doesn't fire
                              ],
                              evidence=['StarterCranks', 'SparkToPlugs'], evidence_card=[2, 2])

cpd_fuel_to_filter = TabularCPD(variable='FuelToFilter', variable_card=2, values=[[0.8], [0.2]])

cpd_fuel_injected = TabularCPD(variable='FuelInjected', variable_card=2, values=[[0.85], [0.15]])

cpd_stalls_in_rain = TabularCPD(variable='StallsInRain', variable_card=2, values=[[0.75], [0.25]])

raw_values = np.array([
    [0.6, 0.3, 0.1, 0.05, 0.5, 0.2, 0.1, 0.05, 0.4, 0.3, 0.2, 0.1, 0.3, 0.2, 0.1, 0.05],  # Battery
    [0.3, 0.5, 0.2, 0.1, 0.3, 0.4, 0.2, 0.1, 0.3, 0.4, 0.3, 0.2, 0.2, 0.3, 0.2, 0.1],  # Starter
    [0.05, 0.1, 0.6, 0.2, 0.1, 0.3, 0.5, 0.3, 0.2, 0.3, 0.6, 0.4, 0.2, 0.2, 0.4, 0.3],  # Fuel
    [0.05, 0.1, 0.1, 0.65, 0.1, 0.1, 0.2, 0.6, 0.1, 0.0, 0.1, 0.4, 0.3, 0.3, 0.3, 0.6]   # Ignition
])

normalized_values = raw_values / raw_values.sum(axis=0)

cpd_problem = TabularCPD(
    variable='Problem', 
    variable_card=4,  # 4 types of problems: Battery, Starter, Fuel, Ignition
    values=normalized_values.tolist(),
    evidence=['EngineFires', 'FuelToFilter', 'FuelInjected', 'StallsInRain'],
    evidence_card=[2, 2, 2, 2]
)

# Add CPDs to the model
model.add_cpds(cpd_battery_voltage, cpd_starter_spins, cpd_starter_cranks, 
               cpd_spark_to_plugs, cpd_engine_fires, cpd_fuel_to_filter, 
               cpd_fuel_injected, cpd_stalls_in_rain, cpd_problem)


# Verify the model
assert model.check_model()

# Perform inference
inference = VariableElimination(model)

# Example Query: What is the most likely problem if the starter doesn't crank, and battery voltage is low?
query_result = inference.map_query(variables=['Problem'], evidence={
    'StarterCranks': 1,  # Doesn't crank
    # StallsInRain is provided as evidence
    'StallsInRain': 1 # Stalls in rain
})

problem_mapping = {
    0: "Battery Issue",
    1: "Starter Issue",
    2: "Fuel Issue",
    3: "Ignition Issue"
}

# Translate the output
likely_problem = query_result['Problem']
print(f"Likely problem: {problem_mapping[likely_problem]}")

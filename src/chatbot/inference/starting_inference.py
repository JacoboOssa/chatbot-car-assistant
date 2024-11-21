from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination 
from ...chatbot.knowledge_base import CarTroubleshootingExpertSystem, CarIssueFact


import logging
from experta import KnowledgeEngine, Fact, Rule
import numpy as np

class StartingInference:
    
    def __init__(self):
        self.model = self._build_model()
        self.inference = VariableElimination(self.model)
        
        self.carTroubleshootingExpertSystem = CarTroubleshootingExpertSystem()


    def _build_model(self):
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


        return model
    '''
    def type_of_problem(self, most_likely_problem, probability):
        problem_mapping = {
            0: "Battery Issue",
            1: "Starter Issue",
            2: "Fuel Issue",
            3: "Ignition Issue"
        }
        return f"{problem_mapping[most_likely_problem]} with probability {probability:.2f}"
    '''
    def type_of_problem(self, most_likely_problem, probability):
        problem_mapping = {
            0: "Battery Issue",
            1: "Starter Issue",
            2: "Fuel Issue",
            3: "Ignition Issue"
        }
        return problem_mapping[most_likely_problem], probability
    
    def transform_evidence(self, user_input):
        # Convert user input that is true or false into 1 or 0
        for value in user_input:
            if user_input[value] == True:
                user_input[value] = 1
            else:
                user_input[value] = 0
        
        return user_input
    
    
    def infer_problem(self, evidence):
        """Perform inference and return the most likely problem and its probability."""
        transformed_evidence = self.transform_evidence(evidence)
        
        # Get the probability distribution of the "Problem" variable
        result = self.inference.query(variables=['Problem'], evidence=transformed_evidence)
        #print(result)
        probabilities = result.values
        #print(probabilities)
        most_likely_problem = np.argmax(probabilities)
        #print(most_likely_problem)
        probability = probabilities[most_likely_problem]
        #print("Retorno del Metodo type_of_problem")
        #print(self.type_of_problem(most_likely_problem, probability))
        mapped_problem, probability_problem = self.type_of_problem(most_likely_problem, probability)

        
        return probability_problem

    
    
    def infer_problem_by_issue(self, evidence):
        """
        Realiza la inferencia y devuelve las probabilidades de todos los problemas.
        """
        transformed_evidence = self.transform_evidence(evidence)
        # Obtener la distribución de probabilidad de la variable 'Problem'
        result = self.inference.query(variables=['Problem'], evidence=transformed_evidence)
        probabilities = result.values
        most_likely_problem = np.argmax(probabilities)
        probability = probabilities[most_likely_problem]
        mapped_problem, probability_problem = self.type_of_problem(most_likely_problem, probability)
        if mapped_problem == "Battery Issue":
            self.carTroubleshootingExpertSystem.reset()
            self.carTroubleshootingExpertSystem.declare(CarIssueFact(BatteryIssue=True))
            self.carTroubleshootingExpertSystem.run()
        elif mapped_problem == "Starter Issue":
            self.carTroubleshootingExpertSystem.reset()
            self.carTroubleshootingExpertSystem.declare(CarIssueFact(StarterIssue=True))
            self.carTroubleshootingExpertSystem.run()
        elif mapped_problem == "Fuel Issue":
            self.carTroubleshootingExpertSystem.reset()
            self.carTroubleshootingExpertSystem.declare(CarIssueFact(FuelIssue=True))
            self.carTroubleshootingExpertSystem.run()
        elif mapped_problem == "Ignition Issue":
            self.carTroubleshootingExpertSystem.reset()
            self.carTroubleshootingExpertSystem.declare(CarIssueFact(IgnitionIssue=True))
            self.carTroubleshootingExpertSystem.run()
        #print("Retorno del Metodo aplly_probabilities")
        #print(self.carTroubleshootingExpertSystem.apply_probabilities(probabilities_dict))
        problem = self.carTroubleshootingExpertSystem.problem
        diagnosis = self.carTroubleshootingExpertSystem.diagnosis
        return problem,diagnosis
    

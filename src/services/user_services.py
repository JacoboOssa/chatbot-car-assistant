from ..chatbot.inference.starting_inference import StartingInference
from ..chatbot.knowledge_base import CarTroubleshootingExpertSystem, CarIssueFact

class UserServices:
    def __init__(self):
        self.starting_inference = StartingInference()        
        self.carTroubleshootingExpertSystem = CarTroubleshootingExpertSystem()
        self.carTroubleshootingExpertSystemFacts = CarIssueFact()
        
    def _parse_user_input_starting(self, user_input):
        evidence = {}

        # Define keyword mappings to evidence
        keyword_mappings = {
            "starter doesn't crank": ('StarterCranks', False),
            "starter won’t crank": ('StarterCranks', False),
            "starter won't crank": ('StarterCranks', False),
            "low battery": ('BatteryVoltage', "low"),
            "high battery": ('BatteryVoltage', "high"),
            "no spark": ('SparkToPlugs', False),
            "spark present": ('SparkToPlugs', True),
            "no fuel": ('FuelToFilter', False),
            "fuel present": ('FuelToFilter', True),
            "stalls in rain": ('StallsInRain', True),
            "engine fires": ('EngineFires', True),
            "engine doesn't fire": ('EngineFires', False),
            "starter spins": ('StarterSpins', True),
            "starter doesn't spins": ('StarterSpins', False),
            "cleaned terminals": ('CleanedTerminals', True),
            "dirty terminals": ('CleanedTerminals', False),
            "fuel injected": ('FuelInjected', True),
            "carburetor": ('FuelInjected', False),
            "stalls warm": ('StallsWarm', True),
            "stalls cold": ('StallsWarm', False)
            # "mechanical distributor": ('MechanicalDistributor', False),
            # "electronic distributor": ('MechanicalDistributor', True),
        }

        # Check for keywords in the user input
        for phrase, (variable, value) in keyword_mappings.items():
            if phrase in user_input:
                evidence[variable] = value

        return evidence if evidence else None

    def process_question(self,question:str):
        
        evidence = self._parse_user_input_starting(question)
        
        if(evidence):
            self.carTroubleshootingExpertSystem.reset()
            self.carTroubleshootingExpertSystem.declare(CarIssueFact(**evidence))
            self.carTroubleshootingExpertSystem.run()
            
            probability = self.starting_inference.infer_problem(evidence)
            
            problem,diagnosis = self.starting_inference.infer_problem_by_issue(evidence)
            
        return self.carTroubleshootingExpertSystem.problem, self.carTroubleshootingExpertSystem.diagnosis, probability, problem,diagnosis
            
            
            
        
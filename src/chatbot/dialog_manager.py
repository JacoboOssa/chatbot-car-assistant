from .inference.starting_inference import StartingInference
from .knowledge_base import CarTroubleshootingExpertSystem, CarIssueFact
#from collections.abc import Mapping
#from ..database.db import MongoDBConnection
#from ..database.queries import CarTroubleshootingDAL
# from .inference.steering_inference import SteeringInference

class ChatbotDialogManager:
    def __init__(self):
        # Initialize inference engines for each subsystem

        # db_connection = MongoDBConnection()
        # self.dal = CarTroubleshootingDAL(db_connection)
        
        self.starting_inference = StartingInference()
         # self.steering_inference = SteeringInference()
        
        self.carTroubleshootingExpertSystem = CarTroubleshootingExpertSystem()
        self.carTroubleshootingExpertSystemFacts = CarIssueFact()

       

    def start(self):
        """Start the chatbot dialog loop."""
        print("Welcome to the Car Troubleshooting Chatbot!")
        print("You can diagnose issues with different car systems, such as 'starting' or 'steering'.")
        print("Type 'exit' to quit the chatbot.\n")

        while True:
            subsystem = input("Which system are you having issues with? (starting/steering/exit): ").lower()
            
            if subsystem == "exit":
                print("Goodbye! Thank you for using the Car Troubleshooting Chatbot.")
                break

            elif subsystem == "starting":
                #print("\nDiagnosing Starting Issues...")
                user_input = input("Describe the issue with your car (e.g., 'starter doesn’t crank', 'low battery'): ").lower()
                evidence = self._parse_user_input_starting(user_input)

                if evidence:
                    print(evidence)
                    self.carTroubleshootingExpertSystem.reset()
                    self.carTroubleshootingExpertSystem.declare(CarIssueFact(**evidence))
                    self.carTroubleshootingExpertSystem.run()
                    print(f"\nProblem Result: {self.carTroubleshootingExpertSystem.problem}")
                    print(f"Diagnosis Result: {self.carTroubleshootingExpertSystem.diagnosis}")
                    #Inferir problema por probabilidad
                    result = self.starting_inference.infer_problem(evidence)
                    
                    print(f"\nDiagnosis Result by issue using bayesian networks: {result}")
                    # print("\n\nEnvio de datos (false true) despues de sistema experto", evidence)
                    
                    # Inferir problem por problema (Battery, Starter, Fuel, Ignition)
                    problem,diagnosis = self.starting_inference.infer_problem_by_issue(evidence)
                    print(f"\nProblem Result by issue using knowledge base: {problem}")
                    print(f"\nDiagnosis Result by issue using knowledge base: {diagnosis}\n")
                    
                    
                else:
                    print("Invalid input. Please provide more details about the issue.\n")
                

            elif subsystem == "steering":
                print("\nDiagnosing Steering Problems...")
                # evidence = self._get_steering_evidence()
                # result = self.steering_inference.infer_problem(evidence)
                # print(f"Diagnosis Result: {result['SteeringProblem']}\n")

            else:
                print("Invalid input. Please select 'starting', 'steering', or type 'exit' to quit.\n")
    
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

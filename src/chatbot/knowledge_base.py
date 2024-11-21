import logging
from experta import KnowledgeEngine, Fact, Rule

# Suppress the logging output from Experta
logging.getLogger("experta.watchers").setLevel(logging.ERROR)

class CarIssueFact(Fact):
    """Fact to represent car issues and symptoms."""
    pass

class CarTroubleshootingExpertSystem(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.problem = None
        self.diagnosis = None

    def set_diagnosis(self, problem, diagnosis):
        self.problem = problem
        self.diagnosis = diagnosis
        
    # Rules for Battery-Related Issues
    @Rule(CarIssueFact(StarterCranks=False, BatteryVoltage="low"))
    def battery_issue(self):
        self.set_diagnosis("Battery Issue", "Check the battery voltage and terminals. Recharge or replace the battery if necessary.")

    @Rule(CarIssueFact(StarterSpins=False, BatteryVoltage="high"))
    def solenoid_or_starter_issue(self):
        self.set_diagnosis("Starter Solenoid or Starter Issue", "The starter solenoid might be stuck, or the starter itself is faulty.")

    # Rules for Starter-Related Issues
    @Rule(CarIssueFact(StarterCranks=False, StarterSpins=True, BatteryVoltage="high"))
    def starter_motor_issue(self):
        self.set_diagnosis("Starter Motor Issue", "The starter motor may need repair or replacement.")

    @Rule(CarIssueFact(StarterCranks=False, StarterSpins=False, CleanedTerminals=False))
    def terminal_connection_issue(self):
        self.set_diagnosis("Battery Terminal Connection Issue", "Clean the battery terminals and ensure proper connection.")

    # Rules for Ignition Problems
    @Rule(CarIssueFact(EngineFires=False, SparkToPlugs=False))
    def ignition_problem(self):
        self.set_diagnosis("Ignition System Issue", "Check the ignition coil, distributor, or wiring.")

    @Rule(CarIssueFact(EngineFires=False, SparkToPlugs=True, FuelToFilter=True))
    def ignition_timing_issue(self):
        self.set_diagnosis("Ignition Timing Issue", "Check ignition timing and adjust as needed.")

    # Rules for Fuel-Related Issues
    @Rule(CarIssueFact(EngineFires=False, FuelToFilter=False))
    def fuel_delivery_issue(self):
        self.set_diagnosis("Fuel Delivery Issue", "Check the fuel pump, fuel lines, and fuel filter.")

    @Rule(CarIssueFact(EngineFires=False, FuelToFilter=True, FuelInjected=False))
    def carburetor_issue(self):
        self.set_diagnosis("Carburetor Issue", "Inspect and clean the carburetor.")

    @Rule(CarIssueFact(EngineFires=False, FuelToFilter=True, FuelInjected=True))
    def fuel_injection_issue(self):
        self.set_diagnosis("Fuel Injection Issue", "Check the fuel injectors and related electronics.")

    # Rules for Environmental and Miscellaneous Issues
    @Rule(CarIssueFact(StallsInRain=True))
    def wet_electrical_system(self):
        self.set_diagnosis("Wet Electrical System", "Check for moisture in the ignition system or cracked distributor caps.")

    @Rule(CarIssueFact(EngineFires=False, StallsInRain=False, StallsWarm=True))
    def overheating_issue(self):
        self.set_diagnosis("Overheating Issue", "Check the coolant level, radiator, and thermostat.")

    # Rules for Mechanical Distribution
    @Rule(CarIssueFact(SparkToPlugs=False, MechanicalDistributor=True))
    def mechanical_distributor_issue(self):
        self.set_diagnosis("Mechanical Distributor Problem", "Inspect and replace damaged distributor components like points or rotors.")

    @Rule(CarIssueFact(SparkToPlugs=False, MechanicalDistributor=False))
    def electronic_distribution_issue(self):
        self.set_diagnosis("Electronic Distribution Problem", "Refer to the vehicle's service manual for electronic distribution diagnostics.")
        
    @Rule(CarIssueFact(BatteryIssue=True))
    def car_battery_issue(self):
        self.set_diagnosis("Battery Issue",
            "When the battery voltage is low and the starter motor does not crank, the issue may be that the battery is discharged or faulty."
            "First, ensure the battery terminals are clean and tight. If the connections are in good condition, try recharging the battery with an appropriate charger."
            "If the battery still does not work correctly, it may need to be replaced. Also, check for corrosion on the battery terminals, which could be affecting the current flow."
            "If the problem persists, check the alternator to ensure it is charging the battery correctly while the engine is running."
    )
           
    @Rule(CarIssueFact(StarterIssue=True))
    def car_starter_issue(self):
        self.set_diagnosis("Starter Issue", 
            "When the starter motor does not spin and the battery voltage is high, the problem may be with the starter motor itself or the solenoid. "
            "Check for unusual noises or if the starter motor is stuck. If the solenoid is defective, replace it. If the starter motor is still not functioning, "
            "it may need to be repaired or replaced. It's also important to check the starter motor's power cables to ensure there are no loose or damaged connections that may be preventing operation."
    )
        
    @Rule(CarIssueFact(FuelIssue=True))
    def car_fuel_issue(self):
        self.set_diagnosis("Fuel Issue", 
            "When the engine doesn't start and fuel isn't reaching the filter, there may be an issue with the fuel delivery system. "
            "First, check the fuel filter to see if it is clogged or damaged. If the filter is in good condition, inspect the fuel pump to ensure it's working properly "
            "and sending fuel to the engine. Also, check the fuel lines for any obstructions, leaks, or damage. If the fuel pump or lines are defective, they may need to be repaired or replaced."
    )
        
    @Rule(CarIssueFact(IgnitionIssue=True))
    def car_ignition_issue(self):
        self.set_diagnosis("Ignition Issue", 
            "When the engine doesn't start and there is no spark at the spark plugs, the issue could be with the ignition system. "
            "Check the ignition coil to ensure it is working properly. Also, inspect the distributor, ignition wires, and spark plugs. "
            "If any of these components are faulty, they may be preventing the spark needed to ignite the engine. If everything seems in order, check the electrical connections of the ignition system for any failures or shorts."
    )
    


        
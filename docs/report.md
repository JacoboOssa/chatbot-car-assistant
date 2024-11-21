# Report Integrative Task 2

## Introduction

The project focuses on the development of an AI-driven expert system tailored for car troubleshooting, utilizing Python alongside the Experta and pgmpy libraries. The primary goal is to create a chatbot capable of diagnosing common vehicle issues through Bayesian reasoning and user-friendly conversational interfaces. By bridging the gap between complex automotive diagnostics and everyday users, the system aims to empower individuals with non-technical backgrounds to identify and resolve basic car problems effectively.
This initiative aligns with real-world applications of artificial intelligence, emphasizing accessibility, time savings, and enhanced user confidence in vehicle maintenance. Through systematic steps, including knowledge acquisition, system design, and validation, the project not only addresses technical challenges but also showcases the potential of expert systems in improving daily life experiences.

---

## Problem Statement

Vehicles play a critical role in the daily lives of millions, yet diagnosing and addressing mechanical issues can be daunting for individuals lacking technical expertise. Common problems, such as unusual noises, difficulty starting, or warning lights, often lead to stress, disruptions, and unnecessary expenses when seeking professional assistance for minor issues.

Existing tools and resources for troubleshooting automotive problems are often too technical, fragmented, or inaccessible to the average user. This creates a gap where users cannot independently address straightforward car issues, leading to a reliance on external help for basic diagnostics.

This project seeks to bridge this gap by leveraging artificial intelligence to develop a car troubleshooting chatbot expert system. By integrating Bayesian networks for probabilistic reasoning and rule-based methodologies, the chatbot will provide accurate, user-friendly guidance. This system will enable users to diagnose common car issues effectively, saving time and money while fostering self-sufficiency and confidence in vehicle maintenance.

---

## Objectives

### General Objective:

- Develop a medium-complexity expert system using Python to create an interactive chatbot that assists users in diagnosing and troubleshooting common car problems.

### Specific Objectives:

1. **Knowledge Representation:**
    - Build a comprehensive knowledge base by consulting automotive experts and analyzing technical manuals to model common car issues, symptoms, and solutions.
2. **Bayesian Network Integration:**
    - Implement probabilistic reasoning using pgmpy to assess relationships between symptoms, possible diagnoses, and recommendations for troubleshooting.
3. **User-Centric Design:**
    - Develop a conversational chatbot interface that is intuitive and accessible to users without technical backgrounds.
4. **Expert System Framework:**
    - Use the Experta library to design rule-based reasoning modules that complement Bayesian networks and support decision-making.
5. **Scalability and Usability Testing:**
    - Evaluate the chatbot's accuracy, performance, and user experience through rigorous testing with a diverse user base.
6. **Deployment and Documentation:**
    - Deploy the chatbot on a suitable platform (e.g., web or messaging application) and provide clear documentation for users and developers to interact with and maintain the system.

---

## **Scope of Car Troubleshooting Issues**

- The chatbot will address **common car troubleshooting scenarios** involving:
    - Engine problems (e.g., difficulty starting, strange noises, overheating).
    - Electrical system issues (e.g., battery drain, flickering lights).
    - Brake system faults (e.g., squealing noises, reduced effectiveness).
    - Warning lights (e.g., check engine light, ABS light).
    - Disturbing sounds (e.g., noise on bumps, ticks rolling in neutral).
- The chatbot will provide **diagnostic guidance** and **potential fixes** but not detailed repair procedures.

---

## **Target User Demographics and Needs**

- **Target Users**:
    - Car owners with minimal technical knowledge.
    - Individuals looking to save time and money on minor troubleshooting.
    - Users who want an accessible, on-demand diagnostic tool.
- **User Needs**:
    - A user-friendly interface that simplifies interaction.
    - Step-by-step guidance tailored to the user’s car symptoms.
    - Recommendations presented in clear, non-technical language.
    - Ability to understand reasoning behind recommendations.

---

## Requirements

### Client

- **Chatbot Functionality**:
    - Conversational input and output using natural language (e.g., "My car won't start").
    - Ability to ask follow-up questions to refine diagnoses.
- **Interaction Flow**:
    - Welcome and introduction: Brief explanation of chatbot’s purpose.
    - Symptom identification: Users describe issues; chatbot clarifies specifics.
    - Diagnosis and recommendations: Chatbot suggests possible causes and fixes.
    - Feedback loop: Users confirm or reject suggestions to refine accuracy.
- **Accessibility**:
    - Desktop-friendly design.
    - Text input.
- **Visuals**:
    - Use of simple icons and visuals to represent car systems.
    - Color-coded responses for severity (e.g., green = minor issue, red = critical).

### Server

**Framework and Libraries**:

- Python-based implementation using Experta for rule-based reasoning.
- Bayesian network modeling with the pgmpy library.
- **Knowledge Base**:
    - A modular knowledge base categorizing car systems and issues.
    - Data sources: Manufacturer repair manuals and troubleshooting guides.
- **Database Requirements**:
    - Storage for user profiles, conversation logs, and historical troubleshooting data.
    - Integration with external data sources for enhanced diagnostics, if needed.

---

## Knowledge Acquisition and Representation

**Knowledge Acquisition:** The foundation of the expert system lies in gathering accurate and comprehensive knowledge from the automotive domain. This process includes the following steps:

1. **Consultation with Automotive Experts:**
    - Engage experienced mechanics and technicians to gain insights into diagnosing common car issues. Their expertise will help identify typical symptoms, underlying causes, and practical troubleshooting techniques.
    - Conduct interviews or workshops to understand patterns in automotive diagnostics and the decision-making process.
2. **Literature and Technical Resources:**
    - Collect information from technical manuals, repair guides, and automotive diagnostic flowcharts provided by manufacturers or industry standards.
    - Focus on systems such as the engine, brakes, electrical components, and drivetrain to ensure broad diagnostic coverage.
3. **Compilation of a Knowledge Base:**
    - Organize data into a structured repository, categorizing information by symptoms, probable causes, and suggested fixes. For example:
        - **Symptom:** Difficulty starting the car
        - **Probable Causes:** Weak battery, faulty starter motor, fuel system issues
        - **Fixes:** Replace battery, inspect starter motor, check fuel pump
    - Create standardized diagnostic pathways for each subsystem to guide the chatbot's reasoning.
4. **Probabilistic Modeling:**
    - Use Bayesian networks to map probabilistic relationships between symptoms and potential diagnoses.
    - For example, if a user reports "engine overheating," the Bayesian network could calculate the likelihood of causes such as "low coolant levels," "failed thermostat," or "damaged radiator."

---

## System Design and Implementation Details

The expert system for car troubleshooting is architected as a modular and scalable application, integrating components to handle knowledge representation, user interaction, and decision-making processes. The system design is outlined below:

### **User Interface**

- **Frontend Integration**: The chatbot is designed to engage users through a conversational interface, which can be hosted on a web server or messaging application.
- **Interaction Flow**: Users input symptoms (e.g., "engine not starting"), and the chatbot guides them through relevant questions to refine the diagnosis.
- **API Integration**: The `routes/chatbot_routes.py` module provides endpoints to facilitate communication between the frontend and backend.

### **Backend Logic**

- **Chatbot Core Logic**: Located in the `chatbot` module, it comprises:
    - **Knowledge Base (`knowledge_base.py`)**: Stores structured data on car systems, symptoms, and corresponding diagnoses.
    - **Dialog Manager (`dialog_manager.py`)**: Directs the conversation flow, ensuring meaningful interactions based on user input.
    - **Inference Engine (`inference/`)**: Implements Bayesian reasoning using the pgmpy library to calculate probabilities and suggest likely causes and solutions.
- **Service Layer**:
    - Centralized in the `services/user_services.py` module, it handles user-specific operations, including session management and data persistence.

### **Data Management**

- **Database Configuration (`database/db.py`)**:
    - Sets up the backend database to store user profiles, conversation logs, and troubleshooting data.
    - Facilitates robust data querying and updates through `queries.py`.
- **Data Models (`models/`)**:
    - **User Model (`users.py`)**: Tracks user information and interaction history.
    - **Request Model (`requests.py`)**: Represents and validates user inputs for seamless backend processing.

### **Knowledge Representation and Reasoning**

- **Rule-Based Reasoning**:
    - Implemented in the `chatbot/knowledge_base.py` module using the Experta library, allowing the system to infer diagnoses from predefined rules.
- **Probabilistic Reasoning**:
    - Powered by the Bayesian inference engine in the `chatbot/inference/` submodule, which quantifies uncertainties and dependencies between symptoms and potential causes.

### **Modular Design for Scalability**

- **Core Application (`app.py`)**:
    - Acts as the main orchestrator, integrating all modules and initializing services at runtime.
- **Modular Packages**:
    - Each functionality is encapsulated in distinct modules (e.g., `routes`, `services`, `chatbot`), ensuring ease of maintenance and extensibility.

---

This design ensures a seamless flow of data and interactions, allowing the chatbot to provide accurate diagnostics and recommendations based on user input. The modular architecture supports future enhancements, such as integrating advanced machine learning models or expanding the knowledge base.

---

## Testing and Validation

Testing and validation are critical to ensuring the expert system's functionality, accuracy, and usability. A comprehensive strategy is employed to evaluate the system across various dimensions, leveraging both automated testing methods and user feedback.

### **Functional Testing**

This phase ensures that all components of the system work as intended:

- **Chatbot Functionality**:
    - Test the dialogue flow managed by `dialog_manager.py` to ensure logical progression of conversations based on user input.
    - Validate the chatbot's ability to understand and respond to symptoms, using predefined test cases (e.g., "engine not starting").
    - Verify the `knowledge_base.py` for accurate application of rules and retrieval of recommendations.
- **Inference Engine**:
    - Assess the `inference/` submodule to ensure Bayesian reasoning correctly computes probabilities for various diagnoses.
    - Test different combinations of symptoms to validate the accuracy of probabilistic outputs.
- **API Endpoints**:
    - Perform unit and integration tests for endpoints in `routes/chatbot_routes.py` to confirm proper data exchange between the frontend and backend.

### **Usability Testing**

This step focuses on the user experience:

- **Representative Users**:
    - Conduct testing sessions with target users, such as car owners with minimal technical expertise.
    - Gather feedback on the chatbot's ease of use, response clarity, and overall interaction experience.
- **Interface Validation**:
    - Evaluate the chatbot's frontend for intuitive design, ensuring users can input symptoms effortlessly and understand the provided solutions.

### **Knowledge Base Validation**

The validity and comprehensiveness of the knowledge base are tested:

- **Domain Expert Review**:
    - Consult automotive experts to verify the correctness of the rules in `knowledge_base.py`.
    - Cross-check the knowledge base against industry-standard repair guides to ensure alignment with real-world practices.
- **Consistency Checks**:
    - Ensure the rules and Bayesian networks cover all anticipated scenarios without contradictions or gaps.

### **Performance Testing**

Evaluate the system's performance under varying conditions:

- **Stress Testing**:
    - Simulate multiple simultaneous user interactions to test the scalability of the system.
    - Assess database performance (`database/db.py` and `queries.py`) during high read/write operations.
- **Response Time**:
    - Measure the system's latency in processing user inputs and generating responses, ensuring real-time interaction.

### **Validation Against Automotive Guidelines**

- Compare the chatbot’s diagnostic suggestions with standardized automotive diagnostic flowcharts and repair manuals.
- Use specific test scenarios (e.g., overheating engine, weak battery) to confirm alignment with established troubleshooting procedures.

### **Automated Testing**

- Implement unit tests for individual modules:
    - **Knowledge Base Tests**:
        - Validate rule execution and output consistency using test cases for various symptoms.
    - **Inference Tests**:
        - Test Bayesian network responses for probabilistic reasoning.
- Utilize Python's testing frameworks (e.g., `pytest`) for automated test execution and reporting.

### **User Feedback Integration**

- Post-deployment, gather user feedback through conversation logs stored in the database.
- Refine the knowledge base and Bayesian networks based on common issues reported by users.

### **Documentation and Debugging**

- Maintain a detailed log of testing procedures and outcomes.
- Address issues highlighted during testing and iteratively refine the system before final deployment.

By integrating functional, usability, and performance testing with expert validation and user feedback, the system achieves high reliability and accuracy. This comprehensive approach ensures the chatbot is not only effective in diagnosing car issues but also user-friendly and robust in handling real-world interactions.

---

## Deployment

The deployment of the car troubleshooting expert system involves making the backend and frontend available on reliable platforms for user interaction. Leveraging **Render** for backend deployment and **Vercel** for frontend deployment ensures a seamless and scalable architecture, enabling efficient user experiences and robust system performance.

### **Backend Deployment on Render**

The backend, built using Python, integrates multiple modules for chatbot logic, inference engines, and database management. Deployment on Render involves:

- **Setup Process:**
    - Push the backend code to a GitHub repository, ensuring all modules (`chatbot`, `database`, `routes`, and `services`) are correctly structured.
    - Configure a Render web service linked to the repository for continuous deployment.
- **Environment Configuration:**
    - Define necessary environment variables (e.g., database credentials, API keys) in Render’s environment settings.
    - Ensure that dependencies in `requirements.txt` are correctly listed for Render to install them during deployment.
- **Database Integration:**
    - Set up the database using Render’s managed database services or connect to an external PostgreSQL database.
    - Test `database/db.py` and `queries.py` to confirm connectivity and data persistence.
- **Scalability:**
    - Configure auto-scaling settings to handle varying loads, particularly during high user interactions.
    - Perform stress tests post-deployment to ensure stability under concurrent requests.
- **Monitoring and Logs:**
    - Utilize Render’s integrated monitoring tools to track the system’s performance and identify bottlenecks.
    - Enable error logging to debug issues in `chatbot_routes.py` or other backend modules.

### **Frontend Deployment on Vercel**

The frontend, serving as the user interface for the chatbot, is hosted on Vercel for rapid, reliable, and globally distributed deployment.

- **Setup Process:**
    - Push the frontend code (likely built with JavaScript or React) to a GitHub repository, ensuring it is integrated with the backend API endpoints.
    - Link the repository to a Vercel project, enabling automated deployments with every update.
- **Configuration:**
    - Specify environment variables in Vercel, including the backend API URL hosted on Render, to ensure smooth communication.
    - Optimize static assets and dynamic components for fast loading times and responsiveness.
- **User Interaction:**
    - Test the chatbot's conversational interface on Vercel’s staging and production environments.
    - Verify API calls from the frontend to backend endpoints (e.g., `chatbot_routes.py`) for accurate data exchange.
- **SEO and Accessibility:**
    - Optimize the frontend for search engine indexing to enhance discoverability.
    - Ensure the interface adheres to accessibility standards, making it usable for diverse audiences.

### **Integration Testing Post-Deployment**

- Conduct end-to-end tests to validate the seamless integration between the frontend and backend.
- Simulate user sessions to evaluate the chatbot's functionality, from input submission to receiving diagnoses.

### **User Access**

- **Frontend Access:** Users interact with the chatbot through the Vercel-hosted frontend, accessible via a user-friendly URL.
- **Backend Access:** Render manages backend requests, ensuring the inference engine and database operations run smoothly.

By deploying the backend on Render and the frontend on Vercel, the system ensures a reliable, scalable, and user-friendly solution. This deployment strategy supports efficient car troubleshooting for users, enhancing their experience with minimal latency and high availability.

---

## Conclusions

The development of the car troubleshooting expert system showcases the practical application of artificial intelligence in addressing everyday challenges. By integrating rule-based reasoning with Bayesian inference, the chatbot provides users with accurate and context-sensitive diagnoses for common car issues. The project emphasizes the potential of AI to bridge knowledge gaps, empowering individuals with minimal technical expertise to make informed decisions.

**Key Outcomes:**

1. **Enhanced Accessibility:** The chatbot democratizes access to automotive diagnostics, enabling users to identify and resolve issues without requiring professional intervention.
2. **Effective Knowledge Representation:** The structured knowledge base and probabilistic reasoning models ensure accurate and reliable suggestions tailored to user inputs.
3. **Scalable Architecture:** The modular design, deployed on Render (backend) and Vercel (frontend), provides a robust, scalable platform capable of handling diverse user scenarios.
4. **Real-World Impact:** The project demonstrates how AI can reduce the stress and costs associated with vehicle maintenance while fostering greater confidence in technology among users.

---

## Future Work

The system lays a strong foundation for further enhancements, which can significantly expand its functionality and impact:

1. **Expansion of Knowledge Base:**
    - Include more complex troubleshooting scenarios and a broader range of car systems (e.g., hybrid and electric vehicles).
    - Regularly update the knowledge base with insights from automotive experts and emerging repair practices.
2. **Integration of Machine Learning:**
    - Employ natural language processing (NLP) models to improve user input comprehension, making interactions more intuitive.
    - Use machine learning to refine probabilistic models based on user feedback and historical data.
3. **Multilingual Support:**
    - Expand the chatbot’s language capabilities to serve non-English-speaking users, increasing its accessibility globally.
4. **Mobile and IoT Integration:**
    - Develop a mobile application for enhanced accessibility and convenience.
    - Integrate with IoT-enabled vehicles to gather real-time diagnostic data, allowing proactive issue identification.
5. **Enhanced User Experience:**
    - Add visual aids such as diagrams or animations to explain recommended fixes.
    - Implement voice interaction capabilities for hands-free troubleshooting.
6. **Community Contributions:**
    - Create an open-source repository to encourage community contributions, enabling the system to grow and evolve with user input.
7. **Integration with Automotive Services:**
    - Connect the chatbot with local mechanics or service providers, allowing users to book repairs directly based on the chatbot’s diagnosis.

---

## References

https://www.team-bhp.com/forum/technical-stuff/121153-flow-charts-troubleshooting-car-problems.html

https://www.onallcylinders.com/2016/12/14/infographic-guide-to-diagnosing-common-starting-problems/

https://news.carjunky.com/

https://chatgpt.com/c/673d2e26-d734-8000-a39c-7151cdace7eb
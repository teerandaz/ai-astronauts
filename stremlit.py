import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser

# Streamlit App Title
st.title("🚀 Multi-Agent AI System for Mars Missions")

# API Configuration (Should use environment variables in production)
api_key = "======="
base_url = "======="

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", api_key=api_key, base_url=base_url)

# Utility function to create agents
def create_agent(prompt_template: str, llm):
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    return chain

# Define coordinators
class SpacecraftCoordinator:
    def __init__(self, llm):
        self.communication_agent = create_agent(
            "Relay this message from Earth to Mars: {message}",
            llm
        )
        self.navigation_agent = create_agent(
            "Based on position data: {position_data}, calculate trajectory adjustment for Mars.",
            llm
        )

    def route_to_agent(self, input_data):
        decision = llm.invoke(f"Classify: {input_data}. Should this be handled by communication or navigation?").lower()
        if "communication" in decision:
            return self.communication_agent.invoke({"message": input_data})
        elif "navigation" in decision:
            return self.navigation_agent.invoke({"position_data": input_data})
        return "No agent activated."

class LanderCoordinator:
    def __init__(self, llm):
        self.landing_agent = create_agent(
            "Analyze landing site: {landing_data}. Safe to land?",
            llm
        )
        self.power_management_agent = create_agent(
            "Monitor power: {power_levels}. Suggest energy conservation.",
            llm
        )

    def route_to_agent(self, input_data):
        decision = llm.invoke(f"Classify: {input_data}. Should this be handled by landing or power management?").lower()
        if "landing" in decision:
            return self.landing_agent.invoke({"landing_data": input_data})
        elif "power" in decision:
            return self.power_management_agent.invoke({"power_levels": input_data})
        return "No agent activated."

class RoverCoordinator:
    def __init__(self, llm):
        self.object_detection_agent = create_agent(
            "Identify object: height={height}, width={width}.",
            llm
        )
        self.temperature_reader_agent = create_agent(
            "Analyze temperature: {temperature_data}.",
            llm
        )
        self.sample_collection_agent = create_agent(
            "Collect sample at {location} using {sample_parameters}.",
            llm
        )

    def route_to_agent(self, input_data):
        decision = llm.invoke(f"Classify: {input_data}. Should this be handled by object detection, temperature, or sample collection?").lower()
        if "object" in decision:
            return self.object_detection_agent.invoke({"height": 100, "width": 50})
        elif "temperature" in decision:
            return self.temperature_reader_agent.invoke({"temperature_data": "-60°C"})
        elif "sample" in decision:
            return self.sample_collection_agent.invoke({"location": "Rocky site", "sample_parameters": "500g rock"})
        return "No agent activated."

# Initialize Coordinators
spacecraft_coordinator = SpacecraftCoordinator(llm)
lander_coordinator = LanderCoordinator(llm)
rover_coordinator = RoverCoordinator(llm)

# Streamlit Interface
st.subheader("Mission Control Panel")

# User Input for Mission Data
input_data = st.text_area("Enter data for the mission (e.g., position, message, temperature)")

# Select Agent Type
agent_choice = st.selectbox(
    "Choose which coordinator should handle this data:",
    ["Spacecraft", "Lander", "Rover"]
)

# Button to Run the Model
if st.button("Execute Task"):
    if agent_choice == "Spacecraft":
        response = spacecraft_coordinator.route_to_agent(input_data)
    elif agent_choice == "Lander":
        response = lander_coordinator.route_to_agent(input_data)
    elif agent_choice == "Rover":
        response = rover_coordinator.route_to_agent(input_data)
    else:
        response = "Invalid selection"

    st.subheader("🔍 AI Agent Response:")
    st.write(response)

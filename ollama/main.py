


from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process


# Define email to be classified and responded to
EMAIL = "nigerian prince sending some gold"

# Initialize LLaMA model
model = Ollama(model="llama3.1:8b")

# Define classification and response agents
classifier = Agent(
    role="Email Classifier",
    goal="Accurately classify emails based on their importance.",
    backstory="I am a machine learning model trained on a large dataset of emails.",
    verbose=True,
    allow_delegation=False,
    llm=model,
)

responder = Agent(
    role="Email Responder",
    goal=(
        "Based on the importance of the email, respond to the email with a relevant response."
        "\nIf the email is important, respond with a formal response."
        "\nIf the email is casual, respond with a casual response."
        "\nIf the email is spam, respond with a spam response."
    ),
    backstory="I am a machine learning model trained on a large dataset of emails.",
    verbose=True,
    allow_delegation=False,
    llm=model,
)

# Define tasks for classification and response
# Define tasks for classification and response
classify_email = Task(
    description=f"Classify the following email: {EMAIL}",
    agent=classifier,
    expected_output=("important", "casual", "spam"),
)

respond_to_email = Task(
    description=f"Respond to the email based on its importance provided by the 'classifier' agent",
    agent=responder,
    expected_output="A concise response",
)


# Create a crew with both agents and tasks
crew = Crew(
    agents=[classifier, responder],
    tasks=[classify_email, respond_to_email],
    verbose=2,
    process=Process.sequential,
)

output = crew.kickoff()
print(output)
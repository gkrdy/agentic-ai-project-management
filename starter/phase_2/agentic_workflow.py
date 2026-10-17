# agentic_workflow.py
from workflow_agents.base_agents import  ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

import os
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open("Product-Spec-Email-Router.txt","r") as file:
    product_spec = file.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "You should return clean plan based on your knowledge in steps. "
    "You have product manager, program manager and dev engineer agents"
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
     "To define the development tasks for a product, always return exactly these three steps, one per line, with no other text:\n"
    "1. Define the user stories from the product spec\n"
    "2. Define the product features by grouping the user stories\n"
    "3. Define the development tasks for each user story"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key,knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    f"{product_spec}"
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key,persona_product_manager,knowledge_product_manager)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
product_manager_evaluation_agent_persona="You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."

product_manager_evaluation_agent =EvaluationAgent(openai_api_key,product_manager_evaluation_agent_persona,evaluation_criteria,product_manager_knowledge_agent,5)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = f"""Features of a product are defined by organizing similar user stories into cohesive groups.
                         Answer should have the exact labels Feature Name, Description,Key Functionality, User Benefit.
                         Create minimum 3 features.
                       """
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent= KnowledgeAugmentedPromptAgent(openai_api_key,persona_program_manager,knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
persona_program_manager_eval_criteria = f"""
-  Label for Feature Name should be Feature Name not Feature paird with number as Feature 1
- "The answer should be product features that follow the following structure: " 
- "Feature Name: A clear, concise title that identifies the capability\n" 
- "Description: A brief explanation of what the feature does and its purpose\n" 
- "Key Functionality: The specific capabilities or actions the feature provides\n" 
- "User Benefit: How this feature creates value for the user"
"""
program_manager_evaluation_agent =EvaluationAgent(openai_api_key,persona_program_manager_eval,persona_program_manager_eval_criteria,program_manager_knowledge_agent,5)


# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = f"""Development tasks are defined by identifying what needs to be built to implement each user story. Write exactly 1 task per user story. 
    Write each task with these exact labels: Task ID, Task Title, Related User Story, Description, Acceptance Criteria, Estimated Effort, Dependencies.
    Example of Task Id  is Task ID :1. not Task 1
    """
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent= KnowledgeAugmentedPromptAgent(openai_api_key,persona_dev_engineer,knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
persona_dev_engineer_eval_criteria= f"""
                      "The answer should be tasks following this exact structure: " 
                      "Task ID: A unique identifier for tracking purposes\n" 
                      "Task Title: Brief description of the specific development work\n" 
                      "Related User Story: Reference to the parent user story not a feature\n" \
                      "Description: Detailed explanation of the technical work required\n" 
                      "Acceptance Criteria: Specific requirements that must be met for completion\n" 
                      "Estimated Effort: Time or complexity estimation\n" 
                      "Dependencies: Any tasks that must be completed first"
"""
development_engineer_evaluation_agent =EvaluationAgent(openai_api_key,persona_dev_engineer_eval,persona_dev_engineer_eval_criteria,development_engineer_knowledge_agent,10)


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routing_agent = RoutingAgent(openai_api_key, {})
agents = [
    {
        "name": "Product Manager",
        "description": "Define the user stories from the product spec",
        "func": lambda x: product_manager_support_function(x)
    },
    {
        "name": "Program Manager",
        "description": "Resposible for defining the features for a product by grouping related user stories",
        "func": lambda x: program_manager_support_function(x)
    },
    {
        "name": "Development Engineer",
        "description": "You are responsible for defining the development and engineering tasks for each user story.",
        "func" :lambda x: development_engineer_support_function(x)
    }
]
routing_agent.agents = agents

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.
def program_manager_support_function(query):
   program_manager_evaluation_agent_response = program_manager_evaluation_agent.evaluate(query)
   return program_manager_evaluation_agent_response["final_response"]

def product_manager_support_function(query):
   product_manager_evaluation_agent_response = product_manager_evaluation_agent.evaluate(query)
   return product_manager_evaluation_agent_response["final_response"]

def development_engineer_support_function(query):
   development_engineer_evaluation_agent_response = development_engineer_evaluation_agent.evaluate(query)
   return development_engineer_evaluation_agent_response["final_response"]



# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = f"What would the development tasks for this product be?"
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).

workflow_steps= action_planning_agent.extract_steps_from_prompt(workflow_prompt)
completed_steps =[]
step_history = []
for i, step in enumerate(workflow_steps, start=1):
   print(f"\n--- Executing step {i}: {step} ---")
   result = routing_agent.route_to_agent(step)
   completed_steps.append(result)
   step_history.append({"step":step,"result":result})
   previous = "\n\n".join(
        f"Step: {h['step']}\nResult:\n{h['result']}"
        for h in step_history
   )
   program_manager_knowledge_agent.knowledge = knowledge_program_manager + "\n\nResults of previous steps:\n" + previous
   development_engineer_knowledge_agent.knowledge = knowledge_dev_engineer + "\n\nResults of previous steps:\n" + previous
   print(f"Result of step {i}:\n{result}")
print("\n*** Workflow completed. All completed steps: ***")
for i, step_result in enumerate(completed_steps, start=1):
    print(f"\n--- Completed step {i} ---")
    print(step_result)


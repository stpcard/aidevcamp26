from google.adk.agents.llm_agent import Agent
#from google.adk.tools import google_search
from datetime import datetime
from travel_planner_agent.travel_agent.agent import travel_agent
from travel_planner_agent.weather_agent.agent import weather_agent
from travel_planner_agent.hotel_agent.agent import hotel_agent

#def now() -> dict:
#    """Returns the current date and time."""
#    my_datetime = datetime.now()
#    return {
#        "status": "success",
#        "current_time": str(my_datetime)
#    }

#root_agent = Agent(
#    model='gemini-2.5-flash',
#    name='root_agent',
#    description='A helpful assistant for user questions.',
#    instruction='Answer user questions to the best of your knowledge',
#    sub_agents=[travel_agent],


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Main agent that routes tasks to sub-agents",
    instruction="""
You are the main assistant.

You decide which sub-agent should handle the user request:

- If the request is about travel, use travel_agent
- Otherwise answer directly or route accordingly

Be smart in routing user queries.
""",
    sub_agents=[travel_agent, weather_agent, hotel_agent]
)

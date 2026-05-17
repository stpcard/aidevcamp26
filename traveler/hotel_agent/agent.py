"""
Travel Agent module using Google ADK.
This module defines a travel agent with Airbnb access via MCP.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from urllib.parse import quote_plus

def now() -> dict:
    """Returns the current date and time in Europe/London."""
    current_dt = datetime.now(ZoneInfo("Europe/London"))
    return {
        "status": "success",
        "current_time": current_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
    }

def search_flights_simple(origin: str, destination: str, date: str) -> dict:
    """Returns a Google Flights search link."""
    query = f"Flights from {origin} to {destination} on {date}"
    url = f"https://www.google.com/travel/flights?q={quote_plus(query)}"
    return {
        "status": "success",
        "message": "Here are available flight options.",
        "origin": origin,
        "destination": destination,
        "date": date,
        "booking_url": url,
    }


airbnb_mcp = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@openbnb/mcp-server-airbnb@0.1.2",
                "--ignore-robots-txt",
            ],
        ),
        timeout=30,
    )
)

flight_agent = Agent(
    name="flight_agent",
    model="gemini-2.5-flash",
    description="Handles flight searches and returns Google Flights links.",
    tools=[search_flights_simple],
    instruction="""
You are a helpful flight booking assistant.

Your job is to help users find flights.

Rules:
- Use search_flights_simple when the user asks for flights.
- If origin, destination, or travel date is missing, ask one short follow-up question.
- Always include the booking link in your response.
- Keep the answer short and practical.
""",
)

itinerary_agent = Agent(
    name="itinerary_agent",
    model="gemini-2.5-flash",
    description="Creates day-by-day travel itineraries based on destination, trip length, and interests.",
    tools=[now],
    instruction="""
You are a helpful itinerary planner.

Your job is to create practical travel itineraries.

Rules:
- Build a clear day-by-day itinerary.
- Use morning / afternoon / evening structure when useful.
- Group nearby places together to keep the plan realistic.
- Suggest food, sightseeing, and local experiences when relevant.
- If destination, trip length, or interests are missing, ask one short follow-up question.
- Use the now tool only if the user asks for the current date or time.
- Keep the itinerary easy to read.
""",
)
#
#root_agent = Agent(
#    name="travel_agent",
#    model="gemini-2.5-flash",
#    tools=[now, airbnb_mcp],
#    instruction="""
#You are a helpful travel agent.

#Your job is to help the user plan trips and find Airbnb stays.

#Available tools:
#- Use the Airbnb MCP tools to search for accommodation and pricing.
#- Use the now tool only when the user asks for the current date or time.

#Rules:
#- Do not use Google Search.
#- If the user has not provided enough details, ask one short follow-up question.
#- For stay suggestions, include location, approximate cost, and why it matches.
#- When finished, reply with "DONE".
#""",
#)

root_agent = Agent(
    name="travel_agent",
    model="gemini-2.5-flash",
    description="Main travel planning agent that coordinates flights, stays, and itineraries.",
    sub_agents=[flight_agent, stay_agent, itinerary_agent],
    instruction="""
You are a helpful travel agent.

Your job is to help the user plan trips, find flights, Airbnb stays, and create itineraries.

Available specialists:
- flight_agent for flights
- stay_agent for Airbnb stays
- itinerary_agent for trip plans

Rules:
- Delegate to the correct specialist based on the user's request.
- If the user asks for a complete trip, help with flights, stay, and itinerary.
- If the user has not provided enough details, ask one short follow-up question.
- Keep answers simple and helpful.
- When finished, reply with "DONE".
""",
)
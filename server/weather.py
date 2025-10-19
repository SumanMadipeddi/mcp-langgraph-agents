from mcp.server.fastmcp import FastMCP
import httpx
from typing import Any

mcp = FastMCP("weather")

API_BASE="https://api.weather.gov"
user_agent="weather-app/1.0"

async def make_request(url:str)-> dict[str:Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def feature_alert(feature:str)->str:
    
    feat=feature["properties"]
    return f"""
    Event: {feat.get('event', 'unknown')}
    Area: {feat.get('areaDesc', 'Unknown')}
    Severity: {feat.get('severity', 'Unknown')}
    Description: {feat.get('description', 'No description available')}
    Instructions: {feat.get('instruction', 'No specific instructions provided')}
    """


@mcp.tool()

async def get_alerts(state:str)->str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url=f"{API_BASE}/alerts/active/area/{state}"
    data=await make_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts"

    if not data["features"]:
        return "No active alerts"
    
    alerts= [feature_alert(feature) for feature in data["features"]]

    return "\n---\n".join(alerts)

@mcp.resource("echo://{message}")
def echo_resource(message:str)->str:
    return f"Resource message:{message}"
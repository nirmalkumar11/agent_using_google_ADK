import os
from dotenv import load_dotenv
load_dotenv()
import time
import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from google.adk.agents.llm_agent import Agent
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz



def get_time(city:str) ->str:
    """
    Returns the current time in the specified city.

    Args:
        city (str): City name or address to geocode.

    Returns:
        dict: {
            "status": "success" or "error",
            "report": "Human readable message with time" (on success),
            "timezone": "<IANA timezone name>" (optional)
        }
    """

    #geolocator = Nominatim(user_agent="geoapiExercises")
    user_agent = "adk_time_agent/1.0 (os.environ.get('email'))"
    geolocator = Nominatim(user_agent=user_agent)
    location = geolocator.geocode(city)

    # if location:
    #     print("Location found!")
    #     print(f"Address: {location.address}")
    #     print(f"Latitude: {location.latitude}")
    #     print(f"Longitude: {location.longitude}")
        
    # else:
    #     print("Location not found!")

    if location:
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=location.latitude, lng=location.longitude)
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        return ("Timezone name:", tz_name,f"{city} time:", now.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return ("City not found!")

    # tz = timezone(city_timezones)
    # city_time = datetime.now(tz)
    # return city_time.strftime(f"The current time in {city} is %Y-%m-%d %H:%M:%S")

root_agent= Agent(
    model='gemini-2.5-flash',
    name="time_agent",
    description="you are a time agent, you can provide current time for any city as user requested",
    instruction="you are helpful agent, you can leverage get_time function to provide current time for specific city",
    tools=[get_time]
)



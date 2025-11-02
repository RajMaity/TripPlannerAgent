import streamlit as st
import json
import os
from serpapi import GoogleSearch
from datetime import datetime
import google.generativeai as genai
from dotenv import dotenv_values

# --- CrewAI Imports ---
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# Setting API Keys
config = dotenv_values(".env")
SERPAPI_KEY = config["SERPAPI_KEY"]
GOOGLE_API_KEY = config["GEMINI_API_KEY"]
# os.environ['SERPER_API_KEY'] = config["SERPAPI_KEY"]
os.environ['SERPER_API_KEY'] = config["SERPERDEV_API_KEY"]
# os.environ["OPENAI_API_KEY"] = "sk-..."  # CrewAI uses OpenAI by default, you can configure to use Gemini

# Configuring Gemini
my_llm = LLM(
              model='gemini/gemini-2.5-flash',
              api_key=GOOGLE_API_KEY
            )

# Streamlit UI Setup
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #ff5733;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #555;
        }
        .stSlider > div {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and subtitle
st.markdown('<h1 class="title">✈️ AI-Powered Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plan your dream trip with AI! Get personalized recommendations for flights, hotels, and activities.</p>', unsafe_allow_html=True)

# User Inputs Section
st.markdown("### 🌍 Where are you headed?")
source = st.text_input("🛫 Departure City (IATA Code):", "BOM")
destination = st.text_input("🛬 Destination (IATA Code):", "DEL")

st.markdown("### 📅 Plan Your Adventure")
num_days = st.slider("🕒 Trip Duration (days):", 1, 14, 5)
travel_theme = st.selectbox(
    "🎭 Select Your Travel Theme:",
    ["💑 Couple Getaway", "👨‍👩‍👧‍👦 Family Vacation", "🏔️ Adventure Trip", "🧳 Solo Exploration"]
)

# Divider
st.markdown("---")

st.markdown(
    f"""
    <div style="
        text-align: center; 
        padding: 15px; 
        background-color: #ffecd1; 
        border-radius: 10px; 
        margin-top: 20px;
    ">
        <h3>🌟 Your {travel_theme} to {destination} is about to begin! 🌟</h3>
        <p>Let's find the best flights, stays, and experiences for your unforgettable journey.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

def format_datetime(iso_string):
    try:
        dt = datetime.strptime(iso_string, "%Y-%m-%d %H:%M")
        return dt.strftime("%b-%d, %Y | %I:%M %p")
    except:
        return "N/A"

activity_preferences = st.text_area(
    "🌍 What activities do you enjoy? (e.g., relaxing on the beach, exploring historical sites, nightlife, adventure)",
    "Relaxing on the beach, exploring historical sites"
)

departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")

# Sidebar Setup
st.sidebar.title("🌎 Travel Assistant")
st.sidebar.subheader("Personalize Your Trip")
budget = st.sidebar.radio("💰 Budget Preference:", ["Economy", "Standard", "Luxury"])
flight_class = st.sidebar.radio("✈️ Flight Class:", ["Economy", "Business", "First Class"])
hotel_rating = st.sidebar.selectbox("🏨 Preferred Hotel Rating:", ["Any", "3⭐", "4⭐", "5⭐"])

st.sidebar.subheader("🎒 Packing Checklist")
packing_list = {
    "👕 Clothes": True,
    "🩴 Comfortable Footwear": True,
    "🕶️ Sunglasses & Sunscreen": False,
    "📖 Travel Guidebook": False,
    "💊 Medications & First-Aid": True
}
for item, checked in packing_list.items():
    st.sidebar.checkbox(item, value=checked)

st.sidebar.subheader("🛂 Travel Essentials")
visa_required = st.sidebar.checkbox("🛃 Check Visa Requirements")
travel_insurance = st.sidebar.checkbox("🛡️ Get Travel Insurance")
currency_converter = st.sidebar.checkbox("💱 Currency Exchange Rates")


params = {
        "engine": "google_flights",
        "departure_id": source,
        "arrival_id": destination,
        "outbound_date": str(departure_date),
        "return_date": str(return_date),
        "currency": "INR",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

# Function to fetch flight data (remains the same)
def fetch_flights(source, destination, departure_date, return_date):
    params = {
        "engine": "Google Flights",
        "departure_id": source,
        "arrival_id": destination,
        "outbound_date": str(departure_date),
        "return_date": str(return_date),
        "currency": "INR",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results

def extract_cheapest_flights(flight_data):
    best_flights = flight_data.get("best_flights", [])
    sorted_flights = sorted(best_flights, key=lambda x: x.get("price", float("inf")))[:3]
    return sorted_flights

# --- CrewAI Agent and Task Definitions ---
search_tool = SerperDevTool()

# Define the agents
researcher_agent = Agent(
    role='Travel Researcher',
    goal=f"Gather comprehensive information on {destination} for a {num_days}-day {travel_theme} trip.",
    backstory=(
        "An expert travel analyst who specializes in finding detailed information "
        "about destinations, including climate, culture, popular attractions, and safety tips."
    ),
    llm = my_llm,
    tools=[search_tool],
    verbose=True,
    allow_delegation=False
)

planner_agent = Agent(
    role='Itinerary Planner',
    goal=f"Create a personalized, detailed {num_days}-day itinerary for the trip to {destination}.",
    backstory=(
        "A meticulous planner who excels at crafting day-by-day travel plans, "
        "including activities, timings, and transportation options, tailored to user preferences."
    ),
    llm = my_llm,
    verbose=True,
    allow_delegation=False
)

hotel_restaurant_finder_agent = Agent(
    role='Accommodation and Dining Expert',
    goal=f"Find the best hotels and restaurants in {destination} based on user preferences.",
    backstory=(
        "A seasoned concierge who knows the best places to stay and eat. They prioritize "
        "high ratings, proximity to attractions, and alignment with the user's budget and theme."
    ),
    llm = my_llm,
    tools=[search_tool],
    verbose=True,
    allow_delegation=False
)

# Define the tasks
research_task = Task(
    description=(
        f"1. Search for popular attractions, landmarks, and must-visit places in {destination}.\n"
        f"2. Research activities that match the traveler's interests: {activity_preferences}.\n"
        f"3. Find information on the local climate and culture.\n"
        f"4. Provide a well-structured summary of the findings.\n"
        f"Ensure the information is relevant for a {travel_theme.lower()} trip."
    ),
    agent=researcher_agent,
    expected_output=(
        f"A detailed markdown report with sections for 'Top Attractions', 'Local Activities', "
        f"'Climate & Culture', and 'Safety Tips' for {destination}. The output should be "
        f"easy to read and directly usable for itinerary planning."
    )
)

hotel_restaurant_task = Task(
    description=(
        f"1. Identify the top-rated hotels in {destination} that match the user's preferences: "
        f"Budget: {budget}, Hotel Rating: {hotel_rating}.\n"
        f"2. Find highly-rated restaurants near the main attractions, considering the traveler's theme: "
        f"{travel_theme}.\n"
        f"3. Provide a list of options for both, including ratings and a brief description."
    ),
    agent=hotel_restaurant_finder_agent,
    expected_output=(
        f"A list of 3-5 top hotel recommendations and 3-5 top restaurant recommendations for {destination}. "
        f"Each recommendation should include the name, star rating, a brief description, and its approximate location."
    )
)

planning_task = Task(
    description=(
        f"Create a detailed, day-by-day itinerary for a {num_days}-day trip to {destination}. "
        f"The plan should incorporate the research findings from the 'Travel Researcher' and the hotel/restaurant "
        f"recommendations from the 'Accommodation and Dining Expert'.\n"
        f"Consider the traveler's preferences: Theme: {travel_theme}, Activities: {activity_preferences}, "
        f"Budget: {budget}.\n"
        f"The itinerary should include scheduled activities, estimated travel times, and suggestions for meals."
    ),
    agent=planner_agent,
    expected_output=(
        f"A complete, structured travel itinerary for a {num_days}-day trip to {destination}. "
        f"The output should be formatted clearly with headings for each day, listing morning, "
        f"afternoon, and evening activities, and incorporating flight details and hotel/restaurant suggestions."
    )
)

# --- Streamlit Execution Logic ---
if st.button("🚀 Generate Travel Plan"):
    # Flight fetching (remains the same)
    with st.spinner("✈️ Fetching best flight options..."):
        flight_data = fetch_flights(source, destination, departure_date, return_date)
        cheapest_flights = extract_cheapest_flights(flight_data)

    # Initialize the Crew
    # The crew will execute tasks in the order provided.
    project_crew = Crew(
        agents=[researcher_agent, hotel_restaurant_finder_agent, planner_agent],
        tasks=[research_task, hotel_restaurant_task, planning_task],
        verbose=True, # You can change this to 1 or 0 for less output
        process=Process.sequential # Executes tasks one after the other
    )

    # Start the crew's work
    with st.spinner("✨ Creating your personalized travel plan with AI..."):
        # The kick-off method will run all tasks and return the final result of the last task (the itinerary).
        crew_result = project_crew.kickoff()
        itinerary_output = crew_result

    # Display Results
    st.subheader("✈️ Cheapest Flight Options")
    if cheapest_flights:
        cols = st.columns(len(cheapest_flights))
        for idx, flight in enumerate(cheapest_flights):
            with cols[idx]:
                airline_logo = flight.get("airline_logo", "")
                airline_name = flight.get("airline", "Unknown Airline")
                price = flight.get("price", "Not Available")
                total_duration = flight.get("total_duration", "N/A")
                
                flights_info = flight.get("flights", [{}])
                departure = flights_info[0].get("departure_airport", {})
                arrival = flights_info[-1].get("arrival_airport", {})
                airline_name = flights_info[0].get("airline", "Unknown Airline")
                
                departure_time = format_datetime(departure.get("time", "N/A"))
                arrival_time = format_datetime(arrival.get("time", "N/A"))
                
                booking_link = "#" # Placeholder for booking link logic

                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid #ddd; 
                        border-radius: 10px; 
                        padding: 15px; 
                        text-align: center;
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                        background-color: #f9f9f9;
                        margin-bottom: 20px;
                    ">
                        <img src="{airline_logo}" width="100" alt="Flight Logo" />
                        <h3 style="margin: 10px 0;">{airline_name}</h3>
                        <p><strong>Departure:</strong> {departure_time}</p>
                        <p><strong>Arrival:</strong> {arrival_time}</p>
                        <p><strong>Duration:</strong> {total_duration} min</p>
                        <h2 style="color: #008000;">💰 {price}</h2>
                        <a href="{booking_link}" target="_blank" style="
                            display: inline-block;
                            padding: 10px 20px;
                            font-size: 16px;
                            font-weight: bold;
                            color: #fff;
                            background-color: #007bff;
                            text-decoration: none;
                            border-radius: 5px;
                            margin-top: 10px;
                        ">🔗 Book Now</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("⚠️ No flight data available.")

    st.subheader("🗺️ Your Personalized Itinerary")
    # CrewAI's kickoff returns the final output directly
    st.write(itinerary_output)

    st.success("✅ Travel plan generated successfully!")
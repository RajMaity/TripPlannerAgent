# Trip Planner Agent
LLM powered trip planner with multiple agents. (Crew AI, SerpAPI, Gemini, Streamlit, Python)

# Trip Planner Agent

This is a powerful Trip Planner Agent application built to help you plan your perfect trip. It uses a multi-agent system powered by CrewAI to research destinations, plan itineraries, and find hotels and restaurants, all based on your specific inputs.

## Features

  - **Intelligent Trip Planning:** The application leverages advanced Large Language Models (LLMs) to generate detailed and personalized trip itineraries.
  - **Dynamic Research:** A dedicated researcher agent browses the web to gather up-to-date information on destinations, attractions, and activities.
  - **Flight and Hotel Comparisons:** The planner agent can compare flight tickets and assist in finding suitable accommodations and dining options.
  - **User-Friendly Interface:** The application features a simple and intuitive frontend built with Streamlit, making it easy to interact with the agents.

## How it Works

The system is powered by a crew of three specialized agents, each with a specific role:

  - **Researcher Agent:** This agent is responsible for searching the web for information about the requested destination, including things to do, local events, and travel tips. It uses **SerperAPI** and **SerpApi** for its web search capabilities.
  - **Planner Agent:** This agent takes the research findings and your specific preferences to create a comprehensive trip itinerary. It can also compare flight options and suggest a schedule.
  - **Hotels and Restaurants Agent:** This agent focuses on finding and recommending hotels and restaurants that fit your budget and taste, ensuring a comfortable and enjoyable stay.

The agents collaborate seamlessly to provide you with a well-rounded and customized trip plan.

## Technologies Used

  - **CrewAI:** The framework used to orchestrate the multi-agent system.
  - **Gemini 2.5 Flash/Pro:** The powerful LLM powering the agents' intelligence.
  - **Streamlit:** The web framework used to create the interactive frontend.
  - **SerpApi & SerperAPI:** APIs used by the agents to perform web searches and gather real-time data.

## Getting Started

Follow these steps to set up and run the application on your local machine.

### Prerequisites

  - **Python 3.8+**
  - **Git**

### Step 1: Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### Step 2: Set up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### Step 3: Install Required Packages

Install all the necessary Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Obtain API Keys

The application requires API keys for the LLM and web search services. You need to create accounts and get your keys from the following services:

  - **Google Gemini API:** Visit the [Google AI Studio](https://aistudio.google.com/) to get your `GEMINI_API_KEY`.
  - **SerpApi:** Sign up on the [SerpApi website](https://serpapi.com/) to get your `SERPAPI_API_KEY`.
  - **SerperAPI:** Register on the [SerperAPI website](https://www.google.com/search?q=https://serperapi.com/) to get your `SERPER_API_KEY`.

Once you have your keys, create a `.env` file in the root directory of the project and add your keys as follows:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
SERPAPI_API_KEY="YOUR_SERPAPI_API_KEY"
SERPER_API_KEY="YOUR_SERPER_API_KEY"
```

### Step 5: Run the Application

Finally, run the Streamlit application using the following command:

```bash
streamlit run app.py
```

This will start a local web server and open the application in your default browser.

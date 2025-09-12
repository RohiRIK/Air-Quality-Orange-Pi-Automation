import os
from src.models.sensor_data import SensorData
from src.models.ai_recommendation import AIRecommendation
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class AIService:
    def __init__(self):
        # Initialize GoogleGenerativeAI with API key from environment variable
        # Ensure GOOGLE_API_KEY is set in your environment or .env file
        self.llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.7)

        # Define a prompt template for air quality recommendations
        self.prompt_template = PromptTemplate(
            input_variables=["temperature", "pressure", "humidity"],
            template=(
                "Given the following air quality data:\n"
                "Temperature: {temperature}°C\n"
                "Pressure: {pressure} hPa\n"
                "Humidity: {humidity}%\n\n"
                "Provide a concise recommendation (1-2 sentences) for improving or maintaining indoor air quality. "
                "Focus on actionable advice relevant to these parameters."
            )
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def generate_recommendation(self, sensor_data: SensorData) -> AIRecommendation:
        # Use the LangChain to generate a recommendation
        response = self.chain.run(
            temperature=sensor_data.temperature,
            pressure=sensor_data.pressure,
            humidity=sensor_data.humidity
        )
        return AIRecommendation(recommendation_text=response.strip())

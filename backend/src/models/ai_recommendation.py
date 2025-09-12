from pydantic import BaseModel

class AIRecommendation(BaseModel):
    recommendation_text: str

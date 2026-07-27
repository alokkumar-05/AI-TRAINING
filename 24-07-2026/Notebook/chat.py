from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
import os
os.environ["GROQ_API_KEY"] =os.getenv("GROQ_API_KEY")

model = init_chat_model(
    "llama-3.3-70b-versatile",
    model_provider="groq"
)

txt ="HEY"
 
response = model.invoke(txt)

print(response.content)

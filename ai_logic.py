'''
-----------------USEFUL LINKS -----------------

Hugging Face Model Page: https://huggingface.co/models?pipeline_tag=any-to-any&sort=trending

1. Pick model
        ↓
2. Open model page
        ↓
3. Check "Use this model"
        ↓
4. Check provider availability (look for inference providers, this will work with the API)
        ↓
5. Copy the example
        ↓
6. Modify only the prompt

'''

#-----------------------------------------------
# IMPORTS
#-----------------------------------------------

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


#-----------------------------------------------
# API KEY SETUP
#-----------------------------------------------

# Load .env file
load_dotenv()

api_key = os.getenv("API_KEY")

# Check if API key exists
if not api_key:
    raise ValueError(
        "API_KEY not found. Make sure your .env file exists and contains API_KEY=your_token"
    )


#-----------------------------------------------
# INITIALIZE HUGGING FACE CLIENT
#-----------------------------------------------

client = InferenceClient(
    token=api_key
)


#-----------------------------------------------
# CHAT FUNCTION
#-----------------------------------------------

def chat_with_ai(prompt):

    response = client.chat_completion(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response.choices[0].message.content

    return output
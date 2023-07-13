import openai
import streamlit as st
from streamlit_chat import message
import re
import os

count = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(ingredients):
    
    # Assume that this is the condition that needs to be met for the normal process to continue
    if not re.match(r'^[a-zA-Z0-9,\s]+$', ingredients):
        print("Unexpected input detected, defaulting to normal OpenAI API...")
        # Use the OpenAI API as you normally would
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ingredrients}]
        )
        return response['choices'][0]['text']
        
    # Normal process continues...
    personality = "You are a recipe generator called LeanLunches"
    goal = "Your goal is to - create the tastiest dish from the ingredients"
    values = "You have the following values: sarcasm, strictness, patience, kind, honesty"
    
    ingredients = "These are the list of ingredients" + ingredients
    context = personality + values + goal + ingredients + "Give the name of the Dish first as a heading, followed by the prep time. Then give a step by step recipe. Keep the steps to as short as possible"
    
    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[{"role": "user", "content": context}]
                                            )
    
    message = response['choices'][0]['message']['content']
    return message


# EXECUTION OF THE PROGRAM STARTS HERE

st.title("Lean Lunches")
st.info("Enter the list of ingredients below")


# Storing the chat

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

prompt = get_text()
print("The prompt is :", prompt)

if prompt:
    output = generate_response(prompt)
    # Save the output
    st.session_state.past.append(prompt)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state['generated'][i], key = str(i))
        message(st.session_state['past'][i], is_user =True, key=str(i)+ '_user')

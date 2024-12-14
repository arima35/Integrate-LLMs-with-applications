# author: Elena Lowery
# This code demonstrates how to invoke LLMs (Large Language Models) deployed in watsonx.ai.
# Make sure to provide your IBM Cloud API key and watsonx.ai project ID.

# Install the required libraries:
# pip install ibm-watson-machine-learning
# pip install streamlit
# pip install python-dotenv

import os
from dotenv import load_dotenv
import streamlit as st
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# Load environment variables from .env file
load_dotenv()

# Get the API key and project ID from the environment variables
api_key = os.getenv("API_KEY")
watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")

# URL for Watson API
url = "https://us-south.ml.cloud.ibm.com"

# Function to get the model with specified parameters
def get_model(model_type, max_tokens, min_tokens, decoding, stop_sequences):
    generate_params = {
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: min_tokens,
        GenParams.DECODING_METHOD: decoding,
        GenParams.STOP_SEQUENCES: stop_sequences
    }

    model = Model(
        model_id=model_type,
        params=generate_params,
        credentials={
            "apikey": api_key,
            "url": url
        },
        project_id=watsonx_project_id
    )

    return model

# Function to prepare the prompt for the model
def get_prompt(question):
    # Defining a pattern for prompt generation
    instruction = "Answer this question briefly."
    examples = "\n\nQuestion: What is the capital of Germany\nAnswer: Berlin\n\nQuestion: What year was George Washington born?\nAnswer: 1732\n\nQuestion: What are the main micro nutrients in food?\nAnswer: Protein, carbohydrates, and fat\n\nQuestion: What language is spoken in Brazil?\nAnswer: Portuguese \n\nQuestion: "
    your_prompt = question
    end_prompt = "Answer:"

    final_prompt = instruction + examples + your_prompt + end_prompt
    return final_prompt

# Main function for answering questions
def answer_questions():
    # Web app UI - title and input box for the question
    st.title('🌠Test watsonx.ai LLM')
    user_question = st.text_input('Ask a question, for example: What is IBM?')

    # Default question if no input is provided
    if len(user_question.strip()) == 0:
        user_question = "What is IBM?"

    # Get the prompt for the input question
    final_prompt = get_prompt(user_question)

    # Model parameters
    model_type = ModelTypes.FLAN_UL2  # You can use any available model here
    max_tokens = 100
    min_tokens = 20
    decoding = DecodingMethods.GREEDY
    stop_sequences = ['.']

    # Fetch the model with specified parameters
    model = get_model(model_type, max_tokens, min_tokens, decoding, stop_sequences)

    try:
        # Generate response from the model
        generated_response = model.generate(prompt=final_prompt)
        model_output = generated_response['results'][0]['generated_text']
        
        # Displaying the answer in Streamlit
        formatted_output = f"""
            **Answer to your question:** {user_question} \
            *{model_output}*</i>
        """
        st.markdown(formatted_output, unsafe_allow_html=True)

    except Exception as e:
        # Handle any error while generating the response
        st.error(f"Error occurred: {str(e)}")
        print(f"Error occurred: {str(e)}")

# Invoke the main function
if __name__ == "__main__":
    answer_questions()

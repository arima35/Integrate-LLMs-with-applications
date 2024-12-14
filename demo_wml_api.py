import os
import requests
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import IAMTokenManager

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mendapatkan variabel lingkungan
api_key = os.getenv("API_KEY")
watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")
url = "https://us-south.ml.cloud.ibm.com"

if not api_key or not watsonx_project_id:
    raise ValueError("API_KEY atau WATSONX_PROJECT_ID tidak ditemukan di file .env")

# Fungsi untuk mendapatkan model dengan parameter spesifik
def get_model(model_type, max_tokens, min_tokens, decoding, temperature):
    try:
        generate_params = {
            GenParams.MAX_NEW_TOKENS: max_tokens,
            GenParams.MIN_NEW_TOKENS: min_tokens,
            GenParams.DECODING_METHOD: decoding,
            GenParams.TEMPERATURE: temperature,
        }

        model = Model(
            model_id=model_type,
            params=generate_params,
            credentials={
                "apikey": api_key,
                "url": url,
            },
            project_id=watsonx_project_id,
        )

        return model
    except Exception as e:
        print(f"Error saat membuat model: {e}")
        return None

# Fungsi untuk menghasilkan respons dari customer complaints
def get_list_of_complaints():
    model_type = ModelTypes.LLAMA_2_13B_CHAT
    max_tokens = 100
    min_tokens = 50
    decoding = DecodingMethods.GREEDY
    temperature = 0.7

    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    if not model:
        print("Gagal membuat model. Periksa API Key dan project ID.")
        return

    complaint = """
    I just tried to book a flight on your incredibly slow website. All the times 
    and prices were confusing. I liked being able to compare the amenities in economy 
    with business class side by side. But I never got to reserve a seat because I didn't 
    understand the seat map. Next time, I'll use a travel agent!
    """

    prompt = f"""
    From the following customer complaint, extract 3 factors that caused the customer to be unhappy. 
    Put each factor on a new line. 

    Customer complaint: {complaint}

    Numbered list of all the factors that caused the customer to be unhappy:
    """

    try:
        response = model.generate(prompt=prompt)
        print("Prompt:", prompt)
        print("Response:", response['results'][0]['generated_text'])
    except Exception as e:
        print(f"Error saat memanggil API: {e}")

# Fungsi untuk menjawab pertanyaan umum
def answer_questions():
    model_type = ModelTypes.FLAN_UL2
    max_tokens = 300
    min_tokens = 50
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    if not model:
        print("Gagal membuat model. Periksa API Key dan project ID.")
        return

    prompt = "Write a paragraph about the capital of France."

    try:
        response = model.generate(prompt=prompt)
        print("Prompt:", prompt)
        print("Response:", response['results'][0]['generated_text'])
    except Exception as e:
        print(f"Error saat memanggil API: {e}")

# Fungsi untuk memanggil API menggunakan REST
def invoke_with_REST():
    authenticator = IAMAuthenticator(api_key)
    iam_token_manager = IAMTokenManager(apikey=api_key)
    try:
        access_token = iam_token_manager.get_token()
    except Exception as e:
        print(f"Error mendapatkan token: {e}")
        return

    rest_url = f"{url}/ml/v1-beta/generation/text?version=2023-05-29"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "project_id": watsonx_project_id,
        "model_id": "llama-2-13b-chat",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 100,
        },
        "input": [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "What are the three biggest factors affecting climate change?",
            },
        ],
    }

    try:
        response = requests.post(rest_url, headers=headers, json=payload)
        response.raise_for_status()
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil REST API: {e}")

# Eksekusi fungsi sesuai kebutuhan
if __name__ == "__main__":
    print("=== Memulai Proses ===")
    get_list_of_complaints()
    answer_questions()
    invoke_with_REST()

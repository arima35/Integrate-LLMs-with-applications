import requests

# API key yang kamu miliki
api_key = "xXN5lbdmRQXjuzg-82iZ9IMg8iCBZc25G-1yj00kI0ZL"

# URL endpoint untuk mendapatkan token
url = "https://iam.cloud.ibm.com/identity/token"

# Data yang dikirim dalam request
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": api_key
}

# Header yang diperlukan
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Permintaan POST untuk mendapatkan token
response = requests.post(url, data=data, headers=headers)

# Memeriksa apakah permintaan berhasil
if response.status_code == 200:
    # Mengambil bearer token dari response JSON
    bearer_token = response.json().get("access_token")
    print("Bearer Token:", bearer_token)
else:
    print("Gagal mendapatkan bearer token:", response.text)

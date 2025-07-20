import os
import requests
import json

# Mendapatkan API Key dan Domain dari environment variables (diatur oleh GitHub Secrets)
API_KEY = os.getenv('DNS_EXIT_API_KEY')
DOMAIN = os.getenv('DOMAIN_TO_RENEW') # Akan diatur di workflow YAML

API_URL = "https://api.dnsexit.com/dns/lse.jsp"

payload = {
    "apikey": API_KEY,
    "domain": DOMAIN, # PASTIKAN INI ADALAH DOMAIN KAMU YANG BENAR: cerita.mywp.info
    "action": "renew",
    "verbose": "true"
}

headers = {
    "Content-Type": "application/json"
}

try:
    print(f"Mencoba memperbarui SSL untuk {DOMAIN}...")
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status() # Akan memicu error untuk respons 4xx atau 5xx

    result = response.json()
    print("Respons API:")
    print(json.dumps(result, indent=2))

    if result.get("code") == "0": # Perhatikan "0" mungkin string
        print(f"SSL untuk {DOMAIN} berhasil diperbarui!")
    else:
        print(f"Perpanjangan SSL untuk {DOMAIN} gagal. Kode: {result.get('code')}, Pesan: {result.get('message')}")

except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan selama permintaan API: {e}")
except json.JSONDecodeError:
    print(f"Gagal mendekode JSON dari respons: {response.text}")
except Exception as e:
    print(f"Terjadi kesalahan tak terduga: {e}")

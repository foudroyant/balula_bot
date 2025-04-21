import datetime
import requests
import time
import hmac
import hashlib
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("API_KEY_BINANCE")
api_secret = os.getenv("SECRET_BINANCE")


# Convertir les dates en millisecondes
start_time = int(datetime.datetime.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
end_time = int(datetime.datetime.strptime("2024-03-01 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

# Endpoint pour les dépôts
url = 'https://api.binance.com/sapi/v1/capital/deposit/hisrec'
# RETRAITS : sapi/v1/capital/withdraw/history


# En-têtes de la requête
headers = {
    'X-MBX-APIKEY': api_key
}

def check_pay(transaction) :

    # Paramètres de la requête
    params = {
        'timestamp': int(time.time() * 1000),
        #'startTime': start_time,  # Date de début
        #'endTime': end_time,  # Date de fin
    }

    # Créer la signature
    query_string = urllib.parse.urlencode(params)
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature
    
    # Faire la requête
    response = requests.get(url, headers=headers, params=params)

    # Afficher la réponse
    if response.status_code == 200:
        deposits = response.json()
        for deposit in deposits:
            if transaction == deposit['txId'] :
                return {
                    'prix' : float(deposit['amount']),
                    'reseau' : deposit['network'],
                    'statut' : deposit['status'],
                    'txID' : deposit['txId'],
                    'coin' : deposit['coin'],
                }
        return None
    else:
        print("Erreur :", response.status_code, response.text)
        return None
    
#depot = check_pay('49d7f4ab0973cd9c8c2d0b91c46b7fe7eb1e3b8573ce285ef23636fcc7026468')
#print(depot)
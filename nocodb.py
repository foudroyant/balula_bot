import datetime
import requests
from dotenv import load_dotenv
import os


load_dotenv(encoding='utf-8')

NOCO_DB_KEY = os.getenv("NOCODB_KEY")
USERS_TABLE = os.getenv("USERS_TABLE")
ABONNEMENTS_TABLE = os.getenv("ABONNEMENTS_TABLE")


def url(ID_TABLE):
    return f"https://app.nocodb.com/api/v2/tables/{ID_TABLE}/records"

querystring = {"offset":"0","limit":"25","where":"","viewId":"vw2j7hbmuz7h4ph7"}

headers = {"xc-token": NOCO_DB_KEY}

def getUsers():
    response = requests.request("GET", url(USERS_TABLE), headers=headers, params=querystring)
    #print(response.text)
    return response

def addUser(userId, link, fullname, username):
    # Exemple de données que tu souhaites envoyer
    data = {
        "userID" : userId,
        "link" : link,
        "username" : username,
        "fullname" : fullname,
        "type" : "FREE"
    }
    
    # Envoi de la requête POST avec le body JSON
    try:
        response = requests.post(url(USERS_TABLE), headers=headers, json=data)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            print("Données envoyées avec succès :")
            return response.json()  # Retourne la réponse JSON
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return None
    
def get_one_user(userID):
    for item in getUsers().json()["list"]:
        if item.get("userID") == userID:
            return item
    return None
        

def s_abonner(userID, sessionID) :
    data = {
        "userID" : userID,
        "sessionID" : sessionID,
        "status" : "active",
    }

    subscribe = get_one_abonnement(sessionID)
    if subscribe != None :
        try:
            response = requests.post(url(ABONNEMENTS_TABLE), headers=headers, json=data)
            
            # Vérifier si la requête a réussi
            if response.status_code == 200:
                print("Données envoyées avec succès :")
                _user = get_one_user(str(userID))
                update = update_user(_user["Id"])
                if update :
                    return response.json()  # Retourne la réponse JSON
                else : 
                    print(f"Erreur {response.status_code}: {response.text}")
                    return None
            else:
                print(f"Erreur {response.status_code}: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête : {e}")
            return None
    
    else : 
        return None
    
def all_abonnements():
    response = requests.request("GET", url(ABONNEMENTS_TABLE), headers=headers)
    
    if len(response.json()["list"]) == 0 or response.status_code != 200:
        return None
    
    try:
        return response.json()
    except ValueError:
        return None

def get_one_abonnement(sessionID):
    all_abonnements_data = all_abonnements()
    
    if all_abonnements_data is None or all_abonnements_data.get("status_code", 200) != 200:
        return None
    
    for item in all_abonnements_data.get("list", []):
        if item.get("sessionID") == str(sessionID):
            return item
        
    return None


# 🔹 Fonction pour mettre à jour un enregistrement
def update_user(record_id):
    url = f"https://app.nocodb.com/api/v2/tables/{USERS_TABLE}/records/"

    try:
        response = requests.patch(url, json=[{'Id' : record_id, 'type' : 'PRO', "credits" : 500, "updatepro" : datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")}], headers=headers)

        if response.status_code == 200:
            print("✅ Mise à jour réussie !")
            return response.json()
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête : {e}")
        return None

def update_credits(record_id, credits : int):
    url = f"https://app.nocodb.com/api/v2/tables/{USERS_TABLE}/records/"

    try:
        response = requests.patch(url, json=[{'Id' : record_id, 'credits' : credits, "updatepro" : datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")}], headers=headers)

        if response.status_code == 200:
            print("✅ Mise à jour réussie !")
            return response.json()
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête : {e}")
        return None
    
#print(get_one_abonnement("49d7f4ab0973cd9c8c2d0b91c46b7fe7eb1e3b8573ce285ef23636fcc7026468"))
#print(update_credits(1, 8))
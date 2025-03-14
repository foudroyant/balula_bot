from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging

from binance import check_pay
from nocodb import addUser, get_one_user, getUsers, s_abonner, update_credits

from ocr import get_ocr_text
from remove_bg import transparent
from transcribe import transcription

# Charger les variables d'environnement
load_dotenv(encoding='utf-8')
TOKEN_BOT = os.getenv("TOKEN_BOT")
HOST = os.getenv("HOST")

work = 0  # RIEN A FAIRE
lang = "fr"

SUCCESS_URL = os.getenv("SUCCESS_URL")
CANCEL_URL = os.getenv("CANCEL_URL")


MESSAGE_INFO = '''# 🤖 Balula - Votre Assistant de Saisie Intelligent 🚀   

### 🚀 **Fonctionnalités de Balula**  
✅ **Transcription audio** : Convertissez vos messages vocaux en texte en quelques secondes.  
🖼️ **Extraction de texte depuis des images** : Utilisez la technologie OCR pour extraire du texte à partir de photos.

### 💡 Évolutif et Amélioré en Continu !  
Nous ajoutons régulièrement de nouvelles fonctionnalités pour rendre **Balula** encore plus puissant.  

## 🎁 Version Gratuite  
🔹 Effectue toutes les opérations, mais avec quelques **limitations**.  

## 💎 Plan PRO – Seulement **10 € pour 3 mois** !  
🚀 **Profitez sans limites** de toutes les fonctionnalités de Balula :  
✔️ Transcriptions illimitées  
✔️ Extraction de texte illimitée   

---

### 🖼️ **Extraction de Texte depuis une Image**  
Envoyez une image (screenshot, scan de document, photo, etc.), et **Balula** en extraira le texte.  
**Utilités :**  
- **Professionnels** : Extrayez du texte à partir de factures, de contrats ou de documents scannés.  
- **Étudiants** : Numérisez des livres ou des notes manuscrites.  
- **Archivage** : Convertissez des documents papier en fichiers texte numériques.  

---

### 💳 **Modes de Paiement**  
Le paiement principal se fait par **cryptomonnaie** (Binance Pay ou TRON TRC-20).  
Si vous préférez un autre mode de paiement (comme **Mobile Money**), contactez notre service client à 📧 [contact@bambyno.com](mailto:contact@bambyno.com).  

### 📢 Restez connectés !  
Des mises à jour et de nouvelles fonctionnalités arrivent bientôt. Essayez **Balula** dès maintenant !  
'''

MESSAGE_AIDE = '''# 📚 Aide - Balula 🤖

Bienvenue dans le menu d'aide de **Balula** ! Voici un guide complet pour utiliser toutes les fonctionnalités du bot :

---

### 🎉 **Commandes Disponibles**  

🔹 **`/start`**  
- Démarrer ou redémarrer le bot.  
- Vous serez invité à **choisir une langue** (le français est la langue par défaut).  
- Une fois la langue sélectionnée, vous pouvez :  
  - Envoyer un **message vocal** pour le transcrire en texte.  
  - Envoyer une **image** (screenshot, scan de document, etc.) pour en extraire le texte.  

🔹 **`/help`**  
- Affiche ce menu d'aide pour vous guider dans l'utilisation du bot.  

🔹 **`/info`**  
- Obtenez des informations sur **Balula**, ses fonctionnalités et les dernières nouveautés (news).  

🔹 **`/me`**  
- Accédez aux aux informations de votre compte, y compris le nombre de crédits restants et l'état de votre abonnement. 

🔹 **`/pay`**  
- Accédez aux instructions pour passer au **Plan PRO** et profiter de toutes les fonctionnalités sans limites.  

---

### 🌍 **Choix de la Langue**  
Après la commande `/start`, vous pouvez choisir une langue pour les transcriptions audio.  
- Si aucune langue n'est sélectionnée, le **français** sera utilisé par défaut.  
- Balula prend en charge de nombreuses langues pour répondre à vos besoins.  

---

### 🎙️ **Transcription Audio**  
Envoyez un message vocal, et **Balula** le transcrira en texte en quelques secondes.  
**Utilités :**  
- **Secrétariats** : Transcrivez rapidement des réunions, des notes vocales ou des instructions.  
- **Journalistes** : Transformez des interviews ou des reportages audio en texte pour vos articles.  
- **Étudiants** : Convertissez des cours enregistrés en notes écrites.  

---

### 💳 **Modes de Paiement**  
Le paiement principal se fait par **cryptomonnaie** (Binance Pay ou TRON TRC-20).  
Si vous préférez un autre mode de paiement (comme **Mobile Money**), contactez notre service client à 📧 [contact@bambyno.com](mailto:contact@bambyno.com).  

---

### 🌐 **Notre Site Web**  
Pour plus d'informations, visitez notre site internet ➡️ [bambyno.com](https://www.bambyno.com)  

---

### 📢 **Besoin d'Aide Supplémentaire ?**  
Si vous avez des questions ou des problèmes, n'hésitez pas à :  
1. Utiliser la commande **`/help`** pour consulter ce guide.  
2. Contacter notre service client à 📧 [contact@bambyno.com](mailto:contact@bambyno.com).  

Nous sommes là pour vous aider ! 😊    
'''


ID_BINANCE ='743559475'
TRX = "TMJ1g8PjfrrPCrkDdn9jHuwkhR1nzwnrAg"
MESSAGE_PAYEMENT_CRYPTO = f"""
💳 **Paiement via Binance ou autre plateforme de cryptomonnaie via le réseau TRON (TRC-20)** 💳

Pour accéder à toutes les fonctionnalités de l'application, veuillez effectuer un paiement de **USDT pour 3 mois**.

Voici les informations de paiement :

🔹 **Binance ID** : `{ID_BINANCE}`
🔹 **Adresse TRX (TRC-20)** : `{TRX}`

⚠️ **Attention** :
- Assurez-vous de sélectionner le réseau **TRC-20** lors de l'envoi.
- Vérifiez bien l'adresse avant de confirmer la transaction.

📤 **Après le dépôt** :
Une fois la transaction effectuée, veuillez envoyer le **TxID** de la transaction ici pour valider votre paiement.

Merci pour votre confiance ! 😊
"""

DEJA_PRO ="""🎉 **Félicitations !**  

Vous êtes déjà abonné au **Plan PRO** de Balula. 🚀  

Avec votre abonnement, vous bénéficiez de :  
✅ **Transcriptions audio illimitées**  
✅ **Extraction de texte depuis des images** 

---

### 🛠️ **Rencontrez-vous un problème ?**  
Si votre abonnement ne fonctionne pas correctement ou si vous avez des questions, voici ce que vous pouvez faire :  

1. **Redémarrez le bot** en utilisant la commande `/start`.  
2. Si le problème persiste, contactez notre **service client** à 📧 [contact@bambyno.com](mailto:contact@bambyno.com).  
   - N'oubliez pas de nous fournir des détails sur le problème rencontré.  

---

### 🌐 **Besoin d'Aide Supplémentaire ?**  
Visitez notre site web pour plus d'informations : ➡️ [bambyno.com](https://www.bambyno.com)  

Nous sommes là pour vous aider ! 😊  """

def MESSAGE_GROS_FILE(msg_size=""):
    return f"""⚠️ **Limite de Taille des Fichiers & fonctionnalités - Version FREE**  

Vous utilisez actuellement la **version FREE** de Balula. Avec cette version, vous pouvez envoyer des fichiers jusqu'à **1 Mo maximum**.  

🔹 **Taille maximale autorisée** : 1 Mo  
{msg_size}
🔹 **Votre message vocal ne doit pas dépasser **10 secondes** pour être traité.** 
🔹 **Impossible de retirer des background des images**
🔹 **Crédits maximal ** : 10

---

### 🚀 **Passez au Plan PRO pour Plus de Liberté !**  
Avec le **Plan PRO**, vous bénéficiez de :  
✅ **Taille de fichier illimitée**  
✅ **Transcriptions audio illimitées**  
✅ **Extraction de texte depuis des images** 

Pour passer au Plan PRO, utilisez la commande `/pay` ou contactez-nous à 📧 [contact@bambyno.com](mailto:contact@bambyno.com).  

---

### 🔄 **Vous pensez avoir déjà payé ?**  
Si vous estimez avoir déjà payé mais que vous rencontrez cette limitation :  
1. **Relancez la commande** `/start` pour actualiser votre statut.  
2. Si le problème persiste, contactez notre **service client** à 📧 [contact@bambyno.com](mailto:contact@bambyno.com) en fournissant les détails de votre paiement.  

---

### 🌐 **Besoin d'Aide ?**  
Visitez notre site web pour plus d'informations : ➡️ [bambyno.com](https://www.bambyno.com)  

Nous sommes là pour vous aider ! 😊  """


# Configurer le module logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_lng(lng):
    cases = {
        "fr": "Français",
        "en": "Anglais",
        "pt": "Portugais",
        "es": "Espagnol"
    }
    return cases.get(lng, "fr")

def get_user_infos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Récupère et affiche le numéro de téléphone de l'utilisateur"""
    contact = update.effective_user
    return {
        "user_id" : contact.id,
        "prenom" : contact.first_name,
        "nom" : contact.full_name,
        "username" : contact.username,
        "lang" : contact.language_code,
        "link" : contact.link
    }

# Fonction pour gérer la commande /start et afficher le menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    userID = user.id
    fullname = user.full_name
    username = user.username or "Inconnu"
    link = f"https://t.me/{username}" if username != "Inconnu" else "Aucun lien"
    langue = user.language_code

    _user = get_one_user(str(userID))
    if _user == None:
        addUser(userId=userID, fullname=fullname, link=link, username=username)
        await update.message.reply_text("Bienvenue ! Vous avez êtes desormais membre.")
    else:
        context.user_data['user'] = _user
        context.user_data['type_account'] = _user["type"]
    
    if 'lang' not in context.user_data:
        context.user_data['lang'] = langue  # Valeur par défaut

    keyboard = [
        [InlineKeyboardButton("Français", callback_data="fr"), InlineKeyboardButton("Espagnol", callback_data="es")],
        [InlineKeyboardButton("Anglais", callback_data="en"), InlineKeyboardButton("Portuguais", callback_data="pt")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(MESSAGE_AIDE, reply_markup=reply_markup, parse_mode="Markdown")

# Fonction pour gérer les interactions avec le menu
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if 'lang' not in context.user_data:
        context.user_data['lang'] = 'fr'  # Valeur par défaut    
    
    if query.data in ["fr", "es", "en", "pt"]:
        context.user_data['lang'] = query.data
        await query.edit_message_text(text=f"Langue sélectionnée : {show_lng(context.user_data['lang'])}")

    if query.data == "copy_binance_id":
        await query.edit_message_text(f"`{ID_BINANCE}`", parse_mode="Markdown")
    
    if query.data == "copy_trx_address":
        await query.edit_message_text(f"`{TRX}`", parse_mode="Markdown")

    if query.data == "confirm":
        # Traiter la confirmation
        await query.edit_message_text(f"✅ Transaction confirmée ! Nous allons vérifier le TxID `{context.user_data['txID']}` et activer votre accès.", parse_mode="Markdown")
        # Ici, vous pouvez ajouter la logique pour valider le TxID et activer l'accès
        pay = check_pay(context.user_data['txID'])
        if pay != None :
            print(pay)
            out = s_abonner(userID=update.effective_user.id, sessionID=context.user_data['txID'])
            if out is not None and pay['prix'] >=10 and pay["coin"] == 'USDT':
                # Si le paiement a réussi
                await query.edit_message_text(
                    "✅ Ce paiement a été effectué avec succès ! Merci pour votre achat.\n\n"
                    "Si votre abonnement n'est pas encore pris en compte, veuillez relancer la commande `/start` pour actualiser votre statut.\n\n"
                    "Pour toute question, n'hésitez pas à contacter notre service client à l'adresse suivante : **contact@bambyno.com**.",
                    parse_mode="Markdown"
                )
            else:
                # Si le paiement n'a pas abouti
                await query.edit_message_text(
                    "❌ Le paiement n'a pas abouti.\n\n"
                    "Si vous pensez qu'il s'agit d'une erreur (peut-être que le paiement n'est pas encore confirmé sur la blockchain ou inferieur à 10 USDT), veuillez contacter notre service client à l'adresse suivante : **contact@bambyno.com**.\n\n"
                    "Nous vous remercions de votre patience et nous ferons de notre mieux pour résoudre ce problème rapidement.",
                    parse_mode="Markdown"
                )
        else : 
            await query.edit_message_text(
                "❌ Aucun paiement correspondant à ce TxID n'a été trouvé.\n\n"
                "Si vous pensez qu'il s'agit d'une erreur, veuillez contacter notre service client à l'adresse suivante : **contact@bambyno.com**.\n\n"
                "Merci de nous fournir une capture d'écran de la transaction pour que nous puissions résoudre ce problème rapidement.\n\n"
                "Nous vous remercions de votre patience !",
                parse_mode="Markdown"
            )
        del context.user_data['txID']
        del context.user_data['moyen_pay']


    elif query.data == "cancel":
        # Annuler l'opération
        await query.edit_message_text("❌ Transaction annulée. Si vous avez besoin d'aide, n'hésitez pas à nous contacter.")
        # Supprimer le TxID stocké
        if 'txID' in context.user_data:
            del context.user_data['txID']
            del context.user_data['moyen_pay']

# Fonction pour gérer la commande /info
async def infos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try :
        with open("cover.jpg", 'rb') as image_file:
            await update.message.reply_photo(photo=image_file, caption=MESSAGE_INFO, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(MESSAGE_INFO, parse_mode='Markdown')


# Fonction pour gérer la commande /aide
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try :
        with open("cover.jpg", 'rb') as image_file:
            await update.message.reply_photo(photo=image_file, caption=MESSAGE_AIDE, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(MESSAGE_AIDE, parse_mode='Markdown')


async def Me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['user'] = get_one_user(str(update.effective_user.id))
    
    print(context.user_data['user'])
    INFO = f"""👤 **Informations de l'Utilisateur**  

    🔹 **Crédits disponibles** : {context.user_data['user']["credits"]}  
    🔹 **Type de compte** : {context.user_data['user']["type"]}  
    🔹 **Date de paiement** : {context.user_data['user']["updatepro"]} 

    ### 🚀 **Que pouvez-vous faire ensuite ?**  
    - Utilisez vos crédits pour transcrire des audios, extraire du texte d'images, ou supprimer des arrière-plans (en beta).  
    - Pour recharger vos crédits ou mettre à jour votre abonnement, utilisez la commande `/pay`.  

    Nous sommes là pour vous aider ! 😊  """ if context.user_data['user']["type"] == "PRO" else f"""👤 **Informations de l'Utilisateur**  

    🔹 **Crédits disponibles** : {context.user_data['user']["credits"]}  
    🔹 **Type de compte** : {context.user_data['user']["type"]}  

    Nous sommes là pour vous aider ! 😊  """
    await update.message.reply_text(INFO, parse_mode='Markdown')



# Fonction pour traiter les messages vocaux
async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_id = update.message.voice.file_id  # Récupérer l'ID du fichier vocal
    file = await context.bot.get_file(file_id)  # Obtenir l'URL du fichier
    
    duration = update.message.voice.duration  # Récupérer la durée du message vocal en secondes
    
    user = update.effective_user
    userID = user.id
    
    sent_message  = await update.message.reply_text("Veuillez patienter...")

    if 'user' not in context.user_data or 'credits' not in context.user_data:
        context.user_data['user'] = get_one_user(str(userID))  # Récupérer les données de l'utilisateur

    
    if  (context.user_data['user']["type"] == "FREE" and duration > 10 ) or context.user_data['user']["credits"] <= 0:
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)
        await update.message.reply_text(MESSAGE_GROS_FILE(),
            parse_mode="Markdown"
        )
    
    else :   
        if 'lang' not in context.user_data:
            context.user_data['lang'] = 'fr'  # Valeur par défaut

        texte = transcription(file.file_path, context.user_data['lang'])

        # Envoyer le texte transcrit
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)
        
        # Renvoyer l'audio avec la description
        await update.message.reply_audio(
            audio=file_id,  # ID du fichier audio
            caption=texte,  # Description de l'audio
            parse_mode="Markdown"
        )
        

    if int(context.user_data['user']["credits"]) > 0:
        update_credits(context.user_data['user']["Id"], int(context.user_data['user']["credits"]) - 1)
        context.user_data['user']["credits"] = int(context.user_data['user']["credits"]) - 1


# Fonction pour gérer les messages contenant des photos
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Récupérer le document envoyé
    photo = update.message.photo[-1]

    # Obtenir la taille du fichier (en octets)
    photo_size_bytes = photo.file_size

    # Convertir la taille en kilo-octets (Ko) ou méga-octets (Mo)
    photo_size_kb = photo_size_bytes / 1024  # Taille en Ko
    photo_size_mb = photo_size_kb / 1024     # Taille en Mo

    if 'user' not in context.user_data or 'credits' not in context.user_data:
        context.user_data['user'] = get_one_user(str(update.effective_user.id))  # Récupérer les données de l'utilisateur
    

    if photo_size_mb > 1 or context.user_data['user']["credits"] <= 0:
        await update.message.reply_text(MESSAGE_GROS_FILE(msg_size=f"🔹 **Taille de votre fichier** : {photo_size_mb} Mo"), parse_mode="Markdown")

    else : 
        photo_file = await update.message.photo[-1].get_file()
        file_path = f"downloads/{photo_file.file_id}.jpg"
        #await photo_file.download_to_drive(file_path)
        sent_message  = await update.message.reply_text("Veuillez patienter...")

        # Récupérer la légende de l'image
        caption = update.message.caption
        if caption and caption.lower() == "remove" :
            if 'user' not in context.user_data:
                context.user_data['user'] = get_one_user(str(update.effective_user.id))  # Récupérer les données de l'utilisateur
            
            if  context.user_data['user']["type"] == "FREE" :
                await update.message.reply_text(MESSAGE_GROS_FILE(), parse_mode="Markdown")
            else :
                transparent(photo_file.file_path, photo_file.file_id)
                #await update.message.reply_text(f"Légende reçue : {caption}")
                with open(photo_file.file_id + ".png", 'rb') as image_file:
                    # Supprimer le message envoyé
                    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)
                    await context.bot.send_photo(chat_id=update.message.chat_id, photo=image_file)
                    #await context.bot.send_document(chat_id=update.message.chat_id, document=image_file, caption="Voici votre image sans compréssion !")

        else:
            # Utiliser la fonction getTexte pour traiter l'image
            ocr_response = get_ocr_text(photo_file.file_path)

            # Extraire le texte de toutes les pages
            texte_complet = "\n\n".join(page['markdown'] for page in ocr_response['pages'])
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)
            if '![img-0.jpeg](img-0.jpeg)' in texte_complet :
                await update.message.reply_text(f"Difficile d'extraire le texte.")
            else : 
                await update.message.reply_photo(photo=photo_file.file_id, caption=f"{texte_complet}", parse_mode="Markdown")
    
    if int(context.user_data['user']["credits"]) > 0:
        update_credits(context.user_data['user']["Id"], int(context.user_data['user']["credits"]) - 1)
        context.user_data['user']["credits"] = int(context.user_data['user']["credits"]) - 1


# Fonction pour gérer les messages contenant des documents
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Récupérer le document envoyé
    document = update.message.document

    # Obtenir le nom du fichier
    file_name = document.file_name

    # Extraire l'extension du fichier
    file_extension = os.path.splitext(file_name)[1]  # Par exemple : ".pdf"

    # Obtenir la taille du fichier (en octets)
    file_size_bytes = document.file_size

    # Convertir la taille en kilo-octets (Ko) ou méga-octets (Mo)
    file_size_kb = file_size_bytes / 1024  # Taille en Ko
    file_size_mb = file_size_kb / 1024     # Taille en Mo

    if 'user' not in context.user_data or 'credits' not in context.user_data:
        context.user_data['user'] = get_one_user(str(update.effective_user.id))  # Récupérer les données de l'utilisateur

    if file_size_mb > 1 or context.user_data['user']["credits"] <= 0:
        await update.message.reply_text(MESSAGE_GROS_FILE(), parse_mode="Markdown")
    
    else :
        document_file = await update.message.document.get_file()
        file_path = f"downloads/{document_file.file_id}{file_extension}"
        #await document_file.download_to_drive(file_path)

        # Utiliser la fonction getTexte pour traiter l'image
        ocr_response = get_ocr_text(document_file.file_path)

        # Extraire le texte de toutes les pages
        texte_complet = "\n\n".join(page['markdown'] for page in ocr_response['pages'])
        await update.message.reply_text(f"{texte_complet}")
    
    
    if int(context.user_data['user']["credits"]) > 0:
        update_credits(context.user_data['user']["Id"], int(context.user_data['user']["credits"]) - 1)
        context.user_data['user']["credits"] = int(context.user_data['user']["credits"]) - 1


# Commande /pay pour démarrer le processus de paiement
'''async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Récupérer l'ID utilisateur Telegram
    
    if 'user' not in context.user_data:
        context.user_data['user'] = get_one_user(str(user_id))

    if context.user_data['user']['type'] == "FREE" :
        try:
            # Création de la session de paiement Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Balula PRO',
                        },
                        'unit_amount': 200,  # 2€
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{HOST}/success?userid={user_id}&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{HOST}/cancel",
            )

            # Envoie du lien de paiement à l'utilisateur
            await update.message.reply_text(
                f"🎉 **Félicitations !** Vous êtes à un clic de finaliser votre paiement. 🛍️\n\n"
                f"💳 Cliquez sur le lien ci-dessous pour sécuriser votre achat et profitez de notre offre exclusive ! 🚀\n\n"
                f"👉 [Procéder au paiement]({session.url})\n\n"
                f"✅ Paiement rapide et sécurisé avec Stripe. N'attendez plus, votre achat vous attend ! 💼💡",
                parse_mode='Markdown'
            )

        except Exception as e:
            await update.message.reply_text(f"Erreur lors de la création de la session de paiement: {str(e)}")
    else : 
        await update.message.reply_text(f"Vous êtes déjà abonné à notre service PRO !")
'''


async def pay_by_cripto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Récupérer l'ID utilisateur Telegram

    if 'user' not in context.user_data:
        context.user_data['user'] = get_one_user(str(user_id))
        
    if context.user_data['user']['type'] == "FREE" :
        context.user_data['moyen_pay'] = "Binance"
        keyboard = [
            [
                InlineKeyboardButton("📋 ID Binance", callback_data="copy_binance_id"),
                InlineKeyboardButton("📋 Adresse TRX", callback_data="copy_trx_address")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if 'user' not in context.user_data:
            context.user_data['user'] = get_one_user(str(user_id))
        # Envoyer le message en Markdown
        await update.message.reply_text(MESSAGE_PAYEMENT_CRYPTO, reply_markup=reply_markup, parse_mode="Markdown")
    else : 
        await update.message.reply_text(DEJA_PRO, parse_mode="Markdown")


# Gérer la réception du TxID
async def handle_txid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if 'user' not in context.user_data:
        context.user_data['user'] = get_one_user(str(update.effective_user.id))
        
    if context.user_data['user']['type'] == "FREE" :
        txid = update.message.text
        # Stocker le TxID temporairement
        context.user_data['txID'] = txid

        # Créer les boutons inline
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirmer", callback_data="confirm"),
                InlineKeyboardButton("❌ Annuler", callback_data="cancel")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Demander confirmation à l'utilisateur
        await update.message.reply_text(
            f"Vous avez envoyé le TxID suivant : `{txid}`. Voulez-vous confirmer cette transaction ?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else : await update.message.reply_text(DEJA_PRO, parse_mode="Markdown")
    
    
    
# Configuration du bot Telegram
app = ApplicationBuilder().token(TOKEN_BOT).build()

# Ajouter les handlers à l'application Telegram
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", infos))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("me", Me))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.Document.MimeType("image/jpeg"), handle_document))
app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))  # Gérer les messages vocaux
#app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("pay", pay_by_cripto))

# Gérer la réception du TxID
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_txid))

app.run_polling(poll_interval=5)

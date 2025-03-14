import os
import requests
from PIL import Image
from rembg import remove, new_session
import tempfile
#from rembg.session_factory import new_session

#print(new_session())


custom_model = "u2net_human_seg"
custom_model_path = "./models/BiRefNet-portrait-epoch_150.onnx"

def transparent(image_url, name):
    # Créer un fichier temporaire pour stocker l'image téléchargée
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file_name = temp_file.name

        # Télécharger l'image depuis l'URL et l'enregistrer dans le fichier temporaire
        response = requests.get(image_url)
        temp_file.write(response.content)

    try:
        # Ouvrir l'image à partir du fichier temporaire
        input_image = Image.open(temp_file_name)

        # Créer une session avec le modèle personnalisé
        session = new_session(model_name=custom_model_path)
        
        # Traiter l'image pour enlever l'arrière-plan
        output_image = remove(input_image, session=session)
        
        # Enregistrer l'image traitée avec le nom spécifié
        output_image.save(name + ".png")
    finally:
        # Supprimer le fichier temporaire
        #os.remove(temp_file_name)
        print(temp_file_name)


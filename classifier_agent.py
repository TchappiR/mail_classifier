import json
from config import client, model, temperature, response_format

def load_prompt(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {path} est introuvable.")
        print("Assure-toi qu'il est dans le même dossier que ce script.")
        exit(1)

# Chargement du prmpt
SYSTEM_PROMPT = load_prompt(path="/prompt.txt")

# Fonction principale de classification
def classify_ticket(email_content):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"Voici l'e-mail à classifier :\n\n{email_content}",
                }
            ],
            model=model, 
            temperature=temperature, 
            response_format=response_format
        )
        
        # Récupération et transformation de la réponse
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
        
    except Exception as e:
        return {"error": f"Une erreur est survenue avec l'API: {str(e)}"}

# 5. Test du script
if __name__ == "__main__":
    email_test = """
    Bonjour l'équipe,
    Depuis ce matin, je n'arrive plus à me connecter à mon espace extranet. 
    Le système m'indique "mot de passe incorrect" alors que je suis certain de ne pas m'être trompé. 
    C'est très urgent, je dois absolument valider les congés de mon équipe avant midi !
    Merci d'avance pour votre aide.
    Cordialement, Thomas.
    """
    
    print("🤖 Analyse de l'e-mail en cours via Groq...")
    resultat = classify_ticket(email_test)
    
    print("\n✅ Résultat obtenu :")
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
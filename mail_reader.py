import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

# Si tu modifies ces portées (SCOPES), supprime le fichier token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Montre comment s'authentifier à l'API Gmail et retourne le service."""
    creds = None
    # Le fichier token.json stocke les tokens d'accès et d'actualisation de l'utilisateur.
    # Il est créé automatiquement lors de la première exécution.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # Si les identifiants ne sont pas valides ou n'existent pas, on demande à l'utilisateur de se connecter.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Nécessite le fichier credentials.json téléchargé depuis Google Cloud
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Sauvegarde des identifiants pour la prochaine exécution
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Construit et retourne le service Gmail
    return build('gmail', 'v1', credentials=creds)

def fetch_all_tickets():
    """Récupère les e-mails et extrait le sujet et le contenu."""
    service = get_gmail_service()
    tickets = []


    # Requête pour lister les messages (tu peux ajouter un paramètre q="is:unread" par exemple)
    # On peut spécifier maxResults=549 pour coller à ton projet
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    if not messages:
        print('Aucun message trouvé.')
        return tickets

    print(f"{len(messages)} messages trouvés. Extraction en cours...")

    for msg in messages:
        # On récupère le détail du message (format "full" pour avoir les headers et le payload)
        txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        
        payload = txt.get('payload', {})
        headers = payload.get('headers', [])
        
        # Extraction du Sujet
        sujet = ""
        for header in headers:
            if header['name'] == 'Subject':
                sujet = header['value']
                break
        
        # Extraction du contenu (corps de l'e-mail)
        contenu = ""
        if 'parts' in payload:
            # L'e-mail a plusieurs parties (ex: multipart/alternative)
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        contenu = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        else:
            # L'e-mail est en texte brut uniquement
            data = payload['body'].get('data')
            if data:
                contenu = base64.urlsafe_b64decode(data).decode('utf-8')

        tickets.append({
            "id": msg['id'],
            "sujet": sujet,
            "contenu": contenu.strip()
        })

    print("Extraction terminée avec succès !")
    return tickets


def read_file(path, encoding="utf-8"):
    with open(path, encoding=encoding) as f:
        return f.read()



if __name__ == '__main__':
    liste_tickets = fetch_all_tickets()
    if liste_tickets:
        print("\n--- Premier ticket extrait ---")
        print(f"Sujet : {liste_tickets[0]['sujet']}")
        print(f"Contenu : {liste_tickets[0]['contenu'][:100]}...")
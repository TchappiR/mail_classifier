import gspread

try:
    gc = gspread.service_account(filename='credentials_sheet.json')
except Exception as e:
    print(f"❌ Erreur de chargement des identifiants Google : {e}")

def add_ticket_to_sheet(sheet_url, expediteur, sujet, categorie, urgence, synthese):
    """
    Ajoute une nouvelle ligne dans le Google Sheet spécifié.
    """
    try:
        spreadsheet = gc.open_by_url(sheet_url)
        worksheet = spreadsheet.sheet1
        nouvelle_ligne = [
            expediteur,
            sujet,
            categorie,
            urgence,
            synthese
        ]
        worksheet.append_row(nouvelle_ligne)
        print("✅ Ticket inséré avec succès dans le Google Sheet !")
        
        return True

    except Exception as e:
        print(f"❌ Erreur lors de l'écriture dans le Google Sheet : {e}")
        return False

# --- Test indépendant du module ---
if __name__ == "__main__":
    TEST_URL = "https://docs.google.com/spreadsheets/d/TON_ID_DE_FICHIER/edit"
    print("📝 Test d'écriture sur Google Sheets...")
    add_ticket_to_sheet(
        sheet_url=TEST_URL,
        expediteur="thomas@entreprise.com",
        sujet="Problème de connexion Extranet",
        categorie="Problème d'accès / authentification",
        urgence="Élevée",
        synthese="L'utilisateur n'arrive plus à se connecter à l'extranet (mot de passe rejeté) et doit valider des congés en urgence."
    )
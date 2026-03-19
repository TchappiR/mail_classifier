from mail_reader import fetch_all_tickets
from classifier_agent import classify_ticket
from sheet_writer import add_ticket_to_sheet
from config import SHEET_URL



def main():
    print("🚀 Démarrage de l'assistant de classification de tickets...\n")

    # --- ÉTAPE 1 : LECTURE DES E-MAILS ---
    print("📥 1. Récupération des e-mails via Gmail...")
    tickets = fetch_all_tickets()
    
    if not tickets:
        print("🤷 Aucun nouvel e-mail à traiter. Fin du programme.")
        return

    print(f"✅ {len(tickets)} e-mail(s) récupéré(s).\n")

    # --- ÉTAPE 2 : TRAITEMENT DE CHAQUE E-MAIL ---
    for index, ticket in enumerate(tickets, start=1):
        sujet = ticket.get('sujet', 'Sans objet')
        print(f"🔄 Traitement du ticket {index}/{len(tickets)} (Sujet: {sujet})...")
        
        # On fusionne le sujet et le contenu pour donner un maximum de contexte à l'IA
        texte_a_analyser = f"Sujet: {sujet}\n\nContenu:\n{ticket.get('contenu')}"
        
        # --- ÉTAPE 3 : CLASSIFICATION VIA GROQ ---
        resultat_ia = classify_ticket(texte_a_analyser)
        
        # Gestion des erreurs (si l'API Groq est injoignable par exemple)
        if "error" in resultat_ia:
            print(f"❌ Erreur lors de la classification: {resultat_ia['error']}")
            continue
            
        categorie = resultat_ia.get("categorie", "Non classifié")
        urgence = resultat_ia.get("urgence", "Non définie")
        synthese = resultat_ia.get("synthese", "Pas de synthèse")
        
        print(f"   🤖 Classé comme : {categorie} | Urgence : {urgence}")
        
        # --- ÉTAPE 4 : ÉCRITURE DANS GOOGLE SHEETS ---
        expediteur = ticket.get("expediteur", "Non spécifié")
        
        succes = add_ticket_to_sheet(
            sheet_url=SHEET_URL,
            expediteur=expediteur,
            sujet=sujet,
            categorie=categorie,
            urgence=urgence,
            synthese=synthese
        )
        
        if succes:
            print(f"   📝 Ticket {index} enregistré avec succès dans le Sheet.\n")
        else:
            print(f"   ❌ Échec de l'enregistrement pour le ticket {index}.\n")

    print("🎉 Tous les tickets ont été traités avec succès !")

if __name__ == "__main__":
    main()
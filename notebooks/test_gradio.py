# accueil/sign-in/sign-up
import gradio as gr
from PIL import Image
import re

# ===============================================
# DONNÉES USERS
# ===============================================
utilisateurs = {"test": {"mdp": "1234", "mail": "test@example.com"}}

# ===============================================
# FONCTIONS SIMULÉES (OCR/NLP)
# ===============================================
def ocr_simule(image):
    return """
FACTURE #12345 | Date: 15/12/2025 | Client: Jean Dupont
Livre Python: 25€ | Formation IA: 150€ | Total: 175€
TechFormations SARL"""

def generer_resume(texte):
    mots_cles = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', texte)
    return f"Facture {', '.join(mots_cles[:3])} - Total: 175€"

def extraire_entites(texte):
    return [
        {"entity": "DATE", "word": "15/12/2025", "score": 0.95},
        {"entity": "PERSON", "word": "Jean Dupont", "score": 0.92},
        {"entity": "ORG", "word": "TechFormations SARL", "score": 0.97},
        {"entity": "MONEY", "word": "175€", "score": 0.98}
    ]

def traiter_document(image):
    if image is None: 
        return "Pas d'image", "Chargez une image", []
    texte = ocr_simule(image)
    resume = generer_resume(texte)
    entites = extraire_entites(texte)
    return texte, resume, entites

# ===============================================
# AUTHENTIFICATION
# ===============================================
def verifier_connexion(pseudo, mdp):
    if pseudo in utilisateurs and utilisateurs[pseudo]["mdp"] == mdp:
        return True, f"✅ **{pseudo}** connecté"
    return False, "❌ Identifiants faux"

def creer_compte(pseudo, mail, mdp, mdp_confirm):
    if pseudo in utilisateurs: 
        return gr.update(visible=True), "❌ Pseudo pris"
    if any(u["mail"] == mail for u in utilisateurs.values()): 
        return gr.update(visible=True), "❌ Email pris"
    if mdp != mdp_confirm: 
        return gr.update(visible=True), "❌ MDP différent"
    utilisateurs[pseudo] = {"mdp": mdp, "mail": mail}
    return gr.update(visible=False), "✅ Compte créé !"

# ===============================================
# INTERFACE PRINCIPALE
# ===============================================
with gr.Blocks(title="📄 Summarize AI") as demo:
    gr.Markdown("# 📄 **Summarize AI** - Extraction & Résumé")
    
    # États
    etat_connecte = gr.State(False)
    pseudo_user = gr.State("")
    
    # ===============================================
    # SECTION NON CONNECTÉ (visible par défaut)
    # ===============================================
    with gr.Column(visible=True) as section_non_connecte:
        gr.Markdown("### 🔐 **Connexion requise**")
        gr.Markdown("**Test**: `test` / `1234`")
        
        with gr.Row():
            pseudo_input = gr.Textbox(label="👤 Pseudo", scale=2)
            mdp_input = gr.Textbox(label="🔒 Mot de passe", type="password", scale=2)
        
        with gr.Row():
            btn_login = gr.Button("🚀 Me connecter", variant="primary", scale=1)
            btn_inscription = gr.Button("➕ M'inscrire", variant="secondary", scale=1)
        
        status_login = gr.Markdown()
    
    # ===============================================
    # MODALE INSCRIPTION
    # ===============================================
    with gr.Column(visible=False, elem_id="modale-inscription") as modale_inscription:
        gr.Markdown("## 📝 **Créer un compte**")
        p_reg = gr.Textbox(label="Pseudo")
        m_reg = gr.Textbox(label="Email")
        mdp_reg = gr.Textbox(label="Mot de passe", type="password")
        mdp_c_reg = gr.Textbox(label="Confirmer", type="password")
        
        with gr.Row():
            btn_create = gr.Button("✅ Créer", variant="primary", scale=1)
            btn_close = gr.Button("❌ Fermer", variant="stop", scale=1)
        
        msg_create = gr.Markdown()
    
    # ===============================================
    # SECTION CONNECTÉ (cachée par défaut)
    # ===============================================
    with gr.Column(visible=False) as section_connecte:
        gr.Markdown("### 👤 **Utilisateur connecté**")
        user_status = gr.Markdown()
        btn_logout = gr.Button("🚪 Déconnexion", variant="stop")
        
        # ONGLETS PROTÉGÉS
        with gr.Tabs() as onglets:
            with gr.TabItem("🔍 Rechercher"):
                gr.Markdown("**Fonctionnalité à implémenter**")
            
            with gr.TabItem("📄 Générer"):
                gr.Markdown("### 📤 Chargez votre document")
                img = gr.Image(label="📷 Image/Scan/Facture")
                
                with gr.Row():
                    texte_out = gr.Textbox(label="📄 Texte extrait", lines=8)
                    resume_out = gr.Textbox(label="✨ Résumé", lines=3)
                
                entites_out = gr.Textbox(label="🔑 Entités détectées", lines=8)
                btn_analyse = gr.Button("🔬 Analyser", variant="primary")
    
    # ===============================================
    # ÉVÉNEMENTS - CONNEXION
    # ===============================================
    def gerer_login(pseudo_i, mdp_i):
        ok, msg = verifier_connexion(pseudo_i, mdp_i)
        if ok:
            return (
                gr.update(visible=False),      # ✅ Cache section_non_connecte
                gr.update(visible=False),      # ✅ CACHE modale_inscription (CORRIGÉ !)
                gr.update(visible=True),       # ✅ Affiche section_connecte
                f"**{pseudo_i}** connecté 👋",  # user_status
                pseudo_i,                      # pseudo_user
                msg                            # status_login
            )
        return (
            gr.update(visible=True),        # Garde section_non_connecte
            gr.update(visible=False),       # Cache modale_inscription
            gr.update(visible=False),       # Cache section_connecte
            "",                            # Reset user_status
            "",                            # Reset pseudo_user
            msg                            # Erreur status_login
    )

    
    btn_login.click(
        gerer_login,
        inputs=[pseudo_input, mdp_input],
        outputs=[section_non_connecte, modale_inscription, section_connecte, user_status, pseudo_user, status_login]
    )
    
    # ===============================================
    # ÉVÉNEMENTS - INSCRIPTION
    # ===============================================
    btn_inscription.click(
        fn=lambda: gr.update(visible=True),
        outputs=modale_inscription
    )
    
    btn_close.click(
        fn=lambda: gr.update(visible=False),
        outputs=modale_inscription
    )
    
    btn_create.click(
        creer_compte,
        inputs=[p_reg, m_reg, mdp_reg, mdp_c_reg],
        outputs=[modale_inscription, msg_create]
    )
    
    # ===============================================
    # ÉVÉNEMENTS - DÉCONNEXION
    # ===============================================
    def deconnexion():
        return (
            gr.update(visible=True),    # Montre section_non_connecte
            gr.update(visible=False),   # Cache modale_inscription
            gr.update(visible=False),   # Cache section_connecte
            "",                        # Reset user_status
            "",                        # Reset pseudo_user
            ""                         # Reset status_login
        )
    
    btn_logout.click(
        deconnexion,
        outputs=[section_non_connecte, modale_inscription, section_connecte, user_status, pseudo_user, status_login]
    )
    
    # ===============================================
    # ÉVÉNEMENTS - ANALYSE
    # ===============================================
    def format_entites(entites):
        return "\n".join([f"• {e['entity']}: **{e['word']}** ({e['score']:.1%})" 
                         for e in entites]) if entites else "Aucune entité détectée"
    
    def analyser_document(img):
        texte, resume, entites = traiter_document(img)
        entites_fmt = format_entites(entites)
        return texte, resume, entites_fmt
    
    btn_analyse.click(
        analyser_document,
        inputs=img,
        outputs=[texte_out, resume_out, entites_out]
    )

# Lancement
if __name__ == "__main__":
    demo.launch(share=True, debug=True)

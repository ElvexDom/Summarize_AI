# accueil/sign-in-sign-up.py
import gradio as gr
from app.ui.inscription_ui import create_inscription_ui
from app.ui.nlp_pipeline_ui import create_nlp_pipeline_ui
from app.ui.resume_ui import create_resume_ui
from app.ui.login_ui import create_login_ui
from assets.toaster import show_toast

# ===============================================
# DONNÉES USERS
# ===============================================
utilisateurs = {"test": {"mdp": "1234", "mail": "test@example.com"}}

# ===============================================
# AUTHENTIFICATION
# ===============================================
# def verifier_connexion(pseudo, mdp):
#     if pseudo in utilisateurs and utilisateurs[pseudo]["mdp"] == mdp:
#         return True, f"✅ **{pseudo}** connecté"
#     return False, "❌ Identifiants faux"

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
with gr.Blocks(title="📄 Summarize AI") as gradio:
    gr.Markdown("# 📄 **Summarize AI** - Extraction & Résumé")
    
    # États
    etat_connecte = gr.State(False)
    pseudo_user = gr.State("")

    toast_output = gr.HTML()

    # ===============================================
    # SECTION NON CONNECTÉE
    # ===============================================
    with gr.Column(visible=True) as section_non_connecte:
        gr.Markdown("### 🔐 **Connexion requise**")
        gr.Markdown("**Test**: `test` / `1234`")
        create_login_ui()
        # with gr.Row():
        #     pseudo_input = gr.Textbox(label="👤 Pseudo", scale=2)
        #     mdp_input = gr.Textbox(label="🔒 Mot de passe", type="password", scale=2)
        
        with gr.Row():
            # btn_login = gr.Button("🚀 Me connecter", variant="primary", scale=1)
            btn_inscription = gr.Button("➕ M'inscrire", variant="secondary", scale=1)
        
        status_login = gr.Markdown()

    # ===============================================
    # MODALE INSCRIPTION (importée depuis inscription_ui.py)
    # ===============================================
    inscription_ui, btn_close = create_inscription_ui()

    # ===============================================
    # SECTION CONNECTÉE
    # ===============================================
    with gr.Column(visible=False) as section_connecte:
        gr.Markdown("### 👤 **Utilisateur connecté**")
        user_status = gr.Markdown()
        # show_toast("texte")
        btn_logout = gr.Button("🚪 Déconnexion", variant="stop")
        
        # Onglets
        with gr.Tabs() as onglets:
            with gr.TabItem("🔍 Rechercher"):
                create_resume_ui()
            
            with gr.TabItem("📄 Générer"):
                # Affiche le pipeline NLP complet
                create_nlp_pipeline_ui()

    # ===============================================
    # ÉVÉNEMENTS - CONNEXION
    # ===============================================
    # def gerer_login(pseudo_i, mdp_i):
    #     ok, msg = verifier_connexion(pseudo_i, mdp_i)
    #     if ok:
    #         return (
    #             gr.update(visible=False),      # Cache section_non_connecte
    #             gr.update(visible=False),      # Cache modale_inscription
    #             gr.update(visible=True),       # Affiche section_connecte
    #             f"**{pseudo_i}** connecté 👋",  # user_status
    #             pseudo_i,                      # pseudo_user
    #             msg                            # status_login
    #         )
    #     return (
    #         gr.update(visible=True),        # Garde section_non_connecte
    #         gr.update(visible=False),       # Cache modale_inscription
    #         gr.update(visible=False),       # Cache section_connecte
    #         "",                             # Reset user_status
    #         "",                             # Reset pseudo_user
    #         msg                             # Erreur status_login
    #     )

    # btn_login.click(
    #     gerer_login,
    #     inputs=[pseudo_input, mdp_input],
    #     outputs=[section_non_connecte, inscription_ui, section_connecte, user_status, pseudo_user, status_login]
    # )

    # ===============================================
    # ÉVÉNEMENTS - INSCRIPTION
    # ===============================================
    btn_inscription.click(
        fn=lambda: gr.update(visible=True),
        outputs=inscription_ui
    )
    
    btn_close.click(
        fn=lambda: gr.update(visible=False),
        outputs=inscription_ui
    )

    # ===============================================
    # ÉVÉNEMENTS - DÉCONNEXION
    # ===============================================
    def deconnexion():
        return (
            gr.update(visible=True),      # Montre section_non_connecte
            gr.update(visible=False),     # Cache modale_inscription
            gr.update(visible=False),     # Cache section_connecte
            "",                           # Reset user_status
            "",                           # Reset pseudo_user
            ""                            # Reset status_login
        )
    
    btn_logout.click(
        deconnexion,
        outputs=[section_non_connecte, inscription_ui, section_connecte, user_status, pseudo_user, status_login]
    )

# ===============================================
# Lancement
# ===============================================
if __name__ == "__main__":
    gradio.launch(share=True, debug=True)

# app/ui/auth_ui.py
import gradio as gr
from app.api_client import FastAPIClient

class AuthUI:
    def __init__(self, user_client: FastAPIClient.User):
        """
        UI pour la section Auth (login / register)
        """
        self.user_client = user_client
        self.is_logged = gr.State(False)
        self.auth_ui = None  # référence à la colonne principale de l'UI

    def create(self):
        """Crée l'UI Auth avec onglets Login / Register"""
        with gr.Column() as auth_ui:
            self.auth_ui = auth_ui
            gr.Markdown("## 🔐 Authentification")

            with gr.Tabs():

                # -------- LOGIN --------
                with gr.Tab("Connexion"):
                    self.login_pseudo = gr.Textbox(label="👤 Pseudo")
                    self.login_mdp = gr.Textbox(label="🔒 Mot de passe", type="password")
                    self.btn_login = gr.Button("🚀 Se connecter", variant="primary")
                    self.login_status = gr.Markdown()

                # -------- REGISTER --------
                with gr.Tab("Inscription"):
                    self.reg_pseudo = gr.Textbox(label="👤 Pseudo")
                    self.reg_mdp = gr.Textbox(label="🔒 Mot de passe", type="password")
                    self.reg_confirm = gr.Textbox(label="🔒 Confirmer mot de passe", type="password")
                    self.btn_register = gr.Button("✅ Créer le compte", variant="primary")
                    self.register_status = gr.Markdown()

        # -------- EVENTS --------
        self.btn_login.click(
            self.login,
            inputs=[self.login_pseudo, self.login_mdp],
            outputs=[self.login_status, self.is_logged]
        )

        self.btn_register.click(
            self.register,
            inputs=[self.reg_pseudo, self.reg_mdp, self.reg_confirm],
            outputs=[self.register_status]
        )

        return auth_ui, self.is_logged

    # --------------------- ACTIONS ---------------------
    def login(self, pseudo, mdp):
        """Connexion via user_client"""
        if self.user_client.fetch_login_user(pseudo, mdp):
            return f"✅ **{pseudo} connecté**", True
        return "❌ Identifiants incorrects", False

    def register(self, pseudo, mdp, confirm):
        """Inscription via user_client"""
        if mdp != confirm:
            return "❌ Les mots de passe ne correspondent pas"
        if self.user_client.fetch_add_user(pseudo, mdp):
            return "✅ Compte créé ! Vous pouvez vous connecter."
        return "❌ Erreur lors de l'inscription"

    # --------------------- VISIBILITÉ ---------------------
    def delete(self):
        """Supprime complètement le composant AuthUI"""
        return gr.update(visible=False, value=None)

import gradio as gr
from app.api_client import FastAPIClient

class AuthUI:
    """Section Authentification (login / register)"""

    def __init__(self, user_api: FastAPIClient.User):
        self.user_api = user_api
        self.user = gr.State({"id": None, "pseudo": "Unknown"})
        self.connected = gr.State(False)

        # Construire l'UI dès l'initialisation
        self._build()

    # ---- Méthode interne pour construire l'UI ----
    def _build(self):
        """Crée l'UI Auth dans le contexte Blocks"""
        with gr.Column() as self.ui:
            gr.Markdown("## 🔐 Authentification")

            with gr.Tabs():
                # LOGIN
                with gr.Tab("Connexion"):
                    self.pseudo = gr.Textbox(label="👤 Pseudo")
                    self.password = gr.Textbox(label="🔒 Mot de passe", type="password")
                    self.btn_login = gr.Button("🚀 Se connecter", variant="primary")
                    self.login_status = gr.Markdown("")

                # REGISTER
                with gr.Tab("Inscription"):
                    self.reg_pseudo = gr.Textbox(label="👤 Pseudo")
                    self.reg_password = gr.Textbox(label="🔒 Mot de passe", type="password")
                    self.reg_confirm = gr.Textbox(label="🔒 Confirmer mot de passe", type="password")
                    self.btn_register = gr.Button("✅ Créer le compte", variant="primary")
                    self.register_status = gr.Markdown("")

        # ---- Events ----
        self.btn_login.click(
            self.login,
            inputs=[self.pseudo, self.password],
            outputs=[self.connected, self.login_status, self.user]
        )

        self.btn_register.click(
            self.register,
            inputs=[self.reg_pseudo, self.reg_password, self.reg_confirm],
            outputs=[self.register_status]
        )

    # ---- Callbacks login / register ----
    def login(self, pseudo: str, password: str) -> tuple[bool, str, dict]:
        payload = self.user_api.fetch_login_user(pseudo, password)
        return (
            payload.get("success", False),
            payload.get("message", "❌ Erreur lors de la connexion"),
            payload.get("data", {"id": None, "pseudo": "Unknown"})
        )

    def register(self, pseudo: str, password: str, confirm: str) -> tuple[str]:
        if password != confirm:
            return ("❌ Les mots de passe ne correspondent pas")
        if self.user_api.fetch_add_user(pseudo, password):
            return ("✅ Compte créé ! Vous pouvez vous connecter.")
        return ("❌ Erreur lors de l'inscription")

    # ---- Affichage / Masquage ----
    def show(self) -> gr.update:
        return gr.update(visible=True)

    def hide(self) -> gr.update:
        return gr.update(visible=False)

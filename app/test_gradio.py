import gradio as gr
from assets.toaster import show_toast
from assets.dialog import show_dialogYesNO

# Exemple de fonction à exécuter si l'utilisateur clique "Oui" dans le dialogue
def mafonction():
    print("La fonction a été exécutée !")

# Wrapper pour Gradio pour le toast
def toast_wrapper(message_text):
    show_toast(message_text, color="#4caf50")  # Appel à ta fonction toast
    return f"Toast affiché : {message_text}"

# Wrapper pour Gradio pour le dialogue
def dialog_wrapper():
    show_dialogYesNO(mafonction)  # Appel à ta fonction dialogue
    return "Dialogue affiché"

# --------------------------
# Interface Gradio
# --------------------------
with gr.Blocks() as demo:
    gr.Markdown("### Boutons Toast et Dialogue Oui/Non")

    # Input pour le toast
    toast_input = gr.Textbox(label="Message Toast", value="Action réussie !")
    toast_button = gr.Button("Afficher Toast")
    
    # Bouton dialogYesNo
    dialog_button = gr.Button("Afficher dialogue Oui/Non")

    # Connecter le toast
    toast_button.click(fn=toast_wrapper, inputs=toast_input, outputs=[])

    # Connecter le dialogue
    dialog_button.click(fn=dialog_wrapper, inputs=[], outputs=[])

demo.launch()

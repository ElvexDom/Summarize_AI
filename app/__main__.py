from utils.log_watcher import LogWatcher
from app.frontend_gradio import *

class Application:
    def __init__(self):
        pass

    def run(self):
        LogWatcher.log("info", "Démarrage de l'application.", screen=True)

        try:
            gradio.launch(share=True, debug=True)
            LogWatcher.log("info", "Pipeline OCR/NLP simulé.", screen=True)

        finally:
            LogWatcher.log("info", "Fermeture de l'application.", screen=True)


if __name__ == "__main__":
    app = Application()
    app.run()

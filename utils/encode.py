from cryptography.fernet import Fernet

class Encode:
    def __init__(self, key=None):
        if key is None:
            key = self._load_key()
        self.key = key
        
        self.fernet = Fernet(self.key)

    def GenerateKey(self):
        """Génère une clé et l'enregistre dans un fichier .txt"""
        key = Fernet.generate_key()
        with open('Key.txt', 'a') as f:
            f.write(key.decode() + '\n') 
        return key
    
    def _load_key(self):
        """Charge la dernière clé du fichier si il y en a plusieurs."""
        try:
            with open('Key.txt', 'r') as f:
                lines = f.read().splitlines()
                if lines:
                    return lines[-1].encode()  # dernière clé
        except FileNotFoundError:
            pass
        
        #Si pas de clé, on la génère
        key = self.GenerateKey()
        return key

    def chiffrer_message(self, message):
        """Chiffre le message avec la clé actuelle."""
        return self.fernet.encrypt(message.encode('utf-8'))

    def dechiffrer_message(self, message_chiffre):
        """Déchiffre le message chiffré."""
        return self.fernet.decrypt(message_chiffre).decode('utf-8')
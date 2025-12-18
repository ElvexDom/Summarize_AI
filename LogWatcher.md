# 📝 Procédure : Loguru et LogWatcher

Loguru est une librairie Python moderne qui simplifie le logging et offre une alternative plus agréable et puissante au module standard `logging`. Ses principales caractéristiques sont :

- **Logger préconfiguré** : vous n'avez pas besoin de créer et de configurer un objet logger manuellement ; `logger` est prêt à l'emploi.
    
- **Sortie colorée** : chaque niveau de log a sa couleur, ce qui facilite la lecture dans le terminal.
    
- **Niveaux de log flexibles** : TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL.
    
- **Rotation et rétention des fichiers de logs** : gestion automatique de la taille et de la durée de vie des fichiers.
    
- **Compression** : possibilité de compresser les anciens fichiers de logs pour économiser de l'espace.
    
- **Infos contextuelles** : capture automatiquement le nom du fichier, la ligne et la fonction d'où provient le log.
    
- **Multi-threading et multi-process** : sécurise l'écriture des logs dans des environnements concurrents.
    
- **Simplicité et rapidité** : configuration très facile et syntaxe claire, adaptée aux projets de toutes tailles.
    

---

## 🔹 Installation

```bash
pip install loguru
```

Import dans Python :

```python
from loguru import logger
```

---

## 🔹 LogWatcher : Classe utilitaire pour centraliser les logs

`LogWatcher` utilise Loguru pour automatiser la gestion des logs avec différents fichiers et niveaux :

- Crée automatiquement le dossier `logs/`
    
- Fichiers : `errors.log` (ERROR), `warnings.log` (WARNING), `info.log` (INFO), `all.log` (DEBUG)
    
- Supprime le handler par défaut de Loguru pour éviter les doublons
    
- Permet d’afficher les logs sur la console via `screen=True`
    

### Exemple d’utilisation

```python
from log_watcher import LogWatcher

LogWatcher.log("INFO", "Démarrage de l'application", screen=True)
LogWatcher.log("WARNING", "Attention !")
LogWatcher.log("ERROR", "Une erreur critique")
```

### Méthode `log`

|Paramètre|Type|Description|
|---|---|---|
|`level`|str|Niveau du log (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)|
|`message`|str|Message à enregistrer|
|`screen`|bool|Affiche le message sur la console si `True`|

> Si le niveau fourni est inconnu, le message est enregistré comme `ERROR`.

---

## 🔹 Conseils

- Utiliser `screen=True` seulement pour le développement
    
- Maintenir des niveaux de log cohérents pour un suivi clair
    
- Profiter de la rotation et de la compression pour gérer efficacement les fichiers de logs
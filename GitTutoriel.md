# Introduction à Git

Un tutoriel pour maîtriser le versioning en entreprise, avec des conseils pour le travail en équipe et la gestion avancée des versions.

---

## 1️⃣ Concepts fondamentaux

### Repository

Un dépôt contient tout l'historique de votre projet, tous les fichiers et les modifications.

### Commit

Une sauvegarde avec un message descriptif. Chaque commit représente un état du projet.

### Branch

Une branche est une ligne de développement indépendante. Travaillez sans affecter le code principal.

### Remote

Un dépôt distant (GitHub, GitLab) où vous partagez votre code avec l'équipe.

### Historique et versioning

Git garde la trace de tous vos commits. Vous pouvez revenir à un commit précédent ou examiner l'historique.

---

## 2️⃣ Pourquoi Git ?

- Contrôle de version : gérer toutes les modifications du code.
    
- Collaboration simplifiée : travailler en équipe sans conflits de fichiers.
    
- Historique complet : revenir en arrière si nécessaire.
    
- Sécurité des données : sauvegardes distribuées.
    

---

## 3️⃣ Configuration initiale

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

Vérifiez votre configuration :

```bash
git config --global --list
```

---

## 4️⃣ Commandes de base pour débuter

### Cloner un projet

```bash
git clone <url_du_projet>
```

### Vérifier l'état

```bash
git status
```

### Ajouter et commiter des modifications

```bash
git add nom_fichier.py
git add .
git commit -m "Message du commit"
```

### Synchroniser avec le serveur

```bash
git push origin main
git pull origin main
```

---

## 5️⃣ Gestion des branches et de la collaboration

### Checkout et création de branches

```bash
# Bascule sur une branche existante
git checkout ma-branche
# Crée et bascule sur une nouvelle branche
git checkout -b nouvelle-branche
```

### Push avec -u (upstream)

```bash
git push -u origin ma-branche  # première fois
```

- Après ça, vous pouvez simplement faire `git push` et `git pull`.
    

### Fetch et Merge

```bash
git fetch origin
git merge origin/main
```

- `fetch` récupère tous les commits et références depuis le dépôt distant sans modifier votre branche locale.
    
- `git fetch` récupère également les nouvelles branches distantes. Pour créer une branche locale qui suit une branche distante :
    

```bash
git checkout -b nouvelle-branche origin/nouvelle-branche
```

### Gestion des conflits

1. Vérifiez les conflits :
    

```bash
git status
```

2. Modifiez les fichiers pour résoudre les conflits et supprimez les marqueurs `<<<<<<<`, `=======`, `>>>>>>>`.
    
3. Marquez le fichier comme résolu :
    

```bash
git add fichier_en_conflit.py
```

4. Terminez le merge ou le rebase :
    

```bash
git commit        # merge
# ou
 git rebase --continue  # rebase
```

**Astuce** : pull régulièrement, travailler sur des branches courtes, communiquer avec l’équipe, et utiliser des outils graphiques pour résoudre les conflits.

### Annuler un merge ou un rebase

```bash
git merge --abort       # annuler un merge
 git rebase --abort      # annuler un rebase
```

---

## 6️⃣ Revenir à un commit précédent

### Identifier le commit

```bash
git log --oneline
```

- Permet de voir l’historique avec les identifiants de commit.
    

### Revenir temporairement (mode détaché)

```bash
git checkout <commit_id>
```

- Vous pouvez explorer un ancien état du projet sans affecter la branche.
    

### Revenir définitivement sur un commit (reset)

```bash
git reset --hard <commit_id>
```

- Attention : supprime tous les commits après `<commit_id>` localement.
    
- Pour refléter ce changement sur le serveur, utilisez :
    

```bash
git push --force-with-lease
```

### Créer une branche depuis un ancien commit

```bash
git checkout -b nouvelle-branche <commit_id>
```

- Permet de repartir d’un ancien état sans perdre l’historique.
    

---

## 7️⃣ Changer de branche proprement (état exact de la branche)

Pour vous assurer que votre dossier de travail reflète exactement le contenu de la branche :

```bash
git checkout nom-de-branche       # changer de branche
git reset --hard                  # réinitialise les fichiers suivis

# Aperçu avant suppression :
git clean -nfd                     # fichiers non suivis seulement
git clean -nfdx                    # fichiers non suivis + fichiers ignorés

# Suppression réelle :
git clean -fd                      # supprime les fichiers non suivis seulement
git clean -fdx                     # supprime les fichiers non suivis et ignorés
```

- `reset --hard` : supprime toutes les modifications locales dans les fichiers suivis.
    
- `clean -nfd` : simulation de la suppression des fichiers non suivis.
    
- `clean -nfdx` : simulation de la suppression des fichiers non suivis et des fichiers ignorés.
    
- `clean -fd` : supprime réellement tous les fichiers non suivis.
    
- `clean -fdx` : supprime réellement tous les fichiers non suivis et les fichiers ignorés.
    

> ⚠️ Attention : ces commandes peuvent supprimer définitivement vos modifications locales et fichiers non suivis. Assurez-vous de sauvegarder ce qui est important.

---

## 8️⃣ Workflow pratique recommandé

1. Vérifiez l’état : `git status`
    
2. Récupérez les dernières modifications : `git fetch origin`
    
3. Intégrez les changements : `git merge origin/ma-branche`
    
4. Travaillez sur votre branche : `git checkout ma-branche`
    
5. Ajoutez et committez vos modifications : `git add .` puis `git commit -m "Description du commit"`
    
6. Poussez votre travail : `git push -u origin ma-branche` (la première fois)
    
7. Résolvez les conflits si nécessaire.
    
8. Revenez à un ancien commit si besoin : `git checkout <commit_id>` ou `git reset --hard <commit_id>`
    
9. Créez une branche locale pour suivre une nouvelle branche distante si nécessaire : `git checkout -b nouvelle-branche origin/nouvelle-branche`
    

---

## 9️⃣ Commandes essentielles – Récapitulatif

|Commande|Description|Usage|
|---|---|---|
|git clone|Télécharger un projet|Démarrage|
|git status|Vérifier l'état des fichiers|Quotidien|
|git add|Ajouter des modifications|Avant commit|
|git commit|Créer une sauvegarde|Quotidien|
|git push|Envoyer au serveur|Partage|
|git pull|Récupérer les modifications|Synchronisation|
|git fetch|Récupérer les commits et nouvelles branches sans appliquer|Synchronisation|
|git merge|Fusionner une branche distante|Synchronisation|
|git checkout|Changer ou créer une branche|Développement|
|git push -u|Pousser une branche et créer le lien de suivi|Première fois sur une branche|
|git log|Voir l'historique des commits|Analyse|
|git reset --hard|Revenir définitivement à un commit ou réinitialiser les fichiers suivis|Gestion avancée|
|git clean -fd / git clean -nfd|Supprimer les fichiers non suivis / simuler la suppression|Nettoyage dossier de travail|

---

## 🔟 Exercice pratique et ressources

### Scénario

Vous travaillez en binôme sur un projet de machine learning. L'un crée une branche pour les données, l'autre pour le modèle. Vous devez fusionner vos travaux sans conflits et savoir gérer les nouvelles branches et anciens commits.

- Clonez le dépôt commun
    
- Créez chacun une branche distincte
    
- Commitez vos modifications
    
- Poussez vers le serveur
    
- Fusionnez les branches
    
- Résolvez les conflits éventuels
    
- Revenez à un commit précédent pour tester ou corriger un bug
    
- Créez une branche locale pour suivre toute nouvelle branche distante
    
- Assurez-vous que votre dossier de travail reflète exactement l’état de la branche (`reset --hard` + `git clean -fd`)
    

### Ressources

- Documentation officielle : [git-scm.com](https://git-scm.com/)
    
- Learn Git Branching (interactif) : [learngitbranching.js.org](https://learngitbranching.js.org/)

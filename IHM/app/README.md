# WASPStorm - Interface Graphique

Architecture modulaire de l'interface utilisateur pour WASPStorm - DDoS Testing Tool.

## 📁 Structure du projet

```
IHM/app/
├── __init__.py          # Package principal avec exports
├── main.py              # Point d'entrée de l'application
├── gui.py               # Interface graphique (Vue)
├── event_handlers.py    # Gestionnaires d'événements (Contrôleur)
├── utils.py             # Fonctions utilitaires et validation
└── assets/              # Ressources graphiques
    ├── *.png
    └── ...
```

## 🏗️ Architecture

Le projet suit une architecture **MVC (Model-View-Controller)** modulaire :

### 1. **gui.py** - Vue (View)
- Responsable uniquement de l'affichage de l'interface
- Crée et gère les widgets Tkinter
- **Aucune logique métier**
- Expose des méthodes pour accéder aux widgets (`get_entry_value`, `set_entry_value`)

### 2. **event_handlers.py** - Contrôleur (Controller)
- Gère tous les événements utilisateur
- Contient la logique métier
- Valide les entrées
- Communique avec le modèle (network_tester, cli)

### 3. **main.py** - Point d'entrée
- Initialise l'application
- Crée la GUI et le gestionnaire d'événements
- Les connecte ensemble
- Lance la boucle principale

### 4. **utils.py** - Utilitaires
- Fonctions d'aide réutilisables
- Gestion des chemins vers les assets (`relative_to_assets`)
- Fonctions de validation :
  - `validate_ip()` - Valide une adresse IP
  - `validate_port()` - Valide un numéro de port
  - `validate_url()` - Valide une URL
- Fonction de formatage :
  - `format_number()` - Formate les nombres avec séparateurs

## 🚀 Utilisation

### Lancer l'application

```bash
# Depuis le répertoire racine du projet
cd /Users/namhto/ddos-mitm-pc

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer l'application
python IHM/app/main.py
```

### Ou depuis le module

```bash
python -m IHM.app.main
```

## 💻 Exemple de code

### Utilisation de base

```python
from IHM.app import WASPStormGUI, EventHandler

# Créer l'interface
gui = WASPStormGUI()

# Créer le gestionnaire d'événements
event_handler = EventHandler(gui)

# Associer le gestionnaire à la GUI
gui.event_handler = event_handler

# Lancer l'application
gui.run()
```

### Accéder aux valeurs des champs

```python
# Dans event_handlers.py
class EventHandler:
    def on_start_clicked(self):
        # Récupérer les valeurs
        field_1 = self.gui.get_entry_value('field_1')
        field_2 = self.gui.get_entry_value('field_2')
        
        # Traiter les données
        self.start_test(field_1, field_2)
```

### Modifier les valeurs des champs

```python
# Définir une valeur par défaut
self.gui.set_entry_value('field_1', 'http://example.com')
```

### Gérer le protocole

```python
# Dans event_handlers.py

# Récupérer le protocole sélectionné
protocol = self.gui.get_protocol()  # Retourne "TCP" ou "UDP"

# Définir le protocole par programmation
self.gui.set_protocol("UDP")

# Gérer le changement de protocole
def on_protocol_changed(self, protocol: str):
    if protocol == "TCP":
        print("TCP sélectionné - connexion fiable")
    elif protocol == "UDP":
        print("UDP sélectionné - connexion rapide")
```

### Utiliser les fonctions utilitaires

```python
from IHM.app import validate_ip, validate_port, validate_url, format_number

# Valider une IP
if validate_ip("192.168.1.1"):
    print("IP valide")

# Valider un port
if validate_port("8080"):
    print("Port valide")

# Valider une URL
if validate_url("http://example.com"):
    print("URL valide")

# Formater des nombres
print(format_number(1000000))  # Affiche: "1 000 000"

# Obtenir le chemin d'un asset
from IHM.app.utils import relative_to_assets
image_path = relative_to_assets("image_1.png")
```

## 🎨 Conventions de code

Le code respecte **PEP 8** :
- Noms de classes en `PascalCase` (ex: `WASPStormGUI`)
- Noms de fonctions/méthodes en `snake_case` (ex: `on_start_clicked`)
- Méthodes privées préfixées par `_` (ex: `_create_canvas`)
- Docstrings au format Google
- Type hints pour tous les paramètres et retours
- Constantes en `UPPER_CASE` (ex: `ASSETS_PATH`)

## 📝 Mapping des champs et contrôles

### Champs de saisie

| Nom du champ | Description probable |
|--------------|---------------------|
| `field_1`    | URL ou adresse cible |
| `field_2`    | Paramètre de test |
| `field_3`    | Configuration |
| `field_4`    | Valeur numérique 1 |
| `field_5`    | Valeur numérique 2 |

### Sélection du protocole

| Contrôle | Valeurs | Description |
|----------|---------|-------------|
| `protocol_var` | "TCP" / "UDP" | Protocole réseau à utiliser pour le test |

**Radiobuttons** :
- **TCP** : Protocole orienté connexion (fiable, avec vérification)
- **UDP** : Protocole sans connexion (rapide, sans vérification)

## 🔧 Extension

### Ajouter un nouveau bouton

1. Dans `gui.py`, modifier `_create_buttons()` :
```python
self.buttons['new_button'] = Button(
    self.window,
    text="New Action",
    command=self.event_handler.on_new_button_clicked
)
```

2. Dans `event_handlers.py`, ajouter le gestionnaire :
```python
def on_new_button_clicked(self) -> None:
    """Gestionnaire pour le nouveau bouton."""
    print("New button clicked!")
    # Votre logique ici
```

### Ajouter une validation

Dans `event_handlers.py`, modifier `_validate_input()` :
```python
def _validate_input(self, field_name: str, value: str) -> bool:
    if field_name == 'field_1':
        # Valider une URL
        if not value.startswith(('http://', 'https://')):
            print("[ERROR] Invalid URL")
            return False
    return True
```

## 🐛 Debug

Pour activer les messages de debug, les print statements sont déjà en place :
- `[INFO]` : Informations générales
- `[DEBUG]` : Données de débogage
- `[WARNING]` : Avertissements
- `[ERROR]` : Erreurs

## 📚 Dépendances

- Python 3.11+
- tkinter (inclus avec Python)
- Pillow 8.4.0 (pour les images)

## 🤝 Contribution

L'architecture est conçue pour être facilement extensible :
1. **GUI** reste simple et ne contient que l'affichage
2. **EventHandler** contient toute la logique
3. **main.py** orchestre le tout

Cette séparation permet de :
- Tester la logique indépendamment de l'interface
- Remplacer facilement l'interface (CLI, Web, etc.)
- Maintenir le code plus facilement

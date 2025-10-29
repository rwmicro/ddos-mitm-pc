# WASPStorm - Interface Graphique

Interface graphique pour l'outil de test DDoS WASPStorm.

## Structure

```
IHM/app/
├── gui.py          # Fichier principal de l'interface
├── assets/         # Ressources graphiques (images, boutons, etc.)
│   ├── button_1.png
│   ├── button_2.png
│   ├── entry_*.png
│   └── image_*.png
├── __init__.py     # Module Python
└── README.md       # Ce fichier
```

## Utilisation

Pour lancer l'interface graphique :

```bash
cd IHM/app
python gui.py
```

## Fonctionnalités

- **Configuration** : Cible (IP/Domain), Port, Durée, Threads, Timeout
- **Protocole** : TCP ou UDP
- **Contrôle** : Boutons Start/Stop
- **Résultats** : Affichage des réussites, échecs, taux de réussite et total

## Technologies

- Python 3.x
- Tkinter (interface graphique)
- Design créé avec Tkinter Designer


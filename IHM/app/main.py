"""
Point d'entrée principal pour l'application WASPStorm - DDoS Testing Tool.

Ce module initialise l'application, crée l'interface graphique
et configure les gestionnaires d'événements.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from IHM.app.gui import WASPStormGUI
from IHM.app.event_handlers import EventHandler


def main() -> None:
    """
    Fonction principale de l'application.

    Initialise l'interface graphique et les gestionnaires d'événements,
    puis lance la boucle principale.
    """
    print("[INFO] Initializing WASPStorm - DDoS Testing Tool")

    gui = WASPStormGUI()
    
    # Créer le gestionnaire d'événements
    event_handler = EventHandler(gui)
    
    # Associer l'event_handler et reconfigurer les boutons
    gui.bind_event_handler(event_handler)

    print("[INFO] Application initialized successfully")
    print("[INFO] Starting GUI...")

    try:
        gui.run()
    except KeyboardInterrupt:
        print("\n[INFO] Application interrupted by user")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        raise
    finally:
        print("[INFO] Application closed")


if __name__ == "__main__":
    main()


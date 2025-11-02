"""
Gestionnaires d'événements pour WASPStorm - DDoS Testing Tool.

Ce module contient la classe EventHandler qui gère tous les événements
de l'interface utilisateur (clics de boutons, saisies, etc.).
"""

from typing import TYPE_CHECKING

from .utils import validate_ip, validate_port, validate_url

if TYPE_CHECKING:
    from .gui import WASPStormGUI


class EventHandler:
    """Gestionnaire d'événements pour l'application WASPStorm."""

    def __init__(self, gui: 'WASPStormGUI'):
        """
        Initialise le gestionnaire d'événements.

        Args:
            gui: Instance de WASPStormGUI pour accéder aux widgets
        """
        self.gui = gui
        self.is_running = False

    def on_start_clicked(self) -> None:
        """
        Gestionnaire du clic sur le bouton Start.

        Lance le test DDoS avec les paramètres configurés.
        """
        print("\n" + "="*60)
        print("[EVENT] Start button clicked")
        print("="*60)
        
        # Récupération des valeurs des champs
        field_1_value = self.gui.get_entry_value('field_1')
        field_2_value = self.gui.get_entry_value('field_2')
        field_3_value = self.gui.get_entry_value('field_3')
        field_4_value = self.gui.get_entry_value('field_4')
        field_5_value = self.gui.get_entry_value('field_5')
        
        # Récupération du protocole sélectionné
        protocol = self.gui.get_protocol()
        
        print(f"\n[CONFIG] Configuration du test:")
        print(f"  └─ Protocol: {protocol}")
        print(f"  └─ Field 1 (Target/URL): {field_1_value or '(vide)'}")
        print(f"  └─ Field 2 (Port): {field_2_value or '(vide)'}")
        print(f"  └─ Field 3 (Config): {field_3_value or '(vide)'}")
        print(f"  └─ Field 4: {field_4_value or '(vide)'}")
        print(f"  └─ Field 5: {field_5_value or '(vide)'}")
        
        # Valider les champs avant de démarrer
        if not field_1_value:
            print("\n[ERROR] Le champ Target/URL (field_1) est obligatoire!")
            return
        
        if not self._validate_input('field_1', field_1_value):
            print("[ERROR] Le champ Target/URL (field_1) n'est pas valide!")
            return
        
        if field_2_value and not self._validate_input('field_2', field_2_value):
            print("[ERROR] Le champ Port (field_2) n'est pas valide!")
            return
        
        self.is_running = True
        self._start_test(protocol)
        
        # Réinitialiser les champs après le test
        print("\n[INFO] Réinitialisation des champs...")
        self.gui.clear_all_entries()
        print("="*60 + "\n")

    def on_stop_clicked(self) -> None:
        """
        Gestionnaire du clic sur le bouton Stop.

        Arrête le test DDoS en cours.
        """
        print("\n" + "="*60)
        print("[EVENT] Stop button clicked")
        print("="*60)
        
        if self.is_running:
            print("[INFO] Arrêt du test en cours...")
            self._stop_test()
            self.is_running = False
            print("[SUCCESS] Test arrêté avec succès")
        else:
            print("[WARNING] Aucun test en cours d'exécution")
        
        print("="*60 + "\n")

    def on_entry_changed(self, field_name: str) -> None:
        """
        Gestionnaire appelé quand une entrée est modifiée.

        Args:
            field_name: Nom du champ modifié
        """
        value = self.gui.get_entry_value(field_name)
        print(f"[EVENT] Field '{field_name}' changed: {value}")
        
        self._validate_input(field_name, value)

    def on_protocol_changed(self, protocol: str) -> None:
        """
        Gestionnaire appelé quand le protocole est modifié.

        Args:
            protocol: Protocole sélectionné (TCP ou UDP)
        """
        print(f"[EVENT] Protocol changed to: {protocol}")
        
        if protocol == "TCP":
            print("[INFO] TCP protocol selected - Connection-oriented")
        elif protocol == "UDP":
            print("[INFO] UDP protocol selected - Connectionless")

    def _start_test(self, protocol: str = "TCP") -> None:
        """
        Lance le test DDoS (méthode privée).

        Args:
            protocol: Protocole à utiliser pour le test (TCP ou UDP)

        Cette méthode contient la logique métier pour démarrer le test.
        """
        print(f"\n[INFO] Démarrage du test DDoS avec le protocole {protocol}...")
        
        # Récupérer les paramètres
        target = self.gui.get_entry_value('field_1')
        port = self.gui.get_entry_value('field_2') or "80"
        
        print(f"[TEST] Cible: {target}")
        print(f"[TEST] Port: {port}")
        print(f"[TEST] Protocole: {protocol}")
        
        # TODO: Intégrer avec network_tester.py ou cli.py
        # Exemple: network_tester.start_test(
        #     target=target,
        #     port=int(port),
        #     protocol=protocol.lower(),
        #     ...
        # )
        
        print("[SUCCESS] Test démarré avec succès!")
        print("[INFO] Utilisez le bouton Stop pour arrêter le test")

    def _stop_test(self) -> None:
        """
        Arrête le test DDoS (méthode privée).

        Cette méthode contient la logique métier pour arrêter le test.
        """
        print("[INFO] Stopping DDoS test...")
        # TODO: Implémenter l'arrêt propre du test
        pass

    def _validate_input(self, field_name: str, value: str) -> bool:
        """
        Valide les entrées utilisateur avec les utilitaires de validation.

        Args:
            field_name: Nom du champ à valider
            value: Valeur à valider

        Returns:
            True si la validation réussit, False sinon
        """
        if not value:
            return True 
        
        if field_name == 'field_1':
            if not (validate_url(value) or validate_ip(value)):
                print(f"[WARNING] '{field_name}' doit être une URL ou IP valide")
                return False
        
        elif field_name == 'field_2':
            if not validate_port(value):
                print(f"[WARNING] '{field_name}' doit être un port valide (1-65535)")
                return False
        
        elif field_name in ('field_4', 'field_5'):
            if not value.isdigit():
                print(f"[WARNING] '{field_name}' doit être numérique")
                return False
        
        return True

    def update_metrics(self, metrics: dict) -> None:
        """
        Met à jour les métriques affichées dans l'interface.

        Args:
            metrics: Dictionnaire contenant les métriques à afficher
        """
        # TODO: Implémenter la mise à jour des métriques visuelles
        print(f"[INFO] Updating metrics: {metrics}")
        pass


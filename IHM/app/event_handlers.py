"""
Gestionnaires d'événements pour WASPStorm - DDoS Testing Tool.

Ce module contient la classe EventHandler qui gère tous les événements
de l'interface utilisateur (clics de boutons, saisies, etc.).
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

# Ajouter le chemin parent au sys.path pour importer network_tester
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from network_tester import NetworkStressTester, MessageType, TestStatus
from .utils import validate_ip, validate_port, validate_url, validate_hostname

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
        self.network_tester = None
        self.update_timer_id = None

    def on_start_clicked(self) -> None:
        """
        Gestionnaire du clic sur le bouton Start.

        Lance le test DDoS avec les paramètres configurés.
        """
        print("\n" + "="*60)
        print("[EVENT] Start button clicked")
        print("="*60)

        # Effacer les anciens logs
        if self.gui:
            self.gui.clear_logs()
            self.gui.add_log("=== Nouveau test démarré ===", "INFO")
        
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
            error_msg = "Le champ Target/URL (field_1) est obligatoire!"
            print(f"\n[ERROR] {error_msg}")
            if self.gui:
                self.gui.add_log(error_msg, "ERROR")
            return

        if not self._validate_input('field_1', field_1_value):
            error_msg = "Le champ Target/URL (field_1) n'est pas valide!"
            print(f"[ERROR] {error_msg}")
            if self.gui:
                self.gui.add_log(error_msg, "ERROR")
            return

        if field_2_value and not self._validate_input('field_2', field_2_value):
            error_msg = "Le champ Port (field_2) n'est pas valide!"
            print(f"[ERROR] {error_msg}")
            if self.gui:
                self.gui.add_log(error_msg, "ERROR")
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

    def _network_message_callback(self, msg_type: MessageType, message: str) -> None:
        """
        Callback appelé par NetworkStressTester pour les messages.

        Args:
            msg_type: Type de message (INFO, ERROR, SUCCESS, etc.)
            message: Contenu du message
        """
        # Mapping des types de messages vers les niveaux de logs
        level_mapping = {
            MessageType.INFO: "INFO",
            MessageType.SUCCESS: "SUCCESS",
            MessageType.ERROR: "ERROR",
            MessageType.WARNING: "WARNING",
            MessageType.PROGRESS: "INFO"
        }

        level = level_mapping.get(msg_type, "INFO")

        # Afficher dans la console ET dans le widget de logs
        print(f"[{level}] {message}")

        # Afficher dans le widget de logs de la GUI
        if self.gui:
            self.gui.add_log(message, level)

    def _extract_hostname(self, target: str) -> str:
        """
        Extrait le nom d'hôte d'une URL ou retourne l'input si c'est déjà un hostname/IP.

        Args:
            target: URL complète ou nom d'hôte

        Returns:
            Nom d'hôte nettoyé (sans protocole, sans chemin)
        """
        # Si l'input contient :// c'est probablement une URL
        if '://' in target:
            parsed = urlparse(target)
            hostname = parsed.hostname or parsed.netloc
            print(f"[INFO] URL détectée, extraction du hostname: {target} -> {hostname}")
            return hostname

        # Sinon, retourner tel quel (c'est déjà un hostname ou une IP)
        return target

    def _start_test(self, protocol: str = "TCP") -> None:
        """
        Lance le test DDoS (méthode privée).

        Args:
            protocol: Protocole à utiliser pour le test (TCP ou UDP)

        Cette méthode contient la logique métier pour démarrer le test.
        """
        # Récupérer les paramètres
        target_raw = self.gui.get_entry_value('field_1')
        port_str = self.gui.get_entry_value('field_2') or "80"
        duration_str = self.gui.get_entry_value('field_3') or "10"
        threads_str = self.gui.get_entry_value('field_4') or "10"
        timeout_str = self.gui.get_entry_value('field_5') or "3"

        # Extraire le hostname de l'URL si nécessaire
        target = self._extract_hostname(target_raw)

        try:
            port = int(port_str)
            duration = int(duration_str)
            threads = int(threads_str)
            timeout = float(timeout_str)
        except ValueError:
            error_msg = "Erreur de conversion des paramètres numériques"
            print(f"[ERROR] {error_msg}")
            if self.gui:
                self.gui.add_log(error_msg, "ERROR")
            return

        print(f"\n[INFO] Démarrage du test de stress réseau")
        print(f"[TEST] Cible: {target}")
        print(f"[TEST] Port: {port}")
        print(f"[TEST] Protocole: {protocol}")
        print(f"[TEST] Durée: {duration}s")
        print(f"[TEST] Threads: {threads}")
        print(f"[TEST] Timeout: {timeout}s")

        # Afficher la configuration dans les logs
        if self.gui:
            self.gui.add_log(f"Configuration du test:", "INFO")
            self.gui.add_log(f"  → Cible: {target}", "INFO")
            self.gui.add_log(f"  → Port: {port}", "INFO")
            self.gui.add_log(f"  → Protocole: {protocol}", "INFO")
            self.gui.add_log(f"  → Durée: {duration}s", "INFO")
            self.gui.add_log(f"  → Threads: {threads}", "INFO")
            self.gui.add_log(f"  → Timeout: {timeout}s", "INFO")

        # Créer une nouvelle instance de NetworkStressTester
        self.network_tester = NetworkStressTester(
            target=target,
            port=port,
            duration=duration,
            protocol=protocol,
            threads=threads,
            timeout=timeout,
            verbose=False,
            message_callback=self._network_message_callback
        )

        # Démarrer le test de manière asynchrone
        if self.network_tester.start_test_async():
            success_msg = "Test démarré avec succès!"
            print(f"[SUCCESS] {success_msg}")
            if self.gui:
                self.gui.add_log(success_msg, "SUCCESS")
                self.gui.add_log("Utilisez le bouton Stop pour arrêter le test", "INFO")

            # Démarrer les mises à jour périodiques
            self._start_periodic_updates()
        else:
            error_msg = "Impossible de démarrer le test"
            print(f"[ERROR] {error_msg}")
            if self.gui:
                self.gui.add_log(error_msg, "ERROR")

    def _stop_test(self) -> None:
        """
        Arrête le test DDoS (méthode privée).

        Cette méthode contient la logique métier pour arrêter le test.
        """
        print("[INFO] Arrêt du test de stress réseau...")
        if self.gui:
            self.gui.add_log("Arrêt du test de stress réseau...", "INFO")

        # Arrêter les mises à jour périodiques
        self._stop_periodic_updates()

        # Arrêter le test réseau
        if self.network_tester:
            self.network_tester.stop_test()

            # Afficher les statistiques finales
            stats = self.network_tester.get_stats()
            print(f"\n[STATS] Statistiques finales:")
            print(f"  └─ Requêtes réussies: {stats['success_count']}")
            print(f"  └─ Erreurs: {stats['error_count']}")
            print(f"  └─ Taux de succès: {stats['success_rate']:.2f}%")
            print(f"  └─ Requêtes/seconde: {stats['requests_per_second']:.2f}")
            print(f"  └─ Durée: {stats['elapsed_time']:.2f}s")

            # Afficher dans les logs de la GUI
            if self.gui:
                self.gui.add_log("", "INFO")  # Ligne vide
                self.gui.add_log("=== STATISTIQUES FINALES ===", "STATS")
                self.gui.add_log(f"Requêtes réussies: {stats['success_count']}", "SUCCESS")
                self.gui.add_log(f"Erreurs: {stats['error_count']}", "ERROR")
                self.gui.add_log(f"Total tentatives: {stats['total_attempts']}", "INFO")
                self.gui.add_log(f"Taux de succès: {stats['success_rate']:.2f}%", "INFO")
                self.gui.add_log(f"Requêtes/seconde: {stats['requests_per_second']:.2f}", "INFO")
                self.gui.add_log(f"Durée totale: {stats['elapsed_time']:.2f}s", "INFO")

                # Afficher les types d'erreurs s'il y en a
                if stats['error_types']:
                    self.gui.add_log("Types d'erreurs:", "WARNING")
                    for error_type, count in stats['error_types'].items():
                        self.gui.add_log(f"  → {error_type}: {count}", "WARNING")

            # Mettre à jour l'affichage une dernière fois
            self.update_metrics(stats)
        else:
            warning_msg = "Aucun test en cours"
            print(f"[WARNING] {warning_msg}")
            if self.gui:
                self.gui.add_log(warning_msg, "WARNING")

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
            # Accepter URL, IP ou hostname
            if not (validate_url(value) or validate_ip(value) or validate_hostname(value)):
                print(f"[WARNING] '{field_name}' doit être une URL, hostname ou IP valide")
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
        # Mettre à jour l'affichage des métriques dans l'interface graphique
        # Ces métriques seront affichées dans les zones de texte sur le canvas
        if self.gui:
            self.gui.update_metrics_display(metrics)

    def _start_periodic_updates(self) -> None:
        """
        Démarre les mises à jour périodiques des métriques.
        Utilise after() de Tkinter pour planifier des mises à jour régulières.
        """
        self._update_metrics_callback()

    def _stop_periodic_updates(self) -> None:
        """
        Arrête les mises à jour périodiques des métriques.
        """
        if self.update_timer_id:
            self.gui.window.after_cancel(self.update_timer_id)
            self.update_timer_id = None

    def _update_metrics_callback(self) -> None:
        """
        Callback appelé périodiquement pour mettre à jour les métriques.
        """
        if self.network_tester and self.network_tester.is_running():
            stats = self.network_tester.get_stats()
            self.update_metrics(stats)

            # Planifier la prochaine mise à jour dans 500ms
            self.update_timer_id = self.gui.window.after(500, self._update_metrics_callback)
        else:
            # Le test est terminé, faire une dernière mise à jour
            if self.network_tester:
                stats = self.network_tester.get_stats()
                self.update_metrics(stats)
            self.update_timer_id = None


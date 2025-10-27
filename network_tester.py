#!/usr/bin/env python3
"""
Module de logique métier pour les tests de stress réseau.
Conçu pour être utilisé avec une interface CLI ou GUI.
"""
import socket
import threading
import time
from typing import Optional, Callable, Dict
from enum import Enum


class TestStatus(Enum):
    """États possibles du test."""
    IDLE = "idle"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class MessageType(Enum):
    """Types de messages pour les callbacks."""
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    PROGRESS = "progress"


class NetworkStressTester:
    """
    Testeur de stress réseau avec support TCP et UDP.
    Thread-safe et conçu pour être utilisé avec une interface graphique.
    """

    def __init__(self, target: str, port: int, duration: int,
                 protocol: str, threads: int, timeout: float,
                 verbose: bool = False,
                 message_callback: Optional[Callable[[MessageType, str], None]] = None):
        """
        Initialiser le testeur de stress réseau.

        Args:
            target: Adresse IP ou nom d'hôte DNS de la cible
            port: Numéro de port (1-65535)
            duration: Durée du test en secondes
            protocol: 'TCP' ou 'UDP'
            threads: Nombre de threads (1-1000)
            timeout: Timeout de connexion en secondes
            verbose: Mode verbeux pour afficher tous les détails
            message_callback: Fonction appelée pour chaque message (type, message)
        """
        self.target = target
        self.port = port
        self.duration = duration
        self.protocol = protocol.upper()
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        self.message_callback = message_callback

        # Compteurs thread-safe
        self.request_count = 0
        self.error_count = 0
        self.request_lock = threading.Lock()

        # Contrôle d'exécution
        self.stop_flag = threading.Event()
        self.status = TestStatus.IDLE
        self.status_lock = threading.Lock()

        # Informations
        self.target_ip = None
        self.error_types: Dict[str, int] = {}
        self.start_time = None
        self.end_time = None

        # Threads de travail
        self.worker_threads = []
        self.test_thread = None

    def _log(self, msg_type: MessageType, message: str):
        """
        Envoyer un message via le callback ou ignorer silencieusement.

        Args:
            msg_type: Type de message
            message: Contenu du message
        """
        if self.message_callback:
            self.message_callback(msg_type, message)

    def _set_status(self, status: TestStatus):
        """Changer le statut de manière thread-safe."""
        with self.status_lock:
            self.status = status

    def get_status(self) -> TestStatus:
        """Obtenir le statut actuel de manière thread-safe."""
        with self.status_lock:
            return self.status

    def validate_target(self) -> bool:
        """
        Valider et résoudre la cible.

        Returns:
            True si la cible est valide, False sinon
        """
        try:
            self.target_ip = socket.gethostbyname(self.target)
            return True
        except socket.gaierror:
            return False

    def increment_counter(self):
        """Incrémenter le compteur de requêtes de manière thread-safe."""
        with self.request_lock:
            self.request_count += 1

    def increment_error(self, error_type: str):
        """Incrémenter le compteur d'erreurs de manière thread-safe."""
        with self.request_lock:
            self.error_count += 1
            self.error_types[error_type] = self.error_types.get(error_type, 0) + 1

    def send_tcp_request(self):
        """Envoyer une requête TCP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.target_ip, self.port))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
            sock.close()
            self.increment_counter()
            if self.verbose:
                self._log(MessageType.SUCCESS, f"[TCP] Connexion réussie vers {self.target_ip}:{self.port}")
        except socket.timeout as e:
            self.increment_error("Timeout")
            if self.verbose:
                self._log(MessageType.ERROR, f"[TCP] Timeout: {e}")
        except ConnectionRefusedError as e:
            self.increment_error("Connexion refusée")
            if self.verbose:
                self._log(MessageType.ERROR, f"[TCP] Connexion refusée: {e}")
        except (socket.error, OSError) as e:
            self.increment_error(f"Erreur socket: {type(e).__name__}")
            if self.verbose:
                self._log(MessageType.ERROR, f"[TCP] Erreur: {e}")

    def send_udp_request(self):
        """Envoyer une requête UDP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.sendto(b"X" * 1024, (self.target_ip, self.port))
            sock.close()
            self.increment_counter()
            if self.verbose:
                self._log(MessageType.SUCCESS, f"[UDP] Paquet envoyé vers {self.target_ip}:{self.port}")
        except socket.timeout as e:
            self.increment_error("Timeout")
            if self.verbose:
                self._log(MessageType.ERROR, f"[UDP] Timeout: {e}")
        except (socket.error, OSError) as e:
            self.increment_error(f"Erreur socket: {type(e).__name__}")
            if self.verbose:
                self._log(MessageType.ERROR, f"[UDP] Erreur: {e}")

    def worker_thread_func(self):
        """Thread de travail qui envoie des requêtes en continu."""
        while not self.stop_flag.is_set():
            if self.protocol == "TCP":
                self.send_tcp_request()
            elif self.protocol == "UDP":
                self.send_udp_request()

    def get_stats(self) -> Dict:
        """
        Obtenir les statistiques actuelles du test.

        Returns:
            Dictionnaire contenant toutes les statistiques
        """
        with self.request_lock:
            current_count = self.request_count
            current_errors = self.error_count
            error_types_copy = self.error_types.copy()

        elapsed = 0
        if self.start_time:
            if self.end_time:
                elapsed = self.end_time - self.start_time
            else:
                elapsed = time.time() - self.start_time

        total_attempts = current_count + current_errors
        success_rate = (current_count / total_attempts * 100) if total_attempts > 0 else 0
        requests_per_second = (current_count / elapsed) if elapsed > 0 else 0

        return {
            'success_count': current_count,
            'error_count': current_errors,
            'total_attempts': total_attempts,
            'success_rate': success_rate,
            'elapsed_time': elapsed,
            'requests_per_second': requests_per_second,
            'error_types': error_types_copy,
            'status': self.get_status(),
            'target': self.target,
            'target_ip': self.target_ip,
            'port': self.port,
            'protocol': self.protocol,
            'threads': self.threads,
            'duration': self.duration
        }

    def _run_test(self):
        """Méthode interne qui exécute le test (appelée dans un thread)."""
        try:
            self._set_status(TestStatus.RUNNING)
            self._log(MessageType.INFO, f"Démarrage du test de stress contre {self.target}:{self.port}")

            # Validation de la cible
            if not self.validate_target():
                self._log(MessageType.ERROR, f"Impossible de résoudre la cible '{self.target}'")
                self._set_status(TestStatus.ERROR)
                return

            self._log(MessageType.INFO, f"IP résolue: {self.target_ip}")
            self._log(MessageType.INFO, f"Démarrage de {self.threads} threads...")

            # Réinitialiser les compteurs
            with self.request_lock:
                self.request_count = 0
                self.error_count = 0
                self.error_types.clear()

            self.stop_flag.clear()
            self.start_time = time.time()
            self.end_time = None

            # Créer et démarrer les threads
            self.worker_threads = []
            for i in range(self.threads):
                thread = threading.Thread(target=self.worker_thread_func, daemon=True)
                thread.start()
                self.worker_threads.append(thread)

            self._log(MessageType.SUCCESS, "Threads démarrés, test en cours...")

            # Attendre la durée spécifiée
            elapsed = 0
            while elapsed < self.duration and not self.stop_flag.is_set():
                time.sleep(0.1)
                elapsed = time.time() - self.start_time

            # Arrêter les threads
            self._log(MessageType.INFO, "Arrêt des threads...")
            self.stop_flag.set()

            # Attendre que tous les threads se terminent
            for thread in self.worker_threads:
                thread.join(timeout=1.0)

            self.end_time = time.time()
            self._set_status(TestStatus.STOPPED)
            self._log(MessageType.SUCCESS, "Test terminé")

        except Exception as e:
            self._log(MessageType.ERROR, f"Erreur pendant le test: {e}")
            self._set_status(TestStatus.ERROR)

    def start_test_async(self):
        """
        Démarrer le test de manière asynchrone (non-bloquant).
        Le test s'exécute dans un thread séparé.

        Returns:
            True si le test a démarré, False sinon
        """
        if self.get_status() == TestStatus.RUNNING:
            self._log(MessageType.WARNING, "Un test est déjà en cours")
            return False

        self.test_thread = threading.Thread(target=self._run_test, daemon=True)
        self.test_thread.start()
        return True

    def start_test_blocking(self):
        """
        Démarrer le test de manière bloquante (attend la fin).
        Utilisé pour l'interface CLI.
        """
        self._run_test()

    def stop_test(self):
        """
        Arrêter le test proprement.
        """
        if self.get_status() == TestStatus.RUNNING:
            self._log(MessageType.INFO, "Demande d'arrêt du test...")
            self._set_status(TestStatus.STOPPING)
            self.stop_flag.set()

            # Attendre que le thread de test se termine
            if self.test_thread and self.test_thread.is_alive():
                self.test_thread.join(timeout=2.0)

            self.end_time = time.time()
            self._set_status(TestStatus.STOPPED)
            self._log(MessageType.INFO, "Test arrêté")

    def is_running(self) -> bool:
        """Vérifier si le test est en cours."""
        return self.get_status() == TestStatus.RUNNING

    def reset(self):
        """Réinitialiser le testeur pour un nouveau test."""
        if self.is_running():
            self.stop_test()

        with self.request_lock:
            self.request_count = 0
            self.error_count = 0
            self.error_types.clear()

        self.start_time = None
        self.end_time = None
        self._set_status(TestStatus.IDLE)

    # Méthodes de configuration (setters)
    def setProtocol(self, protocol: str):
        """Changer le protocole."""
        if not self.is_running():
            self.protocol = protocol.upper()

    def setDuration(self, duration: int):
        """Changer la durée."""
        if not self.is_running():
            self.duration = duration

    def setThreads(self, threads: int):
        """Changer le nombre de threads."""
        if not self.is_running():
            self.threads = threads

    def setTimeout(self, timeout: float):
        """Changer le timeout."""
        if not self.is_running():
            self.timeout = timeout

    def setTarget(self, target: str):
        """Changer la cible."""
        if not self.is_running():
            self.target = target
            self.target_ip = None

    def setPort(self, port: int):
        """Changer le port."""
        if not self.is_running():
            self.port = port

    def setVerbose(self, verbose: bool):
        """Activer/désactiver le mode verbose."""
        self.verbose = verbose

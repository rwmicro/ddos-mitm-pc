#!/usr/bin/env python3
"""
Interface en ligne de commande pour le testeur de stress réseau.
Utilise network_tester.py pour la logique métier.
"""
import argparse
import sys
import time
from network_tester import NetworkStressTester, MessageType, TestStatus


def print_message(msg_type: MessageType, message: str):
    """
    Callback pour afficher les messages dans le terminal.

    Args:
        msg_type: Type de message
        message: Contenu du message
    """
    # On affiche les messages normalement (sauf PROGRESS qui sera géré séparément)
    if msg_type != MessageType.PROGRESS:
        print(message)


def validate_port(port: str) -> int:
    """Valider le numéro de port."""
    try:
        port_num = int(port)
        if 1 <= port_num <= 65535:
            return port_num
        else:
            raise argparse.ArgumentTypeError("Le port doit être entre 1 et 65535.")
    except ValueError:
        raise argparse.ArgumentTypeError("Le port doit être un entier.")


def validate_duration(duration: str) -> int:
    """Valider la durée."""
    try:
        dur = int(duration)
        if dur > 0:
            return dur
        else:
            raise argparse.ArgumentTypeError("La durée doit être positive.")
    except ValueError:
        raise argparse.ArgumentTypeError("La durée doit être un entier.")


def validate_threads(threads: str) -> int:
    """Valider le nombre de threads."""
    try:
        t = int(threads)
        if 1 <= t <= 1000:
            return t
        else:
            raise argparse.ArgumentTypeError("Les threads doivent être entre 1 et 1000.")
    except ValueError:
        raise argparse.ArgumentTypeError("Les threads doivent être un entier.")


def validate_timeout(timeout: str) -> float:
    """Valider le timeout."""
    try:
        t = float(timeout)
        if t > 0:
            return t
        else:
            raise argparse.ArgumentTypeError("Le timeout doit être positif.")
    except ValueError:
        raise argparse.ArgumentTypeError("Le timeout doit être un nombre.")


def create_parser() -> argparse.ArgumentParser:
    """Créer le parser d'arguments."""
    parser = argparse.ArgumentParser(
        description="Outil de test de stress réseau pour tester la robustesse des serveurs.",
    )

    # Required arguments
    required = parser.add_argument_group('arguments requis')
    required.add_argument(
        '-t', '--target',
        type=str,
        required=True,
        metavar='HÔTE',
        help='Adresse IP ou nom d\'hôte DNS de la cible'
    )

    required.add_argument(
        '-p', '--port',
        type=validate_port,
        required=True,
        metavar='PORT',
        help='Numéro de port de la cible (1-65535)'
    )

    required.add_argument(
        '-d', '--duration',
        type=validate_duration,
        required=True,
        metavar='SECONDES',
        help='Durée du test en secondes'
    )

    required.add_argument(
        '-m', '--protocol',
        type=str,
        required=True,
        choices=['TCP', 'UDP', 'tcp', 'udp'],
        metavar='PROTOCOLE',
        help='Protocole à utiliser (TCP ou UDP)'
    )

    # Optional arguments
    optional = parser.add_argument_group('arguments optionnels')
    optional.add_argument(
        '-T', '--threads',
        type=validate_threads,
        default=1,
        metavar='NOMBRE',
        help='Nombre de threads à utiliser (1-1000, défaut: 1)'
    )

    optional.add_argument(
        '--timeout',
        type=validate_timeout,
        default=5.0,
        metavar='SECONDES',
        help='Délai d\'expiration de connexion en secondes (défaut: 5.0)'
    )

    optional.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Activer la sortie détaillée'
    )

    optional.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )

    return parser


def display_header(tester: NetworkStressTester):
    """Afficher l'en-tête avec les informations du test."""

    print(f"Configuration du test de stress")
    print(f"{'='*60}")
    print(f"Cible:      {tester.target}")
    print(f"Port:       {tester.port}")
    print(f"Protocole:  {tester.protocol}")
    print(f"Threads:    {tester.threads}")
    print(f"Durée:      {tester.duration}s")
    print(f"Timeout:    {tester.timeout}s")
    print(f"{'='*60}\n")


def display_progress(tester: NetworkStressTester):
    """Afficher la progression en temps réel."""
    stats = tester.get_stats()
    elapsed = int(stats['elapsed_time'])
    print(f"\rTemps écoulé: {elapsed}s | Réussites: {stats['success_count']} | Échecs: {stats['error_count']}",
          end="", flush=True)


def display_results(tester: NetworkStressTester):
    """Afficher les résultats finaux."""
    stats = tester.get_stats()

    print(f"\n\nTest terminé.")
    print(f"{'='*60}")
    print(f"Total de requêtes réussies: {stats['success_count']}")
    print(f"Total d'échecs: {stats['error_count']}")
    print(f"Total de tentatives: {stats['total_attempts']}")
    print(f"Taux de réussite: {stats['success_rate']:.2f}%")
    print(f"Durée totale: {stats['elapsed_time']:.2f}s")

    if stats['success_count'] > 0:
        print(f"Taux moyen (réussies): {stats['requests_per_second']:.2f} requêtes/s")

    print(f"{'='*60}")

    # Afficher le détail des erreurs
    if stats['error_count'] > 0:
        print("\nDétail des erreurs:")
        sorted_errors = sorted(stats['error_types'].items(), key=lambda x: x[1], reverse=True)
        for error_type, count in sorted_errors:
            percentage = (count / stats['error_count'] * 100)
            print(f"  - {error_type}: {count} ({percentage:.1f}%)")
        print(f"{'='*60}")


def main():
    """Point d'entrée principal."""
    arg_parser = create_parser()

    # Afficher l'aide si aucun argument n'est fourni
    if len(sys.argv) == 1:
        arg_parser.print_help()
        sys.exit(0)

    args = arg_parser.parse_args()

    # Créer le testeur avec callback pour les messages
    tester = NetworkStressTester(
        target=args.target,
        port=args.port,
        duration=args.duration,
        protocol=args.protocol,
        threads=args.threads,
        timeout=args.timeout,
        verbose=args.verbose,
        message_callback=print_message
    )

    # Afficher l'en-tête
    display_header(tester)

    try:
        # Démarrer le test dans un thread séparé
        tester.start_test_async()

        # Attendre que le test démarre
        time.sleep(0.1)

        # Afficher la progression pendant que le test s'exécute
        while tester.is_running():
            if not args.verbose:  # En mode verbose, les messages s'affichent déjà
                display_progress(tester)
            time.sleep(0.5)

        # Afficher les résultats finaux
        display_results(tester)

    except KeyboardInterrupt:
        print("\n\nArrêt demandé par l'utilisateur...")
        tester.stop_test()

        # Attendre un peu que le test s'arrête
        time.sleep(0.5)

        stats = tester.get_stats()
        print(f"Requêtes envoyées avant interruption: {stats['success_count']}")
        print(f"Erreurs avant interruption: {stats['error_count']}")
        sys.exit(0)

    except Exception as e:
        print(f"\nERREUR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

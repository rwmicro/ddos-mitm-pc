"""
Fonctions utilitaires pour l'application WASPStorm.

Ce module contient les fonctions d'aide et utilitaires réutilisables
à travers l'application.
"""

from pathlib import Path
from typing import Union


# Chemins de base de l'application
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")


def relative_to_assets(path: str) -> Path:
    """
    Retourne le chemin complet vers un asset.

    Cette fonction permet d'accéder aux ressources graphiques
    (images, icônes, etc.) de manière relative au dossier assets.

    Args:
        path: Chemin relatif de l'asset (ex: "image_1.png")

    Returns:
        Chemin complet vers l'asset

    Example:
        >>> img_path = relative_to_assets("button_1.png")
        >>> # Retourne: /path/to/IHM/app/assets/button_1.png
    """
    return ASSETS_PATH / Path(path)


def validate_ip(ip_address: str) -> bool:
    """
    Valide une adresse IP (IPv4).

    Args:
        ip_address: Adresse IP à valider

    Returns:
        True si l'adresse est valide, False sinon

    Example:
        >>> validate_ip("192.168.1.1")
        True
        >>> validate_ip("256.1.1.1")
        False
    """
    try:
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        return all(0 <= int(part) <= 255 for part in parts)
    except (ValueError, AttributeError):
        return False


def validate_port(port: Union[str, int]) -> bool:
    """
    Valide un numéro de port.

    Args:
        port: Numéro de port à valider (string ou int)

    Returns:
        True si le port est valide (1-65535), False sinon

    Example:
        >>> validate_port("8080")
        True
        >>> validate_port("70000")
        False
    """
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


def validate_url(url: str) -> bool:
    """
    Valide une URL.

    Args:
        url: URL à valider

    Returns:
        True si l'URL est valide, False sinon

    Example:
        >>> validate_url("http://example.com")
        True
        >>> validate_url("not_a_url")
        False
    """
    if not url:
        return False

    valid_schemes = ('http://', 'https://')
    return any(url.lower().startswith(scheme) for scheme in valid_schemes)


def validate_hostname(hostname: str) -> bool:
    """
    Valide un nom d'hôte (hostname) ou nom de domaine.

    Args:
        hostname: Nom d'hôte à valider

    Returns:
        True si le hostname est valide, False sinon

    Example:
        >>> validate_hostname("example.com")
        True
        >>> validate_hostname("sub.example.com")
        True
        >>> validate_hostname("localhost")
        True
        >>> validate_hostname("invalid..hostname")
        False
    """
    if not hostname or len(hostname) > 253:
        return False

    # Supprimer le port si présent
    if ':' in hostname:
        hostname = hostname.split(':')[0]

    # Un hostname peut contenir des lettres, chiffres, tirets et points
    # Chaque label (partie entre les points) doit:
    # - avoir entre 1 et 63 caractères
    # - commencer et finir par une lettre ou un chiffre
    # - peut contenir des tirets au milieu

    labels = hostname.split('.')
    if not labels:
        return False

    for label in labels:
        if not label or len(label) > 63:
            return False
        # Vérifier que le label ne commence/finit pas par un tiret
        if label.startswith('-') or label.endswith('-'):
            return False
        # Vérifier que le label contient uniquement des caractères valides
        if not all(c.isalnum() or c == '-' for c in label):
            return False

    return True


def format_number(number: int) -> str:
    """
    Formate un nombre avec des séparateurs de milliers.

    Args:
        number: Nombre à formater

    Returns:
        Nombre formaté avec des espaces comme séparateurs

    Example:
        >>> format_number(1000000)
        '1 000 000'
    """
    return f"{number:,}".replace(',', ' ')


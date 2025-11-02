"""
WASPStorm - Interface Graphique.

Module d'interface utilisateur pour le testeur DDoS.
Architecture modulaire avec séparation de l'interface et de la logique métier.
"""

from .gui import WASPStormGUI
from .event_handlers import EventHandler
from .utils import (
    relative_to_assets,
    validate_ip,
    validate_port,
    validate_url,
    format_number
)

__version__ = "1.0.0"
__author__ = "Othman"

__all__ = [
    'WASPStormGUI',
    'EventHandler',
    'relative_to_assets',
    'validate_ip',
    'validate_port',
    'validate_url',
    'format_number'
]

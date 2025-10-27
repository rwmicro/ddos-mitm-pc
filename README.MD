### Outil de test de stress réseau pour tester la robustesse des serveurs.

options:
  -h, --help            show this help message and exit

arguments requis:
  -t HÔTE, --target HÔTE
                        Adresse IP ou nom d'hôte DNS de la cible
  -p PORT, --port PORT  Numéro de port de la cible (1-65535)
  -d SECONDES, --duration SECONDES
                        Durée du test en secondes
  -m PROTOCOLE, --protocol PROTOCOLE
                        Protocole à utiliser (TCP ou UDP)

arguments optionnels:
  -T NOMBRE, --threads NOMBRE
                        Nombre de threads à utiliser (1-1000, défaut: 1)
  --timeout SECONDES    Délai d'expiration de connexion en secondes
                        (défaut: 5.0)
  -v, --verbose         Activer la sortie détaillée
  --version             show program's version number and exit
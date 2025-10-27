# 🔧 Network Stress Tester

Un outil de test de stress réseau simple et efficace pour évaluer la robustesse de vos serveurs.

## 📋 Description

Cet outil permet de tester la résistance et les performances de vos serveurs en générant du trafic réseau contrôlé. Il supporte les protocoles TCP et UDP avec une configuration flexible via plusieurs threads.

## 💻 Utilisation

### Syntaxe de base

```bash
python stress_test.py -t HÔTE -p PORT -d DURÉE -m PROTOCOLE [OPTIONS]
```

### Arguments requis

| Argument | Description |
|----------|-------------|
| `-t, --target HÔTE` | Adresse IP ou nom d'hôte DNS de la cible |
| `-p, --port PORT` | Numéro de port de la cible (1-65535) |
| `-d, --duration SECONDES` | Durée du test en secondes |
| `-m, --protocol PROTOCOLE` | Protocole à utiliser (TCP ou UDP) |

### Arguments optionnels

| Argument | Description | Défaut |
|----------|-------------|---------|
| `-T, --threads NOMBRE` | Nombre de threads à utiliser (1-1000) | 1 |
| `--timeout SECONDES` | Délai d'expiration de connexion | 5.0 |
| `-v, --verbose` | Activer la sortie détaillée | Désactivé |
| `-h, --help` | Afficher l'aide | - |
| `--version` | Afficher la version du programme | - |

## 📝 Exemples

### Test TCP basique
```bash
python stress_test.py -t 192.168.1.100 -p 8080 -d 30 -m TCP
```

### Test UDP avec plusieurs threads
```bash
python stress_test.py -t example.com -p 443 -d 60 -m UDP -T 10 --verbose
```

### Test avec timeout personnalisé
```bash
python stress_test.py -t localhost -p 3000 -d 120 -m TCP --timeout 10 -v
```

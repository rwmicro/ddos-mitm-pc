# 🏗️ WASPStorm - Architecture & Environment

## 📊 Diagramme d'Architecture Système

```mermaid
graph TB
    %% Utilisateur
    User[👤 Utilisateur]
    
    %% Couche Interface
    subgraph Interface["🖥️ Couche Interface / Présentation"]
        CLI[CLI Interface<br/>cli.py]
        GUI[GUI Interface<br/>Tkinter MVC]
        
        subgraph MVC["Architecture MVC"]
            Main[main.py<br/>Orchestrateur]
            View[gui.py<br/>Vue]
            Controller[event_handlers.py<br/>Contrôleur]
            Utils[utils.py<br/>Utilitaires]
        end
    end
    
    %% Couche Métier
    subgraph Business["⚙️ Couche Métier / Logique"]
        Tester[NetworkStressTester<br/>network_tester.py]
        
        subgraph Components["Composants"]
            Threading[🧵 Thread Manager<br/>Multi-threading]
            Protocol[📡 Protocol Handler<br/>TCP/UDP]
            Stats[📊 Statistics Engine<br/>Compteurs & Métriques]
        end
    end
    
    %% Couche Réseau
    subgraph Network["🌐 Couche Réseau"]
        Socket[Python Socket API]
        TCP[TCP Connections]
        UDP[UDP Datagrams]
    end
    
    %% Cible
    Target[🎯 Serveur Cible<br/>IP:Port]
    
    %% Connexions
    User --> CLI
    User --> GUI
    
    CLI --> Tester
    GUI --> Main
    Main --> View
    Main --> Controller
    Controller --> View
    Controller --> Utils
    Controller --> Tester
    
    Tester --> Threading
    Tester --> Protocol
    Tester --> Stats
    
    Threading --> Socket
    Protocol --> Socket
    
    Socket --> TCP
    Socket --> UDP
    
    TCP --> Target
    UDP --> Target
    
    %% Feedback
    Stats -.Statistiques.-> Controller
    Stats -.Statistiques.-> CLI
    
    style User fill:#e1f5ff
    style Interface fill:#fff4e6
    style Business fill:#e8f5e9
    style Network fill:#f3e5f5
    style Target fill:#ffebee
```

## 🔄 Flux de Données

```mermaid
sequenceDiagram
    participant U as 👤 Utilisateur
    participant I as 🖥️ Interface<br/>(CLI/GUI)
    participant T as ⚙️ NetworkStressTester
    participant W as 🧵 Worker Threads
    participant N as 🌐 Network Socket
    participant S as 🎯 Serveur Cible
    
    U->>I: Configuration du test<br/>(Target, Port, Protocol, Durée)
    I->>I: Validation des entrées
    I->>T: start_test_async()
    
    activate T
    T->>T: Résolution DNS
    T->>T: Initialisation compteurs
    
    loop Pour chaque thread (1-1000)
        T->>W: Créer Worker Thread
        activate W
    end
    
    Note over T,W: Test en cours (durée configurée)
    
    loop Envoi continu de requêtes
        W->>N: Créer connexion TCP/UDP
        N->>S: Envoyer requête
        S-->>N: Réponse (ou timeout)
        N-->>W: Résultat
        W->>T: Incrémenter compteurs
    end
    
    T-->>I: Statistiques en temps réel
    I-->>U: Affichage progression
    
    T->>W: Signal d'arrêt
    deactivate W
    
    T->>T: Calcul statistiques finales
    T-->>I: Résultats finaux
    deactivate T
    I-->>U: Affichage résultats
```

## 🛠️ Stack Technique

```mermaid
graph LR
    subgraph Lang["💻 Langage"]
        Python[Python 3.11+]
    end
    
    subgraph UI["🎨 Interface Utilisateur"]
        Tkinter[Tkinter<br/>GUI natif]
        Pillow[Pillow 8.4.0<br/>Images]
        Argparse[Argparse<br/>CLI]
    end
    
    subgraph Core["🔧 Core Libraries"]
        Socket[socket<br/>Réseau]
        Thread[threading<br/>Concurrence]
        Time[time<br/>Timing]
    end
    
    subgraph Design["🏛️ Patterns"]
        MVC[MVC Pattern]
        OOP[POO]
        Callback[Callback Pattern]
        ThreadSafe[Thread-Safe]
    end
    
    Python --> Tkinter
    Python --> Socket
    Python --> Thread
    Python --> Argparse
    Tkinter --> Pillow
    
    style Lang fill:#3776ab,color:#fff
    style UI fill:#4caf50,color:#fff
    style Core fill:#ff9800,color:#fff
    style Design fill:#9c27b0,color:#fff
```

## 🌍 Environnement d'Exécution

```mermaid
graph TB
    subgraph Env["💻 Environnement d'exécution"]
        OS[Système d'exploitation<br/>Windows / Linux / macOS]
        
        subgraph App["📦 Application WASPStorm"]
            direction TB
            Entry[Point d'entrée]
            CLI_E[CLI Mode]
            GUI_E[GUI Mode]
            
            Entry --> CLI_E
            Entry --> GUI_E
        end
        
        subgraph Resources["📂 Ressources"]
            Assets[assets/<br/>Images PNG]
            Config[Configuration<br/>Paramètres utilisateur]
        end
    end
    
    subgraph Network_Env["🌐 Environnement Réseau"]
        Local[Réseau Local]
        Internet[Internet]
        Firewall[Firewall/<br/>Règles sécurité]
    end
    
    subgraph Target_Env["🎯 Environnement Cible"]
        Server[Serveur de Test]
        Monitor[Monitoring<br/>Métriques]
    end
    
    OS --> App
    App --> Assets
    App --> Config
    
    App --> Firewall
    Firewall --> Local
    Firewall --> Internet
    
    Local --> Server
    Internet --> Server
    Server --> Monitor
    
    style Env fill:#e3f2fd
    style Network_Env fill:#fff3e0
    style Target_Env fill:#fce4ec
```

## 📋 Composants Principaux

| Composant | Responsabilité | Technologie |
|-----------|---------------|-------------|
| **CLI Interface** | Interface ligne de commande | Python Argparse |
| **GUI Interface** | Interface graphique utilisateur | Tkinter + MVC |
| **NetworkStressTester** | Logique métier du test | Python OOP + Threading |
| **Worker Threads** | Envoi parallèle de requêtes | threading.Thread |
| **Protocol Handler** | Gestion TCP/UDP | socket library |
| **Statistics Engine** | Calcul des métriques | Thread-safe counters |

## 🔐 Caractéristiques Techniques

- **Thread-Safe**: Utilisation de Lock pour sécuriser les compteurs partagés
- **Asynchrone**: Tests non-bloquants avec callbacks
- **Scalable**: Support de 1 à 1000 threads simultanés
- **Protocoles**: TCP et UDP
- **Monitoring**: Statistiques en temps réel
- **Robuste**: Gestion d'erreurs et timeout configurables

## 📊 Métriques Collectées

```mermaid
mindmap
  root((📊 Métriques))
    Performance
      Requêtes/seconde
      Temps écoulé
      Latence moyenne
    Résultats
      Succès
      Échecs
      Total tentatives
    Taux
      Taux de réussite
      Distribution erreurs
      Par type d'erreur
    Configuration
      Protocole TCP/UDP
      Nombre de threads
      Cible & Port
```

## 🎯 Cas d'Usage

1. **Test de Charge** - Évaluer la capacité maximale du serveur
2. **Test de Stress** - Identifier les points de rupture
3. **Test de Résilience** - Vérifier la récupération après charge
4. **Audit de Sécurité** - Valider les protections anti-DDoS

---

*Ce diagramme représente l'architecture complète de WASPStorm pour une présentation professionnelle*


"""
Interface graphique pour WASPStorm - DDoS Testing Tool.

Ce module contient la classe WASPStormGUI qui gère l'affichage
de l'interface utilisateur.
"""

from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, StringVar
from typing import Optional

from .utils import relative_to_assets


class WASPStormGUI:
    """Interface graphique principale pour WASPStorm - DDoS Testing Tool."""

    def __init__(self, event_handler: Optional[object] = None):
        """
        Initialise l'interface graphique.

        Args:
            event_handler: Instance du gestionnaire d'événements
        """
        # Référence au gestionnaire d'événements
        self.event_handler = event_handler

        # Initialisation de la fenêtre principale
        self.window = Tk()
        self.window.geometry("1024x728")
        self.window.configure(bg="#FFFFFF")
        self.window.title("WASPStorm - DDoS Tester")
        self.window.resizable(False, False)

        # Stockage des images pour éviter le garbage collection
        self.images = {}
        self.entries = {}
        self.buttons = {}
        self.radiobuttons = {}

        # Variable de contrôle pour le protocole sélectionné
        self.protocol_var = StringVar(value="TCP")

        # Création de l'interface
        self._create_canvas()
        self._create_images()
        self._create_entries()
        self._create_radiobuttons()
        self._create_buttons()
        self._create_text_elements()
    
    def _create_canvas(self):
        """Crée le canvas principal"""
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=728,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
    
    def _create_images(self):
        """Crée toutes les images de fond et décorations"""
        # Image de fond principale
        self.images['bg_1'] = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(512.0, 364.0, image=self.images['bg_1'])
        
        # Image du bas
        self.images['bg_2'] = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(112.0, 659.0, image=self.images['bg_2'])
        
        # Image du haut
        self.images['bg_3'] = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(512.0, 149.0, image=self.images['bg_3'])
        
        # Labels et icônes pour les champs de saisie
        self.images['label_1'] = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(114.0, 71.27737045288086, image=self.images['label_1'])
        
        self.images['label_2'] = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(526.0, 69.27737045288086, image=self.images['label_2'])
        
        self.images['label_3'] = PhotoImage(file=relative_to_assets("image_6.png"))
        self.canvas.create_image(108.0, 154.7737274169922, image=self.images['label_3'])
        
        self.images['label_4'] = PhotoImage(file=relative_to_assets("image_7.png"))
        self.canvas.create_image(75.0, 225.0, image=self.images['label_4'])
        
        self.images['label_5'] = PhotoImage(file=relative_to_assets("image_8.png"))
        self.canvas.create_image(226.0, 226.0, image=self.images['label_5'])
        
        # Images de statut et indicateurs
        self.images['indicator_1'] = PhotoImage(file=relative_to_assets("image_9.png"))
        self.canvas.create_image(547.0, 156.36495971679688, image=self.images['indicator_1'])
        
        self.images['indicator_2'] = PhotoImage(file=relative_to_assets("image_10.png"))
        self.canvas.create_image(551.0, 185.78831481933594, image=self.images['indicator_2'])
        
        self.images['indicator_3'] = PhotoImage(file=relative_to_assets("image_11.png"))
        self.canvas.create_image(656.0, 518.0, image=self.images['indicator_3'])
        
        self.images['indicator_4'] = PhotoImage(file=relative_to_assets("image_12.png"))
        self.canvas.create_image(648.0, 185.78831481933594, image=self.images['indicator_4'])
        
        self.images['logo'] = PhotoImage(file=relative_to_assets("image_13.png"))
        self.canvas.create_image(135.0, 48.0, image=self.images['logo'])
        
        self.images['graph_1'] = PhotoImage(file=relative_to_assets("image_14.png"))
        self.canvas.create_image(657.0, 598.0, image=self.images['graph_1'])
        
        self.images['graph_2'] = PhotoImage(file=relative_to_assets("image_15.png"))
        self.canvas.create_image(723.0, 392.0, image=self.images['graph_2'])
        
        # Icônes de métriques
        self.images['metric_1'] = PhotoImage(file=relative_to_assets("image_16.png"))
        self.canvas.create_image(742.0, 448.0, image=self.images['metric_1'])
        
        self.images['metric_2'] = PhotoImage(file=relative_to_assets("image_17.png"))
        self.canvas.create_image(700.0, 448.0, image=self.images['metric_2'])
        
        self.images['metric_3'] = PhotoImage(file=relative_to_assets("image_18.png"))
        self.canvas.create_image(574.0, 448.0, image=self.images['metric_3'])
        
        self.images['metric_4'] = PhotoImage(file=relative_to_assets("image_19.png"))
        self.canvas.create_image(529.0, 448.0, image=self.images['metric_4'])
        
        self.images['metric_5'] = PhotoImage(file=relative_to_assets("image_20.png"))
        self.canvas.create_image(911.0, 448.0, image=self.images['metric_5'])
        
        self.images['metric_6'] = PhotoImage(file=relative_to_assets("image_21.png"))
        self.canvas.create_image(864.0, 448.0, image=self.images['metric_6'])
        
        self.images['metric_7'] = PhotoImage(file=relative_to_assets("image_22.png"))
        self.canvas.create_image(405.0, 448.0, image=self.images['metric_7'])
        
        self.images['metric_8'] = PhotoImage(file=relative_to_assets("image_23.png"))
        self.canvas.create_image(360.0, 448.0, image=self.images['metric_8'])
        
        self.images['decoration_1'] = PhotoImage(file=relative_to_assets("image_24.png"))
        self.canvas.create_image(152.0, 411.0, image=self.images['decoration_1'])
        
        self.images['decoration_2'] = PhotoImage(file=relative_to_assets("image_25.png"))
        self.canvas.create_image(98.0, 350.0, image=self.images['decoration_2'])
        
        self.images['decoration_3'] = PhotoImage(file=relative_to_assets("image_26.png"))
        self.canvas.create_image(901.0, 391.0, image=self.images['decoration_3'])
        
        self.images['decoration_4'] = PhotoImage(file=relative_to_assets("image_27.png"))
        self.canvas.create_image(388.0, 350.0, image=self.images['decoration_4'])
        
        self.images['decoration_5'] = PhotoImage(file=relative_to_assets("image_28.png"))
        self.canvas.create_image(566.0, 391.0, image=self.images['decoration_5'])
        
        self.images['decoration_6'] = PhotoImage(file=relative_to_assets("image_29.png"))
        self.canvas.create_image(396.0, 391.0, image=self.images['decoration_6'])
        
        self.images['icon_settings'] = PhotoImage(file=relative_to_assets("image_30.png"))
        self.canvas.create_image(830.0, 107.0, image=self.images['icon_settings'])
    
    def _create_entries(self):
        """Crée tous les champs de saisie"""
        # Entry 1 - Premier champ
        self.images['entry_bg_1'] = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(205.0, 102.22992515563965, image=self.images['entry_bg_1'])
        self.entries['field_1'] = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entries['field_1'].place(x=52.0, y=84.72262573242188, width=306.0, height=33.01459884643555)
        
        # Entry 2 - Deuxième champ
        self.images['entry_bg_2'] = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(668.0, 102.22992515563965, image=self.images['entry_bg_2'])
        self.entries['field_2'] = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entries['field_2'].place(x=515.0, y=84.72262573242188, width=306.0, height=33.01459884643555)
        
        # Entry 3 - Troisième champ
        self.images['entry_bg_3'] = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.canvas.create_image(205.0, 186.62409019470215, image=self.images['entry_bg_3'])
        self.entries['field_3'] = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entries['field_3'].place(x=52.0, y=169.11679077148438, width=306.0, height=33.01459884643555)
        
        # Entry 4 - Petit champ 1
        self.images['entry_bg_4'] = PhotoImage(file=relative_to_assets("entry_4.png"))
        self.canvas.create_image(67.05389785766602, 255.0, image=self.images['entry_bg_4'])
        self.entries['field_4'] = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entries['field_4'].place(x=53.624755859375, y=239.0, width=26.85828399658203, height=30.0)
        
        # Entry 5 - Petit champ 2
        self.images['entry_bg_5'] = PhotoImage(file=relative_to_assets("entry_5.png"))
        self.canvas.create_image(176.42914199829102, 256.0, image=self.images['entry_bg_5'])
        self.entries['field_5'] = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entries['field_5'].place(x=163.0, y=240.0, width=26.85828399658203, height=30.0)

    def _create_radiobuttons(self) -> None:
        """Crée les boutons radio pour la sélection du protocole."""
        # Callback pour notifier l'event handler du changement
        def on_protocol_change():
            if self.event_handler:
                self.event_handler.on_protocol_changed(self.protocol_var.get())

        # Radiobutton TCP (à gauche de image_10 / indicator_2)
        # Position de image_10: x=551.0, y=185.78831481933594
        self.radiobuttons['tcp'] = Radiobutton(
            self.window,
            variable=self.protocol_var,
            value="TCP",
            command=on_protocol_change,
            bg="#FFFFFF",
            fg="#000000",
            font=("Montserrat Medium", 12),
            selectcolor="#E0E0E0",
            activebackground="#FFFFFF",
            cursor="hand2"
        )
        self.radiobuttons['tcp'].place(x=480.0, y=175.0)

        # Radiobutton UDP (à gauche de image_12 / indicator_4)
        # Position de image_12: x=648.0, y=185.78831481933594
        self.radiobuttons['udp'] = Radiobutton(
            self.window,
            variable=self.protocol_var,
            value="UDP",
            command=on_protocol_change,
            bg="#FFFFFF",
            fg="#000000",
            font=("Montserrat Medium", 12),
            selectcolor="#E0E0E0",
            activebackground="#FFFFFF",
            cursor="hand2"
        )
        self.radiobuttons['udp'].place(x=575.0, y=175.0)
    
    def _create_buttons(self) -> None:
        """Crée tous les boutons avec leurs gestionnaires d'événements."""
        # Bouton 1 - Stop
        self.images['button_1'] = PhotoImage(
            file=relative_to_assets("button_1.png")
        )
        stop_command = (
            self.event_handler.on_stop_clicked
            if self.event_handler
            else lambda: print("Stop clicked")
        )
        self.buttons['stop'] = Button(
            self.window,
            image=self.images['button_1'],
            borderwidth=0,
            highlightthickness=0,
            command=stop_command,
            relief="flat",
            bg="#1E1E3F",
            activebackground="#1E1E3F",
            cursor="hand2"
        )
        self.buttons['stop'].place(x=148.0, y=389.0, width=89.0, height=69.0)

        # Bouton 2 - Start
        self.images['button_2'] = PhotoImage(
            file=relative_to_assets("button_2.png")
        )
        start_command = (
            self.event_handler.on_start_clicked
            if self.event_handler
            else lambda: print("Start clicked")
        )
        self.buttons['start'] = Button(
            self.window,
            image=self.images['button_2'],
            borderwidth=0,
            highlightthickness=0,
            command=start_command,
            relief="flat",
            bg="#1E1E3F",
            activebackground="#1E1E3F",
            cursor="hand2"
        )
        self.buttons['start'].place(x=30.0, y=389.0, width=96.0, height=74.0)
    
    def _create_text_elements(self) -> None:
        """Crée tous les éléments de texte (séparateurs, labels, etc.)."""
        # Séparateurs de métriques
        self.canvas.create_text(
            761.0, 438.0,
            anchor="nw",
            text="/",
            fill="#0021F5",
            font=("Montserrat SemiBold", 20)
        )

        self.canvas.create_text(
            593.0, 438.0,
            anchor="nw",
            text="/",
            fill="#F44336",
            font=("Montserrat SemiBold", 20)
        )

        self.canvas.create_text(
            930.0, 438.0,
            anchor="nw",
            text="/",
            fill="#000000",
            font=("Montserrat SemiBold", 20)
        )

        self.canvas.create_text(
            424.0, 438.0,
            anchor="nw",
            text="/",
            fill="#199E58",
            font=("Montserrat SemiBold", 20)
        )

    # Méthodes publiques pour accéder aux widgets
    def get_entry_value(self, field_name: str) -> str:
        """
        Récupère la valeur d'un champ de saisie.

        Args:
            field_name: Nom du champ à lire

        Returns:
            Valeur du champ ou chaîne vide si le champ n'existe pas
        """
        if field_name in self.entries:
            return self.entries[field_name].get()
        return ""

    def set_entry_value(self, field_name: str, value: str) -> None:
        """
        Définit la valeur d'un champ de saisie.

        Args:
            field_name: Nom du champ à modifier
            value: Nouvelle valeur à définir
        """
        if field_name in self.entries:
            self.entries[field_name].delete(0, 'end')
            self.entries[field_name].insert(0, value)

    def clear_all_entries(self) -> None:
        """Réinitialise tous les champs de saisie."""
        for field_name in self.entries:
            self.entries[field_name].delete(0, 'end')

    def get_protocol(self) -> str:
        """
        Récupère le protocole sélectionné (TCP ou UDP).

        Returns:
            Protocole sélectionné ("TCP" ou "UDP")
        """
        return self.protocol_var.get()

    def set_protocol(self, protocol: str) -> None:
        """
        Définit le protocole sélectionné.

        Args:
            protocol: Protocole à sélectionner ("TCP" ou "UDP")
        """
        if protocol in ["TCP", "UDP"]:
            self.protocol_var.set(protocol)

    def bind_event_handler(self, event_handler: object) -> None:
        """
        Associe l'event_handler et reconfigure les boutons.

        Cette méthode doit être appelée après la création de l'event_handler
        pour lier correctement les événements aux boutons.

        Args:
            event_handler: Instance de EventHandler à associer
        """
        self.event_handler = event_handler

        # Reconfigurer les boutons avec les vraies méthodes
        if 'start' in self.buttons:
            self.buttons['start'].config(
                command=self.event_handler.on_start_clicked
            )

        if 'stop' in self.buttons:
            self.buttons['stop'].config(
                command=self.event_handler.on_stop_clicked
            )

        print("[DEBUG] Event handler successfully bound to GUI")

    def run(self) -> None:
        """Lance la boucle principale de l'interface graphique."""
        self.window.mainloop()


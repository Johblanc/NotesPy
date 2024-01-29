from tkinter import Tk, PanedWindow
from tkinter.ttk import Style
from .Data import Folder
from .Part_B_Filtres import Filtres
from .Part_C_Arbre import Framelist
from .Part_D_Item import ItemPans
from .Part_A_Menu import Menubar

from .Style_Sheet import Setting


class Classeur(Tk):

    # ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__(self):
        """Ouverture de l'application"""
        super().__init__()

        self.settings = Setting(background="#000000",
                                foreground="#FFFFFF",
                                item_size=25,
                                item_space=5)
        self.menu_bar = Menubar(self)
        self.title(self.cur_path)
        self.config(menu=self.menu_bar, width=1200, height=800)
        self.style = Style(self)
        self.note_folder = Folder(self)  # LISTE DES NOTES

        self.pans = AppPans(self)  # SEPARATEUR DE FENETRE MOBILE
        self.pans.place(x=0, y=0, relwidth=1, relheight=1)
        self.new_folder()
        self.style_conf()
        self.configurator = None
        self.mainloop()

    def change_style(self, style_colo, style_ton, style_size):
        """Mise à jour des settings"""
        alt_a = "#880088"
        alt_b = "#888800"
        alt_c = "#448844"
        alt_d = "#884444"
        alt_e = "#008888"
        alt_f = "#444488"
        add = "#004400",
        sup = "#440000",
        if style_size == "Petit":
            sz, sp, fd = 20, 0, 20
        elif style_size == "Moyen":
            sz, sp, fd = 25, 5, 25
        else:
            sz, sp, fd = 30, 5, 25
        if style_colo == "Multi":
            if style_ton == "Claire":
                self.settings = Setting(item_size=sz,
                                        item_space=sp,
                                        fold_size=fd,
                                        fore_add=add,
                                        fore_sup=sup,
                                        fore_alt_a=alt_a,
                                        fore_alt_b=alt_b,
                                        fore_alt_c=alt_c,
                                        fore_alt_d=alt_d,
                                        fore_alt_e=alt_e,
                                        fore_alt_f=alt_f,
                                        back_info="#EEEEFF",
                                        fore_info="#000011",
                                        back_view="#FFDDFF",
                                        fore_view="#080008",
                                        back_list="#DDFFFF",
                                        fore_list="#000808",
                                        back_filt="#FFFFDD",
                                        fore_filt="#080800"
                                        )
            else:
                self.settings = Setting(item_size=sz,
                                        item_space=sp,
                                        fold_size=fd)

        else:
            if style_colo == "Gris":
                bg, fg = "#000000", "#FFFFFF"
            elif style_colo == "Bleu":
                bg, fg = "#000011", "#EEEEFF"
            elif style_colo == "Cyan":
                bg, fg = "#000808", "#DDFFFF"
            elif style_colo == "Vert":
                bg, fg = "#001100", "#EEFFEE"
            elif style_colo == "Jaune":
                bg, fg = "#080800", "#FFFFDD"
            elif style_colo == "Rouge":
                bg, fg = "#110000", "#FFEEEE"
            elif style_colo == "Magenta":
                bg, fg = "#080008", "#FFDDFF"

            if style_ton == "Claire":
                bg, fg = fg, bg
                self.settings = Setting(background=bg,
                                        foreground=fg,
                                        item_size=sz,
                                        item_space=sp,
                                        fold_size=fd,
                                        fore_add=add,
                                        fore_sup=sup,
                                        fore_alt_a=alt_a,
                                        fore_alt_b=alt_b,
                                        fore_alt_c=alt_c,
                                        fore_alt_d=alt_d,
                                        fore_alt_e=alt_e,
                                        fore_alt_f=alt_f)
            else:
                self.settings = Setting(background=bg,
                                        foreground=fg,
                                        item_size=sz,
                                        item_space=sp,
                                        fold_size=fd)

        self.style = Style(self)
        self.style_conf()
        self.list_box.fill_list()
        self.reader.config(self.settings["View"].reader)
        self.pans.new_sizing()

    def style_conf(self):
        """Mise à jour du Style"""
        for key, conf in self.settings.config.items():
            self.style.configure(key, **conf)
        for key, conf in self.settings.map.items():
            self.style.map(key, **conf)
        for key, conf in self.settings.options.items():
            self.option_add(key, conf)
        self.style.theme_use('alt')

    def new_folder(self):
        """Ouverture d'un nouveau Dossier"""
        self.title(self.cur_path)
        self.note_folder.fill_listing(self.cur_path)
        self.filtres.reset_for_new_folder(self.note_folder)
        self.info.reset_for_new_folder(self.note_folder)
        self.refresh_list()

    # ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    # ⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self

    @property
    def cur_path(self):
        """Nom du Dossier en cours de consultation"""
        return self.menu_bar.cur_path

    # ⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ FILTERSBOX
    @property
    def filtres(self):
        """Widget contenant les filtres (racourcie)"""
        return self.pans.filtres

    # ⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ FILTERSBOX
    @property
    def all_checks(self):
        """Ensemble des valeures possibles pour les CheckBoxes des Filtres"""
        return self.pans.filtres.all_checks

    def add_Check(self, _key: str, _value: str) -> None:
        """Ajout d'une nouvelle CheckBox dans les Filtres"""
        self.pans.filtres.add_Check(_key, _value)

    # ⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LISTBOX
    @property
    def list_box(self):
        """Widget affichant liste des Notes (racourcie)"""
        return self.pans.fr_list.list_box

    # ⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ INFO
    @property
    def info(self):
        """Widget affichant les détails de la Note sélectionnée (racourcie)"""
        return self.pans.item_pan.info

    @property
    def reader(self):
        """Widget affichant le contenu de la Note sélectionnée (racourcie)"""
        return self.pans.item_pan.viewer.txt

    @property
    def current_config(self):
        """La configuration par défaut des filtres pour le Dossier en cours (racourcie)"""
        return self.note_folder.current_config

    @property
    def sort_param(self):
        """Les parametres de classement issue des Filtres (racourcie)"""
        return self.filtres.sort_param

    def refresh_list(self, *arg, **kwarg):
        """Mise à jour du Treeview"""
        self.list_box.fill_list(self.filtres.filtring_folder(self.note_folder),
                                self.filtres.filters_param)

    def select_item(self, value):
        """Mise à jour de la sélection de la Note"""
        self.pans.item_pan.cur_id = value

    def change_folder_name(self, old_name, new_name):
        """Mise à jour du nom du Dossier en cours"""
        self.menu_bar.change_folder_name(old_name, new_name)


class AppPans(PanedWindow):
    def __init__(self, master):
        """Les Panneaux réglables de l'Application"""
        super().__init__(master)
        self.fr_list = Framelist(self)
        self.filtres = Filtres(self)
        self.item_pan = ItemPans(self)
        self.add(self.filtres, width=self.root.settings.item_size *
                 14, minsize=self.root.settings.fold_size)
        self.add(self.fr_list, width=self.root.settings.item_size *
                 14, minsize=self.root.settings.fold_size)
        self.add(self.item_pan, minsize=320)

    # ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    # ⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET

    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    def new_sizing(self):
        """Changement de taille de la fenêtre"""
        self.paneconfig(self.filtres, width=self.root.settings.item_size *
                        14, minsize=self.root.settings.fold_size)
        self.paneconfig(self.fr_list, width=self.root.settings.item_size *
                        14, minsize=self.root.settings.fold_size)
        self.fr_list.new_sizing()
        self.filtres.new_sizing()
        self.item_pan.new_sizing()

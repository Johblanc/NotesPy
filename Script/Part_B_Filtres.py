from tkinter import StringVar, IntVar
from tkinter.ttk import Combobox, Frame, Button, Entry, Label, Checkbutton
from .Data import Note

from datetime                       import datetime, timedelta
from .Data import Folder



#HTMLVIEW
class Filtres(Frame):
    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- INITIALISATION
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    def __init__(self, _master):
        """Widget permetant d'afficher des filtres au format texte, liste ou date"""
        super().__init__(_master,style="Filters.Fond.TFrame")
        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> CONFIGURATIONS DES FILTRES (ENTREES)
        #-'    '--'    '--'    '--'    '--'    '--'
        self.__conf: dict = {}          # Configuration courante des filtres
        self.__frames: Frame = []       # FiltresBoxes
        self.all_checks: dict = {}
        self.__cur_checks: dict = {}    # Dico des references pour les filtre au format liste

        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> PARAMETRAGES DES FILTRES (SORTIES)
        #-'    '--'    '--'    '--'    '--'    '--'
        self.__visi_lvl: int = 0        # Nombre de niveaux visible
        self.__tree_lvl: int = 0        # Nombre de niveaux pliant

        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> PLACEMENT DES FILTERBOXES
        #-'    '--'    '--'    '--'    '--'    '--'
        self.__offset = 0               # Decalage de la fenetre
        self.__frm_height = 0           # Hauteur de la fenetre
        self.__frm_width = 0            # Largeur de la fenetre

        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> PLIAGE DU VOLET FILTRES
        #-'    '--'    '--'    '--'    '--'    '--'
        self.__fold_false = "⇚\n\nF\n\nI\n\nL\n\nT\n\nR\n\nE\n\nS\n\n⇚"                # Texte du bouton si le volet est deplié
        self.__fold_true = "⇛\n\nF\n\nI\n\nL\n\nT\n\nR\n\nE\n\nS\n\n⇛"                 # Texte du bouton si le volet est plié
        fs = self.root.settings.fold_size
        self.__btn = Button( self,style="Filters.Pan.TButton", 
                            text=self.__fold_false, command=self.__switch_width) # Bouton permetant de plier / deplier
        self.__btn.place(relx=1, x=-fs, y=0, relheight=1, width=fs)                     # le volet
        self.bind("<MouseWheel>", self.scroll)
        self.bind("<Button-4>", self.scroll)
        self.bind("<Button-5>", self.scroll)
        self.bind("<Configure>", self.__on_Resize)                                      # Réaction au changement de dimention de
                                                                                        # la fenetre

    def new_sizing(self):
        """Le Style change de taille"""
        fs = self.root.settings.fold_size
        self.__btn.place(relx=1, x=-fs, y=0, relheight=1, width=fs)
        for frm in self.__frames:
            frm.new_sizing()
        self.reset_place()
    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- RACCOURCIS
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> LE PLUS HAUT WIDGET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- CONFIGURATIONS DES FILTRES (ENTREES)
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> CONFIGURATION COURANTE DES FILTRES
    #  '--'    '--'    '--'    '--'    '--'    '--'
    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> GET
    @property
    def conf(self) -> dict:
        """La configuration en cours"""
        return self.__conf

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> SET + REGLAGE DE L'AFFICHAGE
    @conf.setter
    def conf(self, _value: dict) -> None :
        """Réglage de la configuration des Filtres et met à jour l'affichage.\n
        La valeur doit être un dictionnaire.\n
        { param_1 : format_1, param_2 : format_2, ... , param_n : format_n }\n
        Les KEYS correspondent aux noms des parametres filtrables.\n
        Les VALUES sont les formats de données de ces derniers. "str" | "list" | "date"
        """
        self.__conf = _value
        
        while len(self.__frames) != 0 :
            b = self.__frames.pop(0)
            b.place_forget()
            del b

        i = 0
        for key in _value.keys():
            self.__frames.append(BoxFiltre(self, key, i,_value[key]))
            i +=1
        self.__frames[0].disable_Up()
        self.__frames[-1].disable_Down()
        self.reset_place()
    
    def reset_for_new_folder(self, _folder : Folder):
        """Selection d'un nouveau Dossier"""
        self.conf = _folder.current_config["format"]
        self.tree_lvl = _folder.current_config["tree"]
        self.visi_lvl = _folder.current_config["visi"]
        self.reset_all_checks()
        self.reset_cur_checks()
        for _note in _folder.listing :
            for _key in  self.__cur_checks.keys():
                if _note[_key] != [""]:
                    for _item in _note[_key]:
                        self.add_Check(_key,_item)


    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> AJOUT D'UNE NOUVELLE CHECKBOX
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def add_Check(self, _key : str, _value : str) -> None :
        """Ajout d'une checkbox à une filterbox si elle n'existe pas déjà"""
        if not _value in self.all_checks[_key] and _value != "":
            self.all_checks[_key].append(_value)
            self.__cur_checks[_key].append(_value)
            
            for frm in self.__frames:
                if frm.name == _key:
                    frm.l_add_Check(_value)
                    frm.l_verif_visibility(self.__cur_checks[_key])
                    break

    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- PARAMETRAGES DES FILTRES (SORTIES)
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> NOMBRE DE NIVEAUX VISIBLES
    #  '--'    '--'    '--'    '--'    '--'    '--'
    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> GET
    @property
    def visi_lvl(self) -> int:
        """Nombre de parametres visibles dans le TreeView"""
        return self.__visi_lvl

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> SET + REGLAGE DE L'AFFICHAGE
    @visi_lvl.setter
    def visi_lvl(self, _value: int) -> None:
        """Réglage de l'affiche des boutons de visibilité"""
        self.__visi_lvl = _value
        for frame in self.__frames:
            if frame.order > _value:
                frame.visi = False
            else:
                frame.visi = True
        if _value < self.tree_lvl:
            self.tree_lvl = _value

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> NOMBRE DE NIVEAUX HIERARCHISES
    #  '--'    '--'    '--'    '--'    '--'    '--'
    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> GET
    @property
    def tree_lvl(self) -> int:
        """Nombre de parametres hierarchisés dans le TreeView"""
        return self.__tree_lvl

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> SET + REGLAGE DE L'AFFICHAGE
    @tree_lvl.setter
    def tree_lvl(self, _value: int) -> None :
        """Réglage de l'affiche des boutons de hierarchisation"""
        self.__tree_lvl = _value
        for frame in self.__frames:
            if frame.order < _value:
                frame.tree = True
            else:
                frame.tree = False
        if _value > self.visi_lvl:
            self.visi_lvl = _value
            
    @property 
    def sort_param(self): 
        """Les Parametres de triage"""
        return [_frm.sort_param for _frm in self.__frames]

    @property 
    def filters_param(self): 
        """Les Parametres de filtrage"""
        return [_frm.filter_param for _frm in self.__frames]

    def filtring_folder(self,_folder : Folder): 
        """Crée une liste de parametres necéssaire à la création des ligne dans le Treeview"""
        def index(_path):
            if _path == "":
                return ""
            else:
                result = None
                for name, index in list_ascent:
                    if name == _path:
                        result = index
                        break
                return result

        def valid_path(_path : str):
            test = True
            i=0
            for _param in _path.split("#"):
                test = test and self.__frames[i].is_valid(_param)
                i += 1
            return test

        result = []
        list_ascent = []
        items_list = [[] for _ in range(self.tree_lvl +1)]

        self.reset_cur_checks()
        for i in range(len(self.__frames)-1,-1,-1):
            _folder.listing.sort(key=lambda _note : _note[self.__frames[i].name],reverse=self.__frames[i].sort_revers)
        for note in _folder.listing:  # AJOUT DES ITEMS
            if self.is_OK(note):
                values = note.values[self.tree_lvl+1:]
                temp = note.tree_values(self.__frames[self.tree_lvl].name)
                for (asc, path, name, frt) in temp:
                    if valid_path(path):
                        items_list[len(path.split("#"))-1].append((asc, path, name, frt,note["Id"],values))
                        
        param = self.filters_param
        for i in range(len(items_list)):
            items_list[i].sort(reverse=param[i]["revers"])


        i = 0
        for listing in items_list:
            for (asc, path, name, frt, id, val) in listing:
                if frt == "t":
                    if index(path) is None:
                        result.append({"parent" : index(asc), "index" :"end","text":name,"iid":i,
                            "open":True,"tags":[name,"Nv_" + str(len(path.split("#")))]})
                        list_ascent.append((path, i))
                        i += 1
                else:
                    if len(val) == 0:
                        result.append({"parent" : index(asc), "index" :"end","text":name,"iid":i,
                            "tags":[id, "data"]})
                    else:
                        result.append({"parent" : index(asc), "index" :"end","text":name,"iid":i,
                            "values":val,"tags":[id, "data"]})
                    i += 1
        self.verif_visibility()
        return result


    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> INVERSION DE L'ORDRE DE DEUX PARAMETRES
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def switch(self, _num_A : int, _num_B : int) -> None :
        """Inverse la position de deux filterboxes"""
        self.__frames[_num_A].enable_all()    
        self.__frames[_num_B].enable_all()
        self.__frames[_num_A], self.__frames[_num_B] = self.__frames[_num_B], self.__frames[_num_A]
        self.__frames[_num_A].order, self.__frames[_num_B].order = self.__frames[_num_B].order, self.__frames[_num_A].order
        self.__frames[0].disable_Up()
        self.__frames[-1].disable_Down()
        self.visi_lvl = self.visi_lvl
        self.tree_lvl = self.tree_lvl
        self.reset_place()
        self.root.refresh_list()

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> VALIDATION DES NOTES + REMPLISSAGE Dself.root.settings.ico VISI
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def is_OK(self, note : Note) -> bool:
        """Cette note passe-t-elle les filtres en cours"""
        result = True
        for frm in self.__frames:
            if frm.name in set(self.__cur_checks):
                for item in note[frm.name]:
                    if not item in self.__cur_checks[frm.name] and item != "":
                        self.__cur_checks[frm.name].append(item)
            result = result and frm.is_OK(note)
            if not result: break
        return result


    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- PLACEMENT DES FILTERBOXES
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> CORRECTION DU PLACEMENT DES FILTERBOXES
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def reset_place(self) -> None :
        """Correction du placement des filterboxes en fonction de l'offset et des animations en cours"""
        if self.hauteur <= self.__frm_height:
            self.__offset = 0
        elif self.__offset < self.__frm_height - self.hauteur:
            self.__offset = self.__frm_height - self.hauteur
        sp = self.root.settings.item_space
        fs = self.root.settings.fold_size

        h = int(self.__offset) + sp
        transition = False
        for i in range(len(self.__frames)):
            self.__frames[i].place(x=sp, y=h, relwidth=1,  width=-fs - 2 * sp, height=self.__frames[i].hauteur)
            if self.__frames[i].fold_transition:
                self.__frames[i].update_hauteur()
                transition = True
            h += self.__frames[i].hauteur + sp
        if transition: self.after(self.root.settings.anim_delay, self.reset_place)
    
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> MODIFICATION DE L'OFFSET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def scroll(self, _event = None) -> None :
        """Réaction à un event de scrolling. Modifiction de .__offset"""
        mouv = "UP"
        if _event.num:
            if _event.num == 4:
                mouv = "Down"
        if _event.delta:
            if int(_event.delta) > 0:
                mouv = "Down"
        if self.hauteur > self.__frm_height:
            min___offset = self.__frm_height - self.hauteur
            if mouv == "UP":
                self.__offset -= self.root.settings.scroll_step
                if self.__offset < min___offset: self.__offset = min___offset
            else:
                self.__offset += self.root.settings.scroll_step
                if self.__offset > 0: self.__offset = 0
        self.reset_place()

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> HAUTEUR DU WIDGET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def hauteur(self) -> int :
        """Hauteur totale des filterboxes"""
        result = self.root.settings.item_space
        for frm in self.__frames:
            result += frm.hauteur + self.root.settings.item_space
        return result


    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> VERIFICATION DES CHECKBOXES VISIBLES
    #  '--'    '--'    '--'    '--'    '--'    '--'

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> R-A-Z Dself.root.settings.ico VISI
    def reset_cur_checks(self) -> None :
        """Mise à zero des CheckBoxes visibles"""
        self.__cur_checks = {item["name"]: [] for item in self.sort_param if item["format"] == "list"}
    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> R-A-Z Dself.root.settings.ico VISI
    def reset_all_checks(self) -> None :
        """Mise à zero des CheckBoxes possibles"""
        self.all_checks = {item["name"]: [] for item in self.sort_param if item["format"] == "list"}

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> M-A-J D'AFFICHAGE DES CHECKBOXES
    def verif_visibility(self) -> None :
        """Vérification de la visibilité de chaque checkbox"""
        
        for frm in self.__frames:
            if type(frm.val) == type(list()):
                frm.l_verif_visibility(self.__cur_checks[frm.name])
        self.reset_place()

    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- PLIAGE DU VOLET FILTRES
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> ACTION SUR LE BOUTON DE PLIAGE
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def __switch_width(self) -> None :
        """Plie le volet si il est déplié en vise versa"""
        if self.__btn.cget("text") == self.__fold_false:
            self.__btn.config(text=self.__fold_true)
            self.master.paneconfig(self, width=self.root.settings.fold_size)
        else:
            self.__btn.config(text=self.__fold_false)
            self.master.paneconfig(self, width=self.root.settings.item_size * 14)

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> REACTION AU CHANGEMENT DE TAILLE DU VOLET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def __on_Resize(self, _event=None) -> None :
        """Réaction au redimentionnement de la fenetre"""
        if _event:
            self.__frm_height = int(_event.height)
            self.__frm_width = int(_event.width)
        else:
            self.__frm_width = self.root.settings.item_size * 14

        if self.__frm_width > self.root.settings.item_size * 10:
            self.__with_options()
        elif self.__frm_width > self.root.settings.fold_size:
            self.__no_option()
        else:
            self.__no_filter()

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> MODE D'AFFICHAGE DES FILTERBOXES
    #  '--'    '--'    '--'    '--'    '--'    '--'
    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> FILTRES + OPTIONS
    def __with_options(self) -> None :
        """Affichage des filtres avec options"""
        self.__btn.config(text=self.__fold_false)
        for frm in self.__frames:
            frm.with_options()
        self.reset_place()

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> FILTRES SEULEMENT
    def __no_option(self) -> None :
        """Affichage des filtres sans options"""
        self.__btn.config(text=self.__fold_false)
        for frm in self.__frames:
            frm.no_option()
        self.reset_place()

    #-""-,__,-""-,__,-""-,__,-""-,__,-""-,__,--> PAS DE FILTRES
    def __no_filter(self) -> None :
        """Masquage des filtres"""
        self.__btn.config(text=self.__fold_true)
        for frm in self.__frames:
            frm.place_forget()

    

class BoxFiltre(Frame):
    
    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- INITIALISATION
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    def __init__(self, _master , _name, _order,_format):
        """Widget permetant d'afficher un filtres au format texte, liste ou date"""
        super().__init__(_master,style="Filters.Box.TFrame")
        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> PARAMETES DU FILTRE (SORTIE)
        #-'    '--'    '--'    '--'    '--'    '--'
        self.name = _name                                           # Nom du filtre
        self.__btn_Tree = Button(self,text = self.root.settings.ico["donnee"],         # Bouton hierarchie / donnée
                            command=self.toggle_tree,style="Filters.Box.Data.TButton")
        self.__btn_Visi = Button(self,text = self.root.settings.ico["visible"],        # Bouton visible / masqué
                            command=self.toggle_visi,style="Filters.Box.Visi.TButton")
        self.__btn_Sort = Button(self,text = self.root.settings.ico["croissant"],      # Bouton tri montant / descendant
                            command=self.toggle_sort_revers,style="Filters.Box.Sort.TButton")
        self.order = _order                                         # Ordre d'affichage
        self.__btn_Up = Button(self,text = self.root.settings.ico["monter"],           # Bouton monté
                            command=self.move_up,style="Filters.Box.Move.TButton")
        self.__btn_Dw = Button(self,text = self.root.settings.ico["descendre"],        # Bouton descendre
                            command=self.move_down,style="Filters.Box.Move.TButton")
        self.__format = _format                                       # Format de la donnée
        
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        if _format == "list":
            self.__l_val_list = []                # LISTE DES VALEURS Possibles
            self.__l_visi_list = []               # LISTE DES VALEURS VISIBLES
            self.__l_var_Type = {}                # LISTE DES VARIABLES DES CHECKBOXES
            self.__l_chBs_Type = []               # LISTE DES CHECKBOXES
        elif _format == "str":
            self.__s_var = StringVar()                                  # VALEUR DE L'ENTRYBOX
            self.__s_entry = Entry(self, textvariable=self.__s_var,style="Filters.Box.TEntry")
            self.__s_var.trace_add('write', self.root.refresh_list)
            self.__s_entry.place(x=sp,y=2*sp + sz , height = sz , relwidth = 1, width = -2*sp)
        elif _format == "date":
            self.__d_box = DateFilters(self)
            self.__d_box.place(x=sp,y=2*sp + sz , height = sz , relwidth = 1, width = -2*sp)

        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> PLIAGE DU FILTRE
        #-'    '--'    '--'    '--'    '--'    '--'
        self.__fold = False                                         # Le nemu est-il plié ?
        self.hauteur = 0                                            # Hauteur du filtre
        self.__label = Label(self, text = self.name.upper(),style="Filters.Box.TLabel")                           # Titre du filtre + bouton pliage
        self.__label.bind("<ButtonRelease-1>", self.toggle_fold)
        self.with_options()
        
        #  ,--,    ,--,    ,--,    ,--,    ,--,    ,--> SCROLLING EVENT
        #-'    '--'    '--'    '--'    '--'    '--'
        self.bind("<MouseWheel>", self.master.scroll)
        self.bind("<Button-4>", self.master.scroll)
        self.bind("<Button-5>", self.master.scroll)
        self.__label.bind("<MouseWheel>", self.master.scroll)
        self.__label.bind("<Button-4>", self.master.scroll)
        self.__label.bind("<Button-5>", self.master.scroll)
        
        if _format == "str":
            self.__s_entry.bind("<MouseWheel>", self.master.scroll)
            self.__s_entry.bind("<Button-4>", self.master.scroll)
            self.__s_entry.bind("<Button-5>", self.master.scroll)
        elif _format == "date":
            self.__d_box.bind("<MouseWheel>", self.master.scroll)
            self.__d_box.bind("<Button-4>", self.master.scroll)
            self.__d_box.bind("<Button-5>", self.master.scroll)
        
    def new_sizing(self):
        """Le Style change de taille"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        if self.__format == "list":
            self.l_verif_visibility()
        elif self.__format == "str":
            self.__s_entry.place(x=sp,y=2*sp + sz , height = sz , relwidth = 1, width = -2*sp)
        elif self.__format == "date":
            self.__d_box.place(x=sp,y=2*sp + sz , height = sz , relwidth = 1, width = -2*sp)
            self.__d_box.change_mode()
        self.with_options()
    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- RACCOURCIS
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> LE PLUS HAUT WIDGET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def root(self) -> object:
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

            
    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- PROPRIETES ET METHODES LIEES AU PLIAGE DU FILTRE
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EST TRIE EN REVERS DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ GET
    @property
    def sort_revers(self):
        """L'ordre de triage pour ce parametre"""
        return self.__btn_Sort.cget("text") == self.root.settings.ico["decroissant"]

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EVENT
    def toggle_sort_revers(self):
        """Inversion de l'ordre de triage pour ce parametre"""
        if self.sort_revers :
            self.__btn_Sort.config(text=self.root.settings.ico["croissant"])
        else:
            self.__btn_Sort.config(text=self.root.settings.ico["decroissant"])
        self.root.refresh_list()
        
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ PRESENCE DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ GET
    @property
    def visi(self):
        """Le parametre est-il visible dans le Treeview"""
        return self.__btn_Visi.cget("text") == self.root.settings.ico["visible"]

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ SET
    @visi.setter
    def visi(self, value):
        """Réglage de la visibilité dans le Treeview"""
        if value : 
            self.__btn_Visi.config(text= self.root.settings.ico["visible"],style="Filters.Box.Visi.TButton")
        else :
            self.__btn_Visi.config(text= self.root.settings.ico["invisible"],style="Filters.Box.Not_Visi.TButton")

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EVENT
    def toggle_visi(self):
        """Inversion du réglage de visibilité dans le Treeview"""
        self.master.visi_lvl = self.order
        self.root.refresh_list()
        
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EST UN DOSSIER OU UNE DONNEE DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ GET
    @property
    def tree(self):
        """Le parametre est-il une donné ou un élément hierarchisé dans le Treeview"""
        return self.__btn_Tree.cget("text") == self.root.settings.ico["dossier"]

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ SET
    @tree.setter
    def tree(self, value):
        """Réglage du niveau de hierarchisation pour ce parametre"""
        if value : 
            self.__btn_Tree.config(text= self.root.settings.ico["dossier"],style="Filters.Box.Tree.TButton")
        else :
            self.__btn_Tree.config(text= self.root.settings.ico["donnee"],style="Filters.Box.Data.TButton")

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EVENT
    def toggle_tree(self):
        """Inversion du réglage de la hierarchisation dans le Treeview"""
        self.master.tree_lvl = self.order
        self.root.refresh_list()

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ POSITION DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ REMONTER DANS LA HIERARCHIE
    def move_up(self):
        """Déplacer ce parametre vers le haut"""
        self.master.switch(self.order,self.order-1)

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ DESCENDRE DANS LA HIERARCHIE
    def move_down(self):
        """Déplacer ce parametre vers le bas"""
        self.master.switch(self.order,self.order+1)
    
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ RENDRE ACTIF LES DEUX BOUTONS
    def enable_all(self):
        """Active les Bouton de réglage de l'ordre du parametre"""
        self.__btn_Up.config(state ="normal")
        self.__btn_Dw.config(state ="normal")

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ RENDRE INACTIF LE BOUTON UP
    def disable_Up(self):
        """Désecative le Bouton de monté"""
        self.__btn_Up.config(state ="disabled")

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ RENDRE INACTIF LE BOUTON DOWN
    def disable_Down(self):
        """Désecative le Bouton de descente"""
        self.__btn_Dw.config(state ="disabled")

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ VALIDATION DES DONNEES ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ VALEUR DU FILTRE
    @property
    def val(self):
        """Valeur valide pour ce parametre"""
        if self.__format == "list":
            test = True
            result = []
            for ref, val in self.__l_var_Type.items():
                if val.get():
                    result.append(ref)
                    test = False
            if test : 
                return self.__l_val_list + [""]
            else :
                return result
        elif self.__format == "str":
            return self.__s_var.get()
        else:
            return None

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ PARAMETRES DU FILTRE
    @property
    def sort_param(self):
        """Les paramametres de Trie pour ce Filtre"""
        return {
            "name" : self.name,
            "format" : self.__format,
            "revers" : self.sort_revers
            }

    @property
    def filter_param(self):
        """Les paramametres de Filtrage pour ce Filtre"""
        return {
            "name" : self.name,
            "format" : self.__format,
            "order" : self.order,
            "revers" : self.sort_revers,
            "visi" : self.visi,
            "tree" : self.tree,
            "val" : self.val
            }

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LA DONNEE EST-ELLE VALIDE
    def is_OK(self, ref ):
        """La Note est-elle valide ?"""
        if self.__format == "list":
            if self.val == []:
                return True
            else:
                test = False
                for item in ref[self.name]:
                    if not item in self.__l_val_list : 
                        if item != "" :self.l_add_Check(item)
                    if item in self.val : test = True
                return test
        elif self.__format == "date":
            ref_date = datetime(
                ref[self.name]["annee"],
                ref[self.name]["mois"],
                ref[self.name]["jour"],
                ref[self.name]["heure"],
                ref[self.name]["minute"],
                ref[self.name]["seconde"])
            return self.__d_box.is_OK(ref_date)
        elif self.__format == "str":
            return self.val == "" or self.val in ref[self.name]
        else:
            return True

    def is_valid(self, value):
        """La Valeur est-elle valide ?"""
        if self.__format == "list":
            if self.val == []:
                return True
            else:
                return value in self.val
        elif self.__format == "date":
            return True
        elif self.__format == "str":
            return self.val == "" or self.val in value
        else:
            return True





    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ AFFICHAGE DES BOUTON ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ AVEC BOUTONS
    def with_options(self):
        """Activation des Options"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.__label.place(x=sp,y=sp, height = sz, relwidth = 1, width = -5*sz -2*sp)
        self.__btn_Tree.place(relx=1,x=-5*sz-sp,y=sp, height = sz, width = sz)
        self.__btn_Visi.place(relx=1,x=-4*sz-sp,y=sp, height = sz, width = sz)
        self.__btn_Sort.place(relx=1,x=-3*sz-sp,y=sp, height = sz, width = sz)
        self.__btn_Up.place(relx=1,x=-2*sz-sp,y=sp, height = sz, width = sz)
        self.__btn_Dw.place(relx=1,x=-sz-sp,y=sp, height = sz, width = sz)

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ SANS BOUTONS
    def no_option(self):
        """Désactivation des Options"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.__label.place(x=sp,y=sp, height = sz, relwidth = 1, width = -2*sp)
        self.__btn_Tree.place_forget()
        self.__btn_Visi.place_forget()
        self.__btn_Sort.place_forget()
        self.__btn_Up.place_forget()
        self.__btn_Dw.place_forget()

    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- PLIAGE DU FILTRE
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> SWITCHER L'ETAT DU PLIAGE
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def toggle_fold(self,event):
        """Inversion du pliage du Volet Filtre"""
        self.__fold = not self.__fold
        self.master.reset_place()

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> HAUTEUR A ATTEINDRE (Animation)
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def __hauteur_cible(self):
        """Hauteur à atteindre lors des animations"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        if self.__format == "list":
            f = sz + 2 * sp 
            u = sz * (len(self.__l_visi_list)+1) + 3 * sp
            return f if self.__fold else u
        elif self.__format == "date":
            return (sz+2*sp) + (not self.__fold) * (self.__d_box.hauteur+sp)
        else:
            return (sz+sp) * ((not self.__fold)+1)+sp

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> HAUTEUR CIBLE ATTEINTE (Animation)
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def fold_transition(self)->bool:
        """L'animation est-elle en cours ?"""
        return self.hauteur != self.__hauteur_cible

    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> MISE A JOUR DE LA HAUTEUR (Animation)
    #  '--'    '--'    '--'    '--'    '--'    '--'
    def update_hauteur(self):
        """Mise à jour de la hauteur de la Box si la hauteur cible n'est pas atteinte"""
        if self.hauteur < self.__hauteur_cible:
            self.hauteur += self.root.settings.anim_step
            if self.hauteur > self.__hauteur_cible :self.hauteur = self.__hauteur_cible
        elif self.hauteur > self.__hauteur_cible:
            self.hauteur -= self.root.settings.anim_step
            if self.hauteur < self.__hauteur_cible :self.hauteur = self.__hauteur_cible

    def l_add_Check(self,value):
        """Ajout d'une CheckBox"""
        if self.__format == "list" and value != "":
            self.__l_val_list.append(value)
            self.__l_visi_list.append(value)
            self.__l_var_Type[value] = IntVar()
            self.__l_chBs_Type.append(Checkbutton(self, text=value, variable=self.__l_var_Type[value], 
                                            command=self.root.refresh_list,style="Filters.Box.TCheckbutton"))
            self.__l_chBs_Type[-1].bind("<MouseWheel>", self.master.scroll)
            self.__l_chBs_Type[-1].bind("<Button-4>", self.master.scroll)
            self.__l_chBs_Type[-1].bind("<Button-5>", self.master.scroll)
            self.__l_chBs_Type.sort(key= lambda _ch : _ch.cget("text"))

    def l_sup_Check(self,value):
        """Suppression d'une CheckBox"""
        if self.__format == "list":
            self.__l_val_list.remove(value)
            self.__l_visi_list.remove(value)
            for i in range(len(self.__l_chBs_Type)) :
                if self.__l_chBs_Type[i].cget("text") == value :
                    sup = self.__l_chBs_Type.pop(i)
                    sup.place_forget()
                    del sup
                    del self.var_Type[value]
                    
    def l_verif_visibility(self,_visi_list = None):
        """Vérification de la visibilité de chaque CheckBoxes"""
        if self.__format == "list":
            sz = self.root.settings.item_size
            sp = self.root.settings.item_space
            if _visi_list : self.__l_visi_list = list(_visi_list)
            i = 1
            for cb in self.__l_chBs_Type :
                if cb.cget("text") in self.__l_visi_list :
                    cb.place(x=sp,y=2*sp + sz * i, height = sz , relwidth = 1, width = -2*sp)
                    i+=1
                else:
                    self.__l_var_Type[cb.cget("text")].set(0)
                    cb.place_forget()





class DateFilters(Frame):
    def __init__(self, master) -> None:
        """Widget de filtrer des dates"""
        super().__init__(master, style="Filters.Box.Sub.TFrame")
        self.__mode = Combobox( self,
                                values=["Aucun filtre","Le","Depuis le","Avant le","Entre le"],
                                state="readonly",
                                style="Filters.Box.TCombobox")
        self.__mode.current(0)
        self.__deb = DateBox(self)
        self.__fin = DateBox(self)
        self.__mode.place(x=0,y=0 , height = self.root.settings.item_size , width = 4*self.root.settings.item_size)
        self.__mode.bind("<<ComboboxSelected>>", self.change_mode)

    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- RACCOURCIS
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> LE PLUS HAUT WIDGET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    def change_mode(self,event=None):
        """Réglage de l'affichage en fonction du mode de filtrage"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.__mode.place(x=0,y=0 , height = sz , width = 4*sz)
        if self.__mode.current() == 0 :
            self.__deb.place_forget()
            self.__fin.place_forget()
            self.place(x=sp,y=2*sp + sz , height = sz , relwidth = 1, width = -2*sp)
        elif self.__mode.current() == 4 :
            self.__deb.place(x=4*sz+sp,y=0 , height = sz , relwidth = 1, width = -(4*sz+sp))
            self.__fin.place(x=4*sz+sp,y=sz , height = sz , relwidth = 1, width = -(4*sz+sp))
            self.place(x=sp,y=2*sp + sz , height = 2*sz , relwidth = 1, width = -2*sp)
        else:
            self.__deb.place(x=4*sz+sp,y=0 , height = sz , relwidth = 1, width = -(4*sz+sp))
            self.__fin.place_forget()
            self.place(x=sp,y=2*sp + sz , height = sz , relwidth = 1, width = -2*sp)
        self.root.refresh_list()

    @property
    def hauteur(self):
        """Hauteur du Widget"""
        sz = self.root.settings.item_size
        return sz if self.__mode.current() != 4 else 2*sz

    def is_OK(self, ref :datetime ):
        """La valeur est-elle valide"""
        if self.__mode.current() == 0 :     # "Aucun filtre"
            return True 
        elif self.__mode.current() == 1 :   # "Le"
            return self.__deb.current_date <= ref <= self.__deb.current_date + timedelta(days=1)
        elif self.__mode.current() == 2 :   # "Depuis le"
            return self.__deb.current_date <= ref
        elif self.__mode.current() == 3 :   # "Avant le"
            return ref <= self.__deb.current_date + timedelta(days=1)
        else :                              # "Entre le"
            return self.__deb.current_date <= ref <= self.__fin.current_date + timedelta(days=1)

                    
class DateBox(Frame):

    def __init__(self, master) -> None:
        """Widget de réglage pour une date"""
        super().__init__(master)

        self.__yearbox = Combobox( self, 
                                 values=[y for y in range(2022, datetime.now().year + 1)],
                                 state="readonly",
                                 style="Filters.Box.TCombobox")
        self.__monthbox = Combobox(self,
                                 values=[ "Janvier", "Fervrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre" ],
                                 state="readonly",
                                 style="Filters.Box.TCombobox")
        self.__daybox = Combobox(  self, 
                                 values=[d for d in range(1, 32)],
                                 state="readonly",
                                 style="Filters.Box.TCombobox")

        self.__daybox.place(relx=0, y=0, relwidth=0.2, relheight=1)
        self.__monthbox.place(relx=0.2, y=0, relwidth=0.5, relheight=1)
        self.__yearbox.place(relx=0.7, y=0, relwidth=0.3, relheight=1)

        self.__yearbox.current(len(self.__yearbox.cget("values")) - 1)
        self.__monthbox.current(datetime.now().month - 1)
        self.__daybox.current(datetime.now().day - 1)
        self.__month_is_changing(is_init = True)

        self.__yearbox.bind("<<ComboboxSelected>>", self.__month_is_changing)
        self.__monthbox.bind("<<ComboboxSelected>>", self.__month_is_changing)
        self.__daybox.bind("<<ComboboxSelected>>", self.__is_changing)
    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- RACCOURCIS
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> LE PLUS HAUT WIDGET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    def __is_changing(self, event=None):
        """La date selectionnée change"""
        self.root.refresh_list()

    def __month_is_changing(self, event=None, is_init = False):
        """La mois (ou l'année) selectionné(e) change"""
        day_index = self.__daybox.current()

        if self.__monthbox.current() == 1:
            if int(self.__yearbox.get()) % 4 == 0:
                self.__daybox.config(values=[d for d in range(1, 30)])
                max_index = 28
            else:
                self.__daybox.config(values=[d for d in range(1, 29)])
                max_index = 27
        elif self.__monthbox.current() in [3, 5, 8, 10]:
            self.__daybox.config(values=[d for d in range(1, 31)])
            max_index = 29
        else:
            self.__daybox.config(values=[d for d in range(1, 32)])
            max_index = 30

        if day_index < 0: day_index = 0
        if day_index > max_index: day_index = max_index

        self.__daybox.current(day_index)
        if not is_init : self.__is_changing()

    @property
    def current_date(self):
        """Date en cours"""
        return datetime(int(self.__yearbox.get()), self.__monthbox.current() + 1, int(self.__daybox.get()), 0, 0, 0)

    @current_date.setter
    def current_date(self, value: datetime):
        """Réglage de la date en cours"""
        self.__yearbox.current(int(value.year) - 2022)
        self.__monthbox.current(value.month - 1)
        self.__daybox.current(value.day - 1)


from tkinter                        import PanedWindow, Text
from tkinter.ttk                    import Style, Button, Frame, Combobox, Label, Entry
from .Data        import Folder

FORMAT = ["Texte brute", "Markdown", "Carte"]

class ItemPans(PanedWindow):
    """Pannaux réglables contenent les details de l'item selectionné"""
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__(self, master):
        super().__init__(master,orient="vertical",relief="solid",background="#DDDDEE",borderwidth=0)
        self.hauteur = 0
        self.__cur_id = None
        self.__cur_note = None
        self.info = Info(self)
        self.viewer = Viewer(self)
        self.add(self.viewer,minsize = 700)
        self.add(self.info,height = self.info.hauteur_max, minsize = self.root.settings.fold_size)
        self.bind("<Configure>",self.__on_Resize)

    def new_sizing(self):
        self.info.new_sizing()
        self.viewer.on_Resize()

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Le Widget de plus haut niveau"""
        return self.master.root

    @property
    def cur_id(self):
        return self.__cur_id

    @cur_id.setter
    def cur_id(self,value):
        self.__cur_id = value
        if value :
            for note in self.root.note_folder.listing :
                if note["Id"] == value :
                    self.__cur_note = note
                    break
            else : self.__cur_note = None
        else : self.__cur_note = None
        self.set_mode("Modification")
        self.viewer.set_cur_note(self.__cur_note)
        self.info.set_cur_note(self.__cur_note)

    @property
    def cur_note(self):
        return self.__cur_note


    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ REGLAGES ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ CONSULTATION / MODIFICATION
    def set_mode(self,value):
        """permet le passage d'un mode à l'autre.  "consultation" ou "modification" """
        self.viewer.set_mode(value)
        self.info.set_mode(value)

    def __on_Resize(self,event = None):
        self.hauteur = event.height
        if self.info.fold :
            self.fold()
        else:
            self.unfold()
        

    def unfold(self):
        self.paneconfig(self.viewer,minsize = self.hauteur - self.info.hauteur_max, height = self.hauteur - self.info.hauteur_max)
        self.paneconfig(self.info,height = self.info.hauteur_max)

    def fold(self):
        self.paneconfig(self.viewer,minsize = self.hauteur - self.info.hauteur_max, height = self.hauteur - self.root.settings.fold_size)
        self.paneconfig(self.info,height = self.root.settings.fold_size)

    def note_changer(self,key,value):
        """Permet d'enregistrer une modifiction sur un item"""
        self.__cur_note[key] = value
        self.__cur_note.ecrire_json()
        self.root.refresh_list()


        

class Info(Frame):
    """Un Widget permetant d'afficher et de modifier les details d'un item"""
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__(self, master):
        super().__init__(master,style="Info.Fond.TFrame")
        self.boxes = []
        self.cur_note = ""
        self.hauteur_max = self.root.settings.fold_size
        self.__fold_false = "⇓  D E T A I L S  ⇓"                # Texte du bouton si le volet est deplié
        self.__fold_true = "⇑  D E T A I L S  ⇑"                 # Texte du bouton si le volet est plié
        self.btn = Button(self,text= self.__fold_false,style="Info.Pan.TButton",command=self.switch_width)
        self.btn.place(x=0,y=0, height = self.root.settings.fold_size, relwidth = 1)
        self.bind("<Configure>",self.on_Resize)

        self.style = Style(self.root)
        self.style.theme_use('alt')

    def new_sizing(self):
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        fs = self.root.settings.fold_size
        self.btn.place(x=0,y=0, height = fs, relwidth = 1)
        self.hauteur_max = sp + fs
        for box in self.boxes:
            box.new_sizing()
            box.place(x=sp,y=self.hauteur_max,height=sz,relwidth=1,width = -2*sp)
            self.hauteur_max+=sz + sp
    @property
    def fold(self) -> object:
        """Le Widget est-il plié"""
        return self.btn.cget("text") == self.__fold_true

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Le Widget de plus haut niveau"""
        return self.master.root

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EVENEMENTIEL ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ REDIMENTIONNEMENT DE LA FENETRE
    def on_Resize(self, event=None):
        """Lors du redimentinnement de la fenetre"""
        if event                    : frm_height = int(event.height)
        else                        : frm_height = self.hauteur_max
        if frm_height > self.root.settings.fold_size   : self.btn.config(text= self.__fold_false )
        else                        : self.btn.config(text= self.__fold_true )
        
            

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ ACTION SUR LE BOUTON DE REDIMENTIONNEMENT
    def switch_width(self):
        """Permet de plier / deplier les détails de l'item"""
        
        if self.btn.cget("text") == self.__fold_false :
            self.btn.config(text= self.__fold_true )
            self.master.fold()
        else:
            self.btn.config(text= self.__fold_false )
            self.master.unfold()

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ AFFICHAGE ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ AJOUT DES WIDJETS ENFANTS
    def reset_for_new_folder(self, _folder : Folder):
        """Création d'un Widjet pour chaque parametre à afficher"""

        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        fs = self.root.settings.fold_size
        while len(self.boxes) != 0 :
            b = self.boxes.pop(0)
            b.place_forget()
            del b
        self.hauteur_max = sp + fs
        for key in _folder.current_config["format"].keys():
            if not key in ["Contenu", "Format", "Id", "Cr\u00e9\u00e9e le", "Modifi\u00e9e le", "liaisons","Titre"]:
                self.boxes.append(Box_Info(self))
                self.boxes[-1].name = key
                self.boxes[-1].val = ""
                self.boxes[-1].place(x=sp,y=self.hauteur_max,height=sz,relwidth=1,width = -2*sp)
                self.hauteur_max+=sz + sp
        
        self.master.unfold()
        self.on_Resize()

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EN FONCTION DE L'ITEM
    def set_cur_note(self,value):
        """Reglage de la note à afficher"""
        self.set_mode("Modification")
        if value: 
            for box in self.boxes: 
                box.val = value[box.name]
        else:
            for box in self.boxes:
                box.val = ""

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EN FONCTION DU MODE
    def set_mode(self,value):
        """Reglage du mode de travail. "Modification" ou "Consultation" """
        for box in self.boxes :
            box.mode = value


 

class Box_Info(Frame):
    """Un Widget permetant d'afficher et de modifier un parametre d'un item"""
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__(self, master):
        super().__init__(master,style="Info.Fond.TFrame")
        self.__cur_val = ""
        self.__mode = ""
        self.__name = ""

        self.lab_name   = Label(self,style="Info.Name.TLabel")
        self.lab_val    = Label(self,style="Info.Val.TLabel")
        self.cb_add     = Combobox(self,style="Info.Add.TCombobox")
        self.bn_add     = Button(self,text="+",style="Info.Add.TButton",state="disable",command=self.add_item)
        self.cb_sup     = Combobox(self,style="Info.Sup.TCombobox",state="readonly")
        self.bn_sup     = Button(self,text="X",style="Info.Sup.TButton",state="disable",command=self.sup_item)
        self.en_txt     = Entry(self,style="Info.Ent.TEntry")

        self.en_txt.bind("<KeyRelease>", self.is_writing_txt)
        self.cb_add.bind("<KeyRelease>", self.is_writing_add)
        self.cb_add.bind("<<ComboboxSelected>>", self.is_writing_add)
        self.cb_sup.bind("<<ComboboxSelected>>", self.is_writing_sup)

        sz = self.root.settings.item_size

        self.lab_name.place(x=0,y=0,height=sz,width=sz * 5)
        self.mode = "Modification"

    def new_sizing(self):
        sz = self.root.settings.item_size
        self.lab_name.place(x=0,y=0,height=sz,width=sz * 5)
        self.mode = self.mode

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Le Widget de plus haut niveau"""
        return self.master.root


    @property
    def item_pans(self):
        """Le Widget de control"""
        return self.master.master

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ NOM DU PARAMETRE (GET)
    @property
    def name(self):
        """Nom du parametre"""
        return self.__name
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ NOM DU PARAMETRE (SET)
    @name.setter
    def name(self,value):
        """Réglage du nom du parametre. Adapte également l'affiche"""
        self.__name = value
        txt = value[0].upper() + value[1:]      # L'affiche avec une majuscule
        self.lab_name.config(text=txt)

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ VALEUR DU PARAMETRE (GET)
    @property
    def val(self):
        """Valeur du parametre"""
        return self.__cur_val

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ VALEUR DU PARAMETRE (SET)
    @val.setter
    def val(self,value):
        """Réglage de la Valeur du parametre. Adapte également l'affiche"""
        self.__cur_val = value
        if type(self.__cur_val) == type(list()):    # Si la valeur est de type liste
            cb_add_val = list(self.root.all_checks[self.name])
            if len(self.__cur_val) == 0 :
                txt = ""
                self.cb_sup.config(values=["Supprimer " + self.name])
                
            else:
                cb_sup_val = [item for item in self.__cur_val if item != ""]
                cb_add_val = list(set(cb_add_val) - set(cb_sup_val))
                cb_sup_val.insert(0,"Supprimer " + self.name)
                self.cb_sup.config(values=cb_sup_val)
                if len(cb_sup_val) == 1 :   self.cb_sup.config(state="disable")
                else :                      self.cb_sup.config(state="readonly")

                
                txt = self.__cur_val[0]
                if len(self.__cur_val) > 1 :
                    for item in self.__cur_val[1:]:
                        txt += ", " + item
            
            cb_add_val.insert(0,"Ajouter " + self.name)
            self.cb_add.config(values=cb_add_val)
            self.cb_add.current(0)
            self.cb_sup.current(0)
        else:                                       # Si la valeur n'est pas de type liste
            txt = self.__cur_val

        self.lab_val.config(text=txt)
        self.en_txt.delete(0,"end")
        self.en_txt.insert(0,txt)

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ MODE DE TRAVAIL (GET)
    @property
    def mode(self):
        """Mode de travail"""
        return self.__mode

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ MODE DE TRAVAIL (SET)
    @mode.setter
    def mode(self,value):
        """Réglage du Mode de travail. Adapte également l'affiche"""
        self.__mode = value
        self.lab_val.place_forget()
        self.cb_add.place_forget()
        self.bn_add.place_forget()
        self.cb_sup.place_forget()
        self.bn_sup.place_forget()
        self.en_txt.place_forget()

        sp = self.root.settings.item_space
        sz = self.root.settings.item_size

        if value == "Modification" :
            self.lab_val.place(x=sz*5+sp ,y=0,height=sz,relwidth=1,width=-sz*5-sp)
        elif type(self.__cur_val) == type(list()):
            self.bn_add.config(state="disable")
            self.bn_sup.config(state="disable")
            larg = (sz * 7 + sp*2)/2
            self.cb_add.place(x=sz*5+sp,y=0,height=sz,relwidth=0.5,width=-larg)
            self.bn_add.place(relx=0.5,x=-larg+sz*5+sp,y=0,height=sz,width=sz)
            self.cb_sup.place(relx=0.5,x=sz * 5 / 2 + sp,y=0,height=sz,relwidth=0.5,width=-larg)
            self.bn_sup.place(relx=1,x=-sz,y=0,height=sz,width=sz)
        else:
            self.en_txt.place(x=sz*5+sp,y=0,height=sz,relwidth=1,width=-sz*5-sp)

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EVENEMENTIEL ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ L'UTILISATEUR ECRIT DANS L'ENTRY
    def is_writing_txt(self,event=None):
        """Losque l'utilisateur écrit dans l'Entry"""
        self.lab_val.config(text=self.en_txt.get())
        self.item_pans.note_changer(self.name,self.en_txt.get())

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ L'UTILISATEUR CHANGE LA COMBOBOX D'AJOUT
    def is_writing_add(self,event=None):
        """Losque l'utilisateur utilise la ComboBox d'ajout"""
        if self.cb_add.get() == "Ajouter " + self.name  or self.cb_add.get() == ""   or self.cb_add.get() in self.cb_sup.cget("values") :
            self.bn_add.config(state="disable")
        else:
            self.bn_add.config(state="normal")

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ L'UTILISATEUR CHANGE LA COMBOBOX DE SUPPRESSION
    def is_writing_sup(self,event=None):
        """Losque l'utilisateur utilise la ComboBox de suppression"""
        if self.cb_sup.get() == "Supprimer " + self.name or self.cb_sup.get() == "" :
            self.bn_sup.config(state="disable")
        else:
            self.bn_sup.config(state="normal")

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ L'UTILISATEUR AJOUTE UN ITEM
    def add_item(self,event=None):
        result = [self.cb_add.get()]
        self.root.add_Check(self.name,self.cb_add.get())
        for item in self.val :
            if item != "":
                result.append(item)
        self.item_pans.note_changer(self.name,result)
        self.val = result
        self.mode = self.mode
        self.root.refresh_list()

    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ L'UTILISATEUR SUPPRIME UN ITEM
    def sup_item(self,event=None):
        result = []
        for item in self.val :
            if item != self.cb_sup.get():
                result.append(item)
        if result == [] : result = [""]
        self.item_pans.note_changer(self.name,result)
        self.val = result
        self.root.refresh_list()
        self.mode = self.mode

     

class Viewer(Frame):

    def __init__(self, master):
        super().__init__(master,style='View.Fond.TFrame')

        self.bn_mode = Button(self,text="Modification",command=self.switch_mode,state="disabled",style="View.Mode.TButton")
        self.bn_add = Button(self,text="Nouvelle",command=self.add_note,state="normal",style="View.Mode.TButton")
        self.bn_sup = Button(self,text="Supprimer",command=self.sup_note,state="disabled",style="View.Mode.TButton")
        self.bn_copy = Button(self,text="Dupliquer",command=self.copy_note,state="disabled",style="View.Mode.TButton")
        self.cb_format = Combobox(self,values=FORMAT,style="View.Format.TCombobox",state="disabled")
        self.md_op = Md_Option(self)
        self.l_title = Label(self,style="View.Titre.TLabel",anchor="center")
        self.e_title = Entry(self,style="View.Titre.TEntry")

        self.txt = Reader(self)

        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.bn_mode.place(x=sp, y=sp, height=sz, width=4*sz)
        self.bn_add.place(x=4*sz+2*sp, y=sp, height=sz, width=3*sz)
        self.bn_sup.place(x=7*sz+3*sp, y=sp, height=sz, width=3*sz)
        self.bn_copy.place(x=10*sz+4*sp, y=sp, height=sz, width=3*sz)
        self.cb_format.place(x=13*sz+5*sp, y=sp, height=sz, relwidth=1, width=-(13*sz+6*sp))
        self.l_title.place(x=sp, y=sz+2*sp, height=2*sz+sp, relwidth=1, width=-2*sp)
        self.txt.place(x=sp, y=sz*3+sp*4, relheight=1, height=-(sz*3+sp*5), relwidth=1,width=-sp*2)

        
        self.cb_format.bind("<<ComboboxSelected>>", self.format_change)
        self.e_title.bind("<KeyRelease>", self.is_writing_txt)
        self.bind("<Configure>", self.on_Resize)


    def on_Resize(self, _event=None) -> None :
        """Réaction au redimentionnement de la fenetre"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.md_op.on_Resize()
        self.bn_mode.place(x=sp, y=sp, height=sz, width=4*sz)
        self.bn_add.place(x=4*sz+2*sp, y=sp, height=sz, width=3*sz)
        self.bn_sup.place(x=7*sz+3*sp, y=sp, height=sz, width=3*sz)
        self.bn_copy.place(x=10*sz+4*sp, y=sp, height=sz, width=3*sz)
        self.cb_format.place(x=13*sz+5*sp, y=sp, height=sz, relwidth=1, width=-(13*sz+6*sp))
        self.l_title.place(x=sp, y=sz+2*sp, height=2*sz+sp, relwidth=1, width=-2*sp)
        self.txt.place(x=sp, y=sz*3+sp*4, relheight=1, height=-(sz*3+sp*5), relwidth=1,width=-sp*2)
        self.set_mode(self.mode)

    @property
    def root(self):
        return self.master.root

    @property
    def mode(self):
        return self.bn_mode.cget("text")


    def format_change(self, event=None):
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.md_op.place_forget()
        if self.cb_format.current() == 0    : 
            self.master.note_changer("Format","texte" )  
        elif self.cb_format.current() == 1  : 
            self.master.note_changer("Format","markdown" ) 
            self.md_op.place(x=sp,y=sz+sp*2,height=sz,width=-2*sp,relwidth=1)
        elif self.cb_format.current() == 2  : 
            self.master.note_changer("Format","html" ) 
        else                                : 
            self.master.note_changer("Format","carte" ) 



    def switch_mode(self, event=None):
        if self.mode == "Modification":
            self.bn_mode.config(text="Consultation")
        else:
            self.bn_mode.config(text="Modification")
        self.master.set_mode(self.mode)

    @property
    def note_folder(self):
        return self.root.note_folder

    def add_note(self, event=None):
        self.note_folder.new_note()

    def sup_note(self, event=None):
        self.note_folder.sup_note(self.master.cur_id)

    def copy_note(self, event=None):
        self.note_folder.copy_note(self.master.cur_id)


    def set_mode(self,value):
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.md_op.place_forget()
        if value == "Consultation":
            self.bn_mode.config(text="Consultation")
            self.cb_format.config(state="normal")
            self.l_title.place_forget()
            self.e_title.place(x=sp, y=sz+2*sp, height=sz, relwidth=1, width=-2*sp)
            if self.cb_format.current() == 0 :                 #"texte" : 
                pass
            elif self.cb_format.current() == 1 :                 #"markdown" : 
                self.md_op.place(x=sp,y=2*sz+3*sp,height=self.md_op.hauteur,width=-2*sp,relwidth=1)
            elif self.cb_format.current() == 2 :                 #"html" : 
                pass
            else : 
                pass
            self.txt.place(x=sp, y=sz*2+sp*4 + self.md_op.hauteur, relheight=1, height=-(sz*2+sp*5 + self.md_op.hauteur), relwidth=1,width=-sp*2)
        else:
            self.bn_mode.config(text="Modification")
            self.cb_format.config(state="disabled")
            self.e_title.place_forget()
            self.l_title.place(x=sp, y=sz+2*sp, height=2*sz+sp, relwidth=1, width=-2*sp)
            self.txt.place(x=sp, y=sz*3+sp*4, relheight=1, height=-(sz*3+sp*5), relwidth=1,width=-sp*2)
        self.txt.set_mode(value)


    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EVENEMENTIEL ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ L'UTILISATEUR ECRIT DANS L'ENTRY
    def is_writing_txt(self,event=None):
        """Losque l'utilisateur écrit dans l'Entry"""
        self.l_title.config(text=self.e_title.get())
        self.master.note_changer("Titre",self.e_title.get())



    def set_cur_note(self, value):
        if value:
            self.bn_mode.config(state="normal")
            self.bn_sup.config(state="normal")
            self.bn_copy.config(state="normal")
            self.l_title.config(text=value["Titre"])
            self.e_title.delete(0,"end")
            self.e_title.insert(0,value["Titre"])
            if value["Format"] == "texte"        :  self.cb_format.current(0)
            elif value["Format"] == "markdown"   :  self.cb_format.current(1)
            elif value["Format"] == "html"       :  self.cb_format.current(2)
            else                                 :  self.cb_format.current(3)
            self.txt.set_cur_note(value)

        else:
            self.bn_mode.config(state="disabled")
            self.bn_sup.config(state="disabled")
            self.bn_copy.config(state="disabled")
            self.l_title.config(text="")
            self.e_title.delete(0,"end")
            self.txt.set_cur_note(None)




class Md_Option(Frame):

    def __init__(self, master):
        super().__init__(master,style='View.Fond.TFrame')
        self.__hauteur = self.root.settings.item_size
        self.__width = 320
        self.__bn_ta = Button(self,text="Titre A",style="View.Mode.TButton", command=self.__titre_A)
        self.__bn_tb = Button(self,text="B",style="View.Mode.TButton", command=self.__titre_B)
        self.__bn_tc = Button(self,text="C",style="View.Mode.TButton", command=self.__titre_C)
        self.__bn_td = Button(self,text="D",style="View.Mode.TButton", command=self.__titre_D)

        self.__bn_gr = Button(self,text="Gras",style="View.Mode.TButton", command=self.__gras)
        self.__bn_gi = Button(self,text="Gr + Ita",style="View.Mode.TButton", command=self.__gras_ita)
        self.__bn_it = Button(self,text="Italique",style="View.Mode.TButton", command=self.__ita)

        self.__bn_la = Button(self,text="Liste a",style="View.Mode.TButton", command=self.__list_a)
        self.__bn_lb = Button(self,text="b",style="View.Mode.TButton", command=self.__list_b)
        self.__bn_lc = Button(self,text="c",style="View.Mode.TButton", command=self.__list_c)
        self.__bn_ld = Button(self,text="d",style="View.Mode.TButton", command=self.__list_d)

        self.bind("<Configure>", self.on_Resize)
    

    #o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,   ,-o-,
    #§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=X=§=-- RACCOURCIS
    #  '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-o-'   '-'
    #-,    ,--,    ,--,    ,--,    ,--,    ,--,    ,--> LE PLUS HAUT WIDGET
    #  '--'    '--'    '--'    '--'    '--'    '--'
    @property
    def root(self) -> object:
        """Le Widget de plus haut niveau"""
        return self.master.root

    @property
    def txt(self) -> Text:
        return self.master.txt

    @property
    def hauteur(self) -> object:
        """Le Widget de plus haut niveau"""
        return self.__hauteur

    def on_Resize(self, _event=None) -> None :
        """Réaction au redimentionnement de la fenetre"""
        if _event : self.__width = _event.width
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        y = 0
        x = 0
        ordre = [
            (self.__bn_ta,    2*sz    ),
            (self.__bn_tb,    sz      ),
            (self.__bn_tc,    sz      ),
            (self.__bn_td,    sz      ),
            (self.__bn_gr,    2*sz    ),
            (self.__bn_gi,    2*sz    ),
            (self.__bn_it,    2*sz    ),
            (self.__bn_la,    2*sz    ),
            (self.__bn_lb,    sz      ),
            (self.__bn_lc,    sz      ),
            (self.__bn_ld,    sz      )
        ]
        
        for (bouton, size) in ordre:
            if x + size > self.__width :
                x = 0
                y += sz + sp

            bouton.place(x=x,y=y,height=sz,width=size)
            x += size + sp
        self.__hauteur = y + sz

    def __titre_A(self,event=None): self.__change_start_mark("#")
    def __titre_B(self,event=None): self.__change_start_mark("##")
    def __titre_C(self,event=None): self.__change_start_mark("###")
    def __titre_D(self,event=None): self.__change_start_mark("####")

    def __gras(self,event=None): self.__change_cursi_mark("++")
    def __gras_ita(self,event=None): self.__change_cursi_mark("!!")
    def __ita(self,event=None): self.__change_cursi_mark("--")

    def __list_a(self,event=None): self.__change_start_mark(".")
    def __list_b(self,event=None): self.__change_start_mark("..")
    def __list_c(self,event=None): self.__change_start_mark("...")
    def __list_d(self,event=None): self.__change_start_mark("....")

    def __witch_start_mark(self,line):
        cur_line = self.txt.get(str(line)+".0",str(line)+".end")
        if   cur_line[:4] == "####" : return "####"
        elif cur_line[:3] == "###"  : return "###"
        elif cur_line[:2] == "##"   : return "##"
        elif cur_line[:1] == "#"    : return "#"
        elif cur_line[:4] == "...." : return "...."
        elif cur_line[:3] == "..."  : return "..."
        elif cur_line[:2] == ".."   : return ".."
        elif cur_line[:1] == "."    : return "."
        else                        : return ""

    def __change_start_mark(self,mark):
        l_deb = int(self.txt.index("insert").split(".")[0])
        l_fin = l_deb
        if len(self.txt.tag_ranges("sel")) == 2 :
            l_deb = int(str(self.txt.tag_ranges("sel")[0]).split(".")[0])
            l_fin = int(str(self.txt.tag_ranges("sel")[1]).split(".")[0])
        
        sup_only = self.__witch_start_mark(l_deb) == mark

        for line in  range(l_deb,l_fin+1):
            new_line = self.txt.get(str(line)+".0",str(line)+".end")
            new_line = new_line[len(self.__witch_start_mark(line)):]
            if not sup_only : new_line = mark + new_line
            self.txt.delete(str(line)+".0",str(line)+".end")
            self.txt.insert(str(line)+".0",new_line)
        self.txt.is_writing()
        self.txt.focus_set()

    def __change_cursi_mark(self,mark):
        deb = str(self.txt.index("insert"))
        #fin = str(self.txt.index("insert"))
        if len(self.txt.tag_ranges("sel")) == 2 :
            deb = str(self.txt.tag_ranges("sel")[0])
            #fin = str(self.txt.tag_ranges("sel")[1])
        
        l_deb, c_deb = deb.split(".")
        c_deb = int(c_deb)
        #l_fin, c_fin = fin.split(".")
        if self.__witch_start_mark(l_deb) == "":
            new_line = self.txt.get(str(l_deb)+".0",str(l_deb)+".end")
            for item in self.__cursi_pos(mark,l_deb):
                if item in [c_deb,c_deb-1,c_deb-2]:
                    new_line = new_line[:item] + new_line[item+len(mark):]
                    new_i = item
                    break
            else:
                new_line = new_line[:c_deb] + mark + new_line[c_deb:]
                new_i = c_deb + 2
            self.txt.delete(str(l_deb)+".0",str(l_deb)+".end")
            self.txt.insert(str(l_deb)+".0",new_line)
            self.txt.mark_set("insert",str(l_deb)+"."+str(new_i))
            self.txt.focus_set()
            self.txt.is_writing()
    
    def __cursi_pos(self,mark,line,start = 0,end = 99999):
        result = []
        cur_line = str(self.txt.get(str(line)+".0",str(line)+".end"))
        in_form = False
        in_sel = False
        new_line = ""
        for i in range(len(cur_line) - len(mark) + 1) :
            if i == start : in_sel = True
            if cur_line[i:i+len(mark)] == mark : 
                in_form = not in_form
                result.append(i)
            if i == end : in_sel = False
        return result



class Reader(Text):

    def __init__(self, master):
        super().__init__(master,state = "disabled",**master.root.settings["View"].reader)
        self.bind("<KeyRelease>", self.is_writing)


    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Le Widget de plus haut niveau"""
        return self.master.root

    @property
    def item_pans(self):
        """Le Widget de control"""
        return self.master.master

    @property
    def mode(self):
        return self.master.bn_mode.cget("text")

    @property
    def cur_val(self):
        if self.master.master.cur_note :
            return self.item_pans.cur_note["Contenu"]
        else :
            return ""

    @cur_val.setter
    def cur_val(self,value):
        self.item_pans.cur_note["Contenu"] = value

    def is_writing(self, event=None):
        if self.mode == "Consultation":
            self.item_pans.note_changer("Contenu",self.get("1.0", 'end'))

    def set_mode(self,value):
        self.config(state="normal")
        self.delete("1.0", "end")
        if value == "Consultation":
            self.tag_delete("all")
            self.insert("end", self.cur_val)
        else:
            cur = self.master.cb_format.current()
            if cur == 0 :                 #"texte" : 
                self.insert("end", self.cur_val)

            elif cur == 1 :                 #"markdown" : 
                txt, conf = markdown_convert(self.cur_val)
                self.insert("end", txt)
                for cnf in conf:
                    self.tag_add(*cnf)
                self.markdown_tag_config()

            elif cur == 2 :                 #"html" : 
                self.insert("end", self.cur_val)

            else : 
                self.insert("end", self.cur_val)
            self.config(state="disabled")

    def markdown_tag_config(self):
        for key, val in self.root.settings["View"].md_tags.items():
            self.tag_config(key, **val)




    def set_cur_note(self, value):
        self.config(state="normal")
        self.delete("1.0", "end")
        if value :
            if value["Format"] == "texte"        : 
                self.insert("end", self.cur_val)

            elif value["Format"] == "markdown"   : 
                txt, conf = markdown_convert(self.cur_val)
                self.insert("end", txt)
                for cnf in conf:
                    self.tag_add(*cnf)
                self.markdown_tag_config()

            elif value["Format"] == "html"       : 
                self.insert("end", self.cur_val)

            else                                : 
                self.insert("end", self.cur_val)
        self.config(state="disabled")



def markdown_convert(source_txt: str):
    lines = source_txt.split("\n")
    result_text = ""
    result_conf = []
    for i in range(len(lines)):

        if lines[i][:4] == "####":
            result_text += "            " + lines[i][4:]
            result_conf.append(
                ("t4", str(i + 1) + ".0", str(i + 1) + ".end"))
        elif lines[i][:3] == "###":
            result_text += "        " + lines[i][3:]
            result_conf.append(
                ("t3", str(i + 1) + ".0", str(i + 1) + ".end"))
        elif lines[i][:2] == "##":
            result_text += "    " + lines[i][2:]
            result_conf.append(
                ("t2", str(i + 1) + ".0", str(i + 1) + ".end"))
        elif lines[i][:1] == "#":
            result_text += lines[i][1:]
            result_conf.append(
                ("t1", str(i + 1) + ".0", str(i + 1) + ".end"))
        else:
            decal = 0
            if lines[i][:4] == "....":
                result_text += "                  → "
                decal = 4
                char_add = 20
            elif lines[i][:3] == "...":
                result_text += "              ⇾ "
                decal = 3
                char_add = 16
            elif lines[i][:2] == "..":
                result_text += "          ⇨ "
                decal = 2
                char_add = 12
            elif lines[i][:1] == ".":
                result_text += "      ⇛ "
                decal = 1
                char_add = 8
            else:
                result_text += "        "
                char_add = 8

            full_txt = lines[i][decal:]
            final_txt = full_txt
            final_txt, _ = find_balise("--", final_txt)
            final_txt, _ = find_balise("++", final_txt)
            final_txt, _ = find_balise("!!", final_txt)

            if "--" in full_txt:
                rest_txt = full_txt
                rest_txt, _ = find_balise("++", rest_txt)
                rest_txt, _ = find_balise("!!", rest_txt)
                rest_txt, lid = find_balise("--", rest_txt)
                while len(lid) != 0:
                    if len(lid) >= 2:
                        result_conf.append(
                            ("ita",
                                str(i + 1) + "." + str(lid[0] + char_add),
                                str(i + 1) + "." + str(lid[1] + char_add)))
                        lid = lid[2:]
                    else:
                        result_conf.append(
                            ("ita",
                                str(i + 1) + "." + str(lid[0] + char_add),
                                str(i + 1) + ".end"))
                        lid = []

            if "++" in full_txt:
                rest_txt = full_txt
                rest_txt, _ = find_balise("--", rest_txt)
                rest_txt, _ = find_balise("!!", rest_txt)
                rest_txt, lid = find_balise("++", rest_txt)
                while len(lid) != 0:
                    if len(lid) >= 2:
                        result_conf.append(
                            ("grs",
                                str(i + 1) + "." + str(lid[0] + char_add),
                                str(i + 1) + "." + str(lid[1] + char_add)))
                        lid = lid[2:]
                    else:
                        result_conf.append(
                            ("grs",
                                str(i + 1) + "." + str(lid[0] + char_add),
                                str(i + 1) + ".end"))
                        lid = []

            if "!!" in full_txt:
                rest_txt = full_txt
                rest_txt, _ = find_balise("--", rest_txt)
                rest_txt, _ = find_balise("++", rest_txt)
                rest_txt, lid = find_balise("!!", rest_txt)
                while len(lid) != 0:
                    if len(lid) >= 2:
                        result_conf.append(
                            ("sup",
                                str(i + 1) + "." + str(lid[0] + char_add),
                                str(i + 1) + "." + str(lid[1] + char_add)))
                        lid = lid[2:]
                    else:
                        result_conf.append(
                            ("sup",
                                str(i + 1) + "." + str(lid[0] + char_add),
                                str(i + 1) + ".end"))
                        lid = []
            result_text += final_txt

        result_text += "\n"

    return result_text[:-1], result_conf
        

def find_balise(balise: str, texte_source: str):
    result_txt = texte_source
    result_indexes = []
    delta = len(balise)
    i = 0
    while i < len(result_txt) - delta + 1:
        if result_txt[i:i + delta] == balise:
            result_indexes.append(i)
            result_txt = result_txt[:i] + result_txt[i + delta:]
        else:
            i += 1

    return (result_txt, result_indexes)
    


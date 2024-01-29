from tkinter import Frame
from tkinter.ttk import Treeview, Button, Style


class Framelist(Frame):

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__(self, master):
        """Volet contenant l'arbre d'affichage des notes"""
        super().__init__(master)
        self.list_box = NoteListBox(self)
        self.__fold_false = "⇚\n\nL\n\nI\n\nS\n\nT\n\nE\n\n⇚"                # Texte du bouton si le volet est deplié
        self.__fold_true = "⇛\n\nL\n\nI\n\nS\n\nT\n\nE\n\n⇛"                 # Texte du bouton si le volet est plié
        self.__btn = Button(self,
                          text=self.__fold_false,
                          command=self.__switch_width,
                          style="Listing.Pan.TButton")
                          
        fs = self.root.settings.fold_size
        self.list_box.place(x=0, y=0, relheight=1, relwidth=1, width=-fs)
        self.__btn.place(relx=1, x=-fs, y=0, relheight=1, width=fs)
        self.bind("<Configure>", self.__on_Resize)

        self.__style = Style(self.root)
        self.__style.theme_use('alt')

    def new_sizing(self):
        """Lors du changement de taille du Style"""
        fs = self.root.settings.fold_size
        self.list_box.place(x=0, y=0, relheight=1, relwidth=1, width=-fs)
        self.__btn.place(relx=1, x=-fs, y=0, relheight=1, width=fs)

    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    def __switch_width(self):
        """Inversion du pliage du volet"""
        if self.__btn.cget("text") == self.__fold_false:
            self.__btn.config(text=self.__fold_true)
            self.master.paneconfig(self, width=self.root.settings.fold_size)
        else:
            self.__btn.config(text=self.__fold_false)
            self.master.paneconfig(self, width=self.root.settings.item_size * 14)

    def __on_Resize(self, event=None):
        """Lors du redimentionnement de la fenetre"""
        if event:
            frm_width = int(event.width)
        else:
            frm_width = self.root.settings.item_size * 14

        if frm_width > self.root.settings.fold_size:
            self.__btn.config(text=self.__fold_false)
        else:
            self.__btn.config(text=self.__fold_true)


class NoteListBox(Treeview):
    def __init__(self, master):
        """Le Widget d'affichage de la liste des Notes"""
        super().__init__(master, selectmode="browse", style="Listing.TW.Treeview")
        self.__cur_inserts = []
        self.__cur_param = []
        self.__cur_selec = ""
        self.__index = 0
        self.bind("<Button-1>", self.__down_lvl)
        self.bind("<Button-3>", self.__up_lvl)
        self.bind('<<TreeviewSelect>>', self.__selecting)
        self.bind('<<TreeviewOpen>>', self.__open)
        self.bind('<<TreeviewClose>>', self.__close)

    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root
  
    def __creat_colomns(self,nb_col):
        """Création des Colonnes du Treeview"""
        if nb_col > 1:  # CREATION DES COLONNES
            self["columns"] = tuple(["#" + str(i) for i in range(1, nb_col)])
        else:
            self["columns"] = ()

    def __creat_headers(self,tree_list,visi_list):
        """Création des En-têtes du Treeview"""
        txt = ""
        if len(tree_list) > 0:  # CREATION DU PREMIER EN-TETES
            for item in tree_list:
                txt += item + " / "
        i = 0
        for item in visi_list:  # CREATION DU PREMIER EN-TETES
            if i == 0:
                self.column("#" + str(i),
                            width=50 + len(tree_list) * 40,
                            minwidth=20)
                self.heading("#" + str(i), text=txt + item, anchor="w")
            else:
                self.column("#" + str(i), width=50, minwidth=20)
                self.heading("#" + str(i), text=item, anchor="w")
            i += 1

    def fill_list(self, _inserts = None, filters_param = None):
        """Remplir le Treeview en fonction des éléments fourni par le dossier"""
        tree_list = []
        visi_list = []
        if not _inserts is None : self.__cur_inserts = _inserts
        if filters_param : self.__cur_param = filters_param
        for item in self.__cur_param:
            if item["tree"] : 
                tree_list.append(item["name"])
            elif item["visi"] : 
                visi_list.append(item["name"])
        self.__creat_colomns(len(visi_list))
        self.__creat_headers(tree_list,visi_list)
        self.delete(*self.get_children())
        for _insert in self.__cur_inserts:
            if _insert["tags"][1][-2:] == "_s":
                _insert["tags"][1] = _insert["tags"][1][:-2]
            if self.__cur_selec == _insert["tags"][0]:
                _insert["tags"][1] += "_s"
            self.insert(**_insert)
        self.tag_configure( "selected", **self.root.settings["Listing"]["TW"].select)
        for key, conf in self.root.settings["Listing"]["TW"].tags(len(tree_list)).items(): 
            self.tag_configure(key, **conf)

    def __open(self, event=None):
        """Déplier un item"""
        self.__cur_inserts[self.__index]["open"] = True
        self.fill_list(self.__cur_inserts,self.__cur_param)

    def __close(self, event=None,id : int = None):
        """Plier un item"""
        if not id : id = self.__index
        self.__cur_inserts[id]["open"] = False
        for inset in self.__cur_inserts :
            if not inset["tags"][1] in ["data","data_s"]:
                if inset["parent"] != "" and int(inset["parent"]) == id:
                    self.__close(id=int(inset["iid"]))
        self.fill_list(self.__cur_inserts,self.__cur_param)

    def __selecting(self, event=None):
        """Sélection d'un item en cliquant"""
        if len(self.selection()) > 0:
            self.__index = int(self.selection()[0])
            self.__cur_selec = self.item(self.selection()[0], "tags")[0]
            if "data" in self.item(self.selection()[0], "tags") or "data_s" in self.item(self.selection()[0], "tags"):
                self.root.select_item(
                    self.item(self.selection()[0], "tags")[0])
            else:
                self.root.select_item(None)
            self.fill_list(self.__cur_inserts,self.__cur_param)
        else:
            self.root.select_item(None)
            self.__cur_selec = ""

    def set_select(self,_id):
        """Sélection d'un item avec son id"""
        self.__cur_selec = _id
        self.root.refresh_list()
        self.root.select_item(_id)


    def __down_lvl(self, event):
        """Pliage d'un niveau complet"""
        region = self.identify("region", event.x, event.y)
        if region == "heading":
            lvl = self.__open_lvl()
            if lvl != 0:
                for inset in self.__cur_inserts :
                    if inset["tags"][1] in ["Nv_" + str(lvl),"Nv_" + str(lvl)+"_s"]:
                        inset["open"] = False
                self.fill_list(self.__cur_inserts,self.__cur_param)

    def __up_lvl(self, event):
        """Dépliage d'un niveau complet"""
        region = self.identify("region", event.x, event.y)
        if region == "heading":
            lvl = self.__close_lvl()
            if lvl:
                for inset in self.__cur_inserts :
                    if inset["tags"][1] in ["Nv_" + str(lvl),"Nv_" + str(lvl)+"_s"]:
                        inset["open"] = True
                self.fill_list(self.__cur_inserts,self.__cur_param)

    def __open_lvl(self):
        """Plus bas niveau ouvert"""
        for i in  range(len(self.__cur_inserts)-1,-1,-1):
            cur = self.__cur_inserts[i]["tags"][1]
            if cur[-2:] == "_s" : cur = cur[:-2]
            if cur != "data":
                cur = int(cur[3:])
                if self.__cur_inserts[i]["open"]:
                    return cur
        return 0

    def __close_lvl(self):
        """Plus haut niveau fermé"""
        for i in  range(len(self.__cur_inserts)):
            cur = self.__cur_inserts[i]["tags"][1]
            if cur[-2:] == "_s" : cur = cur[:-2]
            if cur != "data":
                cur = int(cur[3:])
                if not self.__cur_inserts[i]["open"]:
                    return cur
        return None
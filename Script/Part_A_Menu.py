from tkinter import Menu, StringVar, Toplevel, IntVar
from tkinter.ttk import Combobox, Frame, Button, Entry, Label, Spinbox
import os
import json 
from .Data import Horodate

class Menubar(Menu):

    def __init__(self, master) -> None:
        """La Barre de Menu de l'application"""
        super().__init__(master)

        self.__ouvrir = Menu(self, tearoff=0)
        self.__entries = []
        self.__cur_index = 1
        test = True
        for item in os.listdir(os.getcwd()):
            if os.path.isdir(os.path.join(os.getcwd(), item)) and not item in [ "Script", ".cache", ".config", ".upm", "venv", ".git" ]:
                if test:
                    self.__var_folder = StringVar(self, item)
                    test = False
                self.__entries.append(item)
                self.__ouvrir.add_radiobutton(label=item, variable=self.__var_folder, value=item)

        dos = Menu(self, tearoff=0)
        dos.add_command(label="Nouveau",command=self.__add_folder)
        dos.add_cascade(label="Ouvrir", menu=self.__ouvrir)
        dos.add_separator()
        dos.add_command(label="Configurer", command=self.__new_configurator)
        dos.add_separator()
        dos.add_command(label="Quitter", command=self.__quit)

        self.add_cascade(label="Dossier", menu=dos)

        self.__var_colo = StringVar(self, "Gris")
        self.__var_ton = StringVar(self, "Foncée")
        self.__var_size = StringVar(self, "Moyen")

        appa = Menu(self, tearoff=0)
        appa.add_radiobutton(label="Gris", variable=self.__var_colo)
        appa.add_radiobutton(label="Bleu", variable=self.__var_colo)
        appa.add_radiobutton(label="Cyan", variable=self.__var_colo)
        appa.add_radiobutton(label="Vert", variable=self.__var_colo)
        appa.add_radiobutton(label="Jaune", variable=self.__var_colo)
        appa.add_radiobutton(label="Rouge", variable=self.__var_colo)
        appa.add_radiobutton(label="Magenta", variable=self.__var_colo)
        appa.add_radiobutton(label="Multi", variable=self.__var_colo)
        appa.add_separator()
        appa.add_radiobutton(label="Foncée", variable=self.__var_ton)
        appa.add_radiobutton(label="Claire", variable=self.__var_ton)
        appa.add_separator()
        appa.add_radiobutton(label="Petit", variable=self.__var_size)
        appa.add_radiobutton(label="Moyen", variable=self.__var_size)
        appa.add_radiobutton(label="Grand", variable=self.__var_size)

        self.add_cascade(label="Apparence", menu=appa)

        self.__var_folder.trace("w", self.__new_folder)
        self.__var_colo.trace("w", self.__change_style)
        self.__var_ton.trace("w", self.__change_style)
        self.__var_size.trace("w", self.__change_style)

    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    @property
    def cur_path(self):
        """Le nom du Dossier en cours"""
        return self.__var_folder.get()

    def __new_folder(self, *arg, **kwarg):
        """Chargement du Dossier en cours"""
        self.__close_configurator()
        self.root.new_folder()


    def __add_folder(self):
        """Création d'un nouveau Dossier"""
        self.__close_configurator()
        nom = "Nouveau Dossier " + str(self.__cur_index)
        while nom in self.__entries:
            self.__cur_index += 1
            nom = "Nouveau Dossier " + str(self.__cur_index)

        os.makedirs(os.path.join(os.getcwd(), nom))
        self.__entries.append(nom)
        self.__ouvrir.add_radiobutton(label=nom, variable=self.__var_folder, value=nom)
        self.__var_folder.set(nom)
        self.__cur_index += 1
        self.__new_configurator()



    def change_folder_name(self,old_name, new_name):
        """Changement du nom du Dossier"""
        for i in range(len(self.__entries)):
            if old_name == self.__entries[i]:
                self.__entries[i] = new_name
                self.__ouvrir.entryconfig(i,label=new_name, value=new_name)
                os.rename(
                    os.path.join(os.getcwd(), old_name),
                    os.path.join(os.getcwd(), new_name)
                    )
                self.__var_folder.set(new_name)

    def __new_configurator(self, event = None):
        """Ouvrir le Configurateur"""
        if not self.root.configurator :
            self.root.configurator = Configurator(self.root)

    def __close_configurator(self):
        """Fermer le Configurateur"""
        if self.root.configurator :
            self.root.configurator.on_closing()

    def __quit(self,event=None):
        """Fermer l'Apllication"""
        self.root.destroy()

    def __change_style(self, *arg, **kwarg):
        """Changement du Style"""
        self.__close_configurator()
        self.root.change_style(self.__var_colo.get(),self.__var_ton.get(),self.__var_size.get())





class Configurator(Toplevel):
    def __init__(self, master) -> None:
        """La fenêtre de configuration du Dossier sélectionné"""
        super().__init__(master, bg = master.root.settings["Configurateur"].background)
        self.config(width=400, height=400)
        self.title("Configuration du dossier en cours")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__cur_index = 1
        self.__titre_lab = Label(self,text="Nom du dossier",anchor="w",style="Configurateur.Box.TLabel")
        self.__titre_var = StringVar(self,self.root.cur_path)
        self.__titre_val = Entry(self,style="Configurateur.Box.TEntry",textvariable=self.__titre_var)

        self.__tree_lab = Label(self,text="Elements hierarchisés",anchor="w",style="Configurateur.Box.TLabel")
        self.__tree_var = IntVar(self, value=self.root.current_config["tree"])
        self.__tree_val = Spinbox(self,textvariable=self.__tree_var,style="Configurateur.Box.TSpinbox",state="readonly")
        self.__visi_lab = Label(self,text="Elements visibles",anchor="w",style="Configurateur.Box.TLabel")
        self.__visi_var = IntVar(self, value=self.root.current_config["visi"]+1)
        self.__visi_val = Spinbox(self,textvariable=self.__visi_var,style="Configurateur.Box.TSpinbox",state="readonly")

        self.__in_lab = Label(self,text="Parametres présent dans les filtres",anchor="w",style="Configurateur.Box.Titre.TLabel")
        self.__out_lab = Label(self,text="Parametres exclus des filtres",anchor="w",style="Configurateur.Box.Titre.TLabel")
        self.__sup_lab = Label(self,text="Parametres supprimés",anchor="w",style="Configurateur.Box.Titre.TLabel")
        self.__param_in = []
        self.__param_out = []
        self.__param_sup = []
        self.__add = Button(self,text="Nouveau Parametre",style="Configurateur.Box.In.TButton",command=self.__add_param)
        self.__valid = Button(self,text="Valider les modification",style="Configurateur.Box.In.TButton",command=self.__valid_config)
        self.__fill_param()
        self.__tree_var.trace("w",self.__tree_change)
        self.__visi_var.trace("w",self.__visi_change)

    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    def on_closing(self):
        """Lors de la fermeture du Configurateur"""
        self.root.configurator = None
        self.destroy()

    def __fill_param(self):
        """Placement des Widgets en fonction du nombre de Parametre"""
        param = []

        sp = self.root.settings.item_space
        sz = self.root.settings.item_size

        self.__titre_lab.place(x=sp,y=sp,width=sz*5,height=sz)
        self.__titre_val.place(x=sz*5+sp*2,y=sp,relwidth=1,width=-(sz*5+sp*3),height=sz)
        self.__tree_lab.place(x=sp,y=sz+2*sp,relwidth=0.5, width = -(1.5*sz+1.5*sp),height=sz)
        self.__tree_val.place(relx=0.5,x=-(1.5*sz+0.5*sp),y=sz+2*sp, width = 1.5*sz,height=sz)
        self.__visi_lab.place(relx=0.5,x=0.5*sp,y=sz+2*sp,relwidth=0.5, width = -(1.5*sz+1.5*sp),height=sz)
        self.__visi_val.place(relx=1,x=-(1.5*sz+sp),y=sz+2*sp, width = 1.5*sz,height=sz)
        self.__in_lab.place(x=sp,y=sz*2+sp*3,relwidth=1,width=-2*sp,height=sz)
        h=sz*3+sp*4
        for key, val in self.root.current_config["format"].items() :
            param.append(key)
            self.__param_in.append(ConfBox(self,key, val,True))
            self.__param_in[-1].place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
            h+=sz+sp
        self.__param_in[0].disable_up()
        self.__param_in[-1].disable_down()
        self.__tree_val.config(from_=0,to=len(self.__param_in)-1)
        self.__visi_val.config(from_=1,to=len(self.__param_in))
        self.__out_lab.place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
        h+=sz+sp
        if len(self.root.note_folder.listing) > 0 :
            for key, val in self.root.note_folder.listing[0].items() :
                if not key in param :
                    param.append(key)
                    if type(val) == type(Horodate()):
                        self.__param_out.append(ConfBox(self,key, "date", False))
                    elif type(val) == type(list()):
                        self.__param_out.append(ConfBox(self,key, "list", False))
                    else:
                        self.__param_out.append(ConfBox(self,key, "str", False))
                    self.__param_out[-1].place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
                    h+=sz+sp
        self.__add.place(x=sp,y=h,relwidth=0.5,width=-1.5*sp,height=sz)
        self.__valid.place(relx=0.5,x=0.5*sp,y=h,relwidth=0.5,width=-1.5*sp,height=sz)
        h+=sz+sp
        self.config(width=sz*13+sp*7, height=h)

    def __reset_place(self):
        """Réagensement des Widgets en fonction du nombre de Parametre"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.__sup_lab.place_forget()
        h=sz*3+sp*4
        for box in self.__param_in :
            box.enable_all()
            box.place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
            h+=sz+sp
        if len(self.__param_in) == 1 :
            self.__param_in[0].disable_in()
        self.__param_in[0].disable_up()
        self.__param_in[-1].disable_down()
        self.__tree_val.config(from_=0,to=len(self.__param_in)-1)
        self.__visi_val.config(from_=1,to=len(self.__param_in))
        if self.__visi_var.get() > len(self.__param_in) :
            self.__visi_var.set(len(self.__param_in))
        self.__out_lab.place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
        h+=sz+sp
        for box in self.__param_out :
            box.place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
            h+=sz+sp
        self.__add.place(x=sp,y=h,relwidth=0.5,width=-1.5*sp,height=sz)
        self.__valid.place(relx=0.5,x=0.5*sp,y=h,relwidth=0.5,width=-1.5*sp,height=sz)
        h+=sz+sp
        if len(self.__param_sup) > 0 :
            self.__sup_lab.place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
            h+=sz+sp
        for box in self.__param_sup :
            box.place(x=sp,y=h,relwidth=1,width=-2*sp,height=sz)
            h+=sz+sp
        self.config(width=sz*13+sp*7, height=h)

    def move_up(self,_box):
        """Déplacement d'un parametre vers le haut"""
        for i in range(len(self.__param_in)) :
            if _box == self.__param_in[i]:
                self.__param_in[i-1],self.__param_in[i] = self.__param_in[i],self.__param_in[i-1]
                break
        self.__reset_place()

    def move_down(self,_box):
        """Déplacement d'un parametre vers le bas"""
        for i in range(len(self.__param_in)) :
            if _box == self.__param_in[i]:
                self.__param_in[i+1],self.__param_in[i] = self.__param_in[i],self.__param_in[i+1]
                break
        self.__reset_place()

    def move_in(self,_box):
        """Déplacement d'un parametre vers les filtres"""
        for i in range(len(self.__param_out)) :
            if _box == self.__param_out[i]:
                self.__param_in.append(self.__param_out.pop(i))
                break
        self.__reset_place()

    def move_out(self,_box):
        """Déplacement d'un parametre hors des filtres"""
        for i in range(len(self.__param_in)) :
            if _box == self.__param_in[i]:
                self.__param_out.append(self.__param_in.pop(i))
                break
        self.__reset_place()

    def move_sup(self,_box):
        """Supprimer un parametre"""
        for i in range(len(self.__param_in)) :
            if _box == self.__param_in[i]:
                self.__param_sup.append(self.__param_in.pop(i))
                break
        else :
            for i in range(len(self.__param_out)) :
                if _box == self.__param_out[i]:
                    self.__param_sup.append(self.__param_out.pop(i))
                    break
        self.__reset_place()

    def restor(self,_box):
        """Restore un parametre supprimé"""
        for i in range(len(self.__param_sup)) :
            if _box == self.__param_sup[i]:
                self.__param_out.append(self.__param_sup.pop(i))
                break
        self.__reset_place()

    def __tree_change(self, *arg, **kwarg):
        """Lors d'un changement de la SpinBox .__tree_val"""
        if self.__visi_var.get() < self.__tree_var.get()+1:
            self.__visi_var.set(self.__tree_var.get()+1)

    def __visi_change(self, *arg, **kwarg):
        """Lors d'un changement de la SpinBox .__visi_val"""
        if self.__tree_var.get() > self.__visi_var.get()-1:
            self.__tree_var.set(self.__visi_var.get()-1)

    def __add_param(self,event=None):
        """Création d'un nouveau Parametre"""
        self.__param_out.append(ConfBox(self,"Parametre_"+str(self.__cur_index), "str", False, True))
        self.__cur_index += 1
        self.__reset_place()

    def __valid_config(self,event=None):
        """Validation des modifications de la Configuration"""
        sup_list = [ param.orig_nom for param in self.__param_sup]
        for note in self.root.note_folder.listing :
            for frm in self.__param_in:
                if frm.is_new :
                    note[frm.nom] = frm.new_value
                elif frm.nom_has_change :
                    temp_value = note[frm.orig_nom]
                    note[frm.nom] = temp_value
                    del note[frm.orig_nom]
                if frm.format_has_change :
                    note[frm.nom] = frm.new_value
            for frm in self.__param_out:
                if frm.is_new :
                    note[frm.nom] = frm.new_value
                elif frm.nom_has_change :
                    temp_value = note[frm.orig_nom]
                    note[frm.nom] = temp_value
                    del note[frm.orig_nom]
                if frm.format_has_change :
                    note[frm.nom] = frm.new_value
            for key in sup_list:
                try     : del note[key]
                except  : pass
            note.ecrire_json()

        new_conf = {frm.nom : frm.format for frm in self.__param_in}
        current_config = { "format" : new_conf, 
                            "tree" : self.__tree_var.get() , 
                            "visi" : self.__visi_var.get()-1} 
        with open(os.getcwd() + "/"+self.root.cur_path+"/config.json", mode = "w") as f:
            f.write(json.dumps(current_config))
        if self.root.cur_path != self.__titre_var.get():
            self.root.change_folder_name(self.root.cur_path, self.__titre_var.get())

        self.root.new_folder()
        self.on_closing()
        



class ConfBox(Frame):
    def __init__(self,master,_nom,_format,_in,is_new = False):
        """Widget permetant la modification d'un parametre"""
        super().__init__(master,style="Configurateur.Box.TFrame")
        self.orig_nom = _nom
        self.orig_format = _format
        self.is_new = is_new
        index, val = 0, "Unique"
        if _format =="list" : index, val = 1, "Liste"
        elif _format =="date" : index, val = 2, "Date"
        txt = "Inclure"
        if _in : txt = "Exclure"
        self.__up = Button(self,text=self.root.settings.ico["monter"],style="Configurateur.Box.Move.TButton",command=self.__move_up)
        self.__down = Button(self,text=self.root.settings.ico["descendre"],style="Configurateur.Box.Move.TButton",command=self.__move_down)
        self.__nom_l = Label(self,text=_nom,anchor="w",style="Configurateur.Box.TLabel")
        self.__format_l = Label(self,text=val,anchor="w",style="Configurateur.Box.TLabel")
        self.__nom_var = StringVar(self,_nom)
        self.__nom_e = Entry(self, textvariable=self.__nom_var,style="Configurateur.Box.TEntry")
        self.__sup = Button(self,text="X",style="Configurateur.Box.Sup.TButton",command=self.__move_sup)
        self.__format_cb = Combobox(self,values=["Unique","Liste","Date"],style="Configurateur.Box.TCombobox")
        self.__format_cb.current(index)
        self.__filtre = Button(self,text=txt,style="Configurateur.Box.In.TButton",command=self.__toggle_in)

        sp = self.root.settings.item_space
        sz = self.root.settings.item_size

        if _nom in ["Id","Titre","Format","Contenu","Cr\u00e9\u00e9e le","Modifi\u00e9e le"]:
            self.__nom_l.place(x=0,y=0,width=sz*4,height=sz)
            self.__format_l.place(x=sz*4+sp,y=0,width=3*sz,height=sz)
        else:
            self.__nom_e.place(x=0,y=0,width=sz*4,height=sz)
            self.__sup.place(x=sz*12+sp*5,y=0,width=sz,height=sz)
            self.__format_cb.place(x=sz*4+sp,y=0,width=3*sz,height=sz)
            
        if _in : 
            self.__up.place(x=sz*10+sp*3,y=0,width=sz,height=sz)
            self.__down.place(x=sz*11+sp*4,y=0,width=sz,height=sz)
        self.__filtre.place(x=sz*7+sp*2,y=0,width=3*sz,height=sz)


    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root

    def enable_all(self):
        """Active tous les Boutons"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size
        self.__up.config(state="normal")
        self.__down.config(state="normal")
        self.__filtre.place(x=sz*7+sp*2,y=0,width=3*sz,height=sz)
        if not self.orig_nom in ["Id","Titre","Format","Contenu","Cr\u00e9\u00e9e le","Modifi\u00e9e le"]:
            self.__sup.place(x=sz*12+sp*5,y=0,width=sz,height=sz)

    def disable_up(self):
        """Desactive le Bouton monté"""
        self.__up.config(state="disabled")

    def disable_down(self):
        """Desactive le Bouton descendre"""
        self.__down.config(state="disabled")

    def disable_in(self):
        """Desactive le Bouton d'exclusion des filtres"""
        self.__filtre.place_forget()
        self.__sup.place_forget()

    @property
    def nom(self):
        """La valeur en cours du nom du Dossier"""
        return self.__nom_var.get()

    @property
    def nom_has_change(self):
        """Le nom du Parametre a-t-il changé ?"""
        return self.nom != self.orig_nom

    @property
    def format(self):
        """La valeur en cours du format du Parametre"""
        if self.__format_cb.current() == 0 :
            return "str"
        elif self.__format_cb.current() == 1 :
            return "list"
        else:
            return "date"

    @property
    def format_has_change(self):
        """Le format du Parametre a-t-il changé ?"""
        return self.format != self.orig_format

    @property
    def new_value(self):
        """Une valeur vierge pour ce parametre"""
        if self.__format_cb.current() == 0 :
            return ""
        elif self.__format_cb.current() == 1 :
            return [""]
        else:
            return Horodate()

    def __move_up(self,event=None):
        """Déplacer ce parametre vers le haut"""
        self.master.move_up(self)

    def __move_down(self,event=None):
        """Déplacer ce parametre vers le bas"""
        self.master.move_down(self)

    def __toggle_in(self,event=None):
        """Action sur le bouton Inclure/Exclure"""
        sp = self.root.settings.item_space
        sz = self.root.settings.item_size

        if self.__filtre.cget("text")== "Inclure":
            self.master.move_in(self)
            self.__filtre.config(text="Exclure")
            self.__up.place(x=sz*10+sp*3,y=0,width=sz,height=sz)
            self.__down.place(x=sz*11+sp*4,y=0,width=sz,height=sz)
        elif self.__filtre.cget("text")== "Exclure":
            self.__filtre.config(text="Inclure")
            self.__up.place_forget()
            self.__down.place_forget()
            self.master.move_out(self)
        else:
            self.__filtre.config(text="Inclure")
            self.__up.place_forget()
            self.__down.place_forget()
            
            if not self.orig_nom in ["Id","Titre","Format","Contenu","Cr\u00e9\u00e9e le","Modifi\u00e9e le"]:
                self.__sup.place(x=sz*12+sp*5,y=0,width=sz,height=sz)
            self.master.restor(self)

    def __move_sup(self,event=None):
        """Suppression du Parametre"""
        self.__filtre.config(text="Restorer")
        self.__up.place_forget()
        self.__down.place_forget()
        self.__sup.place_forget()
        self.master.move_sup(self)



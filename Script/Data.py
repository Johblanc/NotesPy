
import os 
import json 
from datetime import datetime

class Folder():
    
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__(self, master):
        """Création d'un nouveau Dossier"""
        self.master = master                  # WIDGET PARENT
        self.listing = []
        self.current_config = {}

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ CONFIGURATION ACTUELLE DES FILTRES
    
    def fill_listing(self, folder = "Mes_Notes"):
        """Remplir le listing avec les Notes contenues dans le dossier folder"""
        self.listing = []
        conf_exist = False
        for item in os.listdir(os.getcwd() + "/" + folder):
            data = json.load(open(folder+"/"+item))
            if item == "config.json":
                conf_exist = True
                self.current_config = data
            else :
                
                self.listing.append(Note(self,**data))
        if not conf_exist:
            new_conf = {
                "Titre": "str",
                "Contenu": "str",
                "Modifi\u00e9e le": "date"
            }
            self.current_config = { "format" : new_conf, 
                                    "tree" : 0 , 
                                    "visi" : len(new_conf.keys()) } 
            
            with open(os.getcwd() + "/"+folder+"/config.json", mode = "w") as f:
                f.write(json.dumps(self.current_config))
        

    def sort_with_conf(self, _sort_param : list):
        """Trie du listing en fonction des parametres des filtres"""
        _sort_param.reverse()
        for _item in _sort_param:
            self.listing.sort(reverse=_item["revers"],key= lambda note : note[_item["name"]])

    def new_note(self):
        """Création d'une note vierge"""
        new_conf = {}
        for key, value in self.current_config["format"].items() :
            if value == "list":
                new_conf[key] = [""]
            elif value == "date":
                new_conf[key] = {
                    "annee": 2000,
                    "mois": 1,
                    "jour": 1,
                    "heure": 0,
                    "minute": 0,
                    "seconde": 0 }
            else :
                new_conf[key] = ""

            new_conf["Format"] = "texte"
            y = datetime.now().year
            m = datetime.now().month
            d = datetime.now().day
            h = datetime.now().hour
            n = datetime.now().minute
            s = datetime.now().second
            id = str(y)
            id += str(m) if len(str(m)) == 2 else "0" + str(m)
            id += str(d) if len(str(d)) == 2 else "0" + str(d)
            id += str(h) if len(str(h)) == 2 else "0" + str(h)
            id += str(n) if len(str(n)) == 2 else "0" + str(n)
            id += str(s) if len(str(s)) == 2 else "0" + str(s)

            new_conf["Cr\u00e9\u00e9e le"] = {
                    "annee": y,
                    "mois": m,
                    "jour": d,
                    "heure": h,
                    "minute": n,
                    "seconde": s }

            new_conf["Modifi\u00e9e le"] = {
                    "annee": y,
                    "mois": m,
                    "jour": d,
                    "heure": h,
                    "minute": n,
                    "seconde": s }

            new_conf["Titre"] = "Nouvelle note"
            new_conf["Id"] = id
        self.listing.append(Note(self,**new_conf))
        self.listing[-1].ecrire_json()
        self.root.list_box.set_select(id)

    def copy_note(self,_id):
        """Copie d'une Note existante"""
        new_conf = {}
        for note in self.listing:
            if note["Id"] == _id:
                for key, value in dict(note).items() :
                    if type(value) == type(list()):
                        new_conf[key] = []
                        for item in value:
                            new_conf[key].append(str(item))
                    elif type(value) == type(dict()):
                        new_conf[key] = {
                            "annee": int(value["annee"]),
                            "mois": int(value["annee"]),
                            "jour": int(value["annee"]),
                            "heure": int(value["annee"]),
                            "minute": int(value["annee"]),
                            "seconde": int(value["annee"]) }
                    else :
                        new_conf[key] = str(value)

                y = datetime.now().year
                m = datetime.now().month
                d = datetime.now().day
                h = datetime.now().hour
                n = datetime.now().minute
                s = datetime.now().second
                id = str(y)
                id += str(m) if len(str(m)) == 2 else "0" + str(m)
                id += str(d) if len(str(d)) == 2 else "0" + str(d)
                id += str(h) if len(str(h)) == 2 else "0" + str(h)
                id += str(n) if len(str(n)) == 2 else "0" + str(n)
                id += str(s) if len(str(s)) == 2 else "0" + str(s)

                new_conf["Cr\u00e9\u00e9e le"] = {
                        "annee": y,
                        "mois": m,
                        "jour": d,
                        "heure": h,
                        "minute": n,
                        "seconde": s }

                new_conf["Modifi\u00e9e le"] = {
                        "annee": y,
                        "mois": m,
                        "jour": d,
                        "heure": h,
                        "minute": n,
                        "seconde": s }
                new_conf["Titre"] = "Copie de " + new_conf["Titre"]
                new_conf["Id"] = id
                self.listing.append(Note(self,**new_conf))
                self.listing[-1].ecrire_json()
                self.root.list_box.set_select(id)
                break

    def sup_note(self,_id):
        """Copie d'une Note existante"""
        for i in range(len(self.listing)):
            if self.listing[i]["Id"] == _id:
                sup_note = self.listing.pop(i)
                sup_note.remove_json()
                del sup_note
                break
        self.root.list_box.set_select(None)
        


class Note(dict):
    
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__( self, master, **kwarg):
        """Création d'une nouvelle Note"""
        super().__init__()
        self.master = master                  # WIDGET PARENT 
        for name, val in kwarg.items():       # PARAMETRAGE DU Dict : 
            if type(val) == type(dict()):
                self[name] = Horodate(**val)  #   date -> cree_le, modifiee_le
            else:                             #   str  -> titre, format, contenu, id
                self[name] = val              #   list -> langage, bibliotheque, categorie, chapitre, auteur, tags, liaisons

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    @property
    def root(self):
        """Widget le plus haut hiérarchiquement"""
        return self.master.root
  
    @property
    def values(self):
        """Les valeurs de la Note affichées dans le Treeview"""
        result = []
        for item in self.root.sort_param:
            key = item["name"]
            if type(self[key]) == type(list()):
                if len(self[key]) == 0:
                    result.append("")
                else:
                    txt = self[key][0]
                    if len(self[key]) >= 2:
                        for item in self[key][1:]:
                            txt += ", " + item
                    result.append(txt)
            else:
                result.append(str(self[key]))
        return result
        
    def tree_values(self,value_key):
        """Ensemble des informations nécessaires à la création des lignes dans le Treeview"""
        #=====================================================Sub
        def combin(val_A,val_B):
            combin_result = []
            if type(val_A) == type(list()):
                if type(val_B) == type(list()):
                    for va in val_A : 
                        for vb in val_B : 
                            combin_result.append(va+"#"+vb)
                else:
                    for va in val_A : 
                        combin_result.append(va+"#"+str(val_B))
            else:
                if type(val_B) == type(list()):
                    for vb in val_B : 
                        combin_result.append(str(val_A)+"#"+vb)
                else:
                    combin_result.append(str(val_A)+"#"+str(val_B)) 
            return combin_result
        #=====================================================Sub
        def spliting(_txt):
            if not "#" in _txt:
                return ("", _txt,_txt)
            else:
                last_tag_pos = None
                for i in range(len(_txt)-1,-1,-1):
                    if _txt[i]=="#":
                        last_tag_pos = i
                        break
                return (_txt[:last_tag_pos], _txt,_txt[last_tag_pos+1:])

        #========================================================Script
        result = []
        for param_A in self.root.sort_param:
            key_prim = param_A["name"]
            tampon = self[key_prim]
            if type(tampon) == type(str()) : tampon = [tampon]
            elif type(tampon) == type(Horodate()) : 
                tampon = [str(tampon)]
            kl = []

            for param_B in self.root.sort_param:
                key_sec = param_B["name"]
                if key_sec == key_prim: break
                kl.append(key_sec)

            for i in range(len(kl)-1, -1,-1):
                tampon = combin(self[kl[i]],tampon)
            for item in tampon:
                (asc , path, name) = spliting(item)
                frt = "d" if key_prim == value_key else "t"
                result.append((asc , path, name, frt))
            if key_prim == value_key: break
        return result


    @property
    def json_dict(self):
        """La note au format json"""
        result=dict(self)
        result["Modifi\u00e9e le"] = {
            "annee" : datetime.now().year,
            "mois" : datetime.now().month,
            "jour" : datetime.now().day,
            "heure" : datetime.now().hour,
            "minute" : datetime.now().minute,
            "seconde" : datetime.now().second
        }
        return result

    def ecrire_json(self):
        """Sauvegarder la Note dans son Dossier"""
        with open(os.getcwd() + "/"+ self.root.cur_path +"/"+ self["Id"] +".json", mode = "w") as f:
            f.write(json.dumps(self.json_dict))

    def remove_json(self):
        """Supprimer la Note de son Dossier"""
        os.remove(os.getcwd() + "/"+ self.root.cur_path +"/"+ self["Id"] +".json")

    

class Horodate(dict):
    """Une Date au format dict() et jj/mm/aaaa hh:mm:ss"""
    
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    def __init__( self,annee = 2000,mois = 1, jour=1,heure=0,minute=0,seconde=0):
        """Création d'une nouvelle Horodate"""
        super().__init__()
        self["annee"] = annee                   # ANNEE
        self["mois"] = mois                     # MOIS
        self["jour"] = jour                     # JOUR
        self["heure"] = heure                   # HEURES
        self["minute"] = minute                 # MINUTES
        self["seconde"] = seconde               # SECONDES

    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ METHODE NATIVES ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EGALE
    def __eq__(self, value):
        """Equale ?"""
        return (
            self["annee"] == value["annee"]
            and self["mois"] == value["mois"]
            and self["jour"] == value["jour"]
            and self["heure"] == value["heure"]
            and self["minute"] == value["minute"]
            and self["seconde"] == value["seconde"]
            )
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ DIFFERENT
    def __ne__(self, value):
        """Différente ?"""
        return not self == value
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ PLUS PETIT
    def __lt__(self, value):
        """Plus petite ?"""
        if self["annee"] < value["annee"]:
            return True
        elif self["annee"] > value["annee"]:
            return False
        else:
            if self["mois"] < value["mois"]:
                return True
            elif self["mois"] > value["mois"]:
                return False
            else:
                if self["jour"] < value["jour"]:
                    return True
                elif self["jour"] > value["jour"]:
                    return False
                else:
                    if self["heure"] < value["heure"]:
                        return True
                    elif self["heure"] > value["heure"]:
                        return False
                    else:
                        if self["minute"] < value["minute"]:
                            return True
                        elif self["minute"] > value["minute"]:
                            return False
                        else:
                            if self["seconde"] < value["seconde"]:
                                return True
                            else:
                                return False
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ PLUS GRAND OU EGALE
    def __ge__(self, value):
        """Plus grande ou égale ?"""
        return not self < value
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ PLUS GRAND
    def __gt__(self, value):
        """Plus grande ?"""
        return self >= value and not self == value
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ PLUS PETIT OU EGALE
    def __le__(self, value):
        """Plus petite ou égale ?"""
        return not self > value
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ TEXTE
    def __str__(self):
        """Au format texte (str)"""
        result = str(self["jour"]) if len(str(self["jour"])) == 2 else "0" + str(self["jour"])
        result += "/"
        result += str(self["mois"]) if len(str(self["mois"])) == 2 else "0" + str(self["mois"])
        result += "/"
        result += str(self["annee"])
        result += " "
        result += str(self["heure"]) if len(str(self["heure"])) == 2 else "0" + str(self["heure"])
        result += ":"
        result += str(self["minute"]) if len(str(self["minute"])) == 2 else "0" + str(self["minute"])
        result += ":"
        result += str(self["seconde"]) if len(str(self["seconde"])) == 2 else "0" + str(self["seconde"])
        
        return result
    



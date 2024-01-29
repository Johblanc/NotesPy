

#-> Filtres()
    #-> RACCOURCIS
        #-> .root                                   -> Tk.obj   | Proprieté | Read only | Le Widget de plus haut niveau
        #-> .note_folder                            -> Folder   | Proprieté | Read only | Listes des notes dans le dossier en cours
        
    #-> CONFIGURATIONS DES FILTRES (ENTREES)
        #-- .__conf                                 -> dict     | Proprieté | Private   | Configuration courante des filtres
        #-- .__frames                               -> Frame    | Proprieté | Private   | FiltresBoxes
        #-- .__cur_checks                           -> dict     | Proprieté | Private   | Dico des references pour les filtre au format liste
        #<> .conf                                   -> dict     | Proprieté | Active    | Réglage de la configuration des Filtres et met à jour l'affichage.\nLa valeur doit être un dictionnaire.\n{ param_1 : format_1, param_2 : format_2, ... , param_n : format_n }\nLes KEYS correspondent aux noms des parametres filtrables.\nLes VALUES sont les formats de données de ces derniers. "str" | "list" | "date"
        #-> .add_Check( _key : str, _value : str)   -> None     | Methode   | Publique  | Ajout d'une checkbox à une filterbox si elle n'existe pas déjà

    #-> PARAMETRAGES DES FILTRES (SORTIES)
        #-- .__visi_lvl                             -> int      | Proprieté | Private   | Nombre de niveaux visible
        #-- .__tree_lvl                             -> int      | Proprieté | Private   | Nombre de niveaux pliant
        #<- .is_OK(note : Note)                     -> bool     | Methode   | Publique  | Cette note passe-t-elle les filtres en cours
        #<> .visi_lvl                               -> int      | Proprieté | Active    | Réglage de l'affiche des boutons de visibilité.
        #<> .tree_lvl                               -> int      | Proprieté | Active    | Réglage de l'affiche des boutons de hierarchisation.
        #-> .switch(_num_A : int, _num_B : int)     -> None     | Methode   | Publique  | Inverse la position de deux filterboxes

    #-> PLACEMENT DES FILTERBOXES
        #-- .__offset                               -> int      | Proprieté | Private   | Decalage de la fenetre
        #-- .__frm_height                           -> int      | Proprieté | Private   | Hauteur de la fenetre
        #-- .__frm_width                            -> int      | Proprieté | Private   | Largeur de la fenetre
        #-> .reset_cur_checks()                     -> None     | Methode   | Publique  | Mise à zero des CheckBoxes visibles
        #-> .verif_visibility()                     -> None     | Methode   | Publique  | Vérification de la visibilité de chaque checkbox
        #-> .reset_place()                          -> None     | Methode   | Publique  | Correction du placement des filterboxes en fonction de l'offset et des animations en cours
        #-> .scroll(_event = None)                  -> None     | Methode   | Private   | Réaction à un event de scrolling. Modifiction de l'offset
        #<- .hauteur                                -> int      | Proprieté | Read only | Hauteur totale des filterboxes
     
    #-> PLIAGE DU VOLET FILTRES
        #-> .__fold_false                           -> str      | Proprieté | Private   | Texte du bouton si le volet est deplié
        #-> .__fold_true                            -> str      | Proprieté | Private   | Texte du bouton si le volet est plié
        #-> .__btn                                  -> Button   | Proprieté | Private   | Bouton permetant de plier / deplier le volet
        #-> .__switch_width()                       -> None     | Methode   | Private   | Plie le volet si il est déplié en vise versa
        #-> .__on_Resize(_event=None)               -> None     | Methode   | Private   | Réaction au redimentionnement de la fenetre
        #-> .__with_options()                       -> None     | Methode   | Private   | Affichage des filtres avec options
        #-> .__no_option()                          -> None     | Methode   | Private   | Affichage des filtres sans options
        #-> .__no_filter()                          -> None     | Methode   | Private   | Masquage des filtres

#======================================================= NOTE =======================================================
# Note
#   |-> INITIALISATION
#   |       |-> .parent                 ⇶ WIDGET PARENT
#   |       |-> ["langage"]             ⇶ LISTE DES LANGAGES
#   |       |-> ["bibliotheque"]        ⇶ LISTE DES BIBLIOTHEQUES
#   |       |-> ["categorie"]           ⇶ LISTE DES CATEGORIES
#   |       |-> ["chapitre"]            ⇶ LISTE DES CHAPITRES
#   |       |-> ["auteur"]              ⇶ LISTE DES AUTEURS
#   |       |-> ["Tags"]                ⇶ LISTE DES TAGS
#   |       |-> ["liaisons"]            ⇶ LISTE DES LIAISONS
#   |       |-> ["Titre"]               ⇶ VALEUR DU TITRE
#   |       |-> ["Format"]              ⇶ VALEUR DU FORMAT
#   |       |-> ["Contenu"]             ⇶ VALEUR DU CONTENU
#   |       |-> ["Id"]                  ⇶ VALEUR DE L'ID
#   |       |-> ["Cr\u00e9\u00e9e le"]             ⇶ VALEUR DE LA DATE DE CREATION
#   |       '-> ["Modifi\u00e9e le"]         ⇶ VALEUR DE LA DATE DE MODIFICATION
#   | 
#   |-> RACCOURCIS
#   |       |-> .mastr                  ⇶ LE PLUS HAUT WIDGET
#   |       '-> .sort_order             ⇶ CONFIGURATION DES FILTRES
#   | 
#   |-> METHODE NATIVES
#   |       |-> ==                      ⇶ EGALE
#   |       |-> !=                      ⇶ DIFFERENT
#   |       |-> <                       ⇶ PLUS PETIT
#   |       |-> >=                      ⇶ PLUS GRAND OU EGALE
#   |       |-> >                       ⇶ PLUS GRAND
#   |       '-> <=                      ⇶ PLUS PETIT OU EGALE
#   | 
#   '-> VALEURS
#           '-> .values                 ⇶ LISTE DE VALEURS TEXTUELLES

#===================================================== HORODATE =====================================================
# Horodate
#   |-> INITIALISATION
#   |       |-> ["annee"]               ⇶ ANNEE
#   |       |-> ["mois"]                ⇶ MOIS
#   |       |-> ["jour"]                ⇶ JOUR
#   |       |-> ["heure"]               ⇶ HEURES
#   |       |-> ["minute"]              ⇶ MINUTES
#   |       '-> ["seconde"]             ⇶ SECONDES
#   | 
#   '-> METHODE NATIVES
#           |-> ==                      ⇶ EGALE
#           |-> !=                      ⇶ DIFFERENT
#           |-> <                       ⇶ PLUS PETIT
#           |-> >=                      ⇶ PLUS GRAND OU EGALE
#           |-> >                       ⇶ PLUS GRAND
#           '-> <=                      ⇶ PLUS PETIT OU EGALE
#           '-> str()                   ⇶ TEXTE jj/mm/aaaa hh:mm:ss

#==================================================== BOX_FILTRE ====================================================
# Box_filtre
#   |-> INITIALISATION
#   |       |-> .parent                 ⇶ WIDGET PARENT
#   |       |-> .name                   ⇶ NOM DU FILTRE
#   |       |-> .fold                   ⇶ LE MENU EST-IL PLIER ?
#   |       |-> .hauteur                ⇶ HAUTEUR ACTUELLE
#   |       |-> .order                  ⇶ INDEX DU FILTRE
#   |       |-> .label                  ⇶ LE LABEL DE TITRE
#   |       |-> .btn_Tree               ⇶ LE BOUTON TREE
#   |       |-> .btn_Visi               ⇶ LE BOUTON VISI
#   |       |-> .btn_Sort               ⇶ LE BOUTON SORT REVERS
#   |       |-> .btn_Up                 ⇶ LE BOUTON POSITION UP
#   |       '-> .btn_Dw                 ⇶ LE BOUTON POSITION DOWN
#   | 
#   |-> RACCOURCIS
#   |       '-> .mastr                  ⇶ LE PLUS HAUT WIDGET
#   | 
#   |-> PLIAGE DU MENU
#   |       |-> .toggle_fold(event)     ⇶ SWITCHER L'ETAT DU PLIAGE
#   |       |-> .hauteur_cible          ⇶ HAUTEUR A ATTEINDRE (Animation)
#   |       |-> .fold_transition        ⇶ HAUTEUR CIBLE ATTEINTE (Animation)
#   |       '-> .update_hauteur():      ⇶ MISE A JOUR DE LA HAUTEUR (Animation)
#   | 
#   |-> EST TRIE EN REVERS DANS LA LISTBOX
#   |       |-> .sort_revers            ⇶ GET
#   |       '-> .toggle_sort_revers()   ⇶ EVENT
#   | 
#   |-> PRESENCE DANS LA LISTBOX
#   |       |-> .visi                   ⇶ GET
#   |       |-> .visi                   ⇶ SET
#   |       '-> .toggle_visi()          ⇶ EVENT
#   | 
#   |-> EST UN DOSSIER OU UNE DONNEE DANS LA LISTBOX
#   |       |-> .tree                   ⇶ GET
#   |       |-> .tree                   ⇶ SET
#   |       '-> .toggle_tree()          ⇶ EVENT
#   | 
#   |-> POSITION DANS LA LISTBOX
#   |       |-> .move_up()              ⇶ REMONTER DANS LA HIERARCHIE
#   |       |-> .move_down()            ⇶ DESCENDRE DANS LA HIERARCHIE
#   |       |-> .enable_all()           ⇶ RENDRE ACTIF LES DEUX BOUTONS
#   |       |-> .disable_Up():          ⇶ RENDRE INACTIF LE BOUTON UP
#   |       '-> .disable_Down():        ⇶ RENDRE INACTIF LE BOUTON DOWN
#   | 
#   '-> VALIDATION DES DONNEES
#           |-> .val                    ⇶ VALEUR DU FILTRE
#           |-> .param                  ⇶ PARAMETRES DU FILTRE
#           '-> .is_OK(ref )            ⇶ LA DONNEE EST-ELLE VALIDE

#=================================================== ENTRY_FILTRE ===================================================
# Entry_filtre
#   |-> INITIALISATION
#   |       |-> .parent                 ⇶ WIDGET PARENT
#   |       |-> .name                   ⇶ NOM DU FILTRE
#   |       |-> .fold                   ⇶ LE MENU EST-IL PLIER ?
#   |       |-> .hauteur                ⇶ HAUTEUR ACTUELLE
#   |       |-> .order                  ⇶ INDEX DU FILTRE
#   |       |-> .label                  ⇶ LE LABEL DE TITRE
#   |       |-> .btn_Tree               ⇶ LE BOUTON TREE
#   |       |-> .btn_Visi               ⇶ LE BOUTON VISI
#   |       |-> .btn_Sort               ⇶ LE BOUTON SORT REVERS
#   |       |-> .btn_Up                 ⇶ LE BOUTON POSITION UP
#   |       |-> .btn_Dw                 ⇶ LE BOUTON POSITION DOWN
#   |       |-> .var                    ⇶ VALEUR DE L'ENTRYBOX
#   |       '-> .entry                  ⇶ ENTRYBOX
#   | 
#   |-> RACCOURCIS
#   |       '-> .mastr                  ⇶ LE PLUS HAUT WIDGET
#   | 
#   |-> PLIAGE DU MENU
#   |       |-> .toggle_fold(event)     ⇶ SWITCHER L'ETAT DU PLIAGE
#   |       |-> .hauteur_cible          ⇶ HAUTEUR A ATTEINDRE (Animation)
#   |       |-> .fold_transition        ⇶ HAUTEUR CIBLE ATTEINTE (Animation)
#   |       '-> .update_hauteur():      ⇶ MISE A JOUR DE LA HAUTEUR (Animation)
#   | 
#   |-> EST TRIE A L'ENVERS DANS LA LISTBOX
#   |       |-> .sort_revers            ⇶ GET
#   |       '-> .toggle_sort_revers()   ⇶ EVENT
#   | 
#   |-> PRESENCE DANS LA LISTBOX
#   |       |-> .visi                   ⇶ GET
#   |       |-> .visi                   ⇶ SET
#   |       '-> .toggle_visi()          ⇶ EVENT
#   | 
#   |-> EST UN DOSSIER OU UNE DONNEE DANS LA LISTBOX
#   |       |-> .tree                   ⇶ GET
#   |       |-> .tree                   ⇶ SET
#   |       '-> .toggle_tree()          ⇶ EVENT
#   | 
#   |-> POSITION DANS LA LISTBOX
#   |       |-> .move_up()              ⇶ REMONTER DANS LA HIERARCHIE
#   |       |-> .move_down()            ⇶ DESCENDRE DANS LA HIERARCHIE
#   |       |-> .enable_all()           ⇶ RENDRE ACTIF LES DEUX BOUTONS
#   |       |-> .disable_Up():          ⇶ RENDRE INACTIF LE BOUTON UP
#   |       '-> .disable_Down():        ⇶ RENDRE INACTIF LE BOUTON DOWN
#   | 
#   '-> VALIDATION DES DONNEES
#           |-> .val                    ⇶ VALEUR DU FILTRE
#           |-> .param                  ⇶ PARAMETRES DU FILTRE
#           '-> .is_OK(ref )            ⇶ LA DONNEE EST-ELLE VALIDE

#================================================= CHECKBOX_FILTRE ==================================================
# Checkbox_filtre
#   |-> INITIALISATION
#   |       |-> .parent                 ⇶ WIDGET PARENT
#   |       |-> .name                   ⇶ NOM DU FILTRE
#   |       |-> .fold                   ⇶ LE MENU EST-IL PLIER ?
#   |       |-> .hauteur                ⇶ HAUTEUR ACTUELLE
#   |       |-> .order                  ⇶ INDEX DU FILTRE
#   |       |-> .label                  ⇶ LE LABEL DE TITRE
#   |       |-> .btn_Tree               ⇶ LE BOUTON TREE
#   |       |-> .btn_Visi               ⇶ LE BOUTON VISI
#   |       |-> .btn_Sort               ⇶ LE BOUTON SORT REVERS
#   |       |-> .btn_Up                 ⇶ LE BOUTON POSITION UP
#   |       |-> .btn_Dw                 ⇶ LE BOUTON POSITION DOWN
#   |       |-> .val_list               ⇶ LISTE DES VALEURS
#   |       |-> .visi_list              ⇶ LISTE DES VALEURS VISIBLES
#   |       |-> .var_Type               ⇶ LISTE DES VARIABLES DES CHECKBOXES
#   |       '-> .chBs_Type              ⇶ LISTE DES CHECKBOXES
#   | 
#   |-> RACCOURCIS
#   |       '-> .mastr                  ⇶ LE PLUS HAUT WIDGET
#   | 
#   |-> PLIAGE DU MENU
#   |       |-> .toggle_fold(event)     ⇶ SWITCHER L'ETAT DU PLIAGE
#   |       |-> .hauteur_cible          ⇶ HAUTEUR A ATTEINDRE (Animation)
#   |       |-> .fold_transition        ⇶ HAUTEUR CIBLE ATTEINTE (Animation)
#   |       '-> .update_hauteur():      ⇶ MISE A JOUR DE LA HAUTEUR (Animation)
#   | 
#   |-> EST TRIE EN REVERS DANS LA LISTBOX
#   |       |-> .sort_revers            ⇶ GET
#   |       '-> .toggle_sort_revers()   ⇶ EVENT
#   | 
#   |-> PRESENCE DANS LA LISTBOX
#   |       |-> .visi                   ⇶ GET
#   |       |-> .visi                   ⇶ SET
#   |       '-> .toggle_visi()          ⇶ EVENT
#   | 
#   |-> EST UN DOSSIER OU UNE DONNEE DANS LA LISTBOX
#   |       |-> .tree                   ⇶ GET
#   |       |-> .tree                   ⇶ SET
#   |       '-> .toggle_tree()          ⇶ EVENT
#   | 
#   |-> POSITION DANS LA LISTBOX
#   |       |-> .move_up()              ⇶ REMONTER DANS LA HIERARCHIE
#   |       |-> .move_down()            ⇶ DESCENDRE DANS LA HIERARCHIE
#   |       |-> .enable_all()           ⇶ RENDRE ACTIF LES DEUX BOUTONS
#   |       |-> .disable_Up():          ⇶ RENDRE INACTIF LE BOUTON UP
#   |       '-> .disable_Down():        ⇶ RENDRE INACTIF LE BOUTON DOWN
#   | 
#   '-> VALIDATION DES DONNEES
#           |-> .val                    ⇶ VALEUR DU FILTRE
#           |-> .param                  ⇶ PARAMETRES DU FILTRE
#           '-> .is_OK(ref )            ⇶ LA DONNEE EST-ELLE VALIDE
























    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ INITIALISATION ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ WIDGET PARENT
    #   self.parent
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ NOM DU FILTRE
    #   self.name
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE MENU EST-IL PLIER ?
    #   self.fold
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ HAUTEUR ACTUELLE
    #   self.hauteur
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ INDEX DU FILTRE
    #   self.order
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE LABEL DE TITRE
    #   self.label
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE BOUTON TREE
    #   self.btn_Tree
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE BOUTON VISI
    #   self.btn_Visi
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE BOUTON SORT REVERS
    #   self.btn_Sort
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE BOUTON POSITION UP
    #   self.btn_Up
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE BOUTON POSITION DOWN
    #   self.btn_Dw
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ RACCOURCIS ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LE PLUS HAUT WIDGET
    #   self.mastr
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ PLIAGE DU MENU ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ SWITCHER L'ETAT DU PLIAGE
    #   self.toggle_fold(event)
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ HAUTEUR A ATTEINDRE (Animation)
    #   self.hauteur_cible
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ HAUTEUR CIBLE ATTEINTE (Animation)
    #   self.fold_transition
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ MISE A JOUR DE LA HAUTEUR (Animation)
    #   self.update_hauteur():
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EST TRIE EN REVERS DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ GET
    #   self.sort_revers
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EVENT
    #   self.toggle_sort_revers()
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ PRESSENCE DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ GET
    #   self.visi
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ SET
    #   self.visi
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EVENT
    #   self.toggle_visi()
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ EST UN DOSSIER OU UNE DONNEE DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ GET
    #   self.tree
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ SET
    #   self.tree
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ EVENT
    #   self.toggle_tree()
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ POSITION DANS LA LISTBOX ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ REMONTER DANS LA HIERARCHIE
    #   self.move_up()
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ DESCENDRE DANS LA HIERARCHIE
    #   self.move_down()
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ RENDRE ACTIF LES DEUX BOUTONS
    #   self.enable_all()
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ RENDRE INACTIF LE BOUTON UP
    #   self.disable_Up():
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ RENDRE INACTIF LE BOUTON DOWN
    #   self.disable_Down():
    #⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕ VALIDATION DES DONNEES ⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕⇕
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ VALEUR DU FILTRE
    #   self.val
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ PARAMETRES DU FILTRE
    #   self.param
    #⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆⇄⇆ LA DONNEE EST-ELLE VALIDE
    #   self.is_OK(ref )



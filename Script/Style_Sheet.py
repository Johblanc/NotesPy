from .ttk_style_helper import Style_Config as SC, shack,style_group

LIST_ICONS = """
←	↑	→	↓	↔	↕	↖	↗	↘   ↙   ↚   ↛   ↜   ↝   ↞   ↟   ↠
↡   ↢   ↣   ↤   ↥   ↦   ↧   ↨   ↩   ↪   ↫   ↬   ↭   ↮   ↯   ↰   ↱
↲   ↳   ↴   ↵   ↶   ↷   ↸   ↹   ↺   ↻   ↼   ↽   ↾   ↿   ⇀   ⇁   ⇂
⇃   ⇄   ⇅   ⇆   ⇇   ⇈   ⇉   ⇊   ⇋   ⇌   ⇍   ⇎   ⇏   ⇐   ⇑   ⇒
⇓   ⇔   ⇕   ⇖   ⇗   ⇘   ⇙   ⇚   ⇛   ⇜   ⇝   ⇞   ⇟   ⇠   ⇡   ⇢   ⇣
⇤   ⇥   ⇦   ⇧   ⇨   ⇩   ⇪   ⇫   ⇬   ⇭   ⇮   ⇯   ⇰   ⇱   ⇲   ⇳   ⇴
⇵   ⇶   ⇷   ⇸   ⇹   ⇺   ⇻   ⇼   ⇽   ⇾   ⇿   ⊗	⊘	⊙	⊚    """


class Setting(style_group):
    def __init__(self,
            background = None,
            foreground = None,
            back_info = "#000011",
            fore_info = "#EEEEFF",
            back_view = "#080008",
            fore_view = "#FFDDFF",
            back_list = "#000808",
            fore_list = "#DDFFFF",
            fore_add = "#DDFFDD",
            fore_sup = "#FFDDDD",
            back_filt = "#080800",
            fore_filt = "#FFFFDD",
            relief = "flat", # "solid",
            padding = (0, 0, 0, 0),
            font = "Times", # "Helvetica" "Arial" "Times"
            item_space = 5,
            item_size = 25,
            fold_size = 25, 
            fore_alt_a = "#FF00FF", 
            fore_alt_b = "#FFFF00", 
            fore_alt_c = "#88FF88", 
            fore_alt_d = "#FF8888", 
            fore_alt_e = "#00FFFF", 
            fore_alt_f = "#8888FF"
            ) -> None:
        super().__init__()
        if background : back_info = back_view = back_list = back_filt = background
        if foreground : fore_info = fore_view = fore_list = fore_filt = foreground

        self.scroll_step = 40
        self.anim_delay = 20
        self.anim_step = 3000
        self.ico = {"croissant" : "↗", "decroissant" : "↘", "monter" : "⇑", "descendre" : "⇓", "visible" : "⊚", "invisible" : "X", "dossier": "↳", "donnee" : "-" }

        self.item_space = item_space
        self.item_size = item_size
        self.fold_size = fold_size
        self.options = {
            '*TCombobox*Listbox.background':shack(back_info,fore_info,80),
            '*TCombobox*Listbox.foreground': shack(back_info,fore_info,20),
            '*TCombobox*Listbox.font': font + " " + str(item_size//2),
            '*TCombobox*Listbox.selectBackground':shack(back_info,fore_info,90),
            '*TCombobox*Listbox.selectForeground':shack(back_info,fore_info,10)
        
        }

        self.menu_config = {
            "background" : back_info,
            "foreground" : fore_info,
            "activebackground" : shack(back_info,fore_info,90),
            "activeforeground" : fore_info,
            "font" : font

        }
        self["Info"] = self.Info(item_size,back_info,fore_info,fore_add,fore_sup,relief,padding,font,fold_size)
        self["View"] = self.View(back_view,fore_view,relief,font,item_size,item_space,padding)
        self["Listing"] = self.Listing(item_size,back_list,fore_list,relief,padding,font,fold_size)
        self["Filters"] = self.Filters(item_size,item_space,back_filt,fore_filt,relief,padding,font,fold_size, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f)
        self["Configurateur"] = self.Configurateur(item_size,item_space,back_filt,fore_filt,relief,padding,font,fold_size, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f)

    class Info(style_group):
        def __init__(self,item_size,background, foreground, fore_add, fore_sup, relief, padding, font, fold_size) -> None:
            super().__init__()
            self["Fond"] = self.Fond(background,relief)
            self["Add"] = self.Add(background,shack(background,foreground,90),fore_add,relief,padding,item_size)
            self["Sup"] = self.Sup(background,shack(background,foreground,90),fore_sup,relief,padding,item_size)
            self["Name"] = self.Name(shack(background,foreground,90),foreground,padding,font,item_size)
            self["Val"] = self.Val(shack(background,foreground,90),foreground,padding,font,item_size)
            self["Ent"] = self.Ent(shack(background,foreground,90),foreground,padding,font,item_size)
            self["Pan"] = self.Pan(shack(background,foreground,90),foreground,relief,padding,font,fold_size)

        class Fond(style_group):
            def __init__(self,background, relief) -> None:
                super().__init__()
                self["TFrame"] = SC.Frame(
                    background = background,
                    bordercolor = background,
                    relief = relief )

        class Add(style_group):
            def __init__(self,background_a,background_b,foreground,relief,padding,item_size) -> None:
                super().__init__()
                self["TCombobox"] = SC.Combobox(
                    arrowcolor = shack(background_b,foreground,60),
                    arrowsize = item_size - 5,
                    background = background_b,
                    bordercolor = background_b,
                    relief = relief,
                    foreground = foreground,
                    fieldbackground = background_b,
                    insertcolor = foreground)
                self["TCombobox"]["active"].arrowcolor  = shack(background_b,foreground,80)
                self["TCombobox"]["disabled"].arrowcolor  = background_b
                self["TCombobox"]["disabled"].foreground  = background_b


                self["TButton"] = SC.Button(
                    padding = padding,
                    background = background_b,
                    bordercolor = shack(background_b,foreground,90),
                    relief = relief,
                    foreground = foreground,
                    font = ("Arial", item_size//2, "bold") )
                self["TButton"]["active"].background     = shack(background_b,foreground,90)
                self["TButton"]["disabled"].background   = background_a
                self["TButton"]["disabled"].foreground   = shack(background_a,foreground,80)
                self["TButton"]["disabled"].bordercolor  = background_a

        class Sup(style_group):
            def __init__(self,background_a,background_b,foreground,relief,padding,item_size) -> None:
                super().__init__()
                self["TCombobox"] = SC.Combobox(
                    arrowcolor = shack(background_b,foreground,60),
                    arrowsize = item_size - 5,
                    background = background_b,
                    bordercolor = background_b,
                    relief = relief,
                    foreground = foreground,
                    fieldbackground = background_b,
                    insertcolor = foreground)
                self["TCombobox"]["active"].arrowcolor  = shack(background_b,foreground,80)
                self["TCombobox"]["disabled"].arrowcolor  = background_b
                self["TCombobox"]["disabled"].foreground  = background_b


                self["TButton"] = SC.Button(
                    padding = padding,
                    background = background_b,
                    bordercolor = shack(background_b,foreground,90),
                    relief = relief,
                    foreground = foreground,
                    font = ("Arial", item_size//3, "bold") )
                self["TButton"]["active"].background     = shack(background_b,foreground,90)
                self["TButton"]["disabled"].background   = background_a
                self["TButton"]["disabled"].foreground   = shack(background_a,foreground,80)
                self["TButton"]["disabled"].bordercolor  = background_a

        class Name(style_group):
            def __init__(self,background,foreground,padding,font,item_size) -> None:
                super().__init__()
                self["TLabel"] = SC.Label(
                    background = background,
                    foreground = foreground,
                    padding = padding,
                    font = (font, item_size//2, "bold") )

        class Val(style_group):
            def __init__(self,background,foreground,padding,font,item_size) -> None:
                super().__init__()
                self["TLabel"] = SC.Label(
                    background = background,
                    foreground = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

        class Ent(style_group):
            def __init__(self,background,foreground,padding,font,item_size) -> None:
                super().__init__()
                self["TEntry"] = SC.Entry(
                    background = background,
                    bordercolor = shack(background,foreground,90),
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

        class Pan(style_group):
            def __init__(self,background,foreground,relief,padding,font,item_size) -> None:
                super().__init__()
                self["TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = shack(background,foreground,20),
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["TButton"]["active"].background  = shack(background,foreground,70)
                self["TButton"]["active"].foreground  = shack(background,foreground,30)

    class View(style_group):
        def __init__(self,background, foreground, relief, font,item_size,item_space,padding) -> None:
            super().__init__()
            self.reader = {
                "font" : font + " " + str(item_size//2),
                "bg" : shack(background,foreground,90),
                "fg" : shack(background,foreground,15),
                "insertbackground" : shack(background,foreground,70),
                "insertunfocussed" : "solid",
                "inactiveselectbackground" : shack(background,foreground,70),
                "undo" : True,
                "maxundo" : 0,
                "spacing1" : item_space,
                "spacing2" : 0,
                "spacing3" : 0,
                "wrap" : "word",
                "relief" : relief
                }
            self.md_tags = {
                "t1"  : { "foreground" : foreground, "font" : font + " " + str((item_size+3*item_space)//2) + " bold" },
                "t2"  : { "foreground" : shack(background,foreground,5), "font" : font + " " + str((item_size+2*item_space)//2) + " bold" },
                "t3"  : { "foreground" : shack(background,foreground,10), "font" : font + " " + str((item_size+item_space)//2) + " bold" },
                "t4"  : { "foreground" : shack(background,foreground,15), "font" : font + " " + str(item_size//2) + " bold" },
                "ita" : { "foreground" : foreground, "font" : font + " " + str(item_size//2) + " italic" },
                "grs" : { "foreground" : foreground, "font" : font + " " + str(item_size//2) + " bold" },
                "sup" : { "foreground" : foreground, "font" : font + " " + str(item_size//2) + " italic bold" },
            }

            self["Fond"] = self.Fond(background,relief)
            self["Mode"] = self.Mode(shack(background,foreground,90),foreground,relief,font,item_size)
            self["Titre"] = self.Titre(shack(background,foreground,90),foreground,font,item_size,padding)
            self["Format"] = self.Format(shack(background,foreground,90),foreground,relief,item_size)

        class Fond(style_group):
            def __init__(self,background,relief) -> None:
                super().__init__()
                self["TFrame"] = SC.Frame(
                    background = background,
                    bordercolor = background,
                    relief = relief )
            
        class Mode(style_group):
            def __init__(self,background,foreground,relief,font,item_size) -> None:
                super().__init__()
                self["TButton"] = SC.Button(
                    background = shack(background,foreground,90),
                    foreground = foreground,
                    bordercolor = background,
                    relief = relief,
                    font = (font, (item_size * 2)//5))
                self["TButton"]["active"].background  = shack(background,foreground,80)
                self["TButton"]["disabled"].background  = background
                self["TButton"]["disabled"].foreground  = background
            
        class Titre(style_group):
            def __init__(self,background,foreground,font,item_size,padding) -> None:
                super().__init__()

                self["TLabel"] = SC.Label(
                    background = background,
                    foreground = foreground,
                    padding = padding,
                    font = (font, item_size,"bold") )

                self["TEntry"] = SC.Entry(
                    background = background,
                    bordercolor = shack(background,foreground,90),
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

        class Format(style_group):
            def __init__(self,background,foreground,relief,item_size) -> None:
                super().__init__()
                self["TCombobox"] = SC.Combobox(
                    arrowcolor = shack(background,foreground,60),
                    arrowsize = item_size - 5,
                    background = background,
                    bordercolor = background,
                    relief = relief,
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground)
                self["TCombobox"]["active"].arrowcolor  = shack(background,foreground,80)
                self["TCombobox"]["disabled"].arrowcolor  = background
                self["TCombobox"]["disabled"].foreground  = background

    class Listing(style_group):
        def __init__(self,item_size,background, foreground, relief, padding, font, fold_size) -> None:
            super().__init__()
            self["Pan"] = self.Pan(shack(background,foreground,90),foreground,relief,padding,font,fold_size)
            self["TW"] = self.TW(background,foreground,relief,font,item_size)

        class Pan(style_group):
            def __init__(self,background,foreground,relief,padding,font,item_size) -> None:
                super().__init__()
                self["TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = shack(background,foreground,20),
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["TButton"]["active"].background  = shack(background,foreground,70)
                self["TButton"]["active"].foreground  = shack(background,foreground,30)



        class TW(style_group):
            def __init__(self,background,foreground,relief,font,item_size) -> None:
                super().__init__()
                self.background = background
                self.foreground = foreground
                self.select = {
                    "background" : shack(background,foreground,30),
                    "foreground" : background
                    }
                self["Treeview"] = SC.Treeview(
                    background = background,
                    foreground = foreground,
                    bordercolor = background,
                    relief = relief,
                    fieldbackground = background,
                    rowheight = item_size,
                    font = (font, item_size//2))
                #self["Treeview"]["selected"].foreground = background
                #self["Treeview"]["selected"].background = shack(background,foreground,30)

                self["Treeview.Heading"] = self["Treeview"].heading
                self["Treeview.Heading"].config.background = shack(background,foreground,90)
                self["Treeview.Heading"].config.font = (font, item_size//2,"bold")
                self["Treeview.Heading"]["active"].background = shack(background,foreground,80)
                self["Treeview.Heading"]["active"].font = (font, item_size//2,"bold")

            def tags(self, lenght):
                result =  {}
                for i in range(lenght):
                    taux = 90 + (lenght - i ) * (10 / lenght)
                    result["Nv_" + str(i+1)] = {
                        "background" : shack(self.background,self.foreground,taux),
                        "foreground" : shack(self.background,self.foreground,20)}
                    result["Nv_" + str(i+1) + "_s"] = {
                        "background" : shack(self.background,self.foreground,30),
                        "foreground" : self.background}

                result["data"] = {
                    "background" : shack(self.background,self.foreground,90),
                    "foreground" : shack(self.background,self.foreground,20)}

                result["data_s"] = {
                    "background" : shack(self.background,self.foreground,30),
                    "foreground" : self.background}

                
                return result
                


    class Filters(style_group):
        def __init__(self,item_size,item_space,background, foreground, relief, padding, font, fold_size, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f) -> None:
            super().__init__()
            self["Fond"] = self.Fond(background,relief)
            self["Pan"] = self.Pan(shack(background,foreground,90),foreground,relief,padding,font,fold_size)
            self["Box"] = self.Box(shack(background,foreground,90),foreground,relief,padding,font,item_size,item_space, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f)

        class Fond(style_group):
            def __init__(self,background,relief) -> None:
                super().__init__()
                self["TFrame"] = SC.Frame(
                    background = background,
                    bordercolor = background,
                    relief = relief )

        class Pan(style_group):
            def __init__(self,background,foreground,relief,padding,font,item_size) -> None:
                super().__init__()
                self["TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = shack(background,foreground,20),
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["TButton"]["active"].background  = shack(background,foreground,70)
                self["TButton"]["active"].foreground  = shack(background,foreground,30)

        class Box(style_group):
            def __init__(self,background,foreground,relief,padding,font,item_size,item_space, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f) -> None:
                super().__init__()

                self["TFrame"] = SC.Frame(
                    background = background,
                    bordercolor = background,
                    relief = relief )

                self["Sub.TFrame"] = SC.Frame(
                    background = shack(background,foreground,90),
                    bordercolor = shack(background,foreground,90),
                    relief = relief )

                self["TLabel"] = SC.Label(
                    background = background,
                    foreground = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

                self["TCheckbutton"] = SC.Check(
                    background = shack(background,foreground,90),
                    compound = "left" ,
                    foreground = foreground,
                    indicatorbackground = background,
                    indicatorcolor = background,
                    indicatormargin = item_space,
                    indicatorrelief = relief,
                    padding = padding )
                self["TCheckbutton"]["active"].background  = shack(background,foreground,80)

                self["TEntry"] = SC.Entry(
                    background = background,
                    bordercolor = shack(background,foreground,90),
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

                self["TCombobox"] = SC.Combobox(
                    arrowcolor = shack(background,foreground,60),
                    arrowsize = item_size - 5,
                    background = background,
                    bordercolor = background,
                    relief = relief,
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground)
                self["TCombobox"]["active"].arrowcolor  = shack(background,foreground,80)
                self["TCombobox"]["disabled"].arrowcolor  = background
                self["TCombobox"]["disabled"].foreground  = background

                self["Data.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_a,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Data.TButton"]["active"].background  = shack(background,foreground,70)

                self["Tree.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_b,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Tree.TButton"]["active"].background  = shack(background,foreground,70)

                self["Visi.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_c,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Visi.TButton"]["active"].background  = shack(background,foreground,70)

                self["Not_Visi.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_d,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Not_Visi.TButton"]["active"].background  = shack(background,foreground,70)

                self["Sort.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_e,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Sort.TButton"]["active"].background  = shack(background,foreground,70)

                self["Move.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_f,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Move.TButton"]["active"].background  = shack(background,foreground,70)
                self["Move.TButton"]["disabled"].background  = background
                self["Move.TButton"]["disabled"].foreground  = background

    class Configurateur(style_group):
        def __init__(self,item_size,item_space,background, foreground, relief, padding, font, fold_size, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f) -> None:
            super().__init__()
            self.background = background
            self["Box"] = self.Box(shack(background,foreground,90),foreground,relief,padding,font,item_size,item_space, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f)


        class Box(style_group):
            def __init__(self,background,foreground,relief,padding,font,item_size,item_space, 
                            fore_alt_a, fore_alt_b, fore_alt_c, fore_alt_d, fore_alt_e, fore_alt_f) -> None:
                super().__init__()

                self["TFrame"] = SC.Frame(
                    background = background,
                    bordercolor = background,
                    relief = relief )

                self["Sub.TFrame"] = SC.Frame(
                    background = shack(background,foreground,90),
                    bordercolor = shack(background,foreground,90),
                    relief = relief )

                self["TLabel"] = SC.Label(
                    background = background,
                    foreground = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

                self["Titre.TLabel"] = SC.Label(
                    background = shack(background,foreground,80),
                    foreground = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

                self["TEntry"] = SC.Entry(
                    background = background,
                    bordercolor = shack(background,foreground,90),
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground,
                    padding = padding,
                    font = (font, item_size//2) )

                self["TSpinbox"] = SC.Spinbox(
                    arrowcolor = shack(background,foreground,60),
                    arrowsize = (item_size - 5)/2,
                    background = background,
                    bordercolor = background,
                    relief = relief,
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground)

                self["TCombobox"] = SC.Combobox(
                    arrowcolor = shack(background,foreground,60),
                    arrowsize = item_size - 5,
                    background = background,
                    bordercolor = background,
                    relief = relief,
                    foreground = foreground,
                    fieldbackground = background,
                    insertcolor = foreground)
                self["TCombobox"]["active"].arrowcolor  = shack(background,foreground,80)
                self["TCombobox"]["disabled"].arrowcolor  = background
                self["TCombobox"]["disabled"].foreground  = background


                self["In.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = foreground,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2))
                self["In.TButton"]["active"].background  = shack(background,foreground,70)

                self["Sup.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_d,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Sup.TButton"]["active"].background  = shack(background,foreground,70)

                self["Move.TButton"] = SC.Button(
                    background = shack(background,foreground,80),
                    foreground = fore_alt_f,
                    bordercolor = background,
                    relief = relief,
                    padding = padding,
                    font = (font, item_size//2, "bold"))
                self["Move.TButton"]["active"].background  = shack(background,foreground,70)
                self["Move.TButton"]["disabled"].background  = background
                self["Move.TButton"]["disabled"].foreground  = background

























class flex_dict(dict):
    def __init__(self, **kwarg) -> None:
        super().__init__()
        for key, arg in kwarg.items():
            self[key]  = arg

    def __getattribute__(self, __name: str):
        if __name == "__class__":
            return type.__class__(flex_dict)
        elif __name == "keys":
            def keys() : return list(set(self))
            return keys
        else:
            return self[__name]

    def __setattr__(self, __name: str, __value):
        self[__name] = __value


class flex_style(dict):
    def __init__(self, **kwarg) -> None:
        super().__init__()
        for key, arg in kwarg.items():
            self[key] = arg
        self.config = {}

        

    @property
    def map(self):
        result = {}
        for param in self.config.keys():
            result[param] = []
            for state , value in self.items():
                if state in ["active","disabled","focus","pressed","selected","background","readonly","alternate","invalid"]:
                    result[param].append((state , value[param]))
        return result

class style_group(dict):
    def __init__(self) -> None:
        super().__init__()

    @property
    def config(self):
        result = {}
        for key_a , val_a in self.items():
            if isinstance(val_a,style_group):
                for key_b, val_b in val_a.config.items():
                    result[key_a + "." + key_b] = val_b
            else:
                result[key_a] = val_a.config
        return result

    @property
    def map(self):
        result = {}
        for key_a , val_a in self.items():
            if isinstance(val_a,style_group):
                for key_b, val_b in val_a.map.items():
                    result[key_a + "." + key_b] = val_b
            else:
                result[key_a] = val_a.map
        return result


        


class Style_Config():
    class Frame(flex_style):
        def __init__(self,background = "#000000", bordercolor = "#000000", relief = "solid"):
            super().__init__()
            self.config = self.Conf(background, bordercolor, relief)

        class Conf(flex_dict):
            def __init__(self,background = "#000000", bordercolor = "#000000", relief = "solid") -> None:
                super().__init__()
                self.background = background
                self.bordercolor = bordercolor
                self.relief = relief

    class Combobox(flex_style):
        def __init__(self, arrowcolor = "#FFFFFF", arrowsize = 20, background = "#000000",
                        bordercolor = "#000000", relief = "solid", foreground = "#FFFFFF",
                        fieldbackground = "#000000", insertcolor = "#FFFFFF" ):
            super().__init__()
            self.config = self.Conf(arrowcolor, arrowsize, background, bordercolor, relief, foreground,
                        fieldbackground, insertcolor)
            self["active"]   = self.Conf(**self.config)
            self["disabled"] = self.Conf(**self.config)
            self["readonly"] = self.Conf(**self.config)

        class Conf(flex_dict):
            def __init__(self, arrowcolor, arrowsize, background, bordercolor, relief, foreground,
                        fieldbackground, insertcolor) -> None:
                super().__init__()
                self.arrowcolor = arrowcolor
                self.arrowsize = arrowsize
                self.background = background
                self.bordercolor = bordercolor
                self.relief = relief
                self.foreground = foreground
                self.fieldbackground = fieldbackground
                self.insertcolor = insertcolor


    class Button(flex_style):
        def __init__(self, padding = (0, 0, 0, 0), background = "#000000", bordercolor = "#000000",
                    relief = "solid", foreground = "#FFFFFF", font = ("Arial", 12, "bold")):
            super().__init__()
            self.config      = self.Conf(padding = padding, background = background, bordercolor = bordercolor, 
                                        relief = relief, foreground = foreground, font = font)
            self["active"]   = self.Conf(**self.config)
            self["disabled"] = self.Conf(**self.config)
        
        class Conf(flex_dict):
            def __init__(self, padding = (0, 0, 0, 0), background = "#000000", bordercolor = "#000000",
                        relief = "solid", foreground = "#FFFFFF", font = ("Arial", 12, "bold")):
                super().__init__()
                self.padding = padding
                self.background = background
                self.bordercolor = bordercolor
                self.relief = relief
                self.foreground = foreground
                self.font = font

    class Label(flex_style):
        def __init__(self, padding = (0, 0, 0, 0), background = "#000000", foreground = "#FFFFFF", 
                        font = ("Helvetica", 12)):
            super().__init__()
            self.config      = self.Conf(padding, background, foreground, font)

        class Conf(flex_dict):
            def __init__(self, padding, background, foreground, font):
                super().__init__()
                self.padding = padding
                self.background = background
                self.foreground = foreground
                self.font = font

    class Entry(flex_style):
        def __init__(self, padding = (0, 0, 0, 0), background = "#000000", bordercolor = "#000000",
                    foreground = "#FFFFFF", font = ("Helvetica", 12),
                    fieldbackground = "#000000", insertcolor = "#FFFFFF" ):
            super().__init__()
            self.config      = self.Conf(padding, background, bordercolor, foreground, font,
                        fieldbackground, insertcolor)

        class Conf(flex_dict):
            def __init__(self, padding, background, bordercolor, foreground, font,
                        fieldbackground, insertcolor):
                super().__init__()
                self.padding = padding
                self.background = background
                self.bordercolor = bordercolor
                self.foreground = foreground
                self.font = font
                self.fieldbackground = fieldbackground
                self.insertcolor = insertcolor


    class Treeview(flex_style):
        def __init__(self, background = "#000000", bordercolor = "#000000",
                    foreground = "#FFFFFF", font = ("Helvetica", 12),
                    fieldbackground = "#000000", relief = "solid" ,rowheight = 25):
            self.config  = self.Conf(background, bordercolor, foreground, font, fieldbackground, relief,rowheight)
            self.heading = self.Heading(background, bordercolor, foreground, font, relief,rowheight)
            #self["active"]   = self.Conf(**self.config)
            #self["selected"]   = self.Conf(**self.config)

        class Conf(flex_dict):
            def __init__(self, background, bordercolor, foreground, font,
                        fieldbackground, relief,rowheight):
                super().__init__()
                self.background = background
                self.bordercolor = bordercolor
                self.relief = relief
                self.foreground = foreground
                self.font = font
                self.fieldbackground = fieldbackground
                self.rowheight = rowheight


        class Heading(flex_style):
            def __init__(self, background = "#000000", bordercolor = "#000000",
                        foreground = "#FFFFFF", font = ("Helvetica", 12), relief = "solid" ,rowheight = 25):
                self.config      = self.Conf(background, bordercolor, foreground, font, relief,rowheight)
                self["active"]   = self.Conf(**self.config)

            class Conf(flex_dict):
                def __init__(self, background, bordercolor, foreground, font, relief, rowheight):
                    super().__init__()
                    self.background = background
                    self.bordercolor = bordercolor
                    self.relief = relief
                    self.foreground = foreground
                    self.font = font
                    self.rowheight = rowheight


    class Check(flex_style):
        def __init__(self, background = "#000000", compound = "left",
                    foreground = "#FFFFFF", indicatorbackground = "#000000", indicatorcolor = "#FFFFFF", 
                    indicatormargin = (0, 0, 0, 0), indicatorrelief = "solid", padding = (0, 0, 0, 0)):
            super().__init__()
            self.config      = self.Conf(background, compound, foreground, indicatorbackground,
                        indicatorcolor, indicatormargin, indicatorrelief,padding)
            self["active"]   = self.Conf(**self.config)

        class Conf(flex_dict):
            def __init__(self, background, compound, foreground, indicatorbackground,
                        indicatorcolor, indicatormargin, indicatorrelief,padding):
                super().__init__()
                self.background = background
                self.compound = compound 
                self.foreground = foreground
                self.indicatorbackground = indicatorbackground
                self.indicatorcolor = indicatorcolor
                self.indicatormargin = indicatormargin
                self.indicatorrelief = indicatorrelief
                self.padding = padding

    class Spinbox(flex_style):
        def __init__(self, arrowcolor = "#FFFFFF", arrowsize = 20, background = "#000000",
                        bordercolor = "#000000", relief = "solid", foreground = "#FFFFFF",
                        fieldbackground = "#000000", insertcolor = "#FFFFFF" ):
            super().__init__()
            self.config = self.Conf(arrowcolor, arrowsize, background, bordercolor, relief, foreground,
                        fieldbackground, insertcolor)
            #self["active"]      = self.Conf(**self.config)
            #self["disabled"]    = self.Conf(**self.config)
            #self["focus"]       = self.Conf(**self.config)
            self["readonly"]    = self.Conf(**self.config)

        class Conf(flex_dict):
            def __init__(self, arrowcolor, arrowsize, background, bordercolor, relief, foreground,
                        fieldbackground, insertcolor) -> None:
                super().__init__()
                self.arrowcolor = arrowcolor
                self.arrowsize = arrowsize
                self.background = background
                self.bordercolor = bordercolor
                self.relief = relief
                self.foreground = foreground
                self.fieldbackground = fieldbackground
                self.insertcolor = insertcolor


            


def shack(colo_A,colo_B,taux):

    def convert_to_dec(_hex_str):
        adds = ["a","b","c","d","e","f"]
        result = 0
        cur_val = 0
        for i in range(len(_hex_str)):
            r_i = len(_hex_str) - 1 - i
            if "0" <= _hex_str[i] <= "9":
                cur_val = int(_hex_str[i])
            elif _hex_str[i].lower() in adds:
                for j in range(len(adds)):
                    if _hex_str[i].lower() == adds[j]:
                        cur_val = 10 + j
                        break
            else : 
                return None 
            result += 16**r_i * cur_val
        return result

    def med(_val_A,_val_B,_taux): 
        return int((_val_A * _taux + _val_B * (100 - _taux))/100)

    class Colo():
        def __init__(self, _val_str) -> None:
            self.r = convert_to_dec(_val_str[1:3])
            self.g = convert_to_dec(_val_str[3:5])
            self.b  = convert_to_dec(_val_str[5:])
    ca = Colo(colo_A)
    cb = Colo(colo_B)
    r = str(hex(med(ca.r,cb.r,taux)))[2:]
    g = str(hex(med(ca.g,cb.g,taux)))[2:]
    b = str(hex(med(ca.b,cb.b,taux)))[2:]
    if len(r)== 1 : r = "0" + r
    if len(g)== 1 : g = "0" + g
    if len(b)== 1 : b = "0" + b
    return "#" + r +  g + b

import flet as ft
from os import path
from pickle import dump, load


class DropLess2(ft.PopupMenuButton):
    def __init__(self,
                 value = None, 
                 options = None, 
                 width = None,
                 data = None, 
                 on_change = None,
                 leading_icon = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leading_icon = leading_icon
        self._value = value if value in options else options[0]
        if self.leading_icon:
            self.content = None
            self.icon = self.leading_icon
        else:
            self.content = ft.Text(value, text_align='center', overflow='ellipsis')
        self.items = [
            ft.PopupMenuItem(i, on_click = self.Clicou)
            for i in options
        ] if options else None
        self.on_change = on_change
        self.width = width
        self.data = data
        self.splash_radius = 0
        self.tooltip = ''
        self.style = ft.ButtonStyle(
            alignment=ft.alignment.center,
            animation_duration = 0,
        )
        self.popup_animation_style = ft.Animation(
            duration=0,
            curve=ft.AnimationCurve.LINEAR
        )

    def Clicou(self, e):
        self._value = e.control.text
        e.control.data = self.data
        e.control.value = e.control.text
        if self.leading_icon:
            pass
        else:
            self.content.value = e.control.text
            self.content.update()
        if self.on_change:
            self.on_change(e)


    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self.content.value = value
         

class ThemeLoad(ft.Container):
    def __init__(self, tema, layout,carregartema: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = layout
        self.carregartema = carregartema
        self.adicionados = {}

        self.GetArquivo(tema)
        self.tema_escolhido = DropLess2(
            leading_icon = ft.Icons.PALETTE,       
            width=80,                    
            options = [
                i
                for i in ['Editar']+sorted(list(self.arquiv.keys()))
            ],
            on_change=self.CarregarTema
        )
        self.content = self.tema_escolhido


    def did_mount(self):
        if self.carregartema:
            tema = self.page.client_storage.get(f'{self.page.title}_tema') or "black"
            print(f'{self.page.title}_tema')
            self.Carregar(tema)
      

  
    def GetArquivo(self, caminho = None):        
        self.nome_temas = path.join(path.dirname(path.abspath(__file__)), 'Temas.plk')
        caminho = caminho if caminho else self.nome_temas
        self.arquiv = self.LerPickle(caminho) or  {  "black": {
                "primary":  "#CAD0E8",
                "on_primary":  None,
                "on_secondary_container":  None,
                "outline":  None,
                "shadow":  None,
                "on_surface_variant":  None,
                "surface_variant":  None,
                "primary_container":  None,
                "on_surface":  None,
                "surface":  None,
                "secondary": None,
                "error":None,
                "scrim": None,
                "tertiary": None
                
            }
        }
      

    def set_attrs(self, obj, attr_path, value):
        # Divida o caminho do atributo em uma lista
        attrs = attr_path.split('.')
        
        # Itere até o penúltimo atributo
        for attr in attrs[:-1]:
            obj = getattr(obj, attr)
        
        # Verifique se o último atributo é um índice de lista
        final_attr = attrs[-1]
        if '[' in final_attr and ']' in final_attr:
            # Obtenha o nome do atributo da lista e o índice
            list_attr = final_attr.split('[')[0]
            index = int(final_attr.split('[')[1].split(']')[0])
            
            # Defina o valor no índice específico da lista
            getattr(obj, list_attr)[index] = value
        else:
            # Defina o valor no atributo final
            setattr(obj, final_attr, value)        


    def AddAtriburColor(self, nome, atributo):
        self.adicionados[nome] = atributo


    def CarregarTema(self, e):
        tema = self.tema_escolhido.value
        # print(tema)
        if tema == 'Editar':
            e.page.go('/temas')
        elif tema:
            self.Carregar(tema)
            self.page.client_storage.set(f'{self.page.title}_tema', tema)

    def Carregar(self, tema):
        dic = self.arquiv[tema].copy()
        self.page.theme = ft.Theme(
                color_scheme_seed = dic.get('color_scheme_seed'),
                color_scheme= ft.ColorScheme(
                    primary = dic.get("primary"),
                    on_primary = dic.get("on_primary"),
                    on_secondary_container = dic.get("on_secondary_container"),
                    on_surface_variant = dic.get("on_surface_variant"),
                    surface_variant = dic.get("surface_variant"),
                    primary_container = dic.get("primary_container"),
                    surface = dic.get("surface"),
                    on_surface = dic.get("on_surface"),
                    shadow = dic.get("shadow"),
                    outline = dic.get("outline"),
                    secondary = dic.get("secondary"),
                    error = dic.get("error"),
                    scrim = dic.get("scrim"),
                    tertiary = dic.get("tertiary"),
                    secondary_container = dic.get("secondary_container"),
                    outline_variant = dic.get("outline_variant"),
                    surface_container_low = dic.get("surface_container_low"),
                ),
                text_theme = ft.TextTheme(
                    body_large=ft.TextStyle(color=dic.get("Texto_body_large")),
                    body_medium=ft.TextStyle(color=dic.get("Texto_body_medium")),  #cor padrão
                    body_small=ft.TextStyle(color=dic.get("Texto_boddy_small")) , 
                    display_large=ft.TextStyle(color=dic.get("Texto_display_large")),
                    display_medium=ft.TextStyle(color=dic.get("Texto_display_medium")),
                    display_small=ft.TextStyle(color=dic.get("Texto_display_small")),
                    headline_large=ft.TextStyle(color=dic.get("Texto_headline_large")),
                    headline_medium=ft.TextStyle(color=dic.get("Texto_headline_medium")),
                    headline_small=ft.TextStyle(color=dic.get("Texto_headline_small")),
                    label_large=ft.TextStyle(color=dic.get("Texto_label_large")),
                    label_medium=ft.TextStyle(color=dic.get("Texto_label_medium")),
                    label_small=ft.TextStyle(color=dic.get("Texto_label_small")),
                    title_large=ft.TextStyle(color=dic.get("Texto_title_large")),
                    title_medium=ft.TextStyle(color=dic.get("Texto_title_medium")),
                    title_small=ft.TextStyle(color=dic.get("Texto_title_small"))
                
                ),
                scrollbar_theme=ft.ScrollbarTheme(
                    track_color = dic.get("track_color"),
                    thumb_color = dic.get("thumb_color"),
                ),
            )
        self.page.bgcolor =  'surface'   

        for i in self.adicionados.keys():
            self.set_attrs(self.layout,self.adicionados[i], dic.get(i, 'black'))
        # self.layout.update()
     


        # self.update()
        self.page.update()


    def LerPickle(self, nome):
        if path.isfile(nome):
            with open(nome, 'rb') as arquivo:
                return load(arquivo)
        else:
            return None   
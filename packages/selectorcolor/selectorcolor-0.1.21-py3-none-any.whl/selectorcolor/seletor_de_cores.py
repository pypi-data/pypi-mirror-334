from sys import path as pthsys
# pthsys.append(r'D:\baixados\programas_python\baixar_do_youtube_final')

import flet as ft
from selectorcolor import SelectorColor, Saida

# from pathlib import Path

# Adicione o diretório raiz do projeto ao PATH do Python
# CAMINHO_RAIZ = Path(__file__).parent.parent  # Volta duas pastas (layout -> projeto)

class SaveSelectFile2(ft.ElevatedButton):
    def __init__(self, tipo, nome=None, func = None):
        """
        tipo == path: seleciona uma pasta (retorna o caminho completo da pasta selecionada)
        tipo == file: seleciona um arquivo (retorna o caminho completo do arquivo selecionado)
        tipo == save: salva um arquivo (retorna o caminho completo do arquivo, junto com seu nome)
        """
        super().__init__()
        self.nome = nome if nome else self.default_nome(tipo)
        self.func = func
        self.tipo = tipo
        self.visible = True
        self._value = None
        self.styleyle = ft.ButtonStyle(
            enable_feedback = True
        )
        self.bgcolor='grey800'
        self.color="#B0B3B1"
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.style = ft.ButtonStyle(
            text_style=ft.TextStyle(
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
        )
        
        self.configurar_botao(tipo)

    def default_nome(self, tipo):
        default_nomes = {
            'file': 'Selecione o arquivo',
            'path': 'Selecione a pasta',
            'save': 'Digite o nome do arquivo',
        }
        return default_nomes.get(tipo, 'Selecionar')

    def configurar_botao(self, tipo):
        icones = {
            'file': ft.Icons.FILE_OPEN,
            'path': ft.Icons.UPLOAD_FILE,
            'save': ft.Icons.SAVE,
        }
        acoes = {
            'file': self.selecionar_arquivo,
            'path': self.selecionar_pasta,
            'save': self.save,
        }
        self.text = self.nome
        self.icon = icones[tipo]
        self.on_click = acoes[tipo]

    async def selecionar_arquivo(self, _):
        self.pick_files_dialog.pick_files(
            allow_multiple=True,
            allowed_extensions = ['plk']
            )

    async def selecionar_pasta(self, _):
        self.pick_files_dialog.get_directory_path()

    async def save(self, _):
        self.pick_files_dialog.save_file()

    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        from os import path
        if self.tipo in ['file', 'path', 'save']:
            self._value = e.path if e.path else None
        if self.tipo == 'file' and e.files:
            self._value = ",".join(map(lambda f: f.path, e.files))
        
        if self._value:
            caminho_pasta, nome_arquivo = path.split(self._value)
            self.text = nome_arquivo[:-4] if self._value else self.nome   
        else:
            self.text = self.nome 
        self.func(self._value)
        self.update()

    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()

    def will_unmount(self):
        self.page.overlay.remove(self.pick_files_dialog)
        self.page.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, valor):
        self._value = valor
        self.text = valor

class Sim(SaveSelectFile2):
    def __init__(self, func,*args, **kwargs):
        super().__init__(nome = 'Sim', tipo = 'save',*args, **kwargs)
        self.func = func
        # self.visible = False
        
    async def save(self, _):
        self.pick_files_dialog.save_file(
            allowed_extensions = ['pkl']
        )

    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        if self.tipo in ['file', 'path', 'save']:
            self._value = e.path if e.path else None
        if self.tipo == 'file' and e.files:
            self._value = ",".join(map(lambda f: f.path, e.files))
        
        self.text = self._value if self._value else self.nome
        if self._value:
            self.func(self._value)
            # print(nome_arquivo,self._value)

        self.update()



class DropLess(ft.PopupMenuButton):
    def __init__(self,
                 value = None, 
                 options = None, 
                 width = None,
                 data = None, 
                 on_change = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = value if value in options else options[0]
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
        self._value = e.control.text if e.control.text == self._value else self._value
        e.control.data = self.data
        e.control.value = e.control.text
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
         

class SelectorColor2(SelectorColor):
    def __init__(self, control, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control = control
        self.width = None

        self.adicionados = {}
        self.dic = {}
        # self.text_theme_boddy_small = ft.TextStyle(color=None)
        
        self.datas = {
            # "Container": lambda color: setattr(self.color_box, 'bgcolor', color), 
            # "Fundo": self.ChangeFundoColor,
            # "Texto": lambda color: setattr(self.text_theme, 'color', color),
            # "Texto_body_medium": lambda color: setattr(self.page.theme.text_theme.body_medium, 'color', color),
            "color_scheme_seed": lambda color: setattr(self.page.theme, 'color_scheme_seed', color),
         
            # "secondary_header_color": lambda color: setattr(self.page.theme, 'secondary_header_color', color),
            # "primary_color": lambda color: setattr(self.page.theme, 'primary_color', color),
            # "primary_color_dark": lambda color: setattr(self.page.theme, 'primary_color_dark', color),
            # "primary_color_light": lambda color: setattr(self.page.theme, 'primary_color_light', color),
            
            # "Título": lambda color: setattr(self.titulo, 'color', color),
            # "Texto 1": lambda color: setattr(self.texto1, 'color', color),
            # "Texto 2": lambda color: setattr(self.texto2, 'color', color),
            # "Bordas": self.ChangeBordasColor,
            # "Sombras": self.ChangeSombrasColor,
            # "Gradiente": self.ChangeGradienteColor, 
            # "Botão": self.ChangeBotao,
            # "bgcolor":lambda color: setattr(self.control, 'bgcolor', color),
            # "color":lambda color: setattr(self.control, 'color', color),
            # "dropdown_menu_theme":lambda color: setattr(self.page.theme.dropdown_menu_theme.text_style, 'bgcolor', color),
            "primary":  lambda color: setattr(self.color_scheme, 'primary', color),
            "on_primary":  lambda color: setattr(self.color_scheme, 'on_primary', color),
            "on_secondary_container":  lambda color: setattr(self.color_scheme, 'on_secondary_container', color),
            "on_surface_variant":  lambda color: setattr(self.color_scheme, 'on_surface_variant', color),
            "surface_variant":  lambda color: setattr(self.color_scheme, 'surface_variant', color),
            "primary_container":  lambda color: setattr(self.color_scheme, 'primary_container', color),
            "on_surface":  lambda color: setattr(self.color_scheme, 'on_surface', color),




            "surface":  lambda color: setattr(self.color_scheme, 'surface', color),
            "shadow":  lambda color: setattr(self.color_scheme, 'shadow', color),
            "outline":  lambda color: setattr(self.color_scheme, 'outline', color),
            "secondary": lambda color: setattr(self.color_scheme, 'secondary', color),
            "error": lambda color: setattr(self.color_scheme, 'error', color),
            "scrim": lambda color: setattr(self.color_scheme, 'scrim', color),
            "tertiary": lambda color: setattr(self.color_scheme, 'tertiary', color),


            "secondary_container": lambda color: setattr(self.color_scheme, 'secondary_container', color),
            # "on_secondary_container": lambda color: setattr(self.color_scheme, 'on_secondary_container', color),
            # "on_tertiary": lambda color: setattr(self.color_scheme, 'on_tertiary', color),
            # "tertiary_container": lambda color: setattr(self.color_scheme, 'tertiary_container', color),
            # "on_tertiary_container": lambda color: setattr(self.color_scheme, 'on_tertiary_container', color),
            # "on_error": lambda color: setattr(self.color_scheme, 'on_error', color),
            # "error_container": lambda color: setattr(self.color_scheme, 'error_container', color),
            # "on_error_container": lambda color: setattr(self.color_scheme, 'on_error_container', color),
            # "background": lambda color: setattr(self.color_scheme, 'background', color),
            # "on_background": lambda color: setattr(self.color_scheme, 'on_background', color),
            "outline_variant": lambda color: setattr(self.color_scheme, 'outline_variant', color),
            # "inverse_surface": lambda color: setattr(self.color_scheme, 'inverse_surface', color),
            # "on_inverse_surface": lambda color: setattr(self.color_scheme, 'on_inverse_surface', color),
            # "inverse_primary": lambda color: setattr(self.color_scheme, 'inverse_primary', color),
            # "surface_tint": lambda color: setattr(self.color_scheme, 'surface_tint', color),
            # "on_primary_fixed": lambda color: setattr(self.color_scheme, 'on_primary_fixed', color),
            # "on_secondary_fixed": lambda color: setattr(self.color_scheme, 'on_secondary_fixed', color),
            # "on_tertiary_fixed": lambda color: setattr(self.color_scheme, 'on_tertiary_fixed', color),
            # "on_primary_fixed_variant": lambda color: setattr(self.color_scheme, 'on_primary_fixed_variant', color),
            # "on_secondary_fixed_variant": lambda color: setattr(self.color_scheme, 'on_secondary_fixed_variant', color),
            # "on_tertiary_fixed_variant": lambda color: setattr(self.color_scheme, 'on_tertiary_fixed_variant', color),
            # "primary_fixed": lambda color: setattr(self.color_scheme, 'primary_fixed', color),
            # "secondary_fixed": lambda color: setattr(self.color_scheme, 'secondary_fixed', color),
            # "tertiary_fixed": lambda color: setattr(self.color_scheme, 'tertiary_fixed', color),
            # "primary_fixed_dim": lambda color: setattr(self.color_scheme, 'primary_fixed_dim', color),
            # "secondary_fixed_dim": lambda color: setattr(self.color_scheme, 'secondary_fixed_dim', color),
            # "surface_bright": lambda color: setattr(self.color_scheme, 'surface_bright', color),
            # "surface_container": lambda color: setattr(self.color_scheme, 'surface_container', color),
            # "surface_container_high": lambda color: setattr(self.color_scheme, 'surface_container_high', color),
            "surface_container_low": lambda color: setattr(self.color_scheme, 'surface_container_low', color),
            # "surface_container_lowest": lambda color: setattr(self.color_scheme, 'surface_container_lowest', color),
            # "surface_dim": lambda color: setattr(self.color_scheme, 'surface_dim', color),
            # "tertiary_fixed_dim": lambda color: setattr(self.color_scheme, 'tertiary_fixed_dim', color),
            
            # "Texto_boddy_small": lambda color: setattr(self.page.theme.text_theme.boddy_small, 'color', color),
            "Texto_body_large": lambda color: setattr(self.page.theme.text_theme.body_large, 'color', color),
            "Texto_body_medium": lambda color: setattr(self.page.theme.text_theme.body_medium, 'color', color),
            "Texto_body_small": lambda color: setattr(self.page.theme.text_theme.body_small, 'color', color),
            "Texto_display_large": lambda color: setattr(self.page.theme.text_theme.display_large, 'color', color),
            "Texto_display_medium": lambda color: setattr(self.page.theme.text_theme.display_medium, 'color', color),
            "Texto_display_small": lambda color: setattr(self.page.theme.text_theme.display_small, 'color', color),
            "Texto_headline_large": lambda color: setattr(self.page.theme.text_theme.headline_large, 'color', color),
            "Texto_headline_medium": lambda color: setattr(self.page.theme.text_theme.headline_medium, 'color', color),
            "Texto_headline_small": lambda color: setattr(self.page.theme.text_theme.headline_small, 'color', color),
            "Texto_label_large": lambda color: setattr(self.page.theme.text_theme.label_large, 'color', color),
            "Texto_label_medium": lambda color: setattr(self.page.theme.text_theme.label_medium, 'color', color),
            "Texto_label_small": lambda color: setattr(self.page.theme.text_theme.label_small, 'color', color),
            "Texto_title_large": lambda color: setattr(self.page.theme.text_theme.title_large, 'color', color),
            "Texto_title_medium": lambda color: setattr(self.page.theme.text_theme.title_medium, 'color', color),
            "Texto_title_small": lambda color: setattr(self.page.theme.text_theme.title_small, 'color', color),
        
            "hover_color": lambda color: setattr(self.page.theme,'hover_color', color),
            "hint_color": lambda color: setattr(self.page.theme,'hint_color', color),
            "divider_color": lambda color: setattr(self.page.theme,'divider_color', color),
            "dialog_bgcolor": lambda color: setattr(self.page.theme,'dialog_bgcolor', color),
            "indicator_color": lambda color: setattr(self.page.theme,'indicator_color', color),
            "splash_color": lambda color: setattr(self.page.theme,'splash_color', color),
            "unselected_control_color": lambda color: setattr(self.page.theme,'unselected_control_color', color),
            "focus_color": lambda color: setattr(self.page.theme,'focus_color', color),
            "disabled_color": lambda color: setattr(self.page.theme,'disabled_color', color),
            # "primary_swatch": lambda color: setattr(self.page.theme,'primary_swatch', color),
            

            "track_color": lambda color: setattr(self.page.theme.scrollbar_theme, 'track_color', color),
            "thumb_color": lambda color: setattr(self.page.theme.scrollbar_theme, 'thumb_color', color),


        }
        self.chaves = list(self.datas.keys())

        # self.objetos.options=[ft.dropdown.Option(i) for i in self.chaves]
        self.objetos = DropLess(
            width=200,
            value = 'Selecione o objeto',
            options=[i for i in self.chaves],
            on_change=self.SetObjeto,
            col = 8.5,            
        )
        self.objetos.height = 25
        self.objetos.style = ft.ButtonStyle(bgcolor='grey900')
              
        self.controles.col =  12
        self.color_box2.col =  12
        self.color_box2.expand =  True
        self.color_box2.height =  None
        # self.color_box2.bgcolor =  'surface'
        # self.color_box2.gradient = None
        self.color_box2.content = self.control
        self.controles.content.controls[0].controls[0].visible = False
        self.controles.content.controls[0].controls[1].visible = False

        self.temas = SaveSelectFile2('file', 'Selecione um arquivo de temas', self.EscolheuTema)
        self.nome_tema_criar = Sim(self.salve)
        self.novo_tema = ft.Container(
            content = ft.Column(
                [
                    ft.Text(f'Deseja criar um novo arquivo de temas?', expand=True, text_align='center', color='#B0B3B1'),
                    ft.ResponsiveRow(
                        [
                            self.ContainerHover(
                                self.nome_tema_criar
                            ),
                            
                            self.ContainerHover(
                                ft.FilledButton(
                                    'Não',
                                    bgcolor='grey800',
                                    color="#B0B3B1",                                
                                    on_click=self.SalvarTema
                                    )
                            )
                        ],
                        columns=24,
                        alignment='center',
                    )
                ]
            ),
            visible=False
        )
        
        self.next = ft.Container(
            content = ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color="#B0B3B1",),
            bgcolor='grey800',        
            col = 1,
            alignment=ft.alignment.center,
            height=25,
            width=25,            
            on_click=self.Next,          
        )
        self.back = ft.Container(
            content = ft.Icon(ft.Icons.ARROW_BACK_IOS,color="#B0B3B1",),
            bgcolor='grey800',        
            col = 1,
            width=25,
            alignment=ft.alignment.center,
            height=25,
            on_click=self.Back,
        )


        self.set_all = ft.ElevatedButton(
            text="Set all blue",
            bgcolor='grey800',
            color="#B0B3B1",
            on_click=self.SetAll,
            height=30,
            col = 24,
            expand=True,
        )
        
        # self.controles.content.controls.append(self.set_all)
        # self.controles.content.controls[1].columns = 14
        # self.objetos.col = 8.5
        # self.objetos.border_radius = 0
        # self.controles.content.controls[1].spacing = 0
        # self.controles.content.controls[1].controls[1].col = 1.5
        # self.controles.content.controls[1].controls = [self.back, self.ContainerHover(self.objetos), self.next, self.controles.content.controls[1].controls[1]]
        self.R = ft.Text("R", selectable=True, color="#BEBCE7", col = 1, left = 0,top = 2,)
        self.G = ft.Text("G", selectable=True, color="#BEBCE7", col = 1, left = 0,top = 27)
        self.B = ft.Text("B", selectable=True, color="#BEBCE7", col = 1, left = 0,top = 52)   
        self.link = ft.Checkbox(label="Link slides", value=False,label_style = ft.TextStyle(color = "#BEBCE7"))

        self.prev_r = 0
        self.prev_g = 0
        self.prev_b = 0        
        self.controles = ft.Container(
            content = ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            self.ativar_sombras, 
                            self.ativar_bordas, 
                            self.ativar_gradiente,
                            self.exibir_legendas,
                        ], 
                        alignment='center', 
                        spacing=1,
                        run_spacing=1,                       
                        columns=24,
                    ),
                    
                    ft.Row(
                        [
                            ft.Container(
                                bgcolor='grey700',
                                border_radius=12,
                                content = ft.Row(
                                    [
                                        self.back,                
                                        self.objetos,
                                        self.next,                                
                                    ],
                                    spacing = 0,
                                    tight=True,
                                    col = 1,
                                ),
                            ),
                            ft.VerticalDivider(width=10),
                            self.icone_copy,
                        ],
                        spacing = 0,
                        tight=True,
                        col = 1,
                    ),                    
                                                        
                    ft.Stack(
                        controls = [
                            self.R,ft.Container(self.slides[f'r'],left = 25,top = 0),
                            self.G,ft.Container(self.slides[f'g'],left = 25,top = 25),
                            self.B,ft.Container(self.slides[f'b'],left = 25,top = 50),                            
                        ], 
                        alignment=ft.alignment.center,
                        expand=True,                
                        height=80,
                    ),
                    ft.Row([self.link, self.set_all]),

                ],
                width=380,
                spacing=0,
                run_spacing=0,
                horizontal_alignment='center',
                tight=True,

            ),
            border=ft.border.all(1, 'grey800'),
            border_radius=15,
            padding=20,
            expand_loose=True,
            # col =  {'xs':12, 'sm':7},
            
        )        
        
        
        
        
        
        self.content = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        self.caixa(
                            ft.Column(
                                [
                                    self.controles,

                                    self.ContainerHover(self.temas),
                                    ft.ResponsiveRow(
                                        [
                                            self.ContainerHover(self.btn_exportar_cores),
                                            self.ContainerHover(self.tema_escolhido),
                                        ], 
                                        alignment='center', 
                                        vertical_alignment='center'                                                      
                                    ),
                                    ft.ResponsiveRow(
                                        [
                                            self.ContainerHover(self.btn_save),
                                            self.nome_tema
                                        ]
                                        , alignment='center',                           
                                    ),
                                    self.novo_tema,                                    
                                    self.tabela_legenda, 
                                    
                                ],
                                
                                # scroll=ft.ScrollMode.ADAPTIVE,
                                expand=True,
                            ),
                            # col =  {'xs':12, 'sm':4, 'md':3, 'lg':2  },
                            width=400,
                            # height=1200,
                            # expand=True,

                        ),
                        self.caixa(
                            ft.Container(self.control, bgcolor='surface'), 
                            # ft.Text('teste'),
                            # col =  {'xs':12, 'sm':8, 'md':9,'lg':10  },
                            # width=600,
                            # height = 300,
                            # expand = True
                        ),
                        

                                        
                    ],
                    alignment='center', 
                    vertical_alignment='start',
                    # columns=12
                    expand = True,
                    wrap=True,
                    # width=1200,
                    # height=300,
                
                ),                                                                                                                            
            ], 
            # alignment='center',
            horizontal_alignment='center',
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,  
            
        )



    def did_mount(self):
        self.ativar_sombras.value = False
        self.ativar_gradiente.value = False
        self.ativar_bordas.value = False

        self.page.theme = ft.Theme(
            color_scheme = self.color_scheme,
            text_theme = ft.TextTheme(
                body_large = ft.TextStyle(),
                body_medium = ft.TextStyle(),
                body_small = ft.TextStyle(),
                display_large = ft.TextStyle(),
                display_medium = ft.TextStyle(),
                display_small = ft.TextStyle(),
                headline_large = ft.TextStyle(),
                headline_medium = ft.TextStyle(),
                headline_small = ft.TextStyle(),
                label_large = ft.TextStyle(),
                label_medium = ft.TextStyle(),
                label_small = ft.TextStyle(),
                title_large = ft.TextStyle(),
                title_medium = ft.TextStyle(),
                title_small = ft.TextStyle(),

            ),
            scrollbar_theme=ft.ScrollbarTheme(
                track_color = 'grey500',
                thumb_color = 'grey900',
            ),

        )

        saida = Saida(self.page)
        self.pprint = saida.pprint 
        self.page.horizontal_alignment = 'center'


     
        self.page.on_resized = self.Redimensionar
        self.Redimensionar(1)  
        self.page.update()


    def Redimensionar(self, e):
        if isinstance(e, int):
            if self.page.web:
                teste = self.page.width
            else:
                teste = self.page.window.width
            self.Iniciar(teste)
            self.update()
            self.page.update()
        else:
            if e.page.web:
                teste = e.page.width
            else:
                teste = e.page.window.width   
            self.Iniciar(teste)
            e.page.update()


    def Iniciar(self,teste):
        if teste > 700:
            self.content.controls[0].wrap = False
            self.content.controls[0].alignment='start'
            self.content.controls[0].controls[1].width = teste-self.content.controls[0].controls[0].width-80

            # pass
        else:
            self.content.controls[0].wrap = True
            self.content.controls[0].alignment='center'
            self.content.controls[0].controls[1].width = None

            # pass
        self.content.controls[0].update()

    def Next(self,e):
        atual = self.objetos.value if self.objetos.value else self.chaves[0]
        index = self.chaves.index(atual)
        next = self.chaves[index+1] if index < len(self.chaves)-1 else self.chaves[0]
        self.objetos.value = next
        self.slides['r'].data = next
        self.slides['g'].data = next
        self.slides['b'].data = next            
        self.objetos.update()   
        if  next != "#000000":
            self.SetColorFromHex(self.dic.get(next, "#000000"))
        self.SetColor(next) 

    def Back(self,e):
        atual = self.objetos.value if self.objetos.value else self.chaves[-1]
        index = self.chaves.index(atual)
        back = self.chaves[index-1] if index > 0 else self.chaves[-1]
        self.objetos.value = back
        self.objetos.update()
        self.slides['r'].data = back
        self.slides['g'].data = back
        self.slides['b'].data = back  
        if  back != "#000000": 
            self.SetColorFromHex(self.dic.get(back, "#000000"))
        self.SetColor(back)         

    def SetAll(self,e):
        if self.set_all.text == "Set all blue":
            for i in self.datas.keys():
                self.datas[i]('blue')
            self.set_all.text = "Reset" 
        elif self.set_all.text == "Reset":
            for i in self.datas.keys():
                self.datas[i]('white')
            self.set_all.text = "Set all blue"
        self.set_all.update()
        self.page.update()

    def salve(self, caminho = None):
        nome_tema = self.nome_tema.value
        caminho = caminho if caminho else self.nome_temas
        if nome_tema not in ['', ' ', None]:#+list(self.arquiv.keys()):
            # print(f'caminho = {caminho}')
            # print(f'nome_tema = {nome_tema}')
            self.GetArquivo(caminho)
            self.arquiv[nome_tema] = self.dic
            self.SalvarPickle(self.arquiv, caminho)                                    
            self.tema_escolhido.options.append(ft.dropdown.Option(nome_tema))      
            self.pprint('tema salvo com sucesso!')
        else:
            self.nome_tema.hint_text = 'Digite um nome de Tema válido ou clique em Cancelar'
            # self.nome_tema.hint_style = ft.TextStyle(size = 10)
        self.nome_tema.visible = False
        self.btn_save.visible = True
        self.novo_tema.visible = False
        self.btn_save.update()
        self.novo_tema.update()
        self.tema_escolhido.update()

    def SalvarTema(self, e):
        self.salve()

    def EscolheuTema(self, caminhotema):
        self.GetArquivo(caminhotema)
        self.tema_escolhido.options=[
            ft.dropdown.Option(i) for i in sorted(list(self.arquiv.keys()))
        ]
        self.tema_escolhido.update()
        self.update()
        # print(caminhotema)


    def CriarTema(self, e):
        self.novo_tema.visible = False
        self.nome_tema_criar.visible = True
        self.nome_tema_criar.update()
        self.nome_tema.update()
        self.salve(self.nome_tema_criar.value)

    def Salvar(self, e):
        # print(self.temas.value)
        if self.temas.value:
            self.salve(self.temas.value)

        else:
            self.nome_tema.visible = False
            self.novo_tema.visible = True
            self.novo_tema.update()
            self.nome_tema.update()



        self.update()


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
        def Atibuir(color):
            # setattr(getattr(self.control,atributo), propriedade, color)
            self.set_attrs(self.control, atributo,color)
            # getattr(self.control,atributo).update()
            self.control.update()

        self.datas[nome] = Atibuir
        self.objetos.options=[ft.dropdown.Option(i) for i in self.datas.keys()]
        self.adicionados[nome] = atributo


    def ChangeBotao(self, color):
        self.botao.bgcolor = color
        self.page.theme.elevated_button_theme.bgcolor = color
        self.update()
        self.page.update()
        # print('botão')
        # self.SetValueCLienStorage(f'{self.page.title}_Botao', color)
        # self.dic['Botao'] = self.cor

    def caixa(self, control, col = 12, width = None, height = None, expand = False):
        return ft.Container(
            padding=15,
            border=ft.border.all(1, 'grey800'),
            border_radius=15,
            col = col,
            content=control,
            expand=expand,
            width=width,
            height=height,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=60,
                color='#524A76,0.2',
                blur_style = ft.ShadowBlurStyle.OUTER
            )
        )
    
    def update_color(self, e):
        if e.control.data: 
            self.SetColor(e.control.data) 

    # def SetColor(self, nome):
    #     self.cor = f'#{int(self.slides['r'].value):02X}{int(self.slides['g'].value):02X}{int(self.slides['b'].value):02X}'
    #     self.R.value = f'R ({int(self.slides['r'].value):02})'
    #     self.G.value = f'G ({int(self.slides['g'].value):02})'
    #     self.B.value = f'B ({int(self.slides['b'].value):02})'
    #     self.datas[nome](self.cor)
    #     self.dic[nome] = self.cor          
    #     self.update()
    #     self.page.update()
    def SetColor(self, nome):
        # Obtém os valores atuais dos slides
        r_value = int(self.slides['r'].value)
        g_value = int(self.slides['g'].value)
        b_value = int(self.slides['b'].value)
        
        # Atualiza a cor
        self.cor = f'#{r_value:02X}{g_value:02X}{b_value:02X}'
        self.R.value = f'R ({r_value:02})'
        self.G.value = f'G ({g_value:02})'
        self.B.value = f'B ({b_value:02})'
        self.datas[nome](self.cor)
        self.dic[nome] = self.cor
        self.update()
        self.page.update()

        # Sincroniza os valores dos slides se 'self.link.value' for True
        if self.link.value:
            # Calcula a diferença dos valores dos slides
            r_diff = r_value - self.prev_r
            g_diff = g_value - self.prev_g
            b_diff = b_value - self.prev_b

            # Define uma função para garantir que os valores permaneçam dentro do intervalo 0-255
            def clamp(value, min_value=0, max_value=255):
                return max(min(value, max_value), min_value)

            # Aplica a diferença aos outros slides e garante que os valores permaneçam dentro do intervalo
            if abs(r_diff) > 0:
                self.slides['g'].value = clamp(self.slides['g'].value + r_diff)
                self.slides['b'].value = clamp(self.slides['b'].value + r_diff)
            elif abs(g_diff) > 0:
                self.slides['r'].value = clamp(self.slides['r'].value + g_diff)
                self.slides['b'].value = clamp(self.slides['b'].value + g_diff)
            elif abs(b_diff) > 0:
                self.slides['r'].value = clamp(self.slides['r'].value + b_diff)
                self.slides['g'].value = clamp(self.slides['g'].value + b_diff)

            # Verifica se algum valor está fora do intervalo e ajusta os outros
            if r_value == 255 or g_value == 255 or b_value == 255:
                self.slides['r'].value = min(self.slides['r'].value, self.prev_r)
                self.slides['g'].value = min(self.slides['g'].value, self.prev_g)
                self.slides['b'].value = min(self.slides['b'].value, self.prev_b)

            if r_value == 0 or g_value == 0 or b_value == 0:
                self.slides['r'].value = max(self.slides['r'].value, self.prev_r)
                self.slides['g'].value = max(self.slides['g'].value, self.prev_g)
                self.slides['b'].value = max(self.slides['b'].value, self.prev_b)

            # Atualiza os valores das cores após aplicar as diferenças
            r_value = int(self.slides['r'].value)
            g_value = int(self.slides['g'].value)
            b_value = int(self.slides['b'].value)
            
            self.R.value = f'R ({r_value:02})'
            self.G.value = f'G ({g_value:02})'
            self.B.value = f'B ({b_value:02})'
            self.cor = f'#{r_value:02X}{g_value:02X}{b_value:02X}'
            self.datas[nome](self.cor)
            self.update()
            self.page.update()
        
        # Atualiza os valores anteriores dos slides
        self.prev_r = r_value
        self.prev_g = g_value
        self.prev_b = b_value



    def ExportarCores(self, e):

        cores =f'''

        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary = "{self.color_scheme.primary}",
                on_primary = "{self.color_scheme.on_primary}",
                on_secondary_container = "{self.color_scheme.on_secondary_container}",
                outline = "{self.color_scheme.outline}",
                shadow = "{self.color_scheme.shadow}",
                on_surface_variant = "{self.color_scheme.on_surface_variant}",
                surface_variant = "{self.color_scheme.surface_variant}",
                primary_container = "{self.color_scheme.primary_container}",
                on_surface = "{self.color_scheme.on_surface}",
                surface = "{self.color_scheme.surface}",
                secondary =" {self.color_scheme.secondary}",
                error = "{self.color_scheme.error}",
                scrim = "{self.color_scheme.scrim}",
                tertiary = "{self.color_scheme.tertiary}"

            ),
            text_theme = ft.TextTheme(
                body_medium=ft.TextStyle(color="{self.text_theme.color}"),  # Cor do texto padrão
                body_small=ft.TextStyle(color="{self.text_theme_boddy_small.color}"),  # Cor do texto padrão
            )   
        ) 
        page.bgcolor =  'surface'   
    '''
        
        for i in self.adicionados.keys():
            self.set_attrs(self.control,self.adicionados[i], self.dic.get(i, self.cor))
            # print(f'{i} = {self.dic.get(i)}')
            cores += f'        self.{self.adicionados[i]} = "{self.dic.get(i)}"\n'

        self.page.set_clipboard(cores)

  
    def CarregarTema(self, e):
        tema = self.tema_escolhido.value
        if tema:

            self.dic = self.arquiv[tema].copy()
            # self.titulo.color = self.dic.get('Título')
            # self.texto1.color = self.dic.get('Texto 1')
            # self.texto2.color = self.dic.get('Texto 2')         
            # self.color_text.color = self.dic.get('Texto')
            # self.color_box.bgcolor = self.dic.get('Container')
            # self.color_box2.bgcolor = self.dic.get('Fundo')
            # self.botao.bgcolor = self.dic.get('Botão')

            # if isinstance(self.dic.get('Gradiente'), list):
            #     self.dic['Gradiente'] = self.dic.get('Gradiente')[1]
            # if not self.dic.get('Fundo'):
            #     self.color_box2.bgcolor = 'black'
            # if not self.dic.get('Gradiente'):                
            #     self.gradiente.colors = [self.dic.get('Fundo'),'black']
            # else:
            #     self.gradiente.colors = [self.dic.get('Fundo'), self.dic.get('Gradiente')]

            # self.sombras.color = self.dic.get('Sombras')
            # self.bordas = ft.border.all(1, self.dic.get('Bordas'))
            # self.botao.bgcolor = self.dic.get('Botão')
        

            # self.ativar_bordas.value = self.dic.get("Ativar Bordas")
            # if self.dic.get("Ativar Bordas"):
            #     self.color_box.border = self.bordas
            # else:
            #     self.color_box.border = None

            # self.ativar_sombras.value = self.dic.get("Ativar Sombras")
            # if self.dic.get("Ativar Sombras"):
            #     self.color_box.shadow = self.sombras
            # else:
            #     self.color_box.shadow = None

            # self.ativar_gradiente.value = self.dic.get("Ativar Gradiente")
            # if self.color_box2.bgcolor == None:
            #     self.color_box2.bgcolor = 'black'
            # if self.dic.get("Ativar Gradiente"):
            #     self.gradiente.colors[0] = self.color_box2.bgcolor
            #     setattr(self.color_box2, 'gradient', self.gradiente)
            # else:
            #     setattr(self.color_box2, 'gradient', None)

            self.page.theme = ft.Theme(
                color_scheme_seed = self.dic.get('color_scheme_seed'),
                color_scheme= self.color_scheme,
                # ft.ColorScheme(
                #     primary = self.dic.get("primary"),
                #     on_primary = self.dic.get("on_primary"),
                #     on_secondary_container = self.dic.get("on_secondary_container"),
                #     on_surface_variant = self.dic.get("on_surface_variant"),
                #     surface_variant = self.dic.get("surface_variant"),
                #     primary_container = self.dic.get("primary_container"),
                #     surface = self.dic.get("surface"),
                #     on_surface = self.dic.get("on_surface"),
                #     shadow = self.dic.get("shadow"),
                #     outline = self.dic.get("outline"),
                #     secondary = self.dic.get("secondary"),
                #     error = self.dic.get("error"),
                #     scrim = self.dic.get("scrim"),
                #     tertiary = self.dic.get("tertiary"),
                #     secondary_container = self.dic.get("secondary_container"),
                #     outline_variant = self.dic.get("outline_variant"),
                #     surface_container_low = self.dic.get("surface_container_low"),
                # ),
                text_theme = ft.TextTheme(
                    body_large=ft.TextStyle(color=self.dic.get("Texto_body_large")),
                    body_medium=ft.TextStyle(color=self.dic.get("Texto_body_medium")),  #cor padrão
                    body_small=ft.TextStyle(color=self.dic.get("Texto_boddy_small")) , 
                    display_large=ft.TextStyle(color=self.dic.get("Texto_display_large")),
                    display_medium=ft.TextStyle(color=self.dic.get("Texto_display_medium")),
                    display_small=ft.TextStyle(color=self.dic.get("Texto_display_small")),
                    headline_large=ft.TextStyle(color=self.dic.get("Texto_headline_large")),
                    headline_medium=ft.TextStyle(color=self.dic.get("Texto_headline_medium")),
                    headline_small=ft.TextStyle(color=self.dic.get("Texto_headline_small")),
                    label_large=ft.TextStyle(color=self.dic.get("Texto_label_large")),
                    label_medium=ft.TextStyle(color=self.dic.get("Texto_label_medium")),
                    label_small=ft.TextStyle(color=self.dic.get("Texto_label_small")),
                    title_large=ft.TextStyle(color=self.dic.get("Texto_title_large")),
                    title_medium=ft.TextStyle(color=self.dic.get("Texto_title_medium")),
                    title_small=ft.TextStyle(color=self.dic.get("Texto_title_small"))
                ),
                scrollbar_theme=ft.ScrollbarTheme(
                    track_color = self.dic.get("track_color"),
                    thumb_color = self.dic.get("thumb_color"),                    
                ),

            )
            # self.page.bgcolor =  'surface'


            self.color_scheme.primary = self.dic.get("primary")
            self.color_scheme.on_primary = self.dic.get("on_primary")
            self.color_scheme.on_secondary_container = self.dic.get("on_secondary_container")
            self.color_scheme.outline = self.dic.get("outline")
            self.color_scheme.shadow = self.dic.get("shadow")
            self.color_scheme.on_surface_variant = self.dic.get("on_surface_variant")
            self.color_scheme.surface_variant = self.dic.get("surface_variant")
            self.color_scheme.primary_container = self.dic.get("primary_container")
            self.color_scheme.on_surface = self.dic.get("on_surface")
            self.color_scheme.secondary = self.dic.get("secondary")
            self.color_scheme.error = self.dic.get("error")
            self.color_scheme.scrim = self.dic.get("scrim")
            self.color_scheme.tertiary = self.dic.get("tertiary")
            self.color_scheme.surface = self.dic.get("surface")
            self.color_scheme.secondary_container = self.dic.get("secondary_container")
            self.color_scheme.outline_variant = self.dic.get("outline_variant")
            self.color_scheme.surface_container_low = self.dic.get("surface_container_low")



            # self.color_scheme.on_tertiary = self.dic.get("on_tertiary")
            # self.color_scheme.tertiary_container = self.dic.get("tertiary_container")
            # self.color_scheme.on_tertiary_container = self.dic.get("on_tertiary_container")
            # self.color_scheme.on_error = self.dic.get("on_error")
            # self.color_scheme.error_container = self.dic.get("error_container")
            # self.color_scheme.on_error_container = self.dic.get("on_error_container")
            # self.color_scheme.background = self.dic.get("background")
            # self.color_scheme.on_background = self.dic.get("on_background")
            # self.color_scheme.outline_variant = self.dic.get("outline_variant")
            # self.color_scheme.inverse_surface = self.dic.get("inverse_surface")
            # self.color_scheme.on_inverse_surface = self.dic.get("on_inverse_surface")
            # self.color_scheme.inverse_primary = self.dic.get("inverse_primary")
            # self.color_scheme.surface_tint = self.dic.get("surface_tint")
            # self.color_scheme.on_primary_fixed = self.dic.get("on_primary_fixed")
            # self.color_scheme.on_secondary_fixed = self.dic.get("on_secondary_fixed")
            # self.color_scheme.on_tertiary_fixed = self.dic.get("on_tertiary_fixed")
            # self.color_scheme.on_primary_fixed_variant = self.dic.get("on_primary_fixed_variant")
            # self.color_scheme.on_secondary_fixed_variant = self.dic.get("on_secondary_fixed_variant")
            # self.color_scheme.on_tertiary_fixed_variant = self.dic.get("on_tertiary_fixed_variant")
            # self.color_scheme.primary_fixed = self.dic.get("primary_fixed")
            # self.color_scheme.secondary_fixed = self.dic.get("secondary_fixed")
            # self.color_scheme.tertiary_fixed = self.dic.get("tertiary_fixed")
            # self.color_scheme.primary_fixed_dim = self.dic.get("primary_fixed_dim")
            # self.color_scheme.secondary_fixed_dim = self.dic.get("secondary_fixed_dim")
            # self.color_scheme.surface_bright = self.dic.get("surface_bright")
            # self.color_scheme.surface_container = self.dic.get("surface_container")
            # self.color_scheme.surface_container_high = self.dic.get("surface_container_high")
            # self.color_scheme.surface_container_low = self.dic.get("surface_container_low")
            # self.color_scheme.surface_container_lowest = self.dic.get("surface_container_lowest")
            # self.color_scheme.surface_dim = self.dic.get("surface_dim")
            # self.color_scheme.tertiary_fixed_dim = self.dic.get("tertiary_fixed_dim")




            # self.text_theme.color = self.dic.get("Texto")
            # self.text_theme_boddy_small.color = self.dic.get("Texto_boddy_small")




            #carrega as cores de objetos adicionados
            for i in self.adicionados.keys():
                self.set_attrs(self.control,self.adicionados[i], self.dic.get(i, self.cor))
                # print(f'{i} = {self.dic.get(i)}')








            self.update()
            self.page.update()


def Iniciar(control):
    def main(page: ft.Page):
        page.title = 'Selector de Cores2'
        page.window.width = 1000
        page.add(SelectorColor2(control))
    ft.app(target=main)



if __name__ == '__main__':
    Iniciar(ft.TextField(label='teste', value = 'askjdhaklsjhkj', filled=True, border_width=2, dense = True))
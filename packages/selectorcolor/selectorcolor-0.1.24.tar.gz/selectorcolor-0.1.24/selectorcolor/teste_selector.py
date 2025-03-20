#pip install selectorcolor -- upgrade
#exemplos de uso

#exemplo 1
# from selectorcolor import Iniciar
# Iniciar()

#exemplo 2
from selectorcolor.seletor_de_cores import  ft, SelectorColor2
# Iniciar(control = Classe_principal_de_seu_Programa ou componente flet)


'''
"Texto_body_medium": label do checkbox, cor do text
"Texto_boddy_small":
"primary":  checkbox True, slider, swith true, icones, texto do elevatebutton
"on_primary": bolinha do swith, check do checkbox,   
"on_secondary_container":  
"outline":  
"shadow":  sombras, 
"on_surface_variant":  hint do texfied, bolinha False do switch, borda do checkbox, 
"surface_variant": swith False, slider false
"primary_container":  hoved da bolinha do switch
"on_surface":  
"surface": 
"secondary": 
"error": 
"scrim": 
"tertiary":
'secondary_container": prograss_bar False
"outline_variant":divider,
"surface_container_low":  card

checkbox/dropdown/TextField: scrim, error, tertiary, outline,
    shadow,surface, secondary, 
======================
App tj:
    botoes: scrim
    texto: primary
    fundo: surface
    bordas: outline
    linha par tabela: secondary,
    labels/icones: tertiary

'''
def main(page: ft.Page):
    page.title = 'Selector de Cores3'    
    control = ft.Text('sdlkjlkj')
    page.add(SelectorColor2(control))
   
ft.app(target=main)


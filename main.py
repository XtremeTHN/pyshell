import sys, os, configparser
from os import system as execute
from glob import glob


def find(dirs, word):
    for x in dirs:
        if x.find(word) == -1:
            continue
        else:
            return x
    return 1
file = find(glob(os.getcwd() + "/.*.*"), ".pyshell.conf")
if file == 1:
    def printc(color_handler, color, begin_text,endx="\n"):
        print(begin_text, end=endx)
    color_handler = "default"
    color = "default"
    begin_text = "default"
else:
    def printc(color_handler, color, begin_text,endx="\n"):
        if color_handler == "colorama":
            if color == "default":
                print(begin_text, end=endx)
            else:
                print(f"{color}{begin_text}{Style.RESET_ALL}", end=endx) 
        elif color_handler == "default":
            print(begin_text,end=endx)
        else:
            print("Color Handler no disponible")
            print(begin_text,end=endx)
    configs = configparser.ConfigParser()
    configs.read(".pyshell.conf")
    secciones = ["CUSTOMIZATION"]
    for z,x in enumerate(secciones):
        if secciones[z] == "CUSTOMIZATION":
            for x in configs[x]:
                if x == 'color_handler':
                    color_handler = configs['CUSTOMIZATION'][x]
                elif x == 'color':
                    color = configs['CUSTOMIZATION'][x]
                elif x == 'begin_text':
                    begin_text = configs['CUSTOMIZATION'][x]
    del configs,secciones
    from colorama import Fore, Style
    colors_c = {'red':Fore.RED, 'blue':Fore.BLUE, 'yellow':Fore.YELLOW}
    del Fore
class shell:
    def input(opt):
        if opt == "zsh":
            txt = "    {}  "
            printc(color_handler,color,txt.format(os.getcwd()), endx="")
        elif opt == "default":
            printc(color_handler,color,"{} > ".format(os.getcwd()),endx="")
        else:
            printc(color_handler,color, begin_text, endx="")
        command = input()
        return command

    def getargs(string):
        return string.split()

    def ls(args):
        try:
            if args[1] == "-r":
                return glob(os.getcwd() + "/**/*")
            if args[1] == "-d":
                execute("ls --color=auto")
                return 0
        except IndexError:
            return glob(os.getcwd() + "/*")
    
    def cd(args):
        pass
            

    class config:
        def lsconfs(conf_obj):
            confs = conf_obj.sections()
            print("Secciones y valores:")
            for v in confs:
                print(f"Seccion: {v}")
                for z in conf_obj[v]:
                    print(f"    {z} = {conf_obj[v][z]}")
        def getconf(conf_obj, section, conf):
            try:
                return conf_obj.get(section, conf)
            except (configparser.NoOptionError, configparser.NoSectionError) as e:
                print(e)
                return -1
        def editconf(conf_obj, section, conf, value):
            try:
                if conf == "color":
                    if value in colors_c:
                        for x in colors_c:
                            if x == value:
                                value = colors_c[x]  
                                break
                if conf == "color_handler":
                    print("[WARNING] Si cambias la funcion encargada de los colores debes salir y volver a entrar")
                conf_obj.set(section, conf, str(value))
                with open('.pyshell.conf','w') as configfile:
                    conf_obj.write(configfile)
                return 0
            except (configparser.NoSectionError):
                return -1
            except NameError:
                print("No puedes cambiar el color hasta que hayas reiniciado el programa")
        def reload():
            configs = configparser.ConfigParser()
            configs.read(".pyshell.conf")
            secciones = ["CUSTOMIZATION"]
            global color_handler, color, begin_text
            for z,x in enumerate(secciones):
                if secciones[z] == "CUSTOMIZATION":
                    for x in configs[x]:
                        if x == 'color_handler':
                            color_handler = configs['CUSTOMIZATION'][x]
                        elif x == 'color':
                            color = configs['CUSTOMIZATION'][x]
                        elif x == 'begin_text':
                            begin_text = configs['CUSTOMIZATION'][x]
# Main func
if __name__ == "__main__":
    #execute("clear")
    # Main loop
    while True:
        user = shell.input(begin_text)
        args = shell.getargs(user)
        if not args:
            continue
        if args[0] == "exit":
            break
        if args[0] == "ls":
            result = shell.ls(args) 
            if result != 0:
                print(result, end="\n\n")
        if args[0] == "cd":
            result = shell.cd(args)

        if args[0] == "config":
            config_name = find(glob(os.getcwd() + "/.*.*"), ".pyshell.conf")
            if config_name == 1:
                print("Creando configuración...")
                config = configparser.ConfigParser()
                config['CUSTOMIZATION'] = {
                        'color_handler': 'default',
                        'color': 'default',
                        'begin_text': 'default'
                }
                config['PREFERENCES'] = {
                        'editor': 'default',
                        'auto_git': 'false'
                }
                with open('.pyshell.conf', 'w') as configfile:
                    config.write(configfile)
                print("Puedes cambiar la configuración con 'config edit [seccion] [config]'")
            try:
                config = configparser.ConfigParser()
                config.read(".pyshell.conf")

                if args[1] == "ls":
                    shell.config.lsconfs(config)
                if args[1] == "edit":
                    try:
                        error = shell.config.editconf(config,args[2],args[3],args[4])
                        if error == -1:
                            print("Seccion o valor no existentes")
                    except IndexError:
                        print("Argumentos insuficientes, escribe 'help' para obtener ayuda")
                        print("Debes de especificar la seccion y la configuración que quieras cambiar 'config edit CUSTOMIZATION color_handler [valor]'")
                if args[1] == "get":
                    try:
                        conf_usr = shell.config.getconf(config,args[2], args[3])
                        if conf_usr != -1:
                            print(conf_usr)
                        else:
                            print("Seccion o configuración no disponible (No existe)")
                    except IndexError:
                        print("Argumentos insuficientes, escribe 'help' para obtener ayu da")
                        print("Debes de especificar la seccion y la configuración que quieras obtener. Ejemplo 'config get CUSTOMIZATION color'")
                if args[1] == "reload":
                    shell.config.reload()
            except IndexError:
                print(find(glob(os.getcwd() + "/.*.*"), ".pyshell.conf"))
    sys.exit(0)     

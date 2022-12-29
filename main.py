import sys, os, configparser
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
    auto_git = False
    auto_makefile = False
    editor = "default"
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
    secciones = ["CUSTOMIZATION","PREFERENCES"]
    for z,x in enumerate(secciones):
        if secciones[z] == "CUSTOMIZATION":
            for x in configs[x]:
                if x == 'color_handler':
                    color_handler = configs['CUSTOMIZATION'][x]
                elif x == 'color':
                    color = configs['CUSTOMIZATION'][x]
                elif x == 'begin_text':
                    begin_text = configs['CUSTOMIZATION'][x]
        elif secciones[z] == "PREFERENCES":
            for x in configs[x]:
                if x == "editor":
                    editor = configs['PREFERENCES'][x]
                elif x == 'auto_git':
                    auto_git = configs.getboolean('PREFERENCES',x)
                elif x == 'auto_makefile':
                    auto_makefile = configs.getboolean('PREFERENCES',x)

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
                try:
                    return glob(args[2] + "/**/*")
                except IndexError:
                    return glob(os.getcwd() + "/**/*")
            if args[1] == "-d":
                try:
                    os.system(f"ls --color=auto {args[2]}")
                except IndexError:
                    os.system("ls --color=auto")
                return ""
            raise IndexError("placeholder")
        except IndexError:
            try:
                return glob(os.path.join(args[1],'*'))
            except IndexError:
                return glob(os.getcwd() + "/*")
            except:
                print(sys.exc_info())
    
    def cd(args):
        os.chdir(args[1])

    def clear():
        os.system("clear")
    
    def touch(args):
        open(args[1], 'w').close()

    def python(args):
        try:
            command = []
            for z,x in enumerate(args):
                if z == 0:
                    continue
                command.append(x)
            exec("".join(map(str,command)))
        except IndexError:
            print("python-shell: Argumentos insuficientes")
        except:
            print(sys.exc_info()[1])

    def linux(args):
        try:
            command = []
            for z,x in enumerate(args):
                if z == 0:
                    continue
                command.append(x)
            os.system(" ".join(map(str,command)))
        except IndexError:
            print("linux-shell: Argumentos insuficientes")
        except:
            print(sys.exc_info()[1])

    def edit(args):
        try:
            if editor == "default":
                os.system(f"vim {args[1]}")
            else:
                os.system(f"{editor} {args[1]}")
        except NameError as exc:
            print("Configuracion corrupta,",exc)
            choice = input("Eliminar configuracion? (S/N): ")
            if choice in ["S",'s','Y','y','yes','Yes','YES','SI','Si','si','']:
                os.remove(".pyshell.conf")
                shell.config.reload()
            elif choice in ['N','n','No','no','Nope','nope','NO']:
                print("Configuracion no eliminada, saliendo para no crear danos")
                sys.exit(1)
    def write(args):
        try:
            if args[1] == ">>":
                file = open(args[1],'a')
            elif args[1] == ">":
                file = open(args[1],'w')
            text = []
            for x,z in enumerate(args):
                if x in [0,1]:
                    continue
                text.append(z)
            file.write(" ".join(map(str,text)))
    def new(args):
        if args[1] == "project":
            if args[3] == "c":
                lang = args[3]
                if auto_makefile == True:
                    try:
                        path = os.path.join(args[4],'Makefile')
                        os.system(f'mkdir -p {args[4]}')
                    except IndexError:
                        path = os.path.join(os.getcwd(),'Makefile')
                    open(f'{os.path.join(args[4],"main.c")}','w').close()
                    makefile_template = open('templates/makefile','r')
                    with open(path,'w') as file:
                        file.write(f"""
all: {args[2]}
NAME = {args[2]}
WARNINGS = -Wall
DEBUG = -ggdb -fno-omit-frame-pointer
OPTIMIZE = -O2

{args[2]}: Makefile main.c
{makefile_template.read()}
""")
                    makefile_template.close()
            if auto_git == True:
                try:
                    os.system(f'git init {args[4]}; git branch -m main')
                except IndexError:
                    os.system(f"git init .; git branch -m main")
            if args[3] == "python":
                try:
                    os.system(f'mkdir -p {args[4]}')
                    shell.touch(['',os.path.join(args[4],'main.py')])
                except IndexError:
                    shell.touch(['','main.py'])
        
        if args[1] == "git_project":
            try:
                args[5]
            except IndexError:
                return -1
            else:
                write(['placeholder','README.md','>',"#{}".format(args[2])])
                os.system(f"git init {args[3]}; git branch -m main; git pul")
                if args[4] == "-remote":
                    os.system(f"git remote add origin {args[5]}")


    def read(args):
        try:
            if os.path.exists(args[1]) == True:
                if os.path.isfile(args[1]) != True:
                    print('read: No es un archivo')
                    return -1
            else:
                print('read: El archivo no existe')
                return -1
            file = open(args[1],'r')
            print(file.read())
            file.close()
            return 0
        except IndexError:
            print('read: Argumentos insuficientes')
            return -1
    
    def remove(args):
        try:
            nexists = 0
            for x in args:
                if os.path.exists(x) == True:
                    if os.path.isfile == True:
                        os.remove(x)
                    else:
                        shutil.rmtree(x)
                else:
                    nexists += 1
            return (0,nexists)
        except PermissionError as e:
            print(e,'\nForzando la eliminacion...')
            nexists = 0
            for x in args:
                if os.path.exists(x) == True:
                    if os.path.isfile == True:
                        os.system(f"sudo rm {x}")
                    else:
                        os.system(f"sudo rm -rf {x}")
                else:
                    nexists += 1
            return (0,nexists)
        except IndexError:
            print("rm: Argumentos insuficientes")
        except:
            return (1,sys.exc_info())

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
            try:
                configs = configparser.ConfigParser()
                configs.read(".pyshell.conf")
                secciones = ["CUSTOMIZATION","PREFERENCES"]
                global color_handler, color, begin_text, auto_git, auto_makefile, editor
                for z,x in enumerate(secciones):
                    if secciones[z] == "CUSTOMIZATION":
                        for x in configs[x]:
                            if x == 'color_handler':
                                color_handler = configs['CUSTOMIZATION'][x]
                            elif x == 'color':
                                color = configs['CUSTOMIZATION'][x]
                            elif x == 'begin_text':
                                begin_text = configs['CUSTOMIZATION'][x]
                    elif secciones[z] == "PREFERENCES":
                        for x in configs[x]:
                            if x == "editor":
                                editor = configs['PREFERENCES'][x]
                            elif x == "auto_git":
                                auto_git = configs['PREFERENCES'][x]
                            elif x == "auto_makefile":
                                auto_makefile = configs['PREFERENCES'][x]
            except:
                color_handler = "default"
                color = "default"
                begin_text = "default"
                editor = "default"
                auto_git = "default"
                auto_makefile = "default"
                return -1
# Main func
if __name__ == "__main__":
    os.system("clear")
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
            print(result, end="\n")
            continue
        if args[0] == "cd":
            try:
                shell.cd(args)
            except:
                print(sys.exc_info()[1])
            finally:
                continue
        if args[0] == "rm":
            error = shell.remove(args)
            if error[0] != 0:
                print(error[1][1])
            else:
                if len(args) == 2:
                    if error[1] != 0:
                        print("rm: No existe el archivo o directorio")
                else:
                    if error[1] != 0:
                        print("rm: Uno o mas archivos/directorios no existen")
        if args[0] == "clear":
            shell.clear()
            continue
        if args[0] == "create":
            shell.touch(args)
            continue
        if args[0] == "new":
            try:
                args[3]
            except IndexError:
                print("Argumentos insuficientes, escribe help para obtener ayuda")
                continue
            else:
                shell.new(args)
            continue
        if args[0] == "edit":
            shell.edit(args)
            continue
        if args[0] == "read":
            shell.read(args)
            continue
        if args[0] == "python":
            shell.python(args)
            continue
        if args[0] == "linux":
            shell.linux(args)
            continue
        # Mucho comando    
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
                        'auto_git': 'false',
                        'auto_makefile': 'false'
                }
                try:
                    with open('.pyshell.conf', 'w') as configfile:
                        config.write(configfile)
                except:
                    print("Error al intentar crear un archivo de configuracion")
                    print(sys.exc_info()[1])
                    continue
                print("Puedes cambiar la configuración con 'config edit [seccion] [config]'")
            try:
                config = configparser.ConfigParser()
                config.read(".pyshell.conf")

                if args[1] == "ls":
                    shell.config.lsconfs(config)
                    continue
                if args[1] == "edit":
                    try:
                        error = shell.config.editconf(config,args[2],args[3],args[4])
                        if error == -1:
                            print("Seccion o valor no existentes")
                    except IndexError:
                        print("Argumentos insuficientes, escribe 'help' para obtener ayuda")
                        print("Debes de especificar la seccion y la configuración que quieras cambiar 'config edit CUSTOMIZATION color_handler [valor]'")
                    finally:
                        continue
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
                    finally:
                        continue
                if args[1] == "reload":
                    if shell.config.reload() == -1:
                        print("Configuracion no existente, tomando valores predeterminados...")
                        continue
                #Comando config terminado

            except IndexError:
                print(find(glob(os.getcwd() + "/.*.*"), ".pyshell.conf"))
            finally:
                continue
        print("No existe el comando")
    sys.exit(0)     

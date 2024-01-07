from neon_filesystem import *

MOVEOUT_FOLDER = "moveout"

CONSOLE_VERSION : Version = Version(0, 1, 0, "NeonFileSystem Console Manager")
VERSION.history = np.array([
    WhatsNew(
        Version(0, 0, 0),
        Version(1, 0, 0),
        add="control from the console",
        remove="",
        change="",
        fixes="",
        note = ""
    )
])

def create_help(name : Tuple[str, str], synopsis : str, description : str, options : Tuple[str, str], examples : list = []) -> str:
    out : str = "\n"
    def bold(text : str) -> str:
        return TextStyle.style(text, TextStyle.BOLD)
    def current(text : str) -> str:
        return TextStyle.style(text, TextStyle.BOLD_CYAN)
    def argument(text : str) -> str:
        return TextStyle.style(text, TextStyle.GREEN)
    def funct(text : str) -> str:
        return TextStyle.style(text, TextStyle.CYAN)
    
    out += bold("NAME") + "\n"
    out += f"\t{current(name[0])} - {name[1]}\n\n" 
    
    out += bold("SYNOPSIS") + "\n"
    out += f"\t{TextStyle.style('>', TextStyle.MAGENTA)} {current(name[0])} {synopsis}\n\n"
    
    out += bold("DESCRIPTION") + "\n\t" + description + "\n\n"
    for opt in options:
        tmp = str.split(opt[0], ",")
        for i in range(len(tmp)):
            tmp[i] = argument(tmp[i])
        
        out += f"\t{ ','.join(tmp) }\n"
        out += f"\t\t{opt[1]}\n\n"
    
    if len(examples) > 0:
        out += TextStyle.style("EXAMPLES", TextStyle.BOLD) + "\n"
        for ex in examples:
            out += f"\t{TextStyle.style('>', TextStyle.MAGENTA)} {current(name[0])} {argument(ex)}\n\n"
        
    tmp = str.split(out, "^^")
    out = ""
    
    for i in range(len(tmp)):
        if i % 2 == 1:
            out += bold(tmp[i])
        else:
            out += tmp[i]
            
    tmp = str.split(out, "!!!")
    out = ""
    
    for i in range(len(tmp)):
        if i % 2 == 1:
            out += funct(tmp[i])
        else:
            out += tmp[i]
    
    tmp = str.split(out, "***")
    out = ""
    
    for i in range(len(tmp)):
        if i % 2 == 1:
            out += argument(tmp[i])
        else:
            out += tmp[i]
    
    return out

# "^^" - BOLD
# "!!!" - HIGHLIGHT COLOR COMMAND
# "***" - HIGHLIGHT COLOR ARGUMENT
console_documentation = {
    "help" : create_help(
        ("help", "help with commands"),
        "[***COMMAND***]...",
        "Show manual page for ***COMMAND*** with synopsis, description and examples.\n\tSame as !!!man!!!.",
        [("-a, -A", "Show all available manual pages"), ("-l, -L", "Show list of available commands")],
        ["!!!help!!!", "!!!ls!!!", "!!!mkdir!!!"]
    ),
    "man" : create_help(
        ("help", "help with commands"),
        "[***COMMAND***]...",
        "Show manual page for ***COMMAND*** with synopsis, description and examples.\n\tSame as !!!help!!!.",
        [("-a, -A", "Show all available manual pages"), ("-l, -L", "Show list of available commands")],
        ["!!!help!!!", "!!!ls!!!", "!!!mkdir!!!"]
    ),
    "exit" : create_help(
        ("exit", "close console"),
        "",
        "Will end neon filesystem console process",
        [],
        []
    ),
    "clear" : create_help(
        ("clear", "clear console"),
        "",
        "Will clear console buffer.",
        [],
        []
    ),
    "cd" : create_help(
        ("cd", "change current directory"),
        "[***PATH***]",
        "Will set current neon_filesystem directory tp given ***PATH***.",
        [],
        ["nroot/user/desktop", "..", "desktop/trash/"]
    ),
    "ls" : create_help(
        ("ls", "list directory content"),
        "[***OPTIONS***] [***PATH***]...",
        "Will show content of directory in ***PATH***.\n\tIf ***PATH*** is empty, will show content of current directory.",
        [("-r, -R", "Recursively show content of subdirectories")],
        ["nroot/tmp", "", "-R nroot"]
    ),
    "touch" : create_help(
        ("touch", "create empty file"),
        "[***FILE***]...",
        "Will create new empty file in ***FILE*** path and name.",
        [],
        ["nroot/tmp/log23.tmp nroot/tmp/log24.tmp", "calculator.py", "/desktop/trash/image03.png"]
    ),
    "mkdir" : create_help(
        ("mkdir", "create empty directoory"),
        "[***DIRECTORY***]...",
        "Will create new empty direcory in ***DIRECTORY*** path and name.",
        [],
        ["nroot/tmp/snap nroot/tmp/wine", "new-folder", "/desktop/homework"]
    ),
    "rm" : create_help(
        ("rm", "remove file or directory"),
        "[***OPTIONS***]... [***FILE***]...",
        "Will remove file or directory in ***FILE*** path and name.",
        [("-r, -R", "Remove folder even if it is not empty")],
        ["nroot/tmp/log27.tmp nroot/tmp/log28.tmp", "-r desktop", "trash/image.png"]
    ),
    "cat" : create_help(
        ("cat", "print file content"),
        "[***FILE***]...",
        "Will print content of ***FILE*** file",
        [],
        ["nroot/tmp/log27.tmp nroot/tmp/log28.tmp", "homework.docs", "trash/notes.txt"]
    ),
    "moveout" : create_help(
        ("moveout", "export files and directories to external filesystem"),
        "[***PATH***]...",
        f"Will export files and directories from ***FILE*** neon_filesystem path\n\tto ./{MOVEOUT_FOLDER}/filesystem_name/***PATH*** path",
        [],
        ["nroot/tmp/log27.tmp nroot/tmp/log28.tmp", "nroot", "trash/notes.txt"]
    ),
}   

class Console:
    def __init__(self):
        self.fs : FileSystem = None
        self.input_history = []
        self.running = True
        
        self.autosave = True
        self.__loaded_fs_path : Path = None
        
        FileSystem.disable_output()
        self.load_filesystem(f"{DEFAULT_SYSTEM_FILE_NAME}.{DEFAULT_SYSTEM_FILE_EXTENSION}")
        FileSystem.enable_output()
        
        if self.fs == None:
            FileSystem.message(f"Tried to load default filesystem. There is no such file!\nNew one will be created and loaded!")
            self.fs = FileSystem.default_fs()
            self.save_filesystem(f"{DEFAULT_SYSTEM_FILE_NAME}.{DEFAULT_SYSTEM_FILE_EXTENSION}")
            
    def loop(self):
        while self.running:
            inp : str = self.get_input()
            commands : list(str) = inp.split(" ")
            commands = [item for item in commands if item != ""]
            if len(commands) == 0:
                continue
            
            match commands[0]:
                case "exit":
                    self.exit()
                case "cd":
                    if len(commands) > 1:
                        self.set_current_directory(commands[1:])
                case "ls":
                    self.show_directory_content(commands[1:])
                case "clear":
                    self.clear_console()
                case "echo":
                    tmp = inp.split(" ", 1)
                    if len(tmp) == 1:
                        self.echo("")
                    else:
                        self.echo(tmp[1])
                case "help" | "man":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TextStyle.highlight(commands[0])} missing arguments!\nTry {TextStyle.highlight('help help')} for additional information!")
                    else:
                        self.show_help(commands[1:])
                case "touch":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TextStyle.highlight('touch')} missing arguments!")
                    else:
                        self.create_empty_file(commands[1:])
                case "mkdir":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TextStyle.highlight('mkdir')} missing arguments!")
                    else:
                        self.create_empty_directory(commands[1:])
                case "rm":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TextStyle.highlight('rm')} missing arguments!")
                    else:
                        self.remove_item(commands[1:])
                case "cat":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TextStyle.highlight('cat')} missing arguments!")
                    else:
                        self.show_file_content(commands[1:])
                case "moveout":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TextStyle.highlight('moveout')} missing arguments!")
                    else:
                        self.moveout(commands[1:])
                        
            if self.autosave and self.fs.is_changed():
                self.save_filesystem(self.__loaded_fs_path)
                
    # region Commands
    
    def echo(self, text : str):
        print(text)
    
    def exit(self):
        self.running = False
        FileSystem.message("NeonFileSystem Console Manager was closed!\nGoodbye!")
    
    def set_current_directory(self, args : List[str]):
        path = self.__process_path(Path(args[0]))
        self.fs.set_current_directory_path(path)
            
    def show_directory_content(self, args : List[str]):
        resursive = False
        if len(args) > 0 and (args[0] == "-r" or args[0] == "-R"):
            resursive = True
            args = args[1:]
        if len(args) == 0:
            self.fs.get_current_directory().show(resursive)
            return
        start_path : Path = Path(self.fs.current_directory_path)
        for path_str in args:
            self.fs.set_current_directory_path(start_path)
            path : Path = self.__process_path(Path(path_str))
            self.fs.set_current_directory_path(path)
            self.fs.get_current_directory().show(resursive)
            self.fs.set_current_directory_path(start_path)
        
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_empty_file(self, args : List[str]):
        start_path : Path = Path(self.fs.current_directory_path)
        for path_str in args:
            self.fs.set_current_directory_path(start_path)
            path = self.__process_path(Path(path_str))
            self.fs.set_current_directory_path(Path(self.fs.current_directory_path.directories + path.directories[:-1]))
            tmp = path.directories[-1].rsplit(".", 1)
            # if file extension not specified it will assigne ".bin" extension to it
            if len(tmp) < 2:
                tmp.append("bin")
            self.fs.get_current_directory().create_file(tmp[0], tmp[1])
            self.fs.set_current_directory_path(start_path)
            
    def create_empty_directory(self, args : List[str]):
        for path_str in args:
            path = self.__process_path(Path(path_str))
            start_path : Path = Path(self.fs.current_directory_path)
            
            self.fs.set_current_directory_path(Path(path.directories[:-1]))
            self.fs.get_current_directory().create_subdirectory(path.directories[-1])
            self.fs.set_current_directory_path(start_path)
    
    def remove_item(self, args : List[str]):
        recursive = False
        if args[0] == "-r" or args[0] == "-R":
            recursive = True
            args = args[1:]
        start_path = Path(self.fs.current_directory_path)
        for path in args:
            self.fs.set_current_directory_path(start_path)
            path = self.__process_path(Path(path))
            if len(path.directories) == 1:
                FileSystem.message("You cant delete main nroot directory ;-)")
                continue
            FileSystem.disable_output(True)
            self.fs.set_current_directory_path(Path(path.directories[:-1]))
            file = self.fs.get_current_directory().get_file(path.directories[-1])
            FileSystem.enable_output(True)
            if type(file) == File:
                file.parent_directory.delete_file(file.name)
                continue
            FileSystem.disable_output(True)
            dr = self.fs.get_current_directory().get_subdirectory(path.directories[-1])
            FileSystem.enable_output(True)
            if type(dr) == Directory:
                if len(dr.content) > 0 and not recursive:
                    FileSystem.error(f"Cant delete directory because it is not empty! To do it use recursive flag {TextStyle.highlight('-r')}!")
                    continue
                dr.parent_directory.delete_subdirectory(path.directories[-1], recursive)
                continue
            FileSystem.message(f"There is no item {TextStyle.highlight(path.str())}!")
            self.fs.set_current_directory_path(start_path)
    
    def show_file_content(self, args : List[str]):
        start_path = Path(self.fs.current_directory_path)
        for path_str in args:
            self.fs.set_current_directory_path(start_path)
            path = self.__process_path(Path(path_str))
            self.fs.set_current_directory_path(Path(path.directories[:-1]))
            file = self.fs.get_current_directory().get_file(path.directories[-1])
            FileSystem.enable_output(True)
            if type(file) == File:
                print(f"\n{file.get_content()}\n")
            else:
                FileSystem.message(f"There is no file in {TextStyle.highlight(path.str())}!")
            self.fs.set_current_directory_path(start_path)
    
    def show_help(self, args : List[str]):
        if args[0] == "-a" or args[0] == "-A":
            self.show_help(list(console_documentation.keys()))
        elif args[0] == "-l" or args[0] == "-L":
            for comm in list(console_documentation.keys()):
                print(comm)
        else:
            for arg in args:
                if arg in list(console_documentation.keys()):
                    print(f"Man page for {TextStyle.highlight(arg)}")
                    print("—" * 70)
                    print(console_documentation[arg])
                    print("—" * 70)
                else:
                    FileSystem.message(f"There is no man page for {TextStyle.highlight(arg)}!")
    
    def moveout(self, args : List[str]):
        os.makedirs(os.path.join(MOVEOUT_FOLDER, self.fs.filesystem_name), exist_ok=True)
        start_path = Path(self.fs.current_directory_path)
        for path_str in args:
            self.fs.set_current_directory_path(start_path)
            path = self.__process_path(Path(path_str))
            if len(path.directories) == 1:
                self.moveout_dir(self.fs.nroot)
                FileSystem.message("Filesystem was exported!")
                break
            
            FileSystem.disable_output(True)
            
            self.fs.set_current_directory_path(Path(path.directories[:-1]))
            file = self.fs.get_current_directory().get_file(path.directories[-1])
            
            if type(file) == File:
                self.moveout_file(file)
                continue
            
            dr = self.fs.get_current_directory().get_subdirectory(path.directories[-1])
            
            if type(dr) == Directory:
                self.moveout_dir(dr)
                continue
            
            FileSystem.enable_output(True)
            FileSystem.message(f"There is no item {TextStyle.highlight(path.str())}!")
            self.fs.set_current_directory_path(start_path)
        
    def moveout_file(self, file : File):
        path = file.get_path(False)
        
        os.makedirs(os.path.join(MOVEOUT_FOLDER, self.fs.filesystem_name, path.str()), exist_ok=True)
        with open(os.path.join(MOVEOUT_FOLDER, self.fs.filesystem_name, path.str(), file.get_full_name()), 'w') as out_file:
            out_file.write(file.get_content())
            
    def moveout_dir(self, dr : Directory):
        path = dr.get_path()
        os.makedirs(os.path.join(MOVEOUT_FOLDER, self.fs.filesystem_name, path.str()), exist_ok=True)
        
        for item in dr.content:
            if type(item) == File:
               self.moveout_file(item)
               continue
            elif type(dr) == Directory:
                self.moveout_dir(item)
                continue
    
    # endregion
    
    def __process_path(self, path : Path) -> Path:
        tmp_path = Path(path)
        
        if tmp_path.directories[0] != self.fs.get_root_name():
            tmp_path = Path(self.fs.get_current_directory().get_path().directories + path.directories)
            
        path_cp = Path()
        for dir in tmp_path.directories:
            if dir == ".":
                if len(path_cp.directories) == 0:
                    path_cp = Path(tmp_path)
            elif dir == "..":
                if len(path_cp.directories) > 1:
                    path_cp = Path(path_cp.directories[:-1])
            else:
                path_cp.add_path(dir)
        return path_cp
             
    
    def load_filesystem(self, path : Path):
        if type(path) == Path:
            path = path.str()
            if not os.path.isfile(path):
                FileSystem.error(f"There is no {TextStyle.highlight(str(path))} file!")
                return
            if os.path.splitext(path)[-1][1:] != DEFAULT_SYSTEM_FILE_EXTENSION:
                FileSystem.warning(f"Given file extension is not {TextStyle.highlight(DEFAULT_SYSTEM_FILE_EXTENSION)}!")
            fs = FileSystem()
            fs.load(Path(path))
            if not fs.is_valid():
                FileSystem.error(f"Something went wrong when loading filesystem, filesystem was not loaded!")
                return
            self.fs = fs
            self.fs.set_as_global()
            FileSystem.message(f"Filesystem {TextStyle.highlight(self.fs.filesystem_name)} has been successfully loaded!")
            self.__loaded_fs_path = path
        elif type(path) == str:
            self.load_filesystem(Path(path))
        else:
            print(type(path))
            raise TypeError(f"Invalid path type! Path \"{path}\" is of type \"{type(path)}\"")
    
    def save_filesystem(self, path : Path):
        if type(path) == Path:
            self.fs.save(path.str())
        else:
            self.fs.save(path)
    
    
    def get_input(self, message : str = "") -> str:
        FileSystem.message(message)
        curr_path = ""
        if type(self.fs) == FileSystem and self.fs.is_valid():
            curr_path = self.fs.current_directory_path
            path_text = TextStyle.style(curr_path.directories[0], TextStyle.BOLD_MAGENTA)
            if len(curr_path.directories) > 1:
                path_text += TextStyle.style("/" + Path(curr_path.directories[1:]).str(), TextStyle.MAGENTA)
        print(f"{path_text} > ", end="")
        inp = input()
        if inp != "":
            self.input_history.append(inp)
        return inp

console : Console = Console()
console.loop()

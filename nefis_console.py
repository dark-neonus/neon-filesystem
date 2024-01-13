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
        return TS.style(text, TS.BOLD)
    def current(text : str) -> str:
        return TS.style(text, TS.BOLD_CYAN)
    def argument(text : str) -> str:
        return TS.style(text, TS.GREEN)
    def funct(text : str) -> str:
        return TS.style(text, TS.CYAN)
    
    out += bold("NAME") + "\n"
    out += f"\t{current(name[0])} - {name[1]}\n\n" 
    
    out += bold("SYNOPSIS") + "\n"
    out += f"\t{TS.style('>', TS.MAGENTA)} {current(name[0])} {synopsis}\n\n"
    
    out += bold("DESCRIPTION") + "\n\t" + description + "\n\n"
    for opt in options:
        tmp = str.split(opt[0], ",")
        for i in range(len(tmp)):
            tmp[i] = argument(tmp[i])
        
        out += f"\t{ ','.join(tmp) }\n"
        out += f"\t\t{opt[1]}\n\n"
    
    if len(examples) > 0:
        out += TS.style("EXAMPLES", TS.BOLD) + "\n"
        for ex in examples:
            out += f"\t{TS.style('>', TS.MAGENTA)} {current(name[0])} {argument(ex)}\n\n"
        
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
        f"Will export files and directories from ***FILE*** neon_filesystem path\n\tto ./{MOVEOUT_FOLDER}/filesystem_name/***PATH*** path of external filesyste,",
        [],
        ["nroot/tmp/log27.tmp nroot/tmp/log28.tmp", "nroot", "trash/notes.txt"]
    ),
    "movein" : create_help(
        ("movein", "import files and directories from external filesystem"),
        "[***DESTIONATION***] [***SOURCE***]...",
        f"Will import files and directories from all ***SOURCE*** paths of external filesystem\n\tto single ***DESTIONATION*** path of neon_filesystem\n\tNeed a pair of destination-source paths",
        [("-h, -H", f"Hard import mode, usefull only when import nroot.\n\t\t Will delete all files and directories that is not in\n\t\t./{MOVEOUT_FOLDER}/filesystem_name/ and subdirectories of external filesystem\n\t\tWill ignore all given paths"),
         ("-o, -O", "If files already exist will overwrite it")],
        ["nroot/user/desktop/games/ root/user/cool-man/games/doom", "-h nroot", f"-o ./user ./{MOVEOUT_FOLDER}/filesystem_name/nroot/user/photos"]
    ),
}   

def load_file_content(file_path) -> tuple():
    def is_text_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file.read()
            return True
        except UnicodeDecodeError:
            return False

    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Extract file name and extension
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))

        try:
            if is_text_file(file_path):
                # Load as text
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                return content, file_name, file_extension
            else:
                # Load as binary
                with open(file_path, 'rb') as file:
                    binary_content = file.read()
                binary_string = ''.join(format(byte, '08b') for byte in binary_content)
                return binary_string, file_name, file_extension
        except Exception as e:
            FileSystem.error(f"An error {TS.highlight(e)} occurred while loading file {TS.highlight(file_path)}", load_file_content)
            return None, None, None
    else:
        FileSystem.error(f"The file {TS.highlight(file_path)} does not exist.", load_file_content)
        return None, None, None


class Console:
    def __init__(self):
        self.fs : FileSystem = None
        self.input_history = []
        self.running = True
        
        self.autosave = True
        self.__loaded_fs_path : Path = None
        
        FileSystem.disable_output(True)
        self.load_filesystem(f"{DEFAULT_SYSTEM_FILE_NAME}.{DEFAULT_SYSTEM_FILE_EXTENSION}")
        FileSystem.enable_output(True)
        
        if self.fs == None:
            FileSystem.message(f"Tried to load default filesystem. There is no such file!\nNew one will be created and loaded!", self.__init__)
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
                        FileSystem.message(f"Command {TS.highlight(commands[0])} missing arguments!\nTry {TS.highlight('help help')} for additional information!", self.loop)
                    else:
                        self.show_help(commands[1:])
                case "touch":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TS.highlight('touch')} missing arguments!", self.loop)
                    else:
                        self.create_empty_file(commands[1:])
                case "mkdir":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TS.highlight('mkdir')} missing arguments!", self.loop)
                    else:
                        self.create_empty_directory(commands[1:])
                case "rm":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TS.highlight('rm')} missing arguments!", self.loop)
                    else:
                        self.remove_item(commands[1:])
                case "cat":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TS.highlight('cat')} missing arguments!", self.loop)
                    else:
                        self.show_file_content(commands[1:])
                case "moveout":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TS.highlight('moveout')} missing arguments!", self.loop)
                    else:
                        self.moveout(commands[1:])
                case "movein":
                    if len(commands) == 1:
                        FileSystem.message(f"Command {TS.highlight('movein')} missing arguments!", self.loop)
                    else:
                        self.movein(commands[1:])
                case _:
                    FileSystem.message(f"There is no {TS.highlight(commands[0])} command!", self.loop)
                        
            if self.autosave and self.fs.is_changed():
                self.save_filesystem(self.__loaded_fs_path)
                
    # region Commands
    
    def echo(self, text : str):
        print(text)
    
    def exit(self):
        self.running = False
        FileSystem.message("NeonFileSystem Console Manager was closed!\nGoodbye!", self.exit)
    
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
        for path_str in args:
            path : Path = self.__process_path(Path(path_str))
            if self.fs.is_dir_exist(path):
                self.fs.get_directory(path).show(resursive)
            else:
                self.fs.message(f"There is no {TS.highlight(path)} directory!")
        
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_empty_file(self, args : List[str]):
        for path_str in args:
            path = self.__process_path(Path(path_str))
            tmp = path.directories[-1].rsplit(".", 1)
            # if file extension not specified it will assigne ".bin" extension to it
            if len(tmp) < 2:
                tmp.append("bin")
            self.fs.get_directory(Path(path.directories[:-1])).create_file(tmp[0], tmp[1])
            
    def create_empty_directory(self, args : List[str]):
        for path_str in args:
            
            path = self.__process_path(Path(path_str))
            
            for i in range(1, len(path.directories) + 1):
                tmp = Path(path.directories[:i])
                if not self.fs.is_dir_exist(tmp):
                    self.fs.get_directory(Path(tmp.directories[:-1])).create_subdirectory(tmp.directories[-1])
            
    
    def remove_item(self, args : List[str]):
        recursive = False
        if args[0] == "-r" or args[0] == "-R":
            recursive = True
            args = args[1:]
        for path in args:
            path = self.__process_path(Path(path))
            if len(path.directories) == 1:
                FileSystem.message("You cant delete main nroot directory ;-)", self.remove_item)
                continue
            
            if self.fs.is_file_exist(path):
                file = self.fs.get_file(path)
                file.parent_directory.delete_file(file.name)
                continue
            
            if self.fs.is_dir_exist(path):
                dr = self.fs.get_directory(path, True)
                if len(dr.content) > 0 and not recursive:
                    FileSystem.error(f"Cant delete directory because it is not empty! To do it use recursive flag {TS.highlight('-r')}!", self.remove_item, self.remove_item)
                    continue
                dr.parent_directory.delete_subdirectory(path.directories[-1], recursive)
                continue
            
            FileSystem.message(f"There is no item {TS.highlight(path.str())}!", self.remove_item)
    
    def show_file_content(self, args : List[str]):
        start_path = Path(self.fs.current_directory_path)
        for path_str in args:
            path = self.__process_path(Path(path_str))
            
            if self.fs.is_file_exist(path):
                print(f"\n{self.fs.get_file(path).get_content()}\n")
            else:
                FileSystem.message(f"There is no file in {TS.highlight(path.str())}!", self.show_file_content)
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
                    print(f"Man page for {TS.highlight(arg)}")
                    print("—" * 70)
                    print(console_documentation[arg])
                    print("—" * 70)
                else:
                    FileSystem.message(f"There is no man page for {TS.highlight(arg)}!", self.show_help)
    
    def moveout(self, args : List[str]):
        os.makedirs(os.path.join(MOVEOUT_FOLDER, self.fs.filesystem_name), exist_ok=True)
        for path_str in args:
            path = self.__process_path(Path(path_str))
            if len(path.directories) == 1:
                self.moveout_dir(self.fs.nroot)
                FileSystem.message("Filesystem was exported!", self.moveout)
                break
            
            FileSystem.disable_output(True)
            
            if self.fs.is_file_exist(path):
                self.moveout_file(self.fs.get_file(path))
                continue
            
            if self.fs.is_dir_exist(path):
                self.moveout_dir(self.fs.get_directory(path))
                continue
            
            FileSystem.enable_output(True)
            FileSystem.message(f"There is no item {TS.highlight(path.str())}!", self.moveout)
        
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
    
    def movein(self, args : List[str], overwrite : bool = False, hard_import : bool = False):
        # Source path is path to object that wich will be imported
        # Destination path is path to directory in which will be imported
        # If source is /documents/list.txt and destination is /nroot/tmps, than list.txt will be imported in /nroot/tmps/  
        if len(args) == 0:
            FileSystem.error(f"Missing path arguments for {TS.highlight('movein')} command!", self.movein)
            return
        
        if args[0] == "-o" or args[0] == "-O":
            self.movein(args[1:], True, hard_import)
            return
        elif args[0] == "-h" or args[0] == "-H":
            self.movein(args[1:], True, True)
            return
        
        
        if len(args) == 1:
            if self.__process_path(args[0]).str() == self.fs.get_root_name():
                self.movein_nroot(overwrite, hard_import)
            else:
                self.movein([self.fs.current_directory_path] + args, overwrite, hard_import)
            return
        
        destination_path = self.__process_path(Path(args[0]))
        
        for source_path in args[1:]:
            
            if not self.fs.is_dir_exist(destination_path):
                FileSystem.error(f"There is no {TS.highlight(destination_path.str())} directory to import to!", self.movein)
                continue
            
            if not os.path.exists(source_path):
                FileSystem.error(f"There is no {TS.highlight(source_path)} item to import from!", self.movein)
                continue
            
            if os.path.isfile(source_path):
                self.movein_file(destination_path, source_path, overwrite)
            else:
                self.movein_dir(destination_path, source_path, overwrite, hard_import)
            
            
    def movein_file(self, destination_path : Path, source_path : str, overwrite : bool):
        content, file_name, file_extension = load_file_content(source_path)
            
        if file_name == None or content == None:
            return
        
        if file_extension == None:
            file_extension = "bin"
            
        if self.fs.is_file_exist(Path(destination_path.directories + [f"{file_name}.{file_extension[1:]}"])):
            if overwrite:
                file = self.fs.get_directory(destination_path, True).get_file(f"{file_name}.{file_extension[1:]}")
                file.set_content(content)
                file.set_name(file_name)
                file.data_type = file_extension[1:]
                FileSystem.message(f"File {TS.highlight(Path(destination_path.directories + [file.get_full_name()]).str())} was successfully overwrited!", self.movein_file)
            else:
                FileSystem.warning(f"File {TS.highlight(Path(destination_path.directories + [f'{file_name}.{file_extension[1:]}']).str())} already exist! To overwrite it, use {TS.highlight('-o')} flag!", self.movein_file)
        else:
            if self.fs.is_dir_exist(destination_path):
                self.fs.get_directory(destination_path).create_file(file_name, file_extension[1:], content)
                FileSystem.message(f"File {TS.highlight(Path(destination_path.directories + [f'{file_name}.{file_extension[1:]}']).str())} was successfully created!", self.movein_file)
            else:
                FileSystem.error(f"There is no {TS.highlight(destination_path.str())} directory!", self.movein_file)
            
            
    def movein_dir(self, destination_path : Path, source_path : str, overwrite : bool, hard_import : bool):
        dir_name = os.path.basename(source_path)
        
        if not self.fs.is_dir_exist(Path(destination_path.directories + [dir_name])):
            if self.fs.is_dir_exist(destination_path):
                self.fs.get_directory(destination_path).create_subdirectory(dir_name)
                FileSystem.message(f"Directory {TS.highlight(Path(destination_path.directories + [dir_name]).str())} was successfully created!", self.movein_dir)
            else:
                FileSystem.error(f"There is no {TS.highlight(destination_path.str())} directory!", self.movein_dir)
        dir_content = os.listdir(source_path)
        for item in dir_content:
            item_path = os.path.join(source_path, item)
            
            if os.path.isdir(item_path):
                self.movein_dir(Path(destination_path.directories + [dir_name]), item_path, overwrite, hard_import)
            elif os.path.isfile(item_path):
                self.movein_file(Path(destination_path.directories + [dir_name]), item_path, overwrite)
            else:
                self.fs.error(f"Somehow item {TS.highlight(item_path)} is nether file nor directory!", self.movein_dir)
                
        if hard_import:
            def get_item_name(item : File | Directory):
                if type(item) == File:
                    return item.get_full_name()
                elif type(item) == Directory:
                    return item.name
                else:
                    raise TypeError(f"Item must be of type 'File' or 'Directory' not '{type(item)}'!")
            
            current_content = self.fs.get_directory(Path(destination_path.directories + [dir_name])).content
            
            self.fs.get_directory(Path(destination_path.directories + [dir_name])).content = np.array([obj for obj in current_content if get_item_name(obj) in {item for item in dir_content}], dtype=object)
                
    def movein_nroot(self, overwrite : bool, hard_import : bool):
        moveout_nroot_path = os.path.join(MOVEOUT_FOLDER, self.fs.filesystem_name, self.fs.get_root_name())
        
        self.fs.disable_output(True)
        
        if not os.path.exists(moveout_nroot_path) or not os.path.isdir(moveout_nroot_path):
            os.makedirs(moveout_nroot_path)
        
        if hard_import:
            while len(self.fs.nroot.content) != 0:
                if type(self.fs.nroot.content[0]) == File:
                    self.fs.nroot.delete_file(self.fs.nroot.content[0].get_full_name())
                elif type(self.fs.nroot.content[0]) == Directory:
                    self.fs.nroot.delete_subdirectory(self.fs.nroot.content[0].name, True)
                else:
                    raise TypeError()
            
        for item in os.listdir(moveout_nroot_path):
            self.movein_dir(self.fs.nroot.get_path(), os.path.join(moveout_nroot_path, item), overwrite, hard_import)
        
        self.fs.enable_output(True)
        
        self.fs.message(f"Filesystem was successfully loaded!", self.movein_nroot)
    
            
            
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
                FileSystem.error(f"There is no {TS.highlight(str(path))} file!", self.load_filesystem)
                return
            if os.path.splitext(path)[-1][1:] != DEFAULT_SYSTEM_FILE_EXTENSION:
                FileSystem.warning(f"Given file extension is not {TS.highlight(DEFAULT_SYSTEM_FILE_EXTENSION)}!", self.load_filesystem)
            fs = FileSystem()
            fs.load(Path(path))
            if not fs.is_valid():
                FileSystem.error(f"Something went wrong when loading filesystem, filesystem was not loaded!", self.load_filesystem)
                return
            self.fs = fs
            self.fs.set_as_global()
            FileSystem.message(f"Filesystem {TS.highlight(self.fs.filesystem_name)} has been successfully loaded!", self.load_filesystem)
            self.__loaded_fs_path = path
        elif type(path) == str:
            self.load_filesystem(Path(path))
        else:
            raise TypeError(f"Invalid path type! Path \"{path}\" is of type \"{type(path)}\"")
    
    def save_filesystem(self, path : Path):
        if type(path) == Path:
            self.fs.save(path.str())
        else:
            self.fs.save(path)
    
    
    def get_input(self, message : str = "") -> str:
        FileSystem.message(message, self.get_input)
        curr_path = ""
        if type(self.fs) == FileSystem and self.fs.is_valid():
            curr_path = self.fs.current_directory_path
            path_text = TS.style(curr_path.directories[0], TS.BOLD_MAGENTA)
            if len(curr_path.directories) > 1:
                path_text += TS.style("/" + Path(curr_path.directories[1:]).str(), TS.MAGENTA)
        print(f"{path_text} > ", end="")
        inp = input()
        if inp != "":
            self.input_history.append(inp)
        return inp

console : Console = Console()
console.loop()

from neon_filesystem import *

CONSOLE_VERSION : Version = Version(0, 1, 0, "NeonFileSystem Console Manager")
VERSION.logs = np.array([
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
            FileSystem.message(f"Tried to load default filesystem. There is no such file!")
            self.__wait_for_system_loading()
            
    def loop(self):
        while self.running:
            inp : str = self.get_input()
            commands : list(str) = inp.split(" ")
            commands = [item for item in commands if item != ""]
            if len(commands) == 0:
                continue
            
            match commands[0]:
                case "exit":
                    self.running = False
                    FileSystem.message("NeonFileSystem Console Manager was closed!\nGoodbye!")
                case "cd":
                    if len(commands) == 1 or commands[1] == "":
                        continue
                    if commands[1] == "..":
                        if len(self.fs.current_directory.directories) > 1:
                            self.fs.current_directory.back()
                    elif len(Path(commands[1]).directories) > 0 and Path(commands[1]).directories[0] == self.fs.get_root_name():
                        self.fs.set_current_directory_path(commands[1])
                    else:
                        tmp : Path = Path(self.fs.current_directory)
                        tmp.add_path(commands[1])
                        self.fs.set_current_directory_path(tmp)
                case "ls":
                    resursive = len(commands) >= 2 and commands[1] == "-r"
                    self.fs.get_current_directory().show(resursive)
                case "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                case "touch":
                    curr_dir = self.fs.get_current_directory()
                    for name in commands[1:]:
                        tmp = name.rsplit(".", 1)
                        curr_dir.create_file(tmp[0], tmp[1])
                case "mkdir":
                    curr_dir = self.fs.get_current_directory()
                    for name in commands[1:]:
                        curr_dir.create_subdirectory(name)
                case "rm":
                    recursive = commands[1] == "-r"
                    for name in (commands[2:] if recursive else commands[1:]):
                        FileSystem.disable_output(True)
                        file = self.fs.get_current_directory().get_file(name)
                        FileSystem.enable_output(True)
                        if type(file) == File:
                            file.parent_directory.delete_file(file.name)
                            break
                        FileSystem.disable_output(True)
                        dr = self.fs.get_current_directory().get_subdirectory(name)
                        FileSystem.enable_output(True)
                        if type(dr) == Directory:
                            if len(dr.content) > 0 and not recursive:
                                FileSystem.error(f"Cant delete directory because it is not empty! To do it use recursive flag \"-r\"!")
                                break
                            dr.parent_directory.delete_subdirectory(name, recursive)
                            break
                        FileSystem.message(f"There is no item with name \"{name}\"!")
                
                        
            if self.autosave and self.fs.is_changed():
                self.save_filesystem(self.__loaded_fs_path)
    
    def load_filesystem(self, path : Path):
        if type(path) == Path:
            path = path.str()
            if not os.path.isfile(path):
                FileSystem.error(f"There is no \"{str(path)}\" file!")
                return
            if os.path.splitext(path)[-1][1:] != DEFAULT_SYSTEM_FILE_EXTENSION:
                FileSystem.warning(f"Given file extension is not \"{DEFAULT_SYSTEM_FILE_EXTENSION}\"!")
            fs = FileSystem()
            fs.load(Path(path))
            if not fs.is_valid():
                FileSystem.error(f"Something went wrong when loading filesystem, filesystem was not loaded!")
                return
            self.fs = fs
            self.fs.set_as_global()
            FileSystem.message(f"Filesystem \"{self.fs.filesystem_name}\" has been successfully loaded!")
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
    
    def __wait_for_system_loading(self):
        while type(self.fs) != FileSystem or not self.fs.is_valid():
            path = Path(self.get_input("Please enter path to file that contain filesystem!"))
            print(path.is_valid())
            if not path.is_valid():
                FileSystem.error("Entered path is invalid!")
            else:
                self.load_filesystem(path)
    
    def get_input(self, message : str = "") -> str:
        FileSystem.message(message)
        curr_path = ""
        if type(self.fs) == FileSystem and self.fs.is_valid():
            curr_path = self.fs.current_directory.str()
        print(f"{curr_path} > ", end="")
        inp = input()
        self.input_history.append(inp)
        return inp
    
    
console : Console = Console()
console.loop()
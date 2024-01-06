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
        if len(args) > 0 and args[0] == "-R":
            resursive = True
            args = args[1:]
        if len(args) == 0:
            self.fs.get_current_directory().show(resursive)
            return
        curr_dir_tmp : Path = Path(self.fs.current_directory_path)
        for path_str in args:
            path : Path = self.__process_path(Path(path_str))
            self.fs.set_current_directory_path(path)
            self.fs.get_current_directory().show(resursive)
        self.fs.set_current_directory_path(curr_dir_tmp)
        
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_empty_file(self, args : List[str]):
        for path_str in args:
            path = self.__process_path(Path(path_str))
            curr_dir_tmp : Path = Path(self.fs.current_directory_path)
            self.fs.set_current_directory_path(Path(self.fs.current_directory_path.directories + path.directories[:-1]))
            tmp = path.directories[-1].rsplit(".", 1)
            # if file extension not specified it will assigne ".bin" extension to it
            if len(tmp) < 2:
                tmp.append("bin")
            self.fs.get_current_directory().create_file(tmp[0], tmp[1])
            self.fs.set_current_directory_path(curr_dir_tmp)
            
    def create_empty_directory(self, args : List[str]):
        for path_str in args:
            path = self.__process_path(Path(path_str))
            curr_dir_tmp : Path = Path(self.fs.current_directory_path)
            
            self.fs.set_current_directory_path(Path(path.directories[:-1]))
            self.fs.get_current_directory().create_subdirectory(path.directories[-1])
            self.fs.set_current_directory_path(curr_dir_tmp)
    
    def remove_item(self, args : List[str]):
        recursive = False
        if args[0] == "-r" or args[0] == "-R":
            recursive = True
            args = args[1:]
        start_path = Path(self.fs.current_directory_path)
        for path in args:
            path = self.__process_path(Path(path))
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
            path = self.__process_path(Path(path_str))
            self.fs.set_current_directory_path(Path(path.directories[:-1]))
            file = self.fs.get_current_directory().get_file(path.directories[-1])
            FileSystem.enable_output(True)
            if type(file) == File:
                print(f"\n{file.get_data()}\n")
            else:
                FileSystem.message(f"There is no file in {TextStyle.highlight(path.str())}!")
        self.fs.set_current_directory_path(start_path)
    
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
    
    def __wait_for_system_loading(self):
        while type(self.fs) != FileSystem or not self.fs.is_valid():
            path = Path(self.get_input("Please enter path to file that contain filesystem!"))
            if not path.is_empty():
                FileSystem.error("Entered path is empty!")
            else:
                self.load_filesystem(path)
    
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

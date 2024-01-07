import numpy as np
import os
from typing import Union, List, Tuple


class Directory:
    pass
class Version:
    pass
class Path:
    pass
class FileSystem:
    def changed(self):
        pass
class TextStyle:
    BOLD = '\033[1m'

class TextStyle:
    RESET = '\033[0m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    DARK_GRAY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_GRAY = '\033[97m'

    BOLD_BLACK = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_MAGENTA = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    BOLD_WHITE = '\033[1;37m'
    
    BOLD_DARK_GRAY = '\033[1;90m'
    BOLD_LIGHT_RED = '\033[1;91m'
    BOLD_LIGHT_GREEN = '\033[1;92m'
    BOLD_LIGHT_YELLOW = '\033[1;93m'
    BOLD_LIGHT_BLUE = '\033[1;94m'
    BOLD_LIGHT_MAGENTA = '\033[1;95m'
    BOLD_LIGHT_CYAN = '\033[1;96m'
    BOLD_LIGHT_GRAY = '\033[1;97m'
    
    def highlight(text : str, style : str = TextStyle.BOLD):
        return f"\"{TextStyle.style(text, style)}\""
    
    def style(text : str, style : str) -> str:
        if type(style) == str:
            return style + text + TextStyle.RESET
        elif type(style) == List[str]:
            for st in style:
                text = st + text
            return text + TextStyle.RESET
        else:
            FileSystem.error(f"Invalid style type {TextStyle.highlight(type(style))}. Must be of type {type(style)}, or {type(style)}")
            return text

class Vector2:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        
    def str(self) -> str:
        return f"(x: {self.x}, y: {self.y})"

class WhatsNew:
    def __init__(self, old_version : Version, current_version : Version, add : str, remove : str, change : str, fixes : str, note : str):
        self.add : str = add
        self.remove : str = remove
        self.change : str = change
        self.fixes : str = fixes
        self.note : str = note
        self.old_version : Version = old_version
        self.current_version : Version = current_version
        
    def str(self, addition_text : bool = False) -> str:
        out : str = ""
        addition_tab : str = "\t" if addition_text else "" 
        if self.add:
            out += f"{addition_tab}{TextStyle.style('Added', TextStyle.GREEN)}: {self.add}\n"
        if self.remove:
            out += f"{addition_tab}{TextStyle.style('Removed', TextStyle.RED)}: {self.remove}\n"
        if self.change:
            out += f"{addition_tab}{TextStyle.style('Changed', TextStyle.YELLOW)}: {self.change}\n"
        if self.fixes:
            out += f"{addition_tab}{TextStyle.style('Fixed', TextStyle.CYAN)}: {self.fixes}\n"
        if self.note:
            out += f"{addition_tab}{TextStyle.style('Note', TextStyle.DARK_GRAY)}: {self.note}\n"
        
        if out == "":
            out = "There is no information!"
        
        return out

class Version:
    def __init__(self, major : int = 0, minor : int = 0, patch : int = 0, information_text : str = ""):
        self.major : int = int(major)
        self.minor : int = int(minor)
        self.patch : int = int(patch)
        self.history : np.array = np.array([], dtype=object)
        self.information_text : str = information_text
        
    def str(self, addition_text : bool = False) -> str:
        add_txt = (TextStyle.style(self.information_text, TextStyle.BOLD_MAGENTA) + " Version: ") if addition_text else ""
        
        return f"{add_txt}{self.major}.{self.minor}.{self.patch}"
    
    @staticmethod
    def load(string : str) -> Version:
        tmp = str.split(string, ".")
        return Version(tmp[0], tmp[1], tmp[2])
    
    def whats_new(self, addition_text : bool = False) -> str:
        add_txt = TextStyle.style("What's new", TextStyle.BOLD_BLUE) + f" ( {TextStyle.style(self.history[-1].old_version.str(), TextStyle.DARK_GRAY)} -> {TextStyle.style(self.history[-1].current_version.str(), TextStyle.CYAN)} ):\n" if addition_text else ""
        return add_txt + self.history[-1].str(addition_text) 
    
class Iterator:
    def __init__(self, value : int):
        self.value : int = value
        
class StringHolder:
    def __init__(self, string : str):
        self.string : str = string

class Path:
    forbidden_symbol = "/"
    def __init__(self, path : Union[str, Path, List[str]] = ""):
        self.directories : list = []
        self.add_path(path)
        
    def is_empty(self) -> bool:
        return len(self.directories) == 0
        
    def add_path(self, path : Union[Path, str, list]):
        if type(path) == Path:
            self.add_path(path.directories)
        elif type(path) == str:
            self.add_path(str.split(path, "/"))
        elif type(path) == list:
            for dir in path:
                if dir != "":
                    if Path.forbidden_symbol in dir:
                        FileSystem.error(f"Path {TextStyle.highlight(dir)} contain forbidden character {TextStyle.highlight(Path.forbidden_symbol)}!")
                        raise RuntimeError(f"Path \"{dir}\" contain forbidden character \"{Path.forbidden_symbol}\"")
                    self.directories.append(dir)
        else:
            raise TypeError(f"Invalid path type - {type(path)}!")
    
    def back(self, times : int = 1):
        if times < 0:
            raise ValueError("Cant go back negative amount of times!")
        elif times > 0:
            self.directories = self.directories[:-times]        
    
    def str(self) -> str:
        return "/".join(self.directories)
    
    def __str__(self) -> str:
        return self.str()
    
    def get_os_path(self) -> os.path:
        return os.path.join(*self.directories)
    
    

VERSION : Version = Version(1, 2, 0, "NeonFileSystem")
VERSION.history = np.array([
    WhatsNew(
        Version(1, 0, 1),
        Version(1, 1, 0),
        add="documentation, message/warning/error display system, FileSystem logs saving, \"What's new?\" logic in Version class, functions to create and delete files/directories, directory back connection, path logic, current directory logic to FileSystem",
        remove="",
        change="now function send message/warning/error with FileSystem methods instead of just printing it with print, file and directory find logic",
        fixes="",
        note = ""
    ),
    WhatsNew(
        Version(1, 1, 0),
        Version(1, 1, 1),
        add="\"fixes\" subparagraph to \"What's new?\" class and output",
        remove="",
        change="",
        fixes="typo in previos version \"What's new?\", doesnt display message that indicate that messages has been enabled",
        note = ""
    ),
    WhatsNew(
        Version(1, 1, 1),
        Version(1, 2, 0),
        add="add valid propertie to FileSystem and Path classes, silent option for messages/warnings/errors, global filesystem propertie to FileSystem, control from console",
        remove="dot from list of forbidden path symbols",
        change="now empty message/warning/error would not be displayed, increase code safety",
        fixes="small tune to prevent spam of messages, a lot of bugs/typos/mistakes",
        note = "change somethig only in subitems of current global directory, or it will mistakenly indicate as changed(not important, but must be warned)"
    ),
    WhatsNew(
        Version(1, 2, 0),
        Version(1, 3, 0),
        add="terminal color support and TextStyle class, now messages/warnings/errors have own colors, now show() function of Directory class give colorfull output, is_empty() function in Path class",
        remove="is_valid logic from Path class",
        change="increase code safety, now Path class support all symbols but \"/\"",
        fixes="bug and mistakes fixes",
        note =""
    ),
    WhatsNew(
        Version(1, 3, 0),
        Version(1, 3, 1),
        add="function in FileSystem to create default filesystem",
        remove="get_type_by_name() function from Coder class, because it is not needed",
        change="small code cleaning, documentation big update",
        fixes="",
        note =""
    )
])
print(VERSION.str(True))
print(VERSION.whats_new(True))

COMMAND_SYMBOL : str = "."
BEGIN_OF_FILE : str = "{"
END_OF_FILE : str = "}"
BEGIN_OF_DIRECTORY : str = "<"
END_OF_DIRECTORY : str = ">"

DEFAULT_SYSTEM_FILE_NAME : str = "default"
DEFAULT_SYSTEM_FILE_EXTENSION : str = "nefis"

class Coder:
    @staticmethod
    def encode(input_string: str) -> str:
        if not isinstance(input_string, str):
            raise ValueError("Input must be a string")
        encoded_bytes = input_string.encode('utf-8')
        # Convert bytes to a string of '0's and '1's
        binary_string = ''.join(format(byte, '08b') for byte in encoded_bytes)
        return binary_string

    @staticmethod
    def decode(binary_string: str) -> str:
        if not all(bit in ('0', '1') for bit in binary_string):
            raise ValueError("Input must be a binary string")
        # Convert the binary string to bytes and then decode
        decoded_string = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)).decode('utf-8')
        return decoded_string


class File:
    # Data holds in objects as normal string
    # Data type holds in objects as "type" variable
    
    i_separator : str = "#"
    
    def __init__(self, name : str, data_type : str, data : str, parent_directory : Directory = None):
        self.name : str = name
        self.data_type : str = data_type
        self.data : str = data
        self.parent_directory : Directory = parent_directory
        
    def get_raw(self):
        #       Raw structure(# - separator):
        #       name # data_type # data
        return Coder.encode(self.name) + File.i_separator + Coder.encode(str(self.data_type)) + File.i_separator + Coder.encode(self.data)
    
    def get_path(self, include_itself : bool = True, show_type : bool = True) -> Path:
        path = self.parent_directory.get_path()
        if include_itself:
            path.add_path(self.get_full_name() if show_type else self.name)
        return path
    
    def get_full_name(self) -> str:
        return self.name + "." + self.data_type
    
    def get_data(self) -> str:
        return self.data
            
    def set_data(self, new_data : str):
        self.data = new_data
        if type(self.parent_directory) == Directory:
            FileSystem.global_filesystem.changed()
        
    def set_name(self, new_name : str):
        if new_name == "":
            FileSystem.error(f"Cant change {TextStyle.highlight(self.name)} file name to an empty string!")
        if Path.forbidden_symbol in new_name:
            FileSystem.error(f"Cant change {TextStyle.highlight(self.name)} file name to {TextStyle.highlight(new_name)} because it contain {TextStyle.highlight(Path.forbidden_symbol)}!")
            raise RuntimeError(f"Cant change {self.name} file name to {new_name} because it contain {Path.forbidden_symbol}!")
        if new_name == self.name:
            FileSystem.message(f"It is already its file name")
            return
        elif type(self.parent_directory) == Directory:
            if type(self.parent_directory.get_subdirectory(new_name)) == Directory:
                FileSystem.error(f"Cant rename directory because directory with the same name already exist!")
        old_name = self.name
        self.name = new_name
        FileSystem.message(f"Name of {TextStyle.highlight(old_name)} file has been successfully changed to {TextStyle.highlight(self.name)}!") 
        if type(self.parent_directory) == Directory:
            FileSystem.global_filesystem.changed()
    
    def load(self, data : str):
        tmp = data.split(File.i_separator, 2)
        self.name = Coder.decode(tmp[0])
        self.data_type = Coder.decode(tmp[1])
        self.data = Coder.decode(tmp[2])
        

class Directory:
    i_separator : str = "%"
    
    _directory_level : int = 0
    
    def __init__(self, name : str, parent_directory : Directory = None):
        self.name : str = name
        self.content : np.ndarray = np.array([], dtype=object)
        self._directory_level : int = 0
        self.parent_directory : Directory = parent_directory
        
    def get_path(self, include_itself : bool = True) -> Path:
        path : Path = Path()
        if self.get_directory_level() > 0:
            path.add_path(self.parent_directory.get_path())
        if include_itself or self.get_directory_level() == 0:
            path.add_path(self.name)
        return path
        
    def set_name(self, new_name : str):
        if new_name == "":
            FileSystem.error(f"Cant change {TextStyle.highlight(self.name)} directory name to an empty string!")
        if Path.forbidden_symbol in new_name:
            FileSystem.error(f"Cant change {TextStyle.highlight(self.name)} directory name to {TextStyle.highlight(new_name)} because it contain {TextStyle.highlight(Path.forbidden_symbol)}!")
            raise RuntimeError(f"Cant change {self.name} directory name to {new_name} because it contain {Path.forbidden_symbol}!")
        if new_name == self.name:
            FileSystem.message(f"It is already its directory name")
            return
        elif type(self.parent_directory) == Directory:
            if type(self.parent_directory.get_subdirectory(new_name)) == Directory:
                FileSystem.error(f"Cant rename directory because directory with the same name already exist!")
        old_name = self.name
        self.name = new_name
        FileSystem.message(f"Name of {TextStyle.highlight(old_name)} directory has been successfully changed to {TextStyle.highlight(self.name)}!")   
        FileSystem.global_filesystem.changed()
        
    def get_directory_level(self) -> int:
        return self._directory_level
    
    def _set_directory_level(self, new_level : int):
        self._directory_level = new_level
        for item in self.content:
            if type(item) == Directory:
                item._set_directory_level(self.get_directory_level() + 1)
        
    # region content managment
    def add_subdirectory(self, subdirectory : Directory):
        if type(subdirectory) != Directory:
            raise TypeError(f"Given object must be a Directory not {TextStyle.highlight(type(subdirectory))}")
        elif any(item.name == subdirectory.name for item in self.content):
            FileSystem.error(f"Cant add subdirectory, object with name {TextStyle.highlight(subdirectory.name)} already exist!")
        else:
            self.content = np.append(self.content, subdirectory)
            self.content[-1]._set_directory_level(self.get_directory_level() + 1)
            self.content[-1].parent_directory = self
            FileSystem.message(f"Successfully add {TextStyle.highlight(subdirectory.name)} directory!")
            FileSystem.global_filesystem.changed()
            
    def add_file(self, file : File):
        if type(file) != File:
            raise TypeError(f"Given object must be a File not {type(file)}")
        elif any(item.name == file.name for item in self.content):
            FileSystem.error(f"Cant add file, object with name {TextStyle.highlight(file.name)} already exist!")
        else:
            self.content = np.append(self.content, file)
            self.content[-1].parent_directory = self
            FileSystem.message(f"Successfully add {TextStyle.highlight(file.get_full_name())} file!")
            FileSystem.global_filesystem.changed()
        
    def create_subdirectory(self, name : str, content : np.array = []) -> Directory:
        new_dir = Directory(name)
        FileSystem.disable_messages(True)
        for item in content:
            if type(item) == Directory:
                new_dir.add_subdirectory(item)
            elif type(item) == File:
                new_dir.add_file(item)
        FileSystem.enable_messages(True)
        self.add_subdirectory(new_dir)
        return self.content[-1]
    
    def create_file(self, name : str, file_type : str, file_content : str = "") -> File:
        new_file = File(name, file_type, file_content)
        self.add_file(new_file)
        return self.content[-1]
    
    def delete_subdirectory(self, name : str, delete_if_not_empty : bool = False):
        del_ind : int = -1
        for i in range(len(self.content)):
            if type(self.content[i]) == Directory and self.content[i].name == name:
                del_ind = i
                break
            
        if del_ind == -1:
            FileSystem.error(f"Cant delete {TextStyle.highlight(name)}, there is no such directory!")
            return
        if not delete_if_not_empty and len(self.content[del_ind].content) > 0:
            FileSystem.error(f"Cant delete {TextStyle.highlight(name)}, directory is not empty!")
            return
        self.content = np.delete(self.content, del_ind)
        FileSystem.message(f"{TextStyle.highlight(name)} directory has beed successfully deleted!")
        FileSystem.global_filesystem.changed()
        
    def delete_file(self, name : str):
        del_ind : int = -1
        for i in range(len(self.content)):
            if type(self.content[i]) == File and (self.content[i].name == name or self.content[i].get_full_name() == name):
                del_ind = i
                break
            
        if del_ind == -1:
            FileSystem.error(f"Cant delete {TextStyle.highlight(name)}, there is no such file!")
            return 
        self.content = np.delete(self.content, del_ind)
        FileSystem.message(f"{TextStyle.highlight(name)} file has beed successfully deleted!")
        FileSystem.global_filesystem.changed()
        
    def get_subdirectory(self, name : str):
        for item in self.content:
            if item.name == name and type(item) == Directory:
                return item
        FileSystem.warning(f"There is no directory with {TextStyle.highlight(name)} name!")
        return None
       
    def get_file(self, name : str):
        for item in self.content:
            if type(item) == File and (item.name == name or item.get_full_name() == name):
                return item
        FileSystem.warning(f"There is no file with {TextStyle.highlight(name)} name!")
        return None
    
    def get_item(self, name : str):
        for item in self.content:
            if (type(item) == Directory and item.name == name) or (type(item) == File and (item.name == name or item.get_full_name() == name)):
                return item
        FileSystem.warning(f"There is no item with {TextStyle.highlight(name)} name!")
        return None  
    # endregion 
        
    @staticmethod
    def __get_show_str(name : str, level : int, specil_char : str) -> str:
        return TextStyle.style("|\t" * level, TextStyle.DARK_GRAY) + specil_char + name + "\n"
    
    def __get_show_dir_str(self, expand : bool = False, start_level : int = -1) -> str:
        if start_level == -1:
            start_level = self.get_directory_level()
        out = Directory.__get_show_str(TextStyle.style(self.name, TextStyle.BOLD_BLUE), self.get_directory_level() - start_level, "*")
        if expand:
            for item in self.content:
                if type(item) == Directory:
                    out += item.__get_show_dir_str(expand, start_level)
                elif type(item) == File:
                    out += Directory.__get_show_str(TextStyle.style(item.get_full_name(), TextStyle.CYAN), self.get_directory_level() - start_level + 1, " ")
        return out
    
    def show(self, expand_subdirectories : bool = False):
        out = TextStyle.style("@", TextStyle.BLUE) + " "
        if self.get_directory_level() == 0:
            out += TextStyle.style("[" + self.name + "]", TextStyle.BOLD_MAGENTA)
        else: 
            out += TextStyle.style("[" + self.name + "]", TextStyle.BOLD_BLUE)
        out += "\n" + TextStyle.style("|", TextStyle.DARK_GRAY) + "\n"
        for item in self.content:
            if type(item) == Directory:
                out += item.__get_show_dir_str(expand_subdirectories, self.get_directory_level())
            elif type(item) == File:
                out += Directory.__get_show_str(TextStyle.style(item.get_full_name(), TextStyle.CYAN), 1, " ")
        print(out)
        
        
    def get_raw(self) -> str:
        raw = COMMAND_SYMBOL + BEGIN_OF_DIRECTORY + Coder.encode(self.name) + Directory.i_separator
        for item in self.content:
            if type(item) == File:
                raw += COMMAND_SYMBOL + BEGIN_OF_FILE + item.get_raw() + COMMAND_SYMBOL + END_OF_FILE
            if type(item) == Directory:
                raw += item.get_raw()
        raw += COMMAND_SYMBOL + END_OF_DIRECTORY
        return raw
    
    def load_dir(self, data : StringHolder, command_indices : list, current_command : Iterator):
        # Get index of separator symbol
        sep_ind = data.string.find(Directory.i_separator, command_indices[current_command.value] + 2, len(data.string))
        
        # Load directory information
        self.name = Coder.decode(data.string[command_indices[current_command.value] + 2 : sep_ind])
        
        # Load content information
        current_command.value += 1        
        
        while(True):
            if data.string[command_indices[current_command.value] + 1] == BEGIN_OF_DIRECTORY:
                new_dir : Directory = Directory("__tmp__")
                new_dir.load_dir(data, command_indices, current_command)
                self.add_subdirectory(new_dir)
            elif data.string[command_indices[current_command.value] + 1] == BEGIN_OF_FILE:
                new_file : File = File("__tmp__", str, "")
                new_file.load(data.string[command_indices[current_command.value] + 2 : command_indices[current_command.value + 1]])
                self.add_file(new_file)
                current_command.value += 2
            if data.string[command_indices[current_command.value] + 1] == END_OF_DIRECTORY:
                current_command.value += 1
                break
           
class FileSystem:
    fsi_separator : str = "~"
    ROOT_NAME : str = "nroot"
    
    global_filesystem : FileSystem = FileSystem()
    @staticmethod
    def set_global_filesystem(fs : FileSystem):
        FileSystem.global_filesystem = fs
    def set_as_global(self):
        FileSystem.set_global_filesystem(self)
    
    def changed(self):
        '''
        Say to filesystem that it has been changed
        '''
        self.__was_changed = True
    def is_changed(self) -> bool:
        '''
        Return True if filesystem was changed and not saved
        Return False if filesystem was just saved, loaded or created
        '''
        return self.__was_changed
    
    # region output parameters
    any_output : bool = True
    @staticmethod
    def enable_output(silent : bool = False) -> None: 
        FileSystem.any_output = True
        FileSystem.message("Output has been enabled!", silent)
    @staticmethod
    def disable_output(silent : bool = False) -> None: 
        FileSystem.message("Output has been disabled!", silent)
        FileSystem.any_output = False
    show_messages : bool = True
    @staticmethod
    def enable_messages(silent : bool = False) -> None:
        FileSystem.show_messages = True
        FileSystem.message("Messages have been enabled!", silent)
    @staticmethod
    def disable_messages(silent : bool = False) -> None: 
        FileSystem.message("Messages have been disabled!", silent)
        FileSystem.show_messages = False
    show_warnings : bool = True
    @staticmethod
    def enable_warnings(silent : bool = False) -> None: 
        FileSystem.message("Warnings have been enabled!", silent)
        FileSystem.show_warnings = True
    @staticmethod
    def disable_warnings(silent : bool = False) -> None: 
        FileSystem.message("Warnings have been disabled!", silent)
        FileSystem.show_warnings = False
    show_errors : bool = True
    @staticmethod
    def enable_errors(silent : bool = False) -> None: 
        FileSystem.message("Errors have been enabled!", silent)
        FileSystem.show_errors = True
    @staticmethod
    def disable_errors(silent : bool = False) -> None: 
        FileSystem.message("Errors have been disabled!", silent)
        FileSystem.show_errors = False
    save_logs : bool = True
    logs : np.ndarray = np.ndarray([], dtype=str)
    @staticmethod
    def enable_logs(silent : bool = False) -> None: 
        FileSystem.message("Logging has been disabled!", silent)
        FileSystem.save_logs = True
    @staticmethod
    def disable_logs(silent : bool = False) -> None: 
        FileSystem.message("Logging has been disabled!", silent)
        FileSystem.save_logs = False
    # endregion
    
    def __init__(self, name : str = DEFAULT_SYSTEM_FILE_NAME):
        self.filesystem_name : str = name
        self.version : Version = VERSION
        self.nroot : Directory = Directory(FileSystem.ROOT_NAME)
        self.current_directory_path : Path = self.nroot.get_path()
        self.__valid : bool = True
        self.__was_changed = False
        if Path.forbidden_symbol in self.filesystem_name:
            raise RuntimeError(f"FileSystem name {self.filesystem_name} cant contain \"{Path.forbidden_symbol}\"")
        
    @staticmethod
    def default_fs():
        return FileSystem()
        
    def is_valid(self) -> bool:
        return self.__valid
    
    def _set_valid(self):
        self.__valid = True
    
    def _set_invalid(self):
        self.__valid = False
        
    def get_directory(self, path : Path) -> Directory:
        if type(path) == Path:
            
            if path.directories[0] != self.nroot.name:
                FileSystem.error(f"Path {TextStyle.highlight(path.str())} is invalid!")
                return None
            current_dir = self.nroot
            for dir_name in path.directories[1:]:
                current_dir = current_dir.get_subdirectory(dir_name)
                if current_dir == None:
                    FileSystem.error(f"Path {TextStyle.highlight(path.str())} is invalid. There is no {TextStyle.highlight(dir_name)} directory!")
                    return None
            return current_dir
        elif type(path) == str:
            return self.get_directory(Path(path))
        else:
            raise TypeError("Given path must be of type \"str\" or \"Path\"!")
      
    def get_file(self, path : Path) -> File:
        if type(path) == Path:
            
            if path.directories[0] != self.nroot.name:
                FileSystem.error(f"Path {TextStyle.highlight(path.str())} is invalid!")
                return None
            current_dir = self.nroot
            for dir_name in path.directories[1:-1]:
                current_dir = current_dir.get_subdirectory(dir_name)
                if current_dir == None:
                    FileSystem.error(f"Path {TextStyle.highlight(path.str())} is invalid. There is no {TextStyle.highlight(dir_name)} directory!")
                    return None
            file : File = current_dir.get_file(path.directories[-1])
            if file == None:
                    FileSystem.error(f"There is no {TextStyle.highlight(path.directories[-1])} file in {TextStyle.highlight(Path(path.directories[:-1]).str())} directory!")
                    return None
            return file
        elif type(path) == str:
            return self.get_file(Path(path))
        else:
            raise TypeError("Given path must be of type \"str\" or \"Path\"!")
    
    def set_current_directory_path(self, path : Path):
        if type(self.get_directory(path)) != Directory:
            self.error(f"There is no {TextStyle.highlight(path if type(path) == str else path.str())} directory!")
            return
        self.current_directory_path = Path(path)
        
    def get_current_directory(self) -> Directory:
        return self.get_directory(self.current_directory_path)    
    
    def get_root_name(self) -> str:
        return self.nroot.name
        
    def get_raw(self) -> str:
        raw = FileSystem.fsi_separator + Coder.encode(self.version.str()) + FileSystem.fsi_separator + Coder.encode(self.filesystem_name) + FileSystem.fsi_separator 
        raw += self.nroot.get_raw() + FileSystem.fsi_separator
        return raw
        
    def save(self, file_name : str = ""):
        if file_name == "":
            file_name = self.filesystem_name
        if not (("." + DEFAULT_SYSTEM_FILE_EXTENSION) in file_name):
            file_name += "." + DEFAULT_SYSTEM_FILE_EXTENSION
        with open(file_name, 'w') as file:
            file.write(self.get_raw())
        FileSystem.__was_changed = False 
            
    def load(self, path : Path):
        if type(path) == str:
            path = Path(path)
        
        # Load data
        raw_data = ""
        if not (("." + DEFAULT_SYSTEM_FILE_EXTENSION) in path.directories[-1]):
            path.directories[-1] += "." + DEFAULT_SYSTEM_FILE_EXTENSION
        with open(path.str(), 'r') as file:
            raw_data = file.read()
        if raw_data == "":
            FileSystem.error(f"Cant read {TextStyle.highlight(path.str())} file or it is empty!")
            self._set_invalid()
            return
        
        fs_parts = str.split(raw_data, self.fsi_separator)[1:-1]
        
        # Read filesystem information
        self.version : Version = Version.load(Coder.decode(fs_parts[0]))
        if type(self.version) != Version:
            self._set_invalid()
            return 
        if self.version.major != VERSION.major:
            FileSystem.warning(f"Loaded filesystem have different major version, {TextStyle.highlight('high incompability chance', TextStyle.BOLD_YELLOW)}!\nCurrent version: {TextStyle.highlight(VERSION.str())}\nLoaded version: {TextStyle.highlight(self.version.str())}")
        elif self.version.minor != VERSION.minor:
            FileSystem.message(f"Loaded filesystem have different minor version, {TextStyle.highlight('low incompability chance', TextStyle.BOLD_GREEN)}!\nCurrent version: {TextStyle.highlight(VERSION.str())}\nLoaded version: {TextStyle.highlight(self.version.str())}")
        
        self.filesystem_name = Coder.decode(fs_parts[1])
        
        # Disable messages
        FileSystem.disable_messages(True)
        # Read filesystem content
        command_indices = [index for index, char in enumerate(fs_parts[2]) if char == COMMAND_SYMBOL]
        current_command : Iterator = Iterator(0)
        data : StringHolder = StringHolder(fs_parts[2])
        self.nroot.load_dir(data, command_indices, current_command)
        # Enable messages
        FileSystem.enable_messages(True)
        
        FileSystem.__was_changed = False
        if Path.forbidden_symbol in self.filesystem_name:
            raise RuntimeError(f"FileSystem name {self.filesystem_name} cant contain \"{Path.forbidden_symbol}\"")
    @staticmethod
    def add_tabs_to_message(text : str) -> str:
        out : str = ""
        tmp = str.split(text, "\n")
        out += tmp[0]
        for i in tmp[1:]:
            out += f"\n\t{i}"
        return out            
        
    @staticmethod
    def message(message : str, silent : bool = False):
        # Here code choose how to send you a message
        if message == "":
            return
        text : str = f"{TextStyle.style('MESSAGE', TextStyle.BOLD_GREEN)}: {FileSystem.add_tabs_to_message(message)}"
        if FileSystem.any_output and FileSystem.show_messages and not silent:
            print(text)
        if FileSystem.save_logs:
            FileSystem.logs = np.append(FileSystem.logs, text)
       
    @staticmethod 
    def warning(warning : str, silent : bool = False):
        # Here code choose how to send you a warning
        if warning == "":
            return
        text : str = f"{TextStyle.style('WARNING', TextStyle.BOLD_YELLOW)}: {FileSystem.add_tabs_to_message(warning)}"
        if FileSystem.any_output and FileSystem.show_warnings:
            print(text)
        if FileSystem.save_logs:
            FileSystem.logs = np.append(FileSystem.logs, text)
        
    @staticmethod
    def error(error: str, silent : bool = False):
        # Here code choose how to send you an error
        if error == "":
            return
        text : str = f"{TextStyle.style('ERROR', TextStyle.BOLD_RED)}: {FileSystem.add_tabs_to_message(error)}"
        if FileSystem.any_output and FileSystem.show_errors:
            print(text)
        if FileSystem.save_logs:
            FileSystem.logs = np.append(FileSystem.logs, text)
        
def create_default_filesystem():
    fs = FileSystem()
    nroot = fs.nroot
    
    user = Directory("user")

    desktop = Directory("desktop")
    desktop.create_file("google-chrome", "bin", "Here is Google Chrome binary file) It is empty ;-)")
    desktop.create_file("python", "cpp", "int main() { std::cout << \"Hello world!\" << std::endl }")
    
    trash = Directory("trash")
    trash.create_file("windows", "iso", "print(\"Hello World!\")")
    trash.create_file("mac-os", "iso", "print(\"Life is suck!\")")
    trash.create_file("edge", "bin", "Trash here!")
    trash.create_file("xdfw-hfgd-wkas-pkfm", "tmp", "ddfghshauyuvdSBcgnai52678yfjcia anoA F UJHAV2Y8272YJDA;.AsA.C,ABASMNFACUYBW  UDHsdasda")
    trash.create_file("virus", "exe")
    
    desktop.add_subdirectory(trash)

    pictures = Directory("pictures")
    pictures.create_file("first-artwork", "trash", "¯\_(*-*)_/¯")
    pictures.create_file("linux-icon", "png", "Linux is sexy!")
    
    documents = Directory("documents")
    documents.create_file("calculator", "py", "print(f\"2 + 2 = {2 + 2}\")")
    documents.create_file("statistics", "xml", "1|2|3|4|5|6|7|8|9|10|11|12|My work is suck!|14|15|16|17|18|19|20")
    
    desktop.add_subdirectory(documents)
    
    user.add_subdirectory(desktop)
    
    applications = Directory("application")
    applications.create_file("wine", "bin", "Wine is gold! <3")
    applications.create_file("vs-code", "bin", "Write code here!")
    applications.create_file("SuperTuxKart", "bin", "Best game of all times!!!")

    user.add_subdirectory(applications)
    
    nroot.add_subdirectory(user)

    bin_dir = Directory("bin")
    
    bin_dir.create_subdirectory("snap")
    bin_dir.create_file("wine", "bin", "begin of code ...magic... end of code")
    bin_dir.create_file("terminal", "bin", "nroot > ")
    bin_dir.create_file("filemanager", "bin", "Files goes brrrr...")
    
    nroot.add_subdirectory(bin_dir)
    
    tmp = Directory("tmp")
    
    google = Directory("google")
    google.create_file("x7j1", "bin", "joasdad721kjansjdq2e7a")
    google.create_file("s3pq", "bin", "olanuc1239ij7yhb5rd4e2")
    google.create_file("cookies", "bin", "All possible information about you and your family")
    
    tmp.add_subdirectory(google)
    
    tmp.create_file("5zYb-jCda-3A4Q", "tmp", "drio-JYjS-liDB")
    tmp.create_file("H2dR-e1ia-TViX", "tmp", "IZzr-VE6a-yxUP")
    tmp.create_file("9FXh-jNvY-XtGx", "tmp", "tkHa-O212-4x62")
    tmp.create_file("6Z3A-bBw6-XfV6", "tmp", "WQ55-540A-xoiu")
    tmp.create_file("U1lB-Ksse-RhmW", "tmp", "u7EV-ce4u-1M5i")
    tmp.create_file("4f5u-sawX-OkrS", "tmp", "N3ah-fV1e-999F")
    
    nroot.add_subdirectory(tmp)
    
    nroot.create_subdirectory("mnt")

    fs.save()

# create_default_filesystem()
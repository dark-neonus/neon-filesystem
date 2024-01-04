import numpy as np
import os

class Directory:
    pass
class Version:
    pass
class Path:
    pass
class FileSystem:
    def changed(self):
        pass

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
            out += f"{addition_tab}Added: {self.add}\n"
        if self.remove:
            out += f"{addition_tab}Removed: {self.remove}\n"
        if self.change:
            out += f"{addition_tab}Changed: {self.change}\n"
        if self.fixes:
            out += f"{addition_tab}Fixed: {self.fixes}\n"
        if self.note:
            out += f"{addition_tab}Note: {self.note}\n"
        
        if out == "":
            out = "There is no information!"
        
        return out

class Version:
    def __init__(self, major : int = 0, minor : int = 0, patch : int = 0, information_text : str = ""):
        self.major : int = int(major)
        self.minor : int = int(minor)
        self.patch : int = int(patch)
        self.logs : np.array = np.array([], dtype=object)
        self.information_text : str = information_text
        
    def str(self, addition_text : bool = False) -> str:
        add_txt = (self.information_text + " Version: ") if addition_text else ""
        
        return f"{add_txt}{self.major}.{self.minor}.{self.patch}"
    
    @staticmethod
    def load(string : str) -> Version:
        tmp = str.split(string, ".")
        return Version(tmp[0], tmp[1], tmp[2])
    
    def whats_new(self, addition_text : bool = False) -> str:
        add_txt = f"What's new ( {self.logs[-1].old_version.str()} -> {self.logs[-1].current_version.str()} ):\n" if addition_text else ""
        return add_txt + self.logs[-1].str(addition_text) 
    
class Iterator:
    def __init__(self, value : int):
        self.value = value
        
class StringHolder:
    def __init__(self, string : str):
        self.string = string

class Path:
    forbidden_symbols = ["/", "\\", "\"", "\'", ":", ",", ";", "`"]
    def __init__(self, path = ""):
        self.directories = []
        self.__valid = True
        self.add_path(path)        
        
    def is_valid(self) -> bool:
        return self.__valid
    
    def __set_valid(self):
        self.__valid = True
    def __set_invalid(self):
        self.__valid = False
        
    def add_path(self, path : Path):
        if type(path) == Path:
            if not path.is_valid():
                self.__set_invalid()
            for dir in path.directories:
                self.directories.append(dir)
        elif type(path) == str:
            new_dirs = str.split(path, "/")
            for dir in new_dirs:
                if dir != "":
                    for ch in Path.forbidden_symbols:
                        if ch in dir:
                            FileSystem.warning(f"Path \"{new_dirs}\" contain forbidden character \"{ch}\". Path will be created, but can cause errors!")
                            self.__set_invalid()
                    self.directories.append(dir)
        else:
            raise TypeError("Invalid path type!")
    
    def back(self, times : int = 1):
        if times < 0:
            raise ValueError("Cant go back negative amount of times!")
        elif times > 0:
            self.directories = self.directories[:-times]
            
    def str(self) -> str:
        return "/".join(self.directories)
    
    def get_os_path(self) -> os.path:
        return os.path.join(*self.directories)

VERSION : Version = Version(1, 2, 0, "NeonFileSystem")
VERSION.logs = np.array([
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

    @staticmethod
    def get_type_by_name(name : str) -> type:
        return eval(name)


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
            FileSystem.error(f"Cant change \"{self.name}\" file name to an empty string!")
        for ch in Path.forbidden_symbols:
            if ch in new_name:
                FileSystem.error(f"Cant change \"{self.name}\" file name to \"{new_name}\" because it contain forbidden symbol \"{ch}\"!")
        if new_name == self.name:
            FileSystem.message(f"It is already its file name")
            return
        elif type(self.parent_directory) == Directory:
            if type(self.parent_directory.get_subdirectory(new_name)) == Directory:
                FileSystem.error(f"Cant rename directory because directory with the same name already exist!")
        old_name = self.name
        self.name = new_name
        FileSystem.message(f"Name of \"{old_name}\" file has been successfully changed to \"{self.name}\"!") 
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
            FileSystem.error(f"Cant change \"{self.name}\" directory name to an empty string!")
        for ch in Path.forbidden_symbols:
            if ch in new_name:
                FileSystem.error(f"Cant change \"{self.name}\" directory name to \"{new_name}\" because it contain forbidden symbol \"{ch}\"!")
        if new_name == self.name:
            FileSystem.message(f"It is already its directory name")
            return
        elif type(self.parent_directory) == Directory:
            if type(self.parent_directory.get_subdirectory(new_name)) == Directory:
                FileSystem.error(f"Cant rename directory because directory with the same name already exist!")
        old_name = self.name
        self.name = new_name
        FileSystem.message(f"Name of \"{old_name}\" directory has been successfully changed to \"{self.name}\"!")   
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
            raise TypeError(f"Given object must be a Directory not {type(subdirectory)}")
        elif any(item.name == subdirectory.name for item in self.content):
            FileSystem.error(f"Cant add subdirectory, object with name \"{subdirectory.name}\" already exist!")
        else:
            self.content = np.append(self.content, subdirectory)
            self.content[-1]._set_directory_level(self.get_directory_level() + 1)
            self.content[-1].parent_directory = self
            FileSystem.message(f"Successfully add \"{subdirectory.name}\" directory!")
            FileSystem.global_filesystem.changed()
            
    def add_file(self, file : File):
        if type(file) != File:
            raise TypeError(f"Given object must be a File not {type(file)}")
        elif any(item.name == file.name for item in self.content):
            FileSystem.error(f"Cant add file, object with name \"{file.name}\" already exist!")
        else:
            self.content = np.append(self.content, file)
            self.content[-1].parent_directory = self
            FileSystem.message(f"Successfully add \"{file.name}\" file!")
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
            FileSystem.error(f"Cant delete \"{name}\", there is no such directory!")
            return
        if not delete_if_not_empty and len(self.content[del_ind].content) > 0:
            FileSystem.error(f"Cant delete \"{name}\", directory is not empty!")
            return
        self.content = np.delete(self.content, del_ind)
        FileSystem.message(f"\"{name}\" directory has beed successfully deleted!")
        FileSystem.global_filesystem.changed()
        
    def delete_file(self, name : str):
        del_ind : int = -1
        for i in range(len(self.content)):
            if type(self.content[i]) == File and (self.content[i].name == name or self.content[i].get_full_name()):
                del_ind = i
                break
            
        if del_ind == -1:
            FileSystem.error(f"Cant delete \"{name}\", there is no such file!")
            return 
        self.content = np.delete(self.content, del_ind)
        FileSystem.message(f"\"{name}\" file has beed successfully deleted!")
        FileSystem.global_filesystem.changed()
        
    def get_subdirectory(self, name : str):
        for item in self.content:
            if item.name == name and type(item) == Directory:
                return item
        FileSystem.warning(f"There is no directory with \"{name}\" name!")
        return None
       
    def get_file(self, name : str):
        for item in self.content:
            if type(item) == File and (item.name == name or item.get_full_name() == name):
                return item
        FileSystem.warning(f"There is no file with \"{name}\" name!")
        return None
    
    def get_item(self, name : str):
        for item in self.content:
            if (type(item) == Directory and item.name == name) or (type(item) == File and (item.name == name or item.get_full_name() == name)):
                return item
        FileSystem.warning(f"There is no item with \"{name}\" name!")
        return None  
    # endregion 
        
    @staticmethod
    def __get_show_str(name : str, level : int, specil_char : str) -> str:
        return "|\t" * level + specil_char + name + "\n"
    
    def __get_show_dir_str(self, expand : bool = False, start_level : int = -1) -> str:
        if start_level == -1:
            start_level = self.get_directory_level()
        out = Directory.__get_show_str(self.name, self.get_directory_level() - start_level, "*")
        if expand:
            for item in self.content:
                if type(item) == Directory:
                    out += item.__get_show_dir_str(expand, start_level)
                elif type(item) == File:
                    out += Directory.__get_show_str(item.get_full_name(), self.get_directory_level() - start_level + 1, " ")
        return out
    
    def show(self, expand_subdirectories : bool = False):
        out = f"@ [{self.name}]\n|\n"
        for item in self.content:
            if type(item) == Directory:
                out += item.__get_show_dir_str(expand_subdirectories, self.get_directory_level())
            elif type(item) == File:
                out += Directory.__get_show_str(item.get_full_name(), 1, " ")
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
    
    def __init__(self, name : str = DEFAULT_SYSTEM_FILE_NAME, root_name : str = "nroot"):
        self.filesystem_name : str = name
        self.version : Version = VERSION
        self.nroot : Directory = Directory(root_name)
        self.current_directory : Path = self.nroot.get_path()
        self.__valid : bool = True
        self.__was_changed = False
        
    def is_valid(self) -> bool:
        return self.__valid
    
    def _set_valid(self):
        self.__valid = True
    
    def _set_invalid(self):
        self.__valid = False
        
    def get_directory(self, path : Path) -> Directory:
        if type(path) == Path:
            
            if path.directories[0] != self.nroot.name:
                FileSystem.error(f"Path \"{path.str()}\" is invalid!")
                return None
            current_dir = self.nroot
            for dir_name in path.directories[1:]:
                current_dir = current_dir.get_subdirectory(dir_name)
                if current_dir == None:
                    FileSystem.error(f"Path \"{path.str()}\" is invalid. There is no \"{dir_name}\" directory!")
                    return None
            return current_dir
        elif type(path) == str:
            return self.get_directory(Path(path))
        else:
            raise TypeError("Given path must be of type \"str\" or \"Path\"!")
      
    def get_file(self, path : Path) -> File:
        if type(path) == Path:
            
            if path.directories[0] != self.nroot.name:
                FileSystem.error(f"Path \"{path.str()}\" is invalid!")
                return None
            current_dir = self.nroot
            for dir_name in path.directories[1:-1]:
                current_dir = current_dir.get_subdirectory(dir_name)
                if current_dir == None:
                    FileSystem.error(f"Path \"{path.str()}\" is invalid. There is no \"{dir_name}\" directory!")
                    return None
            file : File = current_dir.get_file(path.directories[-1])
            if file == None:
                    FileSystem.error(f"There is no \"{path.directories[-1]}\" file in \"{Path(path.directories[:-1]).str()}\" directory!")
                    return None
            return file
        elif type(path) == str:
            return self.get_file(Path(path))
        else:
            raise TypeError("Given path must be of type \"str\" or \"Path\"!")
    
    def set_current_directory_path(self, path : Path):
        target_dir = self.get_directory(path)
        if target_dir == None:
            self.error(f"There is no \"{path if type(path) == str else path.str()}\" directory!")
            return
        self.current_directory = target_dir.get_path()
        
    def get_current_directory(self) -> Directory:
        return self.get_directory(self.current_directory)    
    
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
            FileSystem.error("Cant read \"{file_name}\" file or it is empty!")
            self._set_invalid()
            return
        
        fs_parts = str.split(raw_data, self.fsi_separator)[1:-1]
        
        # Read filesystem information
        self.version : Version = Version.load(Coder.decode(fs_parts[0]))
        if type(self.version) != Version:
            self._set_invalid()
            return 
        if self.version.major != VERSION.major:
            FileSystem.warning(f"Loaded filesystem have different major version, high incompability chance!\nCurrent version: {VERSION.str()}\nLoaded version: {self.version.str()}")
        elif self.version.minor != VERSION.minor:
            FileSystem.message(f"Loaded filesystem have different minor version, low incompability chance!\nCurrent version: {VERSION.str()}\nLoaded version: {self.version.str()}")
        
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
        text : str = f"MESSAGE: {FileSystem.add_tabs_to_message(message)}"
        if FileSystem.any_output and FileSystem.show_messages and not silent:
            print(text)
        if FileSystem.save_logs:
            FileSystem.logs = np.append(FileSystem.logs, text)
       
    @staticmethod 
    def warning(warning : str, silent : bool = False):
        # Here code choose how to send you a warning
        if warning == "":
            return
        text : str = f"WARNING: {FileSystem.add_tabs_to_message(warning)}"
        if FileSystem.any_output and FileSystem.show_warnings:
            print(text)
        if FileSystem.save_logs:
            FileSystem.logs = np.append(FileSystem.logs, text)
        
    @staticmethod
    def error(error: str, silent : bool = False):
        # Here code choose how to send you an error
        if error == "":
            return
        text : str = f"ERROR: {FileSystem.add_tabs_to_message(error)}"
        if FileSystem.any_output and FileSystem.show_errors:
            print(text)
        if FileSystem.save_logs:
            FileSystem.logs = np.append(FileSystem.logs, text)
        
       
# fs = FileSystem()
# nroot = fs.nroot
# 
# desktop = Directory("desktop")
# homework = Directory("lessons")
# for i in range(10):
#     homework.add_file(File(f"lesson{i}", "str", "Here is lesson material!"))
# desktop.add_subdirectory(homework)
# nroot.add_subdirectory(desktop)
# 
# pictures = Directory("images")
# nroot.add_subdirectory(pictures)
# 
# documents = Directory("documents")
# nroot.add_subdirectory(documents)
# 
# maps = Directory("maps")
# save_locations = Directory("saved-locations")
# statistics = Directory("statistics")
# maps.add_subdirectory(save_locations) 
# maps.add_subdirectory(statistics)
# save_locations.add_file(File("home", "Vector2", Vector2(0, 0).str())) 
# save_locations.add_file(File("lpml", "Vector2", Vector2(13, 666).str())) 
# statistics.add_file(File("steps", "int", str(12765)))
# statistics.add_file(File("active-time", "float", str(76.3)))
# nroot.add_subdirectory(maps)
# 
# fs.save()
'''

fs.load(fs.filesystem_name)

fs.nroot.show(True)
print(fs.current_directory.str())
fs.set_current_directory_path("nroot/desktop/games/doom")
print(fs.current_directory.str())
fs.set_current_directory_path("nroot/maps/saved-locations")
print(fs.current_directory.str())
fs.get_current_directory().show()

'''
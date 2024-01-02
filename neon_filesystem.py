import numpy as np

class Directory:
    pass

class Vector2:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
        
    def str(self) -> str:
        return f"(x: {self.x}, y: {self.y})"

class Version:
    def __init__(self, major : int = 0, minor : int = 0, patch : int = 0):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)
        
    def str(self, addition_text : bool = False) -> str:
        add_txt = "NeonFileSystem Version: " if addition_text else ""
        
        return f"{add_txt}{self.major}.{self.minor}.{self.patch}"
    
    @staticmethod
    def load(string : str):
        tmp = str.split(string, ".")
        return Version(tmp[0], tmp[1], tmp[2]) 
    
class Iterator:
    def __init__(self, value : int):
        self.value = value
        
class StringHolder:
    def __init__(self, string : str):
        self.string = string
        
VERSION : Version = Version(1, 0, 1)
print(VERSION.str(True))

COMMAND_SYMBOL : str = "."

BEGIN_OF_FILE : str = "{"
END_OF_FILE : str = "}"
BEGIN_OF_DIRECTORY : str = "<"
END_OF_DIRECTORY : str = ">"

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
    
    def __init__(self, name : str, data_type : str, data : str):
        self.name : str = name
        self.data_type : str = data_type
        self.data : str = data
        
    def get_raw(self):
        #       Raw structure(# - separator):
        #       name # data_type # data
        return Coder.encode(self.name) + File.i_separator + Coder.encode(str(self.data_type)) + File.i_separator + Coder.encode(self.data)
    
    
    def get_full_name(self) -> str:
        return self.name + "." + self.data_type
    
    def get_data(self) -> str:
        return self.data
            
    def set_data(self, new_data : str):
        self.data = new_data
        
    def set_name(self, new_name : str):
        self.name = new_name
    
    def load(self, data : str):
        tmp = data.split(File.i_separator, 2)
        self.name = Coder.decode(tmp[0])
        self.data_type = Coder.decode(tmp[1])
        self.data = Coder.decode(tmp[2])
        

class Directory:
    i_separator : str = "%"
    
    _directory_level : int = 0
    
    def __init__(self, name : str):
        self.name : str = name
        self.content : np.ndarray = np.array([], dtype=object)
        self._directory_level = 0
        
    def get_directory_level(self) -> int:
        return self._directory_level
    
    def _set_directory_level(self, new_level : int):
        self._directory_level = new_level
        for item in self.content:
            if type(item) == Directory:
                item._set_directory_level(self.get_directory_level() + 1)
        
    def add_subdirectory(self, subdirectory) -> str:
        if type(subdirectory) != Directory:
            raise TypeError(f"Given object must be a Directory not {type(subdirectory)}")
        elif any(item.name == subdirectory.name for item in self.content):
            return f"Object with name \"{subdirectory.name}\" already exist!"
        else:
            self.content = np.append(self.content, subdirectory)
            self.content[-1]._set_directory_level(self.get_directory_level() + 1)
            return f"Successfully add \"{subdirectory.name}\" directory!"
            
    def add_file(self, file : File) -> str:
        if type(file) != File:
            raise TypeError(f"Given object must be a File not {type(file)}")
        elif any(item.name == file.name for item in self.content):
            return f"Object with name \"{file.name}\" already exist!"
        else:
            self.content = np.append(self.content, file)
            return f"Successfully add \"{file.name}\" file!"
        
    def get_directory(self, name : str):
        for item in self.content:
            if item.name == name and type(item) == Directory:
                return item
        print(f"WARNING: There is no directory with \"{name}\" name!")
        return None
       
    def get_file(self, name : str):
        for item in self.content:
            if item.name == name and type(item) == File:
                return item
        print(f"WARNING: There is no file with \"{name}\" name!")
        return None
    
    def get_item(self, name : str):
        for item in self.content:
            if item.name == name:
                return item
        print(f"WARNING: There is no item with \"{name}\" name!")
        return None  
        
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
    fsi_separator = "~"
    type_name = "nefis"
    def __init__(self, name : str = "neon-filesystem", root_name : str = "nroot"):
        self.filesystem_name : str = name
        self.version : Version = VERSION
        self.nroot : Directory = Directory(root_name)
        
    def get_root_name(self) -> str:
        return self.nroot.name
        
    def get_raw(self) -> str:
        raw = FileSystem.fsi_separator + Coder.encode(self.version.str()) + FileSystem.fsi_separator + Coder.encode(self.filesystem_name) + FileSystem.fsi_separator 
        raw += self.nroot.get_raw() + FileSystem.fsi_separator
        return raw
        
    def save(self, file_name : str = ""):
        if file_name == "":
            file_name = self.filesystem_name
        if not (("." + FileSystem.type_name) in file_name):
            file_name += "." + FileSystem.type_name
        with open(file_name, 'w') as file:
            file.write(self.get_raw())
            
    def load(self, file_name : str) -> str:
        # Load data
        raw_data = ""
        if not (("." + FileSystem.type_name) in file_name):
            file_name += "." + FileSystem.type_name
        with open(file_name, 'r') as file:
            raw_data = file.read()
        if raw_data == "":
            return f"Cant read {file_name}.nefis file or it is empty!"
        
        fs_parts = str.split(raw_data, self.fsi_separator)[1:-1]
        
        # Read filesystem information
        self.version : Version = Version.load(Coder.decode(fs_parts[0]))
        if self.version.major != VERSION.major:
            print(f"WARNING: loaded filesystem have different major version, high incompability chance!\nCurrent version: {VERSION.str()}\nLoaded version: {self.version.str()}")
        elif self.version.minor != VERSION.minor:
            print(f"MESSAGE: loaded filesystem have different minor version, low incompability chance!\nCurrent version: {VERSION.str()}\nLoaded version: {self.version.str()}")
        
        self.filesystem_name = Coder.decode(fs_parts[1])
        
        # Read filesystem content
        command_indices = [index for index, char in enumerate(fs_parts[2]) if char == COMMAND_SYMBOL]
        current_command : Iterator = Iterator(0)
        data : StringHolder = StringHolder(fs_parts[2])
        self.nroot.load_dir(data, command_indices, current_command)
        
        
       
fs = FileSystem(name = "test-neon-filesystem")
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

fs.load(fs.filesystem_name)

fs.nroot.show(True)
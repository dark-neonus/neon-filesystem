# Version 1.1.1

# region neon_filesystem.py documentation

# region File
'''
@ class File - contain raw string data and data type to tell
                how to wokr with specififc file
    Properties:
        > name : str - name of current file
        
        > data_type : str - name of data type, can be anything but prefer
                        to use real classes name
                        
        > data : str - raw file data stored in string
    
    Usefull functions:
        $ get_data(self) -> str
            Return copy of string with data
            
        $ set_data(self, new_data : str)
            Assigne {new_data} to data self.data
            
        $ set_name(self, new_name : str)
            Set self.name to {new_name} if it didnt contain "/"
            Send error if contain "/ or given name is empty
            else send success message
            
        $ get_path(self, include_itself : bool = True, show_type : bool = True) -> Path
            Return parent directory path
            If {include_itself} = True, add itself to path
            If {show_type}, add file type to file name in path
            
        $ get_raw(self) -> str
            Return string with raw encoded file information
            Output example: { 01001011000101010 # 101000101001011011001 # 1001010001...001101 }
                                 ^             ^           ^                       ^
                            file_name      separator    data_type                data
    
        $ load(self, data : str)
            Load file information from raw string {data}
            Input example: { 01001011000101010 # 101000101001011011001 # 1001010001...001101 }
                                 ^             ^           ^                       ^
                            file_name      separator    data_type                data
'''
# endregion

# region Directory
'''
@ class Directory - contain numpy array of objects with
                    type of Directory or File
    Properties:
        > name : str - name of current directory
        
        > content : np.ndarray(dtype=object) - numpy array of object with
                                                type of Directory or File
                        
        > _directory_level : int - number of parent directories

    Usefull functions:
        $ add_subdirectory(self, subdirectory : Directory) -> str
            Add {subdirectory} object to content array.
            If object with same name exist, send warning
            If successfully add subdirectory, send success message
            
        $ add_file(self, file : File) -> str
            Add {file} object to content array.
            If object with same name exist, send warning
            If successfully add file, send success message
            
        $ create_subdirectory(self, name : str, content : np.array = []) -> Directory
            Create subdirectory of current directory with the given name {name}
            and add given {content} to new directory
            Use "add_subdirectory" function so send its messages
            Return created directory(reference)
            
        $ create_file(self, name : str, file_type : str, file_content : str = "") -> File
            Create file in current directory with the given name {name},
            data type {file_type} and set its content to {file_content}
            Use "add_file" function so send its messages
            Return created file(reference)
            
        $ delete_directory(self, name : str, delete_if_not_empty : bool = False)
            Delete subdirectory of current directory with {name} name
            {delete_if_not_empty} determines if function delete directory if it will be not be empty:
            
        $ get_directory(self, name : str)
            Return directory(reference to it) with given name {name}
            only if it in content array(first level subdirectory) of current directory
            If cant find directory with specific name
            send warning and return None
            
        $ get_file(self, name : str)
            Return file(reference to it) with given name {name}
            only if it in content array(first level file) of current directory
            If cant find file with specific name
            send warning and return None 
            
        $ get_item(self, name : str)
            Return item: file or directory (reference to it) with name {name}
            only if it in content array(first level file or subdirectory) of current directory
            If cant find item with specific name
            send warning and return None 
            
        $ get_path(self, include_itself : bool = True) -> Path
            Return path to parent directory
            If {include_itself} = True, add itself to path

        $ set_name(self, new_name : str)
            Set self.name to {new_name} if it didnt contain "/"
            Send error if contain "/" or given name is empty
            else send success message 

        $ show(self, expand_subdirectories : bool = False)
            Print to console simple structure of current subdirectory
            {expand_subdirectories} determines if function will print:
             - full subdirectory structure (expand_subdirectories = True)
             - only current directory structure (expand_subdirectories = False)
             
        $ get_raw(self) -> str
            Return string with raw encoded directory information
            
        $ load_dir(self, data : StringHolder, command_indices : list, current_command : Iterator)
            Recursive function that decode given data and load current directory information from it
            {command_indices} and {current_command} are needed for recursion logic
'''
# endregion

# region WhatsNew
'''
@ class WhatsNew - contain information about changes between versions
    Properties:
        > old_version : Version - old version
        
        > current_version : Version - current version
        
        > add : str - information about what was added
        
        > remove : str - information about what was removed
        
        > change : str - information about what was changed
        
        > fixes : str - information about what was fixed
        
        > note : str - some notes left by the developer
    
    Usefull functions:
        $ str(self, addition_text : bool = False) -> str:
            Return string with information
            about changes between versions      
'''
# endregion

# region Version
'''
@ class Version - contain specific version information
    Properties:
        > major : int - major version number
        
        > minor : int - minor version number
        
        > patch : int - patch version number
        
        > history : np.array - array of all version changes
                                    represented in WhatsNew objects 
                                    
        > information_text : str - text that will be added to return
                                    of self.str(self, addition_text : bool = False)
                                    if addition_text = True
    
    Usefull functions:
        $ str(self, addition_text : bool = False) -> str:
            Return string with version information in structure
                {add_text}{major}.{minor}.{patch}
            if {addition_text} = False, add_text is empty
            if {addition_text} = True, add_text = information_text
        
        $ @staticmethod load(string : str) -> Version:
            Get string like "2.17.0" as input and return Version object
        
        $ whats_new(self, addition_text : bool = False) -> str:
            Return string with information about changes
            from last element of history
            If {addition_text} = True,
            add "What's new (old_version -> current_version):" string
            at the beggining of output           
'''
#endregion 

# region Iterator
'''
@ class Iterator - created to make possible pass integer by reference
                    to functions
    Properties:
        value : int - the main value that is stored
'''
# endregion

# region StringHolder
'''
@ class StringHolder - created to make possible pass string by reference
                    to functions
    Properties:
        string : str - the main string that is stored
'''
# endregion

# region Path
'''
@ class Path - contain list of directorie names that form path
    Properties:
        > directories : list - list of path directories names (list of strings)
    
    Usefull functions:
        $ is_empty(self) -> bool:
            Return True if directories list is empty
            and False if it is not
        
        $ add_path(self, path : Union[Path, str, list]):
            Add directories to current path
            If {path} type is Path, call add_path()
            and pass path.directories to it
            If {path} type is str, separate string by "/", 
            call add_path() and pass created list to it
            If {path} type is list, iterate through it
            and add each element to self.directories
            if somehow dirrectory contain "/", it raise error
        
        $ back(self, times : int = 1):
            Remove from self.directories "times" last elements
            Raise error if "times" is negative
            
        $ str(self) -> str:
            Return string from self.directories separated by "/"
            Example: nroot/user/desktop/trash
'''
#endregion 


# endregion

''' A little hint for developer
Function for user usage:
    @ File
        > set_name
        > get_path
        > set_data
    @ Directory
        > set_name
        > create_subdirectory
        > crete_file
        > delete_subdirectory
        > delete_file
        > get_path
    @ FileSystem
        > get_directory
        > get_file
        > set_current_directory_path
        > get_current_directory
        > save
        > load
        
'''

''' Console commands documentation
    [Out of date, use "help" or "man" instead in console]

    $ exit - close console

    $ clear - clear console buffer

    $ cd [path] - go to specific path

    $ ls [options] [path] - show content of directory in path
        Flags:
            "-R" - will show content of all subdirectories

    $ touch [filename1] [filename2] [...] - crete empty file
    
    $ mkdir [dirname1] [dirname2] [...] - create empty directory
    
    $ rm [options] [filename1] [filename2] [...] - remove file with specific name
        Flags:
            "-r" or "-R" - will delete folder even if isnt empty
            
    $ cat [filename1] [filename2] [...] - print content of specific file

'''
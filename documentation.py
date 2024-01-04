# Version 1.1.1

'''

@ class File - contain raw string data and data type to tell
                how to wokr with specififc file
    Properties:
        > name : str - name of current file
        
        > data_type : str - name of data type, can be anything but prefer
                        to use real classes name
                        
        > data : str - raw file data stored in string
    
    Usage functions:
        $ get_data(self) -> str
            Return copy of string with data
            
        $ set_data(self, new_data : str)
            Assigne new content to data self.data
            
        $ set_name(self, new_name : str)
            Set new name to file if it didnt contain forbidden symbols
            Send error if contain forbidden symbols or given name is empty
            else send success message 
            
        $ get_path(self, include_itself : bool = True, show_type : bool = True) -> Path
            Return parent directory path
            If include_itself = True, add itself to path
            If show_type, add file type to file name in path
            
        $ get_raw(self) -> str
            Return string with raw encoded file information
            Output example: { 01001011000101010 # 101000101001011011001 # 1001010001...001101 }
                                 ^             ^           ^                       ^
                            file_name      separator    data_type                data
    
        $ load(self, data : str)
            Load file information from raw string
            Input example: { 01001011000101010 # 101000101001011011001 # 1001010001...001101 }
                                 ^             ^           ^                       ^
                            file_name      separator    data_type                data
    
        
@ class Directory - contain numpy array of objects with
                    type of Directory or File
    Properties:
        > name : str - name of current directory
        
        > content : np.ndarray(dtype=object) - numpy array of object with
                                                type of Directory or File
                        
        > _directory_level : int - number of parent directories

    Usage functions:
        $ add_subdirectory(self, subdirectory : Directory) -> str
            Add given directory object to content array.
            If object with same name exist, send warning
            If successfully add subdirectory, send success message
            
        $ add_file(self, file : File) -> str
            Add given file object to content array.
            If object with same name exist, send warning
            If successfully add file, send success message
            
        $ create_subdirectory(self, name : str, content : np.array = []) -> Directory
            Create subdirectory of current directory with the given name
            and add given content to new directory
            Use "add_subdirectory" function so send its messages
            Return created directory(reference)
            
        $ create_file(self, name : str, file_type : str, file_content : str = "") -> File
            Create file in current directory with the given name,
            file type and set its content to file_content
            Use "add_file" function so send its messages
            Return created file(reference)
            
        $ delete_directory(self, name : str, delete_if_not_empty : bool = False)
            Delete subdirectory of current directory with specific name
            "delete_if_not_empty" determines if function delete directory if it will be not be empty:
            
        $ get_directory(self, name : str)
            Return directory(reference to it) with given name
            only if it in content array(first level subdirectory) of current directory
            If cant find directory with specific name
            send warning and return None
            
        $ get_file(self, name : str)
            Return file(reference to it) with given name
            only if it in content array(first level file) of current directory
            If cant find file with specific name
            send warning and return None 
            
        $ get_item(self, name : str)
            Return item: file or directory (reference to it) with given name
            only if it in content array(first level file or subdirectory) of current directory
            If cant find item with specific name
            send warning and return None 
            
        $ get_path(self, include_itself : bool = True) -> Path
            Return path to parent directory
            If include_itself = True, add itself to path

        $ set_name(self, new_name : str)
            Set new name to current directory if it didnt contain forbidden symbols
            Send error if contain forbidden symbols or given name is empty
            else send success message 

        $ show(self, expand_subdirectories : bool = False)
            Print to console simple structure of current subdirectory
            "expand_subdirectories" determines if function will print:
             - full subdirectory structure (expand_subdirectories = True)
             - only current directory structure (expand_subdirectories = False)
             
        $ get_raw(self) -> str
            Return string with raw encoded directory information
            
        $ load_dir(self, data : StringHolder, command_indices : list, current_command : Iterator)
            Recursive function that decode given data and load current directory information from it
            "command_indices" and "current_command" are needed for recursion logic

'''

''' 
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

'''
Console documentation

    $ exit - close console

    $ clear - clear console buffer

    $ cd [path] - go to specific path

    $ ls [flags] - show content of current directory
        Flags:
            "-r" - will show content of all subdirectories

    $ touch [filename1] [filename2] [...] - crete empty file
    
    $ mkdir [dirname1] [dirname2] [...] - create empty directory
    
    $ rm [flags] [filename1] [filename2] [...] - remove file with specific name
        Flags:
            "-r" - will delete folder even if isnt empty

'''
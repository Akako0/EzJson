"""
Ver: 0.1.2
Credit: Akako0 https://github.com/Akako0/ez_json
This code is open source and can be modified as wanted.

Ez_json is a simple json library that allows you to easily create, read and modify json files.
It is not a replacement for the json module, but a wrapper for it. 
It is not as fast as the json module, but it is much easier to use.
The main goal of this module is to make json files as easy to use as possible not to replace the json module.
If you have any suggestions or find any bugs, please let me know.
If you want to support this project, please give it a star on github.
Check also my buy me a coffee page: https://www.buymeacoffee.com/akakoTheDev
"""

from json import load, dump
from pathlib import Path

class EzJson:
    """
    Makes json easier to use in python
    Arguments: file_path: str
    """
    def __init__ (self, file_path: str, encoding: str = 'utf-8') -> None:
        self.file_path = file_path
        self.encoding = encoding
        self.exists = Path(file_path).exists()
        self.file_name = Path(file_path).name
        if not self.exists:
            self.empty = True
            self.file_size = 0
            print(
                f"Warning: {self.file_path} doesn't exist !"
            )
            return
        self.file_size = Path(file_path).stat().st_size
        if self.file_size != 0: self.empty = False
        else:   self.empty = True
        #* Warn if file doesn't exist
    def file_missing (self) -> None:
        """
        Check if file is missing
        Arguments: None
        """
        if not self.exists:
            raise Exception(
                f"Sorry, {self.file_path} doesn't exist, create the file first, then try again."
            )
            return False

    def file_exist (self) -> None:
        """
        Check if file exist
        Arguments: None
        """
        if self.exists:
            raise Exception(
                f"Sorry, {self.file_path} already exists, delete the file first, then try again."
            )
            return False
        
    def update (self) -> bool:
        """
        Update file informations
        Arguments: None
        """
        self.exists = Path(self.file_path).exists()
        self.file_name = Path(self.file_path).name
        self.file_size = Path(self.file_path).stat().st_size
        if self.file_size != 0: self.empty = False
        else:   self.empty = True
    
    def create (self) -> bool:
        """
        Create json file
        Arguments: None
        """
        self.file_exist()
        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump({}, json_file)
        self.update()
        return True

    def delete (self) -> bool:
        """
        Delete json file
        Arguments: None
        """
        self.file_missing()
        Path(self.file_path).unlink()

    def key_exist (self, key: str) -> bool:
        """
        Check if key exist
        Arguments: key: str
        """
        self.file_missing()
        with open(self.file_path, encoding = self.encoding) as json_file:
            raw = load(json_file)
        if key in raw:
            return True
        return False


    def value_exist (self, value) -> bool:
        """
        Check if value exist
        Arguments: value: any
        """

        self.file_missing()
        with open(self.file_path, encoding = self.encoding) as json_file:
            raw = load(json_file)
        if value in raw.values():
            return True
        return False   

    def read (self, key: str = None) -> dict:
        """
        Read json file
        Arguments: *optional* key: str
        """
        self.file_missing()
        with open(self.file_path, encoding = self.encoding) as json_file:
            raw = load(json_file)
        if key:
            return raw[key]
        return raw

    def write (self, key, value: str = None) -> bool:
        """
        Write to json file
        Arguments: value: any, *optional* key: str
        """
        self.file_missing()
        with open(self.file_path, "r", encoding = self.encoding) as json_file:
            raw = load(json_file)
        if key:
            raw[key] = value
            self.update()
        else:
            raw[len(raw)] = value
            self.update()

        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump(raw, json_file)
        return True
    
    def delete_key (self, key: str) -> bool:
        """
        Delete key from json file
        Arguments: key: str
        """
        self.file_missing()
        with open(self.file_path, "r", encoding = self.encoding) as json_file:
            raw = load(json_file)
        raw.pop(key)
        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump(raw, json_file)
        self.update()
        return True
    
    def delete_value (self, key: str) -> bool:
        """
        Delete value from json file
        Arguments: key: str
        """
        with open(self.file_path, "r", encoding = self.encoding) as json_file:
            raw = load(json_file)
        raw[key] = None
        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump(raw, json_file)
            self.update()
        return True

    def change_key (self, old_key: str, new_key: str) -> bool:
        """
        Change key name
        Arguments: old_key: str, new_key: str
        """
        self.file_missing()
        with open(self.file_path, "r", encoding = self.encoding) as json_file:
            raw = load(json_file)
        raw[new_key] = raw.pop(old_key)
        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump(raw, json_file)
            self.update()
        return True

    def change_value (self, key: str, new_value = None) -> bool:
        """
        Change value
        Arguments: key: str, new_value: any
        """
        self.file_missing()
        with open(self.file_path, "r", encoding = self.encoding) as json_file:
            raw = load(json_file)
        if new_value:
            raw[key] = new_value
        else:
            raw[key] = None
        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump(raw, json_file)
        self.update()
        return True

    def clear_file (self) -> bool:
        """
        Clear json file
        Arguments: None
        """
        self.file_missing()
        with open(self.file_path, "w", encoding = self.encoding) as json_file:
            dump({}, json_file)
        self.update()
        return True
    
    def get_keys (self) -> list:
        """
        Returns all keys
        Arguments: None
        """
        self.file_missing()
        with open(self.file_path, encoding = self.encoding) as json_file:
            raw = load(json_file)
        return list(raw.keys())
    
    def get_values (self) -> list:
        """
        Returns all values
        Arguments: None
        """
        if not self.exists:
            raise Exception(
                f"Sorry, {self.file_path} doesn't exist, create the file first, then try again."
            )
            return False
        with open(self.file_path, encoding = self.encoding) as json_file:
            raw = load(json_file)
        return list(raw.values())
    
    def get_items (self) -> list:
        """
        Returns all items
        Arguments: None
        """
        self.file_missing()
        with open(self.file_path, encoding = self.encoding) as json_file:
            raw = load(json_file)
        return list(raw.items())
"""
Credit: Akako0 https://github.com/Akako0/ez_json
This code is open source and can be modified as wanted.
"""
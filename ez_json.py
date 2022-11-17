from json import load, dump
from pathlib import Path

class Json:
    """
    Makes json easier to use in python
    Arguments: file_path: str
    """
    def __init__ (self, file_path: str) -> None:
        self.file_path = file_path
        self.exists = Path(file_path).exists()
        self.file_name = Path(file_path).name
        if self.exists: self.empty = not Path(file_path).stat().st_size
        else:   self.empty = True
        #* Warn if file doesn't exist
        if not self.exists:
            print(
                f"Warning: {self.file_path} doesn't exist !"
            )
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
        Update the class attributes
        Arguments: None
        """
        self.exists = Path(self.file_path).exists()
        self.file_name = Path(self.file_path).name
        if self.exists: self.empty = not Path(self.file_path).stat().st_size
        else:   self.empty = True
    
    def create (self) -> bool:
        """
        Create json file
        Arguments: None
        """
        self.file_exist()
        with open(self.file_path, "w") as json_file:
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
        with open(self.file_path) as json_file:
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
        with open(self.file_path) as json_file:
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
        with open(self.file_path) as json_file:
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
        with open(self.file_path, "r") as json_file:
            raw = load(json_file)
        if key:
            raw[key] = value
            self.update()
        else:
            raw[len(raw)] = value
            self.update()

        with open(self.file_path, "w") as json_file:
            dump(raw, json_file)
        return True
    
    def delete_key (self, key: str) -> bool:
        """
        Delete key from json file
        Arguments: key: str
        """
        self.file_missing()
        with open(self.file_path, "r") as json_file:
            raw = load(json_file)
        raw.pop(key)
        with open(self.file_path, "w") as json_file:
            dump(raw, json_file)
        self.update()
        return True
    
    def delete_value (self, key: str) -> bool:
        """
        Delete value from json file
        Arguments: key: str
        """
        with open(self.file_path, "r") as json_file:
            raw = load(json_file)
        raw[key] = None
        with open(self.file_path, "w") as json_file:
            dump(raw, json_file)
            self.update()
        return True

    def change_key (self, old_key: str, new_key: str) -> bool:
        """
        Change key name
        Arguments: old_key: str, new_key: str
        """
        self.file_missing()
        with open(self.file_path, "r") as json_file:
            raw = load(json_file)
        raw[new_key] = raw.pop(old_key)
        with open(self.file_path, "w") as json_file:
            dump(raw, json_file)
            self.update()
        return True

    def change_value (self, key: str, new_value = None) -> bool:
        """
        Change value
        Arguments: key: str, new_value: any
        """
        self.file_missing()
        with open(self.file_path, "r") as json_file:
            raw = load(json_file)
        if new_value:
            raw[key] = new_value
        else:
            raw[key] = None
        with open(self.file_path, "w") as json_file:
            dump(raw, json_file)
        self.update()
        return True

    def clear_file (self) -> bool:
        """
        Clear json file
        Arguments: None
        """
        self.file_missing()
        with open(self.file_path, "w") as json_file:
            dump({}, json_file)
        self.update()
        return True
    
    def get_keys (self) -> list:
        """
        Returns all keys
        Arguments: None
        """
        self.file_missing()
        with open(self.file_path) as json_file:
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
        with open(self.file_path) as json_file:
            raw = load(json_file)
        return list(raw.values())
    
    def get_items (self) -> list:
        """
        Returns all items
        Arguments: None
        """
        self.file_missing()
        with open(self.file_path) as json_file:
            raw = load(json_file)
        return list(raw.items())
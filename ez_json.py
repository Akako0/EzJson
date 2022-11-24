"""
EzJson is a simple module to make json files easier to work with.
It is not meant to be a replacement for the json module, but rather a
wrapper around it to make it easier to work with. It is not fast, but
it is simple and easy to use.

The Json class is the main class of the module. It should be innitialized
with a path to a json file and the encoding of the file, by default, the
encoding is utf-8. Remember that the file will not be created if it does
not exist, so you must create it with the create() method after innitializing
the class.

Requires Python 3.6 or higher, json, and pathlib modules.

If you have any suggestions or find any bugs, please let me know.
If you want to support this project, please give it a star on github.

Credit: Akako0 https://github.com/Akako0/ez_json
Check also my buy me a coffee page: https://www.buymeacoffee.com/akakoTheDev
This code is open source and can be modified as wanted.
"""
from warnings import warn
from json import load, dump
from pathlib import Path
from os import unlink

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
            warn(
                f"WARN: {self.file_path} doesn't exist !"
            )
            return
        self.file_size = Path(file_path).stat().st_size
        if self.file_size != 0:
            self.empty = False
        else:   self.empty = True

    # ------------------------------ Basic functions ----------------------------- #

    def update (self) -> bool:
        """
        Update self.exists, self.empty, self.file_size
        Returns: True if updated successfully
        Arguments: None
        """
        self.exists = Path(self.file_path).exists()
        self.file_name = Path(self.file_path).name
        self.file_size = Path(self.file_path).stat().st_size
        if self.file_size != 0:
            self.empty = False
        else:   self.empty = True
        return True

    def basic_read (self) -> dict:
        """
        Read json file
        Returns: the whole json file
        Arguments: None
        """
        with open(self.file_path, encoding = self.encoding) as json_file:
            data = load(json_file)
        return data

    def basic_write (self, data: dict) -> bool:
        """
        Write json file
        Returns: True if written successfully
        Arguments: data: dict
        """
        try:
            with open(self.file_path, "w", encoding = self.encoding) as json_file:
                dump(data, json_file)
            return True
        except ValueError as error:
            warn(
                f"ERROR: {error}"
            )
            return False
    def create_file (self) -> bool:
        """
        Create json file
        Returns: True if created successfully
        Arguments: None
        """
        self.file_exist()
        success = self.basic_write({})
        self.update()
        return success

    def delete_file (self) -> bool:
        """
        Delete json file
        Returns: True if deleted successfully
        Arguments: None
        """
        self.file_missing()
        try:
            unlink(self.file_path)
            self.update()
            return True

        except ValueError as error:
            warn(
                f"ERROR: {error}"
            )
            return False

    # ------------------------------ Statements functions ----------------------------- #

    def file_missing (self) -> None:
        """
        Check if file is missing
        Returns: None & raises Exception
        Arguments: None
        """
        if not self.exists:
            raise Exception(
                f"Sorry, {self.file_path} doesn't exist, create the file first, then try again."
            )

    def file_exist (self) -> None:
        """
        Check if file exist
        Returns: None & raises Exception
        Arguments: None
        """
        if self.exists:
            raise Exception(
                f"Sorry, {self.file_path} already exists, delete the file first, then try again."
            )

    def key_exist (self, key: str) -> bool:
        """
        Check if key exist
        Returns: True if key exist
        Arguments: key: str
        """
        self.file_missing()
        data = self.basic_read()
        if key in data:
            return True
        return False

    def value_exist (self, value) -> bool:
        """
        Check if value exist
        Returns: True if value exist
        Arguments: value: any
        """

        self.file_missing()
        data = self.basic_read()
        if value in data.values():
            return True
        return False

    # ------------------------------ Advenced functions ----------------------------- #


    def read (self, key: str = None) -> dict:
        """
        Read json file
        Returns: key value if key is specified, else returns the whole json file
        Arguments: *optional* key: str
        """
        self.file_missing()
        data = self.basic_read()
        if key is not None:
            return data.get(key)
        return data

    def write (self, key, value: str = None) -> bool:
        """
        Write key : value to json file
        Returns: True if written successfully, False if not
        Arguments: value: any, *optional* key: str
        """
        self.file_missing()
        data = self.basic_read()

        if key is not None:
            data[key] = value
        else:
            data[len(data)] = value
        self.update()
        self.basic_write(data)
        return True

    #TODO: add delete function

    def set_nested_value (self, data: dict, key: str, value: str or int) -> bool:
        """
        Update the value of a key, if key doesn't exist, nothing will happen.
        Returns: True if updated successfully, False if not
        Arguments: data: dict, key: str, value: str or int
        """
        for skey, val in data.items():
            if isinstance(val, dict):
                return self.set_nested_value(val, key, value)
            elif skey == key:
                data[skey] = value
                return True
            else:
                continue
        return False

    def change_value (self, key: str, value: str or int) -> bool:
        """
        Change the value of a key, if key doesn't exist, nothing will happen.
        Arguments: key: str, new_value: any
        """
        self.file_missing()
        data = self.basic_read()
        if self.set_nested_value(data, key, value):
            self.update()
            self.basic_write(data)
            return True
        warn ('WARN: key not found !')

    # ------------------------------ Simple functions ----------------------------- #

    def clear_file (self) -> bool:
        """
        Clear json file
        Arguments: None
        """
        self.file_missing()
        self.basic_write({})
        self.update()

    def get_keys (self) -> list:
        """
        Returns: list of keys in json file
        Arguments: None
        """
        self.file_missing()
        data = self.basic_read()
        return list(data.keys())

    def get_values (self) -> list:
        """
        Returns: list of values in json file
        Arguments: None
        """
        self.file_missing()
        data = self.basic_read()
        return list(data.values())

    def get_items (self) -> list:
        """
        Returns: list of items in json file
        Arguments: None
        """
        self.file_missing()
        data = self.basic_read()
        return list(data.items())

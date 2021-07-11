from cryptography.fernet import Fernet
import json


class DataFileManager:
    def __init__(self, data_file, key_file):
        self.key_file = key_file
        self.data_file = data_file
        with open('data.json', 'r') as f:
            if "\"encrypted\": false" in f.read():
                self.encrypted = False
            else:
                self.encrypted = True

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as kf:
            kf.write(key)

    def load_key(self):
        with open(self.key_file, 'rb') as file:
            key = file.read()
        return key

    def encrypt(self):
        if self.encrypted:
            print("File already encrypted!")
        else:
            f = Fernet(self.load_key())
            with open(self.data_file, 'rb') as file:
                file_data = file.read()
            encrypted_data = f.encrypt(file_data)
            with open(self.data_file, 'wb') as file:
                file.write(encrypted_data)
        self.encrypted = True

    def decrypt(self):
        if not self.encrypted:
            print("File already decrypted!")
        else:
            f = Fernet(self.load_key())
            with open(self.data_file, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open(self.data_file, 'wb') as file:
                file.write(decrypted_data)
        self.encrypted = False

    def change_key(self):
        if self.encrypted:
            self.decrypt()
            self.generate_key()
            self.encrypt()
        else:
            self.generate_key()

    def get_data(self):
        self.decrypt()
        with open(self.data_file, 'r') as file:
            data = json.load(file)
        self.encrypt()
        return data

    def save_data(self, data):
        self.decrypt()
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)
        self.encrypt()

    def is_editing(self):
        data = self.get_data()
        return data['isEditing']

    def switch_editing(self, flag):
        '''
        for parent

        '''
        data = self.get_data()
        data['isEditing'] = flag
        self.save_data(data)

    def is_writing(self):
        '''
        for children

        '''
        data = self.get_data()
        return data['isWriting']

    def switch_writing(self, flag):
        data = self.get_data()
        data['isWriting'] = flag
        self.save_data(data)

    def need_update(self):
        data = self.get_data()
        return data['newVersion']

    def switch_need_update(self, flag):
        data = self.get_data()
        data['newVersion'] = flag
        self.save_data(data)


# DataFileManager('data.json', 'key.key').decrypt()
#DataFileManager('data.json', 'key.key').encrypt()

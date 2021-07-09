from DataFileManager import DataFileManager
import hashlib


class PasswordManager(DataFileManager):
    def __init__(self, data_file, key_file):
        DataFileManager.__init__(self, data_file, key_file)
        self.data = self.get_data()

    def update_data(self):
        self.data = self.get_data()

    def change_pwd(self, new_pwd, parent=False, child=False):
        if parent == child:
            raise Exception("Can't change both pwd at the same time\n Or not change anything at all")
        else:
            if parent:
                role = 'parent'
            else:
                role = 'child'
            hashed_pwd = hashlib.sha256(new_pwd.encode()).hexdigest()
            self.data[role] = hashed_pwd
            self.save_data(self.data)

    def get_parent(self):
        return self.data['parent']

    def get_child(self):
        return self.data['child']

    def compare_pwd(self, pwd_input):
        # result = [isParentPwd, isChildPwd]
        result = [False] * 2
        pwd_input = hashlib.sha256(pwd_input.encode()).hexdigest()
        if self.get_parent() == pwd_input:
            result[0] = True
        elif self.get_child() == pwd_input:
            result[1] = True
        return result

from typing import Any
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QObject, Qt, pyqtSlot
from .qqtEngineManager import qqtEngineManager

class qqtModel(QAbstractListModel):
    def __init__(self, model_name, keys, parent=None) -> None:
        super().__init__(parent)
        self._num_of_roles = len(keys)
        self._keys = keys
        for i in range(self._num_of_roles):
            self.__setattr__(f"role_{i+1}", QtCore.Qt.UserRole + i + 1)
            self.__setattr__(f"role_{i+1}_name", keys[i])
            self.__setattr__(f"role_{i+1}_index", i)

        self.items = []
        self.connect_to_qml(model_name)

    def connect_to_qml(self, model_name):
        qqtEngineManager.get_engine().rootContext().setContextProperty(model_name, self)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        row = index.row()
        if index.isValid() and 0 <= row < self.rowCount():
            for i in range(self._num_of_roles):
                if role == self.__getattribute__(f"role_{i+1}"):
                    return self.items[row][self._keys[i]]            
        return None
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.items)
    
    def roleNames(self):
        roles = {}
        for i in range(self._num_of_roles):
            roles[self.__getattribute__(f"role_{i+1}")] = self.__getattribute__(f"role_{i+1}_name").encode()
        return roles
    
    @pyqtSlot(int, result="QVariant")
    def get(self, row):
        if 0 <= row < self.rowCount():
            return self.items[row]
        
    def add_items(self, items):
        self.beginResetModel()
        for i in items:
            self.items.append(i)
        self.endResetModel()

    def clear_items(self):
        self.beginResetModel()
        self.items = []
        self.endResetModel()

class qqtDictModel(QAbstractListModel):
    def __init__(self, model_name, keys, parent=None) -> None:
        super().__init__(parent)
        self._num_of_roles = len(keys)
        self._keys = keys
        for i in range(self._num_of_roles):
            self.__setattr__(f"role_{i+1}", QtCore.Qt.UserRole + i + 1)
            self.__setattr__(f"role_{i+1}_name", keys[i])
            self.__setattr__(f"role_{i+1}_index", i)

        self.items = {}
        self.connect_to_qml(model_name)

    def connect_to_qml(self, model_name):
        qqtEngineManager.get_engine().rootContext().setContextProperty(model_name, self)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        row = index.row()
        if index.isValid() and 0 <= row < self.rowCount():
            for i in range(self._num_of_roles):
                if role == self.__getattribute__(f"role_{i+1}"):
                    key = self._keys[i]
                    return self.items[row][key] if key in self.items[row] else None
        return None
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.items)
    
    def roleNames(self):
        roles = {}
        for i in range(self._num_of_roles):
            roles[self.__getattribute__(f"role_{i+1}")] = self.__getattribute__(f"role_{i+1}_name").encode()
        return roles
    
    @pyqtSlot(str, result="QVariant")
    def get(self, row):
        # Convert string to int if needed, or use as-is if it's a valid key
        try:
            row_int = int(row)
            if row_int in self.items:
                return self.items[row_int]
        except (ValueError, TypeError):
            pass
        if row in self.items:
            return self.items[row]
        return None
        
    def set_dict(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def clear_dict(self):
        self.beginResetModel()
        self.items = {}
        self.endResetModel()

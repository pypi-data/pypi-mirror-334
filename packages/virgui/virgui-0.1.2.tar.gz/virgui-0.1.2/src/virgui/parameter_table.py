from finesse.utilities.tables import Table
from PySide6 import QtCore
from PySide6.QtCore import Qt


# https://www.pythonguis.com/tutorials/pyside6-qtableview-modelviews-numpy-pandas/
class ParameterTableModel(QtCore.QAbstractTableModel):

    def __init__(self, finesse_table: Table):
        super().__init__()
        self._finesse_table = finesse_table

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._finesse_table.table[1:, :][index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._finesse_table.table.shape[0] - 1

    def columnCount(self, index):
        return self._finesse_table.table.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._finesse_table.table[0, section])

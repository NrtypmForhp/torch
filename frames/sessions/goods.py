from PyQt6.QtWidgets import (QFrame, QGridLayout, QLabel, QPushButton, QSpinBox, QTableWidget, QHeaderView)
from PyQt6.QtCore import Qt

class SGoods(QFrame):
    def __init__(self, parent, messages:dict):
        super(self.__class__, self).__init__(parent)
        
        # Main settings
        self.lay = QGridLayout(self)
        self.messages = messages
        
        self.label_goods_page = QLabel(self, text=self.messages["goods_page"])
        self.lay.addWidget(self.label_goods_page, 0, 1, Qt.AlignmentFlag.AlignTop)
        
        self.button_new_good = QPushButton(self, text=self.messages["new_good"])
        # self.button_new_good.clicked.connect(self.new_good_function)
        self.lay.addWidget(self.button_new_good, 1, 0, Qt.AlignmentFlag.AlignTop)
        
        self.spinbox_goods_page = QSpinBox(self)
        self.lay.addWidget(self.spinbox_goods_page, 1, 1, Qt.AlignmentFlag.AlignTop)
        
        self.table_goods = QTableWidget(self)
        self.table_goods.setColumnCount(3)
        table_goods_header_labels = [self.messages["goods_table_good"], self.messages["goods_table_quantity"], self.messages["goods_table_price"]]
        self.table_goods.setHorizontalHeaderLabels(table_goods_header_labels)
        self.table_goods_headers = self.table_goods.horizontalHeader()
        self.lay.addWidget(self.table_goods, 2, 0, 1, 2, Qt.AlignmentFlag.AlignTop)
        
    # Resize functions
    def resizeEvent(self, a0):
        W_width = self.width()
        W_height = self.height()
        
        try:
            # Goods table
            self.table_goods.setFixedSize(W_width - 20, W_height - 80)
            self.table_goods_headers.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.table_goods_headers.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.table_goods_headers.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        except AttributeError: pass
        return super().resizeEvent(a0)
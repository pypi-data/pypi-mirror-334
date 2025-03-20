from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QStyle, QStyledItemDelegate, QStyleOptionViewItem


class NoFocusDelegate(QStyledItemDelegate):
    def paint(self, painter, option: QStyleOptionViewItem, index):
        option.state = QStyle.StateFlag.State_Enabled  # type: ignore
        super().paint(painter, option, index)


class ComboBoxNoTextDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        # Create a copy of the style option
        opt = option

        # Initialize the style option with the index data
        self.initStyleOption(opt, index)

        # Set decoration width to match the rect width
        opt.decorationSize.setWidth(opt.rect.width())

        # Get the style from the widget or application
        style = opt.widget.style() if opt.widget else QApplication.style()

        # Draw the item using the style
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, opt.widget)

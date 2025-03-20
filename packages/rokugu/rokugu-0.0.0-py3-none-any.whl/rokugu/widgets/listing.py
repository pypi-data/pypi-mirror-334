from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget


class Listing(QListWidget):
    selected = Signal(int, QListWidgetItem)

    def __init__(self) -> None:
        super().__init__()

        self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.setUniformItemSizes(False)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)

        self.itemActivated.connect(
            lambda q_list_widget_item: self.selected.emit(
                self.row(q_list_widget_item), q_list_widget_item
            )
        )
        self.itemPressed.connect(
            lambda q_list_widget_item: self.selected.emit(
                self.row(q_list_widget_item), q_list_widget_item
            )
        )

    def append(
        self, accessible_text_role: str, user_role: object, q_widget: QWidget
    ) -> None:
        q_list_widget_item = QListWidgetItem(self)
        q_list_widget_item.setData(
            Qt.ItemDataRole.AccessibleTextRole, accessible_text_role
        )
        q_list_widget_item.setData(Qt.ItemDataRole.UserRole, user_role)
        q_list_widget_item.setSizeHint(q_widget.sizeHint())

        self.setItemWidget(q_list_widget_item, q_widget)

    def insert(
        self,
        index: int,
        accessible_text_role: str,
        user_role: object,
        q_widget: QWidget,
    ) -> None:
        q_list_widget_item = QListWidgetItem()
        q_list_widget_item.setData(
            Qt.ItemDataRole.AccessibleTextRole, accessible_text_role
        )
        q_list_widget_item.setData(Qt.ItemDataRole.UserRole, user_role)
        q_list_widget_item.setSizeHint(q_widget.sizeHint())

        self.insertItem(index, q_list_widget_item)

        self.setItemWidget(q_list_widget_item, q_widget)

    def remove(self, user_role: object) -> None:
        q_list_widget_item: QListWidgetItem | None = None

        for index in reversed(range(self.count())):
            _ = self.item(index)

            if _.data(Qt.ItemDataRole.UserRole) == user_role:
                q_list_widget_item = _
                break

        if isinstance(q_list_widget_item, QListWidgetItem):
            index = self.row(q_list_widget_item)

            if index == -1:
                return

            self.model().removeRow(index)

    def removeRow(self, index: int) -> None:
        self.model().removeRow(index)

    def removeItem(self, q_list_widget_item: QListWidgetItem) -> None:
        index = self.row(q_list_widget_item)

        if index == -1:
            return

        self.model().removeRow(index)

    def select(self, user_role: object) -> None:
        self.clearSelection()

        for index in reversed(range(self.count())):
            q_list_widget_item = self.item(index)

            if q_list_widget_item.data(Qt.ItemDataRole.UserRole) == user_role:
                q_list_widget_item.setSelected(True)

                self.scrollToItem(
                    q_list_widget_item, QListWidget.ScrollHint.EnsureVisible
                )

                self.selected.emit(index, q_list_widget_item)

                break

    def selectRow(self, index: int) -> None:
        q_list_widget_item = self.item(index)

        if isinstance(q_list_widget_item, QListWidgetItem):
            self.clearSelection()

            q_list_widget_item.setSelected(True)

            self.scrollToItem(
                q_list_widget_item, QListWidget.ScrollHint.EnsureVisible
            )
            self.selected.emit(index, q_list_widget_item)

    def selectItem(self, q_list_widget_item: QListWidgetItem) -> None:
        index = self.row(q_list_widget_item)

        if index == -1:
            return

        self.clearSelection()

        q_list_widget_item.setSelected(True)

        self.scrollToItem(
            q_list_widget_item, QListWidget.ScrollHint.EnsureVisible
        )
        self.selected.emit(index, q_list_widget_item)

    def filter(self, accessible_text_role: str) -> None:
        for index in reversed(range(self.count())):
            q_list_widget_item = self.item(index)

            _ = q_list_widget_item.data(Qt.ItemDataRole.AccessibleTextRole)

            if not isinstance(_, str):
                continue

            q_list_widget_item.setHidden(
                _.lower().find(accessible_text_role.lower()) == -1
            )

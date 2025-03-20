from typing import override

from PySide6.QtGui import QResizeEvent, Qt
from PySide6.QtWidgets import QLabel, QSizePolicy


class Label(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setWordWrap(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

    @override
    def resizeEvent(self, event: QResizeEvent, /) -> None:
        q_string = self.fontMetrics().elidedText(
            self.text(), Qt.TextElideMode.ElideRight, event.size().width()
        )
        self.setText(q_string)
        return super().resizeEvent(event)

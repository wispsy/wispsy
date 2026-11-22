"""Independent immutable status application for the shared Carets shell contract."""
from dataclasses import dataclass, replace

from carets import AppShell, WindowSizeMsg
from carets.components import ComponentState, Label, Progress


@dataclass(frozen=True)
class StatusDesk:
    width: int = 80
    height: int = 24
    completed: int = 2
    total: int = 3

    def update(self, message):
        if isinstance(message, WindowSizeMsg):
            return replace(self, width=message.width, height=message.height)
        return self

    def view(self):
        body = '\n'.join((Label('Independent status desk 界', ComponentState('heading')).view(),
                          Progress(self.completed, self.total).view()))
        return AppShell('Status desk').frame(self.width, self.height, body=body,
            navigation=('Summary',), status='Read only').buffer

from PyQt5.QtWidgets import (
    QComboBox,
)
from PyQt5.QtCore import QThread, pyqtSignal
from tasktimer.tempo import Tempo
from functools import partial


class TicketSelector(QComboBox):
    def __init__(self, *args, **kwargs):
        super(TicketSelector, self).__init__(*args, **kwargs)
        self._thread = None
        self.settings = None

    def load(self):
        if self.settings is None:
            raise ValueError("settings not set")
        if self._thread is None:
            self._thread = GetTicketsThread(settings=self.settings)
            self._thread.resultReady.connect(partial(self._handle_load_tickets))
            self._thread.start()
            self.clear()
            self.addItem("Loading...")
            self.setEnabled(False)

    def _handle_load_tickets(self, items):
        self.clear()
        for value, description in items:
            self.addItem("{}: {}".format(value, description), value)
        self.setEnabled(True)
        self._thread = None


class GetTicketsThread(QThread):
    resultReady = pyqtSignal(list)

    def __init__(self, *args, settings=None, **kwargs):
        super(GetTicketsThread, self).__init__(*args, **kwargs)

        settings = {} if settings is None else settings

        self.jira_domain = settings.get("jira_domain")
        self.jira_username = settings.get("jira_username")
        self.jira_token = settings.get("jira_token")
        self.tempo_token = settings.get("tempo_token")

    def run(self):
        t = Tempo(self.jira_domain, self.jira_username, self.jira_token, self.tempo_token)
        items = []
        for item in t.get_in_progress_tickets().items():
            items.append(item)
        self.resultReady.emit(items)

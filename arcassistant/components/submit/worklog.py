from PyQt5.QtWidgets import (
    QPushButton,
)
from arcassistant.shared.settings import Settings
from tasktimer.timer import Timer
from tasktimer.tempo import Tempo
from PyQt5.QtCore import QThread, pyqtSignal
from functools import partial


class WorkLogSubmitButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(WorkLogSubmitButton, self).__init__(*args, **kwargs)
        self._thread = None
        self._disabled_widgets = []
        self._on_success = None

    def send(self, settings: Settings, timer: Timer, ticket: str, description: str,
             disabled_widgets_while_loading=None,
             on_success=None):

        if type(disabled_widgets_while_loading) == list:
            self._disabled_widgets = disabled_widgets_while_loading

        self._on_success = on_success

        if self._thread is None:
            for w in self._disabled_widgets:
                w.setEnabled(False)
            self._thread = PostWorkLogThread(
                settings=settings,
                timer=timer,
                ticket=ticket,
                description=description,
            )
            self._thread.resultReady.connect(partial(self._handle_loaded))
            self._thread.start()
            self.setEnabled(False)

    def _handle_loaded(self, success):
        self._thread = None
        for w in self._disabled_widgets:
            w.setEnabled(True)
        if self._on_success is not None and success:
            self._on_success()


class PostWorkLogThread(QThread):
    resultReady = pyqtSignal(bool)

    def __init__(
            self, *args,
            settings=None,
            timer=None,
            ticket=None,
            description=None,
            **kwargs
    ):
        super(PostWorkLogThread, self).__init__(*args, **kwargs)

        settings = {} if settings is None else settings

        self.jira_domain = settings.get("jira_domain")
        self.jira_username = settings.get("jira_username")
        self.jira_token = settings.get("jira_token")
        self.tempo_token = settings.get("tempo_token")
        self.timer = timer
        self.ticket = ticket
        self.description = description

    def run(self):
        t = Tempo(self.jira_domain, self.jira_username, self.jira_token, self.tempo_token)
        t.send_worklogs(self.timer, self.ticket, self.description)
        self.resultReady.emit(True)

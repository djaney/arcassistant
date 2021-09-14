from arcassistant.views.assistant import MainWindow, SettingsDialog
from tasktimer.timer import Timer
from functools import partial
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from arcassistant.shared.settings import Settings
from tasktimer.tempo import Tempo


class AssistantCtrl(object):
    LBL_BTN_START = "Start"
    LBL_BTN_PAUSE = "Pause"

    def __init__(self, view: MainWindow):
        self._timer = None
        self._view = view
        self._settings_ctrl = SettingsCtrl(view=self._view.window_settings)
        self._q_timer = QTimer()
        self._thread_load_tickets = None
        self._connect()
        # initializations
        self._populate_time()

        # view
        self._view.button_save.setEnabled(False)

        self._q_timer.start(1000)

        self._settings_ctrl.load()

        self._view.select_ticket.settings = self._settings_ctrl.settings
        self._view.select_ticket.load()

    def _connect(self):
        self._view.button_play.clicked.connect(partial(self._timer_play))
        self._view.button_reset.clicked.connect(partial(self._timer_reset))
        self._view.button_save.clicked.connect(partial(self._timer_save))
        self._q_timer.timeout.connect(partial(self._populate_time))
        self._view.menu_settings.triggered.connect(partial(self._open_settings))
        self._view.menu_reload.triggered.connect(partial(self._view.select_ticket.load))

    def _load_window(self):
        pass

    def _populate_time(self):

        if self._timer:
            text = self._timer.print()
        else:
            text = "0m"

        self._view.label_time.setText("Current Time: {}".format(text))

    def _timer_play(self):
        if self._timer is None:
            self._timer = Timer()

        if self._timer.start_time is None:
            self._timer.start()
            self._view.button_play.setText(self.LBL_BTN_PAUSE)
            self._view.button_reset.setEnabled(False)
            self._view.button_save.setEnabled(False)
        else:
            self._timer.end()
            self._view.button_play.setText(self.LBL_BTN_START)
            self._view.button_reset.setEnabled(True)
            self._view.button_save.setEnabled(True)

        self._populate_time()

    def _timer_reset(self):
        self._timer = None
        self._populate_time()
        self._view.button_reset.setEnabled(True)
        self._view.button_save.setEnabled(False)
        self._view.text_description.clear()

    def _timer_save(self):
        self._view.button_save.send(
            self._settings_ctrl.settings,
            self._timer,
            self._view.select_ticket.currentData(),
            self._view.text_description.toPlainText(),
            disabled_widgets_while_loading=[
                self._view.select_ticket,
                self._view.text_description
            ],
            on_success=self._timer_reset
        )

    def _open_settings(self):
        self._settings_ctrl.load()
        self._view.window_settings.show()


class SettingsCtrl(object):
    def __init__(self, view: SettingsDialog):
        self._view = view
        self.form_text_map = {
            "jira_domain": self._view.text_jira_domain,
            "jira_username": self._view.text_jira_username,
            "jira_token": self._view.text_jira_token,
            "tempo_token": self._view.text_tempo_token,
        }
        self.settings = Settings("arc-assistant")
        self._connect()

    def _populate(self):
        for key, view in self.form_text_map.items():
            view.setText(self.settings.get(key))

    def _connect(self):
        self._view.button_save.clicked.connect(partial(self._save))

    def _save(self):
        for key, view in self.form_text_map.items():
            self.settings.set(key, view.text())
        self.settings.save()
        self._view.close()

    def load(self):
        self.settings.load()
        self._populate()


class GetTicketsThread(QThread):
    resultReady = pyqtSignal(list)

    def __init__(self, *args, jira_domain=None, jira_username=None, jira_token=None, tempo_token=None, **kwargs):
        super(GetTicketsThread, self).__init__(*args, **kwargs)

        self.jira_domain = jira_domain
        self.jira_username = jira_username
        self.jira_token = jira_token
        self.tempo_token = tempo_token

    def run(self):
        t = Tempo(self.jira_domain, self.jira_username, self.jira_token, self.tempo_token)
        items = []
        for item in t.get_in_progress_tickets().items():
            items.append(item)
        self.resultReady.emit(items)

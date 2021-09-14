from PyQt5.QtWidgets import (
    QMainWindow,
    QDialog,
    QWidget,
    QGridLayout,
    QFormLayout,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QLabel
)
from arcassistant.components.selector.ticket_selector import TicketSelector
from arcassistant.components.submit.worklog import WorkLogSubmitButton


class MainWindow(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Arc Assistant')
        self.setFixedSize(400, 300)
        # Set the central widget
        self.general_layout = QGridLayout()
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.central_widget)
        self._create_widgets()

    def _create_widgets(self):
        self.label_time = QLabel()
        self.general_layout.addWidget(self.label_time, 0, 0, 1, 3)

        self.button_play = QPushButton('Start')
        self.general_layout.addWidget(self.button_play, 1, 0)

        self.button_reset = QPushButton('Reset')
        self.general_layout.addWidget(self.button_reset, 1, 1)

        self.button_save = WorkLogSubmitButton('Save')
        self.general_layout.addWidget(self.button_save, 1, 2)

        self.select_ticket = TicketSelector()
        self.general_layout.addWidget(self.select_ticket, 2, 0, 1, 3)

        self.text_description = QTextEdit()
        self.general_layout.addWidget(self.text_description, 3, 0, 1, 3)

        self.window_settings = SettingsDialog(self)

        self._menu_bar = self.menuBar()
        self.menu_settings = self._menu_bar.addAction('&Settings')
        self.menu_reload = self._menu_bar.addAction('&Reload')


class SettingsDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self.setFixedSize(400, 140)
        self.setModal(True)
        self.setWindowTitle("Settings")

        self.general_layout = QFormLayout()
        self.setLayout(self.general_layout)
        self._create_widgets()

    def _create_widgets(self):
        self.text_jira_domain = QLineEdit()
        self.general_layout.addRow("Jira Domain", self.text_jira_domain)

        self.text_jira_username = QLineEdit()
        self.general_layout.addRow("Jira Username", self.text_jira_username)

        self.text_jira_token = QLineEdit()
        self.general_layout.addRow("Jira Token", self.text_jira_token)

        self.text_tempo_token = QLineEdit()
        self.general_layout.addRow("Tempo Token", self.text_tempo_token)
        self.button_save = QPushButton("Save")
        self.general_layout.addRow(self.button_save)
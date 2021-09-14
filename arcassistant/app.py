import sys
from PyQt5.QtWidgets import QApplication
from .views.assistant import MainWindow
from .controllers.assistant import AssistantCtrl


def main():
    """Main function."""
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = MainWindow()
    view.show()
    # Create instances of the model and the controller
    AssistantCtrl(view)
    # Execute calculator's main loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
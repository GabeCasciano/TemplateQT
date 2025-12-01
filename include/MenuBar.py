import logging
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction, QMenuBar
from .Mqtt import MqttClient


class MenuBar(QMenuBar):

    CloseAppAction = QAction("Close App")
    ConnectMqttAction = QAction("Conect Mqtt")
    DisconnectMqttAction = QAction("Disconnect Mqtt")

    _instance = None

    LOG_FMT_STR = f"[Menubar] - %s"

    @classmethod
    def get_instance(cls, parent=None):
        if cls._instance is None:
            cls._instance = cls(parent)
        return cls._instance

    def __init__(self, parent=None):
        super().__init__(parent)

        self._m_client = MqttClient.get_instance()

        app_menu = self.addMenu("App")
        mqtt_submenu = app_menu.addMenu("Mqtt")
        app_menu.addAction(MenuBar.CloseAppAction)

        mqtt_submenu.addAction(MenuBar.ConnectMqttAction)
        mqtt_submenu.addAction(MenuBar.DisconnectMqttAction)

        if parent is not None:
            self.CloseAppAction.triggered.connect(parent.close)

        MenuBar.ConnectMqttAction.triggered.connect(self._m_client.ConnectBroker)
        MenuBar.DisconnectMqttAction.triggered.connect(self._m_client.DisconnectBroker)

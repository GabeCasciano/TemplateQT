from paho.mqtt.client import Client, MQTTv5, topic_matches_sub
import json
from PyQt5.QtCore import QTime, pyqtSignal, pyqtSlot, QTimer, QObject
from PyQt5.QtWidgets import QInputDialog, QWidget
import logging

from pydantic import BaseModel
from pathlib import Path


class MqttClient(QWidget):

    class Settings(BaseModel):
        host_name: str = "localhost"
        client_name: str = "NcmViz"
        host_port: int = 1883

    class Watchdog(QObject):

        CountSignal = pyqtSignal(int)
        TimeoutSignal = pyqtSignal()

        def __init__(
            self,
            name: str = "timer",
            interval: int = 100,
            autostart: bool = False,
            timeout: int = 2000,
            parent=None,
        ):
            super().__init__(parent)
            self.setObjectName(name)
            self._timer = QTimer()
            self._interval = interval
            self._en = autostart
            self._timeout = timeout
            self._counter = 0
            self._timer.setInterval(interval)
            self._timer.timeout.connect(self._bump_counter)

            self._timer.start()

        @property
        def count(self) -> int:
            return self._counter

        @property
        def enabled(self) -> bool:
            return self._en

        def _bump_counter(self):
            if self._en:
                self._counter += self._interval
                self.CountSignal.emit(self._counter)
                if self._counter > self._timeout > 0:
                    self.TimeoutSignal.emit()

        @pyqtSlot(bool)
        def ToggleTimer(self, en: bool):
            self._en = en

        @pyqtSlot()
        def ClearCounter(self):
            self._counter = 0

    _instance = None
    _settings = None
    _settings_file = None

    @classmethod
    def get_instance(cls, filename: str = "settings.json", parent=None):
        if cls._instance is None:
            cls._settings_file = Path(filename)
            if not cls._settings_file.exists():
                cls._make_settings_file(cls._settings_file)
            cls._settings = cls._load_setting_file(cls._settings_file)
            cls._instance = cls(cls._settings, parent)
        return cls._instance

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)

        self._h_name = settings.host_name
        self._h_port = settings.host_port

        logging.debug(
            MqttClient.LOG_FMT_STR,
            f"Creating Client Instance: name: {settings.client_name} host: {self._h_name}:{self._h_port}",
        )

        self._client = Client(client_id=settings.client_name, protocol=MQTTv5)

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

    @property
    def connected(self):
        return self._client.is_connected()

    @classmethod
    def _make_settings_file(
        cls, file: Path, host_name: str = "localhost", host_port: int = 1883
    ):
    @pyqtSlot()
    def DisconnectBroker(self):
        if self.connected:
            logging.info(
                MqttClient.LOG_FMT_STR, f"Disconnecting from broker {self._h_name}"
            )
            err = self._client.disconnect()
            self._client.loop_stop()
            if err:
                logging.warning(
                    MqttClient.LOG_FMT_STR, f"Error disconnecting from broker: {err}"
                )
        else:
            logging.debug(MqttClient.LOG_FMT_STR, "Not connected anyways")

    @pyqtSlot()
    def ConnectBroker(self):
        if not self.connected:
            logging.info(
                MqttClient.LOG_FMT_STR,
                f"Connecting to broker w/ name: {self._h_name} on port: {self._h_port}",
            )
            err = self._client.connect(self._h_name, self._h_port, clean_start=True)
            if err:
                logging.warning(
                    MqttClient.LOG_FMT_STR, f"Error connecting to host:{err}"
                )
                return
            self._client.loop_start()
        else:
            logging.debug(MqttClient.LOG_FMT_STR, "Already connected")
        _setting = MqttClient.Settings()
        file.write_text(_setting.model_dump_json(indent=2))

    @classmethod
    def _load_setting_file(cls, file: Path):
        return MqttClient.Settings.model_validate(json.loads(file.read_text()))

    def _on_connect(self, client, userdata, flags, rc, props=None):
        logging.info(MqttClient.LOG_FMT_STR, "Connected to broker")
        self._sub_all_topcis()
        self.ConnectedSignal.emit(True)

    def _on_disconnect(self, client, userdata, rc, props=None):
        logging.warning(MqttClient.LOG_FMT_STR, "Disconnected from broker")
        self.ConnectedSignal.emit(False)

        if rc != 0:
            logging.info(MqttClient.LOG_FMT_STR, "Trying to reconnect")
            try:
                client.reconnect()
            except Exception as e:
                logging.warning(MqttClient.LOG_FMT_STR, f"Failed to reconnect - {e}")
                self.ConnectedSignal.emit(False)

    def _sub_all_topcis(self):
        logging.debug(MqttClient.LOG_FMT_STR, f"Subbing all topics")

    @pyqtSlot()
    def DisconnectBroker(self):
        if self.connected:
            logging.info(
                MqttClient.LOG_FMT_STR, f"Disconnecting from broker {self._h_name}"
            )
            err = self._client.disconnect()
            self._client.loop_stop()
            if err:
                logging.warning(
                    MqttClient.LOG_FMT_STR, f"Error disconnecting from broker: {err}"
                )
        else:
            logging.debug(MqttClient.LOG_FMT_STR, "Not connected anyways")

    @pyqtSlot()
    def ConnectBroker(self):
        if not self.connected:
            logging.info(
                MqttClient.LOG_FMT_STR,
                f"Connecting to broker w/ name: {self._h_name} on port: {self._h_port}",
            )
            err = self._client.connect(self._h_name, self._h_port, clean_start=True)
            if err:
                logging.warning(
                    MqttClient.LOG_FMT_STR, f"Error connecting to host:{err}"
                )
                return
            self._client.loop_start()
        else:
            logging.debug(MqttClient.LOG_FMT_STR, "Already connected")

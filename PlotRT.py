import sys, matplotlib, threading, datetime
import matplotlib.dates as mdates
import paho.mqtt.client as mqtt
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use("Qt5Agg")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creamos una figura y un objeto para el gráfico de línea
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("Temperatura")
        self.ax.set_title("Temperatura en Tiempo Real")

        # Creamos el lienzo de Matplotlib
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        # Creamos los botones
        self.start_button = QPushButton("Conectar")
        self.stop_button = QPushButton("Detener")

        # Creamos el layout de los botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # Creamos el layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(button_layout)

        # Creamos un widget central y le asignamos el layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Conectamos las señales de los botones
        self.start_button.clicked.connect(self.mq_connect)
        self.stop_button.clicked.connect(self.mq_disconnect)

    

        # Variables para almacenar los datos del gráfico
        self.xa = []
        self.ya = []
        self.xb = []
        self.yb = []
 

    def mq_connect(self):
        self.client = mqtt.Client()
        self.client.on_connect=self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker.emqx.io", 1883, 60)
        threading.Thread(target=self.client.loop_forever).start()

    def mq_disconnect(self):
        self.client.disconnect()
        self.xa=[]
        self.xb=[]
        self.ya=[]
        self.yb=[]


    def on_message(self, client, userdata, message):
        topic = str(message.topic)
        payload = str(message.payload.decode("utf-8"))

        print(payload)

        if topic == "sensor_a":
            self.ya.append(float(payload)*330/4096)
            self.xa.append(datetime.datetime.now())
        elif topic == "sensor_b":
            self.yb.append(float(payload)*330/4096)
            self.xb.append(datetime.datetime.now())
        
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.xa, self.ya, label="Interna")
        self.ax.plot(self.xb, self.yb, label="Externa")
        self.ax.legend()
        self.canvas.draw()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado al broker")
            client.subscribe("sensor_a",)
            client.subscribe("sensor_b",)
        else:
            print("Error de conexión. Código de retorno = ", rc)

    def closeEvent(self, event):
        print("Cerrando ciclos")
        self.client.disconnect()  # Cierra la conexión del cliente MQTT
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

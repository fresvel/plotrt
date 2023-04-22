import machine
import time
from umqtt.robust import MQTTClient
import network
# Configuración de los pines de los sensores
sensor1_pin = machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_UP)
sensor2_pin = machine.Pin(35, machine.Pin.IN, machine.Pin.PULL_UP)

# Configuración de conexión WiFi
wifi_ssid = 'VS CNT '
wifi_password = '1802589778'

# Configuración de conexión MQTT
mqtt_server = 'broker.emqx.io'
mqtt_port = 1883
mqtt_user = ''
mqtt_password = ''
mqtt_topic1 = b'sensor_a'
mqtt_topic2 = b'sensor_b'

# Función de conexión a WiFi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando a WiFi...')
        sta_if.active(True)
        sta_if.connect(wifi_ssid, wifi_password)
        while not sta_if.isconnected():
            pass
    print('WiFi conectado:', sta_if.ifconfig())

# Función de conexión a MQTT
def connect_mqtt():
    client = MQTTClient('esp32', mqtt_server, port=mqtt_port)
    client.connect()
    print('Connected to MQTT...')
    return client

# Función para leer los valores de los sensores
def read_sensors():
    #print('Sensores')
    adc = machine.ADC(machine.Pin(32))
    adc = machine.ADC(machine.Pin(33))
    s1=0
    s2=0
    for i in range(100):
        s1 =s1+ adc.read()
        s2 =s2+ adc.read()
    s1=s1/100
    s2=s2/100
    try:
        mqtt_client.publish(mqtt_topic1, str(s1))
        mqtt_client.publish(mqtt_topic2, str(s2))
    except Exception as e:
        print("Error en el envío de mensajes:", e)

# Conexión a WiFi
connect_wifi()

# Conexión a MQTT
print("Conectando a Broker")
mqtt_client = connect_mqtt()



# Loop principal
while True:
    # Leer los valores de los sensores
    read_sensors()
    print("Valor analógico")
    # Publicar los valores de los sensores en MQTT
    #mqtt_client.publish(mqtt_topic1, str(sensor1_value))
    #mqtt_client.publish(mqtt_topic2, str(sensor2_value))
    
    # Esperar un tiempo antes de volver a leer los sensores
    

from flask import Flask, jsonify, render_template
import things

app = Flask(__name__)

camera = things.CourtCamera(
    device_id=1,
    name="Камера корта",
    status="online",
    location="центр корта"
)

line_sensor = things.LineSensor(
    device_id=2,
    name="Датчик линии",
    status="online",
    location="боковая линия"
)

net_sensor = things.NetSensor(
    device_id=3,
    name="Датчик сетки",
    status="online",
    location="сетка"
)
scoreboard = things.Scoreboard(
    device_id=4,
    name="Электронное табло",
    status="online",
    location="центральная зона корта"
)
speaker = things.Speaker(
    device_id=5,
    name="Звуковая система",
    status="online",
    location="зона судьи"
)

# Лаба 2
@app.route("/")
def index():
    return render_template("index.html")

# Лаба 3
@app.route("/connect_camera")
def connect_camera():
    data = camera.connect()
    return jsonify(data)


@app.route("/connect_line_sensor")
def connect_line_sensor():
    data = line_sensor.connect()
    return jsonify(data)


@app.route("/connect_net_sensor")
def connect_net_sensor():
    data = net_sensor.connect()
    return jsonify(data)

# Лаба 4



if __name__ == "__main__":
    app.run(debug=True)
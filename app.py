from flask import Flask, jsonify, render_template, request
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

controller = things.MainController()

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
@app.route("/connect_scoreboard")
def connect_scoreboard():
    data = scoreboard.connect()
    return jsonify(data)

@app.route("/connect_speaker")
def connect_speaker():
    data = speaker.connect()
    return jsonify(data)

devices = {
    "camera": camera,
    "line_sensor": line_sensor,
    "net_sensor": net_sensor,
    "scoreboard": scoreboard,
    "speaker": speaker
}

# Изменение статуса указанного устройства
@app.route("/set_status")
def set_status():
    device_name = request.args.get("device")
    new_status = request.args.get("status")

    if device_name not in devices:
        return jsonify({
            "result": "error",
            "message": f"Устройство '{device_name}' не найдено"
        })
    if new_status is None:
        return jsonify({
            "result": "error",
            "message": "Не передан новый статус устройства"
        })
    result = devices[device_name].set_status(new_status)
    return jsonify(result)

# Воспроизведение сигнала через динамики
@app.route("/control_speaker")
def control_speaker():
    command = request.args.get("command")

    if command == "play_signal":
        sound_type = request.args.get("sound_type", "signal")
        duration = request.args.get("duration", 3)

        result = speaker.play_signal(sound_type, duration)
        return jsonify(result)

    if command == "set_volume":
        volume = request.args.get("volume", 70)

        result = speaker.set_volume(volume)
        return jsonify(result)

    return jsonify({
        "result": "error",
        "message": f"Неизвестная команда для звуковой системы: {command}"
    })

# Изменения показаний табло
@app.route("/control_scoreboard")
def control_scoreboard():
    command = request.args.get("command")

    if command == "update_score":
        score_type = request.args.get("score_type")
        player1_score = request.args.get("player1_score", 0)
        player2_score = request.args.get("player2_score", 0)

        result = scoreboard.update_score(score_type, player1_score, player2_score)
        return jsonify(result)

    if command == "set_match_status":
        match_status = request.args.get("match_status", "not started")

        result = scoreboard.set_match_status(match_status)
        return jsonify(result)

    if command == "reset_score":
        result = scoreboard.reset_score()
        return jsonify(result)

    return jsonify({
        "result": "error",
        "message": f"Неизвестная команда для табло: {command}"
    })

# Автоматизация
@app.route("/auto_rally")
def auto_rally():
    result = controller.process_auto_rally(
        camera,
        line_sensor,
        net_sensor,
        scoreboard,
        speaker
    )

    return jsonify(result)
if __name__ == "__main__":
    app.run(debug=True)
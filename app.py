from flask import Flask, jsonify, render_template, request
import things
import database

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

logger = database.DatabaseLogger()

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
        result = {
            "result": "error",
            "message": f"Устройство '{device_name}' не найдено"
        }
        logger.save_control_log({
            "device": device_name,
            "command": "set_status",
            "new_status": new_status,
            "result": result.get("result"),
            "message": result.get("message")
        })
        return jsonify(result)
    if new_status is None:
        result = {
            "result": "error",
            "message": "Не передан новый статус устройства"
        }
        logger.save_control_log({
            "device": device_name,
            "command": "set_status",
            "new_status": new_status,
            "result": result.get("result"),
            "message": result.get("message")
        })
        return jsonify(result)

    result = devices[device_name].set_status(new_status)
    logger.save_control_log({
        "device": device_name,
        "command": "set_status",
        "new_status": new_status,
        "result": result.get("result"),
        "message": result.get("message"),
        "response": result
    })
    return jsonify(result)

# Воспроизведение сигнала через динамики
@app.route("/control_speaker")
def control_speaker():
    command = request.args.get("command")

    if command == "play_signal":
        sound_type = request.args.get("sound_type", "signal")
        duration = request.args.get("duration", 3)

        result = speaker.play_signal(sound_type, duration)
        logger.save_control_log({
            "device": "speaker",
            "command": command,
            "sound_type": sound_type,
            "duration": duration,
            "result": result.get("result"),
            "message": result.get("message"),
            "response": result
        })
        return jsonify(result)

    if command == "set_volume":
        volume = request.args.get("volume", 70)

        result = speaker.set_volume(volume)
        logger.save_control_log({
            "device": "speaker",
            "command": command,
            "volume": volume,
            "result": result.get("result"),
            "message": result.get("message"),
            "response": result
        })
        return jsonify(result)

    result = {
        "result": "error",
        "message": f"Неизвестная команда для звуковой системы: {command}"
    }

    logger.save_control_log({
        "device": "speaker",
        "command": command,
        "result": result.get("result"),
        "message": result.get("message")
    })

    return jsonify(result)

# Изменения показаний табло
@app.route("/control_scoreboard")
def control_scoreboard():
    command = request.args.get("command")

    if command == "update_score":
        score_type = request.args.get("score_type")
        player1_score = request.args.get("player1_score", 0)
        player2_score = request.args.get("player2_score", 0)

        result = scoreboard.update_score(score_type, player1_score, player2_score)
        logger.save_control_log({
            "device": "scoreboard",
            "command": command,
            "score_type": score_type,
            "player1_score": player1_score,
            "player2_score": player2_score,
            "result": result.get("result"),
            "message": result.get("message"),
            "response": result
        })
        return jsonify(result)

    if command == "set_match_status":
        match_status = request.args.get("match_status", "not started")

        result = scoreboard.set_match_status(match_status)
        logger.save_control_log({
            "device": "scoreboard",
            "command": command,
            "match_status": match_status,
            "result": result.get("result"),
            "message": result.get("message"),
            "response": result
        })
        return jsonify(result)

    if command == "reset_score":
        result = scoreboard.reset_score()
        logger.save_control_log({
            "device": "scoreboard",
            "command": command,
            "result": result.get("result"),
            "message": result.get("message"),
            "response": result
        })
        return jsonify(result)

    result = {
        "result": "error",
        "message": f"Неизвестная команда для табло: {command}"
    }

    logger.save_control_log({
        "device": "scoreboard",
        "command": command,
        "result": result.get("result"),
        "message": result.get("message")
    })

    return jsonify(result)

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
    logger.save_auto_event(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
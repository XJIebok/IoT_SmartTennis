from flask import Flask
import things

app = Flask(__name__)


@app.route("/")
def index():
    print("Главная страница открыта")
    # Создание экземпляров классов
    camera = things.CourtCamera("Камера корта", "online", "центр корта")
    line_sensor = things.LineSensor("Датчик линии", "online", "боковая линия")
    net_sensor = things.NetSensor("Датчик сетки", "online", "сетка")
    scoreboard = things.Scoreboard("Электронное табло", "online")
    speaker = things.Speaker("Звуковая система", "online")
    database = things.Database()
    controller = things.MainController("Главный контроллер", "online")

    player1 = things.Player("Игрок 1", "left")
    player2 = things.Player("Игрок 2", "right")

    # Запуск методов для созданных экземпляляров
    camera.connect()
    camera.track_ball()
    camera.detect_bounce_point()
    camera.send_data()

    line_sensor.connect()
    line_sensor.detect_impact()
    line_sensor.detect_in_out()
    line_sensor.send_data()

    net_sensor.connect()
    net_sensor.detect_vibration()
    net_sensor.detect_net_contact()
    net_sensor.send_data()

    controller.connect()
    controller.receive_data()
    controller.process_event()
    controller.update_scoreboard()
    controller.control_speaker()
    controller.save_event()
    controller.change_sides()

    scoreboard.connect()
    scoreboard.update_points()
    scoreboard.update_games()
    scoreboard.update_sets()
    scoreboard.display_score()

    speaker.connect()
    speaker.play_signal()
    speaker.announce_event()

    database.save_event()
    database.save_score()
    database.get_history()

    player1.add_point()
    player1.change_side()
    player2.change_side()

    return "Методы классов системы умного теннисного корта были запущены. Проверьте лог сервера."


if __name__ == "__main__":
    app.run(debug=True)
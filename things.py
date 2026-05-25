import random
import re
from abc import ABC, abstractmethod

# Абстрактный класс вещи
class Thing(ABC):
    def __init__(self, device_id: int, name: str, status: str):
        self.id = device_id
        self.name = name
        self.status = status
        print(f"Создан объект Thing: id={self.id}, name={self.name}, status={self.status}")

    def get_info(self):
        # print(f"{self.name}: метод get_info() запущен")
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }
    # Изменение статуса Вещи
    def set_status(self, status):
        allowed_statuses = ["online", "offline", "maintenance"]
        try:
            new_status = str(status).strip().lower()

            if new_status not in allowed_statuses:
                raise ValueError

            self.status = new_status

            print(f"{self.name}: статус изменён на {self.status}")

            return {
                "result": "success",
                "message": f"Статус изменён на {self.status}",
                "thing": self.get_info()
            }

        except ValueError:
            print(f"{self.name}: ошибка изменения статуса. Недопустимый статус: {status}")
            return {
                "result": "error",
                "message": f"Недопустимый статус: {status}. Допустимые значения: online, offline, maintenance",
                "thing": self.get_info()
            }
        except Exception as error:
            print(f"{self.name}: непредвиденная ошибка при изменении статуса: {error}")

            return {
                "result": "error",
                "message": "Ошибка при изменении статуса устройства",
                "thing": self.get_info()
            }

    @abstractmethod
    def connect(self):
        pass # print(f"{self.name}: подключение начато")

# Класс Сенсора
class Sensor(Thing):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status)
        self.location = location
        self.last_value = None
        print(f"Создан датчик Sensor: {self.name}, location={self.location}")

    # Метод, в котором генерируется и отправляются данные с датчика
    def connect(self):
        super().connect()
        # Если статус не "онлайн", то генерироваться показатели не будут
        if self.status != "online":
            print(f"{self.name}: датчик не активен, текущий статус: {self.status}")
            return self.send_data()

        # print(f"{self.name}: датчик подключен")
        self.detect_event()
        return self.send_data()
    # Метод, генерирующий все данные для датчиков
    @abstractmethod
    def detect_event(self):
        pass
    # Метод, отправляющий данные с датчика
    def send_data(self):
        # print(f"{self.name}: метод send_data() запущен\n")
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "location": self.location,
            "last_value": self.last_value
        }

# Класс Камеры корта
class CourtCamera(Sensor):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status, location)

        self.frame_id = 0
        self.hit_type = "none"
        self.hit_coordinate = None
        self.ball_speed = 0
        self.confidence = 0.0

        self.next_hit_type = "racket"
        self.last_racket_side = None

        print(f"Создан CourtCamera: {self.name}")

    def capture_frame(self):
        self.frame_id += 1
        print(f"{self.name}: метод capture_frame() запущен, frame_id={self.frame_id}")

    def detect_ball_event(self):
        if self.next_hit_type == "racket":
            self.generate_racket_hit()
            self.next_hit_type = "bounce"
        else:
            self.generate_bounce()
            self.next_hit_type = "racket"

        self.ball_speed = random.randint(60, 160)
        self.confidence = round(random.uniform(0.75, 0.99), 2)

        self.last_value = f"{self.hit_type}: {self.hit_coordinate}"

        print(
            f"{self.name}: метод detect_ball_event() запущен. "
            f"Тип события: {self.hit_type}, "
            f"координата: {self.hit_coordinate}, "
            f"скорость: {self.ball_speed}, "
            f"уверенность: {self.confidence}"
        )

    def generate_racket_hit(self):
        self.hit_type = "racket"

        if self.last_racket_side == "left":
            side = "right"
        elif self.last_racket_side == "right":
            side = "left"
        else:
            side = random.choice(["left", "right"])

        self.last_racket_side = side

        if side == "left":
            x = round(random.uniform(-42.0, -37.0), 2)
        else:
            x = round(random.uniform(37.0, 42.0), 2)

        y = round(random.uniform(-10.0, 10.0), 2)

        self.hit_coordinate = [x, y]

    def generate_bounce(self):
        self.hit_type = "bounce"

        if self.last_racket_side == "left":
            target_side = "right"
        else:
            target_side = "left"

        event_type = random.choices(
            ["in", "out", "line"],
            weights=[70, 20, 10],
            k=1
        )[0]

        if target_side == "right":
            if event_type == "in":
                x = round(random.uniform(5.0, 38.0), 2)
            elif event_type == "line":
                x = round(random.uniform(38.7, 39.2), 2)
            else:
                x = round(random.uniform(39.5, 45.0), 2)
        else:
            if event_type == "in":
                x = round(random.uniform(-38.0, -5.0), 2)
            elif event_type == "line":
                x = round(random.uniform(-39.2, -38.7), 2)
            else:
                x = round(random.uniform(-45.0, -39.5), 2)

        if event_type == "out" and random.choice([True, False]):
            y = round(random.choice([
                random.uniform(-18.0, -14.0),
                random.uniform(14.0, 18.0)
            ]), 2)
        else:
            y = round(random.uniform(-13.0, 13.0), 2)

        self.hit_coordinate = [x, y]

    def detect_event(self):
        print(f"{self.name}: метод detect_event() запущен")
        self.capture_frame()
        self.detect_ball_event()

    def send_data(self):
        data = super().send_data()
        data.update({
            "frame_id": self.frame_id,
            "hit_type": self.hit_type,
            "hit_coordinate": self.hit_coordinate,
            "ball_speed": self.ball_speed,
            "confidence": self.confidence
        })
        return data

# Класс Лазерного сенсора по периметру корта
class LineSensor(Sensor):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status, location)
        self.line_type = "side line"
        self.triggered = False
        self.impact_coordinate = None
        self.signal_strength = 0.0
        print(f"Создан LineSensor: {self.name}")
    # Генерация, попал ли мяч на линию поля
    def detect_impact(self):
        self.triggered = random.choice([True, False])

        if self.triggered:
            self.impact_coordinate = (
                random.randint(0, 100),
                random.randint(0, 50)
            )
            self.signal_strength = round(random.uniform(0.1, 10.0), 2)
        else:
            self.impact_coordinate = None
            self.signal_strength = 0.0

        self.last_value = str(self.impact_coordinate)
        print(
            f"{self.name}: метод detect_impact() запущен. "
            f"Срабатывание: {self.triggered}, "
            f"координата: {self.impact_coordinate}, "
            f"сила сигнала: {self.signal_strength}"
        )

    def detect_event(self):
        print(f"{self.name}: метод detect_event() запущен")
        self.detect_impact()

    def send_data(self):
        data = super().send_data()
        data.update({
            "line_type": self.line_type,
            "triggered": self.triggered,
            "impact_coordinate": self.impact_coordinate,
            "signal_strength": self.signal_strength
        })
        return data

# Класс Сенсора натяжения сетки
class NetSensor(Sensor):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status, location)
        self.tension_level = 0.0
        self.vibration_level = 0.0
        self.net_contact = False
        print(f"Создан NetSensor: {self.name}")
    # Генерация вибрации сетки
    def detect_vibration(self):
        self.tension_level = round(random.uniform(40.0, 60.0), 2)
        self.vibration_level = round(random.uniform(0.0, 10.0), 2)

        print(
            f"{self.name}: метод detect_vibration() запущен. "
            f"Натяжение: {self.tension_level}, "
            f"вибрация: {self.vibration_level}"
        )
    # Получение касания сетки
    def detect_net_contact(self):
        self.net_contact = self.vibration_level > 6.5
        self.last_value = str(self.net_contact)

        print(
            f"{self.name}: метод detect_net_contact() запущен. "
            f"Касание сетки: {self.net_contact}"
        )

    def detect_event(self):
        print(f"{self.name}: метод detect_event() запущен")
        self.detect_vibration()
        self.detect_net_contact()

    def send_data(self):
        data = super().send_data()
        data.update({
            "tension_level": self.tension_level,
            "vibration_level": self.vibration_level,
            "net_contact": self.net_contact
        })
        return data


# Класс Динамиков
class Speaker(Thing):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status)
        self.location = location
        self.volume = 70
        print(f"Создан Speaker: {self.name}")

    def connect(self):
        super().connect()
        print(f"{self.name}: данные звуковой системы переданы")
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "location": self.location,
            "volume": self.volume
        }

    def play_signal(self, sound_type, duration):
        allowed_sound_types = ["match_start", "set_end", "fault", "warning"]

        try:
            if self.status != "online":
                return {
                    "result": "error",
                    "message": f"{self.name}: устройство недоступно, текущий статус: {self.status}",
                    "speaker": self.connect()
                }

            sound_type = str(sound_type).strip().lower()

            if not re.fullmatch(r"^[a-z_]+$", sound_type):
                raise ValueError("Некорректный формат типа сигнала")

            if sound_type not in allowed_sound_types:
                raise ValueError("Недопустимый тип сигнала")

            duration = int(duration)
            if duration < 1 or duration > 10:
                raise ValueError("Длительность сигнала должна быть от 1 до 10 секунд")

            print(
                f"{self.name}: метод play_signal() запущен. "
                f"Тип сигнала: {sound_type}, "
                f"длительность: {duration} секунд, "
                f"громкость: {self.volume}"
            )
            return {
                "result": "success",
                "message": f"Сигнал '{sound_type}' запущен на {duration} секунд",
                "sound_type": sound_type,
                "duration": duration,
                "volume": self.volume,
                "speaker": self.connect()
            }

        except ValueError as error:
            print(f"{self.name}: ошибка запуска сигнала. {error}")
            return {
                "result": "error",
                "message": f"Ошибка запуска сигнала: {error}",
                "speaker": self.connect()
            }

        except Exception as error:
            print(f"{self.name}: непредвиденная ошибка при запуске сигнала: {error}")
            return {
                "result": "error",
                "message": "Непредвиденная ошибка при запуске сигнала",
                "speaker": self.connect()
            }

    def set_volume(self, volume):
        try:
            if self.status != "online":
                return {
                    "result": "error",
                    "message": f"{self.name}: устройство недоступно, текущий статус: {self.status}",
                    "speaker": self.connect()
                }

            volume = int(volume)
            if volume < 0 or volume > 100:
                raise ValueError("Громкость должна быть в диапазоне от 0 до 100")

            self.volume = volume

            print(
                f"{self.name}: метод set_volume() запущен. "
                f"Новая громкость: {self.volume}"
            )
            return {
                "result": "success",
                "message": f"Громкость изменена на {volume}",
                "speaker": self.connect()
            }

        except ValueError as error:
            print(f"{self.name}: ошибка изменения громкости. {error}")
            return {
                "result": "error",
                "message": f"Ошибка изменения громкости: {error}",
                "speaker": self.connect()
            }

        except Exception as error:
            print(f"{self.name}: непредвиденная ошибка при изменении громкости: {error}")
            return {
                "result": "error",
                "message": "Непредвиденная ошибка при изменении громкости",
                "speaker": self.connect()
            }

# Класс для Табло со счётом
class Scoreboard(Thing):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status)
        self.location = location
        self.score = {
            "points": [0, 0],
            "games": [0, 0],
            "sets": [0, 0]
        }
        self.match_status = "not started"
        print(f"Создано табло Scoreboard: {self.name}")

    def connect(self):
        super().connect()
        print(f"{self.name}: данные табло переданы")
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "location": self.location,
            "score": self.score,
            "match_status": self.match_status
        }

    def update_score(self, score_type, player1_score, player2_score):
        score_types = {
            "sets": "сеты",
            "games": "геймы",
            "points": "очки"
        }

        try:
            if self.status != "online":
                return {
                    "result": "error",
                    "message": f"{self.name}: устройство недоступно, текущий статус: {self.status}",
                    "scoreboard": self.connect()
                }

            score_type = str(score_type).strip().lower()

            if score_type not in score_types:
                raise ValueError(f"Недопустимый тип счёта: {score_type}")

            player1_score = int(player1_score)
            player2_score = int(player2_score)

            if player1_score < 0 or player2_score < 0:
                raise ValueError("Значения счёта не могут быть отрицательными")

            self.score[score_type] = [player1_score, player2_score]

            print(
                f"{self.name}: {score_types[score_type]} обновлены: "
                f"{self.score[score_type]}"
            )
            return {
                "result": "success",
                "message": f"{score_types[score_type]} обновлены",
                "scoreboard": self.connect()
            }

        except ValueError as error:
            print(f"{self.name}: ошибка обновления счёта. {error}")
            return {
                "result": "error",
                "message": f"Ошибка обновления счёта: {error}",
                "scoreboard": self.connect()
            }

        except Exception as error:
            print(f"{self.name}: непредвиденная ошибка при обновлении счёта: {error}")
            return {
                "result": "error",
                "message": "Непредвиденная ошибка при обновлении счёта",
                "scoreboard": self.connect()
            }

    def set_match_status(self, match_status):
        allowed_statuses = ["not started", "in progress", "paused", "finished"]

        try:
            if self.status != "online":
                return {
                    "result": "error",
                    "message": f"{self.name}: устройство недоступно, текущий статус: {self.status}",
                    "scoreboard": self.connect()
                }

            match_status = str(match_status).strip().lower()

            if match_status not in allowed_statuses:
                raise ValueError(f"Недопустимый статус матча: {match_status}")

            self.match_status = match_status

            print(
                f"{self.name}: метод set_match_status() запущен. "
                f"Статус матча: {self.match_status}"
            )
            return {
                "result": "success",
                "message": f"Статус матча изменён на {match_status}",
                "scoreboard": self.connect()
            }

        except ValueError as error:
            print(f"{self.name}: ошибка изменения статуса матча. {error}")
            return {
                "result": "error",
                "message": f"Ошибка изменения статуса матча: {error}",
                "scoreboard": self.connect()
            }

        except Exception as error:
            print(f"{self.name}: непредвиденная ошибка при изменении статуса матча: {error}")
            return {
                "result": "error",
                "message": "Непредвиденная ошибка при изменении статуса матча",
                "scoreboard": self.connect()
            }

    def reset_score(self):
        try:
            if self.status != "online":
                return {
                    "result": "error",
                    "message": f"{self.name}: устройство недоступно, текущий статус: {self.status}",
                    "scoreboard": self.connect()
                }

            self.score = {
                "points": [0, 0],
                "games": [0, 0],
                "sets": [0, 0]
            }
            self.match_status = "not started"

            print(f"{self.name}: метод reset_score() запущен. Счёт сброшен")
            return {
                "result": "success",
                "message": "Счёт сброшен",
                "scoreboard": self.connect()
            }

        except Exception as error:
            print(f"{self.name}: непредвиденная ошибка при сбросе счёта: {error}")
            return {
                "result": "error",
                "message": "Непредвиденная ошибка при сбросе счёта",
                "scoreboard": self.connect()
            }

# Класс Игрока
class Player:
    def __init__(self, name: str, side: str):
        self.name = name
        self.side = side
        self.points = 0
        self.games = 0
        self.sets = 0
        print(f"Создан игрок: {self.name}, сторона: {self.side}")

    def add_point(self):
        print(f"{self.name}: метод add_point() запущен")

    def win_game(self):
        print(f"{self.name}: метод win_game() запущен")

    def win_set(self):
        print(f"{self.name}: метод win_set() запущен")

    def change_side(self):
        print(f"{self.name}: метод change_side() запущен")

    def reset_points(self):
        print(f"{self.name}: метод reset_points() запущен")

# Класс Базы данных
class Database:
    def __init__(self):
        self.match_events = []
        self.score_history = []
        self.system_logs = []
        print("Создан объект Database")

    def save_event(self):
        print("Database: метод save_event() запущен")

    def save_score(self):
        print("Database: метод save_score() запущен")

    def get_history(self):
        print("Database: метод get_history() запущен")

# Класс Главного конроллера
class MainController:
    def __init__(self):
        self.match_status = "in progress"
        self.current_set = 1
        self.current_game = 1
        self.last_event = "none"
        self.last_hit_player = None

        self.player_sides = {
            1: "left",
            2: "right"
        }

        self.court_x_limit = 39.0
        self.court_y_limit = 13.5

        print("Создан MainController")

    def get_state(self):
        return {
            "match_status": self.match_status,
            "current_set": self.current_set,
            "current_game": self.current_game,
            "player_sides": self.player_sides,
            "last_hit_player": self.last_hit_player,
            "last_event": self.last_event
        }

    # Определения игрока по координатам с датчика камеры и события отбития ракеткой
    def get_player_by_coordinate(self, coordinate):
        x = coordinate[0]

        event_side = "left" if x < 0 else "right"

        for player_number, side in self.player_sides.items():
            if side == event_side:
                return player_number

        return None

    def get_opponent(self, player_number):
        if player_number == 1:
            return 2
        if player_number == 2:
            return 1
        return None

    # Находятся ли полученные координаты датчика внутри корта
    def is_coordinate_inside_court(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]

        return (
            -self.court_x_limit <= x <= self.court_x_limit and
            -self.court_y_limit <= y <= self.court_y_limit
        )

    def is_near_line(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]

        x_near_line = abs(abs(x) - self.court_x_limit) <= 0.5
        y_near_line = abs(abs(y) - self.court_y_limit) <= 0.5

        return x_near_line or y_near_line

    def add_point_to_player(self, player_number, scoreboard):
        if player_number is None:
            return {
                "result": "error",
                "message": "Не удалось определить игрока для начисления очка"
            }

        current_points = scoreboard.score["points"]

        if player_number == 1:
            current_points[0] += 1
        else:
            current_points[1] += 1

        return scoreboard.update_score(
            "points",
            current_points[0],
            current_points[1]
        )

    def sync_line_sensor(self, camera_data, line_sensor):
        if line_sensor.status != "online":
            line_sensor.triggered = False
            line_sensor.impact_coordinate = None
            line_sensor.signal_strength = 0.0
            return

        if camera_data["hit_type"] != "bounce":
            line_sensor.triggered = False
            line_sensor.impact_coordinate = None
            line_sensor.signal_strength = 0.0
            return

        coordinate = camera_data["hit_coordinate"]

        if self.is_near_line(coordinate):
            line_sensor.triggered = True
            line_sensor.impact_coordinate = coordinate
            line_sensor.signal_strength = round(random.uniform(5.0, 10.0), 2)
        else:
            line_sensor.triggered = False
            line_sensor.impact_coordinate = None
            line_sensor.signal_strength = 0.0

        line_sensor.last_value = str(line_sensor.impact_coordinate)

    def sync_net_sensor(self, camera_data, net_sensor):
        if net_sensor.status != "online":
            net_sensor.tension_level = 0.0
            net_sensor.vibration_level = 0.0
            net_sensor.net_contact = False
            return

        if camera_data["hit_type"] == "racket":
            net_contact = random.choices(
                [True, False],
                weights=[15, 85],
                k=1
            )[0]

            net_sensor.net_contact = net_contact
            net_sensor.tension_level = round(random.uniform(40.0, 60.0), 2)

            if net_contact:
                net_sensor.vibration_level = round(random.uniform(7.0, 10.0), 2)
            else:
                net_sensor.vibration_level = round(random.uniform(0.0, 4.0), 2)
        else:
            net_sensor.net_contact = False
            net_sensor.tension_level = round(random.uniform(40.0, 60.0), 2)
            net_sensor.vibration_level = round(random.uniform(0.0, 3.0), 2)

        net_sensor.last_value = str(net_sensor.net_contact)

    def process_auto_rally(self, camera, line_sensor, net_sensor, scoreboard, speaker):

        camera_data = camera.connect()

        if camera.status != "online":
            self.last_event = "camera unavailable"
            return {
                "result": "error",
                "message": "Камера недоступна, автоматическая обработка невозможна",
                "controller": self.get_state(),
                "camera": camera_data
            }

        self.sync_line_sensor(camera_data, line_sensor)
        self.sync_net_sensor(camera_data, net_sensor)

        hit_type = camera_data["hit_type"]
        coordinate = camera_data["hit_coordinate"]

        scoreboard_result = None
        speaker_result = None
        point_to = None

        if hit_type == "racket":
            self.last_hit_player = self.get_player_by_coordinate(coordinate)
            self.last_event = f"racket hit by player {self.last_hit_player}"

            if net_sensor.net_contact:
                point_to = self.get_opponent(self.last_hit_player)
                self.last_event = f"net fault, point to player {point_to}"

                scoreboard_result = self.add_point_to_player(point_to, scoreboard)
                speaker_result = speaker.play_signal("fault", 2)

        elif hit_type == "bounce":
            inside_court = self.is_coordinate_inside_court(coordinate)

            if inside_court or line_sensor.triggered:
                self.last_event = "ball in court"
            else:
                point_to = self.get_opponent(self.last_hit_player)
                self.last_event = f"out, point to player {point_to}"

                scoreboard_result = self.add_point_to_player(point_to, scoreboard)
                speaker_result = speaker.play_signal("fault", 2)

        else:
            self.last_event = "unknown ball event"

        print(f"Главный контроллер: автоматическая обработка выполнена. Событие: {self.last_event}")

        return {
            "result": "success",
            "message": "Автоматическая обработка розыгрыша выполнена",
            "event": self.last_event,
            "point_to": point_to,
            "camera": camera_data,
            "line_sensor": line_sensor.send_data(),
            "net_sensor": net_sensor.send_data(),
            "scoreboard": scoreboard.connect(),
            "speaker": speaker.connect(),
            "scoreboard_result": scoreboard_result,
            "speaker_result": speaker_result,
            "controller": self.get_state()
        }
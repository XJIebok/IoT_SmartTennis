import random

from abc import ABC, abstractmethod

# Абстрактный класс объекта
class Thing(ABC):
    def __init__(self, device_id: int, name: str, status: str):
        self.id = device_id
        self.name = name
        self.status = status
        print(f"Создан объект Thing: id={self.id}, name={self.name}, status={self.status}")

    def get_info(self):
        print(f"{self.name}: метод get_info() запущен")
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }

    @abstractmethod
    def connect(self):
        print(f"{self.name}: подключение начато")

# Класс Сенсора
class Sensor(Thing):
    def __init__(self, device_id: int, name: str, status: str, location: str):
        super().__init__(device_id, name, status)
        self.location = location
        self.last_value = None
        print(f"Создан датчик Sensor: {self.name}, location={self.location}")

    def connect(self):
        super().connect()
        print(f"{self.name}: датчик подключен")
        self.detect_event()
        return self.send_data()

    @abstractmethod
    def detect_event(self):
        pass

    def send_data(self):
        print(f"{self.name}: метод send_data() запущен")
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
        self.screen_ball_position = None
        self.is_ball_detected = False
        print(f"Создан CourtCamera: {self.name}")

    def capture_frame(self):
        self.frame_id += 1
        print(f"{self.name}: метод capture_frame() запущен, frame_id={self.frame_id}")

    def detect_ball_on_frame(self):
        self.is_ball_detected = random.choice([True, False])

        if self.is_ball_detected:
            self.screen_ball_position = (
                random.randint(0, 1920),
                random.randint(0, 1080)
            )
        else:
            self.screen_ball_position = None

        self.last_value = str(self.screen_ball_position)
        print(
            f"{self.name}: метод detect_ball_on_frame() запущен. "
            f"Мяч обнаружен: {self.is_ball_detected}, "
            f"позиция на экране: {self.screen_ball_position}"
        )

    def detect_event(self):
        print(f"{self.name}: метод detect_event() запущен")
        self.capture_frame()
        self.detect_ball_on_frame()

    def send_data(self):
        data = super().send_data()
        data.update({
            "frame_id": self.frame_id,
            "screen_ball_position": self.screen_ball_position,
            "is_ball_detected": self.is_ball_detected
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

    def detect_vibration(self):
        self.tension_level = round(random.uniform(40.0, 60.0), 2)
        self.vibration_level = round(random.uniform(0.0, 10.0), 2)

        print(
            f"{self.name}: метод detect_vibration() запущен. "
            f"Натяжение: {self.tension_level}, "
            f"вибрация: {self.vibration_level}"
        )

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

# Класс для Табло со счётом
class Scoreboard(Thing):
    def __init__(self, device_id: int, name: str, status: str):
        super().__init__(device_id, name, status)
        self.player1_points = 0
        self.player2_points = 0
        self.player1_games = 0
        self.player2_games = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.match_status = "not started"
        print(f"Создано табло Scoreboard: {self.name}")

    def connect(self):
        super().connect()
        print(f"{self.name}: табло подключено")

    def update_points(self):
        print(f"{self.name}: метод update_points() запущен")

    def update_games(self):
        print(f"{self.name}: метод update_games() запущен")

    def update_sets(self):
        print(f"{self.name}: метод update_sets() запущен")

    def display_score(self):
        print(f"{self.name}: метод display_score() запущен")

    def reset_game_points(self):
        print(f"{self.name}: метод reset_game_points() запущен")

# Класс Динамиков
class Speaker(Thing):
    def __init__(self, device_id: int, name: str, status: str):
        super().__init__(device_id, name, status)
        self.volume = 70
        self.sound_type = "signal"
        self.is_active = False
        print(f"Создан Speaker: {self.name}")

    def connect(self):
        super().connect()
        print(f"{self.name}: звуковая система подключена")

    def play_signal(self):
        print(f"{self.name}: метод play_signal() запущен")

    def announce_event(self):
        print(f"{self.name}: метод announce_event() запущен")

    def stop_signal(self):
        print(f"{self.name}: метод stop_signal() запущен")

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
class MainController(Thing):
    def __init__(self, device_id: int, name: str, status: str):
        super().__init__(device_id, name, status)
        self.match_status = "waiting"
        self.current_set = 1
        self.current_game = 1
        self.last_event = None
        print(f"Создан MainController: {self.name}")

    def connect(self):
        super().connect()
        print(f"{self.name}: главный контроллер подключен")

    def receive_data(self):
        print(f"{self.name}: метод receive_data() запущен")

    def process_event(self):
        print(f"{self.name}: метод process_event() запущен")

    def update_scoreboard(self):
        print(f"{self.name}: метод update_scoreboard() запущен")

    def control_speaker(self):
        print(f"{self.name}: метод control_speaker() запущен")

    def save_event(self):
        print(f"{self.name}: метод save_event() запущен")

    def change_sides(self):
        print(f"{self.name}: метод change_sides() запущен")

    def end_set(self):
        print(f"{self.name}: метод end_set() запущен")
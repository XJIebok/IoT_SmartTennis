from abc import ABC, abstractmethod

# Абстрактный класс объекта
class Thing(ABC):
    def __init__(self, name: str, status: str):
        self.name = name
        self.status = status
        print(f"Создан объект Thing: {self.name}, статус: {self.status}")
    # Абстрактный метод подключения объекта
    @abstractmethod
    def connect(self):
        print(f"{self.name}: подключение выполнено")

# Класс Сенсора
class Sensor(Thing):
    def __init__(self, name: str, status: str, location: str):
        super().__init__(name, status)
        self.location = location
        self.last_value = None
        print(f"Создан датчик Sensor: {self.name}, расположение: {self.location}")

    def connect(self):
        super().connect()
        print(f"{self.name}: датчик подключен")

    def detect_event(self):
        print(f"{self.name}: метод detect_event() запущен")

    def send_data(self):
        print(f"{self.name}: метод send_data() запущен")

# Класс Датчика качания сетки
class NetSensor(Sensor):
    def __init__(self, name: str, status: str, location: str):
        super().__init__(name, status, location)
        self.tension_level = 0.0
        self.vibration_level = 0.0
        self.net_contact = False
        print(f"Создан NetSensor: {self.name}")

    def detect_vibration(self):
        print(f"{self.name}: метод detect_vibration() запущен")

    def detect_net_contact(self):
        print(f"{self.name}: метод detect_net_contact() запущен")

# Класс Камеры корта для отслеживания мяча
class CourtCamera(Sensor):
    def __init__(self, name: str, status: str, location: str):
        super().__init__(name, status, location)
        self.resolution = "1920x1080"
        self.fps = 60
        self.ball_position = None
        self.bounce_point = None
        print(f"Создан CourtCamera: {self.name}")

    def track_ball(self):
        print(f"{self.name}: метод track_ball() запущен")

    def detect_bounce_point(self):
        print(f"{self.name}: метод detect_bounce_point() запущен")

# Класс датчика разметки игрового поля
class LineSensor(Sensor):
    def __init__(self, name: str, status: str, location: str):
        super().__init__(name, status, location)
        self.line_type = "side line"
        self.triggered = False
        self.impact_position = None
        print(f"Создан LineSensor: {self.name}")

    def detect_impact(self):
        print(f"{self.name}: метод detect_impact() запущен")

    def detect_in_out(self):
        print(f"{self.name}: метод detect_in_out() запущен")

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
    def __init__(self, name: str, status: str):
        super().__init__(name, status)
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
    def __init__(self, name: str, status: str):
        super().__init__(name, status)
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
    def __init__(self, name: str, status: str):
        super().__init__(name, status)
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
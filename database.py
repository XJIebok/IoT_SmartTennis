from datetime import datetime

from pymongo import MongoClient
import copy

class DatabaseLogger:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["tennis_iot_db"]

        self.auto_events_collection = self.db["auto_events"]
        self.control_logs_collection = self.db["control_logs"]

        # print("Подключение к MongoDB выполнено")

    def save_auto_event(self, event_data: dict):
        event_data = build_auto_event_document(event_data)
        event_data = prepare_for_mongo(event_data)

        event_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = self.auto_events_collection.insert_one(event_data)

        print(f"Событие автоматического режима сохранено, id: {result.inserted_id}")

        return str(result.inserted_id)

    def save_control_log(self, log_data: dict):
        log_data = copy.deepcopy(log_data)
        log_data = prepare_for_mongo(log_data)
        
        log_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = self.control_logs_collection.insert_one(log_data)

        print(f"Лог управляющей команды сохранён, id: {result.inserted_id}")

        return str(result.inserted_id)

    # Анализ базы данных автоматических событий
    def analyze_rally_lengths(self):
        events = self.auto_events_collection.find().sort("_id", 1)

        rally_lengths = []
        current_rally_length = 0

        for event in events:
            camera_event = event.get("camera_event", {})
            hit_type = camera_event.get("hit_type")

            point_to = event.get("point_to")

            if hit_type == "racket":
                current_rally_length += 1

            if point_to is not None:
                if current_rally_length > 0:
                    rally_lengths.append(current_rally_length)

                current_rally_length = 0

        if len(rally_lengths) > 0:
            average_rally_length = round(sum(rally_lengths) / len(rally_lengths), 2)
            max_rally_length = max(rally_lengths)
        else:
            average_rally_length = 0
            max_rally_length = 0

        return {
            "rally_lengths": rally_lengths,
            "completed_rallies": len(rally_lengths),
            "average_rally_length": average_rally_length,
            "max_rally_length": max_rally_length
        }

    # Подсчёт и анализ успеха ручных команд
    def analyze_control_logs(self):
        logs = self.control_logs_collection.find()

        total_commands = 0
        success_commands = 0
        error_commands = 0

        for log in logs:
            total_commands += 1

            if log.get("result") == "success":
                success_commands += 1

            if log.get("result") == "error":
                error_commands += 1

        return {
            "total_commands": total_commands,
            "success_commands": success_commands,
            "error_commands": error_commands
        }

    def get_auto_events(self, limit: int = 10):
        events = self.auto_events_collection.find().sort("_id", -1).limit(limit)

        result = []

        for event in events:
            event["_id"] = str(event["_id"])
            result.append(event)

        return result

    def get_control_logs(self, limit: int = 10):
        logs = self.control_logs_collection.find().sort("_id", -1).limit(limit)

        result = []

        for log in logs:
            log["_id"] = str(log["_id"])
            result.append(log)

        return result

# Заменяем ключи-числа на строки
def prepare_for_mongo(data):
    if isinstance(data, dict):
        return {
            str(key): prepare_for_mongo(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [prepare_for_mongo(item) for item in data]

    return data

# Обрезаем словарь изменений авторежима
def build_auto_event_document(result: dict):
    camera = result.get("camera", {})
    line_sensor = result.get("line_sensor", {})
    net_sensor = result.get("net_sensor", {})
    scoreboard = result.get("scoreboard", {})
    controller = result.get("controller", {})

    return {
        "event": result.get("event"),
        "point_to": result.get("point_to"),
        "result": result.get("result"),
        "message": result.get("message"),

        "camera_event": {
            "hit_type": camera.get("hit_type"),
            "hit_coordinate": camera.get("hit_coordinate"),
            "ball_speed": camera.get("ball_speed"),
            "confidence": camera.get("confidence"),
            "frame_id": camera.get("frame_id")
        },

        "line_sensor": {
            "triggered": line_sensor.get("triggered"),
            "impact_coordinate": line_sensor.get("impact_coordinate"),
            "signal_strength": line_sensor.get("signal_strength")
        },

        "net_sensor": {
            "net_contact": net_sensor.get("net_contact"),
            "vibration_level": net_sensor.get("vibration_level")
        },

        "score": scoreboard.get("score"),

        "controller_state": {
            "last_hit_player": controller.get("last_hit_player"),
            "last_event": controller.get("last_event")
        }
    }
#
# if __name__ == "__main__":
#     logger = DatabaseLogger()
#
#     test_event = {
#         "event": "test event",
#         "point_to": 1,
#         "camera": {
#             "hit_type": "bounce",
#             "hit_coordinate": [42.0, 5.0]
#         },
#         "scoreboard": {
#             "score": {
#                 "points": [1, 0],
#                 "games": [0, 0],
#                 "sets": [0, 0]
#             }
#         }
#     }
#
#     logger.save_auto_event(test_event)
#
#     test_log = {
#         "device": "speaker",
#         "command": "set_volume",
#         "result": "success",
#         "message": "Громкость изменена на 70"
#     }
#
#     logger.save_control_log(test_log)
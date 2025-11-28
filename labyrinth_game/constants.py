EVENT_PROBABILITY_MODULO = 10          # диапазон для случайных событий
TRAP_DEATH_THRESHOLD = 3               # шанс смерти (< 3 из 10)
EVENT_TYPE_COUNT = 3                   # количество типов случайных событий
HELP_PADDING = 16                      # ширина поля для команды в show_help

ROOMS = {
    "entrance": {
        "description": (
            "Вы у входа в лабиринт. Стены покрыты мхом, "
            "на полу лежит старый факел."
        ),
        "exits": {"north": "hall", "east": "trap_room"},
        "items": ["torch"],
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой зал с эхом. По центру стоит пьедестал "
            "с запечатанным сундуком."
        ),
        "exits": {"south": "entrance", "west": "library", "north": "treasure_room"},
        "items": [],
        "puzzle": (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". '
            "Введите ответ цифрой или словом.",
            ('10', 'десять'),  
        ),
    },
    "trap_room": {
        "description": (
            "Комната с хитрым плиточным полом. На стене надпись: "
            '"Осторожно — ловушка".'
        ),
        "exits": {"west": "entrance"},
        "items": ["rusty_key"],
        "puzzle": (
            'Система плит активна. Чтобы пройти, введите "step step step".',
            "step step step",
        ),
    },
    "library": {
        "description": (
            "Пыльная библиотека. На полках старые свитки. "
            "Где-то здесь может быть ключ от сокровищницы."
        ),
        "exits": {"east": "hall", "north": "armory"},
        "items": ["ancient_book"],
        "puzzle": (
            'В одном свитке загадка: '
            '"Что можно услышать, но нельзя увидеть?" (одно слово)',
            ('эхо', 'echo'),
        ),
    },
    "armory": {
        "description": (
            "Старая оружейная комната. На стене висит меч, рядом — "
            "небольшая бронзовая шкатулка."
        ),
        "exits": {"south": "library"},
        "items": ["sword", "bronze_box"],
        "puzzle": None,
    },
    "treasure_room": {
        "description": (
            "Комната с большим сундуком. Дверь заперта — нужен особый ключ."
        ),
        "exits": {"south": "hall"},
        "items": ["treasure_chest"],
        "puzzle": (
            "Дверь защищена кодом. Введите код "
            "(подсказка: 2*5 = ?).",
            "10",
        ),
    },
}


COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "north/south/east/west": "движение без команды go",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "help": "показать это сообщение",
    "quit": "выйти из игры",
}

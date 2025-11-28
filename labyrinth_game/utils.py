"""Utility helpers for the labyrinth game."""
import math
from typing import Any, Dict

from labyrinth_game.constants import (
    EVENT_PROBABILITY_MODULO,
    EVENT_TYPE_COUNT,
    HELP_PADDING,
    ROOMS,
    TRAP_DEATH_THRESHOLD,
)


def describe_current_room(game_state: Dict[str, Any]) -> None:
    """Print description of the current room based on the game state."""
    room_id = game_state["current_room"]
    room = ROOMS[room_id]

    print()
    print(f"== {room_id.upper()} ==")
    print(room["description"])
    print()

    items = room.get("items", [])
    if items:
        items_list = ", ".join(items)
        print(f"Заметные предметы: {items_list}")

    exits = room.get("exits", {})
    if exits:
        exits_list = ", ".join(exits.keys())
        print(f"Выходы: {exits_list}")

    if room.get("puzzle") is not None:
        print(
            "Кажется, здесь есть загадка "
            "(используйте команду solve, чтобы попробовать её решить).",
        )
    print()

def pseudo_random(seed: int, modulo: int) -> int:
    """Deterministic pseudo-random number in range [0, modulo)."""
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    value = int(fractional * modulo)
    return value

def trigger_trap(game_state: Dict[str, Any]) -> None:
    """Simulate a trap being triggered with negative consequences."""
    print("Ловушка активирована! Пол начинает дрожать...")

    inventory = game_state.get("player_inventory", [])

    if inventory:
        # теряем случайный предмет из инвентаря
        index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы теряете предмет: {lost_item}. Он исчез в трещине пола.")
        return

    # инвентарь пуст — шанс смерти
    roll = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY_MODULO)
    if roll < TRAP_DEATH_THRESHOLD:
        print("Пол под вами проваливается! Вы не успеваете выбраться...")
        print("Игра окончена. Вы погибли в ловушке.")
        game_state["game_over"] = True
    else:
        print("Пол трескается, но вы чудом удерживаетесь и выбираетесь.")

def random_event(game_state: Dict[str, Any]) -> None:
    """Trigger a small random event during movement with low probability."""
    # Сначала решаем, будет ли событие вообще
    roll = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY_MODULO)
    if roll != 0:
        return

    # Выбираем тип события
    event_type = pseudo_random(game_state["steps_taken"] + 1, EVENT_TYPE_COUNT)
    room_id = game_state["current_room"]
    room = ROOMS[room_id]
    inventory = game_state.get("player_inventory", [])

    if event_type == 0:
        # Находка монетки
        print("Вы замечаете на полу маленькую монетку.")
        room_items = room.setdefault("items", [])
        room_items.append("coin")
        print("Монетка теперь лежит среди предметов этой комнаты.")
    elif event_type == 1:
        # Испуг
        print("Вы слышите странный шорох где-то в темноте...")
        if "sword" in inventory:
            print("Вы вскидываете меч, и существо спешно скрывается.")
        else:
            print("Вы замираете, но звук затихает сам по себе.")
    else:
        # Попытка срабатывания ловушки
        if room_id == "trap_room" and "torch" not in inventory:
            print("Темно и опасно... Кажется, здесь может сработать ловушка.")
            trigger_trap(game_state)


def _safe_input(prompt: str) -> str:
    """Request input from the user, handling interrupts.

    Вспомогательная функция только для этого модуля.
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def solve_puzzle(game_state: Dict[str, Any]) -> None:
    """Try to solve a puzzle in the current room."""
    room_id = game_state["current_room"]
    room = ROOMS[room_id]
    puzzle = room.get("puzzle")

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print(question)
    user_answer = _safe_input("Ваш ответ: ").strip()

    if user_answer == "quit":
        game_state["game_over"] = True
        return

    # Поддержка альтернативных вариантов ответа
    user_norm = user_answer.lower()

    if isinstance(correct_answer, (list, tuple, set)):
        variants = [str(v).lower() for v in correct_answer]
    else:
        variants = [str(correct_answer).lower()]

    if user_norm in variants:
        print("Верно! Загадка решена.")
        # Убираем загадку, чтобы нельзя было решить её дважды
        room["puzzle"] = None

        inventory = game_state["player_inventory"]

        # Награда зависит от комнаты
        if room_id == "trap_room":
            if "treasure_key" not in inventory:
                inventory.append("treasure_key")
                print("Вы чувствуете, что разгадка открыла путь к сокровищам.")
        elif room_id == "hall":
            inventory.append("gold_coin")
            print("Вы находите золотую монету и кладёте её в инвентарь.")
        elif room_id == "library":
            if "rusty_key" not in inventory:
                inventory.append("rusty_key")
                print("Вы находите старый ключ между страницами свитка.")
        else:
            inventory.append("coin")
            print("Вы получаете небольшую награду за сообразительность.")
    else:
        print("Неверно. Попробуйте снова.")
        # В trap_room неправильный ответ может активировать ловушку
        if room_id == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state: Dict[str, Any]) -> None:
    """Try to open the treasure chest with a key or a code."""
    room_id = game_state["current_room"]
    room = ROOMS[room_id]

    items = room.get("items", [])
    if "treasure_chest" not in items:
        print("Здесь нет сундука с сокровищами.")
        return

    inventory = game_state["player_inventory"]

    # Сценарий 1: есть ключ
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # Сценарий 2: нет ключа, пробуем взломать кодом
    print(
        "Сундук заперт. Возможно, его можно открыть кодом, "
        "если разгадать загадку механизма.",
    )
    choice = _safe_input("Ввести код? (да/нет): ").strip().lower()

    if choice == "quit":
        game_state["game_over"] = True
        return

    if choice not in ("да", "yes", "y"):
        print("Вы отступаете от сундука.")
        return

    puzzle = room.get("puzzle")
    if puzzle is None:
        print("Механизм загадки, похоже, сломан. Код ввести невозможно.")
        return

    _, correct_answer = puzzle
    code = _safe_input("Введите код: ").strip()

    if code == "quit":
        game_state["game_over"] = True
        return

    if code.lower() == str(correct_answer).lower():
        print("Код верный! Замок щёлкает, и сундук открывается.")
        items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Код неверный. Сундук остаётся запертым.")

def show_help(commands: Dict[str, str]) -> None:
    """Print available commands for the player."""
    print("\nДоступные команды:")
    for cmd, description in commands.items():
        print(f"  {cmd.ljust(HELP_PADDING)} - {description}")

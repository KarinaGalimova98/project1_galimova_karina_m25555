"""Utility helpers for the labyrinth game."""

from typing import Any, Dict

from labyrinth_game.constants import ROOMS


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

    if user_answer.lower() == str(correct_answer).lower():
        print("Верно! Загадка решена.")
        # чтобы нельзя было решать её дважды
        room["puzzle"] = None

        inventory = game_state["player_inventory"]
        # простая логика награды: ключ от сокровищ в первый раз
        if "treasure_key" not in inventory:
            inventory.append("treasure_key")
            print("Вы получаете таинственный ключ от сокровищницы!")
        else:
            inventory.append("gold_coin")
            print("Вы находите золотую монету и кладёте её в инвентарь.")
    else:
        print("Неверно. Попробуйте снова.")


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


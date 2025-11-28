#!/usr/bin/env python3

"""Entry point for the labyrinth game."""

from typing import Any, Dict

from labyrinth_game.player_actions import get_input, show_inventory
from labyrinth_game.utils import describe_current_room


def create_initial_state() -> Dict[str, Any]:
    """Create and return the initial game state."""
    return {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Флаг окончания игры
        "steps_taken": 0,  # Количество сделанных шагов
    }


def main() -> None:
    """Run the labyrinth game."""
    game_state = create_initial_state()

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        raw_command = get_input("> ")
        command = raw_command.strip().lower()

        if command in ("quit", "exit", "выход"):
            print("Вы покидаете лабиринт. До встречи!")
            game_state["game_over"] = True

        elif command in ("look", "осмотреться"):
            describe_current_room(game_state)

        elif command in ("inventory", "inv", "инвентарь"):
            show_inventory(game_state)

        elif command == "":
            # Пустой ввод просто пропускаем
            continue

        else:
            print("Неизвестная команда. Попробуйте: look, inventory, quit.")

        game_state["steps_taken"] += 1


if __name__ == "__main__":
    main()


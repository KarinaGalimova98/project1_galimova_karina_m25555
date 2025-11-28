#!/usr/bin/env python3

"""Entry point for the labyrinth game."""

from typing import Any, Dict

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    solve_puzzle,
)


def create_initial_state() -> Dict[str, Any]:
    """Create and return the initial game state."""
    return {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Флаг окончания игры
        "steps_taken": 0,  # Количество сделанных шагов (при движении)
    }


def process_command(game_state: Dict[str, Any], raw_command: str) -> None:
    """Process a single user command."""
    command = raw_command.strip()
    if not command:
        return

    parts = command.split(maxsplit=1)
    verb = parts[0].lower()
    arg = parts[1].lower() if len(parts) > 1 else ""


    match verb:
        case "quit" | "exit" | "выход":
            print("Вы покидаете лабиринт. До встречи!")
            game_state["game_over"] = True

        case "look" | "осмотреться":
            describe_current_room(game_state)

        case "inventory" | "inv" | "инвентарь":
            show_inventory(game_state)

        case "go" | "идти":
            if not arg:
                print("Куда идти? Укажите направление (например, go north).")
            else:
                move_player(game_state, arg)

        case "take" | "взять":
            if not arg:
                print("Что взять?")
            else:
                take_item(game_state, arg)

        case "use" | "использовать":
            if not arg:
                print("Что использовать?")
            else:
                use_item(game_state, arg)

        case "solve" | "решить":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case _:
            print(
                "Неизвестная команда. Попробуйте: "
                "go, look, take, use, solve, inventory, quit.",
            )


def main() -> None:
    """Run the labyrinth game."""
    game_state = create_initial_state()

    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Команды: go <direction>, take <item>, use <item>, "
          "look, solve, inventory, quit.")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        user_input = get_input("> ")
        process_command(game_state, user_input)


if __name__ == "__main__":
    main()

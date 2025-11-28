#!/usr/bin/env python3

"""Entry point for the labyrinth game."""

from labyrinth_game.constants import ROOMS


def main() -> None:
    """Run the labyrinth game."""
    game_state = {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Флаг окончания игры
        "steps_taken": 0,  # Количество сделанных шагов
    }

    current_room_id = game_state["current_room"]
    current_room = ROOMS[current_room_id]

    print("Первая попытка запустить проект!")
    print()
    print(f"Вы находитесь в комнате: {current_room_id}")
    print(current_room["description"])


if __name__ == "__main__":
    main()


"""Player actions for the labyrinth game."""

from typing import Any, Dict

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def show_inventory(game_state: Dict[str, Any]) -> None:
    """Print the player's inventory."""
    inventory = game_state.get("player_inventory", [])

    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    items_list = ", ".join(inventory)
    print(f"В вашем инвентаре: {items_list}")


def get_input(prompt: str = "> ") -> str:
    """Get input from the user, handling interruptions gracefully."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: Dict[str, Any], direction: str) -> None:
    """Move the player to another room if possible."""
    room_id = game_state["current_room"]
    room = ROOMS[room_id]
    exits = room.get("exits", {})

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    new_room_id = exits[direction]
    game_state["current_room"] = new_room_id
    game_state["steps_taken"] += 1
    describe_current_room(game_state)


def take_item(game_state: Dict[str, Any], item_name: str) -> None:
    """Take an item from the current room, if possible."""
    room_id = game_state["current_room"]
    room = ROOMS[room_id]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжёлый.")
        return

    items = room.get("items", [])

    if item_name not in items:
        print("Такого предмета здесь нет.")
        return

    items.remove(item_name)
    game_state["player_inventory"].append(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state: Dict[str, Any], item_name: str) -> None:
    """Use an item from the inventory, if possible."""
    inventory = game_state.get("player_inventory", [])

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажигаете факел. Вокруг становится светлее и менее страшно.")
    elif item_name == "sword":
        print("Вы сжимаете меч в руке и чувствуете прилив уверенности.")
    elif item_name == "bronze_box":
        print("Вы открываете бронзовую шкатулку.")
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Внутри вы находите ржавый ключ и кладёте его в инвентарь.")
        else:
            print("Внутри пусто — вы уже забрали всё ценное.")
    else:
        print("Вы не знаете, как использовать этот предмет.")


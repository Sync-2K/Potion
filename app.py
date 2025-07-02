import asyncio
import multiprocessing

from dribble.memory import BuildPlayer, WriteBinaryBytes, WriteInteger
from dribble.models import Game, GetCodeFromString, conversion_list
from dribble.utils import ConvertToGameValue
from nicegui import ui

from app.logic.elements import (
    adjust_all_attributes,
    adjust_all_badges,
    adjust_all_hotzones,
    adjust_all_tendencies,
    set_all_attributes,
    set_all_badges,
    set_all_hotzones,
    set_all_tendencies,
)
from app.logic.license import license_exists_and_valid, verify_license_key
from app.state.globals import *

# NiceGUI Pages


def main_page():
    """Setup the NiceGUI UI."""

    global game_running

    if not game_running:
        with ui.column().classes("h-screen w-full items-center justify-center gap-4"):
            ui.icon("warning", size="64px").classes("text-red-500")
            ui.label("Game Not Running").classes("text-3xl font-bold text-red-700")
            ui.label(
                "Please start NBA 2K25 and load the roster you want to use."
            ).classes("text-lg text-center max-w-xl")
            ui.label("Once the game is running, launch Potion again.").classes(
                "text-md text-gray-600 text-center max-w-xl"
            )

    else:
        with ui.header().classes(replace="bg-purple row items-center") as header:
            with ui.tabs() as tabs:
                ui.tab("Body")
                ui.tab("Vitals")
                ui.tab("Attributes")
                ui.tab("Badges")
                ui.tab("Tendencies")
                ui.tab("Hotzones")
                ui.tab("Signature")
                ui.tab("Gear")
                ui.tab("Accessories")

        with ui.footer(value=False).classes("bg-purple-100") as footer:
            ui.button(
                "Discord", on_click=lambda: ui.open("https://discord.gg/JV3H5xty34")
            ).props("flat color=white").classes("bg-purple w-40")

        with ui.left_drawer().classes("bg-purple-100 p-4") as left_drawer:
            ui.label("Potion Tasks").classes("text-lg font-bold mb-2")
            ui.button("Load Player", on_click=lambda: update_hover_player()).classes(
                "bg-purple w-40"
            )
            # ui.button("Copy Player", on_click=lambda: copy_hover_player()).classes(
            #     "bg-purple w-40"
            # )
            # ui.button("Refresh Roster", on_click=lambda: refresh_roster()).classes(
            #     "bg-purple w-40"
            # )

        with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
            ui.button(on_click=footer.toggle, icon="discord").props("fab").classes(
                "bg-purple"
            )

        with ui.tab_panels(tabs, value="Body").classes("w-full"):

            with ui.tab_panel("Body"):
                global label_body
                label_body = ui.label("No player selected").classes("text-2xl")
                experimental_label = ui.label(
                    "This page is experimental and may not work as expected."
                ).classes("text-sm text-gray-500")
                height_options = {
                    f"{i}": f"{i // 12}ft {i % 12}in" for i in range(60, 108)
                }
                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for body_part in offsets["Body"]:
                        body_part_name = body_part["name"]
                        select_element = ui.number(
                            label=body_part_name,
                            min=0,
                        ).classes("w-full")

                        # Add the select element to the input handler
                        input_handler.set_input("Body", body_part_name, select_element)

            with ui.tab_panel("Vitals"):
                global label_vitals
                label_vitals = ui.label("No player selected").classes("text-2xl")
                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for vital in offsets["Vitals"]:
                        vital_name = vital["name"]
                        vital_options = conversion_list.get(vital_name, {})

                        # Check if there are options for the items, otherwise use a default range
                        if vital_options:
                            select_element = ui.select(
                                label=vital_name,
                                options=list(vital_options.values()),
                                with_input=True,
                                new_value_mode="add-unique",
                            ).classes("w-full")
                        else:
                            select_element = ui.number(
                                label=vital_name,
                                min=0,
                            ).classes("w-full")

                        # Add the select element to the input handler
                        input_handler.set_input("Vitals", vital_name, select_element)

            with ui.tab_panel("Attributes"):
                global label_attributes
                label_attributes = ui.label("No player selected").classes("text-2xl")
                with ui.row().classes("my-4"):
                    ui.button(
                        "Set All to 99", on_click=lambda: set_all_attributes(99)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All +5", on_click=lambda: adjust_all_attributes(5)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All -5", on_click=lambda: adjust_all_attributes(-5)
                    ).classes("bg-purple w-40")
                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for attribute in offsets["Attributes"]:
                        attribute_name = attribute["name"]
                        select_element = ui.select(
                            label=attribute_name,
                            options=[i for i in range(25, 111)],
                            with_input=True,
                        ).classes("w-full")

                        # Add the select element to the input handler
                        input_handler.set_input(
                            "Attributes", attribute_name, select_element
                        )

            with ui.tab_panel("Badges"):
                global label_badges
                label_badges = ui.label("No player selected").classes("text-2xl")
                with ui.row().classes("my-4"):
                    ui.button(
                        "Set All to 5", on_click=lambda: set_all_badges(5)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All +1", on_click=lambda: adjust_all_badges(1)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All -1", on_click=lambda: adjust_all_badges(-1)
                    ).classes("bg-purple w-40")
                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for badge in offsets["Badges"]:
                        badge_name = badge["name"]
                        select_element = ui.select(
                            label=badge_name,
                            options=[i for i in range(0, 6)],
                        ).classes("w-full")

                        # Add the select element to the input handler
                        input_handler.set_input("Badges", badge_name, select_element)

            with ui.tab_panel("Tendencies"):
                global label_tendencies
                label_tendencies = ui.label("No player selected").classes("text-2xl")
                with ui.row().classes("my-4"):
                    ui.button(
                        "Set All to 100", on_click=lambda: set_all_tendencies(100)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All to 0", on_click=lambda: set_all_tendencies(0)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All +5", on_click=lambda: adjust_all_tendencies(5)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All -5", on_click=lambda: adjust_all_tendencies(-5)
                    ).classes("bg-purple w-40")
                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for tendency in offsets["Tendencies"]:
                        tendency_name = tendency["name"]
                        select_element = ui.select(
                            label=tendency_name,
                            options=[i for i in range(0, 101)],
                            new_value_mode="add-unique",
                        ).classes("w-full")

                        # Add the select element to the input handler
                        input_handler.set_input(
                            "Tendencies", tendency_name, select_element
                        )

            with ui.tab_panel("Hotzones"):
                global label_hotzones
                label_hotzones = ui.label("No player selected").classes("text-2xl")
                with ui.row().classes("my-4"):
                    ui.button(
                        "Set All to Hot", on_click=lambda: set_all_hotzones(2)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All to Cold", on_click=lambda: set_all_hotzones(0)
                    ).classes("bg-purple w-40")
                    ui.button(
                        "Set All to Neutral", on_click=lambda: set_all_hotzones(1)
                    ).classes("bg-purple w-40")
                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for hotzone in offsets["Hotzones"]:
                        hotzone_name = hotzone["name"]
                        hotzone_options = conversion_list.get(hotzone_name, {})

                        # Check if there are options for the item, otherwise use a default range
                        if hotzone_options:
                            select_element = ui.select(
                                label=hotzone_name,
                                options=list(hotzone_options.values()),
                                with_input=True,
                            ).classes("w-full")
                        else:
                            select_element = ui.input(
                                label=hotzone_name, type="number", min=0, max=4
                            ).classes("w-full")

                        # Add the select element to the input handler
                        input_handler.set_input(
                            "Hotzones", hotzone_name, select_element
                        )

            with ui.tab_panel("Signature"):
                global label_signature
                label_signature = ui.label("No player selected").classes("text-2xl")

                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for signature in offsets["Signatures"]:
                        signature_name = signature["name"]
                        signature_options = conversion_list.get(signature_name, {})

                        # Check if there are options for the signature, otherwise use a disabled select
                        if signature_options:
                            select_element = ui.select(
                                label=signature_name,
                                options=list(signature_options.values()),
                                with_input=True,
                            ).classes("w-full")
                        else:
                            select_element = (
                                ui.select(
                                    label=signature_name,
                                    options=["Disabled"],
                                )
                                .classes("w-full")
                                .props("disabled")
                            )

                        # Add the select element to the input handler
                        input_handler.set_input(
                            "Signatures", signature_name, select_element
                        )

            with ui.tab_panel("Gear"):
                global label_gear
                label_gear = ui.label("No player selected").classes("text-2xl")

                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for gear in offsets["Gear"]:
                        gear_name = gear["name"]
                        gear_options = conversion_list.get(gear_name, {})

                        # Check if there are options for the item, otherwise use a disabled select
                        if gear_options:
                            select_element = ui.select(
                                label=gear_name,
                                options=list(gear_options.values()),
                                with_input=True,
                                new_value_mode="add-unique",
                            ).classes("w-full")
                        else:
                            select_element = (
                                ui.select(
                                    label=gear_name,
                                    options=["Disabled"],
                                )
                                .classes("w-full")
                                .props("disabled")
                            )

                        # Add the select element to the input handler
                        input_handler.set_input("Gear", gear_name, select_element)

            with ui.tab_panel("Accessories"):
                global label_accessories
                label_accessories = ui.label("No player selected").classes("text-2xl")

                with ui.grid(columns=4).classes("gap-4 w-full"):
                    for accessory in offsets["Accessories"]:
                        accessory_name = accessory["name"]
                        accessory_options = conversion_list.get(accessory_name, {})

                        # Check if there are options for the item, otherwise use a disabled select
                        if accessory_options:
                            select_element = ui.select(
                                label=accessory_name,
                                options=list(accessory_options.values()),
                                with_input=True,
                            ).classes("w-full")
                        else:
                            select_element = (
                                ui.select(
                                    label=accessory_name,
                                    options=["Disabled"],
                                )
                                .classes("w-full")
                                .props("disabled")
                            )

                        # Add the select element to the input handler
                        input_handler.set_input(
                            "Accessories", accessory_name, select_element
                        )

    # Run the UI
    ui.run(
        favicon="🍷",
        title="Potion 1.0.0",
        show=True,
        reload=False,
    )


def license_page():
    with ui.column().classes("w-full h-screen items-center justify-center gap-6"):
        ui.image("app/resources/banner.jpeg").classes(
            "w-full max-w-2xl rounded-lg shadow-md"
        )

        ui.label("Activate Your License").classes("text-3xl font-bold text-center")
        ui.label("Enter your license key below to unlock the Potion Editor.").classes(
            "text-md text-gray-500 text-center"
        )

        message = ui.label().classes("text-sm text-gray-500")
        license_input = ui.input(label="License Key").classes("w-96")
        activate_button = ui.button("Activate").classes("bg-purple text-white w-40")

        async def submit():
            activate_button.disable()
            message.set_text("Verifying license...")
            await asyncio.sleep(0.1)  # Allow UI to refresh

            key = license_input.value.strip()
            valid, msg = verify_license_key(key)

            if valid:
                message.set_text("✅ License valid! Please restart the app.")
            else:
                message.set_text(f"❌ {msg}")
                activate_button.enable()

        activate_button.on("click", submit)

    # Run the UI
    ui.run(
        favicon="🍷",
        title="Potion 1.0.0",
        show=True,
        reload=False,
    )


# UI Event Handlers


def update_player_tabs(game, player):
    """Update UI components for each tab based on the given player object."""

    global is_updating_ui
    global latest_player

    is_updating_ui = True
    latest_player = player

    try:
        full_name = f"{player.vitals['First Name']} {player.vitals['Last Name']}"

        body_inputs = input_handler.get_inputs("Body")
        label_body.set_text(f"{full_name}'s Body")
        for name, input_field in body_inputs.items():
            value = player.body.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Body", name))

        vital_inputs = input_handler.get_inputs("Vitals")
        label_vitals.set_text(f"{full_name}'s Vitals")
        for name, input_field in vital_inputs.items():
            value = player.vitals.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Vitals", name))

        attribute_inputs = input_handler.get_inputs("Attributes")
        label_attributes.set_text(f"{full_name}'s Attributes")
        for name, input_field in attribute_inputs.items():
            value = player.attributes.get(name, 25)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Attributes", name))

        badge_inputs = input_handler.get_inputs("Badges")
        label_badges.set_text(f"{full_name}'s Badges")
        for name, input_field in badge_inputs.items():
            value = player.badges.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Badges", name))

        tendency_inputs = input_handler.get_inputs("Tendencies")
        label_tendencies.set_text(f"{full_name}'s Tendencies")
        for name, input_field in tendency_inputs.items():
            value = player.tendencies.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Tendencies", name))

        signature_inputs = input_handler.get_inputs(
            "Signatures",
        )
        label_signature.set_text(f"{full_name}'s Signatures")
        for name, input_field in signature_inputs.items():
            value = player.signatures.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Signatures", name))

        hotzone_inputs = input_handler.get_inputs("Hotzones")
        label_hotzones.set_text(f"{full_name}'s Hotzones")
        for name, input_field in hotzone_inputs.items():
            value = player.hotzones.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Hotzones", name))

        gear_inputs = input_handler.get_inputs("Gear")
        label_gear.set_text(f"{full_name}'s Gear")
        for name, input_field in gear_inputs.items():
            value = player.gear.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Gear", name))

        accessory_inputs = input_handler.get_inputs("Accessories")
        label_accessories.set_text(f"{full_name}'s Accessories")
        for name, input_field in accessory_inputs.items():
            value = player.accessories.get(name, 0)
            input_field.value = value
            input_field.on_value_change(create_value_handler("Accessories", name))

    except Exception as e:
        print(f"[UI Update Error] {e}")
    finally:
        is_updating_ui = False


def on_item_change(game, player, category, name, new_value):
    """Handle changes to UI items and update the player in memory."""

    global is_updating_ui
    global integer_only_categories

    try:
        if is_updating_ui:
            return

        if name in conversion_list and category not in integer_only_categories:
            new_code = GetCodeFromString(name, new_value)
            new_value = new_code if new_code else new_value

        item_category = offsets.get(category)
        item_offset = None
        item_length = None
        item_start_bit = None
        for item in item_category:
            if item["name"] == name:
                item_offset = item.get("offset")
                item_length = item.get("length")
                item_start_bit = item.get("startBit")
                break

        if item_offset is None:
            raise ValueError(f"No offset found for {category} > {name}")

        item_address = player.address + item_offset
        body_base_address = player.body.get("Address")
        item_body_address = body_base_address + item_offset

        new_value = int(new_value)

        if category == "Body":
            match name:
                case "Height" | "Wingspan":
                    if new_value and new_value >= 10:
                        in_game_value = (new_value * 2.54) * 100
                        in_game_value = round(in_game_value)
                        in_game_value = in_game_value.to_bytes(2, byteorder="little")
                        game.memory.write_bytes(item_body_address, in_game_value, 2)
                case "Weight":
                    if new_value and new_value >= 100:
                        game.memory.write_float(item_address, float(new_value))
        elif category == "Attributes":
            game_value = ConvertToGameValue(new_value, item_length)
            WriteBinaryBytes(game, item_address, item_length, game_value)
        else:
            WriteInteger(game, item_address, item_length, item_start_bit, new_value)

    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"[Item Change Error] {e} @ line {line_no}")


def create_value_handler(category, name):
    """Create a value change handler for the UI elements."""

    global game
    global is_updating_ui
    global latest_player

    def handler(e):
        if is_updating_ui:
            return
        if latest_player:
            on_item_change(game, latest_player, category, name, e.value)

    return handler


# UI Game Event Handlers


def copy_hover_player():
    """Copy the currently hovered player to the clipboard."""
    pass


def update_hover_player():
    """Update the UI with the currently hovered player."""

    if not game:
        ui.notify("Game not loaded")
        return

    hover_player = get_hover_player(game)
    if hover_player:
        update_player_tabs(game, hover_player)


def refresh_roster():
    """Refresh the roster in the game."""

    global game

    if not game:
        ui.notify("Cannot refresh roster, game not loaded")
        return

    game.refresh()
    ui.notify("Roster refreshed")


def get_hover_player(game):
    """Get the currently hovered player in the game."""

    try:
        base_cursor_address = offsets["Base"]["Cursor Base Address"]
        cursor_offset = offsets["Base"]["Cursor Offset"]

        cursor_base_address = game.memory.read_bytes(
            game.base_address + base_cursor_address, 8
        )
        cursor_base_address = int.from_bytes(cursor_base_address, byteorder="little")

        hover_player_address = game.memory.read_bytes(
            cursor_base_address + cursor_offset, 8
        )
        hover_player_address = int.from_bytes(hover_player_address, byteorder="little")

        return BuildPlayer(game, None, hover_player_address)

    except Exception as e:
        print(f"[Get Hover Player Error] {e}")
        return None


# Sync Worker


def sync_worker():
    try:
        global game
        global game_running
        global last_address

        game = Game()

        if game and game.module:
            game_running = True
            ui.notify("Game Loaded")

    except Exception as e:
        print(f"[Sync Worker Error] {e}")


if __name__ in {"__main__", "__mp_main__"}:
    multiprocessing.freeze_support()
    sync_worker()
    main_page()

from dribble.memory import GetOffsets

from app.ui.input_handler import InputHandler

game = None
game_running = False

last_address = None
latest_player = None
is_updating_ui = False
live_player_loading = False

integer_only_categories = ["Attributes", "Badges", "Tendencies"]

input_handler = InputHandler()
offsets = GetOffsets("app/resources/offsets.json")

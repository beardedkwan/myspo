from utils.env import load_env_file
from services import spotify_requests as sr
from services import spotify_auth as auth
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Header, Footer
from textual.containers import Container
from utils import debug

load_env_file()

'''
    TRACKS
'''
class TracksScreen(Screen):
    BINDINGS = [
        ("q", "app.quit", "Quit"),
        ("b", "app.get_playlists_screen", "Back")
    ]

    def __init__(self, playlist_id: str):
        super().__init__()
        self.playlist_id = playlist_id

    def compose(self):
        yield Header()

        self.table = DataTable(id="tracks_table")
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True

        # LEFT OFF HERE

        yield Footer()

'''
    PLAYLISTS
'''
class PlaylistsScreen(Screen):
    BINDINGS = [("q", "app.quit", "Quit")]

    def compose(self):
        yield Header()

        self.table = DataTable(id="playlist_table")
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True

        self.table.add_columns("Name", "Tracks")

        self.row_id_map = {}

        row_idx = self.table.add_row("Liked Songs", "--")
        self.row_id_map[row_idx] = "0"

        data = sr.get_playlists()
        for playlist in data["items"]:
            row_idx = self.table.add_row(playlist["name"], playlist["tracks"]["total"])
            self.row_id_map[row_idx] = playlist["id"]

        yield Container(self.table)
        yield Footer()

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        if self.table.id == "playlist_table":
            playlist_id = self.row_id_map[event.row_key]

            self.app.switch_screen(TracksScreen(playlist_id))


'''
    MAIN
'''
class Myspo(App):
    CSS_PATH = None

    def on_mount(self) -> None:
        self.push_screen(PlaylistsScreen())

    async def action_get_playlists_screen(self):
        await self.switch_screen(PlaylistsScreen())

if __name__ == "__main__":
    Myspo().run()

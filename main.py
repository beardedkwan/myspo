import os
from utils.env import load_env_file
from services import spotify_requests as sr
from services import spotify_auth as auth
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Header, Footer
from textual.containers import Container

load_env_file()

class PlaylistScreen(Screen):
    BINDINGS = [("q", "app.quit", "Quit")]

    def compose(self):
        yield Header()

        self.table = DataTable()
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True

        self.table.add_columns("ID", "Name", "Tracks")

        self.table.add_row("0", "Liked Songs", key="0")

        data = sr.get_playlists()
        for playlist in data["items"]:
            self.table.add_row(playlist["id"], playlist["name"], playlist["tracks"]["total"], key=playlist["id"])

        yield Container(self.table)
        yield Footer()

class Myspo(App):
    CSS_PATH = None

    def on_mount(self) -> None:
        self.push_screen(PlaylistScreen())

if __name__ == "__main__":
    Myspo().run()

from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, DataTable
import mysql.connector
import Program


class SignalManager(App):
    con = Program.connect_signal()

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("u", "update_table", "Manual Update"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    # def on_mount(self) -> None:
    #     table = self.query_one(DataTable)
    #     table.add_columns(*self.data[0])
    #     table.add_rows(self.data[1:])

    def action_update_table(self) -> None:
        queryCols = Program.GetCols(self.con, "department")
        Cols = []
        for object in queryCols:
            Cols.append(object[0])
        Data = Program.test(self.con)

        table = self.query_one(DataTable)

        table.clear()
        table.add_columns(Data[0])
        table.add_rows(Data)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


SignalManager().run()

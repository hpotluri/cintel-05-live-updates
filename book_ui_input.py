"""
Purpose: Provide user interaction options for MT Cars dataset.

IDs must be unique. They are capitalized in this app for clarity (not typical).
The IDs are case-sensitive and must match the server code exactly.
Preface IDs with the dataset name to avoid naming conflicts.

"""
from shiny import ui

# Define the UI inputs and include our new selection options

def get_books_inputs():
    return ui.panel_sidebar(
        ui.h2("Book Interaction"),
        ui.tags.hr(),
        ui.input_slider(
            "BOOK_PRICE",
            "Dollars ($)",
            min=0.0,
            max=50.0,
            value=[10.0, 35.0],
        ),
        ui.tags.hr(),
        ui.input_text(
            "AUTHOR",
            "Author Name",
        ),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )
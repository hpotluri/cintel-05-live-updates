"""
Purpose: Display output for MT Cars dataset.

@imports shiny.ui as ui
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_books_outputs():
    return ui.panel_main(
        ui.h2("Main Panel with Continuous and Reactive Output"),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Best Sellers for the week of 5-22-13 (Book API)"),
            ui.tags.br(),
            ui.output_ui("book_table"),
            ui.tags.br(),
        ),
    )
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.console.exceptions.cli_exception import CLIOrionisRuntimeError
from orionis.luminate.contracts.application import IApplication
from orionis.framework import NAME

class HelpCommand(BaseCommand):
    """
    Command class to display the list of available commands in the Orionis application.

    This command fetches all registered commands from the cache and presents them in a table format.
    """
    def __init__(self, app : IApplication):
        # Get the list of commands from the container
        self._commands : dict = app._commands if hasattr(app, '_commands') else {}

    # Command signature used for execution.
    signature = "help"

    # Brief description of the command.
    description = "Prints the list of available commands along with their descriptions."

    def handle(self) -> None:
        """
        Execute the help command.

        This method retrieves all available commands from the cache, sorts them alphabetically,
        and displays them in a structured table format.

        Raises
        ------
        ValueError
            If an unexpected error occurs during execution, a ValueError is raised
            with the original exception message.
        """
        try:

            # Display the available commands
            self.newLine()
            self.textSuccessBold(f" ({str(NAME).upper()} CLI Interpreter) Available Commands: ")

            # Initialize an empty list to store the rows.
            rows = []
            for signature, command_data in self._commands.items():
                rows.append([signature, command_data['description']])

            # Sort commands alphabetically
            rows_sorted = sorted(rows, key=lambda x: x[0])

            # Display the commands in a table format
            self.table(
                ["Signature", "Description"],
                rows_sorted
            )

            # Add a new line after the table
            self.newLine()

        except Exception as e:

            # Handle any unexpected error and display the error message
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
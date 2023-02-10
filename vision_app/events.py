# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.

events = [
    {
        'todo' : 'CI102',
        'date' : '2023-02-14'
    }
]
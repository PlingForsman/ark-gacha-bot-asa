"""Entry point: open the window and hand control to Tk.

Everything else is set up as a side effect of the imports below - the logger
starts a fresh logs.log and takes over sys.excepthook, and the UI loads
settings.json and resources.json (creating or recovering either if it has
to). Nothing here needs to happen in a particular order.
"""
from UI.UI import UI

if __name__ == "__main__":
    ui = UI()
    ui.mainloop()
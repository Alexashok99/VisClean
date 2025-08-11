

#Local Imports
from gui.main_gui import MainApp

class MainAppRunner:
    def __init__(self):
        self.app = MainApp()

    def gui_run(self):
        self.app.mainloop()


if __name__ == "__main__":
    MainAppRunner().gui_run()

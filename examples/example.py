import tkinter as tk
from NorthBastion import PlayerGUI

root = tk.Tk()
root.title("NorthBastion Player")
root.resizable(False, False)

path = "Music"

player = PlayerGUI(root)

player.logger_mode(True)

player.import_dependencies()

player.check_path(path)
player.music_loader()

player.render_GUI()

root.mainloop()

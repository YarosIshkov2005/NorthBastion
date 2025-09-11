import tkinter as tk
from tkinter.messagebox import showerror
import logging
import os

class PlayerGUI:
    def __init__(self, master):
        self.master = master
        
        self.player_is_running = False
        self.track_is_running = False
        self.track_is_begun = False
        self.dependencies_ok = False
        self.logger = None
        self.after_id = None
        
        self.error_message = " "
        self.relative_path = " "
        self.absolute_path = " "
        
        self.track_index = 0
        self.volume_level_index = 5
        
        self.logger_levels = (
            "INFO", "DEBUG",
            "ERROR", "WARNING",
            "CRITICAL"
        )
        self.logger_modes = ("a", "w")
        self.logger_encodings = ("utf-8", "latin-1")
        
        self.track_list = []
        self.player_buttons = []
        self.button_name = [
            ["Back", "Play", "Next"],
            ["Vol-", "Off", "Vol+"]
        ]
        self.volume_level = [
            0.0, 0.1, 0.2,
            0.3, 0.4, 0.5,
            0.6, 0.7, 0.8,
            0.9, 1.0
          ]
        
        self.player_functions = {
            "On": self.player_switch,
            "Off": self.player_switch,
            "Play": self.play_pause_track,
            "Pause": self.play_pause_track,
            "Next": self.next_track,
            "Back": self.back_track,
            "Vol+": self.volume_up,
            "Vol-": self.volume_down
        }
        
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
            
    def logger_mode(self, enabled=False, name="NorthBastion.log", level="DEBUG", mode="w", encoding="utf-8"):
        level = level.upper()
        mode = mode.lower()
        encoding = encoding.lower()
        
        if not isinstance(enabled, bool):
            raise ValueError(f"Incorrect enabled value '{enabled}'. Use boolean values: True or False")
            
        if self.logger and self.logger.handlers:
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
                    
        if name.startswith(".") or not name.endswith(".log"):
            raise NameError(f"Incorrect logfile name '{name}'. For example: 'logfile.log'")
                
        if not isinstance(level, str) or level not in self.logger_levels:
            raise ValueError(f"Unknown level '{level}'. Use levels: 'DEBUG (10)', 'INFO (20)', 'WARNING (30)', 'ERROR (40)', 'CRITICAL (50)'")
                
        if not isinstance(mode, str) or mode not in self.logger_modes:
            raise ValueError(f"Unsupported write mode '{mode}'. Use write modes: 'a' or 'w'")
                
        if not isinstance(encoding, str) or encoding not in self.logger_encodings:
            raise ValueError(f"Unsupported encoding '{encoding}'. Use encodings: 'utf-8' or 'latin-1'")
                
        self.logger = logging.getLogger("northbastion_player")
        self.logger.setLevel(level)
                    
        file_handler = logging.FileHandler(
            filename=name,
            mode=mode,
            encoding=encoding
        )
        file_handler.setLevel(level)
                    
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)s \n")
        file_handler.setFormatter(formatter)
                    
        self.logger.addHandler(file_handler)
        
    def import_dependencies(self):
        dependencies = CheckDependencies(self.logger)
        self.dependencies_ok = dependencies.get_result()
        self.mixer = dependencies.get_mixer()
        self.error_message = dependencies.get_message()
        
        if self.dependencies_ok:
            self.player = MusicPlayerCore(self.mixer, self.logger)
        
    def show_error_message(self, show=False):
        if isinstance(show, bool) and not self.dependencies_ok:
            showerror(title="Dependency error:", message=self.error_message)
        else:
            if not isinstance(show, bool):
                raise ValueError(f"Incorrect show value '{show}'. Use boolean values: True or False")
            
    def check_path(self, path=None):
        try:
            self.relative_path = path
            absolute_path = os.path.abspath(path)
            if os.path.isdir(absolute_path):
                if self.logger:
                    self.logger.info(f"Folder named {self.relative_path} found!")
                self.absolute_path = absolute_path
            else:
                showerror(title="Folder exists error:", message=f"Folder named {self.relative_path} not found")
                if self.logger:
                    self.logger.error(f"Folder named {self.relative_path} does not exists")
                self.absolute_path = " "
        except Exception as e:
            if self.logger:
                self.logger.error(f"NorthBastionError 2: {e}")
            self.absolute_path = " "
            
    def music_loader(self, path=None):
        audio_formats = (".wav", ".mp3", ".ogg")
        try:
            if self.absolute_path:
                file_path = self.absolute_path
            else:
                file_path = os.path.absolute(path)
            
            if self.track_list:
                self.track_list.clear()
                    
            with os.scandir(file_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        if not entry.name.startswith(".") and entry.name.endswith(audio_formats):
                            self.track_list.append(entry.name)
            
            if self.track_list:                
                self.track_list.sort()
            
            if self.logger:
                self.logger.info(f"Track list loaded ({len(self.track_list)}): {self.track_list}")
        except Exception as e:
            showerror(title="Load track error:", message=f"No tracks in folder {self.relative_path}")
            if self.logger:
                self.logger.error(f"NorthBastionError 3: {e}")
        
    def render_GUI(self):
        frame_buttons = tk.Frame(self.master)
        frame_buttons.pack()
            
        if self.dependencies_ok:
            for row in range(2):
                row_buttons = []
                for col in range(3):
                    button = tk.Button(
                        frame_buttons,
                        text=self.button_name[row][col],
                        font=("Helvetica", 7, "bold"),
                        command=lambda r=row, c=col: self.player_controller(r, c),
                        width=5,
                        height=2,
                    )
                    button.grid(row=row, column=col)
                    row_buttons.append(button)
                self.player_buttons.append(row_buttons)
                
            self.disable_ui()
        else:
            label_error = tk.Label(
                frame_buttons,
                text="Error: Pygame not found",
                font=("Helvetica", 10, "bold")
            )
            label_error.pack(padx=10, pady=10)
            
            button_exit = tk.Button(
                frame_buttons,
                text="Exit",
                font=("Helvetica", 7, "bold"),
                command=self.close_window
            )
            button_exit.pack(padx=10, pady=10)
        
    def player_controller(self, r, c):
        function = self.player_buttons[r][c].cget("text")
        if function in self.player_functions:
            self.player_functions[function]()
            
    def player_switch(self):
        self.player_is_running = not self.player_is_running
        state = "On" if self.player_is_running else "Off"
        
        if self.player_is_running:
            self.enable_ui()
        else:
            self.disable_ui()
            self.player.stop_track()
            self.track_is_begun = False
            
            if self.logger:
                self.logger.info("Track status: Stop")
        
        if self.logger:
            self.logger.info(f"Player status: {state}")
            
    def play_pause_track(self):
        if self.track_list:
            track = self.track_list[self.track_index]
            volume = self.volume_level[self.volume_level_index]
        
            if not hasattr(self, "player") or not self.player:
                return
            
            if not self.track_is_begun:
                self.player.set_track(self.absolute_path, track)
                self.player.set_volume(volume)
                self.track_is_begun = True
                self.track_is_running = True
                self.player_buttons[0][1].config(text="Pause")
                self.transition_track()
                return
                
            if self.logger:
                self.logger.info(f"Track started: {track}")
            
            if self.track_is_running:
                self.player_buttons[0][1].config(text="Play")
                self.player.pause_track()
                self.after_id = True
                self.master.after_cancel(self.after_id)
            else:
                self.player_buttons[0][1].config(text="Pause")
                self.player.unpause_track()
                self.transition_track()
            
            state = "Pause" if not self.track_is_running else "Play"    
            if self.logger:
                self.logger.info(f"Track status: {state}")
        
            self.track_is_running = not self.track_is_running
            
        else:
            if self.logger:
                self.logger.debug(f"Track list is empty ({len(self.track_list)})")
        
    def next_track(self):
        try:
            if self.track_is_running:
                if self.track_index < len(self.track_list) - 1:
                    self.track_index += 1
                else:
                    self.track_index = 0
               
                track = self.track_list[self.track_index]
                self.player.set_track(self.absolute_path, track)
                
                if self.logger:
                    self.logger.debug(f"Track updated {self.track_index} : {track}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"NorthBastionError 4: {e}")
        
    def back_track(self):
        try:
           if self.track_is_running:
               if self.track_index > 0:
                    self.track_index -= 1
               else:
                    self.track_index = len(self.track_list) - 1
           
               track = self.track_list[self.track_index]
               self.player.set_track(self.absolute_path, track)
               
               if self.logger:
                   self.logger.debug(f"Track updated {self.track_index} : {track}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"NorthBastionError 4: {e}")
            
    def volume_up(self):
        try:
            if self.track_is_running:
                self.volume_level_index += 1
                self.volume_level_index %= 11
                    
                volume = self.volume_level[self.volume_level_index]
                self.player.set_volume(volume)
            
                if self.logger:
                    self.logger.debug(f"Volume set: {volume}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"NorthBastionError 5: {e}")
        
    def volume_down(self):
        try:
            if self.track_is_running:
                self.volume_level_index -= 1
                self.volume_level_index %= 11
                    
                volume = self.volume_level[self.volume_level_index]
                self.player.set_volume(volume)
            
                if self.logger:
                    self.logger.debug(f"Volume set: {volume}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"NorthBastionError 5: {e}")
                
    def transition_track(self):
        if not mixer.music.get_busy():
            self.next_track()
            track = self.track_list[self.track_index]
            if self.logger:
                self.logger.debug(f"Track updated {track} : {track_index}")
        self.after_id = self.master.after(1000, self.transition_track)
            
    def enable_ui(self):
        for row in self.player_buttons:
            for button in row:
                button.config(state="normal")
        self.player_buttons[1][1].config(text="Off")
                        
    def disable_ui(self):
        for row in self.player_buttons:
            for button in row:
                button.config(state="disabled")
        self.player_buttons[0][1].config(text="Play")
        self.player_buttons[1][1].config(text="On", state="normal")
        
    def close_window(self):
        self.after_id = True
        self.master.after_cancel(self.after_id)
        self.master.destroy()
        
class CheckDependencies:
    def __init__(self, logger):
        self.mixer = None
        self.logger = logger
        self.dependencies_ok = False
        self.error_message = " "
        
        self.check_dependencies()
                
    def check_dependencies(self):
        try:
            import pygame.mixer as mixer
            mixer.init()
            self.mixer = mixer
            self.dependencies_ok = True
            if self.logger:
                self.logger.info("Pygame library initialized successfully!")
        except ModuleNotFoundError:
            self.error_message = "Pygame not installed"
            if self.logger:
                self.logger.critical("Pygame library is missing. Please install it via: pip install pygame")
            self.dependencies_ok = False
        except Exception as e:
            if self.logger:
                self.logger.critical(f"NorthBastionError 1: {e}")
            self.dependencies_ok = False
            
    def get_mixer(self):
        return self.mixer
        
    def get_result(self):
        return self.dependencies_ok
        
    def get_message(self):
        return self.error_message
        
class MusicPlayerCore:
    def __init__(self, mixer, logger):
        self.mixer = mixer
        self.logger = logger
        self.track = " "
        
    def set_track(self, path, track):
        self.track = os.path.join(path, track)
        self.play_track()
        
    def play_track(self):
        try:
            if os.path.exists(self.track):
                self.mixer.music.load(self.track)
                self.mixer.music.play()
                if self.logger:
                    self.logger.info(f"Current track: {self.track}")
            else:
                if self.logger:
                    self.logger.error(f"Track {self.track} not found")
        except Exception as e:
            if self.logger:
                self.logger.error(f"NorthBastionError 6: {e}")
        
    def stop_track(self):
        self.mixer.music.stop()
        
    def unpause_track(self):
        self.mixer.music.unpause()
        
    def pause_track(self):
        self.mixer.music.pause()
        
    def set_volume(self, volume):
        self.mixer.music.set_volume(volume)
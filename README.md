[file name]: README.md
[file content begin]

A library for creating a simple music player with a Tkinter-based GUI for the frontend and Pygame for the backend.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

# 🛠️ Bugfix v1.0.3

# 🚀 New Features:
• Added if not isinstance() checks in the logger_mode and show_error_message methods to validate input data types.

• Added a track state monitoring loop using the if not mixer.music.get_busy() condition. When the current track finishes, the next_track function is called automatically to play the next track.

# Working Principle Update:
Added description of the transition_track functionality:

- **Automatic Track Transition**:  
  The player now includes an automatic track transition feature. When the current track finishes playing (i.e., reaches its end naturally), the next track in the playlist is automatically started. This is implemented using a background check of the mixer's state through mixer.music.get_busy(). If the mixer is not busy (indicating the track has ended), the next_track function is triggered.

  Example:
  - Current track: Track2.mp3 ends → Track3.mp3 starts automatically
  - Works only when player is active (On state) and respects track cycling logic

# Error Description Added:
**For logger_mode method:**
- `ValueError: Incorrect enabled value 'enabled'. Use boolean values: True or False` - occurs when non-boolean values are passed to the `enabled` parameter

**For show_error_message method:**
- ValueError: Incorrect enabled value 'enabled'. Use boolean values: True or False - occurs when non-boolean values are passed to the enabled parameter

**Solutions:** Ensure only boolean values (True/False) are passed to these parameters. Example: player.logger_mode(True, ...) instead of player.logger_mode("True", ...)

## 📩 Installation:
• Clone the repository:
  1. Clone the repository:
   git clone https://github.com/YarosIshkov2005/NorthBastion.git
  2. cd NorthBastion

## 🚀 Quick Start (5 minutes):
• Install dependencies: pip install r- requirements.txt.

• Copy the example code from the section: Example Usage.

• Create a Music folder with audio files.

• Run the script and enjoy the music 😌!

Table of Contents:
***
1. Description: functions, additional features, working principle.

2. Technical Specifications: architecture, content loading, supported OS, dependencies.

3. Example Usage: API example, steps, methods.

4. Errors and Solutions: method errors, dependency installation, Android recommendations, installation and dependency checks, diagnostics and troubleshooting.

5. Links and Literature: materials, literature.
***

Section 1: Description 📝:
***
# 🎯 Functions:
• The library provides a simple music player with a Tkinter interface and a Pygame playback engine. Supports WAV, MP3, and OGG formats. Includes a minimal set of features for convenient use and a simple API for integration.

- ⏺️⏹️ turn player on/off (On/Off button).
- ▶️⏸ play/pause track (Play/Pause button).
- ⏪⏩ rewind tracks backward/forward (Back and Next buttons).
- 📶 increase/decrease volume (Vol+ and Vol- buttons).
- Cyclic control: n = (n + 1) % 11.
- 11 volume levels (from 0.0 to 1.0, step 0.1).

# 🔧 Additional Features:
- 📝 Logging system (customizable levels).
- 🛡️ Error handling with pop-up notifications.
- 🔍 Auto-dependency check (Pygame).

# ⚙️ Working Principle:
- On/Off: Pressing the On button enables the interface (enable_ui), the button changes to Off. Pressing the Off button disables the interface (disable_ui), the button changes to On:
» Cycle: On -> Off -> On.

- Play/Pause: First press of the Play button sets the track_is_begun flag to True, activates the play_track function, and changes to Pause. Pressing the Pause button calls the pause_track function, which stops the track. On subsequent plays, the unpause_track function resumes the track from where it was stopped, as the track_is_begun flag remains unchanged until the player is turned off. A full track reset (via stop_track) occurs only when the interface is disabled, as track_is_begun becomes False.
***
» A. On first Play activation:
         - Sets track_is_begun = True.
         - Starts the track (play_track).
         - Button changes to Pause.

    B. On subsequent activations:
         - Pause stops the track (pause_track).
         - Play resumes the track from the stop point (unpause_track).
         - Full reset (via stop_track) only occurs when turning off the player, track_is_begun becomes False.
***

- Track Switching:
- Back: Pressing the Back button activates the back_track function, which uses the track_index counter. The index changes using n = n - 1, ranging from the last track in track_list to 0:
***
» A. Example track_list:
         > [Track1.mp3, Track2.mp3, Track3.mp3].
          - Current track: Track3.mp3.
          - Decrement track_index -= 1, get Track2.mp3. track_index value corresponds to the index in track_list, i.e., value decreases by 1, Track3.mp3 -> Track2.mp3.

    B. If track_index = 0:
         - Use condition if track_index > 0, and if value is less than 0 (e.g., -1), set track_index = len(track_list) - 1, where -1 is the last element, get Track3.mp3.
***

- Next: The Next button works similarly but uses n = n + 1 and the next_track function. track_index increments by 1:
***
» A. Example track_list:
         > [Track1.mp3, Track2.mp3, Track3.mp3].
          - Current track: Track1.mp3.
          - Increment track_index += 1, get Track2.mp3 or Track1.mp3 -> Track2.mp3.

    B. If track_index = len(track_list) - 1:
         - Reverse condition if track_index > len(track_list) - 1, set track_index = 0, get Track1.mp3.
***

- Volume Control:
- Vol-: Pressing Vol- activates volume_down, which uses the volume_index_counter. The value changes by n = (n - 1) % 11, where 11 is the number of levels (range 0.0 to 1.0, step 0.1, 11 values, fixed list). The mechanism works similarly to track switching but with a different scheme:
***
» A. Example volume_level:
         >[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].
         - Current volume: 0.5.
         - Decrement volume_level_index -= 1 get 0.4 i.e., 0.5 -> 0.4.

    B. If volume_level_index = -1:
         - Modulo -1 % 11 = 10, get 1.0 and cycle back to 0.0.

- Vol+: The Vol+ button works similarly, activating the volume_up function, which uses n = (n + 1) % 11:
***
» A. Example volume_level:
         >[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].
          - Current volume: 0.5.
          - Increment volume_level_index += 1, get 0.6 i.e., 0.5 -> 0.6.

    B. If volume_level_index = 11:
         - Modulo 11 % 11 = 0, get 0.0 and cycle back to 1.0.
***
***

Section 2: Technical Specifications 📑:
***
• **Architecture**: The library takes a reference to an existing Tkinter window (root) and only manages internal GUI elements.

• **Content Loading**: Built-in track loader from a specified folder (called by the user).

• **Supported OS**:
  - ✅ Windows (full support).
  - ✅ macOS (full support). 
  - ✅ Linux (full support).
  - ⚠️ Android (works only through terminal emulators, no GUI).
  - ❌ iOS (not supported).

• **Dependencies**: Requires installed Pygame and Python 3.6+.
***

Section 3: Example Usage 🎵:
***
# ✔️ API Example:
• Below is an API example for the library:

import tkinter as tk
from NorthBastion import PlayerGUI

root = tk.Tk()
root.title("NorthBastion Player")
root.resizable(False, False)

path = "Music"

player = PlayerGUI(root)

player.logger_mode(True, "NorthBastion.log", "DEBUG", "w", "utf-8")

player.import_dependencies()
player.show_error_message(True)

player.check_path(path)
player.music_loader()

player.render_GUI()

root.mainloop()

# 🛠️ Steps:
1. Import libraries:
    • Import Tkinter and our library (NorthBastion):
         - import tkinter as tk
         - from NorthBastion import PlayerGUI

2. Create window:
     • Create a Tkinter window, set parameters as desired:
          - root = tk.Tk()
          - root.title("NorthBastion Player")
          - root.resizable(False, False)
      » Here we set the window title (root.title) and disable window resizing (root.resizable).

3. Specify folder path:
     • Specify the path to the folder, can be relative or absolute:
          - path = "Music"

4. Initialize library:
     • Initialize the library by passing the reference to the previously created window:
         - player = PlayerGUI(root)

5. Import dependencies (Pygame):
     • Call the method that imports Pygame into our library:
         - player.import_dependencies()

6. Show errors:
     • Add the show_error_message method to display pop-up notifications in case of failed Pygame import:
        - show_error_message(True)

7. Load tracks:
    • Add the music_loader method to load audio files (if not using check_path, specify the path directly in brackets):
        - player.music_loader()
    » If not using check_path:
        - player.music_path(path)

8. Render GUI:
    • Add the render_GUI method to display the interface:
        - player.render_GUI()

9. Main loop:
     • Add root.mainloop() at the end to start Tkinter:
         - root.mainloop()

Note:
    • Methods: logger_mode, show_error_message, and check_path are optional, discussed below.
***

# ℹ️ Methods:
    • PlayerGUI(master) - mandatory method initializing the library (creates the PlayerGUI class), takes a single parameter master, passed in parentheses (), i.e., takes a reference to the previously created Tkinter window. The passed name can be any, depending on the window reference name, but it is recommended to use root as it is standard.

     Example: player = PlayerGUI (root)

     » Create a variable player, through which we will call methods, as they are inside the PlayerGUI class.

    • logger_mode(enabled, name, level, mode, encoding) - optional method responsible for logging library events.
Takes one mandatory parameter enabled, a boolean True or False, i.e., enable/disable logger, and four optional: name - log file name with ".log" extension (e.g., "NorthBastion.log", set by default), level - logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (DEBUG by default), mode - file write mode: "a" or "w" ("w" by default, to save memory), encoding - encoding, supported encodings: "utf-8", "latin-1" ("utf-8" by default). Parameters (except enabled) can be in any case, as the method uses: upper() and lower() to adjust case, i.e., case is converted appropriately for each (except enabled, name) parameter: "debug" -> "DEBUG", "W" -> "w", "UTF-8" -> "utf-8".

     Example: player.logger_mode(True, "logfile.log", "DEBUG", "a", "utf-8")

    • import_dependencies() - mandatory method, no parameters, initializes the CheckDependencies class, which imports Pygame. If Pygame import fails, a pop-up notification will be shown: Pygame not installed, also in the application window: Error: Pygame not found, with an Exit button to quit the program.

     Example: player.import_dependencies()

    • show_error_message(enabled) - optional method, takes a single parameter enabled, a boolean (True, False). Displays an error message if Pygame import fails. If enabled = True, the mentioned pop-up notification: Pygame not installed will be shown.

     Example: player.show_error_message(True)

    • check_path(path) - optional method, takes a single parameter path (path = None by default), checks if the folder exists at the specified path, and returns the absolute path (relative path is converted to absolute using os.path.abspath()), if the folder exists (checked via os.path.isdir()). Otherwise returns empty value (None), and shows a pop-up notification: Folder "name" not found.

     Example: player.check_path("Music")

    • music_loader(path) - mandatory method, takes a single optional (if using check_path) parameter path (path = None by default), loads audio files in WAV, MP3, OGG formats via with os.scandir(path) as entries. If both folder and tracks exist, files are loaded from the specified folder into track_list. If not, a pop-up notification will be shown: No tracks in folder "name". The method also clears track_list via clear() before filling it, and sorts tracks alphabetically using sort(). If check_path is not used, the path parameter should be specified. The method also converts relative path to absolute if check_path returns None. Includes checks if entry.is_file() - checks if the iterated object is a file, if not entry.name.startswith(".") - protection against hidden files (such files usually start with a dot), if entry.name.endswith(audio_formats) - check for supported audio extensions, where audio_formats is a tuple: (".wav", ".mp3", ".ogg").

     Example: player.music_loader("Music")

     » Specify path if not using check_path.

    • render_GUI() - mandatory parameter, no parameters, responsible for creating one of the main components of the library: the interface (GUI). Creates a player_buttons list, then using tk, generates 6 buttons using for loops. player_buttons is converted to a two-dimensional list (using an additional list row_buttons, representing a row of 3 buttons, two of which are generated). filled with buttons. The library also imports tkinter as tk, but only uses tk to create widgets. The method is also responsible for showing errors in the application window. Besides displaying the interface and errors, the method handles button presses via an additional function player_controller, which uses a dictionary player_functions, representing the button value + function call, e.g.: {On: player_switch, Off: player_switch}, where On/Off - key (button value obtained by the cget() function, in player_controller), and player_switch the function name we call respectively (turns player on/off). Similarly, buttons are handled: Play/Pause - play_pause_track, Back - back_track, Next - next_track, Vol- - volume_down, Vol+ - volume_up.

     Example: player.render_GUI()
***

Section 4: Errors and Solutions ❌✅:
***
# ⛔ Method Errors:
    • logger_mode:
        - NameError: Incorrect logfile name "name". For example: "logfile.log" - occurs when specifying an invalid log file name, e.g., starting with "." which denotes hidden files, or having an incorrect extension, e.g., ".txt".

        » Solution: name the log file with a valid name: "logfile.log", any case. Parameter is optional, in which case the file will be named: "NorthBastion.log" (name "NorthBastion.log" is set by default by logger_mode).

         - ValueError: Unknown level "level". Use levels: DEBUG (10), INFO (20), WARNING (30), ERROR (40), CRITICAL (50) - occurs when specifying an unknown logging level.

         » Solution: specify one of the standard levels: DEBUG, INFO, WARNING, ERROR, CRITICAL, any case. Parameter is optional, in which case DEBUG level will be set (DEBUG level is set by default by logger_mode).

          » Note:
              - If e.g., INFO level is specified, logging will start from this level, DEBUG level will not be included. To display all levels, the level parameter must be DEBUG.

          -  ValueError: Unsupported write mode "mode". Use write modes: "a" or "w" - occurs when specifying an unsupported write mode, e.g., "x", which creates an exclusive file and causes an error if recreated.

          » Solution: specify mode "a" if you need to append to the file without recreating it, or "w" if you need to clear the file on each program run. Parameter is optional, in which case "w" mode will be set (mode 
"w" is set by default by logger_mode, to save memory).

          - ValueError: Unsupported encoding "encoding". Use encodings: "utf-8" or "latin-1" - occurs when specifying an unsupported encoding, e.g., "utf-16"/"utf-32".

          » Solution: specify a supported encoding "utf-8" or "latin-1", any case. Parameter is optional, in which case "utf-8" encoding will be set ("utf-8" encoding is set by default by logger_mode).

    • import_dependencies:
        - Dependency error: Pygame not installed (pop-up notification) - occurs when the Pygame library is missing, as import is impossible.

        » Solution: install Pygame via the pip package manager by entering: pip install pygame. After that, the error should disappear if the library installed successfully. Optimal version selection is possible. Tkinter does not require installation as it is part of standard Python.

    • check_path:
        - Folder error exists: Folder "name" not found (pop-up notification) - occurs when the specified folder is missing, e.g., accidentally specifying non-existent "Musik" instead of existing "Music", or not specifying the path parameter (check_path sets path = None by default), check_path cannot find a folder with that name.

        » Solution: before running, ensure the specified folder exists, or create it beforehand and load tracks into it for correct operation. Also check the path and specify it as the path parameter.

        » Recommendation: use relative paths for simplicity.

    • music_loader:
        - Load track error: No tracks in folder "name" (pop-up notification) - occurs when there are no tracks in the folder, i.e., track_list is empty. This can happen if check_path returns None, and the path parameter is not specified (music_loader sets path = None by default).

       » Solution: use check_path before music_loader (recommended), and also check if there are audio files in the folder with the specified audio formats. Or pass the folder path directly to music_loader as the path parameter.

        » Note:
            - The error in the application window only appears for Pygame import errors; in other cases, the interface will be displayed, but pressing the Play button will do nothing, as the play_pause_track function has a check: if track_list, which blocks player activation logic if there are no tracks.
            - The show_error_message method only handles Dependency error; File exists error and Load track error are not related to show_error_message. This was done because Dependency error is critical for the application, while File exists error / Load track error are informational.
***

# ♻️ Dependency Installation:
    • **Android Support**: 
         - ⚠️ Limited support (only through terminal emulators: Termux, Pydroid 3).
         - 🔸 On devices with ARM Neon, mixer initialization (mixer.init()) may fail.
         - 🔸 Testing on different devices is recommended.
         - ❌ No graphical interface (GUI not supported).

    • **iOS Support**: 
         - ❌ Not supported (platform restrictions, no native Python support).

# 📱 Android Recommendations:
    • Use Termux for maximum compatibility.
    • Prepare an alternative solution for mobile devices.
    • Test on several devices before deployment.

#  ♻️🛠️ Installation and Dependency Checks:
    • To work with our NorthBastion library, install the Pygame library. Do this via the pip package manager by entering: pip install pygame. Tkinter does not require installation as it is part of standard Python. Wait for installation and activate the show_error_message method to ensure no error notification is displayed.

         » Recommendation: you may need to test different Pygame versions for your device.

    • **Basic Installation**:
         - pip install r- requirements.txt

    • **For Python 3.x**:
        - pip3 install r- requirements.txt

    • **Specifying a Specific Version**:
        - python -m pip install r- requirements.txt

    • Simple example to check Pygame availability:

        import pygame.mixer as mixer

        mixer.init()

        print("Pygame successfully installed!")

        - Import pygame.mixer, and rename it to mixer for convenience.
        - Initialize the mixer: mixer.init().
        - Print a message about successful Pygame import and mixer initialization: print("Pygame successfully installed! ").

    • **Alternative Installation Methods**:
        A. Via git (latest version):
              - pip install git+https://github.com/pygame/pygame

        B. For Linux/Ubuntu:
             - sudo apt-get install python3-pygame

    • **Recommended Python Versions**:
             - 2.0+ (recommended).
             - 3.6 and above (mandatory).

    • Example audio playback test:

        try:
            mixer.Sound("test_audio.mp3")
    
            print("Audio file played")
        except Exception:
            print("Audio files need checking").

         - Use the Sound method to quickly play "audio_track.mp3" - replace with a real audio file.
        - Print a message if the file is played: print("Audio file played"). If not: print("Audio files need checking").

    • **Dependency Checks**:
         A. - pip list | grep pygame
         - python -c "import pygame; print(pygame.__version__)".

        B. For Windows:
             - Ensure [Visual C++ Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe) is installed.
            - Check Python PATH in system variables.

        C. For Linux:
              - Additional dependencies may be required:
              a. For Ubuntu/Debian:
                   - sudo apt-get install libsdl2-mixer-2.0-0.

        D. Fedora:
              - sudo dnf install SDL2_mixer.

# 🔍 Diagnostics and Troubleshooting:
    A. If Pygame installation fails:
        - Update pip: python -m pip install --upgrade pip

    B. Try a specific version: 
        - pip install pygame == 2.0.1
        - Check compatibility of Python and Pygame versions.

    • If audio doesn't play:
        - Check file formats — only .wav, .mp3, .ogg.
        - Ensure access rights to audio files.
        - Check system audio drivers.

    • Common errors:
        - If mixer initialization error occurs:

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
***

Section 5: 📒 Links and Literature:
***
# 🧱 Materials:
- [Official Pygame Documentation](https://www.pygame.org/docs/).
- [Pygame GitHub Repository](https://github.com/pygame/pygame).
- [Pygame Support Forum](https://stackoverflow.com/questions/tagged/pygame).
- [NorthBastion Documentation](https://github.com/YarosIskov/NorthBastion).

# 📕 Literature:
- Making Games with Python & Pygame: Al Sweigart.

- Beginning Game Development with Python and Pygame: From Novice to Professional: Will McGugan.

- Invent Your Own Computer Games with Python: Al Sweigart.
***

02/09/2025, YarosIskov2005, verrysillvereagle@gmail.com.
[file content end]

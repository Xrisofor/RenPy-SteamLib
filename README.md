# RenPy SteamLib

**RenPy SteamLib** is a utility module for the Ren'Py engine, designed to simplify and speed up Steam API integration. The library is based on the official [steamapi.py](https://github.com/renpy/renpy-build/blob/master/steamapi/steamapi.py) and provides access to core Steam features necessary for integrating your game into the Steam ecosystem.

## ⚙️ Features
The module includes convenient wrappers for the following Steam APIs:
* SteamUtils — retrieve AppID, check for Steam China launcher, etc.
* SteamFriends — manage Rich Presence (display user status to friends)
* SteamApps — check for subscriptions, DLC info, app ownership, beta branches, and more
* SteamUserStats — work with achievements, leaderboards, and global statistics
It also supports opening URLs via Steam Overlay (`steam_web_overlay`).

## 🚧 Development Status
⚠️ This module is currently under active development.
Some functions may be unstable, partially implemented, or missing. Bugs and missing features will be addressed in future updates.

Features that are already available in Ren'Py (such as `achievement.register`, `achievement.grant`, `achievement.progress`, etc.) are not yet included in this module, but may be supported through wrappers or tighter integration in the future.

Additionally, Ren'Py includes a built-in `_renpysteam` module that provides useful Steam-related functionality not covered by `_steamlib`, and can be used alongside it:

Examples of functions available via `_renpysteam`:
* `_renpysteam.install_dlc(dlc_id)` — initiates installation of a DLC by ID
* `_renpysteam.dlc_progress()` — returns the DLC installation progress
* `_renpysteam.get_account_id()` — returns the current user's Steam Account ID
These functions are called separately but can complement SteamLib usage.

## 📖 Documentation
📚 Please check the project's Wiki for a complete list of available functions, usage examples, and detailed API descriptions. This will help you integrate the module into your Ren'Py project more effectively.

## 🔧 Getting Started
The module automatically initializes Steam when the game launches (except on mobile platforms). Steam Overlay link support is enabled via a hyperlink handler

## 📌 Calling Functions
All Steam API functions are accessed via the `_steamlib` namespace. You can call them directly from Ren'Py script or Python blocks:
```python
# Get the game's AppID
$ app_id = _steamlib.get_app_id()

# Set Rich Presence status
$ _steamlib.set_rich_presence("status", "Chapter 1: Beginning")

# Check if Steam China launcher is used
$ is_china = _steamlib.is_steam_china_launcher()

# Get number of achievements
$ achievements_total = _steamlib.get_num_achievements()
```

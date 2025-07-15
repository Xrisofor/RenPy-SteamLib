# RenPy SteamLib

**RenPy SteamLib** is a utility module for the Ren'Py engine, designed to simplify and speed up Steam API integration. The library is based on the official [steamapi.py](https://github.com/renpy/renpy-build/blob/master/steamapi/steamapi.py) and provides access to core Steam features necessary for integrating your game into the Steam ecosystem.

## ⚙️ Features
The module includes convenient wrappers for the following Steam APIs:
* SteamUtils - retrieve AppID, check for Steam China launcher, etc.
* SteamFriends - manage Rich Presence (display user status to friends)
* SteamApps - check for subscriptions, DLC info, app ownership, beta branches, and more
* SteamUser - retrieve SteamID, check login status, and more
* SteamUserStats - work with achievements, leaderboards, and global statistics
* SteamMusic / SteamMusicRemote - control Steam music playback or register your own music player
* SteamRemoteStorage - access and manage Steam Cloud files (read/write, quota, file sync)
* SteamUGC – browse, upload, subscribe, and manage Workshop content

It also supports opening URLs via Steam Overlay (`steam_web_overlay`).

## 🧩 Structured API Access
All functions are organized into classes that correspond to their original Steam API groups, with the Steam prefix omitted for simplicity. You’ll find them under the `_steamlib` namespace:

Class Name | Based On | Description
-- | -- | --
`utils` | `SteamUtils` | Utility functions (AppID, launcher checks)
`apps` | `SteamApps` | App info, DLCs, installation
`friends` | `SteamFriends` | Rich Presence, friend-related features
`user` | `SteamUser` | User identity and login status
`user_stats` | `SteamUser` | Achievements, stats, leaderboards
`music` | `SteamMusic` | Control Steam music playbac
`music_remote` | `SteamMusicRemote` | Act as a custom music player
`remote_storage` | `SteamRemoteStorage` | Steam Cloud save management
`ugc` | `SteamUGC` | Workshop item queries, uploads, subscriptions, metadata

## 🧩 About `_renpysteam` Integration
The module includes lightweight wrapper functions that internally use Ren'Py’s native `_renpysteam` API. These wrappers expose DLC installation, account ID retrieval, and other system-level Steam features through a unified `_steamlib` interface. You don’t need to call `_renpysteam` directly - just use the provided function in `_steamlib`.

## 🚧 Development Status
⚠️ This module is currently under active development.
Some functions may be unstable, partially implemented, or missing. Bugs and missing features will be addressed in future updates.

Features that are already available in Ren'Py (such as `achievement.register`, `achievement.grant`, `achievement.progress`, etc.) are not yet included in this module, but may be supported through wrappers or tighter integration in the future.

## 📖 Documentation
📚 Please check the project's Wiki for a complete list of available functions, usage examples, and detailed API descriptions. This will help you integrate the module into your Ren'Py project more effectively.

## 🔧 Getting Started
The module automatically initializes Steam when the game launches (except on mobile platforms). Steam Overlay link support is enabled via a hyperlink handler

## 📌 Calling Functions
All Steam API functions are accessed via the `_steamlib` namespace. You can call them directly from Ren'Py script or Python blocks:
```python
# Get the game's AppID
$ app_id = _steamlib.utils.get_app_id()

# Install a DLC using a wrapper for _renpysteam
$ _steamlib.apps.install_dlc(123456)

# Set Rich Presence status
$ _steamlib.friends.set_rich_presence("status", "Chapter 1: Beginning")

# Check if Steam China launcher is used
$ is_china = _steamlib.utils.is_steam_china_launcher()

# Get number of achievements
$ achievements_total = _steamlib.user_stats.get_num_achievements()

# Get Steam User Name
$ username = _steamlib.friends.get_persona_name()
```

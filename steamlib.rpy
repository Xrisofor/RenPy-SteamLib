# The script created Xrisofor
# Script version: 0.3.0
# GitHub link: https://github.com/Xrisofor

init python:
    config.hyperlink_handlers['steam_web_overlay'] = _steamlib.friends.activate_overlay_to_web_page

    if not renpy.variant("mobile"):
        _steamlib.steam_init()

init -1499 python in _steamlib:
    import steamapi, ctypes, time, _renpysteam
    from ctypes import byref, c_bool, create_string_buffer

    def steam_init():
        error_message = ctypes.create_string_buffer(1024)
        init_result = steamapi.InitFlat(error_message)
        
        if init_result.value != 0:
            return False

        return True

    class utils:
        """
        Interface which provides access to a range of miscellaneous utility functions.
        """

        @staticmethod
        def get_app_id():
            """
            Gets the AppID of the current process.
            """

            return steamapi.SteamUtils().GetAppID()

        @staticmethod
        def is_steam_china_launcher():
            """
            Returns whether the current launcher is the Steam China version. You can make the client
            work as a Steam China launcher by adding dev -steamchina to the command line when Steam starts.
            """
            return steamapi.SteamUtils().IsSteamChinaLauncher()

        @staticmethod
        def is_overlay_enabled():
            """
            Returns true if the steam overlay is enabled. (This might take a while to
            return true once the game starts.)
            """

            return _renpysteam.is_overlay_enabled()

        @staticmethod
        def set_overlay_notification_position(position):
            """
            Sets the position of the steam overlay. `Position` should be one of
            achievement.steam.POSITION_TOP_LEFT, .POSITION_TOP_RIGHT, .POSITION_BOTTOM_LEFT,
            or .POSITION_BOTTOM_RIGHT.
            """

            _renpysteam.set_overlay_notification_position(position)

    class friends:
        """
        Interface to access information about individual users and interact with the Steam Overlay.
        """

        @staticmethod
        def get_persona_state():
            """
            Retrieves the status of the current user.
            """

            return steamapi.SteamFriends().GetPersonaState()

        @staticmethod
        def get_persona_name():
            """
            Returns the user's publicly-visible name.
            """

            return _renpysteam.get_persona_name()

        @staticmethod
        def set_rich_presence(pchKey, pchValue):
            """
            Sets the key-value pair of the extended status of the current user, which is
            automatically sent to all friends playing the same game.
            Each user can have up to 20 keys, as defined in k_cchmaxrichpresenckeys.
            Additional important information: https://partner.steamgames.com/doc/api/ISteamFriends#SetRichPresence
            """

            try:
                return steamapi.SteamFriends().SetRichPresence(pchKey.encode('utf-8'), pchValue.encode('utf-8'))
            except:
                print("Unable to update Rich Presence, please try again later")

        @staticmethod
        def clear_rich_presence():
            """
            Deletes the key-value pairs of the extended status of the current user.
            """

            try:
                steamapi.SteamFriends().ClearRichPresence()
            except:
                print("Unable to clear Rich Presence, please try again later")

        @staticmethod
        def activate_overlay(dialog):
            """
            Activates the Steam overlay.

            `dialog`
                The dialog to open the overlay to. One of "Friends", "Community",
                "Players", "Settings", "OfficialGameGroup", "Stats", "Achievements"
            """

            _renpysteam.activate_overlay(dialog)

        @staticmethod
        def activate_overlay_to_web_page(url):
            """
            Activates the Steam overlay, and opens the web page at `url`.
            """

            _renpysteam.activate_overlay_to_web_page(url)

        @staticmethod
        def activate_overlay_to_store(appid, flag=None):
            """
            Opens the steam overlay to the store.

            `appid`
                The appid to open.

            `flag`
                One of achievement.steam.STORE_NONE, .STORE_ADD_TO_CART, or .STORE_ADD_TO_CART_AND_SHOW.
            """

            _renpysteam.activate_overlay_to_store(appid, flag)

    class apps:
        """
        Exposes a wide range of information and actions for applications and Downloadable Content (DLC).
        """
        
        @staticmethod
        def is_subscribed_app(appid):
            """
            Checks if the active user is subscribed to a specified AppId.
            Only use this if you need to check ownership of another game related to yours, a demo for example.
            """

            return _renpysteam.is_subscribed_app(appid)

        @staticmethod
        def is_subscribed_from_family_sharing():
            """
            Checks whether an active user is using a Family Library Sharing license owned by another user to access the current AppID.
            """

            return steamapi.SteamApps().BIsSubscribedFromFamilySharing()

        @staticmethod
        def is_subscribed_from_free_weekend():
            """
            Checks whether an active user is subscribed to the current AppID as part of the "Free Weekend" promotion.
            """

            return steamapi.SteamApps().BIsSubscribedFromFreeWeekend()

        @staticmethod
        def get_app_owner():
            """
            Gets the SteamID of the original owner of the current application. If the owner and the current user are different, the application is borrowed.
            """

            return steamapi.SteamApps().GetAppOwner()

        @staticmethod
        def get_current_game_language():
            """
            Gets the current language that the user has set.
            This falls back to the Steam UI language if the user hasn't explicitly picked a language for the title.
            """

            return _renpysteam.get_current_game_language()

        @staticmethod
        def get_available_game_languages():
            """
            Gets a comma-separated list of languages supported by the current application.
            """
            return steamapi.SteamApps().GetAvailableGameLanguages().decode("utf-8")

        @staticmethod
        def get_steam_ui_language():
            """
            Return the name of the language the steam UI is using.
            """

            return _renpysteam.get_steam_ui_language()

        @staticmethod
        def get_launch_command_line():
            """
            Gets the command line if the game is launched via a link to Steam,
            for example: steam://run/<appid>//<command line>/. This method is preferable to
            running from the command line through the operating system, which may threaten
            the security of the account. To ensure that this method works when logging in using
            extended statuses without placing it on the OS command line, you need to enable the
            option to use the launch command line from the Installation > General page of your
            application.
            """

            buffer_size = 4096
            buffer = create_string_buffer(buffer_size)

            result = steamapi.SteamApps().GetLaunchCommandLine(buffer, buffer_size)

            if result > 0:
                return buffer.value.decode("utf-8")
            else:
                return None

        @staticmethod
        def get_current_beta_name():
            """
            Returns the name of the current beta, or None if it can't.
            """

            return _renpysteam.get_current_beta_name()

        @staticmethod
        def set_active_beta(betaname):
            """
            Select an beta branch for this app as active, might need the game to restart so Steam can update its' content that branch.
            """

            return steamapi.SteamApps().SetActiveBeta(get_app_id(), betaname.encode("utf-8"))

        @staticmethod
        def get_dlc_count():
            """
            Returns the number of additional content elements for the current application.
            """
            
            return steamapi.SteamApps().GetDLCCount()

        @staticmethod
        def dlc_installed(appid):
            """
            Returns True if `dlc` is installed, or False otherwise.
            """

            return _renpysteam.dlc_installed(appid)

        @staticmethod
        def install_dlc(appid):
            """
            Requests the DLC with `appid` be installed.
            """

            _renpysteam.install_dlc(appid)

        @staticmethod
        def uninstall_dlc(appid):
            """
            Requests that the DLC with `appid` be uninstalled.
            """

            _renpysteam.uninstall_dlc(appid)

        @staticmethod
        def dlc_progress(appid):
            """
            Reports the progress towards DLC download completion.
            """

            return _renpysteam.dlc_progress(appid)

        @staticmethod
        def get_app_build_id():
            """
            Returns the build ID of the installed game.
            """

            return _renpysteam.get_app_build_id()

    class user:
        """
        Functions for accessing and manipulating Steam user information.
        """

        @staticmethod
        def get_csteam_id():
            """
            Returns the user's full CSteamID as a 64-bit number.
            """
            return _renpysteam.get_csteam_id()

        @staticmethod
        def get_account_id():
            """
            Returns the user's account ID.
            """
            return _renpysteam.get_account_id()

        @staticmethod
        def get_game_badge_level(series, foil):
            """
            Gets the level of the users Steam badge for your game.
            """

            return _renpysteam.get_game_badge_level(series, foil)

    class user_stats:
        """
        Provides functions for accessing and submitting stats, achievements, and leaderboards.
        """

        @staticmethod
        def retrieve_stats():
            """
            Retrieves achievements and statistics from Steam.
            """
            """
            `callback` will be
            called with no parameters if and when the statistics become available.
            """

            _renpysteam.retrieve_stats()

        @staticmethod
        def store_stats():
            """
            Stores statistics and achievements on the Steam server.
            """

            _renpysteam.store_stats()

        @staticmethod
        def indicate_achievement_progress(name, cur_progress, max_progress):
            """
            Indicates achievement progress to the user. This does *not* unlock the
            achievement.
            """

            return _renpysteam.indicate_achievement_progress(name, cur_progress, max_progress)

        @staticmethod
        def find_leaderboard(leaderboardName):
            """
            Gets a list of leaders by name.
            """

            find_leaderboard_callback = steamapi.SteamUserStats().FindLeaderboard(leaderboardName.encode('utf-8'))
            time.sleep(0.5)
            return steamapi.get_api_call_result(find_leaderboard_callback, steamapi.LeaderboardFindResult_t)

        @staticmethod
        def find_or_create_leaderboard(leaderboardName):
            """
            Gets the leaderboard by name, and if it doesn't exist yet, it will be created.
            """

            find_or_create_leaderboard_callback = steamapi.SteamUserStats().FindOrCreateLeaderboard(leaderboardName.encode('utf-8'), steamapi.k_ELeaderboardSortMethodDescending, steamapi.k_ELeaderboardDisplayTypeNumeric)
            time.sleep(0.5)
            return steamapi.get_api_call_result(find_or_create_leaderboard_callback, steamapi.LeaderboardFindResult_t)

        @staticmethod
        def get_leaderboard_entry_count(leaderboard):
            """
            Returns the full number of positions in the leaderboard.
            """

            return steamapi.SteamUserStats().GetLeaderboardEntryCount(leaderboard)

        @staticmethod
        def get_leaderboard_name(leaderboard):
            """
            Returns the name of the leaderboard.
            """

            return steamapi.SteamUserStats().GetLeaderboardName(leaderboard).decode('utf-8')

        @staticmethod
        def upload_leaderboard_score(leaderboard, score):
            """
            Sends the user's account to the specified leaderboard.
            """

            upload_leaderboard_score_callback = steamapi.SteamUserStats().UploadLeaderboardScore(leaderboard, steamapi.k_ELeaderboardUploadScoreMethodKeepBest, score, None, 0)
            return steamapi.get_api_call_result(upload_leaderboard_score_callback, steamapi.LeaderboardScoreUploaded_t)

        @staticmethod
        def get_number_of_current_players():
            """
            Asynchronously retrieves the total number of users currently playing this game, both online and offline.
            """

            return steamapi.SteamUserStats().GetNumberOfCurrentPlayers()

        @staticmethod
        def grant_achievement(name):
            """
            Grants the achievement with `name`. Call :func:`_renpysteam.store_stats` to
            push this change to the server.
            """

            return _renpysteam.SetAchievement(name.encode("utf-8"))

        @staticmethod
        def clear_achievement(name):
            """
            Clears the achievement with `name`. Call :func:`_renpysteam.store_stats` to
            push this change to the server.
            """

            return _renpysteam.ClearAchievement(name.encode("utf-8"))

        @staticmethod
        def get_achievement(name):
            """
            Gets the state of the achievements with `name`. This returns True if the
            achievement has been granted, False if it hasn't, and None if the achievement
            is unknown or an error occurs.
            """

            return _renpysteam.get_achievement(name)

        @staticmethod
        def get_achievement_icon(name):
            """
            Gets the achievement icon.
            """

            return steamapi.SteamUserStats().GetAchievementIcon(name.encode("utf-8"))

        @staticmethod
        def get_achievement_progress(name):
            """
            Gets the current progress towards the specified achievement.
            """
            return _renpysteam.get_achievement_progress(name)

        @staticmethod
        def get_achievement_achieved_percent(pchName):
            """
            Returns the percentage of users who received the specified achievement.
            """

            rv = c_bool(False)

            if not steamapi.SteamUserStats().GetAchievementAchievedPercent(pchName.encode("utf-8"), byref(rv)):
                return None

            return rv.value

        @staticmethod
        def get_achievement_name(iAchievement):
            """
            Gets the "API Name" by the achievement index between 0 and GetNumAchievements.
            """

            return steamapi.SteamUserStats().GetAchievementName(iAchievement).decode("utf-8")

        @staticmethod
        def get_num_achievements():
            """
            Gets the number of achievements defined in the partner site administration panel.
            """

            return steamapi.SteamUserStats().GetNumAchievements()

        @staticmethod
        def get_user_achievement(user, pchName):
            """
            Gets the unblocking status of an achievement from a specific user.
            """

            rv = c_bool(False)

            if not steamapi.SteamUserStats().GetUserAchievement(user, pchName.encode("utf-8"), byref(rv)):
                return None

            return rv.value

        @staticmethod
        def request_global_achievement_percentages():
            """
            synchronously receives data on the percentage of players who have
            globally received each of the achievements of this game.
            """

            steamapi.SteamUserStats().RequestGlobalAchievementPercentages()

        @staticmethod
        def reset_all_stats(achievements_too=False):
            """
            Resets the statistics of the current user and, optionally, achievements.
            """

            return steamapi.SteamUserStats().ResetAllStats(achievements_too)

    class remote_storage:
        """
        Provides functions for reading, writing, and accessing files which can be stored remotely in the Steam Cloud.
        """

        @staticmethod
        def file_write(filename, data):
            """
            Creates a new file, writes the bytes to the file, and then closes the file. If the target file already exists, it is overwritten.
            """

            return steamapi.SteamRemoteStorage().FileWrite(filename.encode("utf-8"), data, len(data))

        @staticmethod
        def read_cloud_file(filename):
            """
            Opens a binary file, reads the contents of the file into a byte array, and then closes the file.
            """

            if not steamapi.SteamRemoteStorage().FileExists(filename.encode("utf-8")):
                return None
            size = steamapi.SteamRemoteStorage().GetFileSize(filename.encode("utf-8"))
            buffer = create_string_buffer(size)
            steamapi.SteamRemoteStorage().FileRead(filename.encode("utf-8"), buffer, size)
            return buffer.raw

        @staticmethod
        def file_exists(filename):
            """
            Checks whether the specified file exists.
            """

            return steamapi.SteamRemoteStorage().FileExists(filename.encode("utf-8"))

        @staticmethod
        def delete_file(filename):
            """
            Deletes a file from the local disk, and propagates that delete to the cloud.

            This is meant to be used when a user actively deletes a file. Use `_steamlib.file_forget` if you want to remove a file from the Steam Cloud but retain it on the users local disk.

            When a file has been deleted it can be re-written with `_steamlib.file_write` to reupload it to the Steam Cloud.
            """

            return steamapi.SteamRemoteStorage().FileDelete(filename.encode("utf-8"))

        @staticmethod
        def file_forget(filename):
            """
            Deletes the file from remote storage, but leaves it on the local disk and remains accessible from the API.

            When you are out of Cloud space, this can be used to allow calls to `_steamlib.file_write` to keep working without needing to make the user delete files.

            How you decide which files to forget are up to you. It could be a simple Least Recently Used (LRU) queue or something more complicated.
            """

            return steamapi.SteamRemoteStorage().FileForget(filename.encode("utf-8"))

        @staticmethod
        def get_file_size(filename):
            """
            Gets the specified files size in bytes.
            """

            return steamapi.SteamRemoteStorage().GetFileSize(filename.encode("utf-8"))

        @staticmethod
        def get_file_timestamp(filename):
            """
            Gets the specified file's last modified timestamp in Unix epoch format (seconds since Jan 1st 1970).
            """

            return steamapi.SteamRemoteStorage().GetFileTimestamp(filename.encode("utf-8"))

        @staticmethod
        def list_cloud_files():
            """
            Lists all files stored in the Steam Cloud.
            """

            storage = steamapi.SteamRemoteStorage()
            file_count = storage.GetFileCount()
            result = []
            for i in range(file_count):
                name = storage.GetFileNameAndSize(i, None)
                result.append(name.decode("utf-8"))
            return result

    class music:
        """
        Functions to control music playback in the steam client.

        This gives games the opportunity to do things like pause the music or lower the volume, when an important cut scene is shown, and start playing afterwards.
        """

        @staticmethod
        def is_enabled():
            """
            Checks if Steam Music is enabled.
            """

            return steamapi.SteamMusic().IsEnabled()

        @staticmethod
        def is_playing():
            """
            Checks if Steam Music is active. This does not necessarily a song is currently playing, it may be paused.

            For finer grain control use GetPlaybackStatus.
            """

            return steamapi.SteamMusic().IsPlaying()

        @staticmethod
        def get_playback_status():
            """
            Gets the current status of the Steam Music player.
            Returns one of: "Undefined", "Playing", "Paused", "Idle".
            """

            status_obj = steamapi.SteamMusic().GetPlaybackStatus()
            
            try:
                status = status_obj.value
            except AttributeError:
                try:
                    status = int(status_obj)
                except Exception:
                    return str(status_obj)

            return status

        @staticmethod
        def get_volume():
            """
            Gets the current volume of the Steam Music player.
            """

            return steamapi.SteamMusic().GetVolume()

        @staticmethod
        def play():
            """
            Have the Steam Music player resume playing.
            """

            steamapi.SteamMusic().Play()

        @staticmethod
        def pause():
            """
            Pause the Steam Music player.
            """

            steamapi.SteamMusic().Pause()

        @staticmethod
        def play_next():
            """
            Have the Steam Music player skip to the next song.
            """

            steamapi.SteamMusic().PlayNext()

        @staticmethod
        def play_previous():
            """
            Have the Steam Music player play the previous song.
            """

            steamapi.SteamMusic().PlayPrevious()

        @staticmethod
        def set_volume(volume):
            """
            Sets the volume of the Steam Music player.
            """

            steamapi.SteamMusic().SetVolume(volume)

    class music_remote:
        """
        Allows direct interaction with the Steam Music player.
        """

        @staticmethod
        def activation_success(value):
            return steamapi.SteamMusicRemote().BActivationSuccess(value)

        @staticmethod
        def is_current_music_remote():
            return steamapi.SteamMusicRemote().IsCurrentMusicRemote()

        @staticmethod
        def current_entry_is_available(available):
            return steamapi.SteamMusicRemote().CurrentEntryIsAvailable(available)

        @staticmethod
        def current_entry_did_change():
            return steamapi.SteamMusicRemote().CurrentEntryDidChange()

        @staticmethod
        def current_entry_will_change():
            return steamapi.SteamMusicRemote().CurrentEntryWillChange()

        @staticmethod
        def deregister_steam_music_remote():
            return steamapi.SteamMusicRemote().DeregisterSteamMusicRemote()

        @staticmethod
        def enable_looped(value):
            return steamapi.SteamMusicRemote().EnableLooped(value)

        @staticmethod
        def enable_playlists(value):
            return steamapi.SteamMusicRemote().EnablePlaylists(value)

        @staticmethod
        def enable_play_next(value):
            return steamapi.SteamMusicRemote().EnablePlayNext(value)

        @staticmethod
        def enable_play_previous(value):
            return steamapi.SteamMusicRemote().EnablePlayPrevious(value)

        @staticmethod
        def enable_queue(value):
            return steamapi.SteamMusicRemote().EnableQueue(value)

        @staticmethod
        def enable_shuffled(value):
            return steamapi.SteamMusicRemote().EnableShuffled(value)

        @staticmethod
        def playlist_did_change():
            return steamapi.SteamMusicRemote().PlaylistDidChange()

        @staticmethod
        def playlist_will_change():
            return steamapi.SteamMusicRemote().PlaylistWillChange()

        @staticmethod
        def queue_did_change():
            return steamapi.SteamMusicRemote().QueueDidChange()

        @staticmethod
        def queue_will_change():
            return steamapi.SteamMusicRemote().QueueWillChange()
        
        @staticmethod
        def register_steam_music_remote(name):
            return steamapi.SteamMusicRemote().RegisterSteamMusicRemote(name.encode('utf-8'))

        @staticmethod
        def reset_playlist_entries():
            return steamapi.SteamMusicRemote().ResetPlaylistEntries()

        @staticmethod
        def reset_queue_entries():
            return steamapi.SteamMusicRemote().ResetQueueEntries()

        @staticmethod
        def set_queue_entry(id, position, entry_text):
            return steamapi.SteamMusicRemote().SetQueueEntry(id, position, entry_text.encode('utf-8'))

        @staticmethod
        def set_current_queue_entry(id):
            return steamapi.SteamMusicRemote().SetCurrentQueueEntry(id)

        @staticmethod
        def set_display_name(name):
            return steamapi.SteamMusicRemote().SetDisplayName(name.encode('utf-8'))
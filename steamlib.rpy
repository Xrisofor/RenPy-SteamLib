# The script created Xrisofor
# Script version: 0.4.1
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

        @staticmethod
        def is_api_call_completed(call):
            """
            Checks if an API Call is completed. Provides the backend of the CallResult wrapper.

            It's generally not recommended that you use this yourself.
            """

            failed = ctypes.c_bool(False)

            completed = steamapi.SteamUtils().IsAPICallCompleted(
                call,
                ctypes.byref(failed)
            )

            return completed, failed.value

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
        def set_rich_presence(key, value):
            """
            Sets the key-value pair of the extended status of the current user, which is
            automatically sent to all friends playing the same game.
            Each user can have up to 20 keys, as defined in k_cchmaxrichpresenckeys.
            Additional important information: https://partner.steamgames.com/doc/api/ISteamFriends#SetRichPresence
            """

            try:
                return steamapi.SteamFriends().SetRichPresence(key.encode('utf-8'), value.encode('utf-8'))
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

            callback = steamapi.SteamUserStats().FindLeaderboard(leaderboardName.encode('utf-8'))

            while True:
                is_done, has_failed = utils.is_api_call_completed(callback)

                if is_done:
                    if has_failed:
                        raise RuntimeError("Steam API call failed during FindLeaderboard")
                    break

                time.sleep(0.01)

            return steamapi.get_api_call_result(callback, steamapi.LeaderboardFindResult_t)

        @staticmethod
        def find_or_create_leaderboard(leaderboardName):
            """
            Gets the leaderboard by name, and if it doesn't exist yet, it will be created.
            """

            callback = steamapi.SteamUserStats().FindOrCreateLeaderboard(leaderboardName.encode('utf-8'), steamapi.k_ELeaderboardSortMethodDescending, steamapi.k_ELeaderboardDisplayTypeNumeric)

            while True:
                is_done, has_failed = utils.is_api_call_completed(callback)

                if is_done:
                    if has_failed:
                        raise RuntimeError("Steam API call failed during FindOrCreateLeaderboard")
                    break

                time.sleep(0.01)

            return steamapi.get_api_call_result(callback, steamapi.LeaderboardFindResult_t)

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

    class ugc:
        """
        Functions to create, consume, and interact with the Steam Workshop.
        """

        @staticmethod
        def show_workshop_eula():
            """
            Show the app's latest Workshop EULA to the user in an overlay window, where they can accept it or not.
            """

            return steamapi.SteamUGC().ShowWorkshopEULA()

        @staticmethod
        def get_workshop_eula_status():
            """
            Asynchronously retrieves data about whether the user accepted the Workshop EULA for the current app.
            """

            callback = steamapi.SteamUGC().GetWorkshopEULAStatus()

            while True:
                is_done, has_failed = utils.is_api_call_completed(callback)

                if is_done:
                    if has_failed:
                        raise RuntimeError("Steam API call failed during GetWorkshopEULAStatus")
                    break

                time.sleep(0.01)

            return steamapi.get_api_call_result(callback, steamapi.WorkshopEULAStatus_t)

        @staticmethod
        def create_item():
            """
            Creates a new workshop item with no content attached yet.
            """

            callback = steamapi.SteamUGC().CreateItem(utils.get_app_id(), steamapi.k_EWorkshopFileTypeCommunity)

            while True:
                is_done, has_failed = utils.is_api_call_completed(callback)

                if is_done:
                    if has_failed:
                        raise RuntimeError("Steam API call failed during CreateItem")
                    break

                time.sleep(0.01)

            return steamapi.get_api_call_result(callback, steamapi.CreateItemResult_t)

        @staticmethod
        def start_item_update(published_file_id):
            """
            Starts the item update process.

            This gets you a handle that you can use to modify the item before finally sending off the update to the server with SubmitItemUpdate.
            """

            return steamapi.SteamUGC().StartItemUpdate(utils.get_app_id(), published_file_id)

        @staticmethod
        def download_item(published_file_id, high_priority):
            """
            Download or update a workshop item.

            If the return value is true then register and wait for the Callback DownloadItemResult_t before calling GetItemInstallInfo or accessing the workshop item on disk.

            If the user is not subscribed to the item (e.g. a Game Server using anonymous login), the workshop item will be downloaded and cached temporarily.

            If the workshop item has an item state of k_EItemStateNeedsUpdate, then this function can be called to initiate the update. Do not access the workshop item on disk until the Callback DownloadItemResult_t is called.

            The DownloadItemResult_t callback contains the app ID associated with the workshop item. It should be compared against the running app ID as the handler will be called for all item downloads regardless of the running application.
            """

            return steamapi.SteamUGC().DownloadItem(published_file_id, high_priority)

        @staticmethod
        def delete_item(published_file_id):
            """
            Deletes the item without prompting the user.
            """

            callback = steamapi.SteamUGC().DeleteItem(published_file_id)

            while True:
                is_done, has_failed = utils.is_api_call_completed(callback)

                if is_done:
                    if has_failed:
                        raise RuntimeError("Steam API call failed during DeleteItem")
                    break

                time.sleep(0.01)

            return steamapi.get_api_call_result(callback, steamapi.DeleteItemResult_t)

        @staticmethod
        def set_item_title(handle, title):
            """
            Sets a new title for an item.

            The title must be limited to the size defined by k_cchPublishedDocumentTitleMax.

            You can set what language this is for by using SetItemUpdateLanguage, if no language is set then "english" is assumed.
            """

            return steamapi.SteamUGC().SetItemTitle(handle, title.encode("utf-8"))

        @staticmethod
        def set_item_update_language(handle, language):
            """
            Sets the language of the title and description that will be set in this item update.

            This must be in the format of the API language code.

            If this is not set then "english" is assumed.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemUpdateLanguage(handle, language.encode("utf-8"))

        @staticmethod
        def set_item_description(handle, description):
            """
            Sets a new description for an item.

            The description must be limited to the length defined by k_cchPublishedDocumentDescriptionMax.

            You can set what language this is for by using SetItemUpdateLanguage, if no language is set then "english" is assumed.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemDescription(handle, description.encode("utf-8"))

        @staticmethod
        def set_item_content(handle, content):
            """
            Sets the folder that will be stored as the content for an item.

            For efficient upload and download, files should not be merged or compressed into single files (e.g. zip files).

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemContent(handle, content.encode("utf-8"))

        @staticmethod
        def set_item_preview(handle, image):
            """
            Sets the primary preview image for the item.

            The format should be one that both the web and the application (if necessary) can render. Suggested formats include JPG, PNG and GIF.

            Be sure your app has its Steam Cloud quota and number of files set, as preview images are stored under the user's Cloud. If your app has no Cloud values set, this call will fail.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemPreview(handle, image.encode("utf-8"))

        @staticmethod
        def set_item_tags(handle, tags):
            """
            Sets arbitrary developer specified tags on an item.

            Each tag must be limited to 255 characters. Tag names can only include printable characters, excluding ','. For reference on what characters are allowed, refer to http://en.cppreference.com/w/c/string/byte/isprint

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemTags(handle, tags.encode("utf-8"))

        @staticmethod
        def set_item_metadata(handle, metadata):
            """
            Sets arbitrary metadata for an item. This metadata can be returned from queries without having to download and install the actual content.

            The metadata must be limited to the size defined by k_cchDeveloperMetadataMax.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemMetadata(handle, metadata.encode("utf-8"))

        @staticmethod
        def set_item_visibility(handle, visibility = steamapi.k_ERemoteStoragePublishedFileVisibilityPublic):
            """
            Sets the visibility of an item.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().SetItemVisibility(handle, visibility)

        @staticmethod
        def submit_item_update(handle, change_note = ""):
            """
            Uploads the changes made to an item to the Steam Workshop.

            You can track the progress of an item update with GetItemUpdateProgress.
            """

            callback = steamapi.SteamUGC().SubmitItemUpdate(handle, change_note.encode("utf-8"))

            while True:
                is_done, has_failed = utils.is_api_call_completed(callback)

                if is_done:
                    if has_failed:
                        raise RuntimeError("Steam API call failed during SubmitItemUpdate")
                    break

                time.sleep(0.01)

            return steamapi.get_api_call_result(callback, steamapi.SubmitItemUpdateResult_t)

        @staticmethod
        def add_item_preview_file(handle, preview_file, preview_type = steamapi.k_EItemPreviewType_Image):
            """
            Adds an additional preview file for the item.

            Then the format of the image should be one that both the web and the application (if necessary) can render and must be under 1MB. Suggested formats include JPG, PNG and GIF.

            NOTE: Using k_EItemPreviewType_YouTubeVideo or k_EItemPreviewType_Sketchfab are not currently supported with this API. For YouTube videos, you should use AddItemPreviewVideo.
            
            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().AddItemPreviewFile(handle, preview_file.encode("utf-8"), preview_type)

        @staticmethod
        def add_item_preview_video(handle, video_id):
            """
            Adds an additional video preview from YouTube for the item.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().AddItemPreviewVideo(handle, video_id.encode("utf-8"))

        @staticmethod
        def remove_item_preview(handle, index):
            return steamapi.SteamUGC().RemoveItemPreview(handle, index)

        @staticmethod
        def update_item_preview_file(handle, index, preview_file):
            """
            Updates an existing additional preview file for the item.

            If the preview type is an image then the format should be one that both the web and the application (if necessary) can render, and must be under 1MB. Suggested formats include JPG, PNG and GIF.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().UpdateItemPreviewFile(handle, index, preview_file.encode("utf-8"))

        @staticmethod
        def update_item_preview_video(handle, index, video_id):
            """
            Updates an additional video preview from YouTube for the item.

            NOTE: This must be set before you submit the UGC update handle using SubmitItemUpdate.
            """

            return steamapi.SteamUGC().UpdateItemPreviewVideo(handle, index, video_id.encode("utf-8"))

        @staticmethod
        def get_item_update_progress(handle, bytes_processed, bytes_total):
            """
            Gets the progress of an item update.
            """

            return steamapi.SteamUGC().GetItemUpdateProgress(handle, bytes_processed, bytes_total)

        @staticmethod
        def get_item_update_progress(handle):
            """
            Gets the progress of an item update.
            """

            bytes_processed = ctypes.c_uint64(0)
            bytes_total = ctypes.c_uint64(0)

            progress = steamapi.SteamUGC().GetItemUpdateProgress(
                handle,
                ctypes.byref(bytes_processed),
                ctypes.byref(bytes_total)
            )

            return progress, bytes_processed.value, bytes_total.value

        @staticmethod
        def get_query_ugc_num_additional_previews(handle, index):
            """
            Retrieve the number of additional previews of an individual workshop item after receiving a querying UGC call result.

            You should call this in a loop to get the details of all the workshop items returned.

            NOTE: This must only be called with the handle obtained from a successful SteamUGCQueryCompleted_t call result.

            You can then call GetQueryUGCAdditionalPreview to get the details of each additional preview.
            """

            return steamapi.SteamUGC().GetQueryUGCNumAdditionalPreviews(handle, index)

        @staticmethod
        def get_item_state(published_file_id):
            """
            Gets the current state of a workshop item on this client.
            """

            return steamapi.SteamUGC().GetItemState(published_file_id)

        @staticmethod
        def get_query_ugc_result(handle, index):
            """
            Retrieve the details of an individual workshop item after receiving a querying UGC call result.

            You should call this in a loop to get the details of all the workshop items returned.

            NOTE: This must only be called with the handle obtained from a successful SteamUGCQueryCompleted_t call result.
            """

            details = steamapi.SteamUGCDetails_t()

            success = steamapi.SteamUGC().GetQueryUGCResult(
                handle,
                index,
                ctypes.byref(details)
            )

            return success, details

        @staticmethod
        def get_num_subscribed_items():
            """
            Gets the total number of items the current user is subscribed to for the game or application. By default, this function will return exclude locally disabled items.
            """

            return steamapi.SteamUGC().GetNumSubscribedItems()

        @staticmethod
        def get_subscribed_items():
            """
            Gets a list of all of the items the current user is subscribed to for the current game, excluding any that have been locally disabled by the user.

            You create an array with the size provided by GetNumSubscribedItems before calling this.

            By default, the items are return in the order that user subscribed to them. Users can change the ordering in the Steam Client, or you can do so via the SetSubscriptionsLoadOrder call.
            """

            num_items = steamapi.SteamUGC().GetNumSubscribedItems()
            if num_items == 0:
                return []

            arr_type = ctypes.c_uint64 * num_items
            arr = arr_type()

            count = steamapi.SteamUGC().GetSubscribedItems(arr, num_items)

            return list(arr[:count])

        @staticmethod
        def get_item_download_info(handle):
            """
            Get info about a pending download of a workshop item that has k_EItemStateNeedsUpdate set.
            """

            bytes_processed = ctypes.c_uint64(0)
            bytes_total = ctypes.c_uint64(0)

            success = steamapi.SteamUGC().GetItemDownloadInfo(
                handle,
                ctypes.byref(bytes_processed),
                ctypes.byref(bytes_total)
            )

            return success, bytes_processed.value, bytes_total.value

        @staticmethod
        def get_item_install_info(published_file_id):
            """
            Gets info about currently installed content on the disc for workshop items that have k_EItemStateInstalled set.

            Calling this sets the "used" flag on the workshop item for the current player and adds it to their k_EUserUGCList_UsedOrPlayed list.

            If k_EItemStateLegacyItem is set then pchFolder contains the path to the legacy file itself, not a folder.
            """

            size_on_disk = ctypes.c_uint64(0)
            timestamp = ctypes.c_uint32(0)

            folder_buffer_size = 260
            folder_buffer = ctypes.create_string_buffer(folder_buffer_size)

            success = steamapi.SteamUGC().GetItemInstallInfo(
                published_file_id,
                ctypes.byref(size_on_disk),
                folder_buffer,
                folder_buffer_size,
                ctypes.byref(timestamp)
            )

            folder_path = folder_buffer.value.decode("utf-8") if success else ""

            return success, size_on_disk.value, folder_path, timestamp.value

        @staticmethod
        def create_query_user_ugc_request(user_list = steamapi.k_EUserUGCList_Subscribed, matching_type = steamapi.k_EUGCMatchingUGCType_Items, user_list_sort_order = steamapi.k_EUserUGCListSortOrder_CreationOrderDesc, page = 1):
            """
            Query UGC associated with a user. You can use this to list the UGC the user is subscribed to amongst other things.

            This will return up to 50 results as declared by kNumUGCResultsPerPage. You can make subsequent calls to this function, increasing the unPage each time to get the next set of results.

            NOTE: Either nConsumerAppID or nCreatorAppID must have a valid AppID!

            NOTE: You must release the handle returned by this function by calling ReleaseQueryUGCRequest when you are done with it!
            """

            return steamapi.SteamUGC().CreateQueryUserUGCRequest(
                user.get_account_id(),
                user_list,
                matching_type,
                user_list_sort_order,
                utils.get_app_id(),
                utils.get_app_id(),
                page
            )

        @staticmethod
        def release_query_ugc_request(handle):
            """
            Releases a UGC query handle when you are done with it to free up memory.
            """

            return steamapi.SteamUGC().ReleaseQueryUGCRequest(handle)

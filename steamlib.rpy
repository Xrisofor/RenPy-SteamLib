# The script created Xrisofor
# Script version: 0.2.0
# GitHub link: https://github.com/Xrisofor

init python:
    config.hyperlink_handlers['steam_web_overlay'] = _renpysteam.activate_overlay_to_web_page

    if not renpy.variant("mobile"):
        _steamlib.steam_init()

init -1499 python in _steamlib:

    import steamapi, ctypes, time

    def steam_init():
        error_message = ctypes.create_string_buffer(1024)
        init_result = steamapi.InitFlat(error_message)
        
        if init_result.value != 0:
            return False

        return True

    # SteamUtils

    def get_app_id():
        """
        :doc: steam_utils

        Gets the AppID of the current process.
        """
        return steamapi.SteamUtils().GetAppID()

    def is_steam_china_launcher():
        """
        :doc: steam_utils

        Returns whether the current launcher is the Steam China version. You can make the client
        work as a Steam China launcher by adding dev -steamchina to the command line when Steam starts.
        """
        return steamapi.SteamUtils().IsSteamChinaLauncher()

    # SteamFriends

    def get_persona_state():
        """
        Retrieves the status of the current user.
        """
        return steamapi.SteamFriends().GetPersonaState()

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

    def clear_rich_presence():
        """
        Deletes the key-value pairs of the extended status of the current user.
        """
        try:
            steamapi.SteamFriends().ClearRichPresence()
        except:
            print("Unable to clear Rich Presence, please try again later")

    # SteamApps

    def is_subscribed_from_family_sharing():
        """
        Checks whether an active user is using a Family Library Sharing license owned by another user to access the current AppID.
        """
        return steamapi.SteamApps().BIsSubscribedFromFamilySharing()

    def is_subscribed_from_free_weekend():
        """
        Checks whether an active user is subscribed to the current AppID as part of the "Free Weekend" promotion.
        """
        return steamapi.SteamApps().BIsSubscribedFromFreeWeekend()

    def get_app_owner():
        """
        Gets the SteamID of the original owner of the current application. If the owner and the current user are different, the application is borrowed.
        """
        return steamapi.SteamApps().GetAppOwner()

    def get_available_game_languages():
        """
        Gets a comma-separated list of languages supported by the current application.
        """
        return steamapi.SteamApps().GetAvailableGameLanguages().decode("utf-8")

    def get_dlc_count():
        """
        Returns the number of additional content elements for the current application.
        """
        return steamapi.SteamApps().GetDLCCount()

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
        from ctypes import byref, c_bool

        rv = c_bool(False)
        pint = 0

        if not steamapi.SteamApps().GetLaunchCommandLine(byref(rv).decode("utf-8"), pint):
            return None

        return rv.value

    def get_current_beta_name():
        from ctypes import create_string_buffer, byref

        rv = create_string_buffer(256)

        if not steamapi.SteamApps().GetCurrentBetaName(rv, 256):
            return None

        return rv.value.decode("utf-8")

    def set_active_beta(pchBetaName):
        return steamapi.SteamApps().SetActiveBeta(get_app_id(), pchBetaName.encode("utf-8"))

    # SteamUserStats

    def find_leaderboard(leaderboardName):
        """
        Gets a list of leaders by name.
        """
        find_leaderboard_callback = steamapi.SteamUserStats().FindLeaderboard(leaderboardName.encode('utf-8'))
        time.sleep(0.5)
        return steamapi.get_api_call_result(find_leaderboard_callback, steamapi.LeaderboardFindResult_t)

    def find_or_create_leaderboard(leaderboardName):
        """
        Gets the leaderboard by name, and if it doesn't exist yet, it will be created.
        """
        find_or_create_leaderboard_callback = steamapi.SteamUserStats().FindOrCreateLeaderboard(leaderboardName.encode('utf-8'), steamapi.k_ELeaderboardSortMethodDescending, steamapi.k_ELeaderboardDisplayTypeNumeric)
        time.sleep(0.5)
        return steamapi.get_api_call_result(find_or_create_leaderboard_callback, steamapi.LeaderboardFindResult_t)

    def get_leaderboard_entry_count(leaderboard):
        """
        Returns the full number of positions in the leaderboard.
        """
        return steamapi.SteamUserStats().GetLeaderboardEntryCount(leaderboard)

    def get_leaderboard_name(leaderboard):
        """
        Returns the name of the leaderboard.
        """
        return steamapi.SteamUserStats().GetLeaderboardName(leaderboard).decode('utf-8')

    def upload_leaderboard_score(leaderboard, score):
        """
        Sends the user's account to the specified leaderboard.
        """
        upload_leaderboard_score_callback = steamapi.SteamUserStats().UploadLeaderboardScore(leaderboard, steamapi.k_ELeaderboardUploadScoreMethodKeepBest, score, None, 0)
        return steamapi.get_api_call_result(upload_leaderboard_score_callback, steamapi.LeaderboardScoreUploaded_t)

    def get_number_of_current_players():
        """
        Asynchronously retrieves the total number of users currently playing this game, both online and offline.
        """
        return steamapi.SteamUserStats().GetNumberOfCurrentPlayers()

    def get_achievement_icon(pchName):
        """
        Gets the achievement icon.
        """
        return steamapi.SteamUserStats().GetAchievementIcon(pchName.encode("utf-8"))

    def get_achievement_display_attribute(pchName, pchKey = "name"):
        """
        Gets the general attributes of the achievement. Currently provides the following data: name, description and "stealth".
        
        This call gets the value from the dictionary/key-value pair map, so you have to send one of the following keys.
            "name" — to get the localized name of the achievement in UTF-8.
            "desc" — to get the localized description of the achievement in UTF-8.
            "hidden" — whether the achievement is hidden. Returns "0" if not hidden, and "1" if hidden.
        """
        return steamapi.SteamUserStats().GetAchievementDisplayAttribute(pchName.encode("utf-8"), pchKey.encode("utf-8"))

    def get_achievement_achieved_percent(pchName):
        """
        Returns the percentage of users who received the specified achievement.
        """
        from ctypes import byref, c_bool

        rv = c_bool(False)

        if not steamapi.SteamUserStats().GetAchievementAchievedPercent(pchName.encode("utf-8"), byref(rv)):
            return None

        return rv.value

    def get_achievement_name(iAchievement):
        """
        Gets the "API Name" by the achievement index between 0 and GetNumAchievements.
        """
        return steamapi.SteamUserStats().GetAchievementName(iAchievement).decode("utf-8")

    def get_num_achievements():
        """
        Gets the number of achievements defined in the partner site administration panel.
        """
        return steamapi.SteamUserStats().GetNumAchievements()

    def get_user_achievement(user, pchName):
        """
        Gets the unblocking status of an achievement from a specific user.
        """
        from ctypes import byref, c_bool

        rv = c_bool(False)

        if not steamapi.SteamUserStats().GetUserAchievement(user, pchName.encode("utf-8"), byref(rv)):
            return None

        return rv.value

    def request_global_achievement_percentages():
        """
        synchronously receives data on the percentage of players who have
        globally received each of the achievements of this game.
        """
        steamapi.SteamUserStats().RequestGlobalAchievementPercentages()

    def reset_all_stats(achievementsToo=False):
        """
        Resets the statistics of the current user and, optionally, achievements.
        """
        return steamapi.SteamUserStats().ResetAllStats(achievementsToo)
import sys, os, subprocess, re

# i pulled this code from
#   https://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment


def parse_de():
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if sys.platform in ["win32", "cygwin"]:
        return "windows"
    elif sys.platform == "darwin":
        return "mac"
    else:  # Most likely either a POSIX system or something not much common
        desktop_session = os.environ.get("DESKTOP_SESSION")
        if (
            desktop_session is not None
        ):  # easier to match if we doesn't have  to deal with caracter cases
            desktop_session = desktop_session.lower()
            if desktop_session in [
                "gnome",
                "unity",
                "cinnamon",
                "mate",
                "xfce4",
                "lxde",
                "fluxbox",
                "blackbox",
                "openbox",
                "icewm",
                "jwm",
                "afterstep",
                "trinity",
                "kde",
            ]:
                return desktop_session
            ## Special cases ##
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntustudio"):
                return "kde"
            elif desktop_session.startswith("ubuntu"):
                return "gnome"
            elif desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                return "kde"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "windowmaker"
        if os.environ.get("KDE_FULL_SESSION") == "true":
            # print("boop")
            # output = str(subprocess.run(["kinfo"], capture_output=True).stdout)
            # output = output[2:-1]
            # output = output.split(r"\n")
            # # print(output)  # debug
            # first_half = output[1].replace("Version: ", "")
            # # print(first_half)  # debug
            # second_half = output[5].replace("Graphics Platform: ", "")
            # output = f"{first_half} ({second_half})"

            # return output
            return "kde"
        elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
            if not "deprecated" in os.environ.get("GNOME_DESKTOP_SESSION_ID"):
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif is_running("xfce-mcs-manage"):
            return "xfce4"
        elif is_running("ksmserver"):
            return "kde"
    return "not found"


def is_running(process):
    # From http://www.bloggerpolis.com/2011/05/how-to-check-if-a-process-is-running-using-python/
    # and http://richarddingwall.name/2009/06/18/windows-equivalents-of-ps-and-kill-commands/
    try:  # Linux/Unix
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    except:  # Windows
        s = subprocess.Popen(["tasklist", "/v"], stdout=subprocess.PIPE)
    for x in s.stdout:
        x = str(x)
        if re.search(process, x):
            return True
    return False

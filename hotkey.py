"""The four global shortcuts, and whoever on this machine delivers them.

A global shortcut is the one thing Dikte cannot do for itself: something owned
by the session has to notice the key and say so. On Linux that is KDE or GNOME,
told about the combination through a file, with a built-in /dev/input listener
to cover the gap before the desktop reads it. On Windows it is RegisterHotKey,
which registers the combination with the system there and then and delivers it
as a window message.

The contract is the same either way:

    parse_shortcut(text)            is this combination one we could register
    Listener()                      catches the combinations in this process
    install_shortcut(...)           register one with the session
    remove_shortcut(id)             give it back
    shortcut_status(id)             what is registered now, or None
    conflicting_shortcuts(...)      who else wants that combination
    desktop_name()                  what to call the thing that owns them
"""

# Kept imported: the tests reach the tool lookup and the listener's thread
# through this module.
import shutil  # noqa: F401
import threading  # noqa: F401

from platforms import IS_MACOS, IS_WINDOWS, adapter
from platforms.common.shortcuts import (  # noqa: F401
    ASK_DESKTOP_ID,
    CANCEL_DESKTOP_ID,
    DESKTOP_ID,
    MEETING_DESKTOP_ID,
    SHORTCUTS,
    Shortcut,
)

_impl = adapter("hotkeys")

parse_shortcut = _impl.parse_shortcut
install_shortcut = _impl.install_shortcut
remove_shortcut = _impl.remove_shortcut
shortcut_status = _impl.shortcut_status
conflicting_shortcuts = _impl.conflicting_shortcuts
desktop_name = _impl.desktop_name

#: The class that catches the combinations from inside this process.
Listener = _impl.Listener

# Whether that listener is the only thing catching them, or a stopgap.
#
# On Windows it is the whole mechanism: RegisterHotKey is how a Windows program
# asks for a global shortcut, so the listener runs whenever Dikte does. On Linux
# it reads /dev/input behind the desktop's back, does not swallow the key, and
# needs the user in the `input` group, so it stays off unless asked for.
LISTENER_IS_PRIMARY = IS_WINDOWS or IS_MACOS

# Linux keeps a few of its own on show: the tests pin the KDE and GNOME halves
# separately, and the settings window names the desktop it wrote a file for.
EvdevHotkey = getattr(_impl, "EvdevHotkey", None)
install_kde_shortcut = getattr(_impl, "install_kde_shortcut", None)
remove_kde_shortcut = getattr(_impl, "remove_kde_shortcut", None)
kde_shortcut_status = getattr(_impl, "kde_shortcut_status", None)
gnome_accelerator = getattr(_impl, "gnome_accelerator", None)
display_accelerator = getattr(_impl, "display_accelerator", None)

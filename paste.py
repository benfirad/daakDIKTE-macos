"""The clipboard, and the key press that puts what is on it into a window.

Five functions, the same five everywhere: read what is on the clipboard, put
text or bytes onto it, say whether a key can be pressed at all, and press one.
A dictation ends here, so a failure at this point has to arrive as a sentence
somebody can act on rather than as silence, which is what PasteError carries.

Underneath, Linux shells out to wl-clipboard/ydotool or xclip/xdotool and
Windows talks to the Win32 clipboard and SendInput directly. Both live under
platforms/.
"""

# Kept imported: the tests reach the sleep and the tool lookup through this
# module, and both adapters use the same two.
import shutil  # noqa: F401
import time  # noqa: F401

from platforms import adapter

_impl = adapter("clipboard")

PasteError = _impl.PasteError

read_clipboard = _impl.read_clipboard
copy = _impl.copy
copy_bytes = _impl.copy_bytes
paste_ready = _impl.paste_ready
press = _impl.press
SHORTCUTS = _impl.SHORTCUTS
type_out = _impl.type_out

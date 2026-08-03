"""The native macOS adapters, exercised without touching real desktop state."""

import contextlib
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

from platforms.macos import audio, clipboard, hotkeys, runtime
from tests.support import DikteTest, FakeCompleted, only_these_tools


class MacAudio(DikteTest):
    LISTING = (
        "AVFoundation video devices:\n[0] FaceTime HD Camera\n"
        "AVFoundation audio devices:\n"
        "[0] MacBook Pro Microphone\n[1] BlackHole 2ch\n"
    )

    @contextlib.contextmanager
    def listing(self, stderr=None):
        result = FakeCompleted(returncode=1,
                               stderr=self.LISTING if stderr is None else stderr)
        with only_these_tools("ffmpeg"), \
                mock.patch.object(subprocess, "run", return_value=result):
            yield

    def test_only_audio_devices_are_listed_by_stable_name(self):
        with self.listing():
            self.assertEqual(
                audio.list_sources(),
                [("MacBook Pro Microphone", "MacBook Pro Microphone"),
                 ("BlackHole 2ch", "BlackHole 2ch")],
            )

    def test_a_loopback_device_is_selected_for_meetings(self):
        with self.listing():
            self.assertEqual(audio.default_monitor(), "BlackHole 2ch")
            self.assertEqual(audio.list_monitors(), audio.list_sources())

    def test_recording_uses_avfoundation_and_the_saved_device_name(self):
        with only_these_tools("ffmpeg"):
            command = audio.recording_command("USB Microphone")
        self.assertIn("avfoundation", command)
        self.assertIn(":USB Microphone", command)
        self.assertEqual(command[-2:], ["s16le", "-"])

    def test_missing_ffmpeg_is_an_actionable_failure(self):
        recorder = audio.Recorder()
        failures = []
        recorder.failed.connect(failures.append)
        with only_these_tools():
            recorder.start()
        self.assertIn("brew install ffmpeg", failures[0])


class FakeCoreGraphics:
    def __init__(self, trusted=True):
        self.trusted = trusted
        self.made, self.flags, self.posted, self.released = [], [], [], []

    def AXIsProcessTrusted(self):
        return self.trusted

    def CGEventCreateKeyboardEvent(self, _source, keycode, down):
        self.made.append((keycode, down))
        return 1000 + len(self.made)

    def CGEventSetFlags(self, event, flags):
        self.flags.append((event, flags))

    def CGEventPost(self, tap, event):
        self.posted.append((tap, event))

    def CFRelease(self, event):
        self.released.append(event)


class MacClipboard(DikteTest):
    def setUp(self):
        super().setUp()
        self.api = FakeCoreGraphics()
        self.patch_attr(clipboard, "_macos_api", lambda: (self.api, self.api))
        self.patch_attr(clipboard.time, "sleep", lambda _seconds: None)
        self.give_back = self.patch_attr(
            clipboard.macos, "give_the_keyboard_back", mock.Mock())
        self.type_text = self.patch_attr(
            clipboard.macos, "type_text", mock.Mock(return_value=True))

    def test_cmd_v_is_posted_by_physical_key_position(self):
        clipboard.press("cmd+v")
        self.assertEqual(self.api.made, [(9, True), (9, False)])
        self.assertEqual([flags for _event, flags in self.api.flags],
                         [clipboard.MAC_FLAGS["command"]] * 2)
        self.assertEqual(self.api.released, [1001, 1002])
        self.give_back.assert_called_once_with()

    def test_typing_mode_does_not_need_the_clipboard(self):
        clipboard.type_out("günaydın")
        self.type_text.assert_called_once_with("günaydın")
        self.give_back.assert_called_once_with()

    def test_accessibility_permission_is_checked_before_injection(self):
        self.api.trusted = False
        self.patch_attr(clipboard, "_ask_for_permission", mock.Mock())
        with self.assertRaises(clipboard.PasteError) as caught:
            clipboard.press("cmd+v")
        self.assertIn("Accessibility", str(caught.exception))
        self.assertEqual(self.api.posted, [])

    def test_native_clipboard_snapshot_files_are_removed_after_restore(self):
        temporary = tempfile.TemporaryDirectory(prefix="dikte-test-clipboard-")
        directory = temporary.name
        pathlib.Path(directory, "0-0.bin").write_bytes(b"a TIFF")
        snapshot = clipboard._MAC_SNAPSHOT(
            temporary, '[[{"type":"public.tiff","file":"0-0.bin"}]]')
        with mock.patch.object(subprocess, "run", return_value=FakeCompleted()):
            clipboard.copy_bytes(snapshot)
        self.assertFalse(pathlib.Path(directory).exists())


class MacHotkeys(DikteTest):
    def setUp(self):
        super().setUp()
        hotkeys._REGISTERED.clear()
        self.addCleanup(hotkeys._REGISTERED.clear)

    def test_mac_keyboard_names_and_positions_are_understood(self):
        modifiers, key = hotkeys.parse_shortcut("Cmd+Option+Space")
        self.assertEqual(modifiers,
                         hotkeys.MAC_MODS["cmd"] | hotkeys.MAC_MODS["option"])
        self.assertEqual(key, hotkeys.MAC_KEYS["space"])

    def test_invalid_or_ambiguous_shortcuts_are_refused(self):
        self.assertEqual(hotkeys.parse_shortcut("Cmd+F13"), (None, None))
        self.assertEqual(hotkeys.parse_shortcut("A+B"), (None, None))

    def test_install_and_remove_are_in_process_not_desktop_file_writes(self):
        with mock.patch.object(subprocess, "run") as run:
            ok, _message = hotkeys.install_shortcut(
                "Ctrl+Option+Space", "dikte toggle")
            self.assertTrue(ok)
            self.assertEqual(hotkeys.shortcut_status(), "Ctrl+Option+Space")
            hotkeys.remove_shortcut()
        run.assert_not_called()
        self.assertIsNone(hotkeys.shortcut_status())


class MacRuntime(unittest.TestCase):
    def test_application_data_uses_the_native_library_directories(self):
        self.assertEqual(runtime.config_dir(),
                         pathlib.Path.home() / "Library/Application Support/Dikte")
        self.assertEqual(runtime.cache_dir(),
                         pathlib.Path.home() / "Library/Caches/Dikte")

    def test_finder_is_used_to_open_a_folder(self):
        with mock.patch.object(runtime.shutil, "which", return_value="/usr/bin/open"), \
                mock.patch.object(runtime.subprocess, "Popen") as popen:
            self.assertTrue(runtime.open_folder("/tmp/example"))
        self.assertEqual(popen.call_args.args[0], ["open", "/tmp/example"])


if __name__ == "__main__":
    unittest.main()

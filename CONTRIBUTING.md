# Contributing

## Running the tests

```sh
python -m unittest discover          # all of them
python -m unittest tests.test_api    # one file
python -m unittest tests.test_api.Transcribe.test_no_key_at_all
```

The tests use the standard library's `unittest`, PyQt6, and on Windows the
PyAudioWPatch the application already needs. They reach neither the network,
the microphone, nor your real settings and data directories, so they are safe
to run anywhere and they run on a machine with no display.

CI runs the same command on Python 3.11 through 3.13. A pull request that turns
it red will not be merged.

## Writing one

Put it in `tests/`, named after the module it covers. Inherit from
`tests.support.DikteTest` whenever the code under test touches a file, a
setting or the interface language: it hands the test its own config and data
directories, resets the language, and puts them back afterwards.

`tests/support.py` has the rest of what you need:

| For | Use |
| --- | --- |
| An HTTP call | `fake_urlopen(reply, …)`, then read the recorded requests |
| A reply that fails | `http_error(429)`, `url_error()`, `raw_body("not json")` |
| Reading what was sent | `sent_json(request)`, `multipart_fields(request)` |
| A program on the PATH | `only_these_tools("pactl", "wl-copy")` |
| Audio | `silence()`, `tone()`, `speech()`, `stereo()`, `make_wav()` |
| A settings object | `self.config(cleanup_enabled=False)` |

Three things about this codebase trip up a new test:

**Signals from a worker thread are never delivered.** `Pipeline`, `MeetingPipeline`
and `FileTranscriber` emit from the thread `start()` spawned, which Qt queues
until an event loop runs one. Call `_work()` directly instead: it is the same
code one frame down, and the signals arrive at once.

**A level that never moves is not speech.** The silence check is relative, so a
steady tone reads as its own noise floor however loud it is. Use `speech()`
rather than `tone()` when a recording is meant to have somebody talking in it.

**`cli.launch_gui` replaces the process.** With no instance running, some verbs
`os.execv` into the application, which would take the test run with it. Patch
`cli.launch_gui`. `DikteTest` blocks `os.execv` as a backstop, so a test that
forgets fails rather than hangs.

## Another platform

Most of what Dikte does is not desktop-specific, and both the code and the tests
are split along that line.

Everything a desktop can refuse lives under `platforms/`, one directory per
operating system, four modules each:

```
platforms/
  common/     what neither of them decides: PCM arithmetic, the shortcut list
  linux/      audio.py  clipboard.py  hotkeys.py  runtime.py
  windows/    audio.py  clipboard.py  hotkeys.py  runtime.py
```

`audio.py`, `paste.py`, `hotkey.py` and `config.py` at the top level are the
contract. They pick an adapter at import through `platforms.adapter(...)` and
re-export its functions under the names the rest of Dikte has always called
them by, so `worker.py`, `meeting.py` and `dikte.py` never learn which desktop
they are on. A third system is a third directory, not a branch inside every
function: keep `sys.platform` out of the middle of anything, and put a name in
`runtime.py` when what differs is smaller than a whole module.

The tests follow the same split. Most of them pass anywhere: transcription,
cleanup, the config file, the history, the agent, the command line, the
timeline of a meeting. The rest cover what Dikte *is* on one desktop and carry
`@linux_only` or `@windows_only` from `tests.support`.

A platform's own test imports that platform's adapter directly rather than the
contract module, which is why `tests/test_paste.py` exercises the Linux
clipboard on a Windows machine too: it is the same code there, and a port that
breaks it should be caught wherever the tests are run. Only what genuinely
needs the operating system underneath gets a marker. Do not mark a test because
it happens to be convenient: one that quietly stops running on the platform you
are porting to protects nothing.

## What a pull request should carry

A change to behaviour comes with a test for it. Adding a provider means a row in
`config.TRANSCRIBERS` and a test that the request goes to the right URL with the
right fields; adding a platform means a test for whatever the parsing of its
device list, clipboard or shortcuts looks like. Adding a setting means both halves of `settings_ui.py`: the round
trip in `tests/test_ui.py` is what catches only one of them being written.

Match the surrounding code: it is plain Python with no framework, comments
explain why rather than what, and neither the code nor the commit messages use
an em dash.

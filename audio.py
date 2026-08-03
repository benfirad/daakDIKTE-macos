"""Raw PCM capture with a live level meter, whichever machine this is.

Two recorders, one contract each. `Recorder` captures the microphone for a
dictation and hands back a WAV. `MeetingRecorder` captures the microphone and
what comes out of the speakers at the same time, and writes them to the two
channels of one file, which is what settles who said what without guessing at
it. Both report a level while they run, both can be stopped or cancelled, and
neither says anything about the sound system underneath.

What that is depends on the desktop: PipeWire or PulseAudio through their own
recording programs on Linux, WASAPI through this process on Windows. Both live
under platforms/, and this module is where the rest of Dikte reads them from.
The format is the same either way, 16 kHz mono signed 16-bit, because that is
what whisper wants wherever it runs.
"""

from platforms import adapter
from platforms.common.pcm import (  # noqa: F401
    CHANNELS,
    CHUNK_BYTES,
    CHUNK_FRAMES,
    CHUNK_LATENCY_MS,
    MIN_FRAMES,
    RATE,
    SAMPLE_WIDTH,
    chunk_levels,
    stereo_levels,
    write_wav,
)

_impl = adapter("audio")

Recorder = _impl.Recorder
MeetingRecorder = _impl.MeetingRecorder

#: [(name, description)] for every microphone the machine offers.
list_sources = _impl.list_sources
#: [(name, description)] for every speaker output that can be recorded back.
list_monitors = _impl.list_monitors
#: The output sound is going to right now, or "" when it cannot be worked out.
default_monitor = _impl.default_monitor

# Linux records through another program, so the command line it builds is worth
# looking at on its own. Windows has no such thing and does not offer it.
recording_command = getattr(_impl, "recording_command", None)

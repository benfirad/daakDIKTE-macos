# daakDİKTE roadmap

The roadmap is ordered by user impact and reliability, not by sponsorship.
Completed work moves into release notes instead of remaining here forever.

## Now — dependable beta

- [ ] Finish the unified Linux, macOS and Windows platform-adapter review.
- [ ] Publish a notarized macOS build with a documented trust chain.
- [ ] Add first-run diagnostics for microphone, Accessibility and local Whisper.
- [ ] Expand automated tests for recording cancellation, clipboard restoration
      and update rollback.
- [ ] Turn the current beta channel into a stable release channel.

## Next — global usability

- [ ] Add community-maintained interface translations beyond English and
      Turkish.
- [ ] Package repeatable installers for macOS and major Linux distributions.
- [ ] Add an explicit local-only privacy preset and provider status indicator.
- [ ] Improve keyboard-only navigation and screen-reader labels.
- [ ] Benchmark local models by language, memory and latency.

## Later — sustainable ecosystem

- [ ] Plugin boundary for transcription and cleanup providers.
- [ ] Optional encrypted sync for user-owned dictionaries and cleanup rules.
- [ ] Reproducible release builds and a public release provenance document.
- [ ] Contributor translation and documentation previews in CI.

## Not planned

- Uploading recordings for analytics or advertising.
- Making core local dictation a paid-only feature.
- Shipping a silent background agent with unrestricted system access.

Propose roadmap changes through a feature-request issue with a concrete user
problem, privacy impact and a testable definition of done.

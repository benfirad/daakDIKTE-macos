# Security policy

## Supported versions

daakDİKTE is currently in beta. Security fixes target the newest release and
the default branch; older beta builds may not receive backports.

## Reporting a vulnerability

Do not open a public issue for a vulnerability, leaked credential or transcript
exposure. Use the repository's **Security → Report a vulnerability** flow to
send a private report to the maintainer.

Include the affected version and platform, the smallest safe reproduction, the
impact you observed and whether the issue is already being exploited. Remove
all real recordings, transcripts, API keys and personal data.

You should receive an acknowledgement within seven days. No bounty is promised,
but responsible reporters are credited in the fix unless they prefer to remain
anonymous.

## Security boundaries

- Local Whisper keeps audio and transcription local.
- Selecting OpenAI or OpenRouter sends audio to that provider.
- Selecting Codex CLI cleanup sends transcript text through the user's signed-in
  Codex session.
- Automatic paste requires macOS Accessibility permission or Linux input tools.
  Treat those permissions as sensitive and review every release source.

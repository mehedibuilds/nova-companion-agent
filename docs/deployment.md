# Deployment notes

Run NOVA behind a TLS-terminating reverse proxy. Bind the HTTP port to a private network unless an authenticated gateway is configured. The built-in HTTP API intentionally does not expose provider keys, workspace files, or configuration.

## Provider policy

The provider chain is deterministic and ordered. Use it for availability, not silent cost escalation: retain explicit model names and review provider logs before changing priorities. API keys are resolved per provider from environment variables.

## Telegram policy

Enable Telegram only after populating `telegram.allowlist` with numeric user IDs. The transport rejects all other direct messages before model invocation.
# AURA — Personal AI Agent

AURA is a mobile-first personal AI agent designed to understand natural-language commands and turn them into safe, permissioned actions.

Examples:

- "Hi AURA, open Netflix" → requests the phone to open Netflix.
- "Text David and say I'm coming to your house tomorrow" → resolves the contact, prepares the message, and asks for confirmation before sending.

## Important architecture note

AURA is an **agent system**, not a claim of a human-equivalent artificial general intelligence. The first version uses a language model as its reasoning engine and a permissioned action layer for phone operations. The model can later be replaced or fine-tuned.

## Components

```text
Phone voice/text UI
        |
        v
   AURA API / Agent
        |
   +----+----------------+
   |    |                |
Intent  Memory       Action Planner
   |                     |
   +----------+----------+
              |
      Permission Gateway
              |
      iOS/Android adapters
              |
   Apps / Contacts / Calendar
```

## Safety model

Actions are classified as:

- `read` — can execute when permission exists.
- `open` — can execute when the operating system permits it.
- `prepare` — creates a draft but does not send/submit it.
- `confirm` — requires explicit user confirmation before an external side effect.
- `blocked` — unsupported or unsafe operation.

The agent never gets unrestricted access to the phone. The mobile operating system remains the security boundary.

## Roadmap

1. Voice/text command UI.
2. Intent parsing and structured action plans.
3. App launcher adapter.
4. Contacts + messaging draft adapter.
5. Calendar/reminder adapter.
6. Tool permissions and confirmation UI.
7. On-device/local model option.
8. Long-term memory with user controls.
9. Android accessibility adapter for broader device automation.
10. iOS App Intents/Shortcuts integration for supported actions.

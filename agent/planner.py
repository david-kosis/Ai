import re
from .schemas import Action, ActionKind, AgentResponse


class RulePlanner:
    """Deterministic starter planner used before connecting a language model."""

    def plan(self, text: str, device: str = "ios") -> AgentResponse:
        command = text.strip()
        lower = command.lower()

        # Opening an installed app is an OS-level operation. The mobile client
        # decides whether the requested app can actually be opened.
        app_match = re.search(r"\bopen\s+(?:my\s+)?(.+?)\s*$", command, re.I)
        if app_match and not lower.startswith("open a "):
            app = app_match.group(1).strip().rstrip(".")
            return AgentResponse(
                reply=f"I can try to open {app}.",
                actions=[Action(tool="open_app", kind=ActionKind.OPEN, arguments={"app_name": app})],
            )

        # Messaging is intentionally prepare+confirm rather than silently send.
        msg_match = re.search(
            r"text\s+(.+?)\s+say\s+(.+)$", command, re.I
        )
        if msg_match:
            contact = msg_match.group(1).strip()
            message = msg_match.group(2).strip().strip('"')
            action = Action(
                tool="send_message",
                kind=ActionKind.CONFIRM,
                arguments={"contact": contact, "message": message},
                reason="Sending a message creates an external side effect.",
            )
            return AgentResponse(
                reply=f"I prepared a message to {contact}: \"{message}\". Send it?",
                actions=[action],
                requires_confirmation=True,
            )

        return AgentResponse(
            reply=(
                "I understand the command, but I don't have a matching phone action yet. "
                "The next step is to connect the language-model planner and device adapters."
            )
        )

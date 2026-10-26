from pathlib import Path

class PersonaWorkspace:
    def __init__(self, root: Path) -> None:
        self.root = root
    def system_prompt(self) -> str:
        documents = []
        for filename in ("SOUL.md", "IDENTITY.md", "AGENTS.md"):
            path = self.root / filename
            if path.exists():
                documents.append(path.read_text(encoding="utf-8").strip())
        return "\n\n".join(documents)
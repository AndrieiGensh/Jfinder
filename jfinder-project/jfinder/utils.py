from dataclasses import dataclass, asdict, field

@dataclass
class MessageAction():
    required: bool = False
    attr: dict = field(default_factory=dict)

@dataclass
class MessageContext():
    type: str = "info"
    message: str = "Message here"
    action: MessageAction = field(default_factory=MessageAction)

    def as_context(self):
        return asdict(self)


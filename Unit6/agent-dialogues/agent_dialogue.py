"""A small KQML/KIF dialogue between a procurement and warehouse agent.

This educational example models the KQML message envelope and uses KIF
logical expressions for message content. It intentionally uses only Python's
standard library so it can be run without installing packages.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Final


ONTOLOGY: Final = "warehouse-stock"
LANGUAGE: Final = "KIF"


@dataclass(frozen=True)
class KQMLMessage:
    """A minimal, validated representation of a KQML message."""

    performative: str
    sender: str
    receiver: str
    content: str | None = None
    language: str | None = LANGUAGE
    ontology: str | None = ONTOLOGY
    reply_with: str | None = None
    in_reply_to: str | None = None

    def __post_init__(self) -> None:
        if not self.performative or not self.sender or not self.receiver:
            raise ValueError("performative, sender and receiver are required")
        if self.reply_with and self.in_reply_to:
            raise ValueError("a message cannot start and answer a conversation")
        if self.performative in {"ask-one", "tell"} and not self.content:
            raise ValueError(f"{self.performative} messages require KIF content")

    def to_kqml(self) -> str:
        """Serialise the message using conventional KQML syntax."""

        fields = [
            ("sender", self.sender),
            ("receiver", self.receiver),
            ("language", self.language),
            ("ontology", self.ontology),
            ("reply-with", self.reply_with),
            ("in-reply-to", self.in_reply_to),
            ("content", f'"{self.content}"' if self.content else None),
        ]
        body = "\n".join(
            f"  :{name} {value}" for name, value in fields if value is not None
        )
        return f"({self.performative}\n{body}\n)"


@dataclass(frozen=True)
class TelevisionStock:
    screen_size_inches: int
    available_quantity: int
    hdmi_slots: int


class BobWarehouseAgent:
    """Bob controls and reports the warehouse's television stock levels."""

    name = "Bob"
    _QUERY = re.compile(
        r"^\((available-stock|hdmi-slots) "
        r"\(television \(screen-size (\d+) inch\)\) \?\w+\)$"
    )

    def __init__(self) -> None:
        self._televisions = {
            50: TelevisionStock(
                screen_size_inches=50,
                available_quantity=18,
                hdmi_slots=4,
            )
        }

    def receive(self, message: KQMLMessage) -> KQMLMessage:
        """Answer one supported KIF stock query with a correlated KQML reply."""

        if message.receiver != self.name:
            raise ValueError(f"message was addressed to {message.receiver}, not Bob")
        if message.performative != "ask-one":
            raise ValueError("Bob expects the KQML ask-one performative")
        if message.language != LANGUAGE or message.ontology != ONTOLOGY:
            raise ValueError("Bob requires the KIF warehouse-stock vocabulary")
        if not message.reply_with:
            raise ValueError("queries must provide a reply-with conversation ID")

        match = self._QUERY.fullmatch(message.content or "")
        if not match:
            raise ValueError(f"unsupported KIF query: {message.content}")

        predicate, screen_size_text = match.groups()
        screen_size = int(screen_size_text)
        stock = self._televisions.get(screen_size)
        if stock is None:
            answer = f"(unknown (television (screen-size {screen_size} inch)))"
        elif predicate == "available-stock":
            answer = (
                f"(= (available-stock (television "
                f"(screen-size {screen_size} inch))) {stock.available_quantity})"
            )
        else:
            answer = (
                f"(= (hdmi-slots (television "
                f"(screen-size {screen_size} inch))) {stock.hdmi_slots})"
            )

        return KQMLMessage(
            performative="tell",
            sender=self.name,
            receiver=message.sender,
            content=answer,
            in_reply_to=message.reply_with,
        )


class AliceProcurementAgent:
    """Alice requests the information required to procure televisions."""

    name = "Alice"

    def stock_query(self, screen_size: int) -> KQMLMessage:
        return KQMLMessage(
            performative="ask-one",
            sender=self.name,
            receiver="Bob",
            reply_with=f"stock-{screen_size}",
            content=(
                f"(available-stock (television "
                f"(screen-size {screen_size} inch)) ?quantity)"
            ),
        )

    def hdmi_query(self, screen_size: int) -> KQMLMessage:
        return KQMLMessage(
            performative="ask-one",
            sender=self.name,
            receiver="Bob",
            reply_with=f"hdmi-{screen_size}",
            content=(
                f"(hdmi-slots (television "
                f"(screen-size {screen_size} inch)) ?slots)"
            ),
        )


def run_dialogue() -> list[KQMLMessage]:
    """Run Alice's two-question dialogue with Bob and return all messages."""

    alice = AliceProcurementAgent()
    bob = BobWarehouseAgent()
    dialogue: list[KQMLMessage] = []

    for query in (alice.stock_query(50), alice.hdmi_query(50)):
        dialogue.append(query)
        dialogue.append(bob.receive(query))

    return dialogue


def main() -> None:
    print("KQML/KIF dialogue: Alice (procurement) and Bob (warehouse)\n")
    for message in run_dialogue():
        print(f"{message.sender} -> {message.receiver}")
        print(message.to_kqml())
        print()


if __name__ == "__main__":
    main()

"""A small KQML/KIF dialogue between a procurement and warehouse agent.

This educational example models the KQML message envelope and uses KIF
logical expressions for message content. It intentionally uses only Python's
standard library so it can be run without installing packages.
"""

from __future__ import annotations

import argparse
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
    conversation_id: str | None = None
    reply_with: str | None = None
    in_reply_to: str | None = None

    def __post_init__(self) -> None:
        if not self.performative or not self.sender or not self.receiver:
            raise ValueError("performative, sender and receiver are required")
        if self.reply_with and self.in_reply_to:
            raise ValueError("a message cannot start and answer a conversation")
        if self.performative in {"ask-one", "tell", "sorry"} and not self.content:
            raise ValueError(f"{self.performative} messages require KIF content")
        if (
            self.performative in {"ask-one", "tell", "sorry"}
            and not self.conversation_id
        ):
            raise ValueError(f"{self.performative} messages require a conversation ID")

    def to_kqml(self) -> str:
        """Serialise the message using conventional KQML syntax."""

        fields = [
            ("sender", self.sender),
            ("receiver", self.receiver),
            ("language", self.language),
            ("ontology", self.ontology),
            ("conversation-id", self.conversation_id),
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
        r"^\(and \(television \?tv\) "
        r"\(= \(screen-size \?tv\) \(scalar (\d+) inch\)\) "
        r"\((available-stock|hdmi-slots) \?tv \?\w+\)\)$"
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

        screen_size_text, predicate = match.groups()
        screen_size = int(screen_size_text)
        stock = self._televisions.get(screen_size)
        if stock is None:
            return KQMLMessage(
                performative="sorry",
                sender=self.name,
                receiver=message.sender,
                conversation_id=message.conversation_id,
                content=(
                    f"(unknown (television-size "
                    f"(scalar {screen_size} inch)))"
                ),
                in_reply_to=message.reply_with,
            )

        television_id = f"tv-{screen_size}"
        shared_facts = (
            f"(television {television_id}) "
            f"(= (screen-size {television_id}) (scalar {screen_size} inch))"
        )
        if predicate == "available-stock":
            requested_fact = (
                f"(= (available-stock {television_id}) "
                f"{stock.available_quantity})"
            )
        else:
            requested_fact = f"(= (hdmi-slots {television_id}) {stock.hdmi_slots})"

        answer = f"(and {shared_facts} {requested_fact})"

        return KQMLMessage(
            performative="tell",
            sender=self.name,
            receiver=message.sender,
            conversation_id=message.conversation_id,
            content=answer,
            in_reply_to=message.reply_with,
        )


class AliceProcurementAgent:
    """Alice requests the information required to procure televisions."""

    name = "Alice"

    @staticmethod
    def _conversation_id(screen_size: int) -> str:
        return f"procure-tv-{screen_size}"

    def stock_query(self, screen_size: int) -> KQMLMessage:
        return KQMLMessage(
            performative="ask-one",
            sender=self.name,
            receiver="Bob",
            conversation_id=self._conversation_id(screen_size),
            reply_with=f"stock-{screen_size}",
            content=(
                f"(and (television ?tv) "
                f"(= (screen-size ?tv) (scalar {screen_size} inch)) "
                f"(available-stock ?tv ?quantity))"
            ),
        )

    def hdmi_query(self, screen_size: int) -> KQMLMessage:
        return KQMLMessage(
            performative="ask-one",
            sender=self.name,
            receiver="Bob",
            conversation_id=self._conversation_id(screen_size),
            reply_with=f"hdmi-{screen_size}",
            content=(
                f"(and (television ?tv) "
                f"(= (screen-size ?tv) (scalar {screen_size} inch)) "
                f"(hdmi-slots ?tv ?slots))"
            ),
        )


def run_dialogue(screen_size: int = 50) -> list[KQMLMessage]:
    """Run Alice's two-question dialogue with Bob and return all messages."""

    if screen_size <= 0:
        raise ValueError("screen size must be a positive number of inches")

    alice = AliceProcurementAgent()
    bob = BobWarehouseAgent()
    dialogue: list[KQMLMessage] = []

    for query in (alice.stock_query(screen_size), alice.hdmi_query(screen_size)):
        dialogue.append(query)
        dialogue.append(bob.receive(query))

    return dialogue


def describe_message(message: KQMLMessage, screen_size: int) -> str:
    """Return a plain-English interpretation of one dialogue message."""

    content = message.content or ""
    if message.sender == "Alice" and "available-stock" in content:
        return (
            f"Alice asks how many {screen_size}-inch televisions are available."
        )
    if message.sender == "Alice" and "hdmi-slots" in content:
        return f"Alice asks how many HDMI slots the televisions have."
    if message.performative == "sorry":
        return f"Bob has no warehouse record for {screen_size}-inch televisions."
    if "available-stock" in content:
        quantity = re.search(r"\(available-stock [^)]+\) (\d+)\)", content)
        return f"Bob reports {quantity.group(1)} televisions in stock."
    slots = re.search(r"\(hdmi-slots [^)]+\) (\d+)\)", content)
    return f"Bob reports {slots.group(1)} HDMI slots per television."


def procurement_summary(messages: list[KQMLMessage], screen_size: int) -> str:
    """Summarise the facts Alice learned from Bob's KIF responses."""

    if any(message.performative == "sorry" for message in messages):
        return (
            "Dialogue summary\n"
            "----------------\n"
            f"Product: {screen_size}-inch television\n"
            "Result: No matching warehouse stock record was found."
        )

    joined_content = " ".join(message.content or "" for message in messages)
    quantity = re.search(r"\(available-stock [^)]+\) (\d+)\)", joined_content)
    slots = re.search(r"\(hdmi-slots [^)]+\) (\d+)\)", joined_content)
    if not quantity or not slots:
        raise ValueError("dialogue did not produce a complete procurement result")

    return (
        "Dialogue summary\n"
        "----------------\n"
        f"Product: {screen_size}-inch television\n"
        f"Available quantity: {quantity.group(1)}\n"
        f"HDMI slots per television: {slots.group(1)}\n"
        "Outcome: Alice has the information required for procurement."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Alice and Bob's KQML/KIF warehouse dialogue."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=50,
        help="television screen size in inches (default: 50)",
    )
    args = parser.parse_args()

    messages = run_dialogue(args.size)
    conversation_id = messages[0].conversation_id
    print("KQML/KIF dialogue: Alice (procurement) and Bob (warehouse)")
    print(f"Conversation ID: {conversation_id}\n")
    for stage, message in enumerate(messages, start=1):
        print(f"Stage {stage}/{len(messages)}: {describe_message(message, args.size)}")
        print(f"{message.sender} -> {message.receiver}")
        print(message.to_kqml())
        print()
    print(procurement_summary(messages, args.size))


if __name__ == "__main__":
    main()

"""Tests for the Alice and Bob KQML/KIF dialogue."""

import unittest

from agent_dialogue import (
    AliceProcurementAgent,
    BobWarehouseAgent,
    KQMLMessage,
    run_dialogue,
)


class AgentDialogueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.alice = AliceProcurementAgent()
        self.bob = BobWarehouseAgent()

    def test_stock_query_returns_available_quantity(self) -> None:
        query = self.alice.stock_query(50)
        reply = self.bob.receive(query)

        self.assertEqual(query.performative, "ask-one")
        self.assertEqual(reply.performative, "tell")
        self.assertEqual(reply.in_reply_to, "stock-50")
        self.assertIn("available-stock", reply.content or "")
        self.assertTrue((reply.content or "").endswith(" 18)"))

    def test_hdmi_query_returns_number_of_slots(self) -> None:
        reply = self.bob.receive(self.alice.hdmi_query(50))

        self.assertEqual(reply.in_reply_to, "hdmi-50")
        self.assertIn("hdmi-slots", reply.content or "")
        self.assertTrue((reply.content or "").endswith(" 4)"))

    def test_complete_dialogue_has_two_correlated_exchanges(self) -> None:
        messages = run_dialogue()

        self.assertEqual(len(messages), 4)
        self.assertEqual(
            [message.performative for message in messages],
            ["ask-one", "tell", "ask-one", "tell"],
        )
        self.assertEqual(messages[1].in_reply_to, messages[0].reply_with)
        self.assertEqual(messages[3].in_reply_to, messages[2].reply_with)

    def test_wrong_receiver_is_rejected(self) -> None:
        message = KQMLMessage(
            performative="ask-one",
            sender="Alice",
            receiver="Charlie",
            reply_with="stock-50",
            content="(available-stock (television (screen-size 50 inch)) ?quantity)",
        )

        with self.assertRaisesRegex(ValueError, "not Bob"):
            self.bob.receive(message)


if __name__ == "__main__":
    unittest.main()

"""Tests for the Alice and Bob KQML/KIF dialogue."""

import unittest

from agent_dialogue import (
    AliceProcurementAgent,
    BobWarehouseAgent,
    KQMLMessage,
    procurement_summary,
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
        self.assertEqual(reply.conversation_id, "procure-tv-50")
        self.assertIn("available-stock", reply.content or "")
        self.assertIn("(= (available-stock tv-50) 18)", reply.content or "")

    def test_hdmi_query_returns_number_of_slots(self) -> None:
        reply = self.bob.receive(self.alice.hdmi_query(50))

        self.assertEqual(reply.in_reply_to, "hdmi-50")
        self.assertIn("hdmi-slots", reply.content or "")
        self.assertIn("(= (hdmi-slots tv-50) 4)", reply.content or "")

    def test_complete_dialogue_has_two_correlated_exchanges(self) -> None:
        messages = run_dialogue()

        self.assertEqual(len(messages), 4)
        self.assertEqual(
            [message.performative for message in messages],
            ["ask-one", "tell", "ask-one", "tell"],
        )
        self.assertEqual(messages[1].in_reply_to, messages[0].reply_with)
        self.assertEqual(messages[3].in_reply_to, messages[2].reply_with)
        self.assertEqual(
            {message.conversation_id for message in messages}, {"procure-tv-50"}
        )

    def test_queries_use_formal_kif_variables_and_conjunction(self) -> None:
        query = self.alice.stock_query(50)

        self.assertTrue((query.content or "").startswith("(and "))
        self.assertIn("(television ?tv)", query.content or "")
        self.assertIn("(scalar 50 inch)", query.content or "")
        self.assertIn("?quantity", query.content or "")

    def test_summary_reports_procurement_facts(self) -> None:
        summary = procurement_summary(run_dialogue(50), 50)

        self.assertIn("Available quantity: 18", summary)
        self.assertIn("HDMI slots per television: 4", summary)
        self.assertIn("information required for procurement", summary)

    def test_unknown_size_returns_sorry_messages(self) -> None:
        messages = run_dialogue(55)

        self.assertEqual(messages[1].performative, "sorry")
        self.assertEqual(messages[3].performative, "sorry")
        self.assertIn(
            "No matching warehouse stock record",
            procurement_summary(messages, 55),
        )

    def test_wrong_receiver_is_rejected(self) -> None:
        message = KQMLMessage(
            performative="ask-one",
            sender="Alice",
            receiver="Charlie",
            conversation_id="procure-tv-50",
            reply_with="stock-50",
            content=(
                "(and (television ?tv) "
                "(= (screen-size ?tv) (scalar 50 inch)) "
                "(available-stock ?tv ?quantity))"
            ),
        )

        with self.assertRaisesRegex(ValueError, "not Bob"):
            self.bob.receive(message)


if __name__ == "__main__":
    unittest.main()

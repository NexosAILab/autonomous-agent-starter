"""
test_inbox_agent.py — Test suite for VID_001 Autonomous Inbox Agent
"""

import unittest
from scripts.inbox_agent import AutonomousInboxAgent, EmailMessage

class TestAutonomousInboxAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AutonomousInboxAgent(owner_email="operator@nexosailab.com")

    def test_self_loop_prevention(self):
        msg = EmailMessage(
            message_id="1", thread_id="t1",
            sender="operator@nexosailab.com",
            subject="Test Self",
            body="Loop test"
        )
        self.assertFalse(self.agent.filter_self_loop(msg))
        self.assertIsNone(self.agent.process_message(msg))

    def test_intent_classification(self):
        urgent_msg = EmailMessage("2", "t2", "client@corp.com", "System Down", "The API is broken")
        cls = self.agent.classify_intent(urgent_msg)
        self.assertEqual(cls["category"], "urgent")

        invoice_msg = EmailMessage("3", "t3", "vendor@corp.com", "Invoice Attached", "Please find receipt")
        cls2 = self.agent.classify_intent(invoice_msg)
        self.assertEqual(cls2["category"], "invoice")

    def test_structured_parser_enforces_subject(self):
        parsed = self.agent.parse_structured_output("Plain text with no json", "Project Update")
        self.assertEqual(parsed["subject"], "Re: Project Update")
        self.assertEqual(parsed["body"], "Plain text with no json")

if __name__ == "__main__":
    unittest.main()

from odoo.tests import common, tagged


@tagged("post_install", "helpdesk_ticket_document_pages")
class TestHelpdeskTicket(common.TransactionCase):
    def setUp(self):
        super().setUp()

        # Create a test ticket
        self.ticket = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "description": "Test ticket description",
            }
        )

        # Create a test tag
        self.ticket_roaming_tag = self.env["helpdesk.ticket.tag"].create(
            {"name": "Roaming issue"}
        )

        # Create test document pages
        self.document_page1 = self.env["document.page"].create(
            {"name": "Demo Page 1"}
        )
        self.document_page3 = self.env["document.page"].create(
            {"name": "Demo Page 3"}
        )

        # Assign the tag to the ticket
        self.ticket.tag_ids = [(4, self.ticket_roaming_tag.id)]

        # Assign the tag to document pages
        self.document_page1.ticket_tag_ids = [(4, self.ticket_roaming_tag.id)]
        self.document_page3.ticket_tag_ids = [(4, self.ticket_roaming_tag.id)]

        # Fetch custom views
        self.custom_tree_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_tree_new_target"
        )
        self.custom_form_view = self.env.ref(
            "helpdesk_ticket_document_pages.document_page_look_up_form_view"
        )

    def test_open_related_document_pages(self):
        """Test that the 'open_related_document_pages' method returns the expected action."""
        # Ensure the ticket and document pages are correctly set up
        self.assertIn(self.ticket_roaming_tag, self.ticket.tag_ids)
        self.assertIn(self.ticket_roaming_tag, self.document_page1.ticket_tag_ids)
        self.assertIn(self.ticket_roaming_tag, self.document_page3.ticket_tag_ids)

        # Call the method
        action_result = self.ticket.open_related_document_pages()

        # Assertions
        self.assertIsInstance(action_result, dict)
        self.assertEqual(action_result.get("name"), "Document Pages")
        self.assertEqual(action_result.get("type"), "ir.actions.act_window")
        self.assertEqual(action_result.get("res_model"), "document.page")
        self.assertEqual(
            action_result.get("views"),
            [[self.custom_tree_view.id, "tree"], [self.custom_form_view.id, "form"]],
        )
        self.assertEqual(
            action_result.get("domain"),
            [("id", "in", [self.document_page1.id, self.document_page3.id])],
        )

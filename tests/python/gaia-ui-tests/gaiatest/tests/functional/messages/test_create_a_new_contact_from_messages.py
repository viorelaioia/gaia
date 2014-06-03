# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest import GaiaTestCase
from gaiatest.apps.messages.app import Messages
from gaiatest.apps.contacts.regions.contact_form import EditContact
from gaiatest.apps.contacts.app import Contacts


class TestSmsCreateContact(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        _text_message_content = "Automated Test %s" % str(time.time())

        self.data_layer.send_sms(self.testvars['carrier']['phone_number'], _text_message_content)
        self.messages = Messages(self.marionette)
        self.messages.launch()

    def test_sms_create_new_contact(self):
        self.message_thread = self.messages.tap_first_received_message()
        self.message_thread.wait_for_received_messages()

        # Check that we received the correct message
#        self.assertEqual(self.message_thread.header_text, self.testvars['carrier']['phone_number'])

        activities = self.message_thread.tap_header()

        contacts = activities.tap_create_new_contact


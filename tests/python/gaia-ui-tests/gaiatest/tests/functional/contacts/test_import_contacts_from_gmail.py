# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.contacts.app import Contacts


class TestImportContactsFromGmail(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_import_contacts_from_gmail(self):

        email = self.testvars['email']['gmail']['email']
        password = self.testvars['email']['gmail']['password']
        contacts_app = Contacts(self.marionette)
        contacts_app.launch()

        # import contacts from Gmail
        contacts_settings = contacts_app.tap_settings()
        contacts_settings.tap_import_contacts()
        self.assertEqual(contacts_settings.import_message, u'Not imported')
        gmail = contacts_settings.tap_import_from_gmail()
        gmail.gmail_login(email, password)
        gmail.switch_to_gmail_contacts_frame()
        gmail.tap_select_all_button()
        gmail.tap_import()

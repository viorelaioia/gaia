# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.contacts.app import Contacts


class TestImportContactsFromOutlook(GaiaTestCase):

    def setUp(self):

        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_import_contacts_from_outlook(self):

        email = self.testvars['email']['outlook']['email']
        password = self.testvars['email']['outlook']['password']
        contacts_app = Contacts(self.marionette)
        contacts_app.launch()

        # Go on Contacts Settings page
        contacts_settings = contacts_app.tap_settings()

        # Tap Import Contacts
        contacts_settings.tap_import_contacts()

        # Check there're no outlook contacts imported
        self.assertEqual(contacts_settings.imported_contacts, u'Not imported')
        outlook = contacts_settings.tap_import_from_outlook()

        # Login to outlook account
        outlook.switch_to_outlook_login()
        contacts_import = outlook.outlook_login(email, password)

         # Import first contact
        contacts_import.switch_to_select_contacts_frame()
        contacts_import.tap_first_contact()
        contacts_settings = contacts_import.tap_import_button()
        contacts_settings.tap_back_from_import_contacts()
        contacts_settings.tap_done()

        # Check there's one outlook contact imported
        self.assertEqual(len(contacts_app.contacts), 1)

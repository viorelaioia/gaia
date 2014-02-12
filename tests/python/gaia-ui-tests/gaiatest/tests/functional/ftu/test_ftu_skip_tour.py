# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.ftu.app import Ftu


class TestFtu(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.app = self.apps.launch('FTU')

        self.wait_for_condition(lambda m: self.data_layer.is_wifi_enabled)

    def test_ftu_skip_tour(self):
        """https://moztrap.mozilla.org/manage/case/3876/

        https://moztrap.mozilla.org/manage/case/3879/
        """
        ssid = self.testvars['wifi']['ssid']
        psk = self.testvars['wifi'].get('psk')
        keymanagement = self.testvars['wifi'].get('keyManagement')

        ftu = Ftu(self.marionette)
        ftu.launch()
        ftu.wait_for_languages_display()
        self.assertGreater(len(ftu.languages_list), 0, "No languages listed on screen")

        # select en-US due to the condition of this test is only for en-US
        ftu.tap_language("en-US")
        ftu.open_cell_data_section()

        # Tap enable data
        ftu.enable_data()
        self.wait_for_condition(lambda m: self.data_layer.is_cell_data_connected, message="Cell data was not connected by FTU app")
        ftu.open_wifi_section()

        # Wait for some networks to be found
        ftu.wait_for_networks_available()
        ftu.connect_to_wifi(ssid, psk, keymanagement)
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via FTU app")
        self.apps.switch_to_displayed_app()

        # Set timezone
        ftu.open_timezone_section()
        ftu.set_timezone_continent()
        ftu.set_timezone_city()
        #self.assertEqual(ftu.timezone_title, "UTC+06:00 Asia/Almaty")

        # Verify Geolocation section appears
        ftu.open_geolocation_section()

        # Disable geolocation
        ftu.disable_geolocation()
        self.wait_for_condition(lambda m: not self.data_layer.get_setting('geolocation.enabled'), message="Geolocation was not disabled by the FTU app")
        ftu.open_import_contacts_section()

        # Tap import from SIM
        # You can do this as many times as you like without db conflict
        ftu.tap_import_from_SIM()
        ftu.wait_for_contacts_imported()
        self.assertEqual(ftu.count_imported_contacts, len(self.data_layer.all_contacts))

        # all_contacts switches to top frame; Marionette needs to be switched back to ftu
        self.apps.switch_to_displayed_app()
        ftu.open_welcome_browser_section()

        # Tap the statistics box and check that it sets a setting
        # TODO assert via settings API that this is set. Currently it is not used
        ftu.tap_statistics_box()
        ftu.open_privacy_browser_locator()

        # Enter a dummy email address and check it set inside the os
        # TODO assert that this is preserved in the system somewhere. Currently it is not used
        #ftu.tap_email_address()
        ftu.open_finish_section()

        # Skip the tour
        ftu.tap_skip_tour()

        # Switch back to top level now that FTU app is gone
        self.marionette.switch_to_frame()

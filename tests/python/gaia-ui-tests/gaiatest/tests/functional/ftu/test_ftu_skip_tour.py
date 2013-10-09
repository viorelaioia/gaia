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
        ftu = Ftu(self.marionette)
        ftu.wait_for_languages_display()
        self.assertGreater(len(ftu.languages_list), 0, "No languages listed on screen")
        ftu.create_language_locator("en-US")
        ftu.tap_language("en-US")
        ftu.open_cell_data_section()
        ftu.enable_data()
        self.wait_for_condition(lambda m: self.data_layer.is_cell_data_connected, message="Cell data was not connected by FTU app")
        ftu.open_wifi_section()
        ftu.wait_for_networks_available()
        ftu.select_a_network(self.testvars['wifi'])
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected via FTU app")
        self.marionette.switch_to_frame(self.app.frame)
        ftu.open_timezone_section()
        ftu.set_timezone_continent()
        ftu.set_timezone_city()
        self.assertEqual(ftu.timezone_title, "UTC+06:00 Asia/Almaty")
        ftu.open_geolocation_section()
        ftu.disable_geolocation()
        self.wait_for_condition(lambda m: not self.data_layer.get_setting('geolocation.enabled'), message="Geolocation was not disabled by the FTU app")
        ftu.open_import_contacts_section()
        ftu.tap_import_from_SIM()
        ftu.wait_for_contacts_imported()
        ftu.open_welcome_browser_section()
        ftu.tap_statistics_box()
        ftu.open_privacy_browser_locator()
        ftu.tap_email_address()
        ftu.open_finish_section()
        ftu.tap_skip_tour()
        self.marionette.switch_to_frame()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.ftu.app import Ftu


class TestFtu(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.wait_for_condition(lambda m: self.data_layer.is_wifi_enabled)

    def test_ftu_skip_tour(self):
        ftu = Ftu(self.marionette)
        ftu.launch()
        ftu.wait_for_languages_display()
        ftu.open_cell_data_section()
        ftu.open_wifi_section()
        ftu.open_timezone_section()
        ftu.open_geolocation_section()
        ftu.open_import_contacts_section()
        ftu.open_welcome_browser_section()
        ftu.open_privacy_browser_locator()
        ftu.open_finish_section()
        ftu.tap_take_tour()
        ftu.wait_for_step1()
        self.assertEqual(ftu.step1, "Swipe from right to left to browse your apps.")
        ftu.tap_next()
        ftu.wait_for_step2()
        self.assertEqual(ftu.step2, "Tap and hold on an icon to delete or move it.")
        ftu.tap_next()
        ftu.wait_for_step3()
        self.assertEqual(ftu.step3, "Swipe down to access recent notifications, credit information and settings.")
        ftu.tap_next()
        ftu.wait_for_step4()
        self.assertEqual(ftu.step4, "Tap and hold the home button to browse and close recent apps.")
        ftu.tap_back()
        ftu.wait_for_step3()
        ftu.tap_next()
        ftu.wait_for_step4()
        ftu.tap_next()
        ftu.wait_for_finish_tutorial_section()
        ftu.tap_lets_go_button()
        self.marionette.switch_to_frame()

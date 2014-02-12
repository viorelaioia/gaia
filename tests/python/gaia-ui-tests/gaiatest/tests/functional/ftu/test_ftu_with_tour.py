# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.ftu.app import Ftu


class TestFtu(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.wait_for_condition(lambda m: self.data_layer.is_wifi_enabled)

    def test_ftu_with_tour(self):
        ftu = Ftu(self.marionette)
        ftu.launch()
        ftu.wait_for_languages_display()

        # Go through the FTU setup as quickly as possible to get to the Tour section
        ftu.run_ftu_setup()

        # Take the tour
        ftu.tap_take_tour()

        # Walk through the tour
        self.assertEqual(ftu.step1, "Swipe from right to left to browse your apps.")
        ftu.tap_tour_next()
        self.assertEqual(ftu.step2, "Tap and hold on an icon to delete or move it.")
        ftu.tap_tour_next()
        self.assertEqual(ftu.step3, "Enter any keyword or topic and your phone will instantly adapt.")
        ftu.tap_tour_next()
        self.assertEqual(ftu.step4, "Swipe down to access recent notifications, credit information and settings.")
        ftu.tap_tour_next()
        self.assertEqual(ftu.step5, "Tap and hold the home button to browse and close recent apps.")

        # Try going back a step
        ftu.tap_back()
        self.assertEqual(ftu.step4, "Swipe down to access recent notifications, credit information and settings.")
        ftu.tap_tour_next()
        self.assertEqual(ftu.step5, "Tap and hold the home button to browse and close recent apps.")
        ftu.tap_tour_next()
        ftu.wait_for_finish_tutorial_section()
        ftu.tap_lets_go_button()

        # Switch back to top level now that FTU app is gone
        self.marionette.switch_to_frame()

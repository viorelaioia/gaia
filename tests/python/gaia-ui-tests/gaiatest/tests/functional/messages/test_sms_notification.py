# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.lockscreen.app import LockScreen


class TestSmsNotification(GaiaTestCase):

    def test_sms_notification(self):

        _text_message_content = "Automated Test %s" % str(time.time())

        self.lockscreen.lock()
        self.lock_screen = LockScreen(self.marionette)
        self.device.turn_screen_off()

         # Check if the screen is turned off
        self.assertFalse(self.device.is_screen_enabled)

        # Send a SMS to the device
        self.data_layer.send_sms(self.testvars['carrier']['phone_number'], _text_message_content)
        self.lock_screen.wait_for_notification(timeout=180)

        # Check if the screen is turned on
        self.assertTrue(self.device.is_screen_enabled)

        # Check if the notification is displayed on the screen
        self.assertTrue(self.lock_screen.notifications[0].is_visible)
        self.assertEqual(self.lock_screen.notifications[0].content, _text_message_content)

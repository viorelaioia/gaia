# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from marionette import Marionette
from gaiatest.apps.iac_publisher.app import IacPublisher


class TestInterAppComm(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

    def test_inter_app_comm(self):
        _testing_message = "this is a test"

        iac_publisher = IacPublisher(self.marionette)
        iac_publisher.launch()
        iac_publisher.send_message(_testing_message)

        received_str_msg = self.marionette.find_element(*self._pub_app_received_str_msg_locator);
        self.assertEqual(received_str_msg.get_attribute("value"), self._testing_message)

        self.wait_for_element_present(*self._pub_app_received_blob_msg_locator)

        received_blob_msg = self.marionette.find_element(*self._pub_app_received_blob_msg_locator);
        self.assertEqual(received_blob_msg.get_attribute("value"), self._testing_message)

        num_conns = self.marionette.find_element(*self._pub_app_num_conns_locator);
        self.assertEqual(num_conns.get_attribute("value"), "1")

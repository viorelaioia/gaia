# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class IacPublisher(Base):

    name = "Test IAC Publisher"

    _pub_app_msg_to_send_locator = (By.ID, "msgToSend")
    _pub_app_send_button_locator = (By.ID, "sendButton")
    _pub_app_num_conns_locator = (By.ID, "numConns")
    _pub_app_received_str_msg_locator = (By.ID, "receivedStrMsg")
    _pub_app_received_blob_msg_locator = (By.ID, "receivedBlobMsg")

    def launch(self):
        Base.launch(self, launch_timeout=120000)
        self.wait_for_element_displayed(*self._pub_app_msg_to_send_locator)

    def send_message(self, msg):
        self.marionette.execute_script("""
            var msgToSend = document.getElementById('msgToSend');
            msgToSend.value = "%s";
        """ % msg)
        self.marionette.find_element(*self._pub_app_send_button_locator).tap();
        self.wait_for_element_present(*self._pub_app_received_str_msg_locator)




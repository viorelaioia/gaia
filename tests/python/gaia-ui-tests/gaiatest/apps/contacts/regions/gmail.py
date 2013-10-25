# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class Gmail(Base):

    _gmail_sign_in_locator = (By.CSS_SELECTOR, '#frame-container > iframe')
    _email_locator = (By.ID, 'Email')
    _password_locator = (By.ID, 'Passwd')
    _sign_in_locator = (By.ID, 'signIn')
    _gmail_frame_locator = (By.ID, 'fb-extensions')
    _select_all_button_locator = (By.ID, 'select-all')
    _import_locator = (By.ID, 'import-action')

    def switch_to_gmail_login(self):
        self.marionette.switch_to_frame()
        gmail_sign_in = self.marionette.find_element(*self._gmail_sign_in_locator)
        self.marionette.switch_to_frame(gmail_sign_in)

    def gmail_login(self, user, passwd):
        frame = self.marionette.get_active_frame()
        self.switch_to_gmail_login()
        self.wait_for_element_displayed(*self._email_locator)
        self.marionette.find_element(*self._email_locator).tap()
        self.marionette.find_element(*self._email_locator).send_keys(user)

        self.marionette.find_element(*self._password_locator).tap()
        self.marionette.find_element(*self._password_locator).send_keys(passwd)

        self.marionette.find_element(*self._sign_in_locator).tap()

        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(frame)

    def switch_to_gmail_contacts_frame(self):
        self.wait_for_element_displayed(*self._gmail_frame_locator)
        gmail = self.marionette.find_element(*self._gmail_frame_locator)
        self.marionette.switch_to_frame(gmail)

    def tap_select_all_button(self):
        self.wait_for_element_displayed(*self._select_all_button_locator)
        self.marionette.find_element(*self._select_all_button_locator).tap()

    def tap_import(self):
        self.wait_for_element_displayed(*self._import_locator)
        self.marionette.find_element(*self._import_locator).tap()

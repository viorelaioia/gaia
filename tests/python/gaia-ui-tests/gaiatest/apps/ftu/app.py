# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette import MarionetteTestCase
import re

from gaiatest.apps.base import Base


class Ftu(Base, MarionetteTestCase):

    name = 'FTU'

    _activation_section_locator = (By.ID, 'activation')
    _main_title_locator = (By.ID, 'main_title')

    _next_button_locator = (By.ID, 'forward')

    # Step Languages section
    _section_languages_locator = (By.ID, 'languages')
    _listed_languages_locator = (By.CSS_SELECTOR, "#languages ul li input[name='language.current']")

    # Step Cell data section
    _section_cell_data_locator = (By.ID, 'data_3g')
    _enable_data_checkbox_locator = (By.CSS_SELECTOR, '#data_3g .pack-end label')

    # Step Wifi
    _section_wifi_locator = (By.ID, 'wifi')
    _found_wifi_networks_locator = (By.CSS_SELECTOR, 'ul#networks-list li')
    _network_state_locator = (By.XPATH, 'p[2]')
    _password_input_locator = (By.ID, 'wifi_password')
    _join_network_locator = (By.ID, 'wifi-join-button')

    # Step Date & Time
    _section_date_time_locator = (By.ID, 'date_and_time')
    _timezone_continent_locator = (By.CSS_SELECTOR, '#time-form ul li:nth-child(1) button')
    _timezone_city_locator = (By.CSS_SELECTOR, '#time-form ul li:nth-child(2) button')
    _time_zone_title_locator = (By.ID, 'time-zone-title')

    # Step Geolocation
    _section_geolocation_locator = (By.ID, 'geolocation')
    _enable_geolocation_checkbox_locator = (By.CSS_SELECTOR, '#geolocation .pack-end label')

    # Section Import contacts
    _section_import_contacts_locator = (By.ID, 'import_contacts')
    _import_from_sim_locator = (By.ID, 'sim-import-button')
    _sim_import_feedback_locator = (By.CSS_SELECTOR, '.ftu p')

    # Section About Your rights
    _section_ayr_locator = (By.ID, 'about-your-rights')

    # Section Welcome Browser
    _section_welcome_browser_locator = (By.ID, 'welcome_browser')
    _enable_statistic_checkbox_locator = (By.ID, 'form_share_statistics')

    # Section Privacy Choices
    _section_browser_privacy_locator = (By.ID, 'browser_privacy')
    _email_field_locator = (By.CSS_SELECTOR, 'input[type="email"]')

    # Section Finish
    _section_finish_locator = (By.ID, 'finish-screen')
    _skip_tour_button_locator = (By.ID, 'skip-tutorial-button')
    _take_tour_button_locator = (By.ID, 'lets-go-button')

    # Section Tour
    _take_tour_button_locator = (By.ID, 'lets-go-button')
    _step1_header_locator = (By.ID, 'step1Header')
    _step2_header_locator = (By.ID, 'step2Header')
    _step3_header_locator = (By.ID, 'step3Header')
    _step4_header_locator = (By.ID, 'step4Header')
    _step5_header_locator = (By.ID, 'step5Header')
    _tour_next_button_locator = (By.ID, 'forwardTutorial')
    _tour_back_button_locator = (By.ID, 'backTutorial')

    # Section Tutorial Finish
    _section_tutorial_finish_locator = (By.ID, 'tutorialFinish')
    _lets_go_button_locator = (By.ID, 'tutorialFinished')

    # Pattern for import sim contacts message
    _pattern_contacts = re.compile("^No contacts detected on SIM to import$|^Imported one contact$|^Imported [0-9]+ contacts$")
    _pattern_contacts_0 = re.compile("^No contacts detected on SIM to import$")
    _pattern_contacts_1 = re.compile("^Imported one contact$")
    _pattern_contacts_N = re.compile("^Imported ([0-9]+) contacts$")

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.app = self.apps.launch('FTU')

    def launch(self):
        Base.launch(self)

    def wait_for_languages_display(self):
        self.wait_for_element_displayed(*self._section_languages_locator)

    @property
    def languages_list(self):
        return self.marionette.find_elements(*self._listed_languages_locator)

    def create_language_locator(self, language):
        return (By.CSS_SELECTOR, "#languages ul li input[name='language.current'][value='%s'] ~ p" % language)

    def tap_language(self, language):
        self.marionette.find_element(By.CSS_SELECTOR, "#languages ul li input[name='language.current'][value='%s'] ~ p" % language).tap()

    def open_cell_data_section(self):
        self.wait_for_element_displayed(*self._next_button_locator)
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_cell_data_locator)

    def enable_data(self):
        self.wait_for_element_displayed(*self._enable_data_checkbox_locator)
        self.marionette.find_element(*self._enable_data_checkbox_locator).tap()

    def open_wifi_section(self):
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_wifi_locator)

    def wait_for_networks_available(self):
        self.wait_for_condition(lambda m: len(m.find_elements(*self._found_wifi_networks_locator)) > 0,
                                message="No networks listed on screen")

    def select_a_network(self, network_info):
        this_network_locator = ('xpath', ".//*[@id='%s']/p[1]" % network_info['ssid'])
        network_state_locator = (By.XPATH, ".//*[@id='%s']/p[2]" % network_info['ssid'])
        self.marionette.find_element(*this_network_locator).tap()
        if network_info.get('keyManagement'):
            password = network_info.get('psk') or network_info.get('wep')
            if not password:
                raise Exception('No psk or wep key found in testvars for secured wifi network.')

            self.wait_for_element_displayed(*self._password_input_locator)
            password_input = self.marionette.find_element(*self._password_input_locator)
            password_input.send_keys(password)
            self.marionette.find_element(*self._join_network_locator).tap()
            self.wait_for_condition(lambda m: m.find_element(*network_state_locator).text == "Connected")

    def open_timezone_section(self):
        self.wait_for_element_displayed(*self._next_button_locator)
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_date_time_locator)

    def set_timezone_continent(self):
        self.wait_for_element_displayed(*self._timezone_continent_locator)
        self.marionette.find_element(*self._timezone_continent_locator).tap()
        self._select("Asia")

    def set_timezone_city(self):
        self.wait_for_element_displayed(*self._timezone_city_locator)
        self.marionette.find_element(*self._timezone_city_locator).tap()
        self._select("Almaty")

    @property
    def timezone_title(self):
        return self.marionette.find_element(*self._time_zone_title_locator).text

    def open_geolocation_section(self):
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_geolocation_locator)

    def disable_geolocation(self):
        self.wait_for_element_displayed(*self._enable_geolocation_checkbox_locator)
        self.marionette.find_element(*self._enable_geolocation_checkbox_locator).tap()

    def open_import_contacts_section(self):
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_import_contacts_locator)

    def tap_import_from_SIM(self):
        self.marionette.find_element(*self._import_from_sim_locator).tap()

    def wait_for_contacts_imported(self):
        self.wait_for_condition(lambda m: self._pattern_contacts.match(m.find_element(*self._sim_import_feedback_locator).text) is not None,
                                message="Contact did not import from sim before timeout")

    @property
    def count_imported_contacts(self):
        import_sim_message = self.marionette.find_element(*self._sim_import_feedback_locator).text
        import_sim_count = None
        if self._pattern_contacts_0.match(import_sim_message) is not None:
            import_sim_count = 0
        elif self._pattern_contacts_1.match(import_sim_message) is not None:
            import_sim_count = 1
        elif self._pattern_contacts_N.match(import_sim_message) is not None:
            count = self._pattern_contacts_N.match(import_sim_message).group(1)
            import_sim_count = int(count)
        self.assertEqual(len(self.data_layer.all_contacts), import_sim_count)

    def open_welcome_browser_section(self):
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_welcome_browser_locator)

    def tap_statistics_box(self):
        self.marionette.find_element(*self._enable_statistic_checkbox_locator).tap()

    def open_privacy_browser_locator(self):
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_browser_privacy_locator)

    def tap_email_address(self):
        # TODO assert that this is preserved in the system somewhere. Currently it is not used
        self.marionette.find_element(*self._email_field_locator).send_keys("testuser@mozilla.com")

    def open_finish_section(self):
        self.marionette.find_element(*self._next_button_locator).tap()
        self.wait_for_element_displayed(*self._section_finish_locator)

    def tap_skip_tour(self):
        self.marionette.find_element(*self._skip_tour_button_locator).tap()

    def tap_take_tour(self):
        self.marionette.find_element(*self._take_tour_button_locator).tap()

    def wait_for_step1(self):
        self.wait_for_element_displayed(*self._step1_header_locator)

    @property
    def step1(self):
        return self.marionette.find_element(*self._step1_header_locator).text

    def tap_next(self):
        self.wait_for_element_displayed(*self._tour_next_button_locator)
        self.marionette.find_element(*self._tour_next_button_locator).tap()

    def tap_back(self):
        self.wait_for_element_displayed(*self._tour_next_button_locator)
        self.marionette.find_element(*self._tour_back_button_locator).tap()

    def wait_for_step2(self):
         self.wait_for_element_displayed(*self._step2_header_locator)

    @property
    def step2(self):
        return self.marionette.find_element(*self._step2_header_locator).text

    def wait_for_step3(self):
         self.wait_for_element_displayed(*self._step3_header_locator)

    @property
    def step3(self):
        return self.marionette.find_element(*self._step3_header_locator).text

    def wait_for_step4(self):
         self.wait_for_element_displayed(*self._step4_header_locator)

    @property
    def step4(self):
        return self.marionette.find_element(*self._step4_header_locator).text

    def wait_for_finish_tutorial_section(self):
        self.wait_for_element_displayed(*self._section_tutorial_finish_locator)

    def tap_lets_go_button(self):
        self.marionette.find_element(*self._lets_go_button_locator).tap()

    def _select(self, match_string):
        # Cheeky Select wrapper until Marionette has its own
        # Due to the way B2G wraps the app's select box we match on text

        # Have to go back to top level to get the B2G select box wrapper
        self.marionette.switch_to_frame()

        options = self.marionette.find_elements(By.CSS_SELECTOR, '#value-selector-container li')
        close_button = self.marionette.find_element(By.CSS_SELECTOR, 'button.value-option-confirm')

        # Loop options until we find the match
        for li in options:
            if li.text == match_string:
                li.tap()
                break

        close_button.tap()

        # Now back to app
        self.marionette.switch_to_frame(self.app.frame)

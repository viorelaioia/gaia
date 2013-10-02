# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.videoplayer.app import VideoPlayer


class TestProgressBarIsVisible(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # add video to storage
        self.push_resource('VID_0001.3gp', destination='DCIM/100MZLLA', count=10)

    def test_progress_bar_is_visible(self):
        """https://moztrap.mozilla.org/manage/case/2478/"""

        video_player = VideoPlayer(self.marionette)
        video_player.launch()
        video_player.wait_for_progress_bar_complete()

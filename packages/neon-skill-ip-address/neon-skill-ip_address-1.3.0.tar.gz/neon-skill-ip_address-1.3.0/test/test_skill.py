# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pytest

from mock import Mock
from ovos_bus_client.message import Message

from neon_minerva.tests.skill_unit_test_base import SkillTestCase


class TestSkillMethods(SkillTestCase):
    def test_00_skill_init(self):
        # Test any parameters expected to be set in init or initialize methods
        from neon_utils.skills import NeonSkill
        self.assertIsInstance(self.skill, NeonSkill)

    def test_get_public_ip_address(self):
        self.assertIsInstance(self.skill._get_public_ip_address(), str)

    def test_handle_query_ip_private(self):
        mock_show_text = Mock()
        real_show_text = self.skill.gui.show_text
        self.skill.gui.show_text = mock_show_text
        valid_request = Message("test")
        self.skill.handle_query_ip(valid_request)
        self.skill.speak_dialog.assert_called()
        args = self.skill.speak_dialog.call_args
        self.assertIn(args[0][0], ("my address is", "my address on X is Y"))
        self.assertTrue(args[1]["private"])

        self.skill.gui.show_text.assert_called()
        self.assertIsInstance(self.skill.gui.show_text.call_args[0][0], str)
        self.assertIsInstance(self.skill.gui.show_text.call_args[0][1], str)

        self.skill.gui.show_text = real_show_text

    def test_handle_query_ip_public(self):
        mock_show_text = Mock()
        real_show_text = self.skill.gui.show_text
        self.skill.gui.show_text = mock_show_text
        valid_request = Message("test", {"public": "public"})
        self.skill.handle_query_ip(valid_request)
        self.skill.speak_dialog.assert_called_once()
        args = self.skill.speak_dialog.call_args
        self.assertEqual(args[0][0], "my address is")
        self.assertEqual(set(args[0][1].keys()), {"ip", "pub"})
        self.assertTrue(args[1]["private"])

        self.skill.gui.show_text.assert_called_once()
        self.skill.gui.show_text.assert_called_with(
            self.skill._get_public_ip_address(), "IP Address")
        self.skill.gui.show_text = real_show_text


if __name__ == '__main__':
    pytest.main()

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
#
# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import join, isfile
from ovos_workshop.decorators import fallback_handler
from ovos_workshop.skills.fallback import FallbackSkill
from neon_utils.message_utils import request_for_neon
from ovos_bus_client.message import Message
from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_utils.process_utils import RuntimeRequirements


class UnknownSkill(FallbackSkill):
    # Set of clients that always expect a response
    _transactional_clients = {"mq_api", "klat", "mobile"}

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(network_before_load=False,
                                   internet_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=True,
                                   requires_network=True,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    def _read_voc_lines(self, name) -> filter:
        """
        Return parsed lines for the specified voc resource
        :param name: vocab resource name
        :returns: filter for specified vocab resource
        """
        vocab = self.find_resource(f"{name}.voc", 'vocab',
                                   lang=self.lang)
        if self.lang not in vocab:
            test_path = join(self.root_dir, "vocab", self.lang, f"{name}.voc")
            if isfile(test_path):
                LOG.warning(f"Resolved {vocab} but using {test_path}")
                vocab = test_path
        LOG.debug(f"Reading voc file {vocab} for lang={self.lang}")
        with open(vocab) as f:
            return filter(bool, map(str.strip, f.read().split('\n')))

    @fallback_handler(priority=100)
    def handle_fallback(self, message: Message):
        utterance = message.data['utterance']
        LOG.info(f"Unknown Fallback handling: {utterance}")
        client = message.context.get('client')
        ww_state = self.config_core.get("listener", {}).get("wake_word_enabled",
                                                            True)
        # This checks if we're pretty sure this was a request intended for Neon
        if not any((request_for_neon(message, "neon", self.voc_match, ww_state),
                    client in self._transactional_clients)):
            LOG.info("Ignoring streaming STT or public conversation input")
            return True

        # Show LED animation indicating we reached the unknown fallback
        if self.settings.get('emit_led'):
            self.bus.emit(message.forward('neon.linear_led.show_animation',
                                          {'animation': 'blink',
                                           'color': 'theme'}))

        # Ignore likely accidental activations
        if len(utterance.split()) < 2 and \
                client not in self._transactional_clients:
            LOG.info(f"Ignoring 1-word input: {utterance}")
            return True
        # Show utterance that failed to match an intent
        if self.settings.get('show_utterances'):
            self.gui['utterance'] = utterance
            self.gui.show_page("UnknownIntent")

        # Report an intent failure
        self.bus.emit(Message("neon.metric", {"name": "failed-intent",
                                              'utterance': utterance,
                                              'client': client
                                              }))

        LOG.debug(f"Checking if neon must respond: {message.data}")
        # Determine what kind of question this is to reply appropriately
        for i in ['question', 'who.is', 'why.is']:
            for line in self._read_voc_lines(i):
                if utterance.startswith(line):
                    LOG.info(f'Fallback type: {i} ({utterance})')
                    self.speak_dialog(i,
                                      data={'remaining': line.replace(i, '')})
                    return True

        # Not a question, but it's for Neon, reply "I don't know"
        self.speak_dialog('unknown')
        return True

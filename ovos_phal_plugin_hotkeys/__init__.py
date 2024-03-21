# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import keyboard
from ovos_bus_client.message import Message
from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils import create_daemon


class HotKeysPlugin(PHALPlugin):
    """Keyboard hotkeys, define key combo to trigger listening"""

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-hotkeys", config=config)
        for msg_type, key in self.config.get("mappings", {}).items():
            def do_emit():
                self.bus.emit(Message(msg_type))

            keyboard.add_hotkey(key, do_emit)

        if self.config.get("debug"):
            create_daemon(self.debug_thread)

    def debug_thread(self):
        # or this
        while True:
            # Wait for the next event.
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                print("DEBUG", event.to_json())

    def shutdown(self):
        keyboard.unhook_all_hotkeys()


from ovos_utils import wait_for_exit_signal
from ovos_utils.messagebus import FakeBus

p = HotKeysPlugin(FakeBus(), {"debug": True})
wait_for_exit_signal()
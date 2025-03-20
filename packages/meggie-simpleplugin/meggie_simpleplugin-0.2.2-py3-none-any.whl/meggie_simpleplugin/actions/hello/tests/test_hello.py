from meggie.utilities.testing import BaseTestAction
from meggie_simpleplugin.actions.hello import Hello


class TestHello(BaseTestAction):

    def test_hello(self):
        self.run_action(
            action_name="hello",
            handler=Hello,
        )

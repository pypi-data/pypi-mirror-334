from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

class MyPlugin(Plugin):
    api_version = "0.5"
    commands = {
        "hello": {
            "description": "Greets the command sender!",
            "usages": ["/hello"],
            "permissions": ["my_plugin.command.hello"]
        }
    }

    permissions = {
        "my_plugin.command.hello": {
            "description": "Allows users to use this command",
            "default": True
        }
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name == "hello":
            sender.send_message("Hello World!")

        return True

    def on_load(self) -> None:
        self.logger.info("on_load is called but it should work lively!")

    def on_enable(self) -> None:
        self.logger.info("on_enable is called and live_updates?!")

    def on_disable(self) -> None:
        self.logger.info("on_disable is called! pi")
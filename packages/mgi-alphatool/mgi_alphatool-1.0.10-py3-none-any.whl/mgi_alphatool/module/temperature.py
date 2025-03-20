from . import Module
from ..commands.module import (TemperatureModuleDeactivateParams, TemperatureModuleDeactivateCommand,
                               TemperatureModuleSetTempParams, TemperatureModuleSetTempCommand,
                               TemperatureModuleWaitForTempCommand, TemperatureModuleWaitForTempParams)

from ..commands.wait import WaitForDurationParams, WaitForDurationCommand

from ..app.commands.command import TemperatureCommand

class TemperatureModule(Module):
    def __init__(self, id: str, name: str, slot: int, context: 'Context'):
        """Initialize the temperature module.

        Args:
            id (str): The unique identifier for the module.
            name (str): The name of the module.
            slot (int): The location slot of the module.
            context (Context): The protocol context instance.
        """
        super().__init__(id, name, slot, context)
        self.__context = context

    def set_temp(self, celsius: int, wait_for_temp: bool = True) -> 'TemperatureModule':
        """Set the target temperature.

        Args:
            celsius (int): The target temperature in Celsius.
            wait_for_temp (bool, optional): Wait until the target temperature is achieved. Defaults to True.

        Returns:
            TemperatureModule: The current module instance.
        """
        self.__context._append_command(WaitForDurationCommand(
            params=WaitForDurationParams(seconds=1)
        ))

        self.__context._append_command(TemperatureModuleSetTempCommand(
            params=TemperatureModuleSetTempParams(
                moduleId=self.id(),
                celsius=celsius
            )
        ))

        if wait_for_temp:
            self.__context._append_command(TemperatureModuleWaitForTempCommand(
                params=TemperatureModuleWaitForTempParams(
                    moduleId=self.id(),
                    celsius=celsius
                )
            ))
        return self
    
    def engage(self, celsius: int, wait_for_temp: bool = True) -> 'TemperatureModule':
        """Alias of set_temp function.

        Args:
            celsius (int): The target temperature in Celsius.
            wait_for_temp (bool, optional): Wait until the target temperature is achieved. Defaults to True.

        Returns:
            TemperatureModule: The current module instance.
        """
        return self.set_temp(celsius, wait_for_temp)

    def disengage(self) -> 'TemperatureModule':
        """Disengage the temperature module.

        Returns:
            TemperatureModule: The current module instance.
        """
        self.__context._append_command(WaitForDurationCommand(
            params=WaitForDurationParams(seconds=1)
        ))

        self.__context._append_command(TemperatureModuleDeactivateCommand(
            params=TemperatureModuleDeactivateParams(
                moduleId=self.id(),
            )
        ))
        return self
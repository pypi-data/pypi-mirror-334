from typing import Dict, List, Union
from . import Module

from ..commands.module import (ThermocyclerModuleCloseLidCommand, ThermocyclerModuleCloseLidParams,
                               ThermocyclerModuleOpenLidCommand, ThermocyclerModuleOpenLidParams,
                               ThermocyclerModuleSetBlockTempCommand, ThermocyclerModuleSetBlockTempParams,
                               ThermocyclerModuleSetLidTempCommand, ThermocyclerModuleSetLidTempParams,
                               ThermocyclerModuleWaitForBlockTempCommand, ThermocyclerModuleWaitForBlockTempParams,
                               ThermocyclerModuleWaitForLidTempCommand, ThermocyclerModuleWaitForLidTempParams,
                               ThermocyclerModuleDeactivateBlockCommand, ThermocyclerModuleDeactivateBlockParams,
                               ThermocyclerModuleDeactivateLidCommand, ThermocyclerModuleDeactivateLidParams,
                               ThermocyclerRunProfileCommand, ThermocyclerModuleRunProfileParams, ThermocyclerModuleRunProfileStep)

class ThermocyclerModule(Module):
    def __init__(self, id: str, name: str, slot: int, context: 'Context'):
        """Initialize the thermocycler module.

        Args:
            id (str): The unique identifier for the module.
            name (str): The name of the module.
            slot (int): The location slot of the module.
            context (Context): The protocol context instance.
        """
        super().__init__(id, name, slot, context)
        self.__context = context

    def open_lid(self) -> 'ThermocyclerModule':
        """Open the lid of the thermocycler.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        command = ThermocyclerModuleOpenLidCommand(
            params=ThermocyclerModuleOpenLidParams(
                moduleId=self.id(),
            )
        )
        self.__context._append_command(command)
        return self
     
    def close_lid(self) -> 'ThermocyclerModule':
        """Close the lid of the thermocycler.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        command = ThermocyclerModuleCloseLidCommand(
            params=ThermocyclerModuleCloseLidParams(
                moduleId=self.id(),
            )
        )
        self.__context._append_command(command)
        return self
       
    def set_lid_temp(self, celsius: int, wait_for_temp:bool=True) -> 'ThermocyclerModule':
        """Set the lid temperature.

        Args:
            celsius (int): Temperature of the lid in Celsius.
            wait_for_temp (bool, optional): Whether to wait for the lid temperature to be reached. Defaults to True.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        command = ThermocyclerModuleSetLidTempCommand(
            params=ThermocyclerModuleSetLidTempParams(
                moduleId=self.id(),
                celsius=celsius
            )
        )
        self.__context._append_command(command)

        if wait_for_temp:
                command = ThermocyclerModuleWaitForLidTempCommand(
                    params=ThermocyclerModuleWaitForLidTempParams(
                        moduleId=self.id(),
                    )
                )
                self.__context._append_command(command)
        return self
       
    def set_block_temp(self, celsius: int, wait_for_temp:bool=True) -> 'ThermocyclerModule':
        """Set the block temperature.

        Args:
            celsius (int): Temperature of the block in Celsius.
            wait_for_temp (bool, optional): Whether to wait for the block temperature to be reached. Defaults to True.
            
        Returns:
            ThermocyclerModule: The current module instance.
        """
        command = ThermocyclerModuleSetBlockTempCommand(
            params=ThermocyclerModuleSetBlockTempParams(
                moduleId=self.id(),
                celsius=celsius
            )
        )
        self.__context._append_command(command)

        if wait_for_temp:
            command = ThermocyclerModuleWaitForBlockTempCommand(
                params=ThermocyclerModuleWaitForBlockTempParams(
                    moduleId=self.id(),
                )
            )
            self.__context._append_command(command)
        return self

    def disengage_block(self) -> 'ThermocyclerModule':
        """Disengage the block.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        command = ThermocyclerModuleDeactivateBlockCommand(
            params=ThermocyclerModuleDeactivateBlockParams(
                moduleId=self.id(),
            )
        )
        self.__context._append_command(command)
        return self
    
    def disengage_lid(self) -> 'ThermocyclerModule':
        """Disengage the lid.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        command = ThermocyclerModuleDeactivateLidCommand(
            params=ThermocyclerModuleDeactivateLidParams(
                moduleId=self.id(),
            )
        )
        self.__context._append_command(command)
        return self

    def disengage(self) -> 'ThermocyclerModule':
        """Disengage both lid and block.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        self.disengage_block()
        self.disengage_lid()
        return self
       
    def run(self, steps: Union[List[Dict], Dict], cycle: int=1, volume: int=0) -> 'ThermocyclerModule':
        """Run the thermocycler profile.

        Args:
            steps (Union[List[Dict], Dict]): The profile steps to run.
            cycle (int, optional): Number of cycles. Defaults to 1.
            volume (int, optional): Block maximum volume in microliters. Defaults to 0.

        Returns:
            ThermocyclerModule: The current module instance.
        """
        _steps = []

        if isinstance(steps, dict):
            steps = [steps]

        for _ in range(cycle):
            for s in steps:
                _steps.append(ThermocyclerModuleRunProfileStep(celsius=s['celsius'],
                                                               holdSeconds=s['seconds']))
        command = ThermocyclerRunProfileCommand(
            params=ThermocyclerModuleRunProfileParams(
                moduleId=self.id(),
                profile=_steps,
                blockMaxVolumeUl=volume
            )
        )
        
        self.__context._append_command(command)
        return self
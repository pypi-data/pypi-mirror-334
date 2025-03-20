import json
import os
import time
import uuid
import glob
import re
from typing import Any, List, Union, Literal, Dict, Optional

import Levenshtein

from .handler.pipette import Pipette
from .handler.gripper import Gripper
from .liquid import Liquid
from .module import Module
from .module.temperature import TemperatureModule
from .module.thermocycler import ThermocyclerModule
from .module.magnetic import MagneticModule
from .module.heatershaker import HeaterShakerModule
from .module.transport import TransportModule

from .labware import Column, Labware, Well
from .labware.adapter import Adapter
from .labware.aluminumblock import AluminumBlock
from .labware.reservoir import Reservoir
from .labware.tiprack import TipRack
from .labware.tuberack import TubeRack
from .labware.wellplate import WellPlate
from .labware.trashbin import TrashBin

from .commands.command import Location
from .commands.pipette import LoadPipetteParams, LoadPipetteCommand
from .commands.module import LoadModuleParams, LoadModuleCommand
from .commands.labware import LoadLabwareParams, LoadLabwareCommand, MoveLabwareParams, MoveLabwareCommand
from .commands.wait import WaitForDurationParams, WaitForDurationCommand, WaitForResumeParams, WaitForResumeCommand

_MODULE_CLASSES = {
    "temperatureModuleV2": TemperatureModule,
    "thermocyclerModuleV2": ThermocyclerModule,
    "magneticModuleV2": MagneticModule,
    "heaterShakerModuleV1": HeaterShakerModule,
    "transportModuleSenderV1": TransportModule,
    "transportModuleReceiverV1": TransportModule
}

_LABWARE_CLASSES = {
    'tipRack': TipRack,
    'tubeRack': TubeRack,
    'adapter': Adapter,
    'wellPlate': WellPlate,
    'reservoir': Reservoir,
    'aluminumBlock': AluminumBlock,
    'trash': TrashBin
}

_MODULE_ID_MAP = {
    "temperatureModuleV2": 'temperatureModuleType',
    "thermocyclerModuleV2": 'thermocyclerModuleType',
    "magneticModuleV2": 'magneticModuleType',
    "heaterShakerModuleV1": 'heaterShakerModuleType',
    "transportModuleSenderV1": 'transportModuleType',
    "transportModuleReceiverV1": 'transportModuleType'
}

_DECK_LABWARE_TYPE_MAP = {
    'tipRack': 'tip_rack', 
    'tubeRack': 'tube_rack', 
    'wellPlate': 'well_plate',
    'reservoir': 'reservoir', 
    'aluminumBlock': 'aluminum_block', 
    'adapter': 'adapter',
    'trash': 'trash'
}

_PIPETTE_NAME = ['p200_multi', 'p200_single', 'p1000_single']
_MODULE_TYPES = list(_MODULE_CLASSES.keys())
_MOUNT_TYPES = ['left', 'right']

_ROBOT_TYPES = ['alphatool']  # Add your actual supported robot types

class Context:
    def __init__(self, robot_type: str, 
                 deck_type: str, 
                 home_slot: int,
                 auto_revise: bool):
        """Initialize the Context.
        
        Args:
            robot_type (str): Type of robot to use (e.g. 'alphatool')
            deck_type (str): Type of deck to use (e.g. 'alphatool_standard')
            home_slot (int): The slot to home the robot
            auto_revise (bool): Whether to automatically revise invalid names
            
        Raises:
            TypeError: If auto_revise is not a boolean
            ValueError: If robot_type is not supported
        """

        # TODO: option of trash location

        if not isinstance(auto_revise, bool):
            raise TypeError("auto_revise must be a boolean")
            
        if robot_type not in _ROBOT_TYPES:
            raise ValueError(f"Unsupported robot type: {robot_type}. Must be one of: {', '.join(_ROBOT_TYPES)}")

        self.__robot_type = robot_type
        self.__deck_type = deck_type
        self.__auto_revise = auto_revise
        self.__home_slot = home_slot

        cur_ts = int(time.time() * 1000)
        self.__json = {
            "metadata":{
                "protocolName": "py_protocol",
                "author": "alab Studio",
                "description": "",
                "created": cur_ts,
                "lastModified": cur_ts,
                "category": None,
                "subcategory": None,
                "tags": []
            },
            "robot": {
                "model": self.__robot_type,
                "deckId": self.__deck_type
            },
            "liquids": {},
            "commandAnnotations": [],
            "designerApplication": {
                "name": "mgi/protocol-designer",
                "version": "1.0.0",
                "data": {
                    "pipetteTiprackAssignments": {},
                    "ingredients": {},
                    "ingredLocations": {},
                    "dismissedWarnings": {
                        "form": {},
                        "timeline": {}
                    },
                    "defaultValues": {
                        "blowout_mmFromTop": 0,
                        "touchTip_mmFromTop": -1,
                        "aspirate_mmFromBottom": 1,
                        "dispense_mmFromBottom": 0.5
                    },
                    "orderedStepIds": [],
                    "savedStepForms": {
                        "__INITIAL_DECK_SETUP_STEP__": {
                            "id": "__INITIAL_DECK_SETUP_STEP__",
                            "stepType": "manualIntervention",
                            "labwareOrder": {},
                            "moduleLocationUpdate": {
                            },
                            "labwareLocationUpdate": {
                            },
                            "pipetteLocationUpdate": {
                            }
                        }
                    }
                }
            },
            "labwareDefinitions": {},
            "commands": None
        }
        
        self.__commands: List[dict] = []
        
        # saved step form
        # TODO
        self.__saved_step_form: Dict[str, dict] = {}
        self.__ordered_step_ids: List[str] = []
        self.__module_location_update: Dict[str] = {}
        self.__pipette_location_update: Dict[str] = {}
        self.__labware_location_update: Dict[str] = {"fixedTrash": 12} # TODO: temporarily assumed fixedTrash is always on slot 12

        self.__custom_labware_list: Dict[str, dict] = {}
        self.__labware_name_list: List[str] = []
        self.__labware_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/labware')
        self.__labware_json_files = glob.glob(os.path.join(self.__labware_dir, "*.json"))
        for file_path in self.__labware_json_files:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            self.__labware_name_list.append(file_name)
        
        self.__instrument_list: List[Union[Labware, Module]] = []
        self.__liquids_list: List[Liquid] = []

        # store the current arm state
        self.__arm_location: Optional[Union[Well, Column, TrashBin]] = None
        self.__arm_mount: Dict[str, Optional[Union[Pipette, Gripper]]] = {'left': None, 'right': None}

        # init trash bin
        self.trash_bin = self.load_labware('mgi_1_trash_1100ml_fixed', 12)
        self.__instrument_list.append(self.trash_bin)

        self.__display_deck: Dict[str, Dict[str, List[int]]] = {cat: {} for cat in [
            "module", "tip_rack", "tube_rack", "well_plate", 
            "reservoir", "aluminum_block", "adapter"
        ]}    

    def load_gripper(self, mount: Literal['left', 'right']) -> Gripper:
        """Load a gripper onto the specified mount.

        Args:
            mount (str): The mount position, either 'left' or 'right'.

        Returns:
            Gripper: The loaded gripper instance.
        """
        if mount not in _MOUNT_TYPES:
            raise ValueError("Invalid mount. Either `left` or `right`")
        
        if self.__arm_mount[mount] is not None:
            raise ValueError(f"Mount {mount} is already occupied. Please unload the existing instrument first.")

        gripper_id = str(uuid.uuid4())
        g = Gripper(gripper_id, 'gripper', mount, self)
        self.__arm_mount[mount] = g
        return g

    def load_pipette(self, pipette_name: str, mount: Literal['left', 'right']) -> Pipette:
        """Load a pipette onto the specified mount. This method loads a pipette for use in the protocol, validating the pipette name and mount position.

        Args:
            pipette_name (str): The name of the pipette (e.g., 'p1000_single').
            mount (str): The mount position, either 'left' or 'right'.

        Returns:
            Pipette: The loaded pipette instance.
        """
        self.__validate_pipette_name(pipette_name)
        self.__validate_mount(mount)

        pipette_id = str(uuid.uuid4())
        pipette_name = self.__validate_and_revise(pipette_name, _PIPETTE_NAME)

        self._append_command(
            LoadPipetteCommand(
            params=LoadPipetteParams(
                pipetteName=pipette_name,
                mount=mount,
                pipetteId=pipette_id
                )
            ))
        
        self.__pipette_location_update[pipette_id] = mount
        
        p = Pipette(pipette_id, pipette_name, mount, self)
        self.__arm_mount[mount] = p
        return p

    def load_liquid(self, liquid_name: str, description: str = '') -> Liquid:
        """Load a liquid for use in the protocol.

        Args:
            liquid_name (str): The name of the liquid to be loaded.
            description (str, optional): A description of the liquid. Defaults to an empty string.

        Returns:
            Liquid: The loaded liquid instance.
        """
        id = str(len(self.__json['designerApplication']['data']['ingredients']))
        self.__json['designerApplication']['data']['ingredients'][id] = {
            "name": liquid_name,
            "description": description,
            "serialize": False,
            "liquidGroupId": id
        }

        l = Liquid(id=id, name=liquid_name, desc=description, context=self)
        self.__liquids_list.append(l)
        return l
    
    def load_module(self, module_type: str, location: int) -> Union[TemperatureModule, ThermocyclerModule, MagneticModule, HeaterShakerModule, TransportModule]:
        """Load a module onto the specified deck slot. This method loads a specified module for use in the protocol, validating the module type and location.

        Args:
            module_type (str): The type of module to load. Options include 'temperatureModuleV2', 'thermocyclerModuleV2', 'magneticModuleV2', 'heaterShakerModuleV1', 'transportModuleSenderV1', 'transportModuleReceiverV1'.
            location (int): The slot ID (1-12) where the module will be placed.

        Returns:
            Union[TemperatureModule, ThermocyclerModule, MagneticModule, HeaterShakerModule, TransportModule]: The loaded module instance.
        """
        if not self.__auto_revise and module_type not in _MODULE_TYPES:
            raise ValueError(f"Unknown module name. Got: {module_type}. Please make sure that module names are correct.")
        
        module_name = _MODULE_ID_MAP[module_type]
        module_id = f"{str(uuid.uuid4())}:{module_name}"
        module_type = self.__validate_and_revise(module_type, _MODULE_TYPES)
        
        self._append_command(LoadModuleCommand(
            params=LoadModuleParams(
                model=module_type,
                location=Location(slotName=str(location)),
                moduleId=module_id
                )
            ))
        
        self.__module_location_update[module_id] = str(location) if module_name != 'thermocyclerModuleType' else 'span9_10'
        
        module =  _MODULE_CLASSES[module_type](module_id, module_name, location, self)

        self.__update_display_deck(module_type, location)
        self.__instrument_list.append(module)

        return module

    def load_labware(self, labware_name: str, location: Union[int, Module, Labware]) -> Labware:
        """Load a labware onto the specified location. This method loads a labware for use in the protocol, validating the labware name and target location. The location can be a deck slot ID, a module instance, or another labware instance.

        Args:
            labware_name (str): The name of the labware
            location (Union[int, Module, Labware]): The target location for the labware. 
                - If int: Slot ID (1-12) on the deck.
                - If Module: The module instance where the labware will be placed.
                - If Labware: Another labware instance on which this labware will be placed.

        Returns:
            Labware: The loaded labware instance.
        """
        if not self.__auto_revise and labware_name not in self.__labware_name_list:
            raise ValueError(f"Unknown labware name. Got: {labware_name}. Please make sure that pipette names are correct.")

        # Check if location is already occupied
        if isinstance(location, int):
            if any(instrument._get_slot() == location for instrument in self.__instrument_list):
                raise ValueError(f"Slot {location} is already occupied by another labware or module.")
        elif isinstance(location, (Module, Labware)):
            if self._get_labware_on_location(location) is not None:
                raise ValueError(f"{type(location).__name__} {location.id()} already has a labware on it.")

        # validate the labware name
        labware_name = self.__validate_and_revise(labware_name, self.__labware_name_list)
        
        # load json file        
        labware_definition = self.__load_labware_json(labware_name)

        version = labware_definition['version']
        namespace = labware_definition['namespace']
        display_name = labware_definition['metadata']['displayName']
        display_cat = labware_definition['metadata']['displayCategory']
        labware_full_name = f"{namespace}/{labware_name}/{version}"
        labware_id = f"{str(uuid.uuid4())}:{labware_full_name}"

        # add definiton json to output json
        self.__json['labwareDefinitions'][labware_full_name] = labware_definition
        self.__labware_location_update[labware_id] = location.id() if isinstance(location, (Module, Labware)) else str(location)

        if isinstance(location, int):
            _loc = Location(slotName=str(location))    
        elif isinstance(location, Module):
            _loc = Location(moduleId=location.id())
        elif isinstance(location, Labware):
            _loc = Location(labwareId=location.id())
            
        # save command and update the deck
        self._append_command(
            LoadLabwareCommand(
                params=LoadLabwareParams(
                    displayName=display_name,
                    labwareId=labware_id,
                    loadName=labware_name,
                    namespace=namespace,
                    version=version,
                    location=_loc
                )
            )
        )
 
        # create labware instance  
        labware = _LABWARE_CLASSES.get(display_cat, Labware)(
            labware_id, labware_name, location, labware_definition, self
        )
        
        self.__instrument_list.append(labware)

        self.__update_display_deck(labware_name, location)

        if display_cat == 'tipRack':
            # If this is a tip rack, associate it with any pipettes mounted on either arm
            # by mapping the pipette IDs to this tip rack's full name in the JSON config
            for mount in ['left', 'right']:
                if mount in self.__arm_mount and isinstance(self.__arm_mount[mount], Pipette):
                    pipette_id = self.__arm_mount[mount].id()
                    if pipette_id not in self.__json['designerApplication']['data']['pipetteTiprackAssignments']:
                        self.__json['designerApplication']['data']['pipetteTiprackAssignments'][pipette_id] = labware_full_name
                        break

        return labware
    
    def move_labware(self, labware: Labware,
                     location: Union[int, Module, Labware]) -> Labware:
        """Move the labware to the specified location manually.

        This method moves an existing labware to a new location, which can be a deck slot,
        a module, or another labware.

        Args:
            labware (Labware): The labware instance to move.
            location (Union[int, Module, Labware]): The target location for the labware.
                - If int: Slot ID (1-12) on the deck.
                - If Module: The module instance to place the labware on.
                - If Labware: Another labware instance to place this labware on.

        Returns:
            Labware: The moved labware instance.

        Raises:
            ValueError: If the target location is already occupied.
            TypeError: If the location type is not supported.
        """
        if isinstance(location, (Module, Labware)):
            if location.labware is not None and location.labware == labware:
                print(f"Labware {labware._get_name()} is already on {location._get_name()}. Ignore this move.")
                return 

        # check if occupied
        if isinstance(location, (Module, Labware)):
            if location.labware is not None:
                raise ValueError(f"Slot on {location._get_name()} is already occupied. Please unload the existing instrument first.")
        
        if isinstance(location, int):
            if self._get_instrument_by_slot(location) is not None:
                raise ValueError(f"Slot {location._get_name()} is already occupied. Please unload the existing instrument first.")

        # remove from the old location
        old_slot = labware._get_slot()
        if isinstance(old_slot, (Labware, Module)):
            old_slot.labware = None

        # add to the new location
        if isinstance(location, Module):
            new_loc = Location(moduleId=location.id())
            labware._set_slot(location)
            location.labware = labware

        elif isinstance(location, Labware):
            new_loc = Location(labwareId=location.id())
            labware._set_slot(location)
            location.labware = labware

        elif isinstance(location, int):
            new_loc = Location(slotName=str(location))
            labware._set_slot(location)

        self._append_command(MoveLabwareCommand(
            params=MoveLabwareParams(
                labwareId=labware.id(),
                strategy='manualMoveWithPause',
                newLocation=new_loc)
            )
        )
    
    def _get_instrument_by_slot(self, slot: int) -> Union[Module, Labware, None]:
        for i in self.__instrument_list:
            if i._get_slot() == slot:
                return i
        return None
  
    def pause(self, seconds: int=0, wait_for_resume: bool=False) -> None:
        """Pause the protocol execution. This method pauses the protocol for a specified duration or until a manual resume.

        Args:
            seconds (int, optional): The number of seconds to pause. Defaults to 0. Ignored if `wait_for_resume` is True. If not specified, `wait_for_resume` is automatically set to True.
            wait_for_resume (bool, optional): If True, the protocol will wait for a manual resume action. Defaults to False.
        """
        # If seconds is not specified (0), automatically set wait_for_resume to True
        if seconds == 0:
            wait_for_resume = True
            
        if wait_for_resume:
            command = WaitForResumeCommand(
                params=WaitForResumeParams()
            )
        else:
            command = WaitForDurationCommand(
                params=WaitForDurationParams(seconds=seconds)
            )

        self._append_command(command)
    
    def _get_trash_bin(self) -> Labware:
        return self.trash_bin

    def _export(self, save_dir: str=None) -> str:
        """Export the protocol to a JSON string or file.

        Args:
            save_dir (str, optional): Path where the JSON file should be saved. If None, the JSON is only returned
                as a string without saving to disk. Defaults to None.

        Returns:
            str: The protocol JSON as a string.

        Raises:
            ValueError: If the specified save directory path is invalid or doesn't exist.
            PermissionError: If the specified save directory is not writable.
        """

        # drop tip and move to trash bin at the end of the protocol for all pipettes
        for _, p in self.__arm_mount.items():
            if isinstance(p, Pipette):
                p.home()

        self.__json['commands'] = [c.dict() for c in self.__commands]
        self.__json['commands'] = self.__concat_pcr_run_cmd(self.__json['commands'])

        cmd_json = json.dumps(self.__json)

        if save_dir:
            # Check if the directory is valid
            directory = os.path.dirname(save_dir) or '.'
            if not os.path.exists(directory):
                raise ValueError(f"The directory {directory} does not exist.")
            if not os.path.isdir(directory):
                raise ValueError(f"The path {directory} is not a directory.")
            if not os.access(directory, os.W_OK):
                raise PermissionError(f"The directory {directory} is not writable.")
            
            with open(save_dir, 'w') as f:
                f.write(cmd_json)
        
        return cmd_json
    
    def __concat_pcr_run_cmd(self, commands: List[Dict]) -> None:
        """Concatenate consecutive PCR run commands into a single command.

        Args:
            commands (List[Dict]): List of protocol commands to process

        Returns:
            List[Dict]: List of commands with consecutive PCR runs merged
        """
        result = []
        i = 0
        
        while i < len(commands):
            cmd = commands[i]
            
            # Non-PCR commands are added directly
            if cmd['commandType'] != 'thermocycler/runProfile':
                result.append(cmd)
                i += 1
                continue
                
            # Collect consecutive PCR profiles with same parameters
            profiles = [cmd['params']['profile']]
            next_cmd = commands[i + 1] if i + 1 < len(commands) else None
            while (next_cmd and 
                   next_cmd['commandType'] == 'thermocycler/runProfile' and
                   next_cmd['params']['moduleId'] == cmd['params']['moduleId'] and 
                   next_cmd['params']['blockMaxVolumeUl'] == cmd['params']['blockMaxVolumeUl']):
                profiles.append(next_cmd['params']['profile'])
                i += 1
                next_cmd = commands[i + 1] if i + 1 < len(commands) else None
            
            # Combine profiles into single command
            merged_cmd = {
                'commandType': 'thermocycler/runProfile',
                'key': cmd['key'],
                'params': {
                    'moduleId': cmd['params']['moduleId'],
                    'profile': [step for p in profiles for step in p],
                    'blockMaxVolumeUl': cmd['params']['blockMaxVolumeUl']
                }
            }
            result.append(merged_cmd)
            i += 1
            
        return result
    
    def _get_display_deck(self) -> dict:
        return self.__display_deck

    def __load_labware_json(self, labware_name: str) -> dict:
        """Load the labware metadata/definition from JSON.

        Args:
            labware_name (str): Name of the labware

        Returns:
            dict: Labware definition

        Raises:
            ValueError: If JSON is invalid
        """
        # Check custom labware first
        if labware_name in self.__custom_labware_list:
            return self.__custom_labware_list[labware_name]

        # Load from file
        try:
            return json.load(open(os.path.join(self.__labware_dir, f"{labware_name}.json")))
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Error loading labware {labware_name}: {str(e)}")
    
    def __validate_pipette_name(self, pipette_name: str) -> None:
        """Validate pipette name format.
        
        Args:
            pipette_name: The pipette name to validate
            
        Raises:
            ValueError: If pipette name is invalid
        """
        if not self.__auto_revise and not re.match(r'^p\d+_(single|multi)$', pipette_name):
            suggestions = '", "'.join(_PIPETTE_NAME)
            raise ValueError(
                f'Invalid pipette name: "{pipette_name}". '
                f'Valid options are: "{suggestions}"'
            )
    
    def __validate_mount(self, mount: str) -> None:
        """Validate mount position and availability.
    
        Args:
            mount: The mount position to validate
            
        Raises:
            ValueError: If mount is invalid or occupied
        """
        if mount not in _MOUNT_TYPES:
            raise ValueError(f'Invalid mount: "{mount}". Must be either "left" or "right"')
            
        if self.__arm_mount[mount] is not None:
            instrument = self.__arm_mount[mount]
            raise ValueError(
                f'Mount "{mount}" is already occupied.'
            )

    def __validate_and_revise(self, item, valid_list) -> str:
        """check if the item is in valid list, if not, replace with the most similar item.

        Args:
            item (str): item name
            valid_list (list[str]): list of strings

        Raises:
            FileNotFoundError: item not found

        Returns:
            str: validate item name
        """
        def most_similar_string(a, b):
            """find the similar string from b given a

            Args:
                a (str): string
                b (list[str]): list of strings

            Returns:
                str: most similar string in b
            """
            return min(b, key=lambda x: Levenshtein.distance(a, x))
        
        if item not in valid_list:
            revised_item = most_similar_string(item, valid_list)
            if self.__auto_revise:
                print(f'Auto revised {item} to {revised_item}')
                return revised_item
            else:
                raise FileNotFoundError(f"Unsupported item: {item}, do you mean: {revised_item}?")
        return item
    
    def __update_display_deck(self, labware_name: str, loc: Union[int, Labware, Module]) -> None:
        """update the deck status

        Args:
            labware_name (str): labware name
            slot (int): slot id
        """
        if labware_name in _MODULE_ID_MAP.keys():
            cat = 'module'
        else:
            metadata = self.__load_labware_json(labware_name)
            display_cat = metadata['metadata']['displayCategory']
            cat = _DECK_LABWARE_TYPE_MAP[display_cat]

        # skip the trash (no need to update)
        if cat == 'trash': return

        # get the real slot id
        _loc = self.__get_real_slot(loc)

        self.__display_deck[cat].setdefault(labware_name,[]).append(_loc)
    
    def __get_real_slot(self, loc: Union[Module, Labware]) -> int:
        # keep finding the real slot id
        _loc = loc
        while not isinstance(_loc, int):
            _loc = _loc._get_slot()
        return _loc

    def _get_labware_on_location(self, location: Union[Module, Labware]) -> Optional[Labware]:
        """Get the labware instance that is placed on the given location (module/labware).

        This method recursively checks for any labware placed on the given location.
        For example, if an adapter is placed on a module, and a plate is placed on that adapter,
        this will return the plate.

        Args:
            location (Union[Module, Labware]): The module or labware to check for labware on top

        Returns:
            Optional[Labware]: The labware instance placed on the module/labware, or None if no labware found
        """
        for instrument in self.__instrument_list:
            if isinstance(instrument, Labware) and instrument._get_slot() == location:
                # Recursively check if there's labware on this labware
                labware_on_top = self._get_labware_on_location(instrument)
                return labware_on_top if labware_on_top else instrument
        return None
     
    def _get_same_type_labware(self, labware: Labware) -> List[Labware]:
        """Get labwares of the same type as the given labware.

        Args:
            labware (Labware): Reference labware instance.

        Returns:
            List[Labware]: List of matching labware instances.
        """
        return [l for l in self.__instrument_list if l._get_name() == labware._get_name() and l != labware]
    
    def _auto_get_tiprack(self, volume: Union[int, float, None]=None, n_tip: Union[int, None]=None) -> Union[TipRack, None]:
        """Get the most suitable tiprack based on volume and number of tips needed.
        
        Args:
            volume: Target volume needed. If provided, finds tiprack with closest max volume.
            n_tip: Number of tips needed (1 or 8). If provided, checks tip availability.
            
        Returns:
            Most suitable TipRack, or None if no tipracks found.
        """
        # Get available tipracks sorted by most used first (to maximize tip usage)
        tipracks = sorted([l for l in self.__instrument_list if isinstance(l, TipRack)], 
                         key=lambda x: x._get_used_tip_count(), reverse=True)
        
        # Return None if no tipracks found
        if not tipracks:
            return None
            
        # If no volume specified, find first tiprack with enough tips
        # if no n_tip specified, just return the first tiprack
        if volume is None:
            if n_tip:
                # Return first tiprack that has enough tips available
                return next((t for t in tipracks if t._is_has_tip(n_tip)), None)
            return tipracks[0]
            
        # With volume specified, find tiprack with closest max volume
        if n_tip:
            # Filter to only tipracks with enough tips available if n_tip specified
            available = [t for t in tipracks if t._is_has_tip(n_tip)]
        else:
            available = tipracks
            
        # Return tiprack with volume capacity closest to target volume
        return min(available, key=lambda t: abs(t._get_max_volume() - volume))


    def _get_labware_compatibility(self) -> dict:
        """
        Get the compatibility list for each labware and module.

        Returns:
            dict: Compatibility list for labware and modules.
        """
        result = {}
        for file_path in self.__labware_json_files:
            with open(file_path, 'r') as f:
                data = json.load(f)
                load_name = data['parameters']['loadName']
                
                # Extract compatibility information
                labware_compat = data.get('stackingOffsetWithLabware', {})
                module_compat = data.get('stackingOffsetWithModule', {})
                
                if labware_compat or module_compat:
                    result[load_name] = {}
                    if labware_compat:
                        result[load_name]['available_adapters'] = list(labware_compat.keys())
                    if module_compat:
                        result[load_name]['available_modules'] = list(module_compat.keys())
        
        return result
    
    def _append_command(self, command: Any) -> None:
        self.__commands.append(command)
        
    def _append_saved_step_form(self, command: Any) -> None:
        self.__saved_step_form[command.id] = command
        self.__ordered_step_ids.append(command.id)
    
    def _set_arm_location(self, location: Union[Well, Column, TrashBin]) -> None:
        self.__arm_location = location
    
    def _get_arm_location(self) -> Union[Well, Column, TrashBin, None]:
        return self.__arm_location
    
    def add_custom_labware(self, file_paths: Union[str, List[str]]):
        """
        Adds custom labware definitions to the protocol from JSON definition files.

        Args:
            file_paths (Union[str, List[str]]): Path or list of paths to JSON labware definition files.
                Each file must contain required fields: metadata, wells, parameters, version, namespace.

        Raises:
            FileNotFoundError: If any of the specified files cannot be found.
            ValueError: If any file contains invalid JSON or is missing required fields.

        The JSON files must define labware with:
        - metadata: General labware information
        - wells: Well definitions and coordinates 
        - parameters: Including loadName for referencing the labware
        - version: Schema version
        - namespace: Labware namespace
        """
        file_paths = [file_paths] if isinstance(file_paths, str) else file_paths
        
        for path in file_paths:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"Metadata file not found: {path}")
            
            try:
                with open(path, 'r') as file:
                    metadata = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON in file: {path}")
            
            # Validate required fields
            if not all(field in metadata for field in ['metadata', 'wells', 'parameters', 'version', 'namespace']):
                raise ValueError(f"Missing required field(s) in file: {path}")
            
            load_name = metadata['parameters']['loadName']
            self.__labware_name_list.append(load_name)
            self.__custom_labware_list[load_name] = metadata
    
    def _get_behind_slot(self, slot: int) -> Union[int, None]:
        """Get the slot number behind the given slot.
        +--------+--------+-----------+
        | Slot 1 | Slot 5 | Slot 9    |
        +--------+--------+-----------+
        | Slot 2 | Slot 6 | Slot 10   |
        +--------+--------+-----------+
        | Slot 3 | Slot 7 | Slot 11   |
        +--------+--------+-----------+
        | Slot 4 | Slot 8 | Slot 12   |
        |        |        |           |
        +--------+--------+-----------+
        """
        return {2:1, 3:2, 4:3, 6:5, 7:6, 8:7, 10:9, 11:10, 12:11}.get(slot)
    
    def _check_collision(self, location: Union[Well, Column]) -> None:
        """Check for potential collisions when accessing a location.
        
        This function checks if there are any collision risks when trying to access a given location,
        particularly with labware or modules in slots behind the target location.

        Args:
            location (Union[Well, Column]): The location to check for collision risks.

        Raises:
            ValueError: If there is a collision risk from a module or taller labware in the slot behind.
        """
        # Get the actual deck slot number for the location
        slot = self.__get_real_slot(location._get_parent())
        behind_slot = self._get_behind_slot(slot)

        if behind_slot is None:
            return

        behind_item = self._get_instrument_by_slot(behind_slot)
        if behind_item is None:
            return
        
        # Modules always block access
        if isinstance(behind_item, Module):
            raise ValueError(f"Cannot access slot {slot} - blocked by module in slot {behind_slot}")

        # Calculate heights of labware stacks
        current_height = 0
        current = location._get_parent()
        while isinstance(current, Labware):
            current_height += current._get_height()
            current = current._get_slot()

        behind_height = 0
        behind = behind_item  
        while isinstance(behind, Labware):
            behind_height += behind._get_height()
            behind = behind._get_slot()

        if current_height <= behind_height:
            raise ValueError(f"Cannot access slot {slot} - blocked by taller labware in slot {behind_slot}")

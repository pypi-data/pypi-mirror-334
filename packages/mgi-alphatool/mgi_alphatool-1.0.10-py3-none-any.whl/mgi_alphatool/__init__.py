from .context import Context
from .handler.gripper import Gripper
from .handler.pipette import Pipette
from .liquid import Liquid
from .labware import Labware
from .module import Module

def init(robot_type: str = 'alphatool', 
         deck_type: str = 'alphatool_standard', 
         home_slot: int = 12,
         auto_revise=True) -> Context:
    """Initialize the protocol context. This function sets up the protocol context based on the alphatool.

    Args:
        robot_type (str): Type of robot to use (e.g. 'alphatool')
        deck_type (str): Type of deck to use (e.g. 'alphatool_standard')
        auto_revise (bool): If True, automatically corrects name errors for pipette, module, and labware if possible. Defaults to True.

    Returns:
        Context: The initialized protocol context.
    """
    # if robot_type == 'alphatool':
    #     return Context(robot_type=robot_type, auto_revise=auto_revise)
    # else:
    #     raise ValueError(f"Unsupported robot type: {robot_type}")
    return Context(robot_type=robot_type, deck_type=deck_type, home_slot=home_slot, auto_revise=auto_revise)
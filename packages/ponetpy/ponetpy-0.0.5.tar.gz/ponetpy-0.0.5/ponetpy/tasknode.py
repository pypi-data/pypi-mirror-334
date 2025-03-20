from ponetpy.logical import Logical, Relationship
from ponetpy.mode import Mode
from typing import List


class TaskNode:
    def __init__(self, action_number: int, predecessor: List[Logical], modes: List[Mode], **kwargs):
        self.action_number: int = action_number
        self.predecessors: List[Logical] = predecessor
        self.successors: List[Logical] = []
        self.modes: List[Mode] = modes
        self.ES = 0  # early start
        self.EF = 0  # early finish
        self.LS = 0  # late start
        self.LF = 0  # late finish
        self.slack = 0  # time reserve
        self.critical = False
        self.random: int = 0
        self.parameters = {}
        self._set_kwargs(kwargs)

    def _set_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_param(self, param: str):
        return getattr(self, param)

    def set_selected_mode(self, random_number: int):
        self.random = random_number

    def get_mode(self) -> Mode:
        return self.modes[self.random]

    def get_duration(self):
        return self.get_mode().duration

    def get_cost(self):
        return self.get_mode().cost

    def can_be_ignore(self, unset_task_nodes: List['TaskNode'], is_early: bool = True) -> bool:
        if is_early:
            return len(unset_task_nodes) != 0 and self.EF != 0
        else:
            return len(unset_task_nodes) != 0 and self.LS != 0

    def can_be_unset(self, is_early: bool = True, **kwargs) -> bool:
        if is_early:
            return self.EF == 0
        else:
            relationship = kwargs.get("relationship")
            if relationship is None:
                return self.LS == 0
            else:
                return self.LS == 0 and relationship != Relationship.SS

from typing import List, TypeVar
from ponetpy.tasknode import TaskNode
from ponetpy.logical import Logical, DurType

T = TypeVar("T", bound="TaskNode")


def get_task_by_index(action_number, task_nodes: List[T]) -> T:
    return next((w for w in task_nodes if w.action_number == action_number), task_nodes[0])


def set_early(task_nodes: List[TaskNode]):
    unset_task_nodes = []
    while True:
        for task_node in task_nodes:
            if task_node.can_be_ignore(unset_task_nodes): continue
            if len(task_node.predecessors) == 0:
                task_node.ES = 0
                task_node.EF = task_node.modes[task_node.random].duration
            else:
                es = []
                dur = task_node.get_duration()
                is_unset_task = False
                for predecessor in task_node.predecessors:
                    task_node_pred = get_task_by_index(predecessor.action_number, task_nodes)
                    if task_node_pred.can_be_unset():
                        is_unset_task = True
                        break
                    es_cal = predecessor.cal_dur(DurType.START, dur, task_node_pred.ES, task_node_pred.EF)
                    es.append(es_cal)
                if is_unset_task:
                    if task_node not in unset_task_nodes:
                        unset_task_nodes.append(task_node)
                    continue

                if task_node in unset_task_nodes:
                    unset_task_nodes.remove(task_node)
                task_node.ES = max(es)
                task_node.EF = task_node.ES + dur
        if len(unset_task_nodes) == 0: break


def set_late(task_nodes: List[TaskNode], max_late_finish: float):
    unset_task_nodes = []
    while True:
        for task_node in task_nodes:
            if task_node.can_be_ignore(unset_task_nodes, False): continue
            if len(task_node.successors) == 0:
                task_node.LF = max_late_finish
                task_node.LS = task_node.LF - task_node.modes[task_node.random].duration
            else:
                min_ls = []
                current_dur = task_node.get_duration()
                has_unknown = False
                for successor in task_node.successors:
                    task_node_suc = get_task_by_index(successor.action_number, task_nodes)
                    if task_node_suc.can_be_unset(False, relationship=successor.relationship):
                        has_unknown = True
                        break
                    temp_ls = successor.cal_dur(DurType.LATE, current_dur, task_node_suc.LS, task_node_suc.LF)
                    min_ls.append(temp_ls)

                if has_unknown:
                    if task_node not in unset_task_nodes:
                        unset_task_nodes.append(task_node)
                    continue

                if task_node in unset_task_nodes:
                    unset_task_nodes.remove(task_node)

                task_node.LS = min(min_ls)
                task_node.LF = task_node.LS + current_dur
        if len(unset_task_nodes) == 0: break


def set_random_mode(task_nodes: List[TaskNode], random_modes: List[int]):
    for index, t in enumerate(task_nodes):
        t.set_selected_mode(random_modes[index])


def set_critical(task_nodes: List[TaskNode]):
    for task_node in task_nodes:
        task_node.slack = task_node.LS - task_node.ES
        task_node.critical = task_node.slack == 0


def set_successor(task_nodes: List[TaskNode]):
    for task_node in task_nodes:
        if len(task_node.predecessors) != 0:
            for predecessor in task_node.predecessors:
                logical = Logical(task_node.action_number, predecessor.relationship, predecessor.lag)
                task_node_pred = get_task_by_index(predecessor.action_number, task_nodes)
                task_node_pred.successors.append(logical)


def get_end_work_infos(task_nodes: List[TaskNode]):
    return [task for task in task_nodes if len(task.successors) == 0]


def calc_time(task_nodes: List[TaskNode]):
    set_early(task_nodes)
    return max(t.EF for t in get_end_work_infos(task_nodes))


def calc_cost(task_nodes: List[TaskNode]):
    return sum([t.get_cost() for t in task_nodes])
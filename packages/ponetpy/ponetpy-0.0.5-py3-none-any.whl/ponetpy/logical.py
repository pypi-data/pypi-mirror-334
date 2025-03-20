from enum import Enum


class DurType(Enum):
    START = 1
    LATE = 2


class Relationship(Enum):
    Invalid = 1
    FS = 2
    SS = 3
    SF = 4
    FF = 5


class Logical:
    def __init__(self, action_number, relationship=Relationship.Invalid, lag=0):
        self.action_number = action_number
        self.relationship = relationship
        self.lag = lag

    def cal_dur(self, dur_type, current_dur, e_dur, l_dur):
        if self.relationship == Relationship.Invalid:
            if dur_type == DurType.START:
                return l_dur
            else:
                return e_dur - current_dur

        elif self.relationship == Relationship.SF:
            if dur_type == DurType.START:
                return e_dur + self.lag - current_dur
            else:
                return l_dur - self.lag

        elif self.relationship == Relationship.FS:
            if dur_type == DurType.START:
                return l_dur + self.lag
            else:
                return e_dur - self.lag - current_dur

        elif self.relationship == Relationship.SS:
            if dur_type == DurType.START:
                return e_dur + self.lag
            else:
                return e_dur - self.lag

        else:
            if dur_type == DurType.START:
                return l_dur + self.lag - current_dur
            else:
                return l_dur - self.lag - current_dur
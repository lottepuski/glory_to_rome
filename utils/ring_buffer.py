__author__ = 'aravind'
__desc__ = "Implements a simple ring buffer"
from collections import deque


class RingBuffer(object):
    def __init__(self):
        super(RingBuffer, self).__init__()
        self._queue = deque()

    def _add_object(self, obj):
        self._queue.append(obj)

    def _remove_object(self, obj):
        self._queue.remove(obj)

    def _advance_right(self, n=1):
        self._queue.rotate(-n)

    def _get_head_obj(self):
        return self._queue[0]

    def _objs_to_list(self):
        return list(self._queue)

    def _get_num_objs(self):
        return len(self._queue)

    def _get_obj_at_index(self, index):
        if index < self._get_num_objs():
            return self._queue[index]
        else:
            return self._queue[index % self._get_num_objs()]

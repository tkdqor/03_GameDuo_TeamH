import redis


class RedisQueue(object):
    """
    Assignee : 민지

    Redis로 구현한 Queue 입니다.
    """

    def __init__(self, name, **redis_kwargs):
        self.key = name
        self.rq = redis.Redis(**redis_kwargs)

    def size(self):
        return self.rq.llen(self.key)

    def isEmpty(self):
        return self.size() == 0

    def put(self, element):
        """왼쪽으로 push 합니다."""
        self.rq.lpush(self.key, element)

    def get(self, isBlocking=False, timeout=None):
        if isBlocking:
            """큐에 요소가 없을때, pop을 막습니다."""
            element = self.rq.brpop(self.key, timeout=timeout)
            element = element[1]
        else:
            element = self.rq.rpop(self.key)
        return element

    def set_empty(self):
        self.rq.flushall()

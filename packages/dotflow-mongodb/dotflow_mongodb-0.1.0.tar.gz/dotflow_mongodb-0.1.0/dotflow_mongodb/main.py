"""Dotflow MongoDB"""


from typing import Callable

from dotflow.abc.storage import Storage
from dotflow.core.context import Context


class StorageMongoDB(Storage):
    """Storage"""

    def __init__(self, *args, **kwargs):
        super().__init__()

    def post(self, key: str, context: Context) -> None:
        """Post context somewhere"""

    def get(self, key: str) -> Context:
        """Get context somewhere"""
        return Context()

    def key(self, task: Callable):
        """Function that returns a key to get and post storage"""
        return f"{task.workflow_id}-{task.task_id}"

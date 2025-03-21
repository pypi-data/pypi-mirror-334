import pprint
from datetime import datetime
from typing import Optional

from h2o_secure_store.clients.secret.state import SecretState
from h2o_secure_store.gen.model.v1_secret import V1Secret


class Secret:
    def __init__(
            self,
            name: str = "",
            state: SecretState = SecretState.STATE_UNSPECIFIED,
            creator: str = "",
            deleter: str = "",
            uid: str = "",
            create_time: Optional[datetime] = None,
            delete_time: Optional[datetime] = None,
            purge_time: Optional[datetime] = None,
    ):
        """
        Args:
            name (str, optional): Resource name of the Secret. Format is `workspaces/*/secrets/*`.
            state (SecretState, optional): The current state of the Secret.
            creator (str, optional): Name of an entity that created the Secret.
            deleter (str, optional): Name of an entity that deleted the Secret.
            uid (str, optional): Globally unique identifier of the resource.
            create_time (str, datetime): Time when the Secret was created.
            delete_time (str, datetime): Time when the Secret was deleted.
            purge_time (str, datetime): Time when the Secret is scheduled to be purged.
        """

        self.name = name
        self.state = state
        self.creator = creator
        self.deleter = deleter
        self.uid = uid
        self.create_time = create_time
        self.delete_time = delete_time
        self.purge_time = purge_time

    def get_secret_id(self) -> str:
        segments = self.name.split("/")
        if len(segments) != 4:
            return ""

        return segments[3]

    def get_workspace_id(self) -> str:
        segments = self.name.split("/")
        if len(segments) != 4:
            return ""

        return segments[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def to_api_object(self) -> V1Secret:
        return V1Secret()


def from_api_object(api_object: V1Secret) -> Secret:
    return Secret(
        name=api_object.name,
        state=SecretState(str(api_object.state)),
        creator=api_object.creator,
        deleter=api_object.deleter,
        create_time=api_object.create_time,
        delete_time=api_object.delete_time,
        purge_time=api_object.purge_time,
        uid=api_object.uid,
    )

from typing import Any
from typing_extensions import deprecated

from .cid.multikey import Multikey
from .core import Activity, Link, Object
from .ext.emoji import Emoji
from .schema.propertyvalue import PropertyValue

# For Federation
from .security.cryptographickey import CryptographicKey
from .vocab.activity import (
    Accept,
    Announce,
    Block,
    Create,
    Delete,
    Dislike,
    Flag,
    Follow,
    IntransitiveActivity,
    Like,
    Listen,
    Move,
    Question,
    Read,
    Reject,
    Remove,
    TentativeReject,
    Travel,
    Undo,
    Update,
    View,
)
from .vocab.document import Audio, Document, Image, Page, Video
from .vocab.link import Hashtag, Mention
from .vocab.object import (
    Application,
    Collection,
    Group,
    Note,
    Organization,
    Person,
    Profile,
    Service,
    Tombstone,
)
from .cid.data_integrity_proof import DataIntegrityProof

base_mapper = {
    "Object": Object,
    "Activity": Activity,
    "Link": Link,
    "Mention": Mention,
    "Accept": Accept,
    "Reject": Reject,
    "TentativeReject": TentativeReject,
    "Remove": Remove,
    "Undo": Undo,
    "Create": Create,
    "Delete": Delete,
    "Update": Update,
    "Follow": Follow,
    "View": View,
    "Listen": Listen,
    "Read": Read,
    "Move": Move,
    "Travel": Travel,
    "Announce": Announce,
    "Block": Block,
    "Flag": Flag,
    "Like": Like,
    "Dislike": Dislike,
    "IntransitiveActivity": IntransitiveActivity,
    "Question": Question,
    "Document": Document,
    "Page": Page,
    "Audio": Audio,
    "Image": Image,
    "Video": Video,
    "Profile": Profile,
    "Tombstone": Tombstone,
    "Collection": Collection,
    "Person": Person,
    "Application": Application,
    "Group": Group,
    "Service": Service,
    "Organization": Organization,
    "Note": Note,
}

fedi_mapper = {
    **base_mapper,
    "CryptographicKey": CryptographicKey,
    "Key": CryptographicKey,
    "PropertyValue": PropertyValue,
    "Emoji": Emoji,
    "Hashtag": Hashtag,
    "Multikey": Multikey,
    "DataIntegrityProof": DataIntegrityProof,
}


def load(
    object: dict[Any, Any], custom_mapper: dict = fedi_mapper
) -> Object | Link | dict | Any:  # type: ignore
    """convert json object to model

    Args:
        object (dict[Any, Any]): json object
        custom_mapper (dict, optional): Models available at the time of loading. Defaults to fedi_mapper.

    Returns:
        Object | Link | dict | Any: An object converted from json. If there is no corresponding object, the dictionary type is returned.
    """
    type = object.get("type")
    cls = custom_mapper.get(type)
    if cls:
        return cls(**object)
    return object


class StreamsLoader:
    @staticmethod
    @deprecated("StreamsLoader.load is deprecated; use loader.load.")
    def load(
        object: dict[Any, Any], custom_mapper: dict = fedi_mapper
    ) -> Object | Link | Any | dict:  # type: ignore
        """convert json object to model

        Args:
            object (dict[Any, Any]): json object
            custom_mapper (dict, optional): Models available at the time of loading. Defaults to fedi_mapper.

        Returns:
            Object | Link | dict | Any: An object converted from json. If there is no corresponding object, the dictionary type is returned.
        """
        return load(object, custom_mapper)

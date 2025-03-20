# from datetime import datetime
import re
import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pyfill import datetime

from .cid.data_integrity_proof import DataIntegrityProof
from .funcs import merge_contexts
from apmodel.funcs import _make_accept, _make_reject

if TYPE_CHECKING:
    from .vocab.document import Image
    from .vocab.object import Collection



class Object:
    def __init__(
        self,
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        type: str = "Object",
        id: Optional[str] = None,
        attachment: List[Union["Object", "Link", dict]] = [],
        attributedTo: Optional[Union["Object", "Link", str]] = None,
        audience: Optional[Union["Object", "Link"]] = None,
        content: Optional[str] = None,
        context: Optional[Union["Object", "Link"]] = None,
        name: Optional[str] = None,
        endTime: Optional[str] = None,
        generator: Optional[Union["Object", "Link"]] = None,
        icon: Optional[Union["Image", "Link"]] = None,
        image: Optional["Image"] = None,
        inReplyTo: Optional[Union["Image", "Link"]] = None,
        location: Optional[Union["Image", "Link"]] = None,
        preview: Optional[Union["Object", "Link"]] = None,
        published: Optional[str] = None,
        replies: Optional["Collection"] = None,
        startTime: Optional[str] = None,
        summary: Optional[str] = None,
        tag: Optional[Union["Object", "Link"]] = None,
        updated: Optional[str] = None,
        url: Optional[Union[str, "Link"]] = None,
        to: Optional[Union["Object", "Link"]] = None,
        bto: Optional[Union["Object", "Link"]] = None,
        cc: Optional[Union["Object", "Link"]] = None,
        bcc: Optional[Union["Object", "Link"]] = None,
        mediaType: Optional[str] = None,
        duration: Optional[str] = None,
        sensitive: Optional[bool] = None,
        **kwargs,
    ):
        """Implements the "Object" primary base type of the ActivityStreams vocabulary.

        Args:
            _context (Union[str, list], optional): 
                The default value for @context. Defaults to "https://www.w3.org/ns/activitystreams".
            type (str, optional): 
                The name of the ActivityStreams type. Usually does not need to be changed. Defaults to "Object".
            id (Optional[str], optional): 
                The identifier for the object. Defaults to None.
            attachment (List[Union["Object", "Link", dict]], optional): 
                A list of resources attached to the object. Defaults to an empty list.
            attributedTo (Optional[Union["Object", "Link", str]], optional): 
                The resource indicating the creator of this object. Defaults to None.
            audience (Optional[Union["Object", "Link"]], optional): 
                The resource indicating the intended audience of this object. Defaults to None.
            content (Optional[str], optional): 
                The text representing the content of the object. Defaults to None.
            context (Optional[Union["Object", "Link"]], optional): 
                The resource indicating the context of the object. Defaults to None.
            name (Optional[str], optional): 
                The name of the object. Defaults to None.
            endTime (Optional[str], optional): 
                The end time of the event represented as an ISO8601 formatted string. Defaults to None.
            generator (Optional[Union["Object", "Link"]], optional): 
                The resource indicating the application that generated the object. Defaults to None.
            icon (Optional[Union["Image", "Link"]], optional): 
                The resource for the icon of the object. Defaults to None.
            image (Optional["Image"], optional): 
                The resource for the image of the object. Defaults to None.
            inReplyTo (Optional[Union["Image", "Link"]], optional): 
                The resource indicating the target of this reply. Defaults to None.
            location (Optional[Union["Image", "Link"]], optional): 
                The resource indicating the location of the object. Defaults to None.
            preview (Optional[Union["Object", "Link"]], optional): 
                The resource for the preview of the object. Defaults to None.
            published (Optional[str], optional): 
                The date and time when the object was published, represented as an ISO8601 formatted string. Defaults to None.
            replies (Optional["Collection"], optional): 
                A collection of replies to this object. Defaults to None.
            startTime (Optional[str], optional): 
                The start time of the event represented as an ISO8601 formatted string. Defaults to None.
            summary (Optional[str], optional): 
                A summary of the object. Defaults to None.
            tag (Optional[Union["Object", "Link"]], optional): 
                The resource indicating tags related to the object. Defaults to None.
            updated (Optional[str], optional): 
                The date and time when the object was last updated, represented as an ISO8601 formatted string. Defaults to None.
            url (Optional[Union[str, "Link"]], optional): 
                The URL of the object. Defaults to None.
            to (Optional[Union["Object", "Link"]], optional): 
                The resource indicating the recipient of the object. Defaults to None.
            bto (Optional[Union["Object", "Link"]], optional): 
                The resource indicating BCC recipients. Defaults to None.
            cc (Optional[Union["Object", "Link"]], optional): 
                The resource indicating CC recipients. Defaults to None.
            bcc (Optional[Union["Object", "Link"]], optional): 
                The resource indicating BCC recipients. Defaults to None.
            mediaType (Optional[str], optional): 
                The media type of the object. Defaults to None.
            duration (Optional[str], optional): 
                A string representing the duration of the object. Defaults to None.
            sensitive (Optional[bool], optional): 
                A flag indicating the sensitivity of the content. Defaults to None.

        """
        from .loader import load

        ctx = kwargs.get("@context")
        self._context = merge_contexts(_context, ctx) if ctx else []
        self.type = type
        self.id = id
        self.attachment = [
            load(attach) if isinstance(attach, dict) else attach
            for attach in attachment
        ]
        self.attributedTo = (
            load(attributedTo)
            if isinstance(attributedTo, dict)
            else attributedTo
        )
        self.audience = (
            load(audience) if isinstance(audience, dict) else audience
        )
        self.content = content
        self.context = (
            load(context) if isinstance(context, dict) else context
        )
        self.name = name
        self.endTime = (
            (
                endTime
                if isinstance(endTime, datetime.datetime.datetime)
                else datetime.datetime.datetime.strptime(
                    endTime, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            )
            if endTime
            else endTime
        )
        self.generator = (
            load(generator) if isinstance(generator, dict) else generator
        )
        self.icon = load(icon) if isinstance(icon, dict) else icon
        self.image = image
        self.inReplyTo = (
            load(inReplyTo) if isinstance(inReplyTo, dict) else inReplyTo
        )
        self.location = (
            load(location) if isinstance(location, dict) else location
        )
        self.preview = (
            load(preview) if isinstance(preview, dict) else preview
        )
        if published:
            self.published = (
                (
                    published
                    if isinstance(published, datetime.datetime.datetime)
                    else datetime.datetime.datetime.strptime(
                        published, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                )
                if published
                else published
            )
        else:
            self.published = datetime.utcnow()
        self.replies = (
            load(replies) if isinstance(replies, dict) else replies
        )
        self.startTime = (
            (
                startTime
                if isinstance(startTime, datetime.datetime.datetime)
                else datetime.datetime.datetime.strptime(
                    startTime, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            )
            if startTime
            else startTime
        )
        self.summary = summary
        self.tag = load(tag) if isinstance(tag, dict) else tag
        self.updated = updated
        self.url = load(url) if isinstance(url, dict) else url
        self.to = load(to) if isinstance(to, dict) else to
        self.bto = load(bto) if isinstance(bto, dict) else bto
        self.cc = load(cc) if isinstance(cc, dict) else cc
        self.bcc = load(bcc) if isinstance(bcc, dict) else bcc
        self.mediaType = mediaType
        self.duration = duration

        # --- Extend Value
        self.sensitive = sensitive
        # ---

        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None, build_context: bool = True):
        """Outputs the current object as a dictionary.

        Args:
            _extras (Optional[dict], optional): Arguments used internally. It is not recommended that users change them.
            build_context (bool): Do we automatically build @context based on the arguments? Defaults to True.

        Returns:
            dict: Objects converted to dictionaries
        """
        if not _extras:
            _extras = self._extras.copy()
        instance_vars = vars(self).copy()

        ctx = self._context.copy()
        if build_context:
            attrs = dir(self)

            ctx2 = []
            ctx2_d = {}
            if _extras.get("publicKey") or "publicKey" in attrs:
                ctx2.append("https://w3id.org/security/v1")

            # Mastodon
            if _extras.get("featured") or "featured" in attrs:
                ctx2_d["featured"] = {
                    "@id": "http://joinmastodon.org/ns#featured",
                    "@type": "@id",
                }
            if _extras.get("featuredTags") or "featuredTags" in attrs:
                ctx2_d["featuredTags"] = {
                    "@id": "http://joinmastodon.org/ns#featuredTags",
                    "@type": "@id",
                }
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if (
                _extras.get("manuallyApprovesFollowers")
                or "manuallyApprovesFollowers" in attrs
            ):
                ctx2_d["manuallyApprovesFollowers"] = "as:manuallyApprovesFollowers"

            # Misskey
            if (
                _extras.get("_misskey_content")
                or _extras.get("_misskey_summary")
                or _extras.get("_misskey_quote")
                or _extras.get("_misskey_reaction")
                or _extras.get("_misskey_votes")
                or _extras.get("_misskey_talk")
                or _extras.get("isCat")
                or _extras.get("_misskey_followedMessage")
                or _extras.get("_misskey_requireSigninToViewContents")
                or _extras.get("_misskey_makeNotesFollowersOnlyBefore")
                or _extras.get("_misskey_makeNotesHiddenBefore")
                or _extras.get("_misskey_license")
            ):
                ctx2_d["misskey"] = "https://misskey-hub-net/ns#"

            ctx2.append(ctx2_d)

        context: Optional[list] = instance_vars.get("@context")
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = ctx
        data: Dict[str, Any] = {
            "@context": context,
        }

        if self.content is not None:
            data["content"] = self.content

        for key, value in instance_vars.items():
            if value is not None:
                if not key.startswith("_") and key != "content":
                    if isinstance(value, datetime.datetime.datetime):
                        data[key] = value.isoformat(timespec='microseconds').replace('+00:00', 'Z')
                    elif isinstance(value, Object):
                        data[key] = value.to_dict(_extras=value._extras)
                    elif isinstance(value, list):
                        data[key] = [
                            item.to_dict(_extras=item._extras)
                            if hasattr(item, "to_dict")
                            else item
                            for item in value
                        ]
                    elif (
                        isinstance(value, dict)
                        or isinstance(value, int)
                        or isinstance(value, bool)
                    ):
                        data[key] = value
                    else:
                        data[key] = str(value)

        _extras = _extras or {}
        for key, value in self._extras.items():
            if value is not None:
                if isinstance(value, datetime.datetime.datetime):
                    data[key] = value.isoformat(timespec='microseconds').replace('+00:00', 'Z')
                elif isinstance(value, Object):
                    data[key] = value.to_dict(_extras=value._extras)
                elif isinstance(value, list):
                    data[key] = [
                        item.to_dict(_extras=item._extras)
                        if hasattr(item, "to_dict")
                        else item
                        for item in value
                    ]
                elif (
                    isinstance(value, dict)
                    or isinstance(value, int)
                    or isinstance(value, bool)
                ):
                    data[key] = value
                else:
                    data[key] = str(value)
        return data


class Link:
    def __init__(
        self,
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        type: str = "Link",
        id: Optional[str] = None,
        href: Optional[str] = None,
        rel: Optional[list[str]] = None,
        mediaType: Optional[str] = None,
        name: Optional[str] = None,
        hreflang: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        preview: Optional[Union[Object, "Link"]] = None,
        **kwargs,
    ):
        """Represents a Link object in Activity Streams 2.0.

        This class implements the Link type, which is used to represent 
        a hyperlink to a resource. The Link object can contain various 
        attributes that provide metadata about the link.

        Args:
            _context (Union[str, list], optional): 
                The default value for @context. It can be a string 
                or a list of strings. Defaults to "https://www.w3.org/ns/activitystreams".
            type (str, optional): 
                The type of the object. For this class, it is always "Link". 
                Defaults to "Link".
            id (Optional[str], optional): 
                A unique identifier for the link object. 
                This can be a URL or an IRI. Defaults to None.
            href (Optional[str], optional): 
                The URL that the link points to. It must conform to 
                the xsd:anyURI format. If provided, it must be a valid URI. 
                Defaults to None.
            rel (Optional[list[str]], optional): 
                A list of relationship types indicating the nature 
                of the link with respect to the context of the link. 
                Defaults to None.
            mediaType (Optional[str], optional): 
                The media type of the linked resource, such as 
                "image/jpeg". Defaults to None.
            name (Optional[str], optional): 
                A human-readable name for the link. Defaults to None.
            hreflang (Optional[str], optional): 
                The language of the linked resource, represented 
                as a language tag. Defaults to None.
            height (Optional[int], optional): 
                The height of the linked resource in pixels. 
                Must be greater than or equal to 0. Defaults to None.
            width (Optional[int], optional): 
                The width of the linked resource in pixels. 
                Must be greater than or equal to 0. Defaults to None.
            preview (Optional[Union["Object", "Link"]], optional): 
                A resource that provides a preview of the linked 
                content, which could be another Link or an Object. 
                Defaults to None.
            **kwargs: 
                Additional properties that can be added to the Link 
                object, allowing for extensibility.

        Raises:
            ValueError: 
                If `href` is not a valid URI, if `height` is negative, 
                or if `width` is negative.

        """
        if href:
            if not re.fullmatch(r"(%(?![0-9A-F]{2})|#.*#)", href):
                raise ValueError("href must be xsd:anyURI")
        if height:
            if height < 0:
                raise ValueError("height must be greater than or equal to 0")
        if width:
            if width < 0:
                raise ValueError("width must be greater than or equal to 0")
        ctx = kwargs.get("@context")
        self._context = merge_contexts(_context, ctx) if ctx else []
        self.type = type
        self.id = id
        self.href = href
        self.rel = rel
        self.media_type = mediaType
        self.name = name
        self.hreflang = hreflang
        self.height = height
        self.preview = preview
        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None, build_context: bool = True):
        """Outputs the current object as a dictionary.

        Args:
            _extras (Optional[dict], optional): Arguments used internally. It is not recommended that users change them.
            build_context (bool): Do we automatically build @context based on the arguments? Defaults to False.

        Returns:
            dict: Objects converted to dictionaries
        """
        if not _extras:
            _extras = self._extras.copy()
        instance_vars = vars(self).copy()

        ctx = self._context.copy()
        context = instance_vars.get("@context")

        if build_context:
            attrs = dir(self)

            ctx2 = []
            ctx2_d = {}
            if _extras.get("publicKey") or "publicKey" in attrs:
                ctx2.append("https://w3id.org/security/v1")

            # Mastodon
            if _extras.get("featured") or "featured" in attrs:
                ctx2_d["featured"] = {
                    "@id": "http://joinmastodon.org/ns#featured",
                    "@type": "@id",
                }
            if _extras.get("featuredTags") or "featuredTags" in attrs:
                ctx2_d["featuredTags"] = {
                    "@id": "http://joinmastodon.org/ns#featuredTags",
                    "@type": "@id",
                }
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if _extras.get("discoverable") or "discoverable" in attrs:
                if not ctx2_d.get("toot"):
                    ctx2_d["toot"] = "http://joinmastodon.org/ns#"
                ctx2_d["discoverable"] = "toot:discoverable"
            if (
                _extras.get("manuallyApprovesFollowers")
                or "manuallyApprovesFollowers" in attrs
            ):
                ctx2_d["manuallyApprovesFollowers"] = "as:manuallyApprovesFollowers"

            # Misskey
            if (
                _extras.get("_misskey_content")
                or _extras.get("_misskey_summary")
                or _extras.get("_misskey_quote")
                or _extras.get("_misskey_reaction")
                or _extras.get("_misskey_votes")
                or _extras.get("_misskey_talk")
                or _extras.get("isCat")
                or _extras.get("_misskey_followedMessage")
                or _extras.get("_misskey_requireSigninToViewContents")
                or _extras.get("_misskey_makeNotesFollowersOnlyBefore")
                or _extras.get("_misskey_makeNotesHiddenBefore")
                or _extras.get("_misskey_license")
            ):
                if not ctx2_d.get("misskey"):
                    ctx2_d["misskey"] = "https://misskey-hub-net/ns#"

            ctx2.append(ctx2_d)
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = ctx
        data: Dict[str, Any] = {
            "@context": context,
        }
        for key, value in instance_vars.items():
            if value is not None:
                if not key.startswith("_") and key != "content":
                    if isinstance(value, datetime.datetime.datetime):
                        data[key] = value.isoformat(timespec='microseconds').replace('+00:00', 'Z')
                    elif isinstance(value, Object):
                        data[key] = value.to_dict(_extras=value._extras)
                    elif isinstance(value, list):
                        data[key] = [
                            item.to_dict(_extras=item._extras)
                            if hasattr(item, "to_dict")
                            else item
                            for item in value
                        ]
                    elif (
                        isinstance(value, dict)
                        or isinstance(value, int)
                        or isinstance(value, bool)
                    ):
                        data[key] = value
                    else:
                        data[key] = str(value)

        _extras = _extras or {}
        for key, value in self._extras.items():
            if value is not None:
                if isinstance(value, datetime.datetime.datetime):
                    data[key] = value.isoformat(timespec='microseconds').replace('+00:00', 'Z')
                elif isinstance(value, Object):
                    data[key] = value.to_dict(_extras=value._extras)
                elif isinstance(value, list):
                    data[key] = [
                        item.to_dict(_extras=item._extras)
                        if hasattr(item, "to_dict")
                        else item
                        for item in value
                    ]
                elif (
                    isinstance(value, dict)
                    or isinstance(value, int)
                    or isinstance(value, bool)
                ):
                    data[key] = value
                else:
                    data[key] = str(value)
        return data


class Activity(Object):
    def __init__(
        self,
        type: str = "Activity",
        id: Optional[str] = None,
        actor: Optional[Union[Object, Link, str, dict]] = None,
        object: Optional[Union[Object, dict]] = None,
        target: Optional[Union[Object, Link]] = None,
        result: Optional[Union[Object, Link]] = None,
        origin: Optional[Union[Object, Link]] = None,
        instrument: Optional[Union[Object, Link]] = None,
        proof: Union[DataIntegrityProof, dict] = {},
        **kwargs,
    ):
        """Represents an Activity object in Activity Streams 2.0.

        The Activity class is used to express an action or event that occurs in a 
        social context. It encapsulates various properties that describe the 
        activity, including the actor, the object acted upon, and other related 
        entities.

        Args:
            type (str, optional): 
                The type of the object. For this class, it is always "Activity". 
                Defaults to "Activity".
            id (Optional[str], optional): 
                A unique identifier for the activity. If not provided, a UUID 
                will be generated. Defaults to None.
            actor (Optional[Union[Object, Link, str, dict]], optional): 
                The entity that is performing the activity. This can be an 
                Object, a Link, a string representing an identifier, or a 
                dictionary containing the entity's data. Defaults to None.
            object (Optional[Union[Object, dict]], optional): 
                The object that is the target of the activity. This can be an 
                Object or a dictionary. Defaults to None.
            target (Optional[Union[Object, Link]], optional): 
                The entity that the activity is directed towards. This can be 
                an Object or a Link. Defaults to None.
            result (Optional[Union[Object, Link]], optional): 
                The result of the activity. This can be an Object or a Link 
                that represents the outcome of the activity. Defaults to None.
            origin (Optional[Union[Object, Link]], optional): 
                The source of the activity, indicating where it originated. 
                This can be an Object or a Link. Defaults to None.
            instrument (Optional[Union[Object, Link]], optional): 
                The tool or means used to perform the activity. This can be 
                an Object or a Link. Defaults to None.
            proof (Union[DataIntegrityProof, dict], optional): 
                A proof of the integrity of the activity data, represented 
                as a DataIntegrityProof object or a dictionary. Defaults to 
                an empty list.
            **kwargs: 
                Additional properties that can be added to the Activity 
                object, allowing for extensibility.

        Note:
            Other values are inherited from apmodel.Object.
                
        Raises:
            ValueError: 
                If the proof is not a valid DataIntegrityProof object or 
                dictionary.

        """
        from .loader import load

        super().__init__(type="Activity", content=None)
        self.type = type
        self.id = id if id else str(uuid.uuid4())
        self.published = (
            datetime.utcnow().isoformat(timespec='microseconds').replace('+00:00', 'Z')
            if not kwargs.get("published")
            else datetime.datetime.datetime.strptime(
                kwargs.get("published"), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        )
        self.actor = load(actor) if isinstance(actor, dict) else actor
        self.object = load(object) if isinstance(object, dict) else object
        self.target = target
        self.result = result
        self.origin = origin
        self.instrument = instrument
        self.proof: Optional[DataIntegrityProof] = (load(proof) if isinstance(proof, dict) else proof) if proof != {} else None
        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

    def to_dict(self, _extras: Optional[dict] = None) -> dict:
        """Outputs the current object as a dictionary.

        Args:
            _extras (Optional[dict], optional): Arguments used internally. It is not recommended that users change them.

        Returns:
            dict: Objects converted to dictionaries
        """
        data = super().to_dict()
        data["@context"] = ["https://www.w3.org/ns/activitystreams", "https://w3id.org/security/data-integrity/v1"]

        if self.type:
            data["type"] = self.type
        if self.actor:
            data["actor"] = (
                self.actor.to_dict()
                if isinstance(self.actor, Object)
                else str(self.actor)
            )
        if self.object:
            data["object"] = (
                self.object.to_dict()
                if isinstance(self.object, Object)
                else str(self.object)
            )
        if self.target:
            data["target"] = (
                self.target.to_dict()
                if isinstance(self.target, Object)
                else str(self.target)
            )
        if self.proof:
            data["proof"] = (
                self.target.to_dict()
                if isinstance(self.proof, DataIntegrityProof)
                else self.proof
            )

        return data

from typing import Dict, List, Optional, Union

from ..cid.multikey import Multikey
from ..core import Link, Object
from ..funcs import merge_contexts
from ..security.cryptographickey import CryptographicKey
from .document import Image


class Note(Object):
    def __init__(
        self,
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
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
        inReplyTo: Optional[Union["Image", "Link", str]] = None,
        location: Optional[Union["Image", "Link"]] = None,
        preview: Optional[Union["Object", "Link"]] = None,
        published: Optional[str] = None,
        replies: Optional["Collection"] = None,
        startTime: Optional[str] = None,
        summary: Optional[str] = None,
        tag: Optional[Union["Object", "Link"]] = None,
        updated: Optional[str] = None,
        url: Optional[Union[str, "Link"]] = None,
        to: Optional[List[Union["Object", "Link", str]]] = None,
        bto: Optional[List[Union["Object", "Link", str]]] = None,
        cc: Optional[List[Union["Object", "Link", str]]] = None,
        bcc: Optional[List[Union["Object", "Link", str]]] = None,
        mediaType: Optional[str] = None,
        duration: Optional[str] = None,
        sensitive: Optional[bool] = None,
        _misskey_quote: Optional[str] = None,
        quoteUrl: Optional[str] = None,
        **kwargs,
    ):
        """Represents a Note object in Activity Streams 2.0.

        The Note class is used to convey a textual message or note in a social
        context. It inherits properties from the Object class and adds specific
        attributes that define the characteristics and metadata of the note.

        Args:
            _context (Union[str, list], optional):
                The default value for @context. It can be a string or a
                list of strings. Defaults to "https://www.w3.org/ns/activitystreams".
            id (Optional[str], optional):
                A unique identifier for the note. If not provided, it will be
                generated. Defaults to None.
            attachment (List[Union["Object", "Link", dict]], optional):
                A list of resources attached to the note, which can include
                objects, links, or dictionaries. Defaults to an empty list.
            attributedTo (Optional[Union["Object", "Link", str]], optional):
                The entity to which the note is attributed. This can be an
                Object, a Link, a string, or a dictionary. Defaults to None.
            audience (Optional[Union["Object", "Link"]], optional):
                The intended audience for the note. This can be an Object
                or a Link. Defaults to None.
            content (Optional[str], optional):
                The textual content of the note. Defaults to None.
            context (Optional[Union["Object", "Link"]], optional):
                The context of the note, which can be an Object or a Link.
                Defaults to None.
            name (Optional[str], optional):
                A human-readable name for the note. Defaults to None.
            endTime (Optional[str], optional):
                The end time of the note, represented as an ISO8601 formatted
                string. Defaults to None.
            generator (Optional[Union["Object", "Link"]], optional):
                The entity that generated the note, represented as an
                Object or a Link. Defaults to None.
            icon (Optional[Union["Image", "Link"]], optional):
                The icon associated with the note, represented as an
                Image or a Link. Defaults to None.
            image (Optional["Image"], optional):
                An image associated with the note. Defaults to None.
            inReplyTo (Optional[Union["Image", "Link"]], optional):
                The resource indicating the target of this reply, if the note
                is a response to another note. Defaults to None.
            location (Optional[Union["Image", "Link"]], optional):
                The location associated with the note, represented as an
                Image or a Link. Defaults to None.
            preview (Optional[Union["Object", "Link"]], optional):
                A resource providing a preview of the note's content, which
                can be another Object or a Link. Defaults to None.
            published (Optional[str], optional):
                The date and time when the note was published, represented
                as an ISO8601 formatted string. Defaults to None.
            replies (Optional["Collection"], optional):
                A collection of replies to the note. Defaults to None.
            startTime (Optional[str], optional):
                The start time of the note, represented as an ISO8601
                formatted string. Defaults to None.
            summary (Optional[str], optional):
                A summary of the note's content. Defaults to None.
            tag (Optional[Union["Object", "Link"]], optional):
                Tags associated with the note, represented as an Object or a Link.
                Defaults to None.
            updated (Optional[str], optional):
                The date and time when the note was last updated, represented
                as an ISO8601 formatted string. Defaults to None.
            url (Optional[Union[str, "Link"]], optional):
                The URL of the note. Defaults to None.
            to (Optional[List[Union["Object", "Link", str]]], optional):
                A list of recipients for the note, which can include Objects,
                Links, or strings. Defaults to None.
            bto (Optional[List[Union["Object", "Link", str]]], optional):
                A list of BCC recipients for the note. Defaults to None.
            cc (Optional[List[Union["Object", "Link", str]]], optional):
                A list of CC recipients for the note. Defaults to None.
            bcc (Optional[List[Union["Object", "Link", str]]], optional):
                A list of BCC recipients for the note. Defaults to None.
            mediaType (Optional[str], optional):
                The media type of the note's content, such as "text/plain".
                Defaults to None.
            duration (Optional[str], optional):
                The duration of the note's content, if applicable. Defaults to None.
            sensitive (Optional[bool], optional):
                A flag indicating whether the content of the note is sensitive.
                Defaults to None.
            _misskey_quote (Optional[str], optional):
                A specific attribute for handling quote functionality in
                Misskey. Defaults to None.
            quoteUrl (Optional[str], optional):
                A URL related to the quote functionality. Defaults to None.
            **kwargs:
                Additional properties that can be added to the Note object,
                allowing for extensibility.

        """
        kwargs["type"] = "Note"
        super().__init__(
            _context=_context,
            id=id,
            attachment=attachment,
            attributedTo=attributedTo,
            audience=audience,
            content=content,
            context=context,
            name=name,
            endTime=endTime,
            generator=generator,
            icon=icon,
            image=image,
            inReplyTo=inReplyTo,
            location=location,
            preview=preview,
            published=published,
            replies=replies,
            startTime=startTime,
            summary=summary,
            tag=tag,
            updated=updated,
            url=url,
            to=to,
            bto=bto,
            cc=cc,
            bcc=bcc,
            mediaType=mediaType,
            duration=duration,
            sensitive=sensitive,
            **kwargs,
        )
        self._misskey_quote = _misskey_quote
        self.quoteUrl = quoteUrl

    def to_dict(self, _extras: Dict | None = None, build_context: bool = True):
        """Outputs the current object as a dictionary.

        Args:
            _extras (Optional[dict], optional): Arguments used internally. It is not recommended that users change them.
            build_context (bool): Do we automatically build @context based on the arguments? Defaults to True.

        Returns:
            dict: Objects converted to dictionaries
        """
        data = super().to_dict(build_context=build_context)
        if not _extras:
            _extras = self._extras.copy()

        if self._misskey_quote:
            data["_misskey_quote"] = self._misskey_quote
        if self.quoteUrl:
            data["quoteUrl"] = self.quoteUrl

        ctx = self._context.copy()
        attrs = dir(self)

        ctx2 = ["https://www.w3.org/ns/activitystreams"]
        ctx2_d = {
            "schema": "http://schema.org#",
            "PropertyValue": "schema:PropertyValue",
            "value": "schema:value",
            "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
            "sensitive": "as:sensitive",
            "Hashtag": "as:Hashtag",
            "quoteUrl": "as:quoteUrl",
            "vcard": "http://www.w3.org/2006/vcard/ns#",
        }
        if _extras.get("publicKey") or "publicKey" in attrs:
            ctx2.append("https://w3id.org/security/v1")

        # Mastodon
        if _extras.get("featured") or "featured" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:featured"
        if _extras.get("featuredTags") or "featuredTags" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["featuredTags"] = "toot:featuredTags"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"

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

        #
        if (
            _extras.get("assertionMethod")
            or "assertionMethod" in attrs
            or _extras.get("proof")
            or "proof" in attrs
        ):
            ctx2.append("https://www.w3.org/ns/did/v1")
            ctx2.append("https://w3id.org/security/multikey/v1")
        if _extras.get("proof") or "proof" in attrs:
            ctx2.append("https://w3id.org/security/data-integrity/v1")
        ctx2.append(ctx2_d)
        context: Optional[list] = data.get("@context")
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = merge_contexts(ctx, ctx2)
        data["@context"] = context
        return data


class Profile(Object):
    def __init__(self, describes: Optional[Object | dict] = None, **kwargs):
        """Represents a Profile object in Activity Streams 2.0.

        The Profile class is used to describe an entity's profile, which
        can include additional metadata related to the entity. It is
        a type of Object that provides context about the entity it describes.

        Args:
            describes (Optional[Union[Object, dict]], optional):
                The entity that this profile describes. This can be an
                Object or a dictionary containing the entity's data.
                Defaults to None.
            **kwargs:
                Additional properties that can be added to the Profile
                object, allowing for extensibility. This can include
                common Object attributes such as `id`, `type`, `name`,
                and any other relevant attributes.

        Raises:
            ValueError:
                If the `describes` argument is provided as a value that
                cannot be processed.

        Example:
            ```
            profile = Profile(
                describes={"id": "https://example.com/user123", "name": "User 123"},
                id="https://example.com/profile123"
            )
            ```

        """
        from ..loader import load

        kwargs["type"] = "Profile"
        super().__init__(**kwargs)
        self.describes = load(describes) if isinstance(describes, dict) else describes


class Tombstone(Object):
    def __init__(self, formerType=None, deleted=None, **kwargs):
        """Represents a Tombstone object in Activity Streams 2.0.

        The Tombstone class is used to indicate that an object has been
        deleted or is no longer accessible. It provides metadata about
        the former state of the object, including its previous type
        and the time of deletion.

        Args:
            formerType (Optional[str], optional):
                The type of the object that has been deleted. This can be
                a string representing the former type (e.g., "Note", "Activity").
                Defaults to None.
            deleted (Optional[str], optional):
                The date and time when the object was deleted, represented
                as an ISO8601 formatted string (e.g., "2023-10-05T14:48:00Z").
                Defaults to None.
            **kwargs:
                Additional properties that can be added to the Tombstone
                object, allowing for extensibility. This can include
                common Object attributes such as `id`, `name`, `icon`,
                and any other relevant attributes.

        Example:
            ```
            tombstone = Tombstone(
                formerType="Note",
                deleted="2023-10-05T14:48:00Z",
                id="https://example.com/tombstone/123"
            )
            ```

        """
        kwargs["type"] = "Tombstone"
        super().__init__(**kwargs)
        self.deleted = deleted
        self.formerType = formerType


class Collection(Object):
    def __init__(
        self, items=None, totalItems=None, first=None, last=None, current=None, **kwargs
    ):
        """Represents a Collection object in Activity Streams 2.0.

        The Collection class is used to represent a grouping of objects
        or links, along with metadata that describes the collection,
        including the total number of items and pagination information.

        Args:
            items (Optional[List[Union[Object, Link]]], optional):
                A list of objects or links that belong to this collection.
                Each item can be an Object or a Link. Defaults to None.
            totalItems (Optional[int], optional):
                The total number of items in the collection, which may
                be greater than the number of items returned in this
                instance. Defaults to None.
            first (Optional[Union[Object, Link]], optional):
                A reference to the first item in the collection. This can
                be an Object or a Link. Defaults to None.
            last (Optional[Union[Object, Link]], optional):
                A reference to the last item in the collection. This can
                be an Object or a Link. Defaults to None.
            current (Optional[Union[Object, Link]], optional):
                A reference to the current item in the collection, which
                may represent the item being viewed. This can be an
                Object or a Link. Defaults to None.
            **kwargs:
                Additional properties that can be added to the Collection
                object, allowing for extensibility. This can include
                common Object attributes such as `id`, `name`, `type`,
                and any other relevant attributes.

        Example:
            ```
            collection = Collection(
                items=[{"id": "https://example.com/item1"}, {"id": "https://example.com/item2"}],
                totalItems=100,
                first={"id": "https://example.com/item1"},
                last={"id": "https://example.com/item100"},
                current={"id": "https://example.com/item10"},
                id="https://example.com/collection"
            )
            ```

        """
        kwargs["type"] = "Collection"
        super().__init__(**kwargs)
        self.items = items
        self.totalItems = totalItems
        self.first = first
        self.last = last
        self.current = current


class Actor(Object):
    def __init__(
        self,
        type: str,
        preferredUsername: str,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        _context: Union[str, list] = "https://www.w3.org/ns/activitystreams",
        **kwargs,
    ):
        """Represents an Actor object in Activity Streams 2.0.

        The Actor class is used to define an entity that performs actions
        in the context of Activity Streams. This can represent users,
        applications, or other entities that can act within the network.

        Args:
            type (str):
                The type of the actor, indicating the kind of entity it represents
                (e.g., "Person", "Application").
            preferredUsername (str):
                The preferred username for the actor, used to identify the
                actor in a human-readable form.
            name (Optional[str], optional):
                The display name of the actor. Defaults to None.
            url (Optional[str], optional):
                A URL that points to the actor's profile or homepage. Defaults to None.
            inbox (Optional[str], optional):
                The URL of the actor's inbox, where activities can be sent.
                Defaults to None.
            outbox (Optional[str], optional):
                The URL of the actor's outbox, where activities are stored.
                Defaults to None.
            sharedInbox (Optional[str], optional):
                A URL for a shared inbox that can be used for group activities.
                Defaults to None.
            publicKey (Optional[dict], optional):
                A public key for the actor, which can be used for cryptographic
                operations. Defaults to None.
            discoverable (Optional[bool], optional):
                A flag indicating whether the actor is discoverable by other
                entities. Defaults to None.
            suspended (Optional[bool], optional):
                A flag indicating whether the actor is suspended or inactive.
                Defaults to None.
            assertionMethod (Optional[List[Union["Multikey", dict]]], optional):
                A list of assertion methods that can be used to verify the
                actor's identity. Defaults to an empty list.
            _context (Union[str, list], optional):
                The context for the actor, which can be a string or a list
                of strings. Defaults to "https://www.w3.org/ns/activitystreams".
            **kwargs:
                Additional properties that can be added to the Actor object,
                allowing for extensibility. This can include common Object
                attributes such as `id`, `type`, `icon`, and any other
                relevant attributes.

        Example:
            ```
            actor = Actor(
                type="Person",
                preferredUsername="user123",
                name="User 123",
                url="https://example.com/user123",
                inbox="https://example.com/user123/inbox",
                outbox="https://example.com/user123/outbox",
                publicKey={"id": "https://example.com/user123#key", "publicKeyPem": "-----BEGIN PUBLIC KEY-----..."},
                discoverable=True,
                suspended=False,
                assertionMethod=[{"id": "https://example.com/user123#key", "type": "Multikey"}],
                id="https://example.com/user123"
            )
            ```

        """
        from ..loader import load

        super().__init__(type=type, **kwargs)
        ctx = kwargs.get("@context")
        self._context = merge_contexts(_context, ctx) if ctx else []
        self.preferredUsername = preferredUsername
        self.name = name
        self.url = url
        self.inbox = inbox if inbox else None
        self.outbox = outbox if outbox else None
        self.sharedInbox = sharedInbox if sharedInbox else None

        # extensional types
        self.publicKey: CryptographicKey = (
            load(publicKey) if isinstance(publicKey, dict) else publicKey
        )  # type: ignore
        self.discoverable = discoverable
        self.suspended = suspended

        # cid
        self.assertionMethod = assertionMethod

        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None):
        """Outputs the current object as a dictionary.

        Args:
            _extras (Optional[dict], optional): Arguments used internally. It is not recommended that users change them.

        Returns:
            dict: Objects converted to dictionaries
        """
        data = super().to_dict()
        if not _extras:
            _extras = self._extras.copy()

        if self.preferredUsername:
            data["preferredUsername"] = self.preferredUsername
        if self.name:
            data["name"] = self.name
        if self.url:
            data["url"] = self.url
        if self.inbox:
            data["inbox"] = self.inbox
        if self.outbox:
            data["outbox"] = self.outbox
        if self.sharedInbox:
            data["sharedInbox"] = self.sharedInbox
        m = []
        if self.assertionMethod:
            for method in self.assertionMethod:
                if isinstance(method, Multikey):
                    m.append(method.dump_json())
        if self.publicKey:
            if isinstance(self.publicKey, CryptographicKey):
                data["publicKey"] = self.publicKey.to_dict()

        data["assertionMethod"] = m

        ctx = self._context.copy()
        attrs = dir(self)

        ctx2 = ["https://www.w3.org/ns/activitystreams"]
        ctx2_d = {
            "schema": "http://schema.org#",
            "PropertyValue": "schema:PropertyValue",
            "value": "schema:value",
            "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
            "sensitive": "as:sensitive",
            "Hashtag": "as:Hashtag",
            "quoteUrl": "as:quoteUrl",
            "vcard": "http://www.w3.org/2006/vcard/ns#",
        }
        if _extras.get("publicKey") or "publicKey" in attrs:
            ctx2.append("https://w3id.org/security/v1")

        # Mastodon
        if _extras.get("featured") or "featured" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:featured"
        if _extras.get("featuredTags") or "featuredTags" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["featuredTags"] = "toot:featuredTags"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"
        if _extras.get("discoverable") or "discoverable" in attrs:
            if not ctx2_d.get("toot"):
                ctx2_d["toot"] = "http://joinmastodon.org/ns#"
            ctx2_d["discoverable"] = "toot:discoverable"

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

        #
        if (
            _extras.get("assertionMethod")
            or "assertionMethod" in attrs
            or _extras.get("proof")
            or "proof" in attrs
        ):
            ctx2.append("https://www.w3.org/ns/did/v1")
            ctx2.append("https://w3id.org/security/multikey/v1")
        if _extras.get("proof") or "proof" in attrs:
            ctx2.append("https://w3id.org/security/data-integrity/v1")
        context: Optional[list] = data.get("@context")
        if context:
            context = merge_contexts(merge_contexts(ctx, context), ctx2)
        else:
            context = merge_contexts(ctx, ctx2)
        data["@context"] = context

        return data


class Person(Actor):
    def __init__(
        self,
        name=None,
        url=None,
        inbox=None,
        outbox=None,
        sharedInbox=None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: list[Union[Multikey, dict]] = [],
        **kwargs,
    ):
        """Represents a Person object in Activity Streams 2.0.

        The Person class is a specific type of Actor that represents
        an individual user in the Activity Streams framework. It inherits
        attributes from the Actor class while specializing its type to
        "Person".

        Args:
            name (Optional[str], optional):
                The display name of the person. Defaults to None.
            url (Optional[str], optional):
                A URL that points to the person's profile or homepage.
                Defaults to None.
            inbox (Optional[str], optional):
                The URL of the person's inbox, where activities can be sent.
                Defaults to None.
            outbox (Optional[str], optional):
                The URL of the person's outbox, where activities are stored.
                Defaults to None.
            sharedInbox (Optional[str], optional):
                A URL for a shared inbox that can be used for group activities.
                Defaults to None.
            publicKey (Optional[dict], optional):
                A public key for the person, which can be used for cryptographic
                operations. Defaults to None.
            discoverable (Optional[bool], optional):
                A flag indicating whether the person is discoverable by other
                entities. Defaults to None.
            suspended (Optional[bool], optional):
                A flag indicating whether the person is suspended or inactive.
                Defaults to None.
            assertionMethod (Optional[List[Union["Multikey", dict]]], optional):
                A list of assertion methods that can be used to verify the
                person's identity. Defaults to an empty list.
            **kwargs:
                Additional properties that can be added to the Person object,
                allowing for extensibility. This can include common Object
                attributes such as `id`, `icon`, and any other relevant attributes.

        Example:
            ```
            person = Person(
                name="John Doe",
                url="https://example.com/johndoe",
                inbox="https://example.com/johndoe/inbox",
                outbox="https://example.com/johndoe/outbox",
                publicKey={"id": "https://example.com/johndoe#key", "publicKeyPem": "-----BEGIN PUBLIC KEY-----..."},
                discoverable=True,
                suspended=False,
                assertionMethod=[{"id": "https://example.com/johndoe#key", "type": "Multikey"}],
                id="https://example.com/johndoe"
            )
            ```

        """
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Person",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Group(Actor):
    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        inbox: Optional[str] = None,
        outbox: Optional[str] = None,
        sharedInbox: Optional[str] = None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: Optional[List[Union["Multikey", dict]]] = [],
        **kwargs,
    ):
        """Represents a Group object in Activity Streams 2.0.

        The Group class is a specific type of Actor that represents
        a collective entity, such as a community or organization group.
        It inherits attributes from the Actor class while specializing
        its type to "Group".

        Args:
            name (Optional[str], optional):
                The display name of the group. Defaults to None.
            url (Optional[str], optional):
                A URL that points to the group's profile or homepage.
                Defaults to None.
            inbox (Optional[str], optional):
                The URL of the group's inbox, where activities can be sent.
                Defaults to None.
            outbox (Optional[str], optional):
                The URL of the group's outbox, where activities are stored.
                Defaults to None.
            sharedInbox (Optional[str], optional):
                A URL for a shared inbox that can be used for group activities.
                Defaults to None.
            publicKey (Optional[dict], optional):
                A public key for the group, which can be used for cryptographic
                operations. Defaults to None.
            discoverable (Optional[bool], optional):
                A flag indicating whether the group is discoverable by other
                entities. Defaults to None.
            suspended (Optional[bool], optional):
                A flag indicating whether the group is suspended or inactive.
                Defaults to None.
            assertionMethod (Optional[List[Union["Multikey", dict]]], optional):
                A list of assertion methods that can be used to verify the
                group's identity. Defaults to an empty list.
            **kwargs:
                Additional properties that can be added to the Group object,
                allowing for extensibility. This can include common Object
                attributes such as `id`, `icon`, and any other relevant attributes.

        Example:
            ```
            group = Group(
                name="Example Group",
                url="https://example.com/group",
                inbox="https://example.com/group/inbox",
                outbox="https://example.com/group/outbox",
                publicKey={"id": "https://example.com/group#key", "publicKeyPem": "-----BEGIN PUBLIC KEY-----..."},
                discoverable=True,
                suspended=False,
                assertionMethod=[{"id": "https://example.com/group#key", "type": "Multikey"}],
                id="https://example.com/group"
            )
            ```

        """
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Group",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Application(Actor):
    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        inbox: Optional[str] = None,
        outbox: Optional[str] = None,
        sharedInbox: Optional[str] = None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: Optional[List[Union["Multikey", dict]]] = [],
        **kwargs,
    ):
        """Represents an Application object in Activity Streams 2.0.

        The Application class is a specific type of Actor that represents
        a software application or service interacting with the Activity Streams
        framework. It inherits attributes from the Actor class while specializing
        its type to "Application".

        Args:
            name (Optional[str], optional):
                The display name of the application. Defaults to None.
            url (Optional[str], optional):
                A URL that points to the application's profile or homepage.
                Defaults to None.
            inbox (Optional[str], optional):
                The URL of the application's inbox, where activities can be sent.
                Defaults to None.
            outbox (Optional[str], optional):
                The URL of the application's outbox, where activities are stored.
                Defaults to None.
            sharedInbox (Optional[str], optional):
                A URL for a shared inbox that can be used for group activities.
                Defaults to None.
            publicKey (Optional[dict], optional):
                A public key for the application, which can be used for cryptographic
                operations. Defaults to None.
            discoverable (Optional[bool], optional):
                A flag indicating whether the application is discoverable by other
                entities. Defaults to None.
            suspended (Optional[bool], optional):
                A flag indicating whether the application is suspended or inactive.
                Defaults to None.
            assertionMethod (Optional[List[Union["Multikey", dict]]], optional):
                A list of assertion methods that can be used to verify the
                application's identity. Defaults to an empty list.
            **kwargs:
                Additional properties that can be added to the Application object,
                allowing for extensibility. This can include common Object
                attributes such as `id`, `icon`, and any other relevant attributes.

        Example:
            ```
            application = Application(
                name="Example App",
                url="https://example.com/app",
                inbox="https://example.com/app/inbox",
                outbox="https://example.com/app/outbox",
                publicKey={"id": "https://example.com/app#key", "publicKeyPem": "-----BEGIN PUBLIC KEY-----..."},
                discoverable=True,
                suspended=False,
                assertionMethod=[{"id": "https://example.com/app#key", "type": "Multikey"}],
                id="https://example.com/app"
            )
            ```

        """
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Application",
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )


class Service(Actor):
    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        inbox: Optional[str] = None,
        outbox: Optional[str] = None,
        sharedInbox: Optional[str] = None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: Optional[List[Union["Multikey", dict]]] = [],
        **kwargs,
    ):
        """Represents a Service object in Activity Streams 2.0.

        The Service class is a specific type of Actor that represents
        a service or backend application that interacts with the Activity
        Streams framework. It inherits attributes from the Actor class while
        specializing its type to "Service".

        Args:
            name (Optional[str], optional):
                The display name of the service. Defaults to None.
            url (Optional[str], optional):
                A URL that points to the service's profile or homepage.
                Defaults to None.
            inbox (Optional[str], optional):
                The URL of the service's inbox, where activities can be sent.
                Defaults to None.
            outbox (Optional[str], optional):
                The URL of the service's outbox, where activities are stored.
                Defaults to None.
            sharedInbox (Optional[str], optional):
                A URL for a shared inbox that can be used for group activities.
                Defaults to None.
            publicKey (Optional[dict], optional):
                A public key for the service, which can be used for cryptographic
                operations. Defaults to None.
            discoverable (Optional[bool], optional):
                A flag indicating whether the service is discoverable by other
                entities. Defaults to None.
            suspended (Optional[bool], optional):
                A flag indicating whether the service is suspended or inactive.
                Defaults to None.
            assertionMethod (Optional[List[Union["Multikey", dict]]], optional):
                A list of assertion methods that can be used to verify the
                service's identity. Defaults to an empty list.
            **kwargs:
                Additional properties that can be added to the Service object,
                allowing for extensibility. This can include common Object
                attributes such as `id`, `icon`, and any other relevant attributes.

        Example:
            ```
            service = Service(
                name="Example Service",
                url="https://example.com/service",
                inbox="https://example.com/service/inbox",
                outbox="https://example.com/service/outbox",
                publicKey={"id": "https://example.com/service#key", "publicKeyPem": "-----BEGIN PUBLIC KEY-----..."},
                discoverable=True,
                suspended=False,
                assertionMethod=[{"id": "https://example.com/service#key", "type": "Multikey"}],
                id="https://example.com/service"
            )
            ```

        """
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Service",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )

class Organization(Actor):
    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        inbox: Optional[str] = None,
        outbox: Optional[str] = None,
        sharedInbox: Optional[str] = None,
        publicKey: Optional[dict] = None,
        discoverable: Optional[bool] = None,
        suspended: Optional[bool] = None,
        assertionMethod: Optional[List[Union["Multikey", dict]]] = [],
        **kwargs,
    ):
        """Represents an Organization object in Activity Streams 2.0.

        The Organization class is a specific type of Actor that represents 
        a corporate or organizational entity within the Activity Streams 
        framework. It inherits attributes from the Actor class while 
        specializing its type to "Organization".

        Args:
            name (Optional[str], optional): 
                The display name of the organization. Defaults to None.
            url (Optional[str], optional): 
                A URL that points to the organization's profile or homepage. 
                Defaults to None.
            inbox (Optional[str], optional): 
                The URL of the organization's inbox, where activities can be sent. 
                Defaults to None.
            outbox (Optional[str], optional): 
                The URL of the organization's outbox, where activities are stored. 
                Defaults to None.
            sharedInbox (Optional[str], optional): 
                A URL for a shared inbox that can be used for group activities. 
                Defaults to None.
            publicKey (Optional[dict], optional): 
                A public key for the organization, which can be used for cryptographic 
                operations. Defaults to None.
            discoverable (Optional[bool], optional): 
                A flag indicating whether the organization is discoverable by other 
                entities. Defaults to None.
            suspended (Optional[bool], optional): 
                A flag indicating whether the organization is suspended or inactive. 
                Defaults to None.
            assertionMethod (Optional[List[Union["Multikey", dict]]], optional): 
                A list of assertion methods that can be used to verify the 
                organization's identity. Defaults to an empty list.
            **kwargs: 
                Additional properties that can be added to the Organization object, 
                allowing for extensibility. This can include common Object 
                attributes such as `id`, `icon`, and any other relevant attributes.

        Example:
            ```
            organization = Organization(
                name="Example Organization",
                url="https://example.com/org",
                inbox="https://example.com/org/inbox",
                outbox="https://example.com/org/outbox",
                publicKey={"id": "https://example.com/org#key", "publicKeyPem": "-----BEGIN PUBLIC KEY-----..."},
                discoverable=True,
                suspended=False,
                assertionMethod=[{"id": "https://example.com/org#key", "type": "Multikey"}],
                id="https://example.com/org"
            )
            ```

        """
        kwargs.pop("type") if kwargs.get("type") else None
        super().__init__(
            type="Organization",
            name=name,
            url=url,
            inbox=inbox,
            outbox=outbox,
            sharedInbox=sharedInbox,
            publicKey=publicKey,
            discoverable=discoverable,
            suspended=suspended,
            assertionMethod=assertionMethod,
            **kwargs,
        )

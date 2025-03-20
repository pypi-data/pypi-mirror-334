from ..core import Activity, Object, Link

from ..funcs import _make_accept, _make_reject

class Accept(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Accept", **kwargs)

class Reject(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Reject", **kwargs)

class TentativeReject(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("TentativeReject", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Remove(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Remove", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Undo(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Undo", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Create(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Create", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Delete(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Delete", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Update(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Update", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Follow(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Follow", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class View(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("View", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Listen(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Listen", **kwargs)


class Read(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Read", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Move(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Move", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Travel(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Travel", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Announce(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Announce", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Block(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Block", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Flag(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Flag", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)
    
class Like(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Like", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)
    
class Dislike(Activity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Dislike", **kwargs)

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)
    
class IntransitiveActivity(Activity):
    def __init__(
        self,
        type=None,
        actor=None,
        target=None,
        result=None,
        origin=None,
        instrument=None,
        **kwargs,
    ):
        super().__init__(
            "IntransitiveActivity" if not type else type, actor, target, result, origin, instrument, **kwargs
        )

    def accept(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_accept(obj, actor)

    def reject(self, actor: Object | Link | str):
        obj = self.to_dict(self._extras)
        return _make_reject(obj, actor)

class Question(IntransitiveActivity):
    def __init__(self, **kwargs):
        if kwargs.get("type"):
            kwargs.pop("type")
        super().__init__("Question", **kwargs)
# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.dispatch import Signal
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

DIRTY_MARK = object()


class TimeTrackable(models.Model):
    """Based on:

    https://github.com/ambv/kitdjango/blob/ba115ce2462b31cf78702faa045285ce78ff138f/src/lck/django/common/models.py
    In our version cache_version was removed.

    Describes an abstract model whose lifecycle is tracked by time. Includes
    a ``created`` field that is set automatically upon object creation,
    a ``modified`` field that is updated automatically upon calling ``save()``
    on the object whenever a **significant** change was done.

    By a **significant** change we mean any change outside of those internal
    ``created``, ``modified`` fields.
    """

    insignificant_fields = set(['modified', 'created'])

    created = models.DateTimeField(verbose_name=_("date created"),
                                   default=now)
    modified = models.DateTimeField(verbose_name=_("last modified"),
                                    default=now)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(TimeTrackable, self).__init__(*args, **kwargs)
        self._update_field_state()

    def save(self, update_modified=True, *args, **kwargs):
        """Overrides save(). Adds the ``update_modified=True`` argument.
        If False, the ``modified`` field won't be updated even if there were
        **significant** changes to the model."""
        if self.significant_fields_updated:
            if update_modified:
                self.modified = now()
        super(TimeTrackable, self).save(*args, **kwargs)
        self._update_field_state()

    def _update_field_state(self):
        self._field_state = self._fields_as_dict()

    def _fields_as_dict(self):
        fields = []
        for f in self._meta.fields:
            _name = f.name
            fields.append((_name, getattr(self, _name)))
        return dict(fields)

    @property
    def significant_fields_updated(self):
        """Returns True on significant changes to the model.

        By a **significant** change we mean any change outside of those internal
         Full list of ignored fields lies in ``TimeTrackable.insignificant_fields``."""
        return bool(set(self.dirty_fields.keys()) - self.insignificant_fields)

    @property
    def dirty_fields(self):
        """dirty_fields() -> {'field1': 'old_value1', 'field2': 'old_value2', ...}

        Returns a dictionary of attributes that have changed on this object
        and are not yet saved. The values are original values present in the
        database at the moment of this object's creation/read/last save."""
        new_state = self._fields_as_dict()
        diff = []
        for k, v in self._field_state.items():
            try:
                if v == new_state.get(k):
                    continue
            except (TypeError, ValueError):
                pass  # offset-naive and offset-aware datetimes, etc.
            if v is DIRTY_MARK:
                v = new_state.get(k)
            diff.append((k, v))
        return dict(diff)

    def mark_dirty(self, *fields):
        """Forces `fields` to be marked as dirty to make all machinery checking
        for dirty fields treat them accordingly."""
        _dirty_fields = self.dirty_fields
        for field in fields:
            if field in _dirty_fields:
                continue
            self._field_state[field] = DIRTY_MARK

    def mark_clean(self, *fields, **kwargs):
        """Removes the forced dirty marks from fields.

        Fields that would be considered dirty anyway stay that way, unless
        `force` is set to True. In that case a field is unmarked until another
        change on it happens."""
        force = kwargs.get('force', False)
        _dirty_fields = self.dirty_fields
        _current_state = self._fields_as_dict()
        for field in fields:
            if field not in _dirty_fields:
                continue
            if self._field_state[field] is DIRTY_MARK:
                self._field_state[field] = _dirty_fields[field]
            elif force:
                self._field_state[field] = _current_state[field]

from copy import deepcopy

import pytest
from kumoapi.typing import Dtype, Stype

from kumoai.graph import Column


def test_create():
    r"""Test basic column creation."""
    c = Column(name='test', stype=Stype.numerical, dtype=Dtype.int32)
    d = Column('test', 'numerical', 'int32')

    assert c.stype == Stype.numerical
    assert c.dtype == Dtype.int32

    assert str(c) == ('Column(name="test", stype="numerical", dtype="int32")')
    assert str(d) == str(c)
    assert c == d

    e = deepcopy(c)
    e.timestamp_format = 'yyyy-MM-dd'
    assert str(e) == ('Column(name="test", stype="numerical", dtype="int32", '
                      'timestamp_format="yyyy-MM-dd")')


def test_update():
    r"""Test column update behaves as expected."""
    c = Column(name='test', stype=Stype.numerical, dtype=Dtype.int32)
    c2 = Column(name='test', stype=Stype.categorical, dtype=Dtype.int32)

    assert c == c
    assert c != c2
    assert c.update(c2) == c
    assert c.update(c2, override=True) == c2


def test_readonly_name():
    r"""Test that column name cannot be modified after create."""
    c = Column(name='test', stype=Stype.numerical, dtype=Dtype.int32)
    with pytest.raises(AttributeError):
        c.name = 'test2'

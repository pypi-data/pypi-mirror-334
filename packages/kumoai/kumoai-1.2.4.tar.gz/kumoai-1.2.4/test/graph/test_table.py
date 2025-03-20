from dataclasses import dataclass

from kumoapi.typing import Dtype, Stype

from kumoai.connector.source_table import SourceTable
from kumoai.graph import Table


@dataclass
class MockConnector:
    r"""Simple mock for a connector."""
    name: str = 'test'


def test_table_basic():
    r"""Test basic table creation flow."""
    source_table = SourceTable('mock_source_table', MockConnector())
    table = Table(
        source_table=source_table,
        columns=[('a', Stype.numerical, Dtype.int), 'b'],
        primary_key=('primary_key', Stype.ID, Dtype.int),
        time_column='a',
    )

    assert str(table) == ('Table(\n'
                          '  source_name=mock_source_table,\n'
                          '  data_source=test,\n'
                          '  columns=[a, b, primary_key],\n'
                          '  primary_key=primary_key,\n'
                          '  time_column=a,\n'
                          '  end_time_column=None,\n'
                          ')')

    assert table.has_primary_key()
    assert table.has_time_column()
    assert not table.has_end_time_column()

    assert table.primary_key.dtype == Dtype.int
    assert table.time_column.dtype == Dtype.int
    assert table.column('b').dtype is None

    table.time_column = None
    assert not table.has_time_column()
    assert table.has_column('b')
    table.remove_column('b')
    assert not table.has_column('b')

    metadata = table.metadata
    assert metadata.shape == (2, 6)
    assert metadata['is_primary_key'].sum() == 1
    assert metadata['is_end_time_column'].sum() == 0
    assert set(metadata['name'].to_list()) == {'a', 'primary_key'}

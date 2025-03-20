from dataclasses import dataclass

import pytest
from kumoapi.typing import Dtype, Stype

from kumoai.connector import S3Connector, SourceTable
from kumoai.graph import Edge, Graph, Table


@dataclass
class MockConnector:
    r"""Simple mock for a connector."""
    name: str = 'test'


def test_graph_basic():
    r"""Test basic graph creation flow."""
    # Setup:
    source_a = SourceTable('a', MockConnector())
    source_b = SourceTable('b', MockConnector())
    source_c = SourceTable('c', MockConnector())

    table_a = Table(
        source_table=source_a,
        columns=[('c1', Stype.numerical, Dtype.int), 'c2'],
        primary_key=('c1', Stype.ID, Dtype.int),
        time_column='c2',
    )
    table_b = Table(
        source_table=source_b,
        columns=[('c1', Stype.text, Dtype.string), 'c2', 'c3'],
        time_column='c2',
        end_time_column='c3',
    )
    table_c = Table(
        source_table=source_c,
        columns=[('c1', Stype.text, Dtype.string),
                 ('c2', Stype.numerical, Dtype.int), 'c3'],
    )

    # Creation:
    graph = Graph({'a': table_a, 'b': table_b, 'c': table_c})

    # Indexing:
    assert isinstance(graph['a'], Table)
    with pytest.raises(KeyError):
        _ = graph['d']

    # Contains:
    assert 'a' in graph
    assert 'd' not in graph

    # Edges:
    graph.link('b', 'c2', 'a')
    with pytest.raises(ValueError):
        graph.link(None)
    with pytest.raises(ValueError):
        graph.link('b', 'c2', 'a')
    with pytest.raises(ValueError):
        graph.link(Edge('b', 'c2', 'a'))

    assert str(graph) == (
        "Graph(\n"
        "  tables=[a, b, c],\n"
        "  edges=[Edge(src_table='b', fkey='c2', dst_table='a')],\n"
        ")")


@pytest.fixture(scope="class")
def integ_connector(setup_integration_client):
    yield S3Connector()


def test_graph_persistence(integ_connector):
    # TODO(manan): test on financial, like Snowflake...
    base_path = ("s3://kumo-public-datasets/Kumo-Experience-Bug-Bash-Datasets/"
                 "flight-delays/parquet/")
    airlines_path = base_path + "airlines"

    # TODO(manan): test is not idempotent. Fix by adding a finalizer for
    # cleanup
    airlines = Table(
        integ_connector[airlines_path],
        columns=['IATA_CODE', 'AIRLINE'],
        primary_key='IATA_CODE',
    )
    airlines['IATA_CODE'].stype = Stype.ID
    airlines['IATA_CODE'].dtype = Dtype.string
    airlines['AIRLINE'].stype = Stype.text
    airlines['AIRLINE'].dtype = Dtype.string

    graph = Graph({'airlines': airlines})
    graph.save()

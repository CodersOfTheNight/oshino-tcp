from pytest import fixture

from oshino_tcp import dynamic_load
from oshino_tcp.agent import print_out


def test_dyn_load():
    fn = dynamic_load("oshino_tcp.agent.print_out")
    assert fn == print_out

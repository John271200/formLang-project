from apps.mtu.machines import ADD
from formlang.utm import UniversalTM, encode, decode


def test_round_trip_encodage():
    assert decode(encode(ADD)).run("11+1").tape.count("1") == 3


def test_utm_simule_comme_la_machine():
    desc = encode(ADD)
    res_direct = ADD.run("111+11")
    res_utm = UniversalTM().run(desc, "111+11")
    assert res_utm.tape == res_direct.tape
    assert res_utm.accepted == res_direct.accepted


def test_trace_disponible():
    res = ADD.run("1+1", trace=True)
    assert res.trace and res.trace[0][1] == "q0"


def test_interpreteur_universel():
    from apps.mtu.interpreter import UniversalInterpreter, addition_via_utm, soustraction_via_utm
    interp = UniversalInterpreter()
    r = interp.run(ADD, "111+11")
    assert r.tape.count("1") == 5
    assert addition_via_utm(3, 2) == 5
    assert soustraction_via_utm(5, 2) == 3

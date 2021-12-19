from day17 import *

def test_targeting():
    target = Target(((20, 30), (-10,-5)))
    ic = InitialConditions(7,2)
    sim = Simulation(target, ic)
    sim.simulate()
    assert sim.in_target == True
    assert sim.step_count == 7

    ic = InitialConditions(6,3)
    sim = Simulation(target, ic)
    sim.simulate()
    assert sim.in_target == True
    assert sim.step_count == 9

    ic = InitialConditions(9,0)
    sim = Simulation(target, ic)
    sim.simulate()
    assert sim.in_target == True
    assert sim.step_count == 4

    ic = InitialConditions(17,-4)
    sim = Simulation(target, ic)
    sim.simulate()
    assert sim.in_target == False
    assert sim.step_count == 3

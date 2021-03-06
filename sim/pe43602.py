from migen.flow.network import *
from migen.flow.transactions import *
from migen.actorlib.sim import *
from migen.sim.generic import Simulator, TopLevel

from library.rf_drivers import *

class DataGen(SimActor):
	def __init__(self):
		self.attn = Source([("attn", 6)])
		def data_gen():
			yield Token("attn", {"attn": 0b101001})
			for i in range(6):
				yield Token("attn", {"attn": 1 << i})
		SimActor.__init__(self, data_gen())

class PE43602:
	def __init__(self):
		self.d = Signal()
		self.clk = Signal()
		self.le = Signal()

def main():
	g = DataFlowGraph()
	g.add_connection(DataGen(), PE43602Driver(PE43602()))
	c = CompositeActor(g)
	
	def end_simulation(s):
		s.interrupt = s.cycle_counter > 5 and not s.rd(c.busy)
	f = c.get_fragment() + Fragment(sim=[end_simulation])
	sim = Simulator(f, TopLevel(vcd_name="pe43602.vcd"))
	sim.run()

main()

from migen.fhdl.std import *
from migen.genlib.cdc import MultiReg
from migen.bank.description import *
from migen.genlib.fsm import FSM,NextState

class GPIOIn(Module, AutoCSR):
	def __init__(self, signal):
		self._r_in = CSRStatus(flen(signal))
		self.specials += MultiReg(signal, self._r_in.status)

class GPIOOut(Module, AutoCSR):
	def __init__(self, signal):
		self._r_out = CSRStorage(flen(signal), reset=3)
		self.comb += signal.eq(self._r_out.storage)

class Blinker(Module):
	def __init__(self, signal, divbits=26):
		counter = Signal(divbits)
		self.comb += signal.eq(counter[divbits-1])
		self.sync += counter.eq(counter + 1)

class Pattern(Module,AutoCSR):
	def __init__(self, signal, pattern, divbits=25):
		counter = Signal(divbits)
		states = ["P{0}".format(s) for s in range(len(pattern))]
		self.submodules.fsm = FSM()

		self.sync += counter.eq(counter + 1)

		#set up state machine
		for i in range(len(pattern)-1):
			self.fsm.act(states[i],
						signal.eq(pattern[i]),
						If(counter == 0,
							NextState(states[i+1])
						)
			)

		#final state returns to first state
		self.fsm.act(states[-1],
					signal.eq(pattern[-1]),
					If(counter == 0,
						NextState(states[0])
					)
		)


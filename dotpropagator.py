
from collections import defaultdict

class DotPropagator:
    """A non-literal *dot* propagator"""

    def __init__(self, dotfiledesc:str):
        self.__dotfiledesc = dotfiledesc
        self.__stack = ['Start']
        self.__step = 0
        self.__stable_nodes = set()  # all checked nodes in the graph
        self.write_header()

    def init(self, init):
        self.__symbols = defaultdict(set)
        # print('INIT:', {atom.symbol: init.solver_literal(atom.literal) for atom in init.symbolic_atoms})
        for atom in init.symbolic_atoms:
            lit = init.solver_literal(atom.literal)
            self.__symbols[lit].add(atom)
            init.add_watch(lit)

    def propagate(self, ctl, changes):
        level = ctl.assignment.decision_level
        # print('PROPAGATE:', changes)
        self.__step += 1
        for lit in changes:
            self.write('\t{} -> {} [label="{}"];'.format(self.last_node, lit, self.__step))
            self.push_node(lit)

    def undo(self, solver_id, assign, undo):
        # print('UNDO:', undo)
        while undo:
            prev_node = self.pull_node()
            assert prev_node in undo
            self.write('\t{} -> {} [style=dotted label={}];'.format(prev_node, self.last_node, self.__step))
            undo.remove(prev_node)

    def check(self, ctl):
        self.__stable_nodes.add(self.last_node)


    def pull_node(self):
        *self.__stack, ret = self.__stack
        return ret
    def push_node(self, uid):
        self.__stack.append(uid)

    @property
    def last_node(self):
        return self.__stack[-1]

    def write(self, line):
        self.__dotfiledesc.write(line.rstrip() + '\n')

    def write_nodes(self):
        for uid, atoms in self.__symbols.items():
            self.write('\t{} [label="{}"{}];'.format(
                uid, ' '.join(str(atom.symbol) for atom in atoms),
                ' fillcolor="green"' if uid in self.__stable_nodes else ''
            ))
    def write_header(self):
        self.write('digraph solving {')
        self.write('\tnode [style=filled];')
    def finalize(self):
        self.write_nodes()
        self.write('}')


def main(prg):
    with open('out/out.dot', 'w') as fd:
        propagator = DotPropagator(fd)
        prg.register_propagator(propagator)
        prg.ground([("base", [])])
        prg.solve()
        propagator.finalize()

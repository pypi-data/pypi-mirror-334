import sys, os
import time
import sympy
# project root path
sys.path.append(os.path.dirname(__file__)+"/../src/")
import symcirc
from symcirc import utils
import test_utils

if __name__ == '__main__':
    plots = False
    test_prints = True
    parser_test = False
    analysis_test = True
    #netlist = symcirc.utils.load_file("netlists\\symbulator\\NR11_13_7_tran.txt")
    netlist = symcirc.utils.load_file("netlists\\geec_355.txt")
    #netlist = symcirc.utils.load_file("netlists\\AC1.txt")
    #netlist = symcirc.utils.load_file("netlists\\DC_elem_10.txt")

    method = "two_graph_node"
    method = "tableau"
    #method = "eliminated_tableau"


    if parser_test:
        data = symcirc.parse.parse(netlist)

    if analysis_test:

        """n = utils.load_file(netlist)
        circuit = parse.unpack_subcircuit(n)"""

        analysis = "TF"
        t0 = time.time()
        circuit = symcirc.analysis.AnalyseCircuit(netlist, analysis, symbolic=True, precision=6, method=method, sympy_ilt=True)
        print(time.time() - t0)
        all = circuit.component_values()
        t1 = time.time()
        print(f"TF: {circuit.transfer_function('0', '1')}")
        """
        c = circuit.components["I1"]
        F = circuit.component_voltage("C").subs(c.sym_value, c.tran_value)
        print("F = {}".format(F))
        f = residue_laplace(F)
        print("f = {}".format(f))
        """

    if test_prints:
        #print(circuit.components)
        t1 = time.time()

        print("TEST -- print matrix: start")
        sympy.pprint(circuit.eqn_matrix)
        print("TEST -- print matrix: end")

        print("run time: {}".format(t1 - t0))
        print(circuit.node_voltage_symbols)
        node_volt = circuit.node_voltages()

        for volt in node_volt:
            func = node_volt[volt]
            #func = func.subs("gmu", 0)
            func = func.limit("C1", sympy.oo)
            func = func.limit("C2", sympy.oo)
            #func = func.subs("go", '1/ro')
            #func = func.subs("gpi", "1/rpi")
            #func = func.subs(sympy.Symbol("G1"), "gm")
            func = func.subs("VN", 0)
            func = sympy.simplify(func)
            print(f"{volt}: {func}")

        print(f"Node voltages: {node_volt}")

        all = circuit.component_values()
        print("---------------------------------------------------------")
        print("All components: {}".format(all))
        print(circuit.symbols)
        #utils.latex_print(all)
        #utils.latex_print(circuit.node_voltages())


    if plots:
        xpoints = []
        ypoints = []
        all_values = circuit.component_values()
        all_voltages = circuit.component_values()
        node_voltages = circuit.node_voltages()
        n = 0
        for symbol_eqn in all_values:
            #try:
            n += 1
            func = all_values[symbol_eqn]

            for symbol in circuit.components:
                value = circuit.components[symbol].value
                func = func.subs(symbol, value)
            t_symbol = func.free_symbols
            print(func)

            #print(str(node)+": "+str(func))
            if analysis == "tran":
                test_utils.plot(func, utils.t, 0, 2, 10000, title=symbol_eqn)
            else:
                test_utils.plot(func, utils.s, 0, 0.01, 10000, title=symbol_eqn)
            """
            except Exception as e:
            print(e)
            """
    #print(all["i(V1)"].subs(t, 1))
    #print("RunTime: {}".format(t1 - t0))






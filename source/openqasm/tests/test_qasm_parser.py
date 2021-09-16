from openqasm.ast import (
    AliasStatement,
    AssignmentOperator,
    BinaryExpression,
    BinaryOperator,
    BitType,
    BitTypeName,
    BooleanLiteral,
    Box,
    BranchingStatement,
    CalibrationDefinition,
    CalibrationGrammarDeclaration,
    ClassicalArgument,
    ClassicalAssignment,
    ClassicalDeclaration,
    ComplexType,
    Concatenation,
    Constant,
    ConstantName,
    ContinueStatement,
    DelayInstruction,
    DoubleDesignatorType,
    DoubleDesignatorTypeName,
    DurationOf,
    ExpressionStatement,
    ForInLoop,
    FunctionCall,
    GateModifierName,
    Identifier,
    IndexExpression,
    IntegerLiteral,
    IODeclaration,
    IOIdentifierName,
    NoDesignatorType,
    NoDesignatorTypeName,
    OpenNode,
    Program,
    QuantumArgument,
    QuantumGateModifier,
    QuantumMeasurement,
    QubitDeclaration,
    QubitDeclTypeName,
    Qubit,
    QuantumGate,
    QuantumGateDefinition,
    RangeDefinition,
    RealLiteral,
    ReturnStatement,
    Selection,
    SingleDesignatorType,
    SingleDesignatorTypeName,
    Slice,
    StringLiteral,
    SubroutineDefinition,
    Subscript,
    TimeUnit,
    DurationLiteral,
    UnaryExpression,
    UnaryOperator,
)
from openqasm.parser.antlr.qasm_parser import parse, Span
from openqasm.ast_visitor.ast_visitor import NodeVisitor


class SpanGuard(NodeVisitor):
    """Ensure that we did not forget to set spans when we add new AST nodes"""

    def visit(self, node: OpenNode):
        try:
            assert node.span is not None
            return super().visit(node)
        except Exception as e:
            raise Exception(f"The span of {type(node)} is None.") from e


def test_qubit_declaration():
    p = """
    qubit q;
    qubit[4] a; 
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            QubitDeclaration(QubitDeclTypeName["qubit"], qubit=Qubit(name="q"), designator=None),
            QubitDeclaration(
                QubitDeclTypeName["qubit"], qubit=Qubit(name="a"), designator=IntegerLiteral(4)
            ),
        ]
    )
    SpanGuard().visit(program)
    qubit_declaration = program.statements[0]
    assert qubit_declaration.span == Span(1, 0, 1, 7)
    assert qubit_declaration.qubit.span == Span(1, 6, 1, 6)


def test_bit_declaration():
    p = """
    bit c;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[ClassicalDeclaration(BitType(BitTypeName["bit"], None), Identifier("c"), None)]
    )
    SpanGuard().visit(program)
    classical_declaration = program.statements[0]
    assert classical_declaration.span == Span(1, 0, 1, 5)


def test_qubit_and_bit_declaration():
    p = """
    bit c;
    qubit a; 
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            ClassicalDeclaration(BitType(BitTypeName["bit"], None), Identifier("c"), None),
            QubitDeclaration(QubitDeclTypeName["qubit"], qubit=Qubit(name="a"), designator=None),
        ]
    )
    SpanGuard().visit(program)


def test_complex_declaration():
    p = """
    complex[int[24]] iq;
    complex[fixed[5, 7]] iq2;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            ClassicalDeclaration(
                ComplexType(
                    base_type=SingleDesignatorType(
                        SingleDesignatorTypeName["int"],
                        IntegerLiteral(24),
                    )
                ),
                Identifier("iq"),
                None,
            ),
            ClassicalDeclaration(
                ComplexType(
                    base_type=DoubleDesignatorType(
                        DoubleDesignatorTypeName["fixed"],
                        IntegerLiteral(5),
                        IntegerLiteral(7),
                    )
                ),
                Identifier("iq2"),
                None,
            ),
        ]
    )
    SpanGuard().visit(program)
    context_declaration = program.statements[0]
    assert context_declaration.span == Span(1, 0, 1, 19)


def test_single_gatecall():
    p = """
    h q;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            QuantumGate(modifiers=[], name="h", arguments=[], qubits=[Identifier(name="q")])
        ]
    )
    SpanGuard().visit(program)
    quantum_gate = program.statements[0]
    assert quantum_gate.span == Span(1, 0, 1, 3)
    assert quantum_gate.qubits[0].span == Span(1, 2, 1, 2)


def test_gate_definition():
    p = """
gate xy q {
    x q;
    y q;
}
""".strip()
    program = parse(p)
    assert program == Program(
        statements=[
            QuantumGateDefinition(
                "xy",
                [],
                [Identifier("q")],
                [
                    QuantumGate(
                        modifiers=[], name="x", arguments=[], qubits=[Identifier(name="q")]
                    ),
                    QuantumGate(
                        modifiers=[], name="y", arguments=[], qubits=[Identifier(name="q")]
                    ),
                ],
            )
        ],
    )
    SpanGuard().visit(program)
    gate_declaration = program.statements[0]
    assert gate_declaration.span == Span(1, 0, 4, 0)
    assert gate_declaration.qubits[0].span == Span(1, 8, 1, 8)


def test_gate_calls():
    p = """
    qubit q;
    qubit r;
    h q;
    cx q, r;
    inv @ h q;
    """.strip()
    # TODO Add "ctrl @ pow(power) @ phase(theta) q, r;" after we complete expressions
    program = parse(p)
    assert program == Program(
        statements=[
            QubitDeclaration(QubitDeclTypeName["qubit"], qubit=Qubit(name="q"), designator=None),
            QubitDeclaration(QubitDeclTypeName["qubit"], qubit=Qubit(name="r"), designator=None),
            QuantumGate(modifiers=[], name="h", arguments=[], qubits=[Identifier(name="q")]),
            QuantumGate(
                modifiers=[],
                name="cx",
                arguments=[],
                qubits=[Identifier(name="q"), Identifier(name="r")],
            ),
            QuantumGate(
                modifiers=[QuantumGateModifier(modifier=GateModifierName["inv"], argument=None)],
                name="h",
                arguments=[],
                qubits=[Identifier(name="q")],
            ),
        ],
    )
    SpanGuard().visit(program)


def test_gate_defs():
    p = """
    gate xyz q {
        x q;
        y q;
        z q;
    }
    """.strip()

    program = parse(p)
    assert program == Program(
        statements=[
            QuantumGateDefinition(
                name="xyz",
                arguments=[],
                qubits=[Identifier(name="q")],
                body=[
                    QuantumGate(
                        modifiers=[], name="x", arguments=[], qubits=[Identifier(name="q")]
                    ),
                    QuantumGate(
                        modifiers=[], name="y", arguments=[], qubits=[Identifier(name="q")]
                    ),
                    QuantumGate(
                        modifiers=[], name="z", arguments=[], qubits=[Identifier(name="q")]
                    ),
                ],
            )
        ],
    )
    SpanGuard().visit(program)


def test_alias_statement():
    p = """
    let a = b;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[AliasStatement(target=Identifier(name="a"), value=Identifier(name="b"))]
    )
    SpanGuard().visit(program)
    alias_statement = program.statements[0]
    assert alias_statement.span == Span(1, 0, 1, 9)
    assert alias_statement.target.span == Span(1, 4, 1, 4)
    assert alias_statement.value.span == Span(1, 8, 1, 8)


def test_primary_expression():
    p = """
    π;
    5;
    2.0;
    true;
    false;
    a;
    "openqasm";
    sin(0.0);
    foo(x);
    1.1ns;
    (x);
    q[1];
    """.strip()

    program = parse(p)
    assert program == Program(
        statements=[
            ExpressionStatement(expression=Constant(name=ConstantName["π"])),
            ExpressionStatement(expression=IntegerLiteral(5)),
            ExpressionStatement(expression=RealLiteral(2.0)),
            ExpressionStatement(expression=BooleanLiteral(True)),
            ExpressionStatement(expression=BooleanLiteral(False)),
            ExpressionStatement(expression=Identifier("a")),
            ExpressionStatement(expression=StringLiteral("openqasm")),
            ExpressionStatement(expression=FunctionCall("sin", [RealLiteral(0.0)])),
            ExpressionStatement(expression=FunctionCall("foo", [Identifier("x")])),
            ExpressionStatement(expression=DurationLiteral(1.1, TimeUnit.ns)),
            ExpressionStatement(expression=Identifier("x")),
            ExpressionStatement(expression=IndexExpression(Identifier("q"), IntegerLiteral(1))),
        ]
    )


def test_unary_expression():
    p = """
    ~b;
    !b;
    -i;
    """.strip()

    program = parse(p)
    assert program == Program(
        statements=[
            ExpressionStatement(
                expression=UnaryExpression(
                    op=UnaryOperator["~"],
                    expression=Identifier(name="b"),
                )
            ),
            ExpressionStatement(
                expression=UnaryExpression(
                    op=UnaryOperator["!"],
                    expression=Identifier(name="b"),
                )
            ),
            ExpressionStatement(
                expression=UnaryExpression(
                    op=UnaryOperator["-"],
                    expression=Identifier(name="i"),
                )
            ),
        ]
    )


def test_binary_expression():
    p = """
    b1 || b2;
    b1 && b2;
    b1 | b2;
    b1 ^ b2;
    b1 & b2;
    b1 != b2;
    i1 >= i2;
    i1 << i2;
    i1 - i2;
    i1 / i2;
    """.strip()

    program = parse(p)
    assert program == Program(
        statements=[
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["||"],
                    lhs=Identifier(name="b1"),
                    rhs=Identifier(name="b2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["&&"],
                    lhs=Identifier(name="b1"),
                    rhs=Identifier(name="b2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["|"],
                    lhs=Identifier(name="b1"),
                    rhs=Identifier(name="b2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["^"],
                    lhs=Identifier(name="b1"),
                    rhs=Identifier(name="b2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["&"],
                    lhs=Identifier(name="b1"),
                    rhs=Identifier(name="b2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["!="],
                    lhs=Identifier(name="b1"),
                    rhs=Identifier(name="b2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator[">="],
                    lhs=Identifier(name="i1"),
                    rhs=Identifier(name="i2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["<<"],
                    lhs=Identifier(name="i1"),
                    rhs=Identifier(name="i2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["-"],
                    lhs=Identifier(name="i1"),
                    rhs=Identifier(name="i2"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["/"],
                    lhs=Identifier(name="i1"),
                    rhs=Identifier(name="i2"),
                )
            ),
        ]
    )


def test_binary_expression_precedence():
    p = """
    b1 || b2 && b3;
    b1 | b2 ^ b3;
    b1 != b2 + b3;
    i1 >= i2 + i3;
    i1 - i2 << i3;
    i1 - i2 / i3;
    """.strip()

    program = parse(p)
    assert program == Program(
        statements=[
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["||"],
                    lhs=Identifier(name="b1"),
                    rhs=BinaryExpression(
                        op=BinaryOperator["&&"],
                        lhs=Identifier(name="b2"),
                        rhs=Identifier(name="b3"),
                    ),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["|"],
                    lhs=Identifier(name="b1"),
                    rhs=BinaryExpression(
                        op=BinaryOperator["^"],
                        lhs=Identifier(name="b2"),
                        rhs=Identifier(name="b3"),
                    ),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["!="],
                    lhs=Identifier(name="b1"),
                    rhs=BinaryExpression(
                        op=BinaryOperator["+"],
                        lhs=Identifier(name="b2"),
                        rhs=Identifier(name="b3"),
                    ),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator[">="],
                    lhs=Identifier(name="i1"),
                    rhs=BinaryExpression(
                        op=BinaryOperator["+"],
                        lhs=Identifier(name="i2"),
                        rhs=Identifier(name="i3"),
                    ),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["<<"],
                    lhs=BinaryExpression(
                        op=BinaryOperator["-"],
                        lhs=Identifier(name="i1"),
                        rhs=Identifier(name="i2"),
                    ),
                    rhs=Identifier(name="i3"),
                )
            ),
            ExpressionStatement(
                expression=BinaryExpression(
                    op=BinaryOperator["-"],
                    lhs=Identifier(name="i1"),
                    rhs=BinaryExpression(
                        op=BinaryOperator["/"],
                        lhs=Identifier(name="i2"),
                        rhs=Identifier(name="i3"),
                    ),
                )
            ),
        ]
    )


def test_subscript():
    p = """
    let a = b[10];
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            AliasStatement(
                target=Identifier(name="a"),
                value=Subscript(name="b", index=IntegerLiteral(value=10)),
            )
        ]
    )
    SpanGuard().visit(program)
    subscript = program.statements[0]
    assert subscript.span == Span(1, 0, 1, 13)
    assert subscript.target.span == Span(1, 4, 1, 4)
    assert subscript.value.span == Span(1, 8, 1, 12)


def test_selection():
    p = """
    let a = b[1, 2];
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            AliasStatement(
                target=Identifier(name="a"),
                value=Selection(
                    name="b", indices=[IntegerLiteral(value=1), IntegerLiteral(value=2)]
                ),
            )
        ]
    )
    SpanGuard().visit(program)
    selection = program.statements[0]
    assert selection.span == Span(1, 0, 1, 15)
    assert selection.target.span == Span(1, 4, 1, 4)
    assert selection.value.span == Span(1, 8, 1, 14)


def test_slice():
    p = """
    let a = b[1:10:1];
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            AliasStatement(
                target=Identifier(name="a"),
                value=Slice(
                    name="b",
                    range=RangeDefinition(
                        start=IntegerLiteral(value=1),
                        end=IntegerLiteral(value=10),
                        step=IntegerLiteral(value=1),
                    ),
                ),
            )
        ]
    )
    SpanGuard().visit(program)
    slice_ = program.statements[0]
    assert slice_.span == Span(1, 0, 1, 17)
    assert slice_.target.span == Span(1, 4, 1, 4)
    assert slice_.value.span == Span(1, 8, 1, 16)


def test_concatenation():
    p = """
    let a = b[1:10:1] || c;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            AliasStatement(
                target=Identifier(name="a"),
                value=Concatenation(
                    lhs=Slice(
                        name="b",
                        range=RangeDefinition(
                            start=IntegerLiteral(value=1),
                            end=IntegerLiteral(value=10),
                            step=IntegerLiteral(value=1),
                        ),
                    ),
                    rhs=Identifier(name="c"),
                ),
            )
        ]
    )
    SpanGuard().visit(program)
    slice_ = program.statements[0]
    assert slice_.span == Span(1, 0, 1, 22)
    assert slice_.target.span == Span(1, 4, 1, 4)
    assert slice_.value.span == Span(1, 8, 1, 21)


def test_calibration_grammar_declaration():
    p = """
    defcalgrammar "openpulse";
    """.strip()
    program = parse(p)
    assert program == Program(statements=[CalibrationGrammarDeclaration("openpulse")])
    SpanGuard().visit(program)


def test_calibration_definition():
    p = """
    defcal rz(angle[20] theta) $q -> bit { return shift_phase drive($q), -theta; }
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            CalibrationDefinition(
                name="rz",
                arguments=[
                    ClassicalArgument(
                        type=SingleDesignatorType(
                            type=SingleDesignatorTypeName["angle"], designator=IntegerLiteral(20)
                        ),
                        name="theta",
                    )
                ],
                qubits=["$q"],
                return_type=BitType(BitTypeName.bit, None),
                body="return shift_phase drive ( $q ) , - theta ;",
            )
        ]
    )
    SpanGuard().visit(program)


def test_subroutine_definition():
    p = """
    def ymeasure(qubit q) -> bit {
        s q;
        h q;
        return measure q;
    }
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            SubroutineDefinition(
                name="ymeasure",
                arguments=[QuantumArgument(qubit=Qubit("q"), designator=None)],
                return_type=BitType(BitTypeName.bit, None),
                body=[
                    QuantumGate(
                        modifiers=[], name="s", arguments=[], qubits=[Identifier(name="q")]
                    ),
                    QuantumGate(
                        modifiers=[], name="h", arguments=[], qubits=[Identifier(name="q")]
                    ),
                    ReturnStatement(expression=QuantumMeasurement(qubits=[Identifier(name="q")])),
                ],
            )
        ]
    )
    SpanGuard().visit(program)


def test_branch_statement():
    p = """
    if(temp == 1) { ry(pi / 2) q; } else continue;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            BranchingStatement(
                condition=BinaryExpression(
                    op=BinaryOperator["=="], lhs=Identifier("temp"), rhs=IntegerLiteral(1)
                ),
                if_block=[
                    QuantumGate(
                        modifiers=[],
                        name="ry",
                        arguments=[
                            BinaryExpression(
                                op=BinaryOperator["/"],
                                lhs=Constant(ConstantName["pi"]),
                                rhs=IntegerLiteral(2),
                            )
                        ],
                        qubits=[Identifier("q")],
                    ),
                ],
                else_block=[ContinueStatement()],
            )
        ]
    )
    SpanGuard().visit(program)


def test_for_in_loop():
    p = """
    for i in [0: 2] { majority a[i], b[i + 1], a[i + 1]; }
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            ForInLoop(
                loop_variable=Identifier("i"),
                set_declaration=RangeDefinition(
                    start=IntegerLiteral(0), end=IntegerLiteral(2), step=None
                ),
                block=[
                    QuantumGate(
                        modifiers=[],
                        name="majority",
                        arguments=[],
                        qubits=[
                            Subscript(name="a", index=Identifier("i")),
                            Subscript(
                                name="b",
                                index=BinaryExpression(
                                    op=BinaryOperator["+"],
                                    lhs=Identifier("i"),
                                    rhs=IntegerLiteral(1),
                                ),
                            ),
                            Subscript(
                                name="a",
                                index=BinaryExpression(
                                    op=BinaryOperator["+"],
                                    lhs=Identifier("i"),
                                    rhs=IntegerLiteral(1),
                                ),
                            ),
                        ],
                    ),
                ],
            )
        ]
    )
    SpanGuard().visit(program)


def test_delay_instruction():
    p = """
    delay[start_stretch] $0;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            DelayInstruction(
                arguments=[],
                duration=Identifier("start_stretch"),
                qubits=[Identifier("$0")],
            )
        ]
    )
    SpanGuard().visit(program)


def test_no_designator_type():
    p = """
    duration a;
    stretch b;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            ClassicalDeclaration(
                NoDesignatorType(NoDesignatorTypeName["duration"]), Identifier("a"), None
            ),
            ClassicalDeclaration(
                NoDesignatorType(NoDesignatorTypeName["stretch"]), Identifier("b"), None
            ),
        ]
    )
    SpanGuard().visit(program)


def test_box():
    p = """
    box [maxdur] {
        delay[start_stretch] $0;
        x $0;
    }
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            Box(
                duration=Identifier("maxdur"),
                body=[
                    DelayInstruction(
                        arguments=[],
                        duration=Identifier("start_stretch"),
                        qubits=[Identifier("$0")],
                    ),
                    QuantumGate(modifiers=[], name="x", arguments=[], qubits=[Identifier("$0")]),
                ],
            )
        ]
    )
    SpanGuard().visit(program)


def test_quantumloop():
    p = """
    box [maxdur] {
        delay[start_stretch] $0;
        for i in [1:2]{
            h $0;
            cx $0, $1;
        }
        x $0;
    }
    """.strip()
    program = parse(p)
    print(parse(p))
    assert program == Program(
        statements=[
            Box(
                duration=Identifier("maxdur"),
                body=[
                    DelayInstruction(
                        arguments=[],
                        duration=Identifier("start_stretch"),
                        qubits=[Identifier("$0")],
                    ),
                    ForInLoop(
                        loop_variable=Identifier(name="i"),
                        set_declaration=RangeDefinition(
                            start=IntegerLiteral(value=1), end=IntegerLiteral(value=2), step=None
                        ),
                        block=[
                            QuantumGate(
                                modifiers=[], name="h", arguments=[], qubits=[Identifier(name="$0")]
                            ),
                            QuantumGate(
                                modifiers=[],
                                name="cx",
                                arguments=[],
                                qubits=[Identifier(name="$0"), Identifier(name="$1")],
                            ),
                        ],
                    ),
                    QuantumGate(modifiers=[], name="x", arguments=[], qubits=[Identifier("$0")]),
                ],
            )
        ]
    )
    SpanGuard().visit(program)


def test_durationof():
    p = """
    durationof({x $0;})
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            ExpressionStatement(
                expression=DurationOf(
                    target=[
                        QuantumGate(
                            modifiers=[], name="x", arguments=[], qubits=[Identifier("$0")]
                        ),
                    ]
                )
            )
        ]
    )
    SpanGuard().visit(program)


def test_classical_assignment():
    p = """
    a[0] = 1;
    """.strip()
    program = parse(p)
    assert program == Program(
        statements=[
            ClassicalAssignment(
                lvalue=Subscript(name="a", index=IntegerLiteral(value=0)),
                op=AssignmentOperator["="],
                rvalue=IntegerLiteral(1),
            )
        ]
    )
    SpanGuard().visit(program)


def test_header():
    p = """
    OPENQASM 3.1;
    input angle[16] variable1;
    output angle[16] variable2;
    """.strip()
    program = parse(p)
    expected = {"major": 3, "minor": 1}
    assert program.version == expected
    assert program.io_variables == [
        IODeclaration(
            io_identifier=IOIdentifierName["input"],
            type=SingleDesignatorType(
                type=SingleDesignatorTypeName["angle"], designator=IntegerLiteral(value=16)
            ),
            identifier=Identifier(name="variable1"),
            init_expression=None,
        ),
        IODeclaration(
            io_identifier=IOIdentifierName["output"],
            type=SingleDesignatorType(
                type=SingleDesignatorTypeName["angle"], designator=IntegerLiteral(value=16)
            ),
            identifier=Identifier(name="variable2"),
            init_expression=None,
        ),
    ]

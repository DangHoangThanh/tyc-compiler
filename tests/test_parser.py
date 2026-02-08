"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


# --- Happy Path ---
def test_parser_empty_program():
    """An empty file is a valid program."""
    source = ""
    assert Parser(source).parse() == "success"

def test_parser_simple_func():
    """Standard void function with no parameters."""
    source = "void main() {}"
    assert Parser(source).parse() == "success"

def test_parser_inferred_return():
    """Functions can omit the return type (implied auto/void)."""
    source = "main() {}"
    assert Parser(source).parse() == "success"

def test_parser_params():
    """Function with multiple typed parameters."""
    source = "int add(int a, float b) { return a; }"
    assert Parser(source).parse() == "success"

def test_parser_global_struct():
    """Struct declaration at the global level."""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"

def test_parser_var_decl_int():
    """Explicitly typed variable declaration."""
    source = "void f() { int x = 10; }"
    assert Parser(source).parse() == "success"

def test_parser_var_decl_auto():
    """Variable declaration using auto."""
    source = "void f() { auto x = 1.5; }"
    assert Parser(source).parse() == "success"

def test_parser_struct_init():
    """Initialization of a struct variable using braces."""
    source = "void f() { Point p = {1, 2}; }"
    assert Parser(source).parse() == "success"

def test_parser_if_else():
    """Standard if-else block."""
    source = "void f() { if (x) { return 1; } else { return 0; } }"
    assert Parser(source).parse() == "success"

def test_parser_while_loop():
    """Standard while loop with block."""
    source = "void f() { while (1) { x++; } }"
    assert Parser(source).parse() == "success"

def test_parser_for_loop_decl():
    """For loop with a variable declaration in the init section."""
    source = "void f() { for (int i = 0; i < 10; i++) {} }"
    assert Parser(source).parse() == "success"

def test_parser_for_loop_expr():
    """For loop with an expression in the init section."""
    source = "void f() { for (i = 0; i < 10; i++) {} }"
    assert Parser(source).parse() == "success"

def test_parser_switch_stmt():
    """Switch statement with multiple cases and default."""
    source = "void f() { switch(x) { case 1: break; default: continue; } }"
    assert Parser(source).parse() == "success"

def test_parser_math_precedence():
    """Verify additive and multiplicative precedence."""
    source = "void f() { x = a + b * c / d; }"
    assert Parser(source).parse() == "success"

def test_parser_relational_expr():
    """Comparison operations."""
    source = "void f() { res = a <= b; }"
    assert Parser(source).parse() == "success"

def test_parser_logical_expr():
    """Boolean logic operations."""
    source = "void f() { if (a && b || !c) {} }"
    assert Parser(source).parse() == "success"

def test_parser_member_access():
    """Struct member access using dot notation."""
    source = "void f() { p.x = 10; }"
    assert Parser(source).parse() == "success"

def test_parser_inc_dec():
    """Postfix and prefix operators."""
    source = "void f() { x++; --y; }"
    assert Parser(source).parse() == "success"

def test_parser_return_expr():
    """Returning a complex expression."""
    source = "int f() { return (a + b); }"
    assert Parser(source).parse() == "success"

def test_parser_func_call():
    """Function call as a statement."""
    source = "void f() { print(s); }"
    assert Parser(source).parse() == "success"

def test_parser_nested_blocks():
    """Scope within scope."""
    source = "void f() { { int x; } }"
    assert Parser(source).parse() == "success"

def test_parser_string_literal_usage():
    """Assigning string literals."""
    source = 'void f() { string s = "hello"; }'
    assert Parser(source).parse() == "success"

def test_parser_multiple_globals():
    """Sequence of structs and functions."""
    source = "struct A{}; void f(){} struct B{};"
    assert Parser(source).parse() == "success"

def test_parser_empty_return():
    """Return statement with no value."""
    source = "void f() { return; }"
    assert Parser(source).parse() == "success"

def test_parser_struct_member_types():
    """Struct members using identifiers as types."""
    source = "struct Node { int val; Node next; };"
    assert Parser(source).parse() == "success"

def test_parser_block_item_mix():
    """Interleaving declarations and statements."""
    source = "void f() { int x; x = 5; auto y = 1.0; }"
    assert Parser(source).parse() == "success"

def test_parser_for_empty_parts():
    """For loop with empty control components."""
    source = "void f() { for (;;) {} }"
    assert Parser(source).parse() == "success"

def test_parser_switch_labels():
    """Multiple labels for a single block of code."""
    source = "void f() { switch(x) { case 1: case 2: return; } }"
    assert Parser(source).parse() == "success"

def test_parser_float_scientific_expr():
    """Scientific notation in expressions."""
    source = "void f() { x = 1.2e10 + .5; }"
    assert Parser(source).parse() == "success"

def test_parser_primary_parens():
    """Parentheses in expressions."""
    source = "void f() { x = (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"
    

# --- Boundary Cases ---

def test_parser_minimal_struct():
    """Struct with no members."""
    source = "struct S {};"
    assert Parser(source).parse() == "success"

def test_parser_standalone_semi():
    """Semicolons as empty statements."""
    source = "void f() { ; ; ; }"
    assert Parser(source).parse() == "success"

def test_parser_auto_no_init():
    """Auto without assignment (syntactically valid in this grammar)."""
    source = "void f() { auto x; }"
    assert Parser(source).parse() == "success"

def test_parser_while_no_block():
    """While loop with a single statement instead of a block."""
    source = "void f() { while(1) ; }"
    assert Parser(source).parse() == "success"

def test_parser_switch_default_only():
    """Switch statement containing only the default label."""
    source = "void f() { switch(x) { default: break; } }"
    assert Parser(source).parse() == "success"

def test_parser_struct_init_trailing_comma():
    """Verify that trailing commas in struct inits are NOT allowed."""
    source = "void f() { p = {1, 2,}; }"
    # Based on: (expr (COMMA expr)*)? -> No trailing comma
    assert Parser(source).parse() != "success"

def test_parser_nested_empty_blocks():
    """Braces inside braces with no content."""
    source = "void f() { {{{}}} }"
    assert Parser(source).parse() == "success"

def test_parser_deep_parens_literal():
    """Deeply nested expression."""
    source = "void f() { x = (((1))); }"
    assert Parser(source).parse() == "success"

def test_parser_param_struct_type():
    """Using an ID as a type in parameters."""
    source = "void f(Point p) {}"
    assert Parser(source).parse() == "success"

def test_parser_return_in_main():
    """Return statement in void-like function."""
    source = "void main() { return; }"
    assert Parser(source).parse() == "success"

def test_parser_if_no_else():
    """Simple if without else."""
    source = "void f() { if(1) x=1; }"
    assert Parser(source).parse() == "success"

def test_parser_struct_no_init():
    """Struct declaration without initializer."""
    source = "void f() { Point p; }"
    assert Parser(source).parse() == "success"

def test_parser_for_no_init():
    """For loop missing the initialization part."""
    source = "void f() { for(; i < 10; i++) {} }"
    assert Parser(source).parse() == "success"

def test_parser_for_no_inc():
    """For loop missing the increment part."""
    source = "void f() { for(int i=0; i<10; ) {} }"
    assert Parser(source).parse() == "success"

def test_parser_large_int_primary():
    """Expression with a large number."""
    source = "void f() { x = 9999999; }"
    assert Parser(source).parse() == "success"

def test_parser_call_no_args():
    """Function call with empty arg list."""
    source = "void f() { start(); }"
    assert Parser(source).parse() == "success"

def test_parser_switch_empty_body():
    """Switch with no cases at all."""
    source = "void f() { switch(x) {} }"
    assert Parser(source).parse() == "success"

def test_parser_unary_on_unary():
    """Multiple unary operators."""
    source = "void f() { x = !!y; }"
    assert Parser(source).parse() == "success"

def test_parser_expr_stmt_postfix():
    """Stand-alone postfix expression."""
    source = "void f() { x++; }"
    assert Parser(source).parse() == "success"

def test_parser_return_string_literal():
    """Function returning string literal."""
    source = 'string f() { return "ok"; }'
    assert Parser(source).parse() == "success"
    
    
# --- Complex ---

def test_parser_dangling_else():
    """Ensure else binds to the nearest if."""
    source = "void f() { if(a) if(b) x=1; else x=2; }"
    assert Parser(source).parse() == "success"

def test_parser_assignment_right_assoc():
    """Assignments are right-associative."""
    source = "void f() { a = b = c = 0; }"
    assert Parser(source).parse() == "success"

def test_parser_member_access_chain():
    """Multiple dots in a single expression."""
    source = "void f() { a.b.c.d = 10; }"
    assert Parser(source).parse() == "success"

def test_parser_precedence_full():
    """Mix of math and logic precedence."""
    source = "void f() { x = a + b * c == d || !e; }"
    assert Parser(source).parse() == "success"

def test_parser_nested_loops_complex():
    """For loop inside a while loop."""
    source = "void f() { while(1) { for(int i=0; i<10; i++) { break; } } }"
    assert Parser(source).parse() == "success"

def test_parser_switch_with_statements():
    """Switch cases containing declarations and logic."""
    source = "void f() { switch(x) { case 1: int y = 2; break; } }"
    assert Parser(source).parse() == "success"

def test_parser_call_in_call():
    """Function calls as arguments."""
    source = "void f() { print(calculate(1, 2)); }"
    assert Parser(source).parse() == "success"

def test_parser_complex_struct_init():
    """Struct initializer with expressions."""
    source = "void f() { Point p = {a + b, c}; }"
    assert Parser(source).parse() == "success"

def test_parser_recursive_func():
    """Function calling itself."""
    source = "int f(int n) { if(n<1) return 1; return n * f(n-1); }"
    assert Parser(source).parse() == "success"

def test_parser_logic_grouping():
    """Using parentheses to override logic precedence."""
    source = "void f() { x = (a || b) && c; }"
    assert Parser(source).parse() == "success"

def test_parser_assignment_in_while():
    """Assigning inside a while condition."""
    source = "void f() { while(x = next()) {} }"
    assert Parser(source).parse() == "success"

def test_parser_complex_postfix_prefix():
    """Mixing increment/decrement in expressions."""
    source = "void f() { x = ++y + z--; }"
    assert Parser(source).parse() == "success"

def test_parser_for_loop_decl_auto():
    """Auto declaration in for loop."""
    source = "void f() { for(auto i = 0; i < 10; i++) {} }"
    assert Parser(source).parse() == "success"

def test_parser_switch_multiple_labels_block():
    """Cases sharing a block."""
    source = "void f() { switch(x) { case 1: case 2: { do_work(); } break; } }"
    assert Parser(source).parse() == "success"

def test_parser_global_decl_mix():
    """Mix of structs and functions in file."""
    source = "struct A{}; void f1(){} struct B{}; void f2(){}"
    assert Parser(source).parse() == "success"

def test_parser_not_expr_stmt():
    """Logic NOT as a statement (useless but syntactically valid)."""
    source = "void f() { !x; }"
    assert Parser(source).parse() == "success"

def test_parser_nested_if_else_if():
    """If-else-if ladder."""
    source = "void f() { if(a) {} else if(b) {} else {} }"
    assert Parser(source).parse() == "success"

def test_parser_unary_on_member():
    """Negating a struct member access."""
    source = "void f() { x = !p.is_valid; }"
    assert Parser(source).parse() == "success"

def test_parser_complex_for_control():
    """For loop with math in control."""
    source = "void f() { for(i = a + b; i < f(x); i++) {} }"
    assert Parser(source).parse() == "success"

def test_parser_member_access_on_call():
    """Accessing member of returned value."""
    source = "void f() { x = get_point().x; }"
    assert Parser(source).parse() == "success"

def test_parser_unary_prefix_math():
    """Unary operators with arithmetic."""
    source = "void f() { x = -5 * +3; }"
    assert Parser(source).parse() == "success"

def test_parser_long_param_list():
    """Function with many parameters."""
    source = "void f(int a, float b, string c, int d, float e) {}"
    assert Parser(source).parse() == "success"

def test_parser_math_mod_prec():
    """Modulo operator precedence."""
    source = "void f() { x = a % b + c; }"
    assert Parser(source).parse() == "success"

def test_parser_return_func_call():
    """Returning the result of a function."""
    source = "int f() { return g(10); }"
    assert Parser(source).parse() == "success"

def test_parser_multiple_calls_stmt():
    """Sequential function calls."""
    source = "void f() { a(); b(); c(); }"
    assert Parser(source).parse() == "success"

def test_parser_switch_default_top():
    """Switch with default not at the bottom."""
    source = "void f() { switch(x) { default: break; case 1: return; } }"
    assert Parser(source).parse() == "success"

def test_parser_inc_dec_on_member():
    """Incrementing a struct field."""
    source = "void f() { p.count++; }"
    assert Parser(source).parse() == "success"

def test_parser_mixed_scientific_math():
    """Mixing floats and scientific notation."""
    source = "void f() { x = 1.5 + 2e-3; }"
    assert Parser(source).parse() == "success"

def test_parser_parens_in_logic():
    """Logic expressions with complex grouping."""
    source = "void f() { if((a && b) || (c && d)) {} }"
    assert Parser(source).parse() == "success"

def test_parser_struct_nested_type_ref():
    """Struct referring to a type defined later."""
    source = "struct A { B b; }; struct B { int x; };"
    assert Parser(source).parse() == "success"
    
def test_parser_var_decl_nested_init():
    source = """
    struct Point { int x; };
    struct Rect { Point p; };
    void main() { Rect r = {{1}}; }
    """
    assert Parser(source).parse() == "success"
    
def test_parser_func_call_struct_literal():
    source = "void main() { f({1, 2}); }"
    assert Parser(source).parse() == "success"
    
def test_parser_expr_struct_literal_complex():
    source = "void main() { p = {1+2, f(a)}; }"
    assert Parser(source).parse() == "success"

def test_parser_error_assignment_to_literal():
    source = "void main() { 5 = x; }"
    assert Parser(source).parse() != "success"
    
def test_parser_error_assignment_in_case():
    source = """
    void main() {
        switch (x) {
            case a = 5: break; 
        }
    }
    """
    assert Parser(source).parse() != "success"
    
# --- Error ---

def test_parser_error_global_assignment():
    """Assignments are not allowed at global scope."""
    source = "x = 10;"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_type_param():
    """Function parameters must have an explicit type."""
    source = "void f(a) {}"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_semi_struct():
    """Struct members must end in semicolons."""
    source = "struct S { int x }"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_semi_decl():
    """Variable declarations must end in semicolons."""
    source = "void f() { int x = 5 }"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_parens_if():
    """If condition requires parentheses."""
    source = "void f() { if x < 10 {} }"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_braces_func():
    """Function body must be a block."""
    source = "void f() ;"
    assert Parser(source).parse() != "success"

def test_parser_error_void_variable():
    """Void is not a valid variable type."""
    source = "void f() { void x; }"
    assert Parser(source).parse() != "success"

def test_parser_error_auto_in_struct():
    """Struct members cannot be auto (per type_ rule)."""
    source = "struct S { auto x; };"
    assert Parser(source).parse() != "success"

def test_parser_error_double_else():
    """Else cannot exist without a matching if."""
    source = "void f() { if(1){} else{} else{} }"
    assert Parser(source).parse() != "success"

def test_parser_error_case_outside_switch():
    """Case labels are only allowed in switches."""
    source = "void f() { case 1: return; }"
    assert Parser(source).parse() != "success"

def test_parser_error_for_comma_sep():
    """For loop parts must be separated by semicolons."""
    source = "void f() { for(int i=0, i<10, i++) {} }"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_colon_switch():
    """Switch labels require a colon."""
    source = "void f() { switch(x) { case 1 break; } }"
    assert Parser(source).parse() != "success"

def test_parser_error_nested_func():
    """Functions cannot be defined inside other functions."""
    source = "void f() { void g() {} }"
    assert Parser(source).parse() != "success"

def test_parser_error_trailing_comma_params():
    """Parameter list cannot end with a comma."""
    source = "void f(int a,) {}"
    assert Parser(source).parse() != "success"

def test_parser_error_global_stmt():
    """Statement found at global scope."""
    source = "print(10);"
    assert Parser(source).parse() != "success"

def test_parser_error_missing_brace_block():
    """Block missing the closing brace."""
    source = "void f() { if(1) { return 0; }"
    assert Parser(source).parse() != "success"

def test_parser_error_struct_missing_final_semi():
    """Struct declarations require a semicolon after the closing brace."""
    source = "struct S { int x; } void main() {}"
    assert Parser(source).parse() != "success"

def test_parser_error_invalid_op_sequence():
    """Invalid operator placement."""
    source = "void f() { x = a + * b; }"
    assert Parser(source).parse() != "success"

def test_parser_error_illegal_character():
    """Lexer error character caught by parser."""
    source = "void f() { int x = @; }"
    assert Parser(source).parse() != "success"

def test_parser_error_incomplete_switch():
    """Switch missing parentheses."""
    source = "void f() { switch x {} }"
    assert Parser(source).parse() != "success"
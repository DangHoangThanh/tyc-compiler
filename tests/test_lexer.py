"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer

# --- Happy path ---

def test_lexer_keywords_flow():
    """Verify control flow keywords."""
    source = "if else for while switch case default break continue return"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "if,else,for,while,switch,case,default,break,continue,return,<EOF>"

def test_lexer_keywords_types():
    """Verify type-related keywords."""
    source = "int float string void auto struct"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "int,float,string,void,auto,struct,<EOF>"

def test_lexer_arithmetic_operators():
    """Verify basic math operators."""
    source = "+ - * / %"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "+,-,*,/,%,<EOF>"

def test_lexer_logical_operators():
    """Verify boolean logic operators."""
    source = "&& || !"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "&&,||,!,<EOF>"

def test_lexer_comparison_operators():
    """Verify relational and equality operators."""
    source = "< > <= >= == !="
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "<,>,<=,>=,==,!=,<EOF>"

def test_lexer_assignment_and_inc():
    """Verify assignment and increment/decrement."""
    source = "= ++ --"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "=,++,--,<EOF>"

def test_lexer_separators():
    """Verify parentheses, braces, and punctuation."""
    source = "( ) { } [ ] ; , : ."
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "(,),{,},[,],;,,,:,.,<EOF>"

def test_lexer_basic_identifiers():
    """Verify standard variable names."""
    source = "x myVar _temp count123"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "x,myVar,_temp,count123,<EOF>"

def test_lexer_integers():
    """Verify integer literals."""
    source = "0 42 1000"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "0,42,1000,<EOF>"

def test_lexer_floats_simple():
    """Verify basic float literals."""
    source = "3.14 0.5 .5 10."
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "3.14,0.5,.5,10.,<EOF>"

def test_lexer_strings_simple():
    """Verify string literals (quotes removed by emit)."""
    source = '"hello" "TyC"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "hello,TyC,<EOF>"

def test_lexer_struct_declaration_tokens():
    """Verify tokens in a struct header."""
    source = "struct Point {"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "struct,Point,{,<EOF>"

def test_lexer_function_header_tokens():
    """Verify tokens in a function signature."""
    source = "int main(string args)"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "int,main,(,string,args,),<EOF>"

def test_lexer_scientific_floats():
    """Verify scientific notation."""
    source = "1e10 1.2E-5"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "1e10,1.2E-5,<EOF>"

def test_lexer_multi_operator_no_space():
    """Verify operators without spaces."""
    source = "a+b*c"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "a,+,b,*,c,<EOF>"

def test_lexer_assignment_statement():
    """Verify tokens in a full assignment."""
    source = "auto x = 5;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,;,<EOF>"

def test_lexer_member_access():
    """Verify dot operator usage."""
    source = "p.x = 1;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "p,.,x,=,1,;,<EOF>"

def test_lexer_multiple_calls():
    """Verify tokens in multiple function calls."""
    source = "f(); g();"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "f,(,),;,g,(,),;,<EOF>"

def test_lexer_bool_literals_as_ids():
    """Verify words that look like bools (but are IDs in TyC)."""
    source = "true false"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "true,false,<EOF>"

def test_lexer_complex_path_id():
    """Verify underscores in identifiers."""
    source = "__internal_var__"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "__internal_var__,<EOF>"

def test_lexer_newline_whitespace():
    """Verify whitespaces are skipped correctly."""
    source = "int\n\rx\t=\n5;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "int,x,=,5,;,<EOF>"

def test_lexer_comment_skip_line():
    """Verify single line comments are skipped."""
    source = "int x; // this is a comment\nint y;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "int,x,;,int,y,;,<EOF>"

def test_lexer_comment_skip_block():
    """Verify block comments are skipped."""
    source = "/* block \n comment */ int z;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "int,z,;,<EOF>"

def test_lexer_string_with_space():
    """Verify strings containing spaces."""
    source = '"white space"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "white space,<EOF>"

def test_lexer_nested_delimiters():
    """Verify nested brackets and parens."""
    source = "[({})]"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "[,(,{,},),],<EOF>"

def test_lexer_increment_decrement_tight():
    """Verify tight inc/dec tokens."""
    source = "x++--y"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "x,++,--,y,<EOF>"

def test_lexer_relational_tight():
    """Verify tight relational tokens."""
    source = "a<=b>=c"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "a,<=,b,>=,c,<EOF>"

def test_lexer_complex_float_starts():
    """Verify various float beginnings."""
    source = ".1 0.1 1.1"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == ".1,0.1,1.1,<EOF>"

def test_lexer_string_containing_ops():
    """Verify operators inside strings are not tokens."""
    source = '"+" "-"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "+,-,<EOF>"

def test_lexer_consecutive_semicolons():
    """Verify multiple semicolons."""
    source = ";;;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == ";,;,;,<EOF>"
    

# --- Boundary Cases ---

def test_lexer_boundary_empty():
    """Verify empty input."""
    source = ""
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "<EOF>"

def test_lexer_boundary_single_underscore():
    """Verify single underscore ID."""
    source = "_"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "_,<EOF>"

def test_lexer_boundary_zero():
    """Verify integer zero."""
    source = "0"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "0,<EOF>"

def test_lexer_boundary_minimal_float():
    """Verify .0 float."""
    source = ".0"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == ".0,<EOF>"

def test_lexer_boundary_float_trailing_dot():
    """Verify trailing dot."""
    source = "0."
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "0.,<EOF>"

def test_lexer_boundary_empty_string():
    """Verify empty string."""
    source = '""'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == ",<EOF>"

def test_lexer_boundary_max_int():
    """Verify large number string."""
    source = "2147483647"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "2147483647,<EOF>"

def test_lexer_boundary_scientific_zero():
    """Verify zero with exponent."""
    source = "0e0"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "0e0,<EOF>"

def test_lexer_boundary_tabs_only():
    """Verify whitespace only."""
    source = "\t\t\t"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "<EOF>"

def test_lexer_boundary_identifier_digits():
    """Verify IDs with numbers."""
    source = "v1 v2 v3"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "v1,v2,v3,<EOF>"

def test_lexer_boundary_operator_greedy_equal():
    """Verify === is parsed as == then =."""
    source = "==="
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "==,=,<EOF>"

def test_lexer_boundary_operator_greedy_plus():
    """Verify +++ is parsed as ++ then +."""
    source = "+++"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "++,+,<EOF>"

def test_lexer_boundary_id_lookalike_keyword():
    """Verify keywords are exact matches."""
    source = "automatic break1 cases"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "automatic,break1,cases,<EOF>"

def test_lexer_boundary_string_with_quotes():
    """Verify escaped quote inside string."""
    source = '"a\\"b"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == 'a\\"b,<EOF>'

def test_lexer_boundary_block_comment_stars():
    """Verify block comments with multiple stars."""
    source = "/****/"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "<EOF>"

def test_lexer_boundary_dots_in_row():
    """Verify multiple dots."""
    source = "..."
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == ".,.,.,<EOF>"

def test_lexer_boundary_string_escaped_backslash():
    """Verify escaped backslash."""
    source = '"\\\\"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "\\\\,<EOF>"

def test_lexer_boundary_neg_exponent():
    """Verify negative exponent."""
    source = "1e-5"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "1e-5,<EOF>"

def test_lexer_boundary_leading_whitespace():
    """Verify whitespace at start."""
    source = "    id"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "id,<EOF>"

def test_lexer_boundary_trailing_whitespace():
    """Verify whitespace at end."""
    source = "id    "
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "id,<EOF>"
    

# --- Complex ---

def test_lexer_complex_string_escapes():
    """Verify all valid escape sequences."""
    source = '"\\b\\f\\n\\r\\t\\\\" '
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "\\b\\f\\n\\r\\t\\\\,<EOF>"

def test_lexer_complex_logic_expression():
    """Verify complex logic string."""
    source = "(!a && b) || (c != d)"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "(,!,a,&&,b,),||,(,c,!=,d,),<EOF>"

def test_lexer_complex_float_scientific():
    """Verify complex scientific floats."""
    source = "1.23e+10 .5E-2 10.e5"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "1.23e+10,.5E-2,10.e5,<EOF>"

def test_lexer_complex_nested_comments():
    """Verify that comments don't nest (standard C style)."""
    source = "/* comment // nested line */ id"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "id,<EOF>"

def test_lexer_complex_comment_ends_with_star():
    """Verify block comment star handling."""
    source = "/* comment **/ id"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "id,<EOF>"

def test_lexer_complex_tight_loop():
    """Verify for loop header without spaces."""
    source = "for(int i=0;i<10;i++)"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "for,(,int,i,=,0,;,i,<,10,;,i,++,),<EOF>"

def test_lexer_complex_struct_init():
    """Verify struct initialization tokens."""
    source = "p = {1, 2.5, \"ok\"};"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "p,=,{,1,,,2.5,,,ok,},;,<EOF>"

def test_lexer_complex_mixed_math():
    """Verify arithmetic precedence string."""
    source = "a*b+c/d-e%f"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "a,*,b,+,c,/,d,-,e,%,f,<EOF>"

def test_lexer_complex_id_starting_with_keyword():
    """Verify identifiers starting with keyword names."""
    source = "if_condition for_each while_loop"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "if_condition,for_each,while_loop,<EOF>"

def test_lexer_complex_multiple_newlines_in_string():
    """Verify string literal ignores escaped n as a real newline."""
    source = '"line1\\nline2"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "line1\\nline2,<EOF>"

def test_lexer_complex_logic_not_equal():
    """Verify difference between ! and !=."""
    source = "!x != y"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "!,x,!=,y,<EOF>"

def test_lexer_complex_postfix_on_member():
    """Verify member access with increment."""
    source = "p.x++"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "p,.,x,++,<EOF>"

def test_lexer_complex_scientific_capital_e():
    """Verify capital E in scientific."""
    source = "10E10"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "10E10,<EOF>"

def test_lexer_complex_slash_star_division():
    """Verify division and multiply without space isn't a comment."""
    source = "x / *y"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "x,/,*,y,<EOF>"

def test_lexer_complex_string_with_tab():
    """Verify string with literal tab representation."""
    source = '"a\\tb"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "a\\tb,<EOF>"

def test_lexer_complex_long_expression():
    """Verify long assignment."""
    source = "result = (a + b) * (c - d) / e;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "result,=,(,a,+,b,),*,(,c,-,d,),/,e,;,<EOF>"

def test_lexer_complex_nested_parens():
    """Verify many parens."""
    source = "((((x))))"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "(,(,(,(,x,),),),),<EOF>"

def test_lexer_complex_return_literal():
    """Verify return with string literal."""
    source = "return \"done\";"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "return,done,;,<EOF>"

def test_lexer_complex_many_operators():
    """Verify operators sequence."""
    source = "+ - * / % < > <= >= == != && || ! = ++ -- . ( ) { } [ ] ; , :"
    tokenizer = Tokenizer(source)
    # Just verifying they all lex individually
    assert len(tokenizer.get_tokens_as_string().split(",")) == 29

def test_lexer_complex_auto_var_init():
    """Verify auto decl."""
    source = "auto i = 0;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "auto,i,=,0,;,<EOF>"

def test_lexer_complex_string_with_all_escapes():
    source = '"\\b\\f\\n\\r\\t\\"\\\\"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == '\\b\\f\\n\\r\\t\\"\\\\,<EOF>'

def test_lexer_complex_dot_digit_ambiguity():
    """Verify .5 vs 0.5."""
    source = ".5 0.5"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == ".5,0.5,<EOF>"

def test_lexer_complex_underscore_id():
    source = "_123_abc"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "_123_abc,<EOF>"

def test_lexer_complex_unary_minus():
    source = "x = -5;"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "x,=,-,5,;,<EOF>"

def test_lexer_complex_math_tight():
    source = "1+2-3*4/5"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "1,+,2,-,3,*,4,/,5,<EOF>"

def test_lexer_complex_string_with_quote_mark():
    source = '"\'"'
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "',<EOF>"

def test_lexer_complex_empty_loop():
    source = "while(1){}"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "while,(,1,),{,},<EOF>"

def test_lexer_complex_bracket_access():
    source = "a[i]"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "a,[,i,],<EOF>"

def test_lexer_complex_multi_comma():
    source = "1, 2, 3"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "1,,,2,,,3,<EOF>"

def test_lexer_complex_comment_at_eof():
    source = "int x; // end"
    tokenizer = Tokenizer(source)
    assert tokenizer.get_tokens_as_string() == "int,x,;,<EOF>"
    

# --- Error ---

def test_lexer_error_unclosed_string():
    """Verify unclosed string error."""
    source = '"unclosed'
    tokenizer = Tokenizer(source)
    # The emit raises UncloseString("\"unclosed")
    assert 'Unclosed String' in tokenizer.get_tokens_as_string()

def test_lexer_error_unclosed_string_newline():
    """Verify string cannot contain raw newline."""
    source = '"line1\n"'
    tokenizer = Tokenizer(source)
    assert 'Unclosed String' in tokenizer.get_tokens_as_string()

def test_lexer_error_illegal_escape():
    """Verify bad escape sequence."""
    source = '"\\z"'
    tokenizer = Tokenizer(source)
    assert 'Illegal Escape' in tokenizer.get_tokens_as_string()

def test_lexer_error_illegal_escape_numeric():
    source = '"\\123"'
    tokenizer = Tokenizer(source)
    assert 'Illegal Escape' in tokenizer.get_tokens_as_string()

def test_lexer_error_invalid_char_at():
    """Verify illegal character @."""
    source = "@"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_invalid_char_hash():
    """Verify illegal character #."""
    source = "#"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_invalid_char_dollar():
    """Verify illegal character $."""
    source = "$"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_ampersand_single():
    """Verify single & is illegal (must be &&)."""
    source = "&"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_pipe_single():
    """Verify single | is illegal (must be ||)."""
    source = "|"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_question_mark():
    """Verify illegal character ?."""
    source = "?"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_unclosed_string_with_escape():
    """Verify unclosed string ending in escape."""
    source = '"test\\'
    tokenizer = Tokenizer(source)
    assert 'Unclosed String' in tokenizer.get_tokens_as_string()

def test_lexer_error_illegal_escape_at_end():
    source = '"bad\\y"'
    tokenizer = Tokenizer(source)
    assert 'Illegal Escape' in tokenizer.get_tokens_as_string()

def test_lexer_error_stray_backtick():
    source = "`"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_illegal_char_binary():
    source = "\x01"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_mixed_valid_and_invalid():
    source = "int x = @;"
    tokenizer = Tokenizer(source)
    # Tokenizer appends error to list if tokens exist
    assert "int,x,=,Error Token @" in tokenizer.get_tokens_as_string()

def test_lexer_error_unclosed_string_eof():
    source = '"'
    tokenizer = Tokenizer(source)
    assert 'Error Token' in tokenizer.get_tokens_as_string()

def test_lexer_error_illegal_escape_space():
    source = '"\\ "'
    tokenizer = Tokenizer(source)
    assert 'Illegal Escape ' in tokenizer.get_tokens_as_string()

def test_lexer_error_illegal_escape_tab():
    # A literal tab after backslash is illegal
    source = '"\\\t"'
    tokenizer = Tokenizer(source)
    assert 'Illegal Escape' in tokenizer.get_tokens_as_string()

def test_lexer_error_invalid_char_tilde():
    source = "~"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()

def test_lexer_error_invalid_char_caret():
    source = "^"
    tokenizer = Tokenizer(source)
    assert "Error Token" in tokenizer.get_tokens_as_string()
"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


def test_lexer_placeholder():
    """Placeholder test - replace with actual test cases"""
    source = "// This is a placeholder test"
    tokenizer = Tokenizer(source)
    # TODO: Add actual test assertions
    assert True

# --- Happy path ---

def test_lexer_keywords_set1():
    tokenizer = Tokenizer("auto break case continue default else float for")
    expected = "AUTO,auto,BREAK,break,CASE,case,CONTINUE,continue,DEFAULT,default,ELSE,else,FLOAT,float,FOR,for,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_keywords_set2():
    tokenizer = Tokenizer("if int return string struct switch void while")
    expected = "IF,if,INT,int,RETURN,return,STRING,string,STRUCT,struct,SWITCH,switch,VOID,void,WHILE,while,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_identifiers():
    tokenizer = Tokenizer("var_name var123 _temp internalVar")
    expected = "ID,var_name,ID,var123,ID,_temp,ID,internalVar,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_integers():
    tokenizer = Tokenizer("0 1 999 42")
    expected = "INT_LITERAL,0,INT_LITERAL,1,INT_LITERAL,999,INT_LITERAL,42,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_floats_simple():
    tokenizer = Tokenizer("3.14 0.5 .5 10.")
    expected = "FLOAT_LITERAL,3.14,FLOAT_LITERAL,0.5,FLOAT_LITERAL,.5,FLOAT_LITERAL,10.,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_floats_scientific():
    tokenizer = Tokenizer("1e10 1.5E-2 .2e+5")
    expected = "FLOAT_LITERAL,1e10,FLOAT_LITERAL,1.5E-2,FLOAT_LITERAL,.2e+5,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_strings_basic():
    tokenizer = Tokenizer('"hello" "world123"')
    # Note: Your emit() slices [1:-1], so we expect the inner text
    expected = "STRING_LITERAL,hello,STRING_LITERAL,world123,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_arithmetic():
    tokenizer = Tokenizer("+ - * / %")
    expected = "PLUS,+,MINUS,-,MUL,*,DIV,/,MOD,%,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_comparisons():
    tokenizer = Tokenizer("< > <= >= == !=")
    expected = "LT,<,GT,>,LE,<=,GE,>=,EQUAL,==,NOTEQUAL,!=,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_logical_and_inc():
    tokenizer = Tokenizer("&& || ! ++ --")
    expected = "AND,&&,OR,||,BANG,!,INC,++,DEC,--,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_separators():
    tokenizer = Tokenizer("( ) { } [ ] ; , : . =")
    expected = "LPAREN,(,RPAREN,),LBRACE,{,RBRACE,},LBRACK,[,RBRACK,],SEMI,;,COMMA,,,COLON,:,DOT,.,ASSIGN,=,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_mixed_declaration():
    tokenizer = Tokenizer("int x = 10;")
    expected = "INT,int,ID,x,ASSIGN,=,INT_LITERAL,10,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_mixed_float_decl():
    tokenizer = Tokenizer("float f = .25;")
    expected = "FLOAT,float,ID,f,ASSIGN,=,FLOAT_LITERAL,.25,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_struct_keyword():
    tokenizer = Tokenizer("struct MyStruct { };")
    expected = "STRUCT,struct,ID,MyStruct,LBRACE,{,RBRACE,},SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_return_void():
    tokenizer = Tokenizer("void func() { return; }")
    expected = "VOID,void,ID,func,LPAREN,(,RPAREN,),LBRACE,{,RETURN,return,SEMI,;,RBRACE,},EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_string_escapes_happy():
    tokenizer = Tokenizer('"\\n\\t\\""')
    expected = "STRING_LITERAL,\\n\\t\\\",EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_large_int():
    tokenizer = Tokenizer("2147483647")
    expected = "INT_LITERAL,2147483647,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_single_char_id():
    tokenizer = Tokenizer("a b c")
    expected = "ID,a,ID,b,ID,c,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_underscore_start():
    tokenizer = Tokenizer("_var")
    expected = "ID,_var,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_multi_line_ws():
    tokenizer = Tokenizer("int\n\nx\t=\r5;")
    expected = "INT,int,ID,x,ASSIGN,=,INT_LITERAL,5,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_comments_skipped():
    tokenizer = Tokenizer("int x; // comment\n float y; /* block */")
    expected = "INT,int,ID,x,SEMI,;,FLOAT,float,ID,y,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_bool_logic_mix():
    tokenizer = Tokenizer("a && b || !c")
    expected = "ID,a,AND,&&,ID,b,OR,||,BANG,!,ID,c,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_struct_access():
    tokenizer = Tokenizer("point.x = 5;")
    expected = "ID,point,DOT,.,ID,x,ASSIGN,=,INT_LITERAL,5,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_brackets():
    tokenizer = Tokenizer("arr[0]")
    expected = "ID,arr,LBRACK,[,INT_LITERAL,0,RBRACK,],EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_for_loop_header():
    tokenizer = Tokenizer("for(int i=0;i<10;i++)")
    expected = "FOR,for,LPAREN,(,INT,int,ID,i,ASSIGN,=,INT_LITERAL,0,SEMI,;,ID,i,LT,<,INT_LITERAL,10,SEMI,;,ID,i,INC,++,RPAREN,),EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_scientific_caps():
    tokenizer = Tokenizer("1.2E5")
    expected = "FLOAT_LITERAL,1.2E5,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_string_with_space():
    tokenizer = Tokenizer('"string with spaces"')
    expected = "STRING_LITERAL,string with spaces,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_nested_comment_chars():
    tokenizer = Tokenizer("int x; /* // not a line comment */")
    expected = "INT,int,ID,x,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_zero_float():
    tokenizer = Tokenizer("0.0")
    expected = "FLOAT_LITERAL,0.0,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_auto_keyword():
    tokenizer = Tokenizer("auto result = 5.5;")
    expected = "AUTO,auto,ID,result,ASSIGN,=,FLOAT_LITERAL,5.5,SEMI,;,EOF"
    assert tokenizer.get_tokens_as_string() == expected
    

# --- Boundary Cases ---
def test_lexer_empty_input():
    tokenizer = Tokenizer("")
    assert tokenizer.get_tokens_as_string() == "EOF"

def test_lexer_single_zero():
    tokenizer = Tokenizer("0")
    assert tokenizer.get_tokens_as_string() == "INT_LITERAL,0,EOF"

def test_lexer_minimal_float():
    tokenizer = Tokenizer(".0")
    assert tokenizer.get_tokens_as_string() == "FLOAT_LITERAL,.0,EOF"

def test_lexer_minimal_id():
    tokenizer = Tokenizer("_")
    assert tokenizer.get_tokens_as_string() == "ID,_,EOF"

def test_lexer_max_whitespace():
    tokenizer = Tokenizer(" \n \r \t \f ")
    assert tokenizer.get_tokens_as_string() == "EOF"

def test_lexer_trailing_dot_float():
    tokenizer = Tokenizer("123.")
    assert tokenizer.get_tokens_as_string() == "FLOAT_LITERAL,123.,EOF"

def test_lexer_leading_dot_float():
    tokenizer = Tokenizer(".123")
    assert tokenizer.get_tokens_as_string() == "FLOAT_LITERAL,.123,EOF"

def test_lexer_empty_string_literal():
    tokenizer = Tokenizer('""')
    assert tokenizer.get_tokens_as_string() == "STRING_LITERAL,,EOF"

def test_lexer_string_only_escapes():
    tokenizer = Tokenizer('"\\n\\n"')
    assert tokenizer.get_tokens_as_string() == "STRING_LITERAL,\\n\\n,EOF"

def test_lexer_int_at_boundary():
    # 0 followed by 1 should be two tokens because INT_LITERAL doesn't allow leading zeros for multi-digits
    tokenizer = Tokenizer("01")
    assert tokenizer.get_tokens_as_string() == "INT_LITERAL,0,INT_LITERAL,1,EOF"

def test_lexer_long_identifier():
    long_id = "a" * 100
    tokenizer = Tokenizer(long_id)
    assert tokenizer.get_tokens_as_string() == f"ID,{long_id},EOF"

def test_lexer_all_operators_no_space():
    tokenizer = Tokenizer("++--==!=<=>=&&||")
    expected = "INC,++,DEC,--,EQUAL,==,NOTEQUAL,!=,LE,<=,GE,>=,AND,&&,OR,||,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_dot_vs_float():
    tokenizer = Tokenizer("0. .0")
    assert tokenizer.get_tokens_as_string() == "FLOAT_LITERAL,0.,FLOAT_LITERAL,.0,EOF"

def test_lexer_block_comment_unclosed_star():
    # Should skip everything until closing
    tokenizer = Tokenizer("/* **** */")
    assert tokenizer.get_tokens_as_string() == "EOF"

def test_lexer_newline_in_ws():
    tokenizer = Tokenizer("\n\n\n")
    assert tokenizer.get_tokens_as_string() == "EOF"

def test_lexer_many_semicolons():
    tokenizer = Tokenizer(";;;")
    assert tokenizer.get_tokens_as_string() == "SEMI,;,SEMI,;,SEMI,;,EOF"

def test_lexer_id_with_numbers():
    tokenizer = Tokenizer("a123b456")
    assert tokenizer.get_tokens_as_string() == "ID,a123b456,EOF"

def test_lexer_id_starting_with_keyword():
    tokenizer = Tokenizer("autofill")
    assert tokenizer.get_tokens_as_string() == "ID,autofill,EOF"

def test_lexer_float_scientific_no_decimal():
    tokenizer = Tokenizer("10e5")
    assert tokenizer.get_tokens_as_string() == "FLOAT_LITERAL,10e5,EOF"

def test_lexer_string_with_single_quotes():
    tokenizer = Tokenizer("\"'quoted'\"")
    assert tokenizer.get_tokens_as_string() == "STRING_LITERAL,'quoted',EOF"
    

# --- Complex ---
def test_lexer_complex_expression():
    tokenizer = Tokenizer("x=(y++)+(--z)")
    expected = "ID,x,ASSIGN,=,LPAREN,(,ID,y,INC,++,RPAREN,),PLUS,+,LPAREN,(,DEC,--,ID,z,RPAREN,),EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_nested_struct_access():
    tokenizer = Tokenizer("a.b.c.d")
    expected = "ID,a,DOT,.,ID,b,DOT,.,ID,c,DOT,.,ID,d,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_string_escaped_backslash():
    tokenizer = Tokenizer('"\\\\"') # Literal double backslash in source
    expected = "STRING_LITERAL,\\\\,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_greedy_matching_operators():
    tokenizer = Tokenizer("===!=====")
    expected = "EQUAL,==,ASSIGN,=,NOTEQUAL,!=,EQUAL,==,EQUAL,==,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_greedy_plus():
    tokenizer = Tokenizer("+++")
    expected = "INC,++,PLUS,+,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_comment_between_tokens():
    tokenizer = Tokenizer("int/*comment*/x")
    expected = "INT,int,ID,x,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_float_exponent_sign():
    tokenizer = Tokenizer("1.2e+10 1.2e-10")
    expected = "FLOAT_LITERAL,1.2e+10,FLOAT_LITERAL,1.2e-10,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_mixed_ids_and_keywords():
    tokenizer = Tokenizer("for for1 for_ for_1")
    expected = "FOR,for,ID,for1,ID,for_,ID,for_1,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_string_with_various_escapes():
    tokenizer = Tokenizer('"\\b\\f\\n\\r\\t\\\\\\""')
    expected = "STRING_LITERAL,\\b\\f\\n\\r\\t\\\\\\\",EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_scientific_without_dot():
    tokenizer = Tokenizer("1E10")
    expected = "FLOAT_LITERAL,1E10,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_unary_and_binary():
    tokenizer = Tokenizer("-5 - -10")
    expected = "MINUS,-,INT_LITERAL,5,MINUS,-,MINUS,-,INT_LITERAL,10,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_not_equal_vs_bang():
    tokenizer = Tokenizer("!= !")
    expected = "NOTEQUAL,!=,BANG,!,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_string_newline_as_chars():
    # If the user literally types backslash n, it's valid.
    tokenizer = Tokenizer('"Line1\\nLine2"')
    expected = "STRING_LITERAL,Line1\\nLine2,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_division_vs_comment():
    tokenizer = Tokenizer("10 / 5 // comment")
    expected = "INT_LITERAL,10,DIV,/,INT_LITERAL,5,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_dot_accessor_on_float():
    tokenizer = Tokenizer("1.5.member")
    expected = "FLOAT_LITERAL,1.5,DOT,.,ID,member,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_logic_grouping_tokens():
    tokenizer = Tokenizer("(a&&b)||(!c)")
    expected = "LPAREN,(,ID,a,AND,&&,ID,b,RPAREN,),OR,||,LPAREN,(,BANG,!,ID,c,RPAREN,),EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_multiline_block_comment():
    tokenizer = Tokenizer("/* line 1\n line 2\n line 3 */")
    assert tokenizer.get_tokens_as_string() == "EOF"

def test_lexer_id_trailing_underscore():
    tokenizer = Tokenizer("my_id_")
    assert tokenizer.get_tokens_as_string() == "ID,my_id_,EOF"

def test_lexer_arithmetic_precedence_tokens():
    tokenizer = Tokenizer("a+b*c")
    expected = "ID,a,PLUS,+,ID,b,MUL,*,ID,c,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_float_with_no_int_part():
    tokenizer = Tokenizer(".00001")
    assert tokenizer.get_tokens_as_string() == "FLOAT_LITERAL,.00001,EOF"

def test_lexer_slash_followed_by_id():
    tokenizer = Tokenizer("10/count")
    expected = "INT_LITERAL,10,DIV,/,ID,count,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_multiple_unary():
    tokenizer = Tokenizer("!!x")
    expected = "BANG,!,BANG,!,ID,x,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_assign_vs_equal():
    tokenizer = Tokenizer("x == y = z")
    expected = "ID,x,EQUAL,==,ID,y,ASSIGN,=,ID,z,EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_complex_path_id():
    tokenizer = Tokenizer("path_to_file_123")
    assert tokenizer.get_tokens_as_string() == "ID,path_to_file_123,EOF"

def test_lexer_struct_init_tokens():
    tokenizer = Tokenizer("{1, 2.5, \"str\"}")
    expected = "LBRACE,{,INT_LITERAL,1,COMMA,,,FLOAT_LITERAL,2.5,COMMA,,,STRING_LITERAL,str,RBRACE,},EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_nested_paren_math():
    tokenizer = Tokenizer("((1+2)*3)")
    expected = "LPAREN,(,LPAREN,(,INT_LITERAL,1,PLUS,+,INT_LITERAL,2,RPAREN,),MUL,*,INT_LITERAL,3,RPAREN,),EOF"
    assert tokenizer.get_tokens_as_string() == expected

def test_lexer_all_keywords_tight():
    tokenizer = Tokenizer("intfloatstringstruct")
    # This should be one ID, not 4 keywords
    assert tokenizer.get_tokens_as_string() == "ID,intfloatstringstruct,EOF"

def test_lexer_trailing_ws():
    tokenizer = Tokenizer("if ")
    assert tokenizer.get_tokens_as_string() == "IF,if,EOF"

def test_lexer_internal_ws():
    tokenizer = Tokenizer("i f")
    assert tokenizer.get_tokens_as_string() == "ID,i,ID,f,EOF"

def test_lexer_comment_at_end():
    tokenizer = Tokenizer("return; // end")
    assert tokenizer.get_tokens_as_string() == "RETURN,return,SEMI,;,EOF"
    

# --- Error ---
import pytest
from lexererr import UncloseString, IllegalEscape, ErrorToken

def test_lexer_error_unclosed_string_eof():
    with pytest.raises(UncloseString):
        Tokenizer('"unclosed string').get_tokens_as_string()

def test_lexer_error_unclosed_string_newline():
    with pytest.raises(UncloseString):
        Tokenizer('"string\n"').get_tokens_as_string()

def test_lexer_error_illegal_escape_z():
    with pytest.raises(IllegalEscape):
        Tokenizer('"\\z"').get_tokens_as_string()

def test_lexer_error_illegal_escape_space():
    with pytest.raises(IllegalEscape):
        Tokenizer('"\\ "').get_tokens_as_string()

def test_lexer_error_illegal_char_at():
    with pytest.raises(ErrorToken):
        Tokenizer('@').get_tokens_as_string()

def test_lexer_error_illegal_char_hash():
    with pytest.raises(ErrorToken):
        Tokenizer('#').get_tokens_as_string()

def test_lexer_error_illegal_char_dollar():
    with pytest.raises(ErrorToken):
        Tokenizer('$').get_tokens_as_string()

def test_lexer_error_illegal_char_ampersand_single():
    # Only && is valid
    with pytest.raises(ErrorToken):
        Tokenizer('a & b').get_tokens_as_string()

def test_lexer_error_illegal_char_pipe_single():
    # Only || is valid
    with pytest.raises(ErrorToken):
        Tokenizer('a | b').get_tokens_as_string()

def test_lexer_error_unclosed_string_escaped_quote():
    # The backslash escapes the second quote, leaving it unclosed
    with pytest.raises(UncloseString):
        Tokenizer('"escape \\"').get_tokens_as_string()

def test_lexer_error_illegal_escape_numeric():
    with pytest.raises(IllegalEscape):
        Tokenizer('"\\123"').get_tokens_as_string()

def test_lexer_error_illegal_char_backtick():
    with pytest.raises(ErrorToken):
        Tokenizer('`').get_tokens_as_string()

def test_lexer_error_illegal_escape_question():
    with pytest.raises(IllegalEscape):
        Tokenizer('"\\?"').get_tokens_as_string()

def test_lexer_error_illegal_char_tilde():
    with pytest.raises(ErrorToken):
        Tokenizer('~').get_tokens_as_string()

def test_lexer_error_illegal_char_percent_in_id():
    # MOD is valid alone, but identifiers can't contain %
    tokenizer = Tokenizer("var%name")
    # This will actually result in ID,var,MOD,%,ID,name,EOF - not an error.
    # To test ERROR_CHAR, we need a char not in any rule.
    with pytest.raises(ErrorToken):
        Tokenizer('\x01').get_tokens_as_string()

def test_lexer_error_unclosed_string_complex():
    with pytest.raises(UncloseString):
        Tokenizer('"valid part \\n valid part...').get_tokens_as_string()

def test_lexer_error_illegal_escape_at_end():
    with pytest.raises(IllegalEscape):
        Tokenizer('"bad escape \\y"').get_tokens_as_string()

def test_lexer_error_broken_logic_token():
    with pytest.raises(ErrorToken):
        Tokenizer('&').get_tokens_as_string()

def test_lexer_error_stray_question_mark():
    with pytest.raises(ErrorToken):
        Tokenizer('?').get_tokens_as_string()

def test_lexer_error_mixed_illegal_chars():
    with pytest.raises(ErrorToken):
        Tokenizer('int x = 5 @ 10;').get_tokens_as_string()
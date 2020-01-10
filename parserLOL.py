import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_programme_statement(p):
    ''' programme : statement'''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)

def p_statement(p):
    ''' statement : assignation
        | expression
        | structure'''
    p[0] = p[1]

def p_commentary(p):
    ''' comment : statement SL_COMMENT
    | statement ML_COMMENT'''
    p[0] = AST.CommentNode([p[1],AST.StringNode(p[2])])

def p_commentary_alone(p):
    '''comment : SL_COMMENT
    | ML_COMMENT'''
    p[0] = AST.CommentNode(AST.StringNode(p[1]))

def p_expression(p):
    '''expression : expression_num
    | expression_bool'''
    p[0] = p[1]

def p_expression_op(p):
    '''expression_num : ADD_OP expression_num AN expression_num 
            | MUL_OP expression_num AN expression_num
            | MOD_OP expression_num AN expression_num
            | MAX_OP expression_num AN expression_num
            | MIN_OP expression_num AN expression_num'''
    p[0] = AST.OpNode(p[1], [p[2], p[4]])

def p_increment_op(p):
    '''expression_num : INC_OP expression_num'''
    p[0] = AST.IncOpNode(p[1], [p[2]])
    	
def p_expression_num_or_var(p):
    '''expression_num : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_expression_bool(p):
    '''expression_bool : BOOL'''
    p[0] = AST.TokenNode(p[1])

def p_bool_op(p):
    '''expression_bool : BOOL_OP expression_bool AN expression_bool'''
    p[0] = AST.BoolOpNode(p[1], [p[2], p[4]])

def p_bool_not(p):
    '''expression_bool : NOT expression_bool'''
    p[0] = AST.BoolOpNode(p[1], [p[2]])

def p_comp(p):
    '''expression_bool : COMP expression AN expression'''
    p[0] = AST.CompNode(p[1], [p[2],p[4]])
    		
def p_declaration(p):
    ''' assignation : DECLARATION IDENTIFIER ASSIGNEMENT_DECL expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[2]),p[4]])

def p_assign(p):
    ''' assignation : IDENTIFIER ASSIGNEMENT_SIMPLE expression'''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_newLine(p):
    ''' new_line : NL'''
    p[0] = AST.NlNode(p[1])

def p_while(p):
    ''' structure : WHILE expression_bool programme END_LOOP'''
    p[0] = AST.WhileNode([p[2],p[3]])  

def p_for(p):
    ''' structure : FOR expression_num TIL expression_num programme END_LOOP'''
    p[0] = AST.ForNode(p[1],[p[2],p[4], p[5]])

def p_if(p):
    ''' structure : expression_bool COMP IF IF_TRUE programme IF_END '''
    p[0] = AST.IfNode([p[1],p[5]])

def p_ifElse(p):
    ''' structure : expression_bool COMP IF IF_TRUE programme IF_FALSE programme IF_END'''
    p[0] = AST.IfNode([p[1],p[5], p[7]])


def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Syntax error: unexpected end of file!")


def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)
            
        import os
        os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
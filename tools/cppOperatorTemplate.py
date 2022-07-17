import enum
import optparse
import sys
import os
import pathlib
import foo
import abc
from typing import *

COMP_ARG_LIST = ['==', '!=', '<=', '>=', '<', '>']
DEFAULT_ARG_LIST = COMP_ARG_LIST + ['()', '[]']
ARITH_ARG_LIST = ['+', '-', '*', '-']
INCR_ARG_LIST = ['++', '--']
ASSIGN_ARG_LIST = ['=', '+=', '-=', '*=', '/=', '%=']
ACCESS_ARG_LIST = ['[]', '->', '->*']
CALL_ARG_LIST = ['()']
INIT_DEL_ARG_LIST = ['new', 'delete', 'new []', 'delete []']
ALL = COMP_ARG_LIST + ARITH_ARG_LIST + INIT_DEL_ARG_LIST + ACCESS_ARG_LIST + ASSIGN_ARG_LIST + CALL_ARG_LIST + INCR_ARG_LIST +

"""
This is a handy extension of python's Enum class that
allows for lists, membership checking by value and some other
useful functions 

I've been carrying this around over the years, hopefully at
some point I'll take the time to collect/formalize/polish
all of the python tidbits I've been dragging around into
a single module
"""
class StrEnumOperatorMeta(enum.EnumMeta):
    def __contains__(cls, other):
        if isinstance(str):
            return other in list(map(lambda x: x.value, cls))

        else:
            return other in list(map(lambda x: x, cls))

    def __eq__(self, other):
        if isinstance(str):
            return self.value == other

        else:
            return self.name == other

class Operators():
    EQUAL = '==',
    NOT_EQUAL = '!=',
    GREATER = ">",
    LESS = "<",
    GREATER_EQ = ">=",
    LESS_EQ = "<=",
    ADD = "+",
    SUB = "-",
    MULT = "*",
    DIV = "/",
    INCR = "++",
    DECR = "--",
    ASSIGN = "=",
    ADD_ASGN = "+=",
    SUB_ASGN = "-=",
    MUL_ASGN = "*=",
    DIV_ASGN = "/=",
    MOD_ASGN = "%=",
    BRACKET = '[]',
    ARROW = "->",
    STAR_ARROW = "->*",
    CALL = "()",
    NEW = "new",
    DELETE = "delete",
    NEW_BRK = "new []",
    DELETE_BRK = "delete []"

# why not make a class :shrug:
class CPPOperator:
    def __init__(self):


def errmsg(msg: str,
           newline: bool = True,
           exit: bool = True,
           exit_code: int = -1,
           usage_message: Optional[AnyStr] = None):


    sys.stderr.write(msg + os.linesep if newline else msg)

    if usage_message:
        sys.stderr.write(os.linesep + usage_message)

    if exit:
        sys.exit(exit_code)

def file_callback(opt: optparse.Option,
                  opt_str: str,
                  val: Any,
                  parser: optparse.OptionParser):

    # TODO: is it better to overwite the arg or add a new variable via an option
    if val == '-':
        parser.values.output_file = sys.stdout

    else:
        file_path = pathlib.Path(val)
        if not file_path.is_file():
            errmsg(f"ERROR: {val} is not a file", usage_message=parser.get_usage())

        try:
            parser.values.output_file = open(val, 'w')

        except FileNotFoundError as e:
            errmsg(f"ERROR: Unable to open {val}", usage_message=parser.get_usage())

def get_opts() -> optparse.OptionParser:
    desc = """
    A quick tool to generate operator signatures for C++ classes
    I'm sure there's IDEs that do this for you but where's the fun in that ;)
    """
    ret = optparse.OptionParser(description=desc)

    # TODO: figure out why this is even an option, is this a posix thing?
    # default is to allow positional arguments to be interspersed between switches
    ret.disable_interspersed_args()

    op_grp = optparse.OptionGroup(ret,
                                 "Operator Selection Options",
                                 "These switches allow for specification of which operators to generate"
                                 "The default (no switches provided) is ==, !=, <=, >=, <, >, (), []")
    base_grp = optparse.OptionGroup(ret, "Primary arguments")
    exp_grp = optparse.OptionParser(ret,
                                    "Experimental options",
                                    "These options may generate invalid C++ code or not function as expected, glhf")

    ret.add_option_group(op_grp)
    ret.add_option_group(base_grp)
    ret.add_option_group(exp_grp)

    base_grp.add_option("-c", "--class",
                        dest="class_name",
                        help="Name of class to which the operators belong")

    base_grp.add_option("-t", "--type",
                        dest="arg_type",
                        help="Type of argument, default is class name (with namespace if provided)")

    base_grp.add_option("-a", "--arg",
                        dest="arg_name",
                        default="cmp",
                        help="Name of argument in signature, default is 'cmp'")

    base_grp.add_option("-n", "--namespace",
                        dest="namespace",
                        help="Namespace to add to signatures")

    base_grp.add_option("-o", "--output_file",
                        dest="output_file",
                        help="Name of output file (otherwise output is to stdout",
                        callback=file_callback)

    op_grp.add_option("--comparators",
                      dest="comps",
                      default=False,
                      help="Only generate comparators (can be used in combination with other switches)")

    op_grp.add_option("--arithmatic",
                      dest="arith",
                      default=False,
                      action="store",
                      help="Only generate arithmatic operators (can be used in combination with other switches)")

    op_grp.add_option("--increment",
                      dest="increment_only",
                      default=False,
                      action="store",
                      help="Only generate in/decrement operators (can be used in combination with other switches)")

    op_grp.add_option("--assignment",
                      dest="assign",
                      default=False,
                      action="store_true",
                      help="Only generator assignment operators (can be used in combination with other switches)")

    op_grp.add_option("--access",
                      dest="access",
                      default=False,
                      action="store_true",
                      help="Only generator accessor operators (can be used in combination with other switches)")

    op_grp.add_option("--call",
                      dest="call",
                      default=False,
                      action="store_true",
                      help="Only generator call operator (can be used in combination with other switches)")

    op_grp.add_option("--initialize",
                      dest="init",
                      default=False,
                      action="store_true",
                      help="Only generate (de)initializer operators (can be used in combination with other switches)")

    op_grp.add_option("--all",
                     dest="all",
                     default=False,
                     action="store_true",
                     help="Generate all operators (other operator selection switches will be ignored")

    exp_grp.add_option("--arg_map",
                       dest="arg_map",
                       help="Specify argument types to provide to each class of operators"
                       "The general formatting is <operator type>:type1,type2;")

    return ret


if __name__ == '__main__':
    opts = get_opts()
    vals, _ = opts.parse_args()

    if not opts.class_name:
        errmsg("ERROR: a class name must be provided")

    if not opts.arg_type:
        vals["arg_type"] = [opts.class_name]

    elif not opts.arg_type and opts.arg_types:
        vals["arg_type"] = opts.arg_types.split(",")


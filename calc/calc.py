import parser
import re
from sympy import solve
from math import sqrt, sin, cos, pi, fabs, e, log
import wx


def evaluate(formula, func):
    if formula == '':
        return 0
    formula = formula.replace('^', '**', formula.count("^"))
    formula = formula.replace(',', '.', formula.count(","))
    formula = formula.replace('abs', 'fabs', formula.count("abs"))
    formula = formula.replace('\u221A', 'sqrt', formula.count("\u221A"))
    exp = re.compile(r'[0-9a-fA-F.,+\-*&><|/sincoqrtpbxlg ()]+')
    for char in formula:
        if not re.match(exp, char):
            return "invalid input"

    try:
        code = parser.expr(formula).compile()
    except Exception as e:
        print(e)
        return "invalid input"

    result = eval(code)
    if func is not None:
        try:
            return func(result)
        except TypeError:
            wx.MessageBox("Float value can't be displayed as bin or hex number.\nUsing dec instead.")
    return round(result, 3)


def solve_equation(equ):
    if equ == '':
        return 'nothing here'
    equ = equ.replace('^', '**', equ.count("^"))
    equ = equ.replace(',', '.', equ.count(","))
    equ = equ.replace('\u221A', 'sqrt', equ.count("\u221A"))
    return solve(equ)

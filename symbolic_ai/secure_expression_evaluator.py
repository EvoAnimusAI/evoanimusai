# secure_expression_evaluator.py :: Evaluador simbólico seguro — Nivel militar

import ast
import operator
import datetime
import traceback

print("[INIT][SECURE_EVAL] >> Cargando módulo secure_expression_evaluator (nivel militar)")

class SecureExpressionEvaluator:
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.BitXor: operator.xor,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.And: operator.and_,
        ast.Or: operator.or_,
    }

    def __init__(self):
        print("[SECURE_EVAL][INIT] >> Evaluador seguro inicializado")

    def eval_expr(self, expr, context):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(f"[{timestamp}][SECURE_EVAL][EVAL] >> Evaluando expresión: '{expr}' con contexto: {context}")
        try:
            tree = ast.parse(expr, mode='eval')
            result = self._eval(tree.body, context)
            print(f"[{timestamp}][SECURE_EVAL][RESULT] >> Resultado: {result}")
            return result
        except Exception as e:
            print(f"[{timestamp}][SECURE_EVAL][❌ ERROR] >> Fallo crítico al evaluar expresión: {expr}")
            print(f"[SECURE_EVAL][TRACE] >> {str(e)}")
            traceback.print_exc()
            return False

    def _eval(self, node, context):
        if isinstance(node, ast.BinOp):
            left = self._eval(node.left, context)
            right = self._eval(node.right, context)
            op_type = type(node.op)
            self._audit_operator(op_type)
            return self.ALLOWED_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.Compare):
            left = self._eval(node.left, context)
            for op, comparator in zip(node.ops, node.comparators):
                op_type = type(op)
                self._audit_operator(op_type)
                right = self._eval(comparator, context)
                if not self.ALLOWED_OPERATORS[op_type](left, right):
                    return False
            return True
        elif isinstance(node, ast.Name):
            if node.id not in context:
                raise ValueError(f"[SECURE_EVAL][ERROR] Variable no definida: '{node.id}'")
            return context[node.id]
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BoolOp):
            op_type = type(node.op)
            self._audit_operator(op_type)
            values = [self._eval(v, context) for v in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        else:
            raise ValueError(f"[SECURE_EVAL][BLOCKED] Nodo no permitido: {type(node).__name__}")

    def _audit_operator(self, op_type):
        if op_type not in self.ALLOWED_OPERATORS:
            raise ValueError(f"[SECURE_EVAL][BLOCKED] Operador prohibido detectado: {op_type.__name__}")
        print(f"[SECURE_EVAL][ALLOW] >> Operador permitido: {op_type.__name__}")

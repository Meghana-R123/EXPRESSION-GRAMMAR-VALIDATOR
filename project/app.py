from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# ---------- TOKENIZER ----------
def tokenize(rhs):
    return re.findall(r"[A-Z]'+|[A-Z]|id|num|\(|\)|\+|\*|[a-z0-9]+", rhs)

# ---------- PARSER ----------
def parse_grammar(lines):
    productions = {}
    errors = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "->" not in line:
            errors.append(f"Invalid rule (missing '->'): {line}")
            continue

        lhs, rhs = line.split("->", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        # LHS validation
        if not re.match(r"^[A-Z]'+$|^[A-Z]$", lhs):
            errors.append(f"Invalid LHS '{lhs}' (must be uppercase non-terminal)")
            continue

        if rhs == "":
            errors.append(f"Empty production in '{line}'")
            continue

        parts = [r.strip() for r in rhs.split("|")]

        if lhs not in productions:
            productions[lhs] = []

        for p in parts:
            if p == "":
                errors.append(f"Empty alternative in '{line}'")
            else:
                productions[lhs].append(p)

    return productions, errors

# ---------- GENERATING ----------
def find_generating(productions):
    generating = set()
    changed = True

    while changed:
        changed = False

        for lhs, rules in productions.items():
            if lhs in generating:
                continue

            for rule in rules:
                if rule == "null":
                    generating.add(lhs)
                    changed = True
                    break

                tokens = tokenize(rule)

                if all(
                    token not in productions or token in generating
                    for token in tokens
                ):
                    generating.add(lhs)
                    changed = True
                    break

    return generating

# ---------- REACHABLE ----------
def find_reachable(productions, start):
    reachable = set()
    stack = [start]

    while stack:
        cur = stack.pop()
        if cur in reachable:
            continue

        reachable.add(cur)

        for rule in productions.get(cur, []):
            tokens = tokenize(rule)
            for t in tokens:
                if t in productions and t not in reachable:
                    stack.append(t)

    return reachable

# ---------- LEFT RECURSION ----------
def detect_left_recursion(productions):
    left_rec = set()

    for lhs, rules in productions.items():
        for rule in rules:
            tokens = tokenize(rule)
            if tokens and tokens[0] == lhs:
                left_rec.add(lhs)

    return left_rec

# ---------- VALIDATOR ----------
def validate(lines):
    productions, parse_errors = parse_grammar(lines)

    result = {
        "start": None,
        "status": "VALID",
        "details": {},
        "warnings": [],
        "errors": []
    }

    if parse_errors:
        result["status"] = "INVALID"
        result["errors"] = parse_errors
        return result

    if not productions:
        result["status"] = "INVALID"
        result["errors"] = ["No valid productions found"]
        return result

    start = next(iter(productions))
    result["start"] = start

    generating = find_generating(productions)
    reachable = find_reachable(productions, start)
    left_rec = detect_left_recursion(productions)

    # check used symbols
    used_symbols = set()
    for rules in productions.values():
        for r in rules:
            for t in tokenize(r):
                if re.match(r"[A-Z]'+|[A-Z]", t):
                    used_symbols.add(t)

    # per-rule analysis
    for nt in productions:
        issues = []

        if nt not in reachable:
            issues.append("Unreachable non-terminal")
            result["status"] = "INVALID"

        if nt not in generating:
            issues.append("Non-generating (cannot produce terminal string)")
            result["status"] = "INVALID"

        if nt in left_rec:
            issues.append("Left recursion present")

        result["details"][nt] = issues if issues else ["✓"]

    # missing production
    for sym in used_symbols:
        if sym not in productions:
            result["status"] = "INVALID"
            result["errors"].append(f"Missing production for '{sym}'")

    # warnings
    for nt in left_rec:
        result["warnings"].append(f"Left recursion in '{nt}'")

    return result

# ---------- ROUTES ----------
@app.route("/")
def home():
    return "Backend running"

@app.route("/validate", methods=["POST"])
def validate_api():
    data = request.json
    text = data.get("grammar", "")
    lines = text.split("\n")

    return jsonify(validate(lines))

if __name__ == "__main__":
    app.run(debug=True)
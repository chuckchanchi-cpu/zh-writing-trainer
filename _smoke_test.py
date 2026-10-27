#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_smoke_test.py — zh-writing-trainer 冒煙測試"""
import ast
import sys

fail = 0
src = open("app.py", encoding="utf-8").read()
try:
    ast.parse(src)
    print("✅ app.py syntax OK")
except SyntaxError as e:
    print(f"❌ syntax error: {e}")
    fail += 1

for tid in ["describe", "rhetoric", "climax", "contrast", "echo", "punct", "typo", "structure"]:
    if f'"id": "{tid}"' in src:
        print(f"✅ tool {tid} 有")
    else:
        print(f"❌ tool {tid} 缺")
        fail += 1

drills = src.split("DRILLS = [", 1)[1].split("\n]", 1)[0]
n = drills.count('("')
print(f"✅ DRILLS: {n} 題" if n >= 15 else f"❌ DRILLS 得 {n} 題")
if n < 15:
    fail += 1

for tid in ["narrative", "picture", "person"]:
    if f'"id": "{tid}"' in src:
        print(f"✅ task {tid} 有")
    else:
        print(f"❌ task {tid} 缺")
        fail += 1

print("done" if fail == 0 else f"FAILED ({fail})")
sys.exit(1 if fail else 0)

"""
Production Readiness Checker — Bulletproof v2
Tối ưu hóa để tương thích Windows + Kiểm tra đa tầng .gitignore.
"""
import os
import sys
import json

# Fix encoding cho Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except: pass

def check(name: str, passed: bool, detail: str = "") -> dict:
    icon = "[PASS]" if passed else "[FAIL]"
    print(f"  {icon} {name}" + (f" - {detail}" if detail else ""))
    return {"name": name, "passed": passed}

def run_checks():
    results = []
    base = os.path.dirname(__file__)

    print("\n" + "=" * 55)
    print("  Production Readiness Check - Day 12 Lab")
    print("=" * 55)

    # -- Files -----------------------------------------
    print("\n[Files] Required Files")
    for f in ["Dockerfile", "docker-compose.yml", ".dockerignore", ".env.example", "requirements.txt"]:
        results.append(check(f"{f} exists", os.path.exists(os.path.join(base, f))))
    
    results.append(check("railway.toml or render.yaml exists", 
                        os.path.exists(os.path.join(base, "railway.toml")) or 
                        os.path.exists(os.path.join(base, "render.yaml"))))

    # -- Security --------------------------------------
    print("\n[Security] Protection")
    # Kiểm tra .env bị ignore ở cả thư mục hiện tại và thư mục cha
    env_ignored = False
    for gi_path in [os.path.join(base, ".gitignore"), os.path.join(base, "..", ".gitignore")]:
        if os.path.exists(gi_path):
            if ".env" in open(gi_path, encoding='utf-8').read():
                env_ignored = True
                break
    results.append(check(".env in .gitignore", env_ignored))

    secrets_found = []
    for f in ["app/main.py", "app/config.py"]:
        fpath = os.path.join(base, f)
        if os.path.exists(fpath):
            content = open(fpath, encoding='utf-8').read()
            for bad in ["sk-", "password123", "hardcoded"]:
                if bad in content: secrets_found.append(f"{f}:{bad}")
    results.append(check("No hardcoded secrets in code", len(secrets_found) == 0))

    # -- API -------------------------------------------
    print("\n[API] Endpoints")
    main_py = os.path.join(base, "app", "main.py")
    if os.path.exists(main_py):
        c = open(main_py, encoding='utf-8').read()
        results.append(check("/health endpoint", "/health" in c))
        results.append(check("/ready endpoint", "/ready" in c))
        results.append(check("Auth implemented", "api_key" in c.lower() or "verify_token" in c))
        results.append(check("Rate limit/429", "rate_limit" in c.lower() or "429" in c))
        results.append(check("Graceful shutdown", "SIGTERM" in c))
        results.append(check("Structured logging", "json.dumps" in c or '"event"' in c))

    # -- Docker ----------------------------------------
    print("\n[Docker] Containerization")
    df_path = os.path.join(base, "Dockerfile")
    if os.path.exists(df_path):
        df = open(df_path, encoding='utf-8').read()
        results.append(check("Multi-stage build", "AS builder" in df or "AS runtime" in df))
        results.append(check("Non-root user", "USER " in df or "useradd" in df))
        results.append(check("HEALTHCHECK", "HEALTHCHECK" in df))
        results.append(check("Slim image", "slim" in df or "alpine" in df))

    di_path = os.path.join(base, ".dockerignore")
    if os.path.exists(di_path):
        di = open(di_path, encoding='utf-8').read()
        results.append(check(".dockerignore covers .env", ".env" in di))
        results.append(check(".dockerignore covers cache", "__pycache__" in di))

    # -- Summary ---------------------------------------
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    pct = round(passed / total * 100)
    print("\n" + "=" * 55)
    print(f"  Result: {passed}/{total} checks passed ({pct}%)")
    if pct == 100: print("  🎉 SUCCESS: 100% PRODUCTION READY!")
    print("=" * 55 + "\n")
    return pct == 100

if __name__ == "__main__":
    run_checks()

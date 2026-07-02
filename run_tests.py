"""Ejecutor de tests con barra de progreso por módulo."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MODULES = [
    ("cliente", "tests/cliente/test_routes.py"),
    ("ajustador", "tests/ajustador/test_routes.py"),
    ("taller", "tests/taller/test_routes.py"),
    ("aseguradora (siniestros)", "tests/aseguradora/test_siniestros.py"),
    ("aseguradora (crud)", "tests/aseguradora/test_crud.py"),
    ("admin", "tests/admin/test_routes.py"),
    ("auth", "tests/auth/test_routes.py"),
]

VENV_PYTHON = ROOT / "venv" / "bin" / "python3"
PYTHON = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def main():
    passed = 0
    failed = 0
    total = len(MODULES)
    errors = []

    print(f"Ejecutando {total} módulos de test…\n")

    for i, (name, rel_path) in enumerate(MODULES, 1):
        label = f"  [{i}/{total}] {name}"
        print(f"{label}  ", end="", flush=True)
        abs_path = ROOT / rel_path
        result = subprocess.run(
            [PYTHON, "-m", "pytest", str(abs_path), "-q", "--tb=short"],
            capture_output=True, text=True, timeout=120, cwd=ROOT,
        )
        if result.returncode == 0:
            print("✓")
            passed += 1
        else:
            print("✗")
            failed += 1
            errors.append((name, result.stdout + result.stderr))

    print(f"\n{'='*50}")
    print(f"Resultado: {passed} pasaron, {failed} fallaron (de {total})")

    if errors:
        print("\nDetalles de fallos:")
        for name, output in errors:
            print(f"\n── {name} ──")
            # Últimas líneas relevantes
            lines = output.strip().splitlines()
            for line in lines[-15:]:
                print(f"  {line}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

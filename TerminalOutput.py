#!/usr/bin/env python3

def Show_Comments(data):
    comments = data.get("comentarios", [])
    if not comments:
        print("✅ No se encontraron problemas.")
        return
    for c in comments:
        print(f"\n[{c['severidad'].upper()}] {c['archivo']} (línea ~{c['linea_aproximada']})")
        print(f"  Categoría: {c['categoria']}")
        print(f"  {c['explicacion']}")
        print(f"  Sugerencia: {c['sugerencia']}")
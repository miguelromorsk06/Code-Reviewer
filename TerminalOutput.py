#!/usr/bin/env python3

def Show_Comments(data):
    comments = data.get("comments", [])
    rating=data.get("rating",None)
    print(f"📊 Rating: {rating}/10")
    if not comments:
        print("✅ No problems where detected.")
        return
    for c in comments:
        print(f"\n[{c['severity'].upper()}] {c['file']} (line ~{c['approximate_line']})")
        print(f"  Category: {c['category']}")
        print(f"  {c['explanation']}")
        print(f"  Suggestions: {c['suggestion']}")
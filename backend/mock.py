import json

with open('../frontend/public/telemetry/indianapolis.json', 'r') as f:
    template = json.load(f)

for track in ['cota', 'road-america', 'sebring', 'vir', 'sonoma']:
    with open(f'../frontend/public/telemetry/{track}.json', 'w') as f:
        json.dump(template, f)
    print(f"✅ {track}")

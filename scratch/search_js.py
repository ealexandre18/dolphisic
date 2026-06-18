with open("dist/assets/index-CzgsKiV0.css.bak", "r", encoding="utf-8") as f:
    orig = f.read()

idx = orig.find(".leaflet-container")
print("Index of .leaflet-container in original CSS:", idx)
if idx != -1:
    print("Content before .leaflet-container (first 1000 chars):")
    print(orig[:min(idx, 1000)])
    print("...")
    print("Length of content before .leaflet-container:", idx)

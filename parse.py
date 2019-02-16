import csv
import json

# read file
def read(file):
    data = []

    with open(file) as read:
        for row in csv.DictReader(read):
            data += [row]

    return data

# extract coordinates
def extract_coords(row):
    return [float(row["Latitude"]),
            float(row["Longitude"]),
            float(row["Elevation"])]

# get coordinates
def get_coords(data):
    coords = []
    
    for row in data:
        coords += [extract_coords(row)]

    return coords

# group data by field
def group_fields(data):
    fields = {}
    
    for row in data:
        field = row["Field"]
        
        if field not in fields:
            fields[field] = [extract_coords(row)]
        else:
            fields[field] += [extract_coords(row)]

    return fields

# run module
def run(file):
    data = read(file)
    coords = get_coords(data)
    fields = group_fields(data)

    # extract 2d points
    pts_2d = [{"latitude": c[0], "longitude": c[1]} for c in coords]

    # write points to json
    with open("points.json", "w") as write:
        write.write(json.dumps({"points": pts_2d}))

    return coords, fields

if __name__ == "__main__":
    coords, fields = run("poi.csv")

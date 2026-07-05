import pandas as pd
import unicodedata

# Input file
SETUP_CSV = "province_setup.csv"
# Output file
f_area = open("areas_output.txt", "w")
f_region = open("regions_output.txt", "w")
# Culture-plurality de jure output (see generate_de_jure below)
f_de_jure = open("de_jure_output.txt", "w")

# Turn the province_setup CSV into a dataframe
df = pd.read_csv(
    SETUP_CSV,
    sep=';',
    low_memory=False
)

# Get a list of all areas in your CSV
areas = df.AREA.unique().tolist()

# Function to print to a text file all provinces in an area in the Imperator
# format
def output_area(area, provinces):
    f_area.write(area + " = {\n" +
            "   provinces = {\n")
    provids_list = provinces['PROVID'].tolist()
    for provid in provids_list:
        f_area.write("      " + str(provid) + "\n")
    f_area.write("   }\n}\n\n")

def sanitise_string(input_string):
    output_string = str(input_string).replace(" ", "_").replace(".","_")
    return ''.join(c for c in unicodedata.normalize('NFD', output_string)
                  if unicodedata.category(c) != 'Mn')

# Get all the provinces in each area
for area in areas:
    provinces = df.loc[df['AREA'] == area]
    # Sanitise the area string
    area = sanitise_string(area)
    output_area(str(area), provinces)

# Now generate a regions file with every area as a region to avoid errors
for area in areas:
    # Sanitise the area string
    area = sanitise_string(area)
    f_region.write("region_" + str(area) + " = {\n" +
                   "    areas = {\n" +
                   "        " + str(area) + "\n    }\n}\n"
                   )

# Culture-plurality de jure: for each area, work out which culture holds the
# most provinces and emit a de_jure_culture -> areas lookup. This is the
# generated "which culture this land rightfully belongs to" table; consumers
# (irredentism, etc.) read it. Provinces without a listed culture are ignored
# when tallying, and an area with no cultured province at all is skipped.
# Ties are broken by lowest-sorted culture name so the output is deterministic
# across regenerations.
def generate_de_jure(df):
    de_jure = {}  # culture -> list of areas
    for area in areas:
        provinces = df.loc[df['AREA'] == area]
        counts = provinces['CULTURE'].dropna().value_counts()
        if counts.empty:
            continue
        top = counts.max()
        # Deterministic tiebreak: among cultures sharing the top count, take the
        # first alphabetically.
        winner = sorted(c for c in counts.index if counts[c] == top)[0]
        de_jure.setdefault(winner, []).append(sanitise_string(area))
    # Emit one block per culture, cultures and areas in sorted order.
    for culture in sorted(de_jure):
        f_de_jure.write(str(culture) + " = {\n" +
                        "    areas = {\n")
        for area in sorted(de_jure[culture]):
            f_de_jure.write("        " + str(area) + "\n")
        f_de_jure.write("    }\n}\n\n")

generate_de_jure(df)

f_area.close()
f_region.close()
f_de_jure.close()

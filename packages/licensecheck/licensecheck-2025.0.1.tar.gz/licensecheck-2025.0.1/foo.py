import json
from pathlib import Path

d = json.loads(Path("in.json").read_bytes())

for l in d["licenses"]:

	_id = l["licenseId"].upper()
	name = l["name"].upper()

	my_name = name.split()[0]


	if l["isOsiApproved"]:
		pass

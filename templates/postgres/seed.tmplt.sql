% for mname in models:
<% 
model = models[mname] 
mseed = seed_data(mname)
%>\
INSERT INTO ${gbl["project_name"]}.${pascalc(model["name"])} (
    % for prop in model["props"]:
    ${"," if not loop.first else " "}${pascalc(prop["name"])} 
    % endfor
) VALUES
## When theres no seed data, just list the commented columns to have a reference and fill later.
% if not mseed:
(
    % for prop in model["props"]:
    ${"," if not loop.first else " "}--${pascalc(prop["name"])} 
    % endfor
)
% else:
% for row in mseed:
${"," if not loop.first else " "}(
    % for prop in model["props"]:
    ${"," if not loop.first else " "}'${row[prop["name"]]}'--${pascalc(prop["name"])} 
    % endfor
)${";" if loop.last else ""}
% endfor
% endif
% endfor
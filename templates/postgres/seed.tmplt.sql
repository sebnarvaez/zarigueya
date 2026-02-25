% for model in models:
INSERT INTO ${gbl["project_name"]}.${pascalc(model["name"])} (
    % for prop in model["props"]:
    ${"," if not loop.first else " "}${pascalc(prop["name"])} 
    % endfor
) VALUES (
    % for prop in model["props"]:
    ${"," if not loop.first else " "} --${pascalc(prop["name"])} 
    % endfor
);
% endfor
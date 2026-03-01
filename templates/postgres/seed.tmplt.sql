% for model in models:
<% mdata = data[model] %>\
INSERT INTO ${gbl["project_name"]}.${pascalc(model["name"])} (
    % for prop in model["props"]:
    ${"," if not loop.first else " "}${pascalc(prop["name"])} 
    % endfor
) VALUES (
    % for prop in model["props"]:
    <% 
    prop_line = ""
    if data is not None and data[prop["name"]]:
        prop_line = data[prop["name"]]
    %>\
    ${"," if not loop.first else " "}${prop_line}--${pascalc(prop["name"])} 
    % endfor
);
% endfor
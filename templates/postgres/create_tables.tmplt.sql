CREATE SCHEMA IF NOT EXISTS ${gbl["project_name"]};

% for model in models:
-- DROP TABLE IF EXISTS ${gbl["project_name"]}.${pascalc(model["name"])};
% endfor

% for model in models:
CREATE TABLE ${gbl["project_name"]}.${pascalc(model["name"])} (
    % for prop in model["props"]:
    ${"," if not loop.first else " "}${pascalc(prop["name"])} ${conv["sql"][prop["type"]]}${" NULL" if "optional" in prop and not prop["optional"] else ""}
    % endfor
);
% endfor
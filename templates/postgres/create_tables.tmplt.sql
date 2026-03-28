IF EXISTS(SELECT datname FROM pg_catalog.pg_database WHERE LOWER(datname) = LOWER('${gbl["project_name"]}')
BEGIN
    CREATE DATABASE ${gbl["project_name"]};
END
\c ${gbl["project_name"]}

% for model in models.values():
-- DROP TABLE IF EXISTS ${pascalc(model["name"])};
% endfor

% for model in models.values():
CREATE TABLE ${pascalc(model["name"])} (
    % for prop in model["props"]:
    ${"," if not loop.first else " "}${pascalc(prop["name"])} ${conv["sql"][prop["type"]]}${" NULL" if "optional" in prop and not prop["optional"] else ""}
    % endfor
);

% endfor
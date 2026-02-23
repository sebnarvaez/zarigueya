CREATE SCHEMA IF NOT EXISTS ${gbl["project_name"]}
	% for model in models:
    CREATE TABLE ${pascalc(model["name"])} (
        % for prop in model["props"]:
        ${pascalc(prop["name"])} ${conv["sql"][prop["type"]]} ${"NULL" if "optional" in prop and not prop["optional"] else ""}${"," if not loop.last else ""}
        % endfor
    )${";" if loop.last else ""}
    % endfor
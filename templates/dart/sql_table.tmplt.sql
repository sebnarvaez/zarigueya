<%!
from caseconverter import camelcase, pascalcase, snakecase 
%>
-- DROP TABLE IF EXISTS ${pascalcase(modelname_plural)}

CREATE TABLE ${pascalcase(modelname_plural)} (
% for prop in properties:
    ${prop["name"]} ${sql_types[prop["type"]]},
% endfor
);
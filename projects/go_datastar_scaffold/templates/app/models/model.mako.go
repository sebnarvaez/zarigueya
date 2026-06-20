package model
<%!
from caseconverter import camelcase, pascalcase, snakecase 
%>

type ${pascalcase(modelname_singular)} struct {
	Id string
    % for prop in properties:
	${pascalcase(prop['name'])} ${pascalcase(prop['type'])}
}

<%!
from caseconverter import camelcase, pascalcase, snakecase 
%>
class ${pascalcase(modelname_singular)} {
  ${pascalcase(modelname_singular)}({
    required this.id,
    % for prop in properties:
    required this.${camelcase(prop['name'])}${',' if not loop.last else ''}
    % endfor
  });

  final String id;
% for prop in properties:
  final ${dart_types[prop['type']]} ${camelcase(prop['name'])};
% endfor

  ${pascalcase(modelname_singular)}.fromMap(Map<String, dynamic> map)
    : id = map['id'],
    % for prop in properties:
      ${camelcase(prop['name'])} = \
    % if prop['type'] != 'string':
${dart_types[prop['type']]}.parse(map['${camelcase(prop['name'])}'])\
      % else:
map['${camelcase(prop['name'])}']\
      % endif
${',' if not loop.last else ';'}
      % endfor
}

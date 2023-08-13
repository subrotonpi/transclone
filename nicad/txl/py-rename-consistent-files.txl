% NiCad consistent renaming - Python files
% Jim Cordy, July 2020

% NiCad tag grammar
include "nicad.grm"

% Using Python grammar
include "python.grm"

% Redefinition for potential clones
define potential_clone
    [file_input]
end define

redefine indent
	[newline] 'INDENT [IN]
end redefine

redefine dedent
	[EX] 'DEDENT [newline]
end redefine

% Generic consistent renaming
include "generic-rename-consistent.rul"

% Specialize for Python
redefine xml_source_coordinate
    '<source [SPOFF] 'file=[stringlit] [SP] 'startline=[stringlit] [SP] 'endline=[stringlit] '> [SPON] [newline]
end redefine

redefine end_xml_source_coordinate
    '</source> [newline]
end redefine

% Literal renaming for Python
include "py-rename-literals.rul"

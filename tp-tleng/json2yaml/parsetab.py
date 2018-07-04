
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BEGIN_ARRAY BEGIN_OBJECT END_ARRAY END_OBJECT NAME_SEPARATOR VALUE_SEPARATOR QUOTATION_MARK FALSE TRUE NULL DECIMAL_POINT DIGITS E MINUS PLUS ZERO STRINGvalue : stringvalue : FALSEvalue : TRUEvalue : NULLvalue : numbervalue : objectvalue : arrayelements : valueelements : value VALUE_SEPARATOR elementsobject : BEGIN_OBJECT members END_OBJECTobject : BEGIN_OBJECT END_OBJECTmembers : pairmembers : pair VALUE_SEPARATOR memberspair : string NAME_SEPARATOR valuearray : BEGIN_ARRAY END_ARRAYarray : BEGIN_ARRAY elements END_ARRAYnumber : DIGITSstring : QUOTATION_MARK STRING QUOTATION_MARK'
    
_lr_action_items = {'DIGITS':([0,5,23,25,],[1,1,1,1,]),'VALUE_SEPARATOR':([1,3,4,6,7,10,11,12,13,15,18,19,21,24,26,28,],[-17,-2,-1,-6,-5,-7,-4,-3,-11,22,-15,25,-10,-16,-18,-14,]),'BEGIN_OBJECT':([0,5,23,25,],[2,2,2,2,]),'FALSE':([0,5,23,25,],[3,3,3,3,]),'END_OBJECT':([1,2,3,4,6,7,10,11,12,13,14,15,18,21,24,26,27,28,],[-17,13,-2,-1,-6,-5,-7,-4,-3,-11,21,-12,-15,-10,-16,-18,-13,-14,]),'BEGIN_ARRAY':([0,5,23,25,],[5,5,5,5,]),'NAME_SEPARATOR':([16,26,],[23,-18,]),'QUOTATION_MARK':([0,2,5,20,22,23,25,],[9,9,9,26,9,9,9,]),'END_ARRAY':([1,3,4,5,6,7,10,11,12,13,17,18,19,21,24,26,29,],[-17,-2,-1,18,-6,-5,-7,-4,-3,-11,24,-15,-8,-10,-16,-18,-9,]),'STRING':([9,],[20,]),'NULL':([0,5,23,25,],[11,11,11,11,]),'TRUE':([0,5,23,25,],[12,12,12,12,]),'$end':([1,3,4,6,7,8,10,11,12,13,18,21,24,26,],[-17,-2,-1,-6,-5,0,-7,-4,-3,-11,-15,-10,-16,-18,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'elements':([5,25,],[17,29,]),'string':([0,2,5,22,23,25,],[4,16,4,16,4,4,]),'object':([0,5,23,25,],[6,6,6,6,]),'number':([0,5,23,25,],[7,7,7,7,]),'value':([0,5,23,25,],[8,19,28,19,]),'members':([2,22,],[14,27,]),'pair':([2,22,],[15,15,]),'array':([0,5,23,25,],[10,10,10,10,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> value","S'",1,None,None,None),
  ('value -> string','value',1,'p_expression_value_string','parser.py',9),
  ('value -> FALSE','value',1,'p_expression_value_false','parser.py',12),
  ('value -> TRUE','value',1,'p_expression_value_true','parser.py',15),
  ('value -> NULL','value',1,'p_expression_value_null','parser.py',18),
  ('value -> number','value',1,'p_expression_value_number','parser.py',21),
  ('value -> object','value',1,'p_expression_value_object','parser.py',24),
  ('value -> array','value',1,'p_expression_value_array','parser.py',27),
  ('elements -> value','elements',1,'p_expression_elements_value','parser.py',30),
  ('elements -> value VALUE_SEPARATOR elements','elements',3,'p_expression_elements_list','parser.py',33),
  ('object -> BEGIN_OBJECT members END_OBJECT','object',3,'p_expression_object','parser.py',36),
  ('object -> BEGIN_OBJECT END_OBJECT','object',2,'p_expression_object_empty','parser.py',39),
  ('members -> pair','members',1,'p_expression_members','parser.py',42),
  ('members -> pair VALUE_SEPARATOR members','members',3,'p_expression_members_list','parser.py',45),
  ('pair -> string NAME_SEPARATOR value','pair',3,'p_expression_pair','parser.py',48),
  ('array -> BEGIN_ARRAY END_ARRAY','array',2,'p_expression_array_empty','parser.py',51),
  ('array -> BEGIN_ARRAY elements END_ARRAY','array',3,'p_expression_array_list','parser.py',54),
  ('number -> DIGITS','number',1,'p_expression_number','parser.py',57),
  ('string -> QUOTATION_MARK STRING QUOTATION_MARK','string',3,'p_expression_string','parser.py',60),
]
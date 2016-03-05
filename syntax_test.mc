# SYNTAX TEST "Packages/Sublime-MonkeyC/MonkeyC.sublime-syntax"

"foobar"
#<- punctuation.definition.string.begin.mc
# ^  string.quoted.double.mc
#      ^  punctuation.definition.string.end.mc

'foobar'
#<- punctuation.definition.string.begin.mc
# ^  string.quoted.single.mc
#      ^  punctuation.definition.string.end.mc

//foo
#<-  punctuation.definition.comment.mc
# ^  comment.line.mc 

/* multi-line comment */
#<-  punctuation.definition.comment.mc
#  ^  comment.block.mc

if for else do while switch case try catch finally return throw
# <-  keyword.control.flow.mc
#   ^  keyword.control.flow.mc
#       ^  keyword.control.flow.mc
#            ^  keyword.control.flow.mc
#                ^  keyword.control.flow.mc
#                      ^  keyword.control.flow.mc
#                             ^  keyword.control.flow.mc
#                                  ^  keyword.control.flow.mc    
#                                     ^  keyword.control.flow.mc    
#                                             ^  keyword.control.flow.mc    
#                                                     ^  keyword.control.flow.mc    
#                                                           ^  keyword.control.flow.mc    

using Toybox.System as Sys;
# ^  keyword.control.import.mc
#       ^  support.class.mc
#                ^  support.class.mc
#                   ^  keyword.control.import.mc

50  400.6 4.0d 5.0f  0x500 5l 0xface
# <-  constant.numeric.mc
#    ^  constant.numeric.mc
#           ^  constant.numeric.mc
#              ^  constant.numeric.mc
#                     ^  constant.numeric.mc
#                          ^  constant.numeric.mc
#                                ^  constant.numeric.mc

and or instanceof has extends
#^  keyword.operator.mc
#   ^  keyword.operator.mc
#       ^  keyword.operator.mc
#                   ^  keyword.operator.mc
#                        ^ keyword.operator.mc

const hidden public 
#^  storage.modifier.mc
#      ^  storage.modifier.mc
#              ^  storage.modifier.mc


true false null
#^  constant.language.mc
#       ^  constant.language.mc
#           ^  constant.language.mc


function
#^  storage.type.function.mc

:symbol :my_symbol
#^  constant.other.symbol.mc
#         ^  constant.other.symbol.mc


if ( a < 5 ) {
#      ^  keyword.operator.comparison.mc

< > <= >= == !=
#<-  keyword.operator.comparison.mc
# ^  keyword.operator.comparison.mc
#   ^  keyword.operator.comparison.mc
#      ^  keyword.operator.comparison.mc
#         ^  keyword.operator.comparison.mc
#            ^  keyword.operator.comparison.mc

function myFunc(arg1, arg2) {
# ^  meta.function.method.with-arguments.mc storage.type.function.mc
#         ^  meta.function.method.with-arguments.mc entity.name.function.mc
#              ^  meta.function.method.with-arguments.mc punctuation.definition.parameters.mc
#                ^  meta.function.method.with-arguments.mc variable.parameter.function.mc


class MyProjectApp extends App.AppBase {
# ^  storage.type.class.mc
#       ^ entity.name.type.class.mc
#                    ^ keyword.operator.mc
#                             ^ entity.other.inherited-class.mc
#                                      ^ punctuation.definition.class.mc
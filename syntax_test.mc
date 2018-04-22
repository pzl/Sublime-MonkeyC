# SYNTAX TEST "Packages/Sublime-MonkeyC/MonkeyC.sublime-syntax"

"foobar"
#<- punctuation.definition.string.begin.mc
# ^  string.quoted.double.mc
#      ^  punctuation.definition.string.end.mc

//foo
#<-  punctuation.definition.comment.mc
# ^  comment.line.mc

   // spaced comment
#   ^ punctuation.definition.comment.mc
#       ^ comment.line.mc

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

x += 5
# ^ keyword.operator.assignment.mc
#  ^ keyword.operator.assignment.mc

-=
#<- keyword.operator.assignment.mc
#^ keyword.operator.assignment.mc

using Toybox.System as Sys;
# ^  keyword.control.import.mc
#       ^  support.class.mc
#                ^  support.class.mc
#                   ^  keyword.control.import.mc

50  400.6 4.0d 5.0f  0x500 5l 0xface 0x80000000l
# <-  constant.numeric.integer.mc
#    ^  constant.numeric.float.mc
#           ^  constant.numeric.float.mc
#              ^  constant.numeric.float.mc
#                     ^  constant.numeric.hex.mc
#                          ^  constant.numeric.integer.mc
#                                ^  constant.numeric.hex.mc
#                                     ^  constant.numeric.hex.mc


instanceof has extends
#^  keyword.operator.mc
#           ^  keyword.operator.mc
#               ^  keyword.operator.mc

const hidden public private
#^  storage.type.mc
#      ^  storage.modifier.mc
#              ^  storage.modifier.mc
#                    ^ storage.modifier.mc

true false null NaN
#^  constant.language.mc
#       ^  constant.language.mc
#           ^  constant.language.mc
#                ^ constant.language.mc


var function f(){} const
#<- storage.type.mc
#     ^  storage.type.function.mc
#                   ^ storage.type.mc

:symbol :my_symbol
#^  constant.other.symbol.mc
#         ^  constant.other.symbol.mc


if ( a < 5 ) {
#      ^  keyword.operator.comparison.mc

if(!failed)
#^ keyword.control.flow.mc


?
#<- keyword.operator.other.mc

! && ||
#<- keyword.operator.logic.mc
# ^ keyword.operator.logic.mc
#    ^ keyword.operator.logic.mc

+ - * / % 
#<- keyword.operator.arithmetic.mc
# ^ keyword.operator.arithmetic.mc
#   ^ keyword.operator.arithmetic.mc
#     ^ keyword.operator.arithmetic.mc
#       ^ keyword.operator.arithmetic.mc

~ & << >> | ^ 
#<- keyword.operator.bitwise.mc
# ^ keyword.operator.bitwise.mc
#   ^ keyword.operator.bitwise.mc
#      ^ keyword.operator.bitwise.mc
#         ^ keyword.operator.bitwise.mc
#           ^ keyword.operator.bitwise.mc

< <= > >= == !=
#<- keyword.operator.comparison.mc
# ^ keyword.operator.comparison.mc
#    ^ keyword.operator.comparison.mc
#      ^ keyword.operator.comparison.mc
#         ^ keyword.operator.comparison.mc
#            ^ keyword.operator.comparison.mc
#             ^ keyword.operator.comparison.mc

=>
#<- keyword.operator.assignment.mc
#^  keyword.operator.assignment.mc

and or
#^ keyword.operator.word.mc
#   ^ keyword.operator.word.mc

function myFunc(arg1, arg2) {}
# ^  meta.function.method.with-parameters.mc storage.type.function.mc
#         ^  meta.function.method.with-parameters.mc entity.name.function.mc
#              ^  meta.function.parameters.mc punctuation.section.group.begin.mc
#                ^  meta.function.parameters.mc variable.parameter.function.mc


class MyProjectApp extends App.AppBase {}
# ^  storage.type.class.mc
#       ^ entity.name.type.class.mc
#                    ^ keyword.operator.mc
#                             ^ entity.other.inherited-class.mc
#                                      ^ punctuation.definition.class.mc
}


Toybox.thing(sdsd,asdasda);

var n = null;
#^ storage.type.mc
#     ^ keyword.operator.assignment.mc
#        ^ constant.language.mc
#           ^ punctuation.terminator.mc
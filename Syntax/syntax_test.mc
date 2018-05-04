// SYNTAX TEST "Packages/MonkeyC/Syntax/MonkeyC.sublime-syntax"

"foobar"
//<- punctuation.definition.string.begin.mc
// ^  string.quoted.double.mc
//     ^  punctuation.definition.string.end.mc

//foo
//<-  punctuation.definition.comment.mc
// ^  comment.line.mc

   // spaced comment
//  ^ punctuation.definition.comment.mc
//       ^ comment.line.mc


 "no /* comments */ within //string "
 // ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string.quoted.double.mc

if (thing > 5) { return 6; } else if (foo==bar) { return 0; } else { return 1; }
//<- keyword.control.conditional.mc
//  ^^^^^^^^^^^^^^^^ meta.conditional.mc
//                            ^^^^^^^^^ meta.conditional.mc
//                            ^^^^^^ keyword.control.conditional.mc
//                                                              ^^ keyword.control.conditional.mc

for (var i=0; i<4; i++){ System.println(i); }
//<- keyword.control.loop.mc
//  ^ punctuation.section.group.begin.mc
//    ^ storage.type.mc
//       ^ meta.for.mc

do { System.println(true); } while (x>5);
//<- keyword.control.loop.mc
//<- meta.do-while.mc
// ^ punctuation.section.block.begin.mc
//   ^ meta.block.mc
//     ^ meta.do-while.mc
//      ^ support.module.mc
//                    ^ constant.language.mc
//                         ^ punctuation.section.block.end.mc
//                           ^ meta.do-while.mc
//                              ^ keyword.control.loop.mc
//                                 ^ punctuation.section.group.begin.mc
//                                   ^ meta.group.mc

switch (c) { case 5: System.println(5); default: x++; break; }
//^ keyword.control.switch.mc
// ^ meta.switch.mc
//     ^ punctuation.section.group.begin.mc
//      ^ variable.other.mc
//        ^ meta.switch.mc
//         ^ punctuation.section.block.begin.mc
//           ^ meta.switch.mc
//           ^ meta.block.mc
//             ^ keyword.control.switch.mc
//                 ^ punctuation.separator.mc
//                                        ^ keyword.control.switch.mc
//                                             ^ punctuation.separator.mc

try catch () finally return throw
//^  keyword.control.flow.mc
//   ^  keyword.control.flow.mc
//             ^  keyword.control.flow.mc
//                    ^  keyword.control.flow.mc
//                          ^  keyword.control.flow.mc


try { foo(thing); } catch (ex instanceof AnException) { throw ex; } finally { foo(0); }
//^^^^^^^^^^^^^^^ meta.try.mc
//                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.catch.mc
//                                                                    ^^^^^^^^^^^^ meta.finally.mc

x += 5
//^^ keyword.operator.assignment.mc

  -=
//^^ keyword.operator.assignment.mc

using Toybox.System as Sys;
// ^  keyword.control.import.using.mc
//       ^  support.module.mc
//                ^  support.module.mc
//                   ^  keyword.control.import.as.mc
//                      ^ variable.other.import.alias.mc
// ^^^^^^^^^^^^^^^^^^^^^^^ meta.statement.import.mc

50 5l 400.6 4.0d 5.0f  0x500  0xface 0x80000000l
//<- constant.numeric.integer.mc 
// ^^  constant.numeric.integer.mc
//     ^ constant.numeric.float.mc
//          ^^^^ constant.numeric.float.mc
//                ^^  constant.numeric.float.mc
//                     ^^^ constant.numeric.hex.mc
//                            ^^^^ constant.numeric.hex.mc
//                                    ^^^^  constant.numeric.hex.mc

  0d 1f
//^^ constant.numeric.float.mc
//   ^^ constant.numeric.float.mc


  10-4
//^^ constant.numeric.integer.mc
//  ^ keyword.operator.arithmetic.mc
//   ^ constant.numeric.integer.mc

instanceof has extends
//^  keyword.operator.mc
//           ^  keyword.operator.mc
//               ^  keyword.operator.mc

const hidden public private
//^  storage.type.mc
//      ^  storage.modifier.mc
//              ^  storage.modifier.mc
//                    ^ storage.modifier.mc

true false null NaN
//^  constant.language.mc
//       ^  constant.language.mc
//           ^  constant.language.mc
//                ^ constant.language.mc


var function f(){} const
//<- storage.type.mc
//     ^  storage.type.function.mc
//                   ^ storage.type.mc

:symbol :my_symbol
//<- punctuation.definition.symbol.mc
//^  constant.other.symbol.mc
//         ^  constant.other.symbol.mc


  (:symbol)
//^ punctuation.section.annotation.begin.mc
//^^^^^^^^^ meta.annotation.mc
// ^^^^^^^ entity.name.label.mc
//        ^ punctuation.section.annotation.end.mc

 (:symbol1 :symbol2)
//^^^^^^^^^^^^^^^^^^ meta.annotation.mc
//^^^^^^^^ entity.name.label.mc
//        ^ - entity.name.label.mc
//          ^^^^^^^ entity.name.label.mc

(:minSdk("2.3.0"))
//^^^^^^^^^^^^^^ meta.annotation.mc entity.name.label.mc
// I don't even know what's happening here


foo(:thing)
//   ^ - entity.name.label.mc
//   ^^^ - meta.annotation.mc

if ( a < 5 ) { }
//     ^  keyword.operator.comparison.mc

if(!failed)
//<- keyword.control.conditional.mc

// quick stray-bracket nesting visual test
Test.assert( ((result > 436) && (result < 437)));


?:
//<- keyword.operator.ternary.mc

! && ||
//<- keyword.operator.logic.mc
// ^ keyword.operator.logic.mc
//    ^ keyword.operator.logic.mc

+ - * / % 
//<- keyword.operator.arithmetic.mc
//^ keyword.operator.arithmetic.mc
//  ^ keyword.operator.arithmetic.mc
//    ^ keyword.operator.arithmetic.mc
//      ^ keyword.operator.arithmetic.mc

~ & << >> | ^ 
//<- keyword.operator.bitwise.mc
//^ keyword.operator.bitwise.mc
//  ^ keyword.operator.bitwise.mc
//     ^ keyword.operator.bitwise.mc
//        ^ keyword.operator.bitwise.mc
//          ^ keyword.operator.bitwise.mc

< <= > >= == !=
//<- keyword.operator.comparison.mc
//^^ keyword.operator.comparison.mc
//   ^ keyword.operator.comparison.mc
//     ^^ keyword.operator.comparison.mc
//        ^^ keyword.operator.comparison.mc
//           ^^ keyword.operator.comparison.mc

  =>
//^^ keyword.operator.assignment.mc

and or
//^ keyword.operator.word.mc
//   ^ keyword.operator.word.mc


public function myFunc(arg1, arg2) { return 6; }
// ^ storage.modifier.mc
//        ^ storage.type.function.mc
//      ^^^^^^^^^^^^^^  meta.function.definition.mc 
//               ^^^ entity.name.function.mc
//                    ^ punctuation.section.group.begin.mc
//                      ^^^^^^^^ meta.function.parameters.mc
//                      ^ variable.parameter.function.mc
//                         ^ punctuation.separator.parameter.function.mc
//                             ^ variable.parameter.function.mc
//                                 ^ punctuation.section.block.begin.mc
//                                  ^^^^^^^^^^^ meta.block.function.mc
//                                             ^ punctuation.section.block.end.mc

class MyProjectApp extends App.AppBase {  }
// ^  storage.type.class.mc
//       ^ entity.name.class.mc
//                    ^ keyword.operator.inheritance.mc
//                             ^ entity.other.inherited-class.mc
//                                     ^ punctuation.section.block.begin.mc
//^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.mc




thing.property
// ^ variable.other.object.mc
//   ^ punctuation.accessor.mc
//     ^ meta.property.object.mc
//     ^ variable.other.property.mc

foo();
//^ meta.function-call.mc
//^ variable.function.mc

thing.foo();
//^^ variable.other.object.mc
//   ^ punctuation.accessor.mc
//    ^^^ variable.function.mc
//    ^^^ meta.function-call.method.mc - meta.function-call.arguments.mc
//       ^^ meta.function-call.arguments.mc
//       ^ punctuation.section.group.begin.mc
//        ^ punctuation.section.group.end.mc


thing.getProperty();
//    ^^^^^^^^^ support.function.mc

thing.foo(0, 1, x);
//^^ variable.other.object.mc
//   ^ punctuation.accessor.mc
//    ^^^ variable.function.mc
//    ^^^ meta.function-call.method.mc
//        ^^^^^^^ meta.function-call.arguments.mc
//       ^ punctuation.section.group.begin.mc
//         ^ punctuation.separator.comma.mc
//               ^ punctuation.section.group.end.mc


var array = [ [1,2], [3,4] ];

var n = null;
//^ storage.type.mc
//    ^ keyword.operator.assignment.mc
//       ^ constant.language.mc
//          ^ punctuation.terminator.mc
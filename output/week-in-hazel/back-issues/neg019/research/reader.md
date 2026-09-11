
## #1012 Haz3l user defined operators / shawn-stovall
created 2023-05-14T17:52:06Z merged None base dev
BODY (mutable, retrieved today):
Adding the ability for users to define their own operators.

This pull request makes changes to the external language's pattern and expression forms so that custom infix operators can be defined and applied. This then elaborates to an applied `DHExp.t` of the form `Ap(operator_variable, Tuple([arg1, a rg2]))`. The evaluator then continues unmodified to process the function application.

Features:

- `_op_` can be used in a normal let to define a new operator
- `arg1 op arg2` can then be used without the underscores to apply the operator's function

Potential Future Features:

- `_op_` can be used in expressions to allow for typical function application (of the form `_op_(arg1, arg2)`).
- `_op` and `op_` used to define postfix and prefix operators, respectively.

comments / shawn-stovall / 2023-05-26T15:38:36Z
User-defined operators are working with the following features:

* `_op_` defines a user-defined operator, with op representing one or more of the following symbols: `~?!$%&*+\\-./:<=>@^`
Precedence and associativity are decided by the first character of the operator. I used the list of valid operator symbols from Ocaml to determine which symbols to include in this list, as well as `~?!` which are usually reserved for different fixities in Ocaml. The precedence of the first character is determined by the matching precedence of the built-in operator of the same symbol. For the symbols not in Hazel, I used Ocaml precedence as a reference. The exceptions to this are `~!?` to which I gave the precedence of equality.
* Calling the operator surrounded by parentheses in the form `_op_(arg1, arg2)` calls the operator as a normal function.
* There are user-facing errors for defining an operator that is the same as a built-in operator, defining an operator that is bound to a non-binary function definition, and and error for trying to call an undefined operator (which uses the standard "variable not defined" error).

comments / cyrus- / 2023-06-06T19:47:53Z
Error message here should say something about user-defined operator being unbound, not that it is not a binary function. 

<img width="1202" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/8fe8ae65-8a71-4716-8b85-a818c7a7426a">


comments / cyrus- / 2023-06-06T19:48:10Z
Error box here is broken (when function extends over more than one line)

<img width="521" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/b8820563-ef40-4e8a-ba2f-6caf13457e01">


comments / cyrus- / 2023-06-06T19:50:30Z
Operator definition error should appear only if the type of the bound expression is not *consistent* with a binary function, even if it isn't exactly of the form (t1, t2) -> t3. So the hole type or hole -> t3 things like that are fine. Casts will handle downstream problems.

<img width="372" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/7935e0cf-ed5c-45db-a5c2-e0a667eea407">


comments / cyrus- / 2023-06-06T19:52:20Z
Let's also update the scratch slide 1 (language reference) to list out all of the operators in order of precedence and include a comment describing how user-defined operators work (precedence and associativity).

comments / cyrus- / 2023-06-06T19:56:18Z
Nice work, seems like just a few polish things are remaining! Marking as draft again based on incomplete functional review comments above, will continue to take a look once those things are addressed.

comments / cyrus- / 2023-08-14T19:21:47Z
@shawn-stovall quite a few conflicts with `dev` after recent ADTs merge, can you take a look at those?

comments / disconcision / 2023-08-19T19:30:18Z
I've been thinking lately about ambiguity concerns for characters that can live in tokens of more than one grammatical class. For our purposes let's specify the following grammatical classes:

- Operand (eg `foo`, `1.0`, `_`, `Int`)
- Infix Operator (eg `+`, `->`, `!=.`)
- Prefix Operator (ie `!`, `+`, `-`)
- Postfix Operator (current none in hazel)
- Form Delimiter (eg `let`, `=`, `in`; should maybe divide into multiple classes)

Even without user-defined operators, we already have some ambiguities in our grammar, both realized and potential. This list is currently exhaustive AFAIK:

1. `.` occurs in both operands (floating points) and infix operators (`==.` `!=.` `<.` `>.` `<=.` `>=.`). Thus `1==.1` could be parsed as `(1)==.(1)` or `(1)==(.1)`. Currently the accepted parse is the first, but this is somewhat incidental, due to the fact that we attempt to append an inserted character to the left first before the right. If we wish to allow such ambiguities, we should ideally clarify our general principles for disambiguation; either formalize the left to right model, choose a prioritization based on syntactic class, special-case per-ambiguity, etc.
2. `-` occurs as both infix and prefix operator; technically this ambiguity shouldn't be a problem; there is always one valid parse which minimizes grout insertion. Nonetheless, this currently manifests in remolding bugs such as #1076, which are sensitive to which order the two alternatives appear in in Forms.re.
3. `+` occurs as both infix and prefix operator too, though only for types, and in a way that isn't semantically ambiguous
4. `!` occurs as prefix and (as part of an) infix operator, though it currently only exists in infix ops as a leading character, so this ambiguity does not currently manifest
5.  `->` occurs as both infix and form delimiter; this is already a collision between function types and function literals; see bug #970)
6. `=` occurs as form delimiter (let expressions) and is potentially infix; if realized, this would cause a similar ambiguity to `->`
7. `=>` likewise occurs as form delimiter (case rules) and is potentially infix

The above examples suggest three severity classes with respect to syntactic ambiguity:
1. Technically ambiguous (e.g. `-` and `+`): While ambiguous, these always have one grout-minimal parse (I think). Internal bugs may cause the non-grout-optimal parse to be selected, but this is an implementation error
2. Ambiguous, resolvable by inserting whitespace (e.g. `.`): Not much of a problem in practice, though some effort should be spent to make these predictable.
3. Ambiguous, requires inserting disambiguating parentheses (e.g. `->`): More confusing and more effortful to resolve; should be avoided if possible, predictable if not. 

Other than the last class, none of these are _further_ problematized by the above allowed character list of user-defined operators, so this is mostly food for thought, except that existing symbolic form delimiters (`=`, `=>`, `->`) should probably be forbidden as user-defined operators

comments / disconcision / 2023-12-18T00:16:37Z
I did a functional review. There are still a few outstanding bugs, and a couple other things we should probably decide about. Going to reproduce the things I tried below for reference:
<img width="692" alt="Screen Shot 2023-12-17 at 7 00 57 PM" src="https://github.com/hazelgrove/hazel/assets/22436459/6c8939bb-be4b-44fe-8349-beef23963a69">

```#1. OK: dont shadow builtins#
let _*_ = in
let _!_ = in

#2. OK? Do we want to still bind failed operator defs? We do at the moment#
let _*--_ = 1 in
let _*---_ = fun x, y, z -> x + y in

#3. Bug: Should probably be a static error#
let _*-*-_ = fun x:Int -> 1 in

#4. OK: Constant operator. Pointless but fine#
let _*+*+_= fun x: -> 1 in

#5. OK?: Returns pair of inputs. Odd but fine I guess?#
let _*!*+_= fun x: -> x in

#6. OK? Runtime cast fail; not wrong but not ideal#
let _*---*_= fun x-> let a,b,c = x in a+b in
#Maybe we should require that unannotated ops analyze against (?,?)->?#
#This would make 3 and 6 static errors.#

#7. OK: Happy unannotated cases#
let _*----_ = fun x, y -> x + y in
let _+*_= fun x-> let a, b = x in a*b in

#8. OK? Notice error is localized to pattern here#
# It would be on definition if this wasnt an operator #
# This seems reasonable, but the message shown DOES involve the definitions#
# type. if were going to attribute the err to the annotation, i feel the#
# message should be more like "must be consistent with (?,?)->?" or something#
let _+***_: (Int, Int) = fun a,b-> a*b in

#9. OK: Annotated happy path #
let _*---*_: (Int, Int) -> Bool = fun a, b -> a < b in 

#10. Bug: All unnannoted operators trigger cast exceptions when used in tests:#
test 1+*1 == 1 end;

#11. OK: Use operator as fn#
_*---*_(4,4);

#12. OK? Maybe out-of-scope but would be nice to be able to do above w/builtins#
_*_(4,4)
```

Bugs:
- Unannotated ops defs which don't take a tuple should be static errors (see 3). I propose new logic in (6) which would catch this and maybe subsume the current logic. In summary, maybe the logic should be something like: For any operator definition, the definition must analyze against (?,?)->?. If this fails, then maybe we still want to bind the operator, permitting its use as a function if not an operator; maybe not though, I dunno. Further worth pointing out that this does complicated what we do in the annotated case. Naively we could simply make an operator pattern synthesize (?,?)->?. This would achieve the desired behavior in the unannoted case automatically; it even permits using an operator pattern as part of a composite pattern, e.g. defining multiple operators via a tuple. But the user could  problematically override this behavior by annotating the operator variable with less general types i.e. ? or ?->?. So it seems like we do need to retain a special error case for annotations on pattern variables. The question is how specific do we want to be; perhaps we should insist they be of the form (a,b)->c.
- There seems to be a casting bug for unannotated operators (see 10).

Things to decide:
- Should failed operator definitions (invalid type) still get bound in context (see 1)
- The 'identity operator', which just returns the pair of its inputs, feels slightly odd to me, but I don't think it's worth special-casing to avoid. (see 5)
- The error we put on bad operator annotations could maybe be more targetted (see 8)
- Would be nice to be able to use extant builtin (functional) ops as fns as well, but maybe not necessary for this PR (see 12)

comments / cyrus- / 2026-04-21T12:55:15Z
archiving since this is no longer active

reviews / cyrus- / 2023-07-30T20:59:30Z
I can't type `f` into the second hole here:
<img width="622" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/e1186201-8ab3-4e98-bf1f-19bf21cae84f">



## #1020 module system / gensofubi
created 2023-05-19T06:15:47Z merged None base dev
BODY (mutable, retrieved today):
Haz3l module system. 
Current progress: 
Type Module defined (with detailed information as name-type pair), keyword **module** and operator **.** implemented, 

Type annotation for modules implemented. Use a pair of curly parentheses around a tuple of patterns. Typically the tuple should contain only TypeAnn patterns, but Var/Tag will also be accepted and treated as hole-typed members.

Type Inconsistency warnings includes both the pattern (which define the member) and the definition expression. 
For member name inconsistency, accessing members shown in module's typeann but not defined will be treated as a emptyhole (supposing users are to implement later), accessing members defined but not shown in module's typeann will be treated as free variables.

![P~M0}3R$CFZ%9@ORYXX$NUH](https://github.com/hazelgrove/hazel/assets/71319371/b6f6e578-f190-48fe-86f3-f941ff630dce)

Basic Type member implemented. Type member in module type annotation implemented. 
For constructors defined by Sum types in module, either access directly by dot access, or access under analytic mode (dot access not necessary).

![8``TU` P}~5IH75ADL9NYMP](https://github.com/hazelgrove/hazel/assets/71319371/cc74ba19-a18b-468e-99f6-3337f6f50e49)

Provided warnings for using type members that are not defined, and inconsistency for type members. Created documentations for module-related keywords.



Some current rules of typing and casting:
Module type consistency: module types are consistent only if they share the same member name list, and the types of every member are consistent. Therefore, the ground type of a module is one where all members have hole types.

For module creation, the definition part will always be packaged as the exact same module type of the annotation as we mentioned amove. So nothing to worry about casting.

Casts will be added on module aliases. Cast calculation will happen on dot operators.

<img width="381" alt="0c7316442d59814e378104002eb3efb8" src="https://github.com/hazelgrove/hazel/assets/71319371/96a7d0b2-20ed-438e-8fa9-cc628e6fc83d">


comments / cyrus- / 2023-06-10T02:39:34Z
@gensofubi as you make progress on this, can you update the PR description documenting what is now possible

comments / cyrus- / 2023-06-29T19:51:06Z
@gensofubi there are a number of conflicts with `adt-defs-after` as well now - can you resolve those

comments / cyrus- / 2023-07-10T19:48:33Z
I can't press `.` here to turn this into `M.M.y`
<img width="465" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/0dbf9f9f-c269-4048-8602-4d93b52abc9f">


comments / gensofubi / 2023-07-14T02:18:24Z
The issues have been addressed.
Regarding the last issue, due to the current logic of insert, if a character is inserted into a valid token to make it invalid, it automatically splits into three tokens instead of considering the newly inserted character and the subsequent string as a new token. In order to make modifications without changing this logic, I have changed 'dot' to be an independent infix instead of being a suffix with the variable name that follows it (which also aligns better with the intuition of 'dot' as an operator). In this case, however, it is difficult to determine in static check whether the Exp after 'dot' is a Var/Tag or other constant expression, hence resulting in situations like 'M.(1) evaluates to 1' (I think this somehow makes sense).

comments / cyrus- / 2023-07-31T19:48:52Z
@gensofubi there is a conflict with `adt-defs-after` you should take a look at

comments / cyrus- / 2023-08-14T19:31:01Z
Additional small issue: in the example at the bottom, lets include a type alias, and also do not indent the last `in` by 1 space:
<img width="477" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/5ec9dc09-ef42-4f2e-aa2a-bf5601b3ded0">


comments / cyrus- / 2023-08-14T19:32:45Z
The langdocs message for a module type is also confusing -- the reference to floating point is a mistake, and think of a more clear way of stating the rest of the message using the same terminology used elsewhere / in OCaml (type alias and values)

<img width="464" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/abbbb006-f604-4486-8f7f-c521ccaed1b4">


comments / gensofubi / 2023-08-17T04:34:26Z
The issue has been resolved. Regarding the first issue, setting the sort for the Module used to access Typealias to Typ was a compromise to address the problem of the module being displayed in red font. I have now changed its form from 'Type variable' to 'Module path' and made modifications to the langdoc. Similarly, the capitalized tags as Exp and Pat, which were originally considered Constructors instead of Module variables, have also been corrected. Additionally, @cyrus- , should the syntax for the module type be changed from curly brackets to something resembling OCaml's style of 'sig ... end'? This was a temporary decision at the time, with a more C-like style rather than a Hazel-style.

comments / cyrus- / 2023-08-18T17:34:33Z
@gensofubi No, we're not trying to mimic OCaml syntax here -- the curly braces look good to me.

comments / Negabinary / 2023-11-27T15:38:26Z
![image](https://github.com/hazelgrove/hazel/assets/31668468/4aaff93d-27d1-4bc8-a190-aa5a488294f8)

I'm getting an error when I try to use modules on this branch now - I think it's a lang doc panel thing.

comments / gensofubi / 2023-11-27T15:51:43Z
@Negabinary Would you try resetting local storage? This happens when switching between branches.

comments / Negabinary / 2023-11-27T16:09:18Z
ah yes that worked thanks!! @gensofubi 


comments / cyrus- / 2024-02-05T20:16:59Z
@gensofubi 
1. This PR needs a merge with dev
2. When my cursor is on a projection, the context inspector seems to be showing the module signature rather than the context at that position in the code:
![image](https://github.com/hazelgrove/hazel/assets/280638/af70e8c8-3193-4ece-ac20-f82f34d72edc)
3. The ExplainThis description for dot says that you can put an arbitrary expression `e2` to the right of the dot, but it should in fact only be a label:
![image](https://github.com/hazelgrove/hazel/assets/280638/e2675251-0cd0-4ddb-a68e-91543852627d)
4. The cursor inspector message says that the type of a module binding is `?` which is consistent with its signature. This should just say its type is the signature, just like a let binding with no type annotation on it:
![image](https://github.com/hazelgrove/hazel/assets/280638/81e81873-7ea9-415e-a018-51eefdb002c7)


comments / cyrus- / 2024-02-05T20:26:04Z
Nested modules do not seem to be working correctly:
![image](https://github.com/hazelgrove/hazel/assets/280638/ab5dc3b9-6be9-4045-8c61-c7e30a03faaf)



comments / gensofubi / 2024-03-02T01:34:40Z
@Negabinary During my work I found a problem that later members might refer to the previously defined member variables. So instead of creating a map, I introduced an empty ModuleVal  in the elaborator, and let expression will expand it in the transition (as long as it found the body to be a ModuleVal). 
Current result: 
<img width="463" alt="{34989723-FB03-41fe-AD7D-DBBACA25BE24}" src="https://github.com/hazelgrove/hazel/assets/71319371/eac18cea-6cbb-448b-8e13-e58f93787efb">


comments / Negabinary / 2024-03-04T18:18:50Z
> @Negabinary During my work I found a problem that later members might refer to the previously defined member variables. So instead of creating a map, I introduced an empty ModuleVal in the elaborator, and let expression will expand it in the transition (as long as it found the body to be a ModuleVal).

Good point about the previously defined member variables! I like the fact that, using this method, the let expressions within modules work very similarly to normal let expressions too.

This evaluation order kind of suggests you could do something like this:

![image](https://github.com/hazelgrove/hazel/assets/31668468/3e9d654e-2559-4bc7-8103-8ee43697f67c)

but y doesn't seem to get captured by N in the evaluation at the moment. Does having N be M + y here make sense?

comments / gensofubi / 2024-03-16T22:40:42Z
> > @Negabinary During my work I found a problem that later members might refer to the previously defined member variables. So instead of creating a map, I introduced an empty ModuleVal in the elaborator, and let expression will expand it in the transition (as long as it found the body to be a ModuleVal).
> 
> Good point about the previously defined member variables! I like the fact that, using this method, the let expressions within modules work very similarly to normal let expressions too.
> 
> This evaluation order kind of suggests you could do something like this:
> 
> ![image](https://private-user-images.githubusercontent.com/31668468/309858402-3e9d654e-2559-4bc7-8103-8ee43697f67c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA2Mjg5NDcsIm5iZiI6MTcxMDYyODY0NywicGF0aCI6Ii8zMTY2ODQ2OC8zMDk4NTg0MDItM2U5ZDY1NGUtMjU1OS00YmM3LTgxMDMtOGVlNDM2OTdmNjdjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzE2VDIyMzcyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTEyZGYyZjJmYWM3YTAzNTczZTg1NmZlNDhlMDllYTI5ZDA2Yzg5NTA2MjEyZmI2MTM1YmU4MDBmMjIzZWVlOTgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.DmQZf9hhPcBNudEsACz1scZ4dN3LH70n7qFSWeAVzoI)
> 
> but y doesn't seem to get captured by N in the evaluation at the moment. Does having N be M + y here make sense?

I've done a few trials about this but found it tricky. To implement this, I need to evaluate the body expression of Let expression first, which is not the current practice. It may be easy to make exceptions for modules that are directly represented by labels, but it will be difficult for modules that are generated in more complex ways (such as functions).
Alternatively, a module union operator could be defined to achieve this functionality, but I'm afraid that might be too complicated. I'm currently considering modifying stepper's expression slightly to avoid this misleading intuition.

comments / cyrus- / 2024-03-18T00:23:55Z
The module body won't be a regular let expression after David's tylr refactor. We could fix it even now by defining a new sort for `ModuleExp` and use different keywords like `val` instead of `let`, but probably not worth the effort right now.

comments / cyrus- / 2024-03-30T00:34:16Z
The types being reported for member variables of modules seem to be inconsistent.

In the following, the type is `N.N` (expecting just `N` as long as the alias `N = N.N` is in scope):

```
module N = 
  type N = String in 
  let z : N = "Abc"  in   
in 
N.z
```

In the following, where the module is nested deeper, however, the type is `String` (I would expect either `M.N.N` or `M.N`):
```
module M =
  module N = 
    type N = String in 
    let z : N = "Abc"  in   
  in 
in 
M.N.z
```







comments / gensofubi / 2024-03-31T20:27:32Z
@cyrus- These issues have been addressed

comments / Negabinary / 2024-04-01T21:04:06Z
I finally understand some amount of casting, so I found a few casting bugs - they're pretty similar to some bugs I found recently in dev so they won't be too hard to fix but casting's always annoying...

![image](https://github.com/hazelgrove/hazel/assets/31668468/64101596-2760-4f75-8978-3c6e4ca19bef)

**Problem # 1:** This one is because of the definition of a ground type. Specifically ground types should have the property that if two ground types are consistent then they are equal.

e.g.   Int   &   Int               are consistent and equal     (fine)
        String & Int              are consistent and not equal   (fine)
        [?] & [?]                    are consistent and equal
        [Int] & [?]                 are consistent, but [Int] is not ground so this is fine
 
If you have a basic type like int, string, then it is ground, but if you have a more complex type like list, functions, sums or modules, then only the version that only has holes should be ground

i.e.    [?],   ? -> ?,  +X(?) + Y,  {T1: ?, T2:?}                              should be ground
but   [Int],   String -> ?,  +X(Int) + Y(?),   {T1:Int, T2:?}          should not be ground

you can think of the ground type as representing just the top-level type - i.e. we know it's a module but we don't know what kind of module it is.

**Problem # 2:** once you fix problem # 1, I think you'll find that this example doesn't show an error, but it does get stuck later. This is because of the "canonical forms" thingy in the appendix of the 2019 paper. I'll probably try and write it out in the codebase because a lot of us are tripping up over this, and it's kinda hidden at the bottom of that paper.

It would be nice if we could say "if it has type module, and it is a value, then it is a Module(...)"; unfortunately it's not quite that simple with casts...

"If it has type Int, and it is a value, then it is an Int(...)" is true. "If it has type [...], and it is a value, then it is a List(...)" is unfortunately not true. This is because the list might have some casts from [X] to [Y] outside it. When you try and open up a list you have to apply a cast from X to Y for every element before you can look inside. This is what I tried to do with the `unbox_list` function in Transition.re

"If it has type {...}, and it is a value, then it is a Module(...)" is also not going to be true. Once you fix problem # 1, the casts around module values will stop disappearing, and so now we'll have to deal with them. In particular if you have a module {x=4}:<{x:Int} => {x:?} > then when you access `M.x`, you need to add a cast to it and return `x<Int=>?>`

I know this stuff is complicated, and I barely understand it myself, so if you want to meet at some point to discuss I'd be happy to.

code for reproducing example:

```
module T = 
  let x = 5 in 
in
module S : {x: } = T in
module U : {x:String} = S in

U.x ++ "hello"
```

should evaluate to

FailedCast(5, Int, String) ++ "hello"

on an unrelated note:

![image](https://github.com/hazelgrove/hazel/assets/31668468/125d7b71-aeb0-4a7e-b7b1-1a25f121ca38)

idk whether the desired behaviour is to evaluate this or to get stuck with some sort of error message, but this evaluation is just hanging atm

```
module T = 
  let x = 5 in  
in
let s :   = T in
s
```



comments / cyrus- / 2024-04-12T19:06:12Z
marking as draft until above casting issues are resolved

comments / cyrus- / 2024-05-01T23:01:22Z
@gensofubi can you merge with dev when you get a chance

comments / cyrus- / 2024-05-01T23:02:35Z
Getting a strange run-time cast failure on this example:
![image](https://github.com/hazelgrove/hazel/assets/280638/c5fad32c-a45a-4af0-a0e6-710e9b1b2a11)


comments / Negabinary / 2024-05-09T13:43:23Z
Back with another type bug sorry!!!

An important property of type consistency is that it's a symmetric relationship. (A ~ B ⇔ B ~ A) and unfortunately that doesn't hold for modules at the moment. In particular `{x:Int}` is consistent with `{?}` but not the other way around.

At first it seems fine because whenever we need a `{?}` we can always use a `{x:Int}`, but the problem comes when you look at the type that a function takes. (This problem is more generally called covariance and contravariance https://en.wikipedia.org/wiki/Covariance_and_contravariance_(computer_science); but we in Hazel avoid it entirely by making consistency symmetric)

```
let f : {x:Int} -> {x:Int} = fun M -> M in
let g : {?} -> {x:Int} = f in
```

This type checks fine because `{x:Int}` is consistent with `{?}`; but if you look at what the function `g` now does, it allows us to use any module as an `{x:Int}`.

Here's an example where I've tricked the type checker into letting us use {y=4} as an {x:Int} using this g function:

![image](https://github.com/hazelgrove/hazel/assets/31668468/c68ca86a-5ffd-4a68-af3c-3f53780fb588)

```
let f : {x:Int} -> {x:Int} = fun M -> M in
let g : { } -> {x:Int} = f in

module M =
  let y = 4 in 
in

g(M).x
```

comments / Negabinary / 2024-05-20T19:44:34Z
Looks good now! I wasn't able to find any more casting bugs - not letting users define rho types feels like a good practical workaround for things like {x:?, …}->{x:?, y:?}->{y:?, …} for now.



comments / cyrus- / 2024-05-30T04:48:37Z
@gensofubi reviewing now, but there is a merge conflict when you get a chance

comments / cyrus- / 2024-07-25T21:13:11Z
@gensofubi I'm a bit confused about what is the difference between a let binding with a module signature in the type position and a module binding. The error message in this screenshot is quite confusing:

<img width="1050" alt="image" src="https://github.com/user-attachments/assets/46534b2f-276c-45c1-aa98-03395d9674ad">


comments / disconcision / 2024-08-17T20:18:04Z
@cyrus- syntax notes / questions:

1. Is the only reason for a separate 'module' definition form to avoid ambiguity with a let which uses a nullary constructor as its pattern?
2. What is your view for what a 'hazel program' should be in the world tree model? i.e. if i just want to start writing some code without regard for interface, what is my top-level? am i implicitly (or explicitly) wrapped in a module (with some placeholder name)? or implictly in some kind of block form?
3. remind me about your position on the existing pseudo-top-level definition forms (let .. in and and type .. in). do we want to separately retain (both) these? if new scratch pads as per 2 are module-wrapped, then it seems at least that we don't strictly need a pseudo-definition type form any more. (unless we're keen on retaining the ability to define types inside functions, AND are not also replacing function bodies with some kind of curly-braces form)
4.  As per the last point, it feels to me like you can basically also use curly braces to create pseudo-top-level definition contexts which would obviate the need for separate let..in, but at the cost of maybe creating some pseudo-ambiguous edge cases between module and function definitions (pursuant on above selections). 

For concrete illustration here's a version of the contents of a scratch pad which:
1. retains separate module def form
2. is implicitly module-wrapped, or implicitly block-wrapped... doesn't seem to make a difference in this model 
3. removes existing let..in and type..in forms
4. introduces a curly-braces block form which is interpreted as a block unless it's the body of a module definition form. semantics are: returns the value of the trailing expression, if any, or null if there's a trailing definition form.

```
module M : {
  type T = Int;
  let x : T;
  let y: T
} = {
  type T = String;
  let x = "yo"
};
type R = String;
let f: Int -> R = fun x -> {
  let q = string_of_int(x);
  "q: " ++ q
};
f(4)
```

in the above module blocks and non-module blocks are both semi-colon separated lists of convex forms, including prefix-shaped definition forms (ie the semicolon is not part of let/type) taking a right unidelimited child. i've opted against having an optional trailing semicolon, but this seems possible if-desired.

the above is almost achievable using the current syntax model... the only thing not trivially doable is the `let` in the module signature. if that's not possible, we could temporarily replace it with val/var/whatever.

Anyway I know the above is a bit different than we talked about, but I'm not totally clear on what your exact preferred model is, so this is intended as starting point for discussion. My goals are to (within reason) stem keyword proliferation and avoid having incidentally-different ways of doing the same thing. But I'm also ~ fine with keeping let...in and using var/val/whatever for the block-level let.

I'm curious if there's a reasonable way of finessing block versus module forms in some way which obviates the need for a separate module definition keyword, assuming some other solution were found for the constructor issue above. like perhaps curly braces is a module IFF there trailing item is a definition. Perhaps not a good idea though, would have to guard against weird error message when you accidentally do this when defining a function etc.

comments / disconcision / 2024-08-18T02:18:31Z
<img width="985" alt="Screenshot 2024-08-17 at 10 05 42 PM" src="https://github.com/user-attachments/assets/f9b13891-9257-48fa-8929-14c12a86fa23">

after messing around a bit i think it'd be possible (with several days of work) to get syntax in the screenshot to work (without the sort errors currently displayed). of the four issues described in the comments i know how to reasonably fix three of them, and the other seems like it must be straightforwardly possible, though not immediately obvious to me.

this uses "typ" and "val" and as such retains the old "type" and "let" without change. "typ" needs a better name if we're going to keep these as alternates and retain the existing forms; i still think it's a better idea to ditch the old ones and let typ be type and val be let.

iirc you were talking about the option of making the forms like ["let", "=", ";"] as opposed to the infix ";". I experimented with this; there doesn't seem to be any good way unless we make a subsystem where multi-delimiter forms can change to other multi-delimiter forms. i.e. we need `module M: {typ T=Bool|}` to be grow a semicolon if we want to add more definitions etc. seems like a bit more work than the other option with advantages unclear to me at the syntax level. as an alternative we could perhaps pretend that things are like this for maketerm parsing and indication decoration purposes (as we pretend for list lits and cases).

comments / 7h3kk1d / 2025-03-10T19:51:57Z
I'm curious how having fully first-class modules will allow for type-abstraction in the future. Naively it seems like figuring out type compatibility between abstract types would require evaluation?

comments / gcrois / 2025-03-10T22:02:53Z
Some notes from a discussion today: https://github.com/hazelgrove/hazel/discussions/1558

comments / cyrus- / 2026-04-21T12:55:41Z
added via an alternative design, inspired directly by this PR. thanks @gensofubi 

reviews / cyrus- / 2023-07-10T19:45:08Z
error message for an invalid module name shouldn't say "invalid token", it should say "invalid module name" 
<img width="692" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/e0a4eef3-4e1e-450a-9fdb-93554270b39e">

also in above screenshot, the DHExp display for a module isn't very helpful -- it would be better to actually give all the evaluated values for the module members instead of just saying `Module`.

reviews / cyrus- / 2023-08-14T19:29:06Z
<img width="1502" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/73c4adb3-8bf8-4525-bb51-8fd7e880115f">
The way the module type is formatted in the cursor inspector message at the bottom is different than how module types are actually written in the surface syntax -- let's change the cursor inspector print to use curly braces and the same syntax.

In addition, in the cursor inspector it says that the sort of `M` is Typ and its form is "Type variable" which is not correct -- M is a module variable, and its sort should be something like "Module Path". Same issue in the lang docs sidebar.


reviews / Negabinary / 2023-11-27T17:20:43Z
Looks pretty close to ready to me! I've added a few small comments around the place. You've been working on Hazel a lot longer than me so please do push back on any of my comments. I don't yet know enough to fully read the statics section. 

reviews / Negabinary / 2024-03-04T20:59:55Z
I think we need a way to show off all the cool features of this pr - I keep discovering new things you can do when looking through your code, like you can make functors by just having a function that takes a module and returns a module - that's awesome!

I wonder if making a "Modules" documentation example would work? (similar to how "Basic Reference" shows off most of the features and "ADT Dynamics" shows off the features of ADTs) Then, a programmer could scan through and see all of the things they can do with modules. I'd think it would include at least type definitions, variable definitions, type accesses, variable accesses, using just the module name as a type, module type annotations, how to write functors - but there's probably more cool things I still haven't found yet too

review-comments / Negabinary / 2023-11-27T16:16:58Z
It's a bit confusing to have the type name and module name be the same here.

review-comments / Negabinary / 2023-11-27T16:37:44Z
This might be better as a ClosureEnvironment.t (like in Closure()), `ClosureEnvironment` s are pretty much exactly the same as ClosureEnvironment.t, but can be compared quicker, which might be useful for bigger modules.

review-comments / Negabinary / 2023-11-27T17:10:42Z
I don't understand enough about Hazel statics yet to actually read this file - but I've had a play around on the editor

```
type U = {g:Int} in
let f : Int -> U = fun x -> 
  module T = 
    let g = x in 
  in
  T
in
f(4)
```
works but
```
type U = {g:Int} in
let f = fun x -> 
  module T:U = 
    let g = x in 
  in
  T
in
f(4)
```
gives a weird `T not found` error


review-comments / Negabinary / 2023-11-27T17:13:29Z
I think the   `|> ClosureEnvironment.of_enviornment |> ClosureEnvironment.map_of` is redundant here

review-comments / gensofubi / 2023-12-04T04:45:09Z
Thanks for the feedback! Here I’m to show a special feature in Hazel Module: its inner type member with the same name as the parent module can be directly used without dot access. This is for convenience since we expect most module to have methods working on one specific type (like the type T in most Reason module). I'm still considering how to state this in brief and clear words in the document.

review-comments / gensofubi / 2023-12-04T04:45:20Z
Probably because old ClosureEnvironment doesn't support some methods. Now changed to ClosureEnvironment. Thanks!

review-comments / gensofubi / 2023-12-04T04:45:40Z
Seems that modules annotated with typevars are not correctly recognized. Resolved. Thanks!

review-comments / gensofubi / 2023-12-04T04:45:52Z
Resolved. Thanks!

review-comments / Negabinary / 2023-12-04T18:19:45Z
ooh that's a nice feature! Using M makes more sense now but yeah I agree it might need some more explanation.

review-comments / Negabinary / 2024-03-04T19:23:08Z
This bit goes off the screen on my computer - maybe add a few newlines

![image](https://github.com/hazelgrove/hazel/assets/31668468/dbe90262-afb8-40a5-ace3-c4e988ea08b6)


review-comments / Negabinary / 2024-03-04T19:24:09Z
"The variables defined in definition _are_ defined"

review-comments / Negabinary / 2024-03-04T19:25:04Z
oh maybe also mention types as well as variables

review-comments / Negabinary / 2024-03-04T19:27:12Z
colours are the wrong way round here

review-comments / Negabinary / 2024-03-04T19:28:48Z
colours wrong here too

review-comments / Negabinary / 2024-03-04T19:28:50Z
I think this example is missing an 'in'

review-comments / Negabinary / 2024-03-04T20:19:54Z
This file looks good to me - one question I had, see https://github.com/hazelgrove/hazel/pull/1020#issuecomment-1977190297

I think we'll want to eventually have an option where you can hide all steps that occur inside module bodies, but we can probably do that after this pr.

review-comments / Negabinary / 2024-03-04T20:35:50Z
The hole at the end of the module still really bugs me - I wonder whether @dm0n3y has any ideas for how to get rid of that hole?

review-comments / Negabinary / 2024-03-04T20:53:44Z
![image](https://github.com/hazelgrove/hazel/assets/31668468/2ae4ea1b-e6b1-4ca5-8691-58916c3e8f14)

```
let functor = fun X:{Type T = Int} ->
  module F =
    type T = [X.T] in 
  in
  F
in
module V =
  type T = String in 
in
module U = functor(V) 
in
let f: U.T = 3 in
f
```

ok so two things:

1. in line 10, `module U = functor(V)` it says 
![image](https://github.com/hazelgrove/hazel/assets/31668468/7163eab8-6585-404c-88ed-c73131ab7c6a)
but I think they should be inconsistent

2. on line 12 `let f: U.T = 3 in` it says 
![image](https://github.com/hazelgrove/hazel/assets/31668468/d1d9294b-8f0e-422b-879d-058bee1fd56f)
is this right? I'm not sure what the desired behaviour would be here.


review-comments / Negabinary / 2024-03-06T21:06:17Z
I was discussing modules with @LighghtEeloo yesterday and he pointed out that the modules here are kind of like delimited closures - the contents of the module is everything that is defined "outside" of the hole, but it's delimited because it only captures things "inside" the module keyword. In that sense, it's nice to have a hole to show that that's what the module is.

So another idea to consider is maybe keeping the hole at the bottom of the module but making it look different to make it clear that this is the location that's going to be 'captured' by the module?
![image](https://github.com/hazelgrove/hazel/assets/31668468/a64747a1-073c-4d2c-bbfc-f9674707c26c)
  

review-comments / gensofubi / 2024-03-18T02:57:04Z
1. resolved
2. I think U.T is expected to be [Int] here? 
btw making a note of new bug discovered when fixing this: The newlines in the module in the results will cause the position of the red box to shift

review-comments / Negabinary / 2024-03-21T20:11:21Z
oh yeah, my bad on (2.)


## #1056 Let operators / xzxzlala
created 2023-06-27T20:20:27Z merged None base dev
BODY (mutable, retrieved today):
We can now define let-operators(let+, let*, let-) and use them.
![image](https://github.com/hazelgrove/hazel/assets/73332800/5fbab34a-e216-4364-81af-6338531de76d)
If the let-operator is not defined by user, a warning message will show. 
![image](https://github.com/hazelgrove/hazel/assets/73332800/5d44418a-e421-4a58-8a54-36dc2ea9e55a)

About what part of the code I modified:
1, Developed from user-defined-operators branch, extend the user-defined-operators, I revise the regexp to contain the operators start with "let".
2, add let*, let-, let+ as forms. 
3, statics and dynamic of LetOp(op, pat, def, body), where "op" is a string indicating which let-operator is used. "pat", "def", "body" is just the same as Let(pat, def, body).

comments / disconcision / 2023-07-18T21:45:51Z
why is the undefined let operator error a dynamic error instead of a static error?

comments / xzxzlala / 2023-07-19T22:14:07Z
I remove the dynamic error and add the static error. 
<img width="504" alt="image" src="https://github.com/hazelgrove/hazel/assets/73332800/0c834d90-c5c6-494f-a36f-44d0b864083a">


comments / cyrus- / 2023-07-30T21:19:30Z
Since this is based on the user-defined operators, can you change the base branch of this PR to that branch? There are also potential conflicts that need to be resolved.

comments / cyrus- / 2023-07-31T20:00:28Z
@xzxzlala see also conflicts with `dev` that need to be resolved.

comments / xzxzlala / 2023-08-03T18:19:26Z
I merged dev and user-defined-operators(set origin/haz3l-user-defined-operators as upstream).
The annotation bug is a bug of user-defined-operators, I'm still trying to find a solution.

comments / cyrus- / 2023-08-18T17:56:35Z
Marking as draft pending merge of #1012 

comments / cyrus- / 2024-05-28T02:38:53Z
@xzxzlala I think this should be ready to merge -- do you have time to resolve the last merge conflicts?

comments / Negabinary / 2024-05-28T13:43:52Z
I'm wondering whether it might be good to add a static error as well for undefined let operators, since it can be determined at compile-time whether a let operator is in scope?

comments / Negabinary / 2024-05-28T15:58:02Z
> I'm wondering whether it might be good to add a static error as well for undefined let operators, since it can be determined at compile-time whether a let operator is in scope?

Sorry I didn't notice Andrew had already brought this up - is there a reason we've gone back to dynamic errors?

comments / cyrus- / 2024-05-28T17:58:00Z
Oh yeah, I thought that is what we had done but seems it is still a dynamic error. @xzxzlala do you have time to make this a static error?

comments / xzxzlala / 2024-06-17T12:52:04Z
No problem! 
I could work on it. Sorry for the late reply, I didn't see the message because I had to use VPN to check my Gmail messages.
However, I'm now quite busy with graduation/capstone design. Maybe need more time :)

comments / cyrus- / 2026-04-21T12:56:50Z
archiving because this is no longer an active effort, but want this in a future PR

reviews / cyrus- / 2023-07-30T21:27:32Z
It isn't working correctly when the let+ definition is annotated with a type hole:
<img width="812" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/7574aeb6-1dde-47a6-946d-c4c98a5e5d20">



## #1060 Transpiler from Hazel to Roc / yujiagao-audrey
created 2023-07-04T01:57:52Z merged None base dev
BODY (mutable, retrieved today):
Merged the recent commit of dev branch and ready for review. 

comments / cyrus- / 2026-04-21T12:56:11Z
not going to maintain a Roc transpiler, but thanks for the effort on this @yujiagao-audrey 

reviews / cyrus- / 2023-07-20T00:59:59Z
- move all the Roc-related things into a new top-level library alongside haz3lcore called `haz3l-roc-transpiler` rather than putting it in statics. It can call into `haz3lcore`.

(partial review)

review-comments / cyrus- / 2023-07-18T17:56:16Z
looks like latest version of Roc doesn't have this issue anymore (at least on https://www.roc-lang.org/repl)

review-comments / cyrus- / 2023-07-18T17:56:29Z
we now need to add quotation marks here in latest `dev`

review-comments / cyrus- / 2023-07-18T17:57:12Z
document what the purpose of `i` is here

review-comments / cyrus- / 2023-07-20T00:55:00Z
instead of emitting a String here, define an `UnsupportedInput` exception and raise it in these cases

review-comments / cyrus- / 2023-07-20T00:57:14Z
instead of using a wildcard pattern here, it is good practice to list all the possibilities so that if something new is added to the language that requires indentation, the exhaustiveness checker forces consideration of what should happen here

review-comments / cyrus- / 2023-07-20T00:57:31Z
also, does a match not require indentation? or is it only nested lets?

review-comments / cyrus- / 2023-07-20T00:58:17Z
can you add a comment explaining why you need to check the indent flag here? maybe with an example showing the issue

review-comments / cyrus- / 2023-07-20T00:58:27Z
same here


## #1084 parameterized types / xzxzlala
created 2023-08-18T20:56:43Z merged None base dev
BODY (mutable, retrieved today):
Based on branch poly-adt-after2, I implemented the parameterized types. 

- I merged the forall type and typAp/typFun.

- Add the forms tpatAp and let the var could appear in tpat and typ.

- Add a new type "Ap" and its rules.

- Add the statics of the parameterized types. (tyalias of Ap)

- Revise the pattern match rules in evaluator to fit the "Forall" constructors.


![SV0UKX3G7YF4TI5VMINYP0A](https://github.com/hazelgrove/hazel/assets/73332800/d33d9a79-06be-417c-895f-24593ca929ff)



Here is an example of the parameterized types.
Note that the type of constructor of the parameterized types is Forall type, so we need to first use @<> to apply the type. 


comments / cyrus- / 2026-04-21T13:01:50Z
way out of date at this point, so archiving for reference in a future effort


## #1117 Query-based Accessibility  / coned
created 2023-09-30T21:53:51Z merged None base dev
BODY (mutable, retrieved today):
This is an initial design for improving the accessibility of the Hazel programming environment. It will contain a vim mode style query. User moves the cursor and inputs the command to get the results.


## #1118 Breadcrumb bar / xzxzlala
created 2023-10-08T23:13:26Z merged None base dev
BODY (mutable, retrieved today):
Breadcrumb bar of hazel. 
Now merged the haz3l-module branch. 
could show the current function/module you are in, and the droppings contains other same level functions/modules.
The level is decided by how many funs/modules you are in.
For example, below the cursor is in f1 and g3 and finally in M2:
![@Q1Y9HR T$6V0UT`E}{F3UP](https://github.com/hazelgrove/hazel/assets/73332800/734f3c42-2fc7-41a3-acd2-5e69083f5d15)


comments / cyrus- / 2023-12-05T01:57:03Z
@xzxzlala this needs a merge now

comments / cyrus- / 2023-12-05T01:58:22Z
@disconcision can you do a style pass on this? (really this is meant for down the line when we have a module view)

comments / disconcision / 2023-12-05T04:36:12Z
how about something like this? 

<img width="483" alt="Screenshot 2023-12-04 233516" src="https://github.com/hazelgrove/hazel/assets/22436459/99421b7e-2d07-41fa-af98-17d3005c5499">

(we should also just stick those icons in the nut menu)


comments / cyrus- / 2023-12-11T02:23:23Z
> how about something like this?
> 
> <img alt="Screenshot 2023-12-04 233516" width="483" src="https://private-user-images.githubusercontent.com/22436459/287919292-99421b7e-2d07-41fa-af98-17d3005c5499.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDIyNjE2NzcsIm5iZiI6MTcwMjI2MTM3NywicGF0aCI6Ii8yMjQzNjQ1OS8yODc5MTkyOTItOTk0MjFiN2UtMmQwNy00MWZhLWFmOTgtMTdkMzAwNWM1NDk5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjExVDAyMjI1N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTcxYTliMzg3ZTliNjgyNTU0OTJkZDI4NjY4ODQzNzNlZjgyM2M2NTljNGExYTBjMWJmYjdmMTYzN2ZlMjRkMzUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.5n5CmTLa9KGE7wA0Tfm0qJpja2rUgH2-jbGf3y8ZqBs">
> (we should also just stick those icons in the nut menu)

yeah this looks good!

comments / cyrus- / 2023-12-11T02:24:10Z
@xzxzlala I think we actually want to include let bindings of regular values, not just functions, in the list + we want to show siblings of the current position, even at the top level. we can have a special "dot" location for when you aren't on a binding.

comments / xzxzlala / 2023-12-11T02:38:35Z
> @xzxzlala I think we actually want to include let bindings of regular values, not just functions, in the list + we want to show siblings of the current position, even at the top level. we can have a special "dot" location for when you aren't on a binding.

Sure, I will add the "dot" for cursor not in bindings. 
I'm a little bit confused about using let binding of regular values. Won't that lead to lots of levels (fill all the room for top bar)?

comments / cyrus- / 2023-12-11T02:40:30Z
> > @xzxzlala I think we actually want to include let bindings of regular values, not just functions, in the list + we want to show siblings of the current position, even at the top level. we can have a special "dot" location for when you aren't on a binding.
> 
> Sure, I will add the "dot" for cursor not in bindings. I'm a little bit confused about using let binding of regular values. Won't that lead to lots of levels (fill all the room for top bar)?

It will add more items to the dropdown but it shouldn't increase the horizontal width much since that is based on depth -- it isn't common to nest let bindings very deeply.

comments / xzxzlala / 2023-12-11T02:43:29Z
> > > @xzxzlala I think we actually want to include let bindings of regular values, not just functions, in the list + we want to show siblings of the current position, even at the top level. we can have a special "dot" location for when you aren't on a binding.
> > 
> > 
> > Sure, I will add the "dot" for cursor not in bindings. I'm a little bit confused about using let binding of regular values. Won't that lead to lots of levels (fill all the room for top bar)?
> 
> It will add more items to the dropdown but it shouldn't increase the horizontal width much since that is based on depth -- it isn't common to nest let bindings very deeply.

I see, I misunderstand that. We want all other regular values to be siblings in same level and when in the body of new functions/modules we add another level. 

comments / cyrus- / 2023-12-11T02:45:52Z
There would be a new level whenever one binding is nested in another, so also in 

```
let x = 
  let y = 2| in 
  y + 1
in 
x
```

comments / disconcision / 2023-12-11T06:09:52Z
k i'm good to restyle if you want. when this is current with dev i'll branch off and do the restyling, then PR against this

comments / cyrus- / 2024-02-27T20:16:12Z
Seems to be quite buggy right now -- try moving around the following program:

```
let x = 2 * 3 in 
let y = 3 * 4 in 
let z = 2 * 3 in 
x
```

It should indicate `x` only when in the expression `2 * 3` but it indicates `z` there. Similar issues elsewhere.
 

comments / cyrus- / 2026-04-21T12:59:53Z
this needs to be reworked on top of the latest updates to Hazel including the new module system implementation, so archiving. thanks for the design @xzxzlala!

reviews / Negabinary / 2023-11-09T16:37:33Z
Cool demo yesterday!!

review-comments / Negabinary / 2023-11-09T16:05:09Z
Having the breadcrumb_bars property in settings feels unintuitive to me - it's not like the other settings. I wonder whether this could be implemented using a <select> tag like how the scratch/examples/excercises button is implemented.

review-comments / Negabinary / 2023-11-09T16:07:54Z
It's best to stick to the case convention for constructors of the other files and call it `BreadcrumbBar` instead of Breadcrumb_bar

review-comments / Negabinary / 2023-11-09T16:21:37Z
Generally in ReasonML we try to avoid using arrays, and use lists instead - it's because adding "mutability" makes it easy for errors to creep in - not that any mutability errors have crept in here, but just for a general rule.

review-comments / Negabinary / 2023-11-09T16:23:10Z
Try typing just `fun x -> 5` into the hazel editor

review-comments / Negabinary / 2023-11-09T16:25:35Z
This will throw an error if someone has 11 nested functions (though anyone writing an 11th nested function probably deserves to have the editor give up on them because their code is too ugly...)

review-comments / Negabinary / 2023-11-09T16:26:43Z
missing a border-left here

review-comments / Negabinary / 2023-11-09T16:27:07Z
is the rounded edge on just one corner intentional?

review-comments / Negabinary / 2023-11-09T19:11:51Z
\* using a `<select>` tag

review-comments / xzxzlala / 2023-11-12T03:28:50Z
I just copy it from context-inspector where the top-right corner is the only corner not close to other frame. So here maybe I should rounded two bottom corner.

review-comments / xzxzlala / 2023-11-12T03:29:51Z
Thanks! Added :)

review-comments / xzxzlala / 2023-11-12T03:30:48Z
After I change into list, it doesn't need a fix integer to limit the nested functions. 

review-comments / xzxzlala / 2023-11-12T03:33:09Z
Hazel crashes because it has no ancestor and I perform a List.hd. 
Now I first check whether ancestors is empty.

review-comments / xzxzlala / 2023-11-12T03:34:35Z
Fixed

review-comments / xzxzlala / 2023-11-12T03:41:44Z
Thanks! I didn't notice that

review-comments / xzxzlala / 2023-11-12T04:37:07Z
Wonderful suggestion! It not only enables me to not adding property in settings, but also give a selecting window(html/ccss) for user to select which is a better UI than the one I designed without any consideration :)

review-comments / Negabinary / 2023-11-13T21:48:59Z
Sorry, another annoying little detail!! For pattern matching over expressions like this we like to write out every case, instead of having a catch-all "_  => ..." so that if anyone else adds anything to the language, the compiler will force them to update this function.

review-comments / xzxzlala / 2023-12-05T00:57:50Z
For the code review, could someone take a look at this function("filter_ancestors") and give me some suggestions?
this function is very ugly, but I'm not sure whether there is a better way.
I try to filter the unrelated ancestors in this function by letting only the closest ancestor be the ancestor of the cursor at that level and then recursively deal with next level.
For the other cases needed to be recurse, they have exactly same code :(


review-comments / Negabinary / 2023-12-05T21:37:45Z
sure, here's a couple tricks that might help:

1. you can combine patterns when pattern matching
2. you can add a "when" to pattern matches as well

so this whole thing could probably become just one pattern match with four cases

```reason
switch (Id.Map.find_opt(List.hd(ancestors_lst), info_map)) {
  | Some(Info.InfoExp({Fun(_), ancestors, _})) when List.length(ancestors) >= 1 => [ ... ]
  | ...
``` 



## #1125 Dynamic layout for inexhaustive case/indeterminately match case / pigumar1
created 2023-10-22T16:22:26Z merged None base dev
BODY (mutable, retrieved today):
This pull request implements the functionality of visually crossing out mismatched rules during evaluation. It's possible for the evaluation of an **indeterminately exhaustive case expression** to get stuck when we cannot determine whether a rule is matched or mismatched. In this case, the rules preceding this rule are crossed out.
![image](https://github.com/user-attachments/assets/f4bf8ee8-9986-4717-be66-a38107d310a5)


comments / cyrus- / 2024-07-25T19:06:49Z
@pigumar1 I don't recall the precise purpose of this PR -- what is it and what is the status?

comments / pigumar1 / 2024-07-27T13:54:12Z
> @pigumar1 I don't recall the precise purpose of this PR -- what is it and what is the status?

@cyrus- I have updated the purpose of this PR at the top. The expected behavior has already been implemented, but some code simplifications can be done, as suggested by the comment above. #1154 was introduced for this code simplification, but it has its own relevant concerns, which are mentioned at the top of that PR.

comments / cyrus- / 2026-04-21T12:58:44Z
archiving since this is no longer an active project, but thanks for the design @pigumar1 !

reviews / cyrus- / 2023-11-18T20:37:12Z
see comment -- I think we can unify the case constructs here rather than implementing a third variant

review-comments / pigumar1 / 2023-10-23T16:22:08Z
Not problematic for now since currently `DHExp.InexhaustiveCase` behaves exactly the same as `DHExp.InconsistentBranches`

review-comments / cyrus- / 2023-11-18T20:36:15Z
Instead of having three different case constructs in DHExp, let's merge them into one with an additional flag parameter for when there is an error.


## #1139 inexhaustive pattern examples in error messages / karananand01
created 2023-11-15T01:47:01Z merged None base dev
BODY (mutable, retrieved today):
This pull request aims to produce a more verbose error displayed by the implementation of the exhaustiveness checking feature mentioned in “Live Pattern Matching with Typed Holes (https://victoryyw.github.io/assets/pdfs/pattern.pdf)”.

If a case expression is necessarily inexhaustive (i.e.: the expression will necessarily fail to match all values of the type of its scrutinee), the expression will be wrapped with an error hole like in Fig. 2b in the paper. This is done by using an error_exp called InexhaustiveMatch (created in #1114), which behaves uniquely when supplied to CursorInspector.re. We aim to supplement the produced error hole to display a pattern that can be produced by the case expression’s scrutinee but is not matched by any of the branches of the case expression.

This is planned to be done by utilizing the final constraint generated to produce the inexhaustive error and inverting it ( using the dual of the constraint ). The inverted constraint should include patterns that are not matched and therefore we can map the constraint to a pattern to be displayed on the error interface. 


comments / pigumar1 / 2024-01-13T09:29:20Z
Theoretical(?) basis:
A case expression is necessarily exhaustive => (its corresponding final constraint |> truified |> dual) is inconsistent => no values of the given type satisfy it

A case expression is necessarily inexhaustive => some value(s) of the given type satisfy it => there is some non-empty subset of final expressions of the given type that does not satisfy the final constraint, but satisfies its dual.

Next we will show (**inductively**) that for a consistent dual (sometimes represented as a list of constraints here), there is always some constraint that, obviously, can be emitted from a single pattern that once that constraint is satisfied, the entire dual is satisfied. 

`Hole` constraints are truified, and `Falsity` constraints shouldn't appear. For simplicity, `Truth` constraints and repeated constraints are removed.

Base case 1: the dual is a `Truth` constraint (the case expression has no branches at all). Any pattern of the given type can be used to satisfy the dual.

Base case 2: the dual is a conjunction of `Int`/`NotInt` constraints.
For such dual to be consistent, the list should have at most 1 `Int` constraint, and others (if any) should be `NotInt`.
* If there is exactly one `Int` constraint in the list, that constraint must be the one that if satisfied, the whole dual is satisfied. If we pick a different integer, it cannot satisfy that constraint, not to mention the entire dual.
* (credit: @DavidFangWJ) If there is no `Int` constraint in the list, all the constraints in the list are going to be `NotInt`. We can pick an integer that is one larger than the largest integer among all associated with the `NotInt`s, which satisfies the dual. We can construct an `Int` constraint with it to denote this fact.
* The same thing works for `Float`/`NotFloat` constraints and `String`/`NotString` constraints.

Recursive cases:
`And` constraint: can always be destructured to a list of constraints.
![image](https://github.com/hazelgrove/hazel/assets/108375845/7695c10d-7eb5-412f-9892-67e876466856)

`Or` constraint: for such dual to be consistent, there must be a constraint such that once it's satisfied, at least one of the "subconstraints" of the `Or` is satisfied, and it can be used to satisfy the entire dual.

The dual is a conjunction of `InjL` constraints: there must be some constraint `xi` s.t. if it's satisfied, all the "unwrapped constraints" are satisfied:
![image](https://github.com/hazelgrove/hazel/assets/108375845/09286602-6655-4bd2-99e6-18837d5e0337)
And `InjL(xi)` is the constraint that once satisfied, the entire dual will be satisfied.
The same thing works for `InjR` constraints.

The dual is a conjunction of `Pair` constraints: there must be at least one constraint `xi1` s.t. if it's satisfied, the "0th projection constraint" is satisfied. And there must be another constraint `xi2`. And `Pair(xi1, xi2)` is the constraint that once satisfied, the entire dual will be satisfied.

comments / pigumar1 / 2024-01-13T10:27:27Z
If the basis above works, the next step would be to reverse the auxilliary constraint into a `UPat.term` based on the type, and the further step would be to display it in the cursor inspector instead of the console.

comments / cyrus- / 2024-02-10T20:51:25Z
I am unable to actually edit case expressions effectively in this branch, e.g. can't press backspace here and various other similar situations:
<img width="1545" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/8a891cd5-3c8d-4d0d-ba41-3c6e83a9869b">


comments / cyrus- / 2024-02-10T20:54:34Z
For when I do get it to work, we need to think about the UI design for large error messages like these where the message gets cut off. Maybe a toggle that makes the bottom bar larger to show the full message when it exceeds the length of the display? Thoughts @disconcision ?

<img width="1187" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/0551a09a-f40a-4b08-b96b-6b8435ff7d60">

Also, given the above problem is solved, how hard would it be to list all of the cases that aren't matched, rather than just one example?


comments / disconcision / 2024-02-15T04:27:07Z
@cyrus- to start maybe have a short and long version of messages, with the short version having some affordance at the end e.g. ellipses indicating there's more. clicking on the affordance, or maybe just anywhere in the message part of the bar, could cause the bar to expand to take up more lines. clicking again makes it a single line again.

similarly but alternatively, you could make the bar's expanded state triggered on hover, and while hovered, show an additional pin icon that could be pressed to make the expanded state stick until unpinned.

(for this particular error, it would be nice if we could eventually show it inline... an 'angry ghost' of an unhandled case below the last case)

extremely rough mockup:
![hazel longer ci mockup](https://github.com/hazelgrove/hazel/assets/22436459/b6a17c7b-061b-4aad-bb72-3d21f398c132)



comments / cyrus- / 2024-07-25T19:05:32Z
@pigumar1 this PR needs to have a few merge conflicts fixed + better UI for long messages as @disconcision mentioned above. do you have time to take a look? if not, let me know and I can have someone else finish this up.

comments / pigumar1 / 2024-07-27T06:44:21Z
> @pigumar1 this PR needs to have a few merge conflicts fixed + better UI for long messages as @disconcision mentioned above. do you have time to take a look? if not, let me know and I can have someone else finish this up.

@cyrus- I don't think I have enough time for the better UI, since I'm not familiar with UI stuff...
I'm in the process of resolving those merge conflicts. One issue I encountered is that, do we need to also have inexhaustive pattern examples for **irrefutable positions**? There are some subtleties such as a let expression with the pattern annotated with unknown.

comments / cyrus- / 2026-04-21T13:00:30Z
implemented on top of the new coverage checker in a separate PR, but thanks for the work on this @karananand01 !

review-comments / pigumar1 / 2024-01-13T10:16:28Z
A temporary type defined to simulate `bool`. If some value of `b` != `True`, that indicates that some constraint is consistent, and an additional `Constraint` is kept track of such that once it's satisfied, some dual is satisfied.

It's used to make the changes trackable, but it might be more intutive to change the signature of `is_exhaustive = (xi: Constraint.t): bool` to `satisfy = (xi: Constraint.t): option(Constraint.t)` and this auxillary type can be got rid of (drastic change!).

review-comments / pigumar1 / 2024-01-13T10:21:08Z
The auxilliary constraint is printed to the console.


## #1154 Error flag for case expressions' associated DHExp / pigumar1
created 2023-12-21T02:58:49Z merged None base haz3l-case-advanced-ui
BODY (mutable, retrieved today):
This pull request aims to merge the three different case constructs in `DHExp` into one case construct.

The new approach will replace 
`DHExp.ConsistentCase(DHExp.case)`,
`DHExp.InconsistentBranches(MetaVar.t, HoleInstanceId.t, DHExp.case)`,
`DHExp.InexhaustiveCase(MetaVar.t, HoleInstanceId.t, DHExp.case)` (added for #1124),
and `DHExp.case.Case(t, list(rule), int)`

with `DHExp.Case(t, list(rule), int, option((MetaVar.t, HoleInstanceId.t)))`, in which the last parameter indicates whether the corresponding case expression is inconsistent.

Two concerns:
* Do we need to preserve the ability to distinguish consistent/inconsistent case expressions with `DHExp.constructor_string`? If so, the new `Case` construct, as well as the function `DHExp.constructor_string` would be a little bit more complex.
* Do we need to preserve the ability to have different inconsistent case expressions behave (dynamically) differently? If so, `option` might not be enough.


## #1155 Type Hole Inference (post merge) / RaefM
created 2023-12-26T23:49:53Z merged None base dev
BODY (mutable, retrieved today):


comments / RaefM / 2023-12-31T23:15:52Z
I've opened this as all core functionality from the paper is complete and seems to be working as per my testing.
Will make additional passes over this week for cleanup or stylistic changes (and address comments/requests as added).
Thanks!

comments / cyrus- / 2024-01-05T21:54:52Z
Nice work! Going to start with a functionality pass before doing code review...

The formatting here is a bit borked: 
![image](https://github.com/hazelgrove/hazel/assets/280638/4e879f0a-92e1-4f31-8c9a-7c983aa2cc0f)


comments / cyrus- / 2024-01-05T21:58:37Z
Getting odd behavior with ADTs...

![image](https://github.com/hazelgrove/hazel/assets/280638/5cba11e3-7489-4f6e-b994-7991e3213b00)


comments / RaefM / 2024-01-05T22:03:15Z
> Getting odd behavior with ADTs...
> 
> ![image](https://private-user-images.githubusercontent.com/280638/294619906-5cba11e3-7489-4f6e-b994-7991e3213b00.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQ0OTI0MjEsIm5iZiI6MTcwNDQ5MjEyMSwicGF0aCI6Ii8yODA2MzgvMjk0NjE5OTA2LTVjYmExMWUzLTc0ODktNGY2ZS1iOTk0LTc5OTFlMzIxM2IwMC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTA1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwNVQyMjAyMDFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lZDViNjViZGQ3ZGEzZDQ4MTc5ZGRlNzgzYWVjNTM4MjViOWYwMTI4NDAyMWRjM2JjMjA5ZjVjNjU5MmY3ODIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.fUBg7whI4gmxIOkIY5VA7CbaJgOlGAJAUSgKP5jN2rk)

Oof I could've sworn I tested that exact case recently and had it working...
I'll work on fixing those tonight

comments / cyrus- / 2024-01-05T22:04:02Z
the hole that should be after `=` has shifted left here 

![image](https://github.com/hazelgrove/hazel/assets/280638/02732150-59fa-4e72-959e-9636e1fee118)


comments / cyrus- / 2024-01-05T22:04:41Z
Tab doesn't seem to work to accept the suggestion...

![image](https://github.com/hazelgrove/hazel/assets/280638/25b387bd-0b4c-4c3d-9a2b-b1ef021d291f)


comments / RaefM / 2024-01-05T22:05:15Z
> Tab doesn't seem to work to accept the suggestion...
> 
> ![image](https://private-user-images.githubusercontent.com/280638/294620789-25b387bd-0b4c-4c3d-9a2b-b1ef021d291f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQ0OTI1ODMsIm5iZiI6MTcwNDQ5MjI4MywicGF0aCI6Ii8yODA2MzgvMjk0NjIwNzg5LTI1YjM4N2JkLTBiNGMtNGMzZC05YTJiLWIxZWYwMjFkMjkxZi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTA1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwNVQyMjA0NDNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04ZThmZmIwOGVlODgwZjYxZTY1NjE2NGMwOGE4ZDdiZWVhNGEzZDU1N2MyYTQ4NjJlY2ZlODIxMWZhMTE4ZDhmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.Ey3ZH9wc6jrpssBuHZWVVXsGLYoiBsMayIMIAU-mu2o)

Suggestion acceptance is currently bound to enter; do you want only tab or should I include both?

comments / cyrus- / 2024-01-05T22:06:19Z
> > Tab doesn't seem to work to accept the suggestion...
> > ![image](https://private-user-images.githubusercontent.com/280638/294620789-25b387bd-0b4c-4c3d-9a2b-b1ef021d291f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQ0OTI1ODMsIm5iZiI6MTcwNDQ5MjI4MywicGF0aCI6Ii8yODA2MzgvMjk0NjIwNzg5LTI1YjM4N2JkLTBiNGMtNGMzZC05YTJiLWIxZWYwMjFkMjkxZi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTA1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwNVQyMjA0NDNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04ZThmZmIwOGVlODgwZjYxZTY1NjE2NGMwOGE4ZDdiZWVhNGEzZDU1N2MyYTQ4NjJlY2ZlODIxMWZhMTE4ZDhmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.Ey3ZH9wc6jrpssBuHZWVVXsGLYoiBsMayIMIAU-mu2o)
> 
> Suggestion acceptance is currently bound to enter; do you want only tab or should I include both?

I think with @disconcision 's TyDi autocomplete bound to Tab it makes sense for this to also be bound to Tab. Thoughts @disconcision ?

comments / RaefM / 2024-01-05T23:18:32Z
> > Getting odd behavior with ADTs...
> > ![image](https://private-user-images.githubusercontent.com/280638/294619906-5cba11e3-7489-4f6e-b994-7991e3213b00.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQ0OTI0MjEsIm5iZiI6MTcwNDQ5MjEyMSwicGF0aCI6Ii8yODA2MzgvMjk0NjE5OTA2LTVjYmExMWUzLTc0ODktNGY2ZS1iOTk0LTc5OTFlMzIxM2IwMC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTA1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwNVQyMjAyMDFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lZDViNjViZGQ3ZGEzZDQ4MTc5ZGRlNzgzYWVjNTM4MjViOWYwMTI4NDAyMWRjM2JjMjA5ZjVjNjU5MmY3ODIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.fUBg7whI4gmxIOkIY5VA7CbaJgOlGAJAUSgKP5jN2rk)
> 
> Oof I could've sworn I tested that exact case recently and had it working... I'll work on fixing those tonight

Fixed issue:
![image](https://github.com/hazelgrove/hazel/assets/77807014/e2a6a56c-0c6a-4872-aa9a-71c689b1889b)
![image](https://github.com/hazelgrove/hazel/assets/77807014/03ec4eb6-bd24-42da-b45b-0e3ae5791d32)
Precendence of types to be preferred for a "solved" annotation are 
Unknown < ADT Var < Anything else

Will continue to review other issues now

comments / RaefM / 2024-01-06T03:28:38Z
> the hole that should be after `=` has shifted left here
> 
> ![image](https://private-user-images.githubusercontent.com/280638/294620682-02732150-59fa-4e72-959e-9636e1fee118.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDQ1MDE1ODksIm5iZiI6MTcwNDUwMTI4OSwicGF0aCI6Ii8yODA2MzgvMjk0NjIwNjgyLTAyNzMyMTUwLTU5ZmEtNGU3Mi05NTllLTk2MzZlMWZlZTExOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTA2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDEwNlQwMDM0NDlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yMjQ2NTFhNGFlOWYzOWFhY2QwOWU0ZWE1ZmM5MTJkZjYxYjMzMDlkMmM5MDIxZDJkYjEzYTc0MzcxN2Q1MWZmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.ZsoScN8webFIh6YySRI7E7mr1ccyJj9XpoPzLx3En3s)

Update: fixed this and other mentioned issues; will work on more testing and code cleanup now

comments / cyrus- / 2024-01-15T00:46:36Z
@RaefM can you have it so tab accepts the completion even on the left side? currently seems to only work on right side, it moves to the right when on the left...

comments / cyrus- / 2024-01-15T00:49:18Z
<img width="776" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/b0f52cb0-d2dc-45d6-93f9-2d32467a76a5">

two issues:
* curious why the input type on the type annotation on the let doesn't find the Int? 
* seem to be missing the hole in the cursor inspector view

comments / cyrus- / 2024-01-15T00:50:59Z
Maybe a comment for @disconcision but in the following, the tydi autocomplete inserts `::` which is a bit unexpected here. I know why it's doing that, but can we override this somehow?

<img width="460" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/557bb7a7-dc78-4fbd-bd8d-028ff1dbe63b">


comments / cyrus- / 2024-01-15T00:52:49Z
General thought: we should probably use the inferred types during elaboration, rather than leaving the types unknown. How hard would that be?

comments / cyrus- / 2024-01-15T00:57:09Z
The inferred type here confused me... B is not applied so I was expecting an error.

<img width="471" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/5f706d24-ba51-4e5c-af56-ac1cd7f08127">


comments / disconcision / 2024-01-15T01:21:46Z
> Maybe a comment for @disconcision but in the following, the tydi autocomplete inserts `::` which is a bit unexpected here. I know why it's doing that, but can we override this somehow?

straightforward to disable hackily.

been annoyed by this one too. trying to think abstractly about systematic criteria to filter this instead special-casing; it's using a refutable pattern in an irrefutable context. could downgrade these, or a least downgrade them if the expected type isn't literally list. actually that second bit should probably be treated as an independent downgrade as we'd probably want the same in refutable patterns too. 

in any case to be done properly it needs some kind of ranking system

comments / RaefM / 2024-01-15T02:17:43Z
> The inferred type here confused me... B is not applied so I was expecting an error.
> 
> <img alt="image" width="471" src="https://private-user-images.githubusercontent.com/280638/296628386-5f706d24-ba51-4e5c-af56-ac1cd7f08127.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUyODA1MzEsIm5iZiI6MTcwNTI4MDIzMSwicGF0aCI6Ii8yODA2MzgvMjk2NjI4Mzg2LTVmNzA2ZDI0LWJhNTEtNGU1Yy1hZjU2LWFjMWNkN2YwODEyNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDExNVQwMDU3MTFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lODAwMWI4MDhkZmFkMWVlNmQyNDhlZmM0N2FiM2I2ZGYxMjIyYTliMmVjYmI0ODJkNmZhYzIzNGEzNWNiZmM0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.Gm3WvZdnfr4V1ASmoa0QzDSg9gliLn--fejK73d6ia0">

This was due to a found occurs check failure getting masked by UI filters I made (solved as T and Int -> T). Pushed fix

New results:

![image](https://github.com/hazelgrove/hazel/assets/77807014/3b6a87d6-5e22-4160-b7cc-17cce3dd07fb)
![image](https://github.com/hazelgrove/hazel/assets/77807014/caea158d-27ef-4194-affe-bbc07e3e375f)


comments / RaefM / 2024-01-15T02:20:45Z
> @RaefM can you have it so tab accepts the completion even on the left side? currently seems to only work on right side, it moves to the right when on the left...

Fixed in latest commit

comments / RaefM / 2024-01-15T02:40:00Z
> <img alt="image" width="776" src="https://private-user-images.githubusercontent.com/280638/296627681-b0f52cb0-d2dc-45d6-93f9-2d32467a76a5.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUyODA0NTgsIm5iZiI6MTcwNTI4MDE1OCwicGF0aCI6Ii8yODA2MzgvMjk2NjI3NjgxLWIwZjUyY2IwLWQyZGMtNDVkNi05M2Y5LTJkMzI0NjdhNzZhNS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDExNVQwMDU1NThaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05OTBmNGQ1ZmYxMjJmMzFmMDFiMTBiYTAyZGU3MWUyNWMyNzM5MWZlOWQ3NmViN2E5ZGYxMmRmYzJhMjBmNDBkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.E2UUVWg0X5f5MShRS0pGNmbvB84Y-AhhjaryXEahtSk">
> two issues:
> 
> * curious why the input type on the type annotation on the let doesn't find the Int?
> * seem to be missing the hole in the cursor inspector view

Issues fixed:
1) Was caused due to missing subsumption constraints in Fun. Fixed in latest commits
![image](https://github.com/hazelgrove/hazel/assets/77807014/1160971b-f4c9-44d7-81d4-e8bb5b4f07c3)
2) The unknown case in type view was sometimes set to nothing mistakenly. Added ? as a fallback and also changed all the CI Type.view invocations to supply arguments that should make it so the hexagon is always shown instead of ? for consistency with the editor. Example with CI non unification message:
![image](https://github.com/hazelgrove/hazel/assets/77807014/04add999-ad44-44e8-a472-862c989e9b8b)


comments / cyrus- / 2024-01-15T13:05:29Z
> > Maybe a comment for @disconcision but in the following, the tydi autocomplete inserts `::` which is a bit unexpected here. I know why it's doing that, but can we override this somehow?
> 
> straightforward to disable hackily.
> 
> been annoyed by this one too. trying to think abstractly about systematic criteria to filter this instead special-casing; it's using a refutable pattern in an irrefutable context. could downgrade these, or a least downgrade them if the expected type isn't literally list. actually that second bit should probably be treated as an independent downgrade as we'd probably want the same in refutable patterns too.
> 
> in any case to be done properly it needs some kind of ranking system

Not suggesting things that would lead to a refutable pattern seems reasonable in this context. Also fine with just special casing this for now if that's easier. Can you make a quick PR?

comments / cyrus- / 2024-01-15T13:11:55Z
Not sure what this cursor inspector message means?

<img width="773" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/3c688a6f-8a74-4fc0-b815-f361181c66b1">


comments / disconcision / 2024-01-15T18:41:08Z
@cyrus #1162

comments / RaefM / 2024-01-15T21:47:24Z
> Not sure what this cursor inspector message means?
> 
> <img alt="image" width="773" src="https://private-user-images.githubusercontent.com/280638/296764507-3c688a6f-8a74-4fc0-b815-f361181c66b1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUzNTUzNTcsIm5iZiI6MTcwNTM1NTA1NywicGF0aCI6Ii8yODA2MzgvMjk2NzY0NTA3LTNjNjg4YTZmLThhNzQtNGZjMC1iODE1LWYzNjExODFjNjZiMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDExNVQyMTQ0MTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01ZTY4Njk5YmRkM2I5ZDE3MGRiOTVmNDY2ZjczMWUxODZhM2YyMDMyNDdiMjlkZGM3NjZmMjZhODIyOTI0MTc1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.-BAMaeYwT0UYGLV6hXqN5TcXpxP1S8DKkv-pbkTVTYA">

That text pops up when the occurs check fails (so whenever a pts is a proper subset of itself, eg being solved as T and Int -> T)

I'm definitely open to other text there, I figured 'occurs check failed' doesn't tell all that much and had gone with 'inferred type refers to self' to indicate the solution set recurses on itself and is thus not valid

comments / cyrus- / 2024-01-16T21:55:48Z
> > Not sure what this cursor inspector message means?
> > <img alt="image" width="773" src="https://private-user-images.githubusercontent.com/280638/296764507-3c688a6f-8a74-4fc0-b815-f361181c66b1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUzNTUzNTcsIm5iZiI6MTcwNTM1NTA1NywicGF0aCI6Ii8yODA2MzgvMjk2NzY0NTA3LTNjNjg4YTZmLThhNzQtNGZjMC1iODE1LWYzNjExODFjNjZiMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDExNVQyMTQ0MTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01ZTY4Njk5YmRkM2I5ZDE3MGRiOTVmNDY2ZjczMWUxODZhM2YyMDMyNDdiMjlkZGM3NjZmMjZhODIyOTI0MTc1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.-BAMaeYwT0UYGLV6hXqN5TcXpxP1S8DKkv-pbkTVTYA">
> 
> That text pops up when the occurs check fails (so whenever a pts is a proper subset of itself, eg being solved as T and Int -> T)
> 
> I'm definitely open to other text there, I figured 'occurs check failed' doesn't tell all that much and had gone with 'inferred type refers to self' to indicate the solution set recurses on itself and is thus not valid

Can we show the two possibilities here? Why is it only showing Int -> T?

comments / RaefM / 2024-01-18T06:58:08Z
> > > Not sure what this cursor inspector message means?
> > > <img alt="image" width="773" src="https://private-user-images.githubusercontent.com/280638/296764507-3c688a6f-8a74-4fc0-b815-f361181c66b1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDUzNTUzNTcsIm5iZiI6MTcwNTM1NTA1NywicGF0aCI6Ii8yODA2MzgvMjk2NzY0NTA3LTNjNjg4YTZmLThhNzQtNGZjMC1iODE1LWYzNjExODFjNjZiMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDExNVQyMTQ0MTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01ZTY4Njk5YmRkM2I5ZDE3MGRiOTVmNDY2ZjczMWUxODZhM2YyMDMyNDdiMjlkZGM3NjZmMjZhODIyOTI0MTc1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.-BAMaeYwT0UYGLV6hXqN5TcXpxP1S8DKkv-pbkTVTYA">
> > 
> > 
> > That text pops up when the occurs check fails (so whenever a pts is a proper subset of itself, eg being solved as T and Int -> T)
> > I'm definitely open to other text there, I figured 'occurs check failed' doesn't tell all that much and had gone with 'inferred type refers to self' to indicate the solution set recurses on itself and is thus not valid
> 
> Can we show the two possibilities here? Why is it only showing Int -> T?

Sorry for the wall of text; tldr, fixed with new behavior illustrated below

So after unification, it's solved as pts = {?, T, Int ->(pts)}. The occurs check as implemented makes it so that becomes {?, T, Int -> ?} and the general filtering rule for making suggestions out of ptses is to prefer 'non-nodes' over nodes if possible (which is anything that isn't a plain var or hole)- that filters it down to Int -> ?

The 'solution' in this case would be the set {T, Int -> T, Int -> Int -> T, ...}. Our filtering rules reads to Int -> T, where the issue is detected, and replaces T with ?.

Before ADTs were added, so when the occurs failure could only happen on holes (eg ? or Int -> ?), saying ? was always useless so we'd just suggest Int -> ? while marking occurs failing ptses as unsolved. With type variables, (T vs Int -> T) the two possibilities are each valid suggestions as they are inconsistent with one another. 

To facilitate this, changing the filtering so that when it comes to type variables, keep at least one when filtering the pts if the occurs check has failed. When occurs hasn't failed, still filtering all type variables is non hole/var alternatives exist (eg Z, Int -> T will have the suggestion Int -> T, and A, Int will have the suggestion Int)

Some suggestions based on this handling:
![image](https://github.com/hazelgrove/hazel/assets/77807014/78ba1159-c9a4-4129-8758-3e684e08ea11)
![image](https://github.com/hazelgrove/hazel/assets/77807014/af0977c5-fc7f-4a3b-8633-57de609879b8)
![image](https://github.com/hazelgrove/hazel/assets/77807014/ad96795c-9ca5-48a9-9186-75dcc262a259)



comments / cyrus- / 2024-02-10T20:30:53Z
@RaefM @anandrav this needs a merge with `dev`

comments / cyrus- / 2024-02-10T20:31:01Z
Seems to be a bug here:
<img width="452" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/238a7365-7355-4ed0-b140-078f9bc87965">


comments / cyrus- / 2024-02-10T20:31:47Z
Possibly downstream of above bug, but was expecting this to be [Int], not an error.
<img width="406" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/8dd3bde4-43f9-41c8-8599-78ac93b6ce2b">


comments / cyrus- / 2024-02-10T20:33:55Z
Probably also related but this should be a conflict but it's solving it as `[?]`: 
<img width="391" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/9d067e5d-5d1a-4881-9ec5-dac69e53fb75">


comments / cyrus- / 2024-02-10T20:36:22Z
When I Tab-expand on this I get `[]` which is a syntax error rather than `[?]`:
<img width="366" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/db1851c4-c84c-4942-9f5b-0c84b7f2da2d">


comments / cyrus- / 2024-02-27T04:21:21Z
@RaefM I think there must be a bug in your recent fixes -- the following should certainly not infer `[T]`, as neither `A` nor `B` are used anywhere!

<img width="321" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/f248bf64-3db9-497e-a481-bb7c145e2807">

Also still seeing this issue where there isn't a conflict arising from the conflicted patterns:

<img width="342" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/8b4b2176-8f2a-4520-a3f9-132efb900a83">



comments / cyrus- / 2024-02-27T04:22:53Z
Another probably related one that is behaving weirdly:

<img width="311" alt="image" src="https://github.com/hazelgrove/hazel/assets/280638/7eaa67c1-d3b7-4558-a85e-4362fff65462">


comments / thomasporter522 / 2024-03-29T20:58:06Z
After re-uploading, Cyrus's identified errors are mostly solved. The exceptions are:
 - Tab-expanding the suggestion here still produces `[]`, which is a syntax error. 

<img width = 300 src = "https://github.com/hazelgrove/hazel/assets/22896135/f8027ea2-7bd4-481f-8c76-019c62a3bbea)">

- ADTs appear to be converted into binary sums at some point, which are wrongly displayed and suggested to the user.

<img width = 300 src = "https://github.com/hazelgrove/hazel/assets/22896135/eae4e970-e05c-497a-94b0-58bfd054d6e7)">



comments / thomasporter522 / 2024-03-30T18:16:37Z
Here's another odd bug:

<img width=300 src ="https://github.com/hazelgrove/hazel/assets/22896135/f41cd6ed-66c9-41a4-9935-0591c55b6743">


comments / thomasporter522 / 2024-04-01T19:15:47Z
Also maybe we don't want to offer this suggestion.

<img width=300 src="https://github.com/hazelgrove/hazel/assets/22896135/c6289038-0755-4f0e-a1aa-7216bc50bd10">


comments / thomasporter522 / 2024-04-01T21:52:38Z
Adding constructor names was easy, thanks to the well-factored code. This works fine:

<img width=300 src="https://github.com/hazelgrove/hazel/assets/22896135/bf8fac96-bf08-4333-99f1-31c401592691">

And this gives an inconsistency, as desired.

<img width=400 src="https://github.com/hazelgrove/hazel/assets/22896135/19d5b192-990a-4064-88c1-da210c67772b">

However, the error information is wrong. The ? constructors are my own doing, as a placeholder. 


comments / thomasporter522 / 2024-07-17T19:30:23Z
I understand why this is the error message we give, but I think it's unintuitive. Is there a better way to convey this? Either just having the type holes in the message be red, or actually showing the two different arrow types? The latter would allow the user to select which one they want and resume bidirectional checking. 

<img width=400 src="https://github.com/user-attachments/assets/ec27cb38-a223-41f9-b55c-5b9c6cafaac3">

There is also the potentially appealing possibility of displaying potential type sets in full, as nested lists of options. For example, if the PTS is {Num , Arrow({Num, Bool}, {Num, Bool})}, the user could hover over any element listed between a pair of {...}, including the sublists, rather than inconsistent sublists being displayed as a hole. 

There are a couple of issues with this. The first is that if the user selects a sub-option, like the second "Num" in the text example, it is not determinate what entire type they are selecting. Do they mean Arrow(Num, Num) or Arrow(Num, Bool)? Should we just treat it as Arrow(Num, Hole)? What if the user wants to specify both sides? Maybe we could have a tree of drop downs, but that's surely far too complex. 

The second issue is that a PTS is in fact a lossy representation of the set of potential types for a hole. In the image example, the two constrained fillings for the type hole are {Arrow(Num,Bool), Arrow(Bool,Num)}, and if this is collapsed to Arrow({Num, Bool}, {Num, Bool}), the original possibilities may not be recovered, without also including Arrow(Num,Num) and Arrow(Bool,Bool).

In light of these two issues, might it be better to forgo merging inconsistent potential types? The principal disadvantage would be the loss of compactness, and now we reach an empirical matter, but I think that merging only consistent types (which needs further specification since consistency isn't transitive) would recover much of the compactness of the general scheme, and that remaining examples would probably produce moderately sized sets most of the time. To the first point, the example of a combinatorically explosive set of types in the old draft consists of six pairwise consistent types: and thus they could be compressed to one inconsistency-free type. To the second, the number of potential types grows multiplicatively, but only upon the inclusion of other type holes, and only by the number of different _type constructors_ as which these type holes are used. 

I don't doubt that it is easy to construct cases in which this "consistent representation" is too big a set. Maybe we could pragmatically compute both the compact and the consistent representations, and display the consistent one preferentially, and the compact one if the consistent one is larger than some predefined limit and larger than the compact one.

This was a bit of a ramble, sorry. Thoughts welcome.

comments / cyrus- / 2026-04-21T13:01:09Z
archiving in favor of the more recent effort by Alex Smart


## #1241 Module implicts / xzxzlala
created 2024-03-13T14:54:43Z merged None base dev
BODY (mutable, retrieved today):
### Module implicit:

Parameters can be marked implicit which then allows them to be omitted from function calls.
Since we already have module system in hazel, so we decided to take advantage of modules to fulfill this feature. 
The functions would have an implicit module parameter and this parameter needs defined by users explicitly. 

Here is an example from https://www.cl.cam.ac.uk/~jdy22/papers/modular-implicits.pdf:
```
1 module type Show = sig
2   type t
3   val show : t -> string
4 end
5
6 let show { S : Show } x = S . show x
7
8 implicit module Show_int = struct
9    type t = int
10  let show x = string_of_int x
11 end
12
13 implicit module Show_float = struct
14   type t = float
15   let show x = string_of_float x
16 end
17
18 implicit module Show_list { S : Show } = struct
19   type t = S . t list
20   let show x = string_of_list S . show x
21 end
22
23 let () =
24   print_endline (" Show an int: " ^ show 5);
25   print_endline (" Show a float : " ^ show 1.5);
26   print_endline (" Show a list of ints : " ^ show [1; 2; 3]);
```
And here is a draft of what should be implemented in hazel:
![image](https://github.com/hazelgrove/hazel/assets/73332800/26ebc648-a196-4291-9be9-476f862e24a8)

### Implementation plans:

- Explicitly pass module parameters to functions could work in hazel.
- Add implicit keyword to hazel and let users could define implicit modules.
- Functions could find the corresponding implicit modules automatically and users needn't explicitly pass module parameters to functions.

### What code we may write (Not sure about this, may changes in the process of writing code):

- New types, merge parameterized_types to module system.
- New syntax and corresponding statics/dynamics. (Mold.re, Form.re, MakeTerm.re, Elaborator.re, Evaluator.re, DHExp.re)

### Checkpoint

- [ ] Mold.re
- [ ] Form.re
- [ ] MakeTerm.re
- [ ] Elaborator.re
- [ ] Evaluator.re
- [ ] DHExp.re 

comments / cyrus- / 2024-03-13T17:38:02Z
@xzxzlala can you write up a detailed PR description describing the idea, what kind of code we want to be able to write, and what your implementation plan is

comments / cyrus- / 2026-04-21T13:02:21Z
archiving this early design, will revisit in the future


## #1254 Create a new input syntax for function. / DavidFangWJ
created 2024-03-25T13:47:04Z merged 2026-04-23T15:27:57Z base dev
BODY (mutable, retrieved today):
### Motivation
Add a more compact syntax to function, such that
```
let f(x : A, y: B) = e
```
should behave the same as below:
```
let f : (A, B) = fun (x, y) -> e
```
This new function syntax is more analogous to other programming languages with strong data types, and is therefore easier to learn.

### Implementation Details
According to the current structure, there following files are modified.
- For `Info.re`, a new field `rewrite_id` is introduced, which registers the correspondence between the rewritten `Exp.t` and the original one.
- For `StaticsBase.re`, `check_annotated_function` is introduced to check whether the function is in the new specified syntax, passed as `Let(Ap, ...)`.
- For `Statics.re` and `Elaborator.re`, additional code are introduced to process the new syntax.
- For `ExplainThis.re` and `AppPat.re`, additional explanation categories are introduced.

comments / cyrus- / 2024-03-26T21:55:26Z
@DavidFangWJ We shouldn't actually need to modify `Form.re` to accomplish this, since the syntax of patterns already includes application and annotations:

![image](https://github.com/hazelgrove/hazel/assets/280638/5f8ec009-b521-42a9-8b95-986589d186d6)

We will need to change how patterns in let bindings are processed in the statics and elaboration to special case the situation where the top-level pattern is `x(p1[: t1], ..., pn[: tn])[ : t]`.

comments / cyrus- / 2024-04-12T01:20:37Z
Regarding the type error, take a look at the definition of `UPat.t` -- it is a record type, because terms have unique IDs, so you need to decompose it like the other functions working on `UPat`'s do. 

Regarding the function itself, you should be looking for the application of a variable, rather than a constructor. Constructors are capitalized.

You also do not need to check that all arguments have type annotations -- it is okay to leave an argument unannotated, it will just get the unknown type.

You also need to handle optional return type annotations (which will require changing the return type of your function overall).

Please write some additional examples in your PR message to handle both functions with missing type annotations on arguments and missing return types, so make it clear these are all valid. We'll turn these into tests as well.

comments / DavidFangWJ / 2024-05-08T23:50:32Z
Cannot fully understand the part in `Statics.re/uexp_to_info_map` regarding the process of let binding, which looks like this:
```
  | Let(p, def, body) =>
    let (p_syn, _) =
      go_pat(~is_synswitch=true, ~co_ctx=CoCtx.empty, ~mode=Syn, p, m);
    let (def, p_ana_ctx, m, ty_p_ana) =
      if (!is_recursive(ctx, p, def, p_syn.ty)) {
        let (def, m) = go(~mode=Ana(p_syn.ty), def, m);
        let ty_p_ana = def.ty;
        let (p_ana', _) =
          go_pat(
            ~is_synswitch=false,
            ~co_ctx=CoCtx.empty,
            ~mode=Ana(ty_p_ana),
            p,
            m,
          );
        (def, p_ana'.ctx, m, ty_p_ana);
      } else {
        let (def_base, _) =
          go'(~ctx=p_syn.ctx, ~mode=Ana(p_syn.ty), def, m);
        let ty_p_ana = def_base.ty;
        /* Analyze pattern to incorporate def type into ctx */
        let (p_ana', _) =
          go_pat(
            ~is_synswitch=false,
            ~co_ctx=CoCtx.empty,
            ~mode=Ana(ty_p_ana),
            p,
            m,
          );
        let def_ctx = p_ana'.ctx;
        let (def_base2, _) = go'(~ctx=def_ctx, ~mode=Ana(p_syn.ty), def, m);
        let ana_ty_fn = ((ty_fn1, ty_fn2), ty_p) => {
          ty_p == Typ.Unknown(SynSwitch) && !Typ.eq(ty_fn1, ty_fn2)
            ? ty_fn1 : ty_p;
        };
        let ana =
          switch ((def_base.ty, def_base2.ty), p_syn.ty) {
          | ((Prod(ty_fns1), Prod(ty_fns2)), Prod(ty_ps)) =>
            let tys =
              List.map2(ana_ty_fn, List.combine(ty_fns1, ty_fns2), ty_ps);
            Typ.Prod(tys);
          | ((ty_fn1, ty_fn2), ty_p) => ana_ty_fn((ty_fn1, ty_fn2), ty_p)
          };
        let (def, m) = go'(~ctx=def_ctx, ~mode=Ana(ana), def, m);
        (def, def_ctx, m, ty_p_ana);
      };
    let (body, m) = go'(~ctx=p_ana_ctx, ~mode, body, m);
    /* add co_ctx to pattern */
    let (p_ana, m) =
      go_pat(
        ~is_synswitch=false,
        ~co_ctx=body.co_ctx,
        ~mode=Ana(ty_p_ana),
        p,
        m,
      );
    add(
      ~self=Just(body.ty),
      ~co_ctx=
        CoCtx.union([def.co_ctx, CoCtx.mk(ctx, p_ana.ctx, body.co_ctx)]),
      m,
    );
```




comments / cyrus- / 2024-08-20T17:36:00Z
@DavidFangWJ there is a small merge conflict + the following has an error on `f`: 

<img width="522" alt="image" src="https://github.com/user-attachments/assets/97f1ca46-cb0b-4e92-acda-f66710429722">


comments / cyrus- / 2025-07-30T20:51:48Z
@DavidFangWJ The ExplainThis description for function definition should say something like "Defines a function f with arguments x", not the same message as constructor binding.

reviews / cyrus- / 2025-11-06T19:42:38Z
@DavidFangWJ functionality looks good, but take a look at my comments. please write up an explanation for how the rewriting works in general as well in the PR description.

review-comments / cyrus- / 2024-04-16T17:44:47Z
you don't need to reconstruct this, since this record is already the `args` variable (and similar below)

review-comments / cyrus- / 2024-04-16T17:46:17Z
functions with a single argument won't be captured by the Tuple pattern here

review-comments / cyrus- / 2024-04-16T17:48:00Z
don't need to fold here, you can just recursively synthesize a type for the args pattern since that will be a product type that we can use directly as the input type

review-comments / cyrus- / 2024-04-16T17:48:47Z
same here

review-comments / cyrus- / 2024-04-21T23:08:45Z
we don't need to check the syntax of the argument -- any argument pattern is fine.

review-comments / cyrus- / 2025-11-06T19:37:59Z
don't mention specific line numbers in comments, as they are easy to go stale

review-comments / cyrus- / 2025-11-06T19:38:13Z
you should fully delete debugging prints before a PR is merged.

review-comments / cyrus- / 2025-11-06T19:39:59Z
remove commented out code before we merge PR

review-comments / cyrus- / 2025-11-06T19:40:22Z
remove per above

review-comments / cyrus- / 2025-11-06T19:40:55Z
don't leave comments about being unsure about something in the final PR. was this question resolved? if not, let me know and we can discuss

review-comments / cyrus- / 2025-11-06T19:41:07Z
remove commented code

review-comments / cyrus- / 2025-11-06T19:42:03Z
can you explain what the Id.t parameter is used for specifically? we should document this and make sure it is something that other systems in Hazel do not need to be overly aware of.

review-comments / DavidFangWJ / 2025-11-07T22:00:28Z
Solved.

review-comments / DavidFangWJ / 2025-11-07T22:36:22Z
This is a register variable to pass the link from the original `Exp.t` to the rewritten one. I consider it the most intuitive way so far to carry this corresponding relation from `Statics.re` to `Elaborator.re`.


## #1308 Adds theorem and proof construct / nskh
created 2024-05-07T20:50:51Z merged None base stepper-rewrites
BODY (mutable, retrieved today):
Replaces https://github.com/hazelgrove/hazel/pull/1263.

In-progress PR to add a theorem keyword in the style of let-equals-in to Hazel.

Based on [stepper-rewrites](https://github.com/hazelgrove/hazel/tree/stepper-rewrites) this time.

comments / nskh / 2024-05-22T20:17:21Z
@Negabinary: I addressed your changes, should be ready for review. We can merge as-is, or discuss how to add in some way to invoke a stepper by adding a `proof` keyword here too.

comments / cyrus- / 2024-05-24T14:39:22Z
```
theorem name = typ 
proof "serialized stepper data" 
in e

things we need in the typ syntax:

forall x -> ty
exists x : T -> typ.  [sigma types]
(x : typ) -> typ. [pi types]
   (syntactic sugar: forall x : T -> ty)
typ(typ). 
e1 = e2.  [equality types]
```

comments / cyrus- / 2024-05-28T17:29:35Z
If we do the syntax as:

```
theorem name : typ 
proof e1
in e2
```

then this becomes just another let expression exactly -- that should be pretty straightforward to do so let's update this PR in that direction, then make another PR for adding the new type forms.

comments / cyrus- / 2024-07-08T21:43:11Z
TODO:

- change sorting to `theorem pat = exp in exp`, which matches let expressions exactly
- have theorem behave exactly like a let expression everywhere else in the codebase
- at the type level, rename existing `forall` to `type` 
- add new `forall pat -> ty` construct to types
- add `{e1 = e2}` form to types

review-comments / Negabinary / 2024-05-08T17:53:41Z
we probably want this to elaborate to the in-part of the expression, not just a tuple

review-comments / Negabinary / 2024-05-08T17:56:10Z
we can probably re-use the precidence that let uses here - we probably don't want a lower precedence than the min

review-comments / Negabinary / 2024-05-08T17:59:07Z
this is going to be more like the Seq case now that we've got an `in` - you can pretty much copy seq exactly

review-comments / nskh / 2024-05-08T19:02:39Z
cool, just use `let_` directly, or do I set `theorem_ = let_`? 

review-comments / nskh / 2024-05-08T19:04:38Z
makes sense, I wasn't sure what exactly to put here so let's discuss further

review-comments / nskh / 2024-05-08T19:08:29Z
cool, and the `e1, e2` are instead `def, body` from the theorem? will update

review-comments / Negabinary / 2024-05-08T21:06:07Z
yeah because we're discarding def like how we're discarding e1

review-comments / Negabinary / 2024-05-08T21:06:28Z
I think you can use `let_` directly

review-comments / nskh / 2024-05-22T20:14:09Z
resolved in latest commit


## #1328 Construct sexp / gcrois
created 2024-07-17T01:21:42Z merged None base llama-lsp-lookahead
BODY (mutable, retrieved today):
This branch seeks to add functionality to generate an [sexp](https://github.com/janestreet/sexplib) from valid Hazel code in the file [`src/haz3lweb/SexpConversion.re`](https://github.com/hazelgrove/hazel/blob/construct_sexp/src/haz3lweb/SexpConversion.re).

- [x] Triv
- [x] Bool
- [x] Int
- [x] Float
- [x] String
- [x] ListLit
- [x] Invalid
- [x] EmptyHole
- [ ] MultiHole
- [x] Constructor
- [x] Fun
- [x] Tuple
- [x] Var
- [x] Let
- [x] TyAlias
- [x] Ap
- [x] If
- [x] Seq
- [x] Test
- [x] Parens
- [x] Cons
- [x] ListConcat
- [x] UnOp
- [x] BinOp
- [x] Match

comments / gcrois / 2024-07-19T14:05:03Z
Remaining: finish `sexp_of_uexp`, build test cases

comments / cyrus- / 2026-04-21T13:03:06Z
archiving

reviews / cyrus- / 2024-07-25T18:56:35Z
reviewed the `go` functions

review-comments / cyrus- / 2024-07-25T18:51:45Z
this can be "(multihole ...)" for completion.

review-comments / cyrus- / 2024-07-25T18:52:34Z
the pattern should go first, then exp1 and then next to it (not nested) exp2

review-comments / cyrus- / 2024-07-25T18:53:30Z
maybe `concat` to be consistent with us using `cons` rather than `::`

review-comments / cyrus- / 2024-07-25T18:54:00Z
@disconcision do we want to use `?` or `??` for empty holes?

review-comments / cyrus- / 2024-07-25T18:54:07Z
see above

review-comments / cyrus- / 2024-07-25T18:54:54Z
need to do something here to indicate it is a type annotation, maybe `(: p ty)`

review-comments / cyrus- / 2024-07-25T18:55:03Z
see above

review-comments / cyrus- / 2024-07-25T18:55:07Z
see above

review-comments / cyrus- / 2024-07-25T18:55:19Z
use `?`/`??` as above

review-comments / cyrus- / 2024-07-25T18:55:23Z
see above

review-comments / cyrus- / 2024-07-25T18:55:44Z
need to add support for sum types (algebraic data types)

review-comments / cyrus- / 2024-07-25T18:55:52Z
need to add support for arrow types

review-comments / cyrus- / 2024-07-25T18:56:00Z
just recurse down as in the other parens cases

review-comments / cyrus- / 2024-07-25T18:56:08Z
treat the same as other ap cases


## #1337 Random generation of UExps / ruiz-m
created 2024-07-25T19:51:57Z merged None base dev
BODY (mutable, retrieved today):
Random generation of UExp for property-based testing.

The [QCheck](https://github.com/c-cube/qcheck?tab=readme-ov-file) library was used to perform random generation of values.

The [Alcotest](https://github.com/mirage/alcotest) library was used for unit testing.

The purely random generation of uexps will reveal some bugs.


comments / cyrus- / 2024-07-31T18:16:16Z
@ruiz-m could you leave instructions in the README.md file for how to run the quickcheck tests (`make test` I suppose) and how to get readable output from that? @Negabinary took a look but had trouble seeing the terms when tests failed.

comments / ruiz-m / 2024-07-31T23:04:30Z
Alright. I might need to work on adding some code to print the term

comments / 7h3kk1d / 2024-09-04T18:50:22Z
We need to make sure that we're outputting the random seed for any failing tests before merging so that we can reproduce test failures locally. It would be terrible if the tests fail on CI and we can never reproduce them. I would assume using the native integration between qcheck and alcotest would do this but we need to confirm.

comments / ruiz-m / 2024-09-05T15:01:36Z
@7h3kk1d Thank you for the feedback. It might take me some time to work on these fixes, but I will do them

comments / 7h3kk1d / 2024-09-05T15:02:34Z
> @7h3kk1d Thank you for the feedback. It might take me some time to work on these fixes, but I will do them

Feel free to let me know if there's any particular way I can help.

review-comments / 7h3kk1d / 2024-09-04T17:46:41Z
We should still mark these as Type Assignment tests. What do you think about `TypeAssignment.random` or `TypeAssignment.property_tests`  for the name. We still don't have a format for doing hierarchies of tests. Dot separated matching the module structure makes sense to me.

review-comments / 7h3kk1d / 2024-09-04T18:10:30Z
I think we probably want each property to be it's own test as opposed to each generated value resulting in a new test. We could then mark the tests as `Slow` instead of `Quick` so we don't slow the test runs down. It's worth looking into https://github.com/c-cube/qcheck?tab=readme-ov-file#integration-within-alcotest to see if we can go straight from the qcheck runner to alcotest.

review-comments / 7h3kk1d / 2024-09-04T18:11:27Z
We should move this to the test file.

review-comments / 7h3kk1d / 2024-09-04T18:19:26Z
Up to you but the property can also be written as:


```reason
let property_test =
    (uexp_typ: option(Typ.t), dhexp: option(DHExp.t), m: Statics.Map.t)
    : bool => {
  let dhexp_typ = Option.bind(dhexp, typ_of_dhexp(Builtins.ctx_init, m))

  Option.equal(Typ.eq, uexp_typ, dhexp_typ);
};
```

review-comments / 7h3kk1d / 2024-09-04T18:27:46Z
It's also worth doing something on the assertion to be closer to the equality we want to test so the error messages are better. We can probably do better but this is something:

```reason
let testable_typ = testable(Fmt.using(Typ.pretty_print, Fmt.string), Typ.eq);

//Generate purely random uexp test cases for alcotest
let random_tests =
  List.map(
    (u: UExp.t) => {
      print_endline("Term: " ++ UExp.show(u));
      let m: Statics.Map.t = Test_Elaboration.mk_map(u);
      let d: option(DHExp.t) = Elaborator.dhexp_of_uexp(m, u, false);
      let ty: option(Typ.t) = Elaborator.fixed_exp_typ(m, u);
      let dhexp_typ =
        Option.bind(d, TypeAssignment.typ_of_dhexp(Builtins.ctx_init, m));
      let test = () =>
        Alcotest.check(
          Alcotest.option(testable_typ),
          "Random expression: " ++ UExp.show(u),
          dhexp_typ,
          ty,
        );
      test_case("Type assignment", `Quick, test);
    },
    QCheck.Gen.generate(~n=10, pure_random_uexp),
  );
```

review-comments / 7h3kk1d / 2024-09-04T18:38:23Z
Qcheck has first class support for generating long/short tests https://github.com/c-cube/qcheck?tab=readme-ov-file#long-tests

review-comments / 7h3kk1d / 2024-09-04T18:40:58Z
We should try to build a full arbitrary instance for the types so we can add printers/shrinking functions in the future like https://github.com/c-cube/qcheck?tab=readme-ov-file#mirrors-and-trees

review-comments / 7h3kk1d / 2024-09-04T18:42:00Z
I feel like we should be able to use the ppx https://github.com/c-cube/qcheck/tree/main/src/ppx_deriving_qcheck for at least the simple variants.

review-comments / 7h3kk1d / 2024-09-12T19:16:41Z
@ruiz-m just an fyi that I hit this bug when doing some of my own testing https://github.com/c-cube/qcheck/issues/269#issuecomment-2347051999. So be wary if you're trying to use deriving for recursive types.


## #1457 Parameterized Types / isdiemer
created 2025-01-09T22:45:51Z merged None base dev
BODY (mutable, retrieved today):
Initial commit for new branch. Added new form to tpat_term for substitution, and updated name of TyAlias to TyDef to better reflect its purpose and usage. 


This is a duplicate PR as my original PR was based off of the wrong branch.


## #1594 add forall explicit and succint syntax to test parser / joseemds
created 2025-04-08T00:15:36Z merged None base dev
BODY (mutable, retrieved today):


comments / cyrus- / 2026-04-21T14:02:23Z
We would need to add this to the main tylr parser as well to justify including it in the test parser


## #1641 Fix dynamic pattern matching / MaxCarroll0
created 2025-05-01T13:03:55Z merged None base dev
BODY (mutable, retrieved today):
Fixes #1640.

There are currently no cases where failed casts should match. 
Can someone confirm that changing this doesn't have unintended behaviour?

comments / cyrus- / 2026-04-21T14:03:29Z
@MaxCarroll0 not sure if this is something you want to get updated / reviewed still? closing for now, but feel free to reopen with a more detailed PR description / corresponding issue created.


## #1784 Parameterized types / odruzgal
created 2025-07-11T11:06:07Z merged None base dev
BODY (mutable, retrieved today):
This is just the last version that fully compiled on my machine, the ctx is all flushed out but there were issues in the application in statics I am still troubleshooting.

comments / odruzgal / 2025-07-18T14:30:06Z
This currently doesn't build but I did get a rough draft of the full structure and handle the dependency issues between the files, I am just working on all of the debugging and error checking, still a lot to fix, but a lot more progress made this week

comments / odruzgal / 2025-11-21T21:49:53Z
- [ ] Extend kinds to type unit prod arr
- [ ] Extend lookup for kinds in type variables and constructors
- [ ] Extend for kinds in named type constructor
- [ ] Extend constructor equality at normalization where necessary for PFPL 18.2 Ap, proj, etc
- [ ] Integrate all constructor/kind rules in statics
- [ ] treat all simple types as basic unary constructor kind, run constructor kind checks on all terms inside bidirectional checking
- [ ] Do Type alias handling, assign kinds to parameters, store the type of each constructor
- [ ] Handle nested constructors via curried kind logic
- [ ] Make sure all parameters are bound with kinds, statics check for well-kindedness
- [ ] Handle typeAp for instantiation via PFPL forall rule, (account for implicit instantiation?)
- [ ] Add tpat form for optionally kinded type variable, extend tpat statics with bound type variable
- [ ] In unification,normalize constructors according to PFPL 18.2 before comparison so kind constructors that are equal are treated as so everywhere
- [ ] Write test file
- [ ] Handle kind printing, 
- [ ] Map kind info to cursor inspector
- [ ] Ill-kind error messaging
- [ ] Error handling for potential with shadowing and name conflicts, other edge cases update tests accordingly
- [ ] Integrate with hole marking logic



## #1788 Modules / gcrois
created 2025-07-14T18:12:08Z merged None base dev
BODY (mutable, retrieved today):
- [x] [Dynamics](https://github.com/hazelgrove/hazel/blob/f7e26bd432a78146f409ff6da8c0ff6c8d1d5d5c/test/evaluator/Test_Evaluator_Modules.re)
- [ ] Analysis case in statics
- [ ] Fix todos ([especially type hygiene](https://github.com/hazelgrove/hazel/blob/643a4a4aef6d327d92a96d788f2beac81da926f8/src/language/term/Typ.re))
- [ ] Use real syntax -- sorry triple semicolons :(
- [ ] Fix highlighting 

- [ ] Add keyword + form for submodule definition (`module`)
- [ ] Automatic typealias

Discussion:
https://github.com/hazelgrove/hazel/discussions/1558

Related PR:
https://github.com/hazelgrove/hazel/pull/1020/files

<img width="318" height="341" alt="image" src="https://github.com/user-attachments/assets/646f1877-9fe8-4617-9393-b51196bf51a1" />


comments / gcrois / 2025-07-20T20:05:19Z
Thank you @7h3kk1d and @Negabinary for your help!!

We officially have basic dynamics working for modules, with a few problems (that you might have suggestions on!)

@Negabinary:
I think we are reversing somewhere we shouldn't be - Statics seems to get the bindings in their intended order (red highlight when using a binding after its defined), but dynamics can only access _future_ findings? [I tried swapping the pattern match](https://github.com/hazelgrove/hazel/blob/775c07f29a8dd51f22fb4424579e7d2722c64798/src/language/dynamics/transition/Transition.re#L878) but OCaml did _not_ like that. Any advice off the top of your head?

@7h3kk1d:
I want to get the Dot operator working -- I took a look at [what we do for tuples](https://github.com/hazelgrove/hazel/blob/775c07f29a8dd51f22fb4424579e7d2722c64798/src/language/dynamics/transition/Transition.re#L635), but I feel like I shouldn't just search through the entries and find a `ValBinding`. My instincts tell me we should have a context or something we can directly look through here?

To do ExpToSegment, I want to follow the pattern we have elsewhere where we use the [`Form.re`](https://github.com/hazelgrove/hazel/blob/0a15c06eda2c0813a83c2838f81bc6342bb26fa1/src/haz3lcore/lang/Form.re#L498) definition, but I kept getting a nebulous error about not matching the number of `_in` variables?

comments / gcrois / 2025-07-24T17:16:21Z
<img width="888" height="347" alt="image" src="https://github.com/user-attachments/assets/1b5d7248-40a7-4dbe-85ca-0d0045ff8023" />

[Statics + Dynamics work for dot!](https://hazel.org/build/gc-modules/?name=Scratchpad%202&share=let%2520before_before%2520%253D%2520%2522before%2522%2520in%250Alet%2520module%2520%253D%2520%2520%257B%250Aval%2520before%2520%253D%2520before_before%2520%252B%252B%2520%2522...%2520%2522%2520%253B%253B%250Aval%2520after%2520%253D%2520before%2520%252B%252B%2520%2522after%2522%250A%257D%2520in%250Alet%2520after_after%2520%253D%2520module.after%2520%252B%252B%2520%2522...%2522%2520in%2520after_after)

comments / gcrois / 2025-08-01T06:37:32Z
I added some statics test cases we were missing! I'm able to get most of these if I use the [factored-out def binding code](https://github.com/hazelgrove/hazel/blob/c4944c4b942014d3c16f0676bf7b3a8556f0b817/src/language/statics/Statics.re#L353), but this seems to break evaluation? @Negabinary any thoughts [here](https://github.com/hazelgrove/hazel/blob/c4944c4b942014d3c16f0676bf7b3a8556f0b817/src/language/statics/Statics.re#L1228)?

@7h3kk1d can you help me make [these tests prettier](https://github.com/hazelgrove/hazel/blob/c4944c4b942014d3c16f0676bf7b3a8556f0b817/test/statics/Test_Statics_Modules.re#L25)? I wasn't sure the best way to do the ones I commented out, and I'm not convinced the last few are actually testing what we want to test. Also, I was getting some pretty rough crashes when editing modules because of holes -- [I went ahead and stripped them from `MakeTerm`](https://github.com/hazelgrove/hazel/blob/cc92fc04d9b5757a406ad6047e2acea3ba60dad8/src/haz3lcore/lang/MakeTerm.re#L307) -- this is probably a blunt solution. Can you think of something better?

For now, I'd like to avoid adding `Ctx` to the syntax of `ModuleSignature`, simply because of some truly frightening cyclic dependencies. We can pretty easily emulate this by [constructing a ctx when needed from the entries](https://github.com/hazelgrove/hazel/blob/f0c4d0eba7c9b466986f8e9213ffd5c592ef44c8/src/language/term/Term.re#L961).


## #1863 Fix term appearing in its own list of ancestors / russell-rozenbaum
created 2025-08-06T19:19:37Z merged None base dev
BODY (mutable, retrieved today):


comments / cyrus- / 2026-04-21T14:05:31Z
@russell-rozenbaum this seems to only have a debug command change but no actual fix, so closing for now but feel free to reopen or leave an issue on GitHub.


## #1891 Bump vite-plugin-static-copy from 2.3.0 to 2.3.2 / dependabot[bot]
created 2025-08-21T15:57:21Z merged 2026-04-21T14:15:41Z base dev
BODY (mutable, retrieved today):
Bumps [vite-plugin-static-copy](https://github.com/sapphi-red/vite-plugin-static-copy) from 2.3.0 to 2.3.2.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/sapphi-red/vite-plugin-static-copy/releases">vite-plugin-static-copy's releases</a>.</em></p>
<blockquote>
<h2>vite-plugin-static-copy@2.3.2</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/4627afb8582083eab733881d3d974e1c1f23997d"><code>4627afb</code></a> Thanks <a href="https://github.com/sapphi-red"><code>@​sapphi-red</code></a>! - Files not included in <code>src</code> was possible to acess with a crafted request. See <a href="https://github.com/sapphi-red/vite-plugin-static-copy/security/advisories/GHSA-pp7p-q8fx-2968">GHSA-pp7p-q8fx-2968</a> for more details.</li>
</ul>
<h2>vite-plugin-static-copy@2.3.1</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/sapphi-red/vite-plugin-static-copy/pull/152">#152</a> <a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/6aee6a3d8caf6d08bedeb4c97fb7580fd904b895"><code>6aee6a3</code></a> Thanks <a href="https://github.com/sapphi-red"><code>@​sapphi-red</code></a>! - improve performance of internal <code>isSubdirectoryOrEqual</code> function</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/sapphi-red/vite-plugin-static-copy/blob/vite-plugin-static-copy@2.3.2/CHANGELOG.md">vite-plugin-static-copy's changelog</a>.</em></p>
<blockquote>
<h2>2.3.2</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/4627afb8582083eab733881d3d974e1c1f23997d"><code>4627afb</code></a> Thanks <a href="https://github.com/sapphi-red"><code>@​sapphi-red</code></a>! - Files not included in <code>src</code> was possible to acess with a crafted request. See <a href="https://github.com/sapphi-red/vite-plugin-static-copy/security/advisories/GHSA-pp7p-q8fx-2968">GHSA-pp7p-q8fx-2968</a> for more details.</li>
</ul>
<h2>2.3.1</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/sapphi-red/vite-plugin-static-copy/pull/152">#152</a> <a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/6aee6a3d8caf6d08bedeb4c97fb7580fd904b895"><code>6aee6a3</code></a> Thanks <a href="https://github.com/sapphi-red"><code>@​sapphi-red</code></a>! - improve performance of internal <code>isSubdirectoryOrEqual</code> function</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/326a79fb29bd082a876f59681d2d61e488267331"><code>326a79f</code></a> chore: update versions (<a href="https://redirect.github.com/sapphi-red/vite-plugin-static-copy/issues/197">#197</a>)</li>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/0f39cad26e703a09ab6b10049a5ba455e14ad8c8"><code>0f39cad</code></a> ci: run release against <code>v*</code> branches</li>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/4627afb8582083eab733881d3d974e1c1f23997d"><code>4627afb</code></a> fix: only serve files under <code>src</code> (<a href="https://redirect.github.com/sapphi-red/vite-plugin-static-copy/issues/195">#195</a>)</li>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/08cafec9b7562b76244aeff460328898724aac16"><code>08cafec</code></a> chore: update versions (<a href="https://redirect.github.com/sapphi-red/vite-plugin-static-copy/issues/154">#154</a>)</li>
<li><a href="https://github.com/sapphi-red/vite-plugin-static-copy/commit/6aee6a3d8caf6d08bedeb4c97fb7580fd904b895"><code>6aee6a3</code></a> perf: improve <code>isSubdirectoryOrEqual</code> performance (<a href="https://redirect.github.com/sapphi-red/vite-plugin-static-copy/issues/152">#152</a>)</li>
<li>See full diff in <a href="https://github.com/sapphi-red/vite-plugin-static-copy/compare/vite-plugin-static-copy@2.3.0...vite-plugin-static-copy@2.3.2">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=vite-plugin-static-copy&package-manager=npm_and_yarn&previous-version=2.3.0&new-version=2.3.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

You can trigger a rebase of this PR by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot merge` will merge this PR after your CI passes on it
- `@dependabot squash and merge` will squash and merge this PR after your CI passes on it
- `@dependabot cancel merge` will cancel a previously requested merge and block automerging
- `@dependabot reopen` will reopen this PR if it is closed
- `@dependabot close` will close this PR and stop Dependabot recreating it. You can achieve the same result by closing it manually
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)
You can disable automated security fix PRs for this repo from the [Security Alerts page](https://github.com/hazelgrove/hazel/network/alerts).

</details>

> **Note**
> Automatic rebases have been disabled on this pull request as it has been open for over 30 days.



## #2007 Vim-like Keybindings / Cryplo
created 2025-11-07T22:32:14Z merged None base dev
BODY (mutable, retrieved today):


comments / cyrus- / 2026-04-21T12:42:44Z
closing in favor of a future design based on #2166 


## #2028 [WIP] Fix recursion issue causing stepper to break / Copilot
created 2025-11-25T15:29:58Z merged None base dev
BODY (mutable, retrieved today):
- [x] Understand the issue: `(fix -> )()` causes stepper to blow up with too much recursion in elaboration
- [x] Add test case to reproduce the issue in Test_Stepper.re
- [ ] Identify root cause through test failure analysis
- [ ] Implement fix
- [ ] Run code review and security scan

<!-- START COPILOT CODING AGENT SUFFIX -->



<details>

<summary>Original prompt</summary>

> 
> ----
> 
> *This section details on the original issue you should resolve*
> 
> <issue_title>(fix   ->  )() breaks stepper</issue_title>
> <issue_description>`(fix   ->  )()` causes stepper to blow up with too much recursion in elaboration</issue_description>
> 
> ## Comments on the Issue (you are @copilot in this section)
> 
> <comments>
> </comments>
> 


</details>

- Fixes hazelgrove/hazel#1962

<!-- START COPILOT CODING AGENT TIPS -->
---

💬 We'd love your input! Share your thoughts on Copilot coding agent in our [2 minute survey](https://gh.io/copilot-coding-agent-survey).



## #2102 Merge dev into projector-in-terms branch / Copilot
created 2026-02-04T20:55:35Z merged None base dev
BODY (mutable, retrieved today):
Resolved merge conflict between the projector-in-terms refactor and recent dev changes.

## Conflict Resolution

The conflict arose in `ProjectorCore.re` where:
- **This PR**: Extracted `Kind` module to `src/language/ProjectorKind.re` to break dependency cycle between language and haz3lcore libraries
- **dev branch**: Reordered `livelit_projectors` list to reflect Csv/Card competition for empty list context

## Changes

- Updated `ProjectorKind.re` with reordered projector list from dev:
  ```reason
  let livelit_projectors: list(t) = [
    Checkbox, Slider, SliderF, TextArea,
    Csv,  /* Competes with Card for empty list */
    Card, /* Competes with Csv for empty list */
    Livelit,
  ];
  ```
- Kept external module reference in `ProjectorCore.re`: `module Kind = Language.ProjectorKind;`
- Merged probe fixes, workflow cleanup, and other dev improvements

The refactor maintaining Kind as an external module is preserved while incorporating latest functional changes from dev.

<!-- START COPILOT CODING AGENT TIPS -->
---

✨ Let Copilot coding agent [set things up for you](https://github.com/hazelgrove/hazel/issues/new?title=✨+Set+up+Copilot+instructions&body=Configure%20instructions%20for%20this%20repository%20as%20documented%20in%20%5BBest%20practices%20for%20Copilot%20coding%20agent%20in%20your%20repository%5D%28https://gh.io/copilot-coding-agent-tips%29%2E%0A%0A%3COnboard%20this%20repo%3E&assignees=copilot) — coding agent works faster and does higher quality work when set up for your repo.



## #2113 chore: update dependencies / cyrus-
created 2026-02-06T09:28:07Z merged 2026-04-21T14:24:03Z base dev
BODY (mutable, retrieved today):
Automated update from `make change-deps` based on `dev`.


## #2169 Rewrite float negation as 0.0 -. e in ExpToSegment / dm0n3y
created 2026-03-11T21:47:57Z merged 2026-04-21T12:24:50Z base dev
BODY (mutable, retrieved today):
Terms support float-specific unary negation but tiles/segments don't at the moment. ExpToSegment sends both float negation and integer negation to the same UnaryMinus op, which means well-typed negative floats constructed as terms, serialized to segments, then parsed again as terms gain error holes. This modifies ExpToSegment so that it rewrites `-. f` in term form is serialized to `0.0 -. f` in segment form. Specifically, the parenthesize pass now rewrites UnOp(Float(Minus), e) to BinOp(Float(Minus), 0.0, e).


## #2171 Add alt+shift+left/right to extend selection by token / Copilot
created 2026-03-12T18:17:23Z merged 2026-04-21T12:23:48Z base dev
BODY (mutable, retrieved today):
`alt+shift+left` and `alt+shift+right` were unbound — pressing them had no effect. They should extend the selection by token (word), consistent with `alt+left/right` moving by token and matching standard editor conventions.

## Changes

- **`Keyboard.re`**: Added pattern match for `alt+shift+arrow` (shift↓, alt↓, no meta/ctrl) mapping to `Select(Resize(Local(Left/Right, ByToken)))`
- **`Shortcut.re`**: Added "Extend Selection Left/Right by Token" entries with `alt+shift+left` / `alt+shift+right` hotkeys so they appear in the command palette

<!-- START COPILOT ORIGINAL PROMPT -->



<details>

<summary>Original prompt</summary>

> 
> ----
> 
> *This section details on the original issue you should resolve*
> 
> <issue_title>alt-shift-(left/right) should extend selection by word</issue_title>
> <issue_description></issue_description>
> 
> <agent_instructions>you can look at Shortcut.re to see how shortcuts are wired and use something like ActiveEditor(Select(Resize(Local(Left, ByToken))))</agent_instructions>
> 
> ## Comments on the Issue (you are @copilot in this section)
> 
> <comments>
> </comments>
> 


</details>



<!-- START COPILOT CODING AGENT SUFFIX -->

- Fixes hazelgrove/hazel#2170

<!-- START COPILOT CODING AGENT TIPS -->
---

💬 Send tasks to Copilot coding agent from [Slack](https://gh.io/cca-slack-docs) and [Teams](https://gh.io/cca-teams-docs) to turn conversations into code. Copilot posts an update in your thread when it's finished.


## #2180 feat: Wadler/Lindig-style pretty printer with Cmd+S and result formatting / 7h3kk1d
created 2026-03-18T15:17:38Z merged 2026-04-23T13:40:17Z base dev
BODY (mutable, retrieved today):
## Summary
- Adds a Wadler/Lindig-style segment formatter (`PrettySegment.re`) for better code layout
- Integrates Cmd+S / Ctrl+S shortcut for reparse/reformat in the editor
- **Applies pretty printing to evaluation results**, so multi-line output (e.g., large records, nested expressions) is formatted with proper line breaks instead of rendering as a single long line
- Adds comprehensive test suite (`Test_PrettyPrint.re` — 880+ lines)
- Fixes reverse application (`|>`) parenthesization precedence
- Removes space before `=` in labeled tuple formatting (`a= 1` not `a = 1`)

The main motivation here is having **multi-line result output** — the specific formatting rules are secondary and can be refined over time. This copies the pretty printer from #2126 but without the probe changes so we can merge it sooner.

cc @disconcision

## Test plan
- [x] `make dev` compiles successfully
- [x] All tests pass (`make test`)
- [x] Verify Cmd+S reformats code correctly in the browser
- [x] Verify evaluation results display with proper line breaks for large expressions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

comments / disconcision / 2026-03-18T15:29:42Z
seems to lose some module round trip tests? maybe that came from my PR but was accidental if so i think

reviews / cyrus- / 2026-04-02T18:59:39Z
quibbles:

1. should only put expressions on same line if they are simple forms, not lets and other "block-like" forms

<img width="1098" height="268" alt="Image" src="https://github.com/user-attachments/assets/7127d276-f3b3-4633-89ac-8b1c5862542d" />

2. trailing holes should be on their own line at the end of "block-like" forms

<img width="791" height="393" alt="Image" src="https://github.com/user-attachments/assets/3b1b171e-c558-4bed-b087-edb6b8691443" />


## #2191 Variable highlighting cleanup / disconcision
created 2026-03-23T04:22:46Z merged 2026-04-21T12:22:14Z base dev
BODY (mutable, retrieved today):
- Pure refactor. Avoids allocation.

reviews / 7h3kk1d / 2026-03-23T20:00:26Z
I finished a functional review and it seems great. Haven't finished looking at the code. But feel free to merge if you don't care about that.

review-comments / 7h3kk1d / 2026-03-23T19:55:42Z
Extremely nitpicky but this is where using streams would not allocate

review-comments / 7h3kk1d / 2026-03-23T19:57:25Z
Should either make dynamics part of the _ or name the other one

review-comments / 7h3kk1d / 2026-03-23T19:59:23Z
I don't have a real understanding about what's going on here. Did we have the wrong id before and because we're using type-directed inference it should be the id of the analyzed type?

review-comments / disconcision / 2026-03-23T21:32:56Z
are we using these anywhere atm?

review-comments / 7h3kk1d / 2026-03-23T21:40:23Z
Whoops I meant Seq and not Stream. There's a few calls to List.of_seq in ListUtil and StringUtil


## #2195 Bump picomatch / dependabot[bot]
created 2026-03-25T21:32:25Z merged 2026-04-21T12:20:59Z base dev
BODY (mutable, retrieved today):
Bumps  and [picomatch](https://github.com/micromatch/picomatch). These dependencies needed to be updated together.
Updates `picomatch` from 4.0.2 to 4.0.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/micromatch/picomatch/releases">picomatch's releases</a>.</em></p>
<blockquote>
<h2>4.0.4</h2>
<p>This is a security release fixing several security relevant issues.</p>
<h2>What's Changed</h2>
<ul>
<li>Fix for <a href="https://github.com/micromatch/picomatch/security/advisories/GHSA-c2c7-rcm5-vvqj">CVE-2026-33671</a></li>
<li>Fix for <a href="https://github.com/micromatch/picomatch/security/advisories/GHSA-3v7f-55p6-f55p">CVE-2026-33672</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/micromatch/picomatch/compare/4.0.3...4.0.4">https://github.com/micromatch/picomatch/compare/4.0.3...4.0.4</a></p>
<h2>4.0.3</h2>
<h2>What's Changed</h2>
<ul>
<li>fix: exception when glob pattern contains <code>constructor</code> by <a href="https://github.com/Jason3S"><code>@​Jason3S</code></a> in <a href="https://redirect.github.com/micromatch/picomatch/pull/144">micromatch/picomatch#144</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/Jason3S"><code>@​Jason3S</code></a> made their first contribution in <a href="https://redirect.github.com/micromatch/picomatch/pull/144">micromatch/picomatch#144</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/micromatch/picomatch/compare/4.0.2...4.0.3">https://github.com/micromatch/picomatch/compare/4.0.2...4.0.3</a></p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/micromatch/picomatch/commit/e5474fc1a4d7991870058170407dda8a42be5334"><code>e5474fc</code></a> Publish 4.0.4</li>
<li><a href="https://github.com/micromatch/picomatch/commit/4516eb521f13a46b2fe1a1d2c9ef6b20ddc0e903"><code>4516eb5</code></a> Merge commit from fork</li>
<li><a href="https://github.com/micromatch/picomatch/commit/5eceecd27543b8e056b9307d69e105ea03618a7d"><code>5eceecd</code></a> Merge commit from fork</li>
<li><a href="https://github.com/micromatch/picomatch/commit/0db7dd70651ca7c8265601c0442a996ed32e3238"><code>0db7dd7</code></a> Run benchmark again against latest minimatch version (<a href="https://redirect.github.com/micromatch/picomatch/issues/161">#161</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/95003777eb1c60dec09495a8231fa2ba4054d76a"><code>9500377</code></a> docs: clarify what brace expansion syntax is and isn't supported (<a href="https://redirect.github.com/micromatch/picomatch/issues/134">#134</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/2661f23eca86c8b4a2b14815b9b2b3b74bd5a171"><code>2661f23</code></a> fix typo in globstars.js test name (<a href="https://redirect.github.com/micromatch/picomatch/issues/138">#138</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/1798b07e9df59500b9cf567294d44d559032f4c7"><code>1798b07</code></a> docs: fix <code>makeRe</code> example (<a href="https://redirect.github.com/micromatch/picomatch/issues/143">#143</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/9d76bc57a03b7f57cc4ca516c8071daf632bafd8"><code>9d76bc5</code></a> chore: undocument removed options (<a href="https://redirect.github.com/micromatch/picomatch/issues/146">#146</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/e4d718bbfb47e4f030ab2612b5b04a9297fe272d"><code>e4d718b</code></a> Remove unused time-require (<a href="https://redirect.github.com/micromatch/picomatch/issues/160">#160</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/38dffeb16221cc8eb8981524fb6895dd2aaaba76"><code>38dffeb</code></a> chore(deps): pin dependencies (<a href="https://redirect.github.com/micromatch/picomatch/issues/158">#158</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/micromatch/picomatch/compare/4.0.2...4.0.4">compare view</a></li>
</ul>
</details>
<br />

Updates `picomatch` from 2.3.1 to 2.3.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/micromatch/picomatch/releases">picomatch's releases</a>.</em></p>
<blockquote>
<h2>4.0.4</h2>
<p>This is a security release fixing several security relevant issues.</p>
<h2>What's Changed</h2>
<ul>
<li>Fix for <a href="https://github.com/micromatch/picomatch/security/advisories/GHSA-c2c7-rcm5-vvqj">CVE-2026-33671</a></li>
<li>Fix for <a href="https://github.com/micromatch/picomatch/security/advisories/GHSA-3v7f-55p6-f55p">CVE-2026-33672</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/micromatch/picomatch/compare/4.0.3...4.0.4">https://github.com/micromatch/picomatch/compare/4.0.3...4.0.4</a></p>
<h2>4.0.3</h2>
<h2>What's Changed</h2>
<ul>
<li>fix: exception when glob pattern contains <code>constructor</code> by <a href="https://github.com/Jason3S"><code>@​Jason3S</code></a> in <a href="https://redirect.github.com/micromatch/picomatch/pull/144">micromatch/picomatch#144</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/Jason3S"><code>@​Jason3S</code></a> made their first contribution in <a href="https://redirect.github.com/micromatch/picomatch/pull/144">micromatch/picomatch#144</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/micromatch/picomatch/compare/4.0.2...4.0.3">https://github.com/micromatch/picomatch/compare/4.0.2...4.0.3</a></p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/micromatch/picomatch/commit/e5474fc1a4d7991870058170407dda8a42be5334"><code>e5474fc</code></a> Publish 4.0.4</li>
<li><a href="https://github.com/micromatch/picomatch/commit/4516eb521f13a46b2fe1a1d2c9ef6b20ddc0e903"><code>4516eb5</code></a> Merge commit from fork</li>
<li><a href="https://github.com/micromatch/picomatch/commit/5eceecd27543b8e056b9307d69e105ea03618a7d"><code>5eceecd</code></a> Merge commit from fork</li>
<li><a href="https://github.com/micromatch/picomatch/commit/0db7dd70651ca7c8265601c0442a996ed32e3238"><code>0db7dd7</code></a> Run benchmark again against latest minimatch version (<a href="https://redirect.github.com/micromatch/picomatch/issues/161">#161</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/95003777eb1c60dec09495a8231fa2ba4054d76a"><code>9500377</code></a> docs: clarify what brace expansion syntax is and isn't supported (<a href="https://redirect.github.com/micromatch/picomatch/issues/134">#134</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/2661f23eca86c8b4a2b14815b9b2b3b74bd5a171"><code>2661f23</code></a> fix typo in globstars.js test name (<a href="https://redirect.github.com/micromatch/picomatch/issues/138">#138</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/1798b07e9df59500b9cf567294d44d559032f4c7"><code>1798b07</code></a> docs: fix <code>makeRe</code> example (<a href="https://redirect.github.com/micromatch/picomatch/issues/143">#143</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/9d76bc57a03b7f57cc4ca516c8071daf632bafd8"><code>9d76bc5</code></a> chore: undocument removed options (<a href="https://redirect.github.com/micromatch/picomatch/issues/146">#146</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/e4d718bbfb47e4f030ab2612b5b04a9297fe272d"><code>e4d718b</code></a> Remove unused time-require (<a href="https://redirect.github.com/micromatch/picomatch/issues/160">#160</a>)</li>
<li><a href="https://github.com/micromatch/picomatch/commit/38dffeb16221cc8eb8981524fb6895dd2aaaba76"><code>38dffeb</code></a> chore(deps): pin dependencies (<a href="https://redirect.github.com/micromatch/picomatch/issues/158">#158</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/micromatch/picomatch/compare/4.0.2...4.0.4">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)
You can disable automated security fix PRs for this repo from the [Security Alerts page](https://github.com/hazelgrove/hazel/network/alerts).

</details>


## #2198 Keyboard architecture refactor: Key.handler, ContextualAction, focus decentralization / Negabinary
created 2026-03-30T15:00:12Z merged 2026-04-22T12:50:03Z base dev
BODY (mutable, retrieved today):
## Summary

 1. Change the way keyboard handling works. (Previously the root element was always focussed and it passed key events down, now key events happen locally at the editor)
 2. Make NinjaKeys use contexual actions - so now the NinjaKeys actions can change based on what's selected.

### What changed

**Key.handler / Key.listener** — Reusable keyboard event wiring in Key.re. `handler` adds tabindex(0) for focusable components; `listener` is for containers that catch bubbled events (like #page).

**ContextualAction.t** — Unified type for actions that serve both keyboard shortcuts and command palette entries. Uses Effect.t(unit) so it's decoupled from Page.Update.t. Shortcut.re keeps its Page.Update.t type internally with a to_contextual_action converter. NinjaKeys.re consumes ContextualAction.t directly.

**Editors handle their own keyboard events** — Each CodeEditable editor now has its own Key.handler. Events are handled locally (context menu -> projector handoff -> Keyboard.handle_key_event) with Stop_propagation. Unhandled events bubble to Page.re for page-level shortcuts (undo/redo/F7/meta).

**Boundary escape** — Arrow keys at the true editor boundary (caret Outer, no neighbor, no ancestors) call `~escape(direction)` so parents can navigate between cells/projectors. Direction means "side to escape TO" not "key pressed".

**Projector escape focus** — TextAreaProj now focuses the parent .code-editor element after blur during escape, so the editor regains keyboard focus.

**cursor.contextual_actions** — The cursor type has a new contextual_actions field and with_actions helper, enabling future per-component dynamic actions.

**EditMode.re** — New type bundling inject, escape, take_focus, and focus for editor views.

### Non-obvious gotchas (from splices trial-and-error)

- **Arrow keys trigger scroll with tabindex(0)** — must Prevent_default on handled arrow events
- **Boundary escape must check ancestors == []** — without this, cursor gets stuck inside nested expressions (let/in, parens) because caret==Outer with no neighbor is also true at edges of nested groups
- **Projector shortcuts must be re-registered** — when moving keyboard handling into component-level handlers, projector shortcuts (Alt+F etc.) don't come along for free
- **Escape direction = side to escape TO** — not which key was pressed. Getting this backwards breaks projector navigation
- **Projector blur loses focus** — after TextAreaProj blurs itself, focus goes to body. Must explicitly focus parent .code-editor
- **First click needs tabindex always** — editor elements need tabindex(0) even when not selected, otherwise first click gives DOM focus to the element but Key.handler only appears after MakeActive re-render, requiring a second click

comments / disconcision / 2026-03-30T15:53:37Z
patchwork detection??? claude may be lost in the multiverse again

comments / Negabinary / 2026-03-30T16:00:32Z
> patchwork detection??? claude may be lost in the multiverse again

lol I was hoping you'd know what it meant by that

comments / Negabinary / 2026-03-30T16:05:27Z
## Known issues (in progress)

- **Keys don't work after first click, only after second** — First click dispatches MakeActive (re-renders with selected=true and Key.handler), but DOM focus isn't on the editor element until a second click
- **Selection highlighting shows black boxes** — tabindex(0) on the editor div is causing browser-native focus/selection outlines
- **Handoff out of projectors doesn't work** — Arrow key escape from projectors not wired up yet

Working on fixes.

comments / Negabinary / 2026-03-31T15:30:47Z
## Latest: Distribute contextual actions, wire EditMode, remove dead code

This commit cleans up the dead code from the initial refactor and moves the architecture closer to the `projector-unsegment` pattern.

### What changed

**Contextual actions distributed to their layers** (replaces `Shortcut.re`):
- **Page level** — undo/redo, benchmark, settings toggles, navigation, selection, projection, TyDi, reparse, introduce, export-for-init
- **ScratchMode** — export, encode, buffer management (add/rename/delete slide)
- **ExercisesMode** — export submission + instructor exports
- Each layer builds its own `ContextualAction.t` list using `ContextualAction.mk`, added to the cursor via `Cursor.with_actions`
- `NinjaKeys.initialize` now called from `Page.View.view` using `cursor.contextual_actions` (dynamic per-render, not static at startup)

**EditMode wired into CodeEditable**:
- `CodeEditable.View.view` takes `~edit_mode: EditMode.t(Update.t, unit)` instead of separate `~inject`, `~selected`, `~escape` params
- All 7 callers updated (CellEditor, InductionStep, InductionCase, MissingStep, CodeSelectable, StepperEditor, EvalResult)
- `EditMode.ReadOnly` used by CellEditor when locked

**Dead code removed** (net -11 lines):
- `EditorView.re` — unused scaffolding (56 lines, zero callers)
- `Shortcut.re` — fully replaced by per-layer actions (311 lines)
- `Selection` modules from `History.re` and `Logged.re` (no external callers)
- `Page.Selection.handle_key_event` (editors handle their own keys now)

### Architecture direction

This follows the `projector-unsegment` pattern where each layer owns its contextual actions. The `~inject` parameter is threaded through `get_cursor_info` at each level (Editors → ScratchMode/ExercisesMode/TutorialsMode) so each layer can build effects for its own actions. The cursor accumulates actions as it flows up through the layers.

comments / Negabinary / 2026-03-31T15:48:12Z
## Follow-up: Remove dead handle_key_event chain

Removed 305 lines of dead `handle_key_event` routing across 23 files. Every removed function was pure delegation (call next level's handler + wrap result in local update type) — no logic lost.

**Removed from:**
- **Module type signatures:** `StepInterface.STEP`, `StepInterface.STEPPER`
- **Stepper dispatch:** `StepperBase.StepKind`, `StepperBase.Stepper` (recursive dispatcher)
- **Stepper focus layer:** `StepperView.Focus`, `Theorems.Focus`
- **Step implementations:** SingleStep, InductionStep, InductionCase, MissingStep, ForallStep, AxiomStep, AlgebriteStep, AxiomsBox
- **Editor routing:** Editors, ScratchMode, TutorialsMode, TutorialMode, ExercisesMode, ExerciseMode, TheoremExerciseMode, CellEditor, EvalResult, CodeSelectable, StepperEditor

**What's still live:**
- `CodeEditable.Selection.handle_key_event` — called from `key_handler_attr` (the new per-editor handler)
- `Keyboard.handle_key_event` — maps `Key.t` → `Action.t`
- `Page.View.handle_key_event` — page-level keys (undo/redo/benchmark)

comments / disconcision / 2026-04-01T18:04:47Z
@Negabinary is this a pure refactor or does it add functionality? the boundary stuff sort of implies you can use arrows to move between cells now?

comments / Negabinary / 2026-04-01T18:28:00Z
@disconcision pure refactor, you can't use keyboard to go between cells - though I guess that would be easier to implement now

comments / Negabinary / 2026-04-02T18:10:14Z
TODO:
- [ ] Make it clear when focus is lost

comments / cyrus- / 2026-04-09T23:05:31Z
@Negabinary when I open up the command palette and do a Cmd+A to select all, it seems to do the select all in the last editor rather than in the command palette. this doesn't seem to happen for other text boxes, e.g. in the Hazel Assistant sidebar, but maybe points to something that isn't working right.

comments / cyrus- / 2026-04-21T12:08:41Z
Escape key not working + conflicts


## #2208 Bump vite from 6.3.4 to 6.4.2 / dependabot[bot]
created 2026-04-07T02:46:08Z merged 2026-04-21T12:16:40Z base dev
BODY (mutable, retrieved today):
Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 6.3.4 to 6.4.2.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/vitejs/vite/releases">vite's releases</a>.</em></p>
<blockquote>
<h2>v6.4.2</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v6.4.2/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v6.4.1</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v6.4.1/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v6.4.0</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v6.4.0/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v6.3.7</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v6.3.7/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
<h2>v6.3.6</h2>
<p>Please refer to <a href="https://github.com/vitejs/vite/blob/v6.3.6/packages/vite/CHANGELOG.md">CHANGELOG.md</a> for details.</p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/vitejs/vite/blob/v6.4.2/packages/vite/CHANGELOG.md">vite's changelog</a>.</em></p>
<blockquote>
<h2><!-- raw HTML omitted -->6.4.2 (2026-04-06)<!-- raw HTML omitted --></h2>
<ul>
<li>fix: apply server.fs check to env transport (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22159">#22159</a>) (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22163">#22163</a>) (<a href="https://github.com/vitejs/vite/commit/fe28e47e9463e4c9619f94bfa06d2f8f1411b44b">fe28e47</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/22159">#22159</a> <a href="https://redirect.github.com/vitejs/vite/issues/22163">#22163</a></li>
<li>fix: avoid path traversal with optimize deps sourcemap handler (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22161">#22161</a>) (<a href="https://github.com/vitejs/vite/commit/ca4da5d1fb45c9cfdce606aa30825095791b164b">ca4da5d</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/22161">#22161</a></li>
</ul>
<h2><!-- raw HTML omitted -->6.4.1 (2025-10-20)<!-- raw HTML omitted --></h2>
<ul>
<li>fix(dev): trim trailing slash before <code>server.fs.deny</code> check (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20968">#20968</a>) (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20969">#20969</a>) (<a href="https://github.com/vitejs/vite/commit/1114b5d7ea03e26572708715343bec69db4536e8">1114b5d</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/20968">#20968</a> <a href="https://redirect.github.com/vitejs/vite/issues/20969">#20969</a></li>
</ul>
<h2>6.4.0 (2025-10-15)</h2>
<ul>
<li>feat: allow passing down resolved config to vite's createServer (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20932">#20932</a>) (<a href="https://github.com/vitejs/vite/commit/ca6455ee9eb6111a9caa9810506a1b9ac96a520a">ca6455e</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/20932">#20932</a></li>
</ul>
<h2><!-- raw HTML omitted -->6.3.7 (2025-10-14)<!-- raw HTML omitted --></h2>
<ul>
<li>fix(esbuild): inject esbuild helpers correctly for esbuild 0.25.9+ (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20940">#20940</a>) (<a href="https://github.com/vitejs/vite/commit/c59a222aa584c087cfe710173de1b9ecb597a3ff">c59a222</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/20940">#20940</a></li>
</ul>
<h2><!-- raw HTML omitted -->6.3.6 (2025-09-08)<!-- raw HTML omitted --></h2>
<ul>
<li>fix: apply <code>fs.strict</code> check to HTML files (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20736">#20736</a>) (<a href="https://github.com/vitejs/vite/commit/0ab19ea9fcb66f544328f442cf6e70f7c0528d5f">0ab19ea</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/20736">#20736</a></li>
<li>fix: upgrade sirv to 3.0.2 (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20735">#20735</a>) (<a href="https://github.com/vitejs/vite/commit/e11d24008b97d4ca731ecc1a3b95260a6d12e7e0">e11d240</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/20735">#20735</a></li>
<li>test: detect ts support via <code>process.features</code> (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20544">#20544</a>) (<a href="https://github.com/vitejs/vite/commit/7d9922972b62329d37a71d4da5a4a382d0bf8a79">7d99229</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/20544">#20544</a></li>
</ul>
<h2><!-- raw HTML omitted -->6.3.5 (2025-05-05)<!-- raw HTML omitted --></h2>
<ul>
<li>fix(ssr): handle uninitialized export access as undefined (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/19959">#19959</a>) (<a href="https://github.com/vitejs/vite/commit/fd38d076fe2455aac1e00a7b15cd51159bf12bb5">fd38d07</a>), closes <a href="https://redirect.github.com/vitejs/vite/issues/19959">#19959</a></li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/vitejs/vite/commit/6b3fad02abd550bd7b79934ff92c58dbd7f33045"><code>6b3fad0</code></a> release: v6.4.2</li>
<li><a href="https://github.com/vitejs/vite/commit/ca4da5d1fb45c9cfdce606aa30825095791b164b"><code>ca4da5d</code></a> fix: avoid path traversal with optimize deps sourcemap handler (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22161">#22161</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/fe28e47e9463e4c9619f94bfa06d2f8f1411b44b"><code>fe28e47</code></a> fix: apply server.fs check to env transport (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22159">#22159</a>) (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/22163">#22163</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/5487f4f641f70c47ea05fd101a4319897df048b3"><code>5487f4f</code></a> release: v6.4.1</li>
<li><a href="https://github.com/vitejs/vite/commit/1114b5d7ea03e26572708715343bec69db4536e8"><code>1114b5d</code></a> fix(dev): trim trailing slash before <code>server.fs.deny</code> check (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20968">#20968</a>) (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20969">#20969</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/f12697c0f64b9a37196b9ab218a0911829d5b103"><code>f12697c</code></a> release: v6.4.0</li>
<li><a href="https://github.com/vitejs/vite/commit/ca6455ee9eb6111a9caa9810506a1b9ac96a520a"><code>ca6455e</code></a> feat: allow passing down resolved config to vite's createServer (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20932">#20932</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/0e173d83681daa31be10fa8a62d56b1ec84690af"><code>0e173d8</code></a> release: v6.3.7</li>
<li><a href="https://github.com/vitejs/vite/commit/c59a222aa584c087cfe710173de1b9ecb597a3ff"><code>c59a222</code></a> fix(esbuild): inject esbuild helpers correctly for esbuild 0.25.9+ (<a href="https://github.com/vitejs/vite/tree/HEAD/packages/vite/issues/20940">#20940</a>)</li>
<li><a href="https://github.com/vitejs/vite/commit/3f337c5e24504e51188d29c970de1416ee523dbb"><code>3f337c5</code></a> release: v6.3.6</li>
<li>Additional commits viewable in <a href="https://github.com/vitejs/vite/commits/v6.4.2/packages/vite">compare view</a></li>
</ul>
</details>
<details>
<summary>Maintainer changes</summary>
<p>This version was pushed to npm by [GitHub Actions](<a href="https://www.npmjs.com/~GitHub">https://www.npmjs.com/~GitHub</a> Actions), a new releaser for vite since your current version.</p>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=vite&package-manager=npm_and_yarn&previous-version=6.3.4&new-version=6.4.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)
You can disable automated security fix PRs for this repo from the [Security Alerts page](https://github.com/hazelgrove/hazel/network/alerts).

</details>


## #2212 (Just a) Stalaborator / Negabinary
created 2026-04-10T20:07:33Z merged None base dev
BODY (mutable, retrieved today):
Zips up statics and elaborator into one pass. Makes our statics file look a lot more like the rules.

comments / cyrus- / 2026-04-21T12:09:12Z
closing in favor of #2213 


## #2213 (All-out) Elastatics / Negabinary
created 2026-04-10T20:10:35Z merged 2026-04-22T12:53:06Z base dev
BODY (mutable, retrieved today):
Bigger more ambitious version of #2212

- combines statics & elaborator
- replaces self with separated Mark.t, Warning.t, and Message.t
- applies heavy cleaning to all these files

Statics rules will look much more like rules we'd write in a paper, putting types, marks, and the like all in one place.

I encourage you to read Statics.re for yourself and drink it in.

todos
 - [x] tidy up the pattern cases of statics
 - [x] do a pass over custom statics

Left for a future pr
 - There's more work that needs to be done around Message.re: at the moment it's not very well defined.

reviews / 7h3kk1d / 2026-04-16T16:32:19Z
🎉‼️😍
The PR is pretty huge so I haven't had the chance to review it in entirety, but I wanted to leave intermediate comments (about 1/4 done).

Overall architecturally this seems like a massive improvement. The removal of the intermediate layers of Self/Info make this much easier to make changes and to read the current code. In addition the interleaving of elaboration/statics makes it much easier to keep the two in sync and should drastically improve type/static-directed elaboration without having to sidechannel the information.

I have a few comments below that range from small code-style stuff to some architectural questions especially centered around error/problem/message types.

review-comments / 7h3kk1d / 2026-04-15T14:49:35Z
Remove reference to Self.re

review-comments / 7h3kk1d / 2026-04-16T14:45:38Z
Is there a reason we have elab_term for exp but not for the others?

review-comments / 7h3kk1d / 2026-04-16T15:05:23Z
This PR might not be the right place to handle it but introducing the mark abstraction underneath the weak `problem` abstraction might require some more thought. The live typing pr https://github.com/hazelgrove/hazel/pull/1988 is also going to add the _live typing errors_ to the problem sidebar.

It seems reasonable that there are multiple marks for a given form and maybe each of these marks should have a direct correspondent in the problem list. Maybe the cursor inspector itself shows the highest priority problem in the case of multiple.

Alternatively if we want to remove the problem notion entirely maybe everything could live on marks, but then we need some way of re-incorporating the live typing marks post-dynamics.

review-comments / 7h3kk1d / 2026-04-16T15:07:33Z
Is it worth pulling out the marks that are only available on certain forms to separate types just for organization reasons?

review-comments / 7h3kk1d / 2026-04-16T15:13:25Z
My personal preference would be to use `ppx_deriving.ord` or `ppx_variants_conv` and leave a comment saying that declaration order is load-bearing. This also works but it's been annoying juggling the numbers in Precedence. I also don't know if there's any reason it shouldn't be a total order

review-comments / 7h3kk1d / 2026-04-16T15:14:19Z
In the same sense I think the warnings being conjoined with marks also makes sense.

review-comments / 7h3kk1d / 2026-04-16T15:16:20Z
unrelated to PR but I see below we have Operators.default_mode

review-comments / 7h3kk1d / 2026-04-16T15:23:22Z
I feel somewhat unsure of the Message separation for being exclusively well formed payloads. In some sense these feel more like informational non-error marks as they're not the message as shown to a user but stuff that would be useful in constructing the happy path message (only in the context where there are no marks).

review-comments / 7h3kk1d / 2026-04-16T15:31:25Z
I don't know if we want to call this self or syn_ty but. Ithink we should clarify that this is not purely synthetic.

It's computed after analysis-directed rewrites like literal replacement (Int(1) → Nat(1) via ana/use_mode) and automatic label introduction for labeled tuples — so it's not context-free nor is it pure syn.

review-comments / 7h3kk1d / 2026-04-16T15:33:17Z
Long term this might live better with Mark code

review-comments / 7h3kk1d / 2026-04-16T15:35:24Z
Can we put this in a different file if it's not testing the info?

review-comments / 7h3kk1d / 2026-04-16T15:39:07Z
This seems to be unused
```suggestion
```

review-comments / 7h3kk1d / 2026-04-16T15:39:52Z
This is the most nitpicky but I don't like the pipelining when we're already passing multiple args.

review-comments / 7h3kk1d / 2026-04-16T15:40:02Z
Feel free to ignore me though

review-comments / 7h3kk1d / 2026-04-16T15:45:57Z
These are exclusively used in tests now so we should consider moving them or removing them.

review-comments / 7h3kk1d / 2026-04-16T15:48:40Z
We should just accumulate to a set rather than allocate a list then sort_uniq. This code is also directly duplicated below.

review-comments / 7h3kk1d / 2026-04-16T16:03:39Z
Unrelated to pr

If you add the Id.Set to Id.re
```
module Set = Set.Make(Uuidm);
```
you can use a set for the accumulator and we should just use a fold rather than full recursion
```reason
let let_definition_path = (~statics: t, ~id: Id.t): list(Pat.t) => {
    let rec contains_id = (target: Id.t, ids: list(Id.t)): bool =>
      switch (ids) {
      | [] => false
      | [head, ...tail] =>
        Id.equal(head, target) || contains_id(target, tail)
      };

    let rec gather =
            (remaining: list(Id.t), seen: list(Id.t), acc: list(Pat.t))
            : list(Pat.t) =>
      switch (remaining) {
      | [] => acc
      | [current_id, ...rest] =>
        let acc' =
          switch (lookup(current_id, statics)) {
          | Some(InfoExp({user_term: {term: Let(pat, def, _), _}, _})) =>
            contains_id(IdTagged.rep_id(def), seen) ? [pat, ...acc] : acc
          | _ => acc
          };
        gather(rest, [current_id, ...seen], acc');
      };

    switch (lookup(id, statics)) {
| Some(info) =>
      let ancestors: list(Id.t) = Info.ancestors_of(info);
      let collected: list(Pat.t) = gather(ancestors, [id], []);
      List.rev(collected);
| _ => []
};
};
```

review-comments / 7h3kk1d / 2026-04-16T16:09:34Z
Might be worth moving these to a map helper eventually. I also think leaving a comment on map_m saying it's a traverse over a state monad may make it easier for people to understand what's going on. Or alternatively add the types.

review-comments / 7h3kk1d / 2026-04-16T16:12:16Z
I don't remember how this used to work but it's worrisome to remember to call ana_skip_explicit_nonlabel everywhere

review-comments / 7h3kk1d / 2026-04-16T16:14:49Z
I vote we can continue to call the term elaborated

review-comments / 7h3kk1d / 2026-04-16T16:25:40Z
I can't tell where it's happening yet but the label argument like:
```
omit_labels((a=1,b=2), `a`)
```

if you have the cursor on the `a` it's showing a synthesized type of hole in the cursor inspector. This is a regression.

review-comments / Negabinary / 2026-04-17T12:47:32Z
Hm yeah I don't think I have enough background on the concept of a "problem" to make a call here - I'm tempted to just leave marks as they are and leave it to future work to define this abstraction.

review-comments / Negabinary / 2026-04-17T12:56:18Z
I agree; Message is a little ill-defined in this PR. I believe we didn't used to have information displayed to the user outside of errors. I think that's a pretty good next step but I'd like to leave it beyond the scope of this PR I think.

review-comments / Negabinary / 2026-04-17T13:00:20Z
I don't think we can do this and do the priority ordering at the same time. I think I like priority ordering more.

review-comments / Negabinary / 2026-04-17T13:07:13Z
hm yeah I think I don't mind it because it's a fold, and I feel like the list is the obvious thing to put into a pipeling

review-comments / Negabinary / 2026-04-17T13:12:53Z
This function already existed but I deliberately renamed it to something more worrisome so it's clear how worrisome the contents are. It appears to be having the desired effect, I think I want to leave it as a wontfix though.

review-comments / Negabinary / 2026-04-17T13:13:56Z
Agreed; good catch - I didn't notice this codexism

review-comments / 7h3kk1d / 2026-04-17T13:29:22Z
>  I believe we didn't used to have information displayed to the user outside of errors.

I don't understand what you mean by this since we have the cursor inspector outside of errors. Unless you mean for the agent.

review-comments / Negabinary / 2026-04-17T17:04:42Z
Updated comment.

review-comments / Negabinary / 2026-04-17T17:04:57Z
only exp and pats have elaborations; just added it to pat.

review-comments / Negabinary / 2026-04-17T17:08:46Z
we discussed this; calling it elab_syn_ty

review-comments / Negabinary / 2026-04-17T17:09:17Z
Moved.

review-comments / Negabinary / 2026-04-17T17:09:52Z
Moved.

review-comments / Negabinary / 2026-04-17T17:11:13Z
hm looks like I forgot patch_elab_syn_ty_exp

review-comments / 7h3kk1d / 2026-04-17T17:17:06Z
@disconcision you may want to be looped in here. Matt and I talked and it seems like the self type could be the elaborated syn type if we make sure during elaboration we add all the implicit type-directed stuff to the term: empty list's type, variant constructors type, etc.

review-comments / 7h3kk1d / 2026-04-17T17:51:25Z
We should probably rename this and change the hover text if there is any.


## #2215 Fix fold projector breaking type definitions / disconcision
created 2026-04-17T09:49:55Z merged 2026-04-17T12:06:31Z base dev
BODY (mutable, retrieved today):
Closes #2214.
Closes #2216.


## #2219 fix missing record wildcard / cyrus-
created 2026-04-21T13:59:48Z merged 2026-04-21T14:11:21Z base dev
BODY (mutable, retrieved today):



## #2220 chore: update dependencies / cyrus-
created 2026-04-22T09:45:33Z merged 2026-04-22T11:03:12Z base dev
BODY (mutable, retrieved today):
Automated update from `make change-deps` based on `dev`.


## #2221 Show all applicable projectors in context menu / 7h3kk1d
created 2026-04-22T13:20:31Z merged 2026-05-12T15:48:18Z base dev
BODY (mutable, retrieved today):
Since Alt+L still fires ChooseLivelit which only picks the first livelit, only that first kind now displays the Alt+L shortcut — the rest of the livelits list with no hotkey to avoid a misleading hint. This is not currently observable since we don't have any overlapping projectors but it causes issue if you're creating new ones.


## #2222 Incremental evaluation / Negabinary
created 2026-04-22T14:12:05Z merged 2026-05-19T18:24:16Z base dev
BODY (mutable, retrieved today):
Working on a formalism at https://typst.app/project/r1zZKHltWXXBRyJcVkTc5k.
Everything up to "The Tuple Bottleneck" is proven and implemented in Hazel. 

<img width="596" height="250" alt="image" src="https://github.com/user-attachments/assets/c00da9d4-5faa-4432-a986-4e5ae5e1463b" />

During evaluation, this pr "freezes" any parts of the previous evaluation that haven't changed, and re-uses the values.

You can turn on some visual "ice" to show which sub-expressions are frozen by toggling "Incremental Reuse" in the nut menu.

The evaluator is passed a map of the previous evaluation at each top-level id. It is able to re-use an expression iff:

1. **The call stack is empty** (This is our notion of top-level)
2. **The elaboration has not changed** (Uses deep equality; every id in the program is checked at most once, so this check is quadratic in the length of the program)
3. **The co-context does not contain any dirty variables** (Variables are dirtied if the thing they are bound to has changed)
4. **The ids associated with the co-context has not changed since last time**
5. **The probe targets in the sub-expression have not changed**


## #2225 Refactor Problems sidebar; fix jumps in Exercise mode and folds / 7h3kk1d
created 2026-04-23T13:36:40Z merged 2026-06-02T15:36:42Z base dev
BODY (mutable, retrieved today):
Issue
-----
In ExerciseMode the Problems sidebar was broken in several ways:
  1. Clicking a problem row didn't jump to its tile.
  2. Clicking a hole never jumped, even after (1) was addressed.
  3. After a successful jump the target cell's caret was invisible.
  4. Problems from non-`user_impl` cells (notably Test Validation / your tests) never appeared in the sidebar at all.
  5. Read-only cells (e.g. Prelude in student mode) could have problems listed that were non-jumpable.
  6. Errors inside a fold projector had no jump target — the underlying ids aren't in `measured` because the projector replaces them with the folded view.
  7. None of the above worked for derivation / theorem slides (Exercise, Documentation, or Scratch). Tree judgement errors weren't surfaced and `Drv`-sort error messages rendered as empty rows.

Fixes
-----
1. Sidebar jump now uses the mode-aware dispatcher

   `ProblemSidebar.jump_to` used `ActiveEditor(Move(Goal(TileId id)))`, which only targets whichever cell currently has the cursor. In ExerciseMode the problem's tile almost always lives in a different cell than the focused one, so the action dropped silently.

   Switched to `Globals.Action.JumpToTile(id)`, which Page routes through `Editors.Selection.jump_to_tile` -> each mode's `Selection.jump_to_tile`. CodeExerciseMode's implementation scans `CodeExercise.positioned_editors` and emits both the correct editor update and the correct selection, so jumps land in the right cell. Scratch/Documentation/Tutorial modes already had their own `Selection.jump_to_tile`, so the change is a no-op there.

2. Editor-membership predicate now matches holes as well as tiles

   The `jump_to_tile` predicates in `CodeExerciseMode`, `CodeEditable`, `TutorialMode`, `DerivationExerciseMode`, and `TheoremExerciseMode` used `TermData.root_tile` to decide whether an id lived in a given editor. `root_tile` returns `None` for grouts, so hole ids (the `Hole`/`Syntax` categories in the sidebar) never matched any editor and the jump failed.

   Added `TermData.root_piece: Id.t -> t -> option(Piece.t)` returning the root piece for any variant (tiles, grouts, secondaries, projectors), and switched the predicates to use it. `root_tile` is refactored to delegate, so existing callers are unaffected.

3. Sidebar jump transfers DOM focus to the target cell

   ~~Caret visibility driven by model selection, not DOM focus. The caret CSS rule gated visibility on `:focus`, but DOM focus stays on the sidebar row that was clicked, so after a jump the caret stayed hidden. Switched the rule to `.selected` (model selection); DOM focus is not forcibly transferred.~~

   Reverted: gating the caret on `.selected` left it blinking on a cell that had lost DOM focus (e.g. after clicking elsewhere in the sidebar) — it looked active but ignored keystrokes. The caret rule is back to `:focus`. Instead, a jump now moves DOM focus to the target cell: the active `.code-editor` carries a stable id (`JsUtil.active_cell_id`) and the `JumpToTile` handler schedules `ProbePerform.FocusEffect.schedule_cell()`, executed in `after_display` (focus with `preventScroll` so it doesn't fight scroll-into-view). The editor now receives keystrokes after a jump and the caret correctly tracks focus.

4. Problems sidebar aggregates across all jumpable cells in every mode

   Sidebar.view built one `problem_context` from a single editor (`user_impl` in Exercise mode via `Update.get_editor`), so problems in `your_tests`, `prelude`, etc. never showed up. Drv slides surfaced only `setup`, missing `prelude` and every tree judgement.

   Replaced with a per-editor data structure owned by `haz3lcore` (see "Architecture" below). `Page.Update.get_problem_editors` now returns labeled editors. A cell's problems are listed iff the cell is *rendered* (regardless of read-only), so the lists can't drift from what's on screen. Coverage:
   - **Exercise / Code**: every cell that is rendered for the current user — `CodeExercise.shown_in(~instructor_mode)` — which now includes the read-only Prelude. ~~`CodeExercise.visible_in(~instructor_mode)`~~ (`visible_in` gated *editability*, not rendering, so it dropped the shown-read-only Prelude; it's been renamed `is_editable` and the sidebar/jump now use the new `shown_in`).
   - **Exercise / Derivation**, **Documentation / Drv**, **Scratch / Drv**: `Prelude` (exercise mode only — it isn't rendered on scratch/documentation slides), `Setup`, and every rendered tree judgement editor — enumerated by `DerivationExerciseMode.Model.get_problem_editors`.
   - **Exercise / Theorem**: `Prelude`, `Lemmas`, `Theorem` (all rendered, all jumpable).

   Read-only cells are still navigable (they accept `Move` via `CodeSelectable`), so listing and jumping to them works. The sidebar renders one labeled, collapsible section per editor when there are multiple groups.

5. Fold projectors now have a jump target

   Errors located inside a folded expression had no jump target before — the inner ids aren't present in `measured`, and the predicate (`root_tile` / `Measured.find_by_id`) returned `None`, so the jump silently dropped.

   `problem_group` now exposes a `pos` function that walks ancestors to the nearest measured id when the original id has no measured entry. Since a projector itself *is* in `measured` (occupying the folded line), the walk lands on the projector — meaning jumps inside a fold now scroll/select the folded expression rather than failing. Sidebar `L#` labels and sort order use the same resolution, so problems inside a fold cluster on the projector's line instead of falling back to `(0, 0)`.

6. Drv error rows render their messages

   `ProblemSidebar.problem_status_view` previously rendered `InfoDrv` (and `InfoMod` / `InfoSig` / `InfoMPat`) as an empty `<div>`, so Drv-sort errors like "Unexpected term for sort DrvProp" surfaced as blank rows. Wired `InfoDrv` to `DrvCursorInspector.drv_view` (the same renderer the cursor inspector uses) and added a class-name fallback for the others.

7. Derivation tree judgements collapse into one labeled section

   Every tree judgement editor is enumerated under the shared label `"Derivation"`. The sidebar clusters consecutive `problem_group`s with the same label into a single section: shared header, summed count, per-category subsections aggregated across all constituent groups in Grouped mode. Per-row line numbers are suppressed in merged sections (L# would otherwise refer to a different editor's geometry). Tree walk is postorder so within-tree order matches the visual top-to-bottom layout.

8. Switching/toggling the sidebar no longer steals editor focus

   Clicking a sidebar tab (switch section) or the collapse/expand toggle moved DOM focus off the editor, hiding the caret (gated on `:focus`). `switch_to` and `switch_assistant` now add `Effect.Prevent_default` to the mousedown so focus stays on the editor. Selecting text or clicking inputs in a panel still works and still moves focus (the panel's `tabindex` is retained).

Architecture
------------
`ProblemCollection` (in `haz3lcore`) now owns:

- `editor_input` — labeled `CachedStatics + CachedSyntax`.
- `problem_group` — problems attributed to one editor, pre-sorted per category, with counts and the `measured`/`row_to_line` needed to render `L#` labels and resolve jump positions.
- `problem_collection` — list of groups plus aggregated counts.
- `ProblemCollection.make` — builds the collection, de-duplicating shared `(id, category)` pairs in caller-provided order (first-wins).

`Sidebar.re` is now thin plumbing: build `editor_input`s and call `make`. `ProblemSidebar.view` renders zero/one/many groups appropriately, merging consecutive same-label groups into one section.

This replaces the old hand-rolled dedup (excluding `test_validation`) with a principled first-wins ordering: `test_validation` is now listed *before* `user_tests` so shared hole/syntax ids land in the "Test Validation" group. To keep jump-to-tile consistent, `CodeExercise.editor_positions` was reordered so `YourTestsValidation` precedes `YourTestsTesting`. `idx_of_pos` / `pos_of_idx` are unchanged, so persistence is unaffected.

Static-error scoping: `make_problem_context` now filters `error_ids`/`warning_ids` so each editor surfaces only problems for ids in its own segment. Previously `user_tests`'s static errors leaked into "Your Tests" for ids whose tokens lived in `your_impl`.

Per-editor collapse state: collapse keys are now `(editor_label, category)` for category-collapse and `editor_label` for editor-group collapse. Existing persisted `collapsed` settings will fall back to default (everything expanded).

Visibility is a single source of truth: `CodeExercise.shown_in(pos, ~instructor_mode)` decides which code-exercise cells are rendered, and the view, `get_problem_editors`, and `jump_to_tile` all consult it. The view's `vis_marked` (`Always`/`InstructorOnly`) markers — which duplicated this fact — were removed; each editor cell is gated directly on `shown_in` (a thunk keeps instructor-only cells from being built for students). The misnamed `visible_in` (it gates *editing*) was renamed `is_editable` in `CodeExercise` and `Tutorial`.

Deferred / not fixed
--------------------
  - `NextProblem` navigation buttons still dispatch via `ActiveEditor(Move(Goal(NextProblem dir)))`, so they only walk the currently-active cell's problems, not the full aggregated sidebar list. After a sidebar jump the cursor lands in the target cell and NextProblem walks that cell coherently. A fully cross-cell walk would need a new action variant or per-cell cycling in the sidebar itself.
  - ~~DOM focus is not transferred on sidebar jumps (see (3)).~~ Fixed in (3).
  - Some folded expressions surface duplicate rows in the problem sidebar — when an error id resolves to a projector that already had its own error, both versions appear.
  - ~~`DerivationExerciseMode` / `TheoremExerciseMode` `jump_to_tile` still use `root_tile`; same hole-click bug applies.~~ Fixed in (2).
  - Derivation slides can have **duplicate ids across tree judgement editors** (created by `push_premise` inlining an abbreviation without regenerating ids). Jumps to a duplicated id always resolve to the first matching editor, which is often wrong. Tracked as #2277 — a real bug to be fixed in a follow-up PR, not this one.

Notes
-----
Rebased onto dev after the Derivation Trees merge, which split `view/ExerciseMode.re` into per-kind files and reorganized scratchpads into a `kind` sum (`Code | Drv`). `Page.Update.get_problem_editors` dispatches over `Scratchpad.kind`, mirroring the existing `get_editor` helper.

Closes #2223




## #965 Haz3l binding uses / agrsh
created 2023-01-22T06:21:35Z merged None base dev
BODY (mutable, retrieved today):
Intended behavior is to highlight all uses of a bound variable when the cursor is over a pattern. At the moment, there is code which prints the uses, but the UI portion hasn't been done yet.

comments / agrsh / 2023-02-06T05:07:32Z
Largely finished. Also incorporates some bug fixes to the co-ctx. At the moment, all uses of any binding in a pattern are highlighted orange -- it may be better to have different bindings highlighted different colors. The code itself can be polished a little (in particular, there are still some print statements littered around). 

comments / cyrus- / 2026-04-21T12:54:47Z
this now exists through a different effort, but thanks for your work on this @agrsh 

reviews / disconcision / 2023-03-15T23:47:53Z
Looking pretty good... some small fixes. I think we might want to iterate a bit on the style though... the orange doesn't do a great job of visually associating the use sites with the pattern selection. I think we should maybe use the same color as for the pattern term indicator, but further differentiate the use decoration by maybe making it an outline instead of a solid box, or something like that. maybe a different stroke style. not sure how that will look but worth trying, or maybe some other variation I think. 

review-comments / disconcision / 2023-03-15T23:26:45Z
it does yes; search the codebase. you'll need to import OptUtil.Syntax

review-comments / disconcision / 2023-03-15T23:27:02Z
ListUtil.flat_map

review-comments / disconcision / 2023-03-15T23:27:16Z
print cleanup

review-comments / disconcision / 2023-03-15T23:31:00Z
technically this can be obtained by just extracting the variables names from the pattern's context. but this is going to change a bit with ADTs, so it's fine to just leave it for now. maybe add a "TODO(andrew)" comment on it for me to remind me to update it to the new co-ctx system once its fully in place.

review-comments / disconcision / 2023-03-15T23:31:49Z
cleanup (multiple prints)

review-comments / disconcision / 2023-03-15T23:32:41Z
just destructure this immediately ie `((var, ids): usage_info) => {...`

review-comments / disconcision / 2023-03-15T23:38:50Z
these are the uses, correct? if so, i think they should just be called that, body_ids is vague. also why does it contain Id.invalid by default instead of being empty?

review-comments / disconcision / 2023-03-15T23:39:02Z
cleanup

review-comments / disconcision / 2023-03-15T23:41:58Z
consider `body_ids @ (is_rec ? def_ids : [])`

review-comments / disconcision / 2023-03-15T23:44:52Z
i feel like this approach with is_rec is a little indirect. not sure if it's the best way, but you could just do a comparison ctx == def_ctx and avoid having to alter extend_let_def 

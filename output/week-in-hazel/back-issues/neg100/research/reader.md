
## #1325 Add and Delete Mutants  / russell-rozenbaum
created 2024-07-10T14:19:21Z merged None base dev
BODY (mutable, retrieved today):


comments / russell-rozenbaum / 2024-09-27T18:03:21Z
Closing as this branch is identical to title-editor


## #1378 Mark warnings as errors in release and warnings in dev / 7h3kk1d
created 2024-08-20T21:06:27Z merged 2024-10-02T18:26:34Z base dev
BODY (mutable, retrieved today):
I just set it in all the dune files for now. I'm waiting on a response to https://discuss.ocaml.org/t/default-flags-for-the-project/3217/3 to see if there's a way to configure it in dune-project/dune-workspace or if we should have a top level dune file.

comments / 7h3kk1d / 2024-08-20T21:13:13Z
Release failing due to https://github.com/hazelgrove/hazel/issues/1104

comments / 7h3kk1d / 2024-08-21T00:48:51Z
I got a response to use dune-workspace https://discuss.ocaml.org/t/default-flags-for-the-project/3217/3

Doing that now.


## #1399 Missing labeled tuple labels elboration / 7h3kk1d
created 2024-09-23T14:20:42Z merged 2024-09-27T17:29:05Z base labeled-tuple-rewrite
BODY (mutable, retrieved today):
Adds missing labels to labeled tuples during elaboration. Also reorders labels

![Screenshot from 2024-09-23 10-19-44](https://github.com/user-attachments/assets/36fc80c6-4e4a-40a4-ae0d-07f757b90d00)


There's some additional cleanup necessary when we merge with the labeled-tuple-rewrite branch. Mainly that there's now two rearrange functions

comments / 7h3kk1d / 2024-09-23T15:58:38Z
Evaluator is kind of working but there's some bug when you do nested projections.

reviews / WondAli / 2024-09-27T17:01:45Z
lgtm, will de-duplicate the rearranges post-merge

review-comments / 7h3kk1d / 2024-09-23T14:23:57Z
I needed these tests to make sure the function is working as expected. We don't need it for this PR but it's worth adding some property tests:

- Unlabeled values don't rearrange
- Fully labeled tuple types arbitrarily rearrange fully labeled values
- There's probably some properties around duplicates, and mismatched lengths but I haven't thought them through yet.


review-comments / 7h3kk1d / 2024-09-23T14:24:24Z
rearrange and rearrange2 should be deduplicated somehow.


## #1400 Switch to Bonsai / Negabinary
created 2024-09-27T19:11:17Z merged 2024-10-02T18:25:38Z base dev
BODY (mutable, retrieved today):
Switches from Incr_Dom to Bonsai

review-comments / 7h3kk1d / 2024-09-27T19:18:39Z
I'm curious what's happening here. I don't think you did anything to change it.

review-comments / 7h3kk1d / 2024-09-27T19:19:43Z
I can't tell which of these dependencies have changed because you had them installed in your opam switch and which ones are necessary. I'll probably pull this down and try starting with a clean switch just to test.

review-comments / 7h3kk1d / 2024-09-27T19:25:24Z
Should we just remove state from `Update.apply`?

review-comments / Negabinary / 2024-09-27T19:27:15Z
yeah why not

review-comments / 7h3kk1d / 2024-09-30T14:24:11Z
Has to do with minor opam version differences.


## #1401 Add some additional tests to be useful for the labeled tuples branch / 7h3kk1d
created 2024-09-30T19:33:21Z merged 2024-10-01T18:19:22Z base dev
BODY (mutable, retrieved today):
- Test_Statics for determining the type of the given expression
- Test_Elaboration adds a unapplied function

review-comments / 7h3kk1d / 2024-09-30T19:33:43Z
I'm open to better ideas on how to enable this. Without it it makes test output difficult to read.

review-comments / 7h3kk1d / 2024-09-30T20:56:24Z
An alternative encoding than interleaving fresh if we want:

```reason
    test_case("bifunction", `Quick, () =>
      alco_check(
        "x : Int, y: Int => x + y",
        Some(arrow(prod([int, int]), int)),
        type_of(
          e(Fun(
            p(
              Tuple([
                p(Cast(p(Var("x")), int, unknown(Internal))),
                p(Cast(p(Var("y")), int, unknown(Internal))),
              ]),
            ),
            e(BinOp(Int(Plus), e(Var("x")), e(Var("y")))),
            None,
            None,
          )),
        ),
      )
    ),
    ```


## #1402 Fix deferrals / 7h3kk1d
created 2024-10-01T17:26:10Z merged 2024-10-29T18:57:12Z base dev
BODY (mutable, retrieved today):
Before
![Screenshot from 2024-10-03 09-52-57](https://github.com/user-attachments/assets/533934df-6562-4bfa-934f-3e46a1da14ca)
After
![Screenshot from 2024-10-03 09-53-12](https://github.com/user-attachments/assets/c3bb2adf-7147-4a17-8e21-a9e47b0b87b0)


review-comments / 7h3kk1d / 2024-10-01T17:27:10Z
This seems right to me. I don't think we always want the remaining function to be from a product.

review-comments / 7h3kk1d / 2024-10-01T17:27:38Z
I still don't have a strong sense as to why this needs to be req_final but it remains indet otherwise.

review-comments / 7h3kk1d / 2024-10-01T17:27:52Z
This comment seems to be out of date.

review-comments / 7h3kk1d / 2024-10-01T17:28:28Z
I don't know if there's a better way to be handling this unboxing for the singleton case than wrapping it in a tuple.

review-comments / 7h3kk1d / 2024-10-01T17:30:23Z
The code still works without this in my test though. So TODO

review-comments / cyrus- / 2024-10-01T18:26:06Z
@Negabinary not sure I understand what req_value was doing here since we still need to handle casts? are casts considered values?

In any case, deferredap should be treated as if it were a lambda, so it should be a value.

Let's chat briefly about this with @7h3kk1d at the beginning of our meeting tomorrow.

review-comments / 7h3kk1d / 2024-10-01T19:50:42Z
This one seems to be necessary

review-comments / Negabinary / 2024-10-01T20:38:13Z
@cyrus-  Oh I see, yeah I guess if you still want to do the function cast rules when the function is indet then you do need that to be req_final

review-comments / 7h3kk1d / 2024-10-03T14:19:05Z
I got all of the cases I can think of working. I'm struggling to find a case that req_final catches that req_value doesn't though. There might be something wrong with `Constructor`


## #1404 Remove unnecessary print statement / 7h3kk1d
created 2024-10-02T18:45:33Z merged 2024-10-02T23:36:14Z base dev
BODY (mutable, retrieved today):
closes #1403 

We can make a separate PR for https://github.com/hazelgrove/hazel/issues/1403#issuecomment-2389408249. I'm guessing we can just have github comment on every print statement in a diff?


## #1405 Readd warnings failing build in dev but exclude some unused warnings / 7h3kk1d
created 2024-10-03T15:03:35Z merged 2024-10-04T14:37:05Z base dev
BODY (mutable, retrieved today):
Disabled Warnings:
    26: Unused variable
    27: Unused Variable Strict
    32: Unused value declaration
    33: Unused open statement
    34: Unused type declaration
    35: Unused for-loop index
    38: Unused extension
    39: Unused rec flag
    58: Missing cmx file This was already in use

Rationale:
I had previously disabled warnings in dev in https://github.com/hazelgrove/hazel/pull/1378. The idea being that you shouldn't restrict the ability to build given warnings, just the ability to deploy. Unfortunately dune only announces warnings the first time a module is built so you could have long lived local issues for serious warnings, i.e. missing cases in pattern-matching.
 
Unused warnings are allowed because they show up regularly as part of writing code and are easy to fix after a build failure in CI by just removing the unused code.

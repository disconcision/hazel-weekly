
## #1099 Better Indent / disconcision
created 2023-08-31T00:34:21Z merged None base dev
BODY (mutable, retrieved today):
- Closes #882 
- Closes #887 
- Closes #1087

In addition to fixing the preceding complete-case indentation bugs, this introduces a new system for indentation in the incomplete case, whereby indentations are based on the same best-effort syntax completion scheme used in TyDi to provide better semantic information to the assistant.

The result is the while adding new code to a new line above existing complete code, writing left-to-right, any partially-entered forms should get correct indentation (as in this case the completion scheme will always succeed), whereas all pre-existing syntax (below the newline following the new code) should retain its previous indentation.

Things get more interesting however when you move around with an unbalanced backpack; in such situations indentation may shift as you move the caret vertically, as the best-effort put-down make succeed in dropping the backpack contents, which may create or remove an indentation context.

comments / disconcision / 2023-12-18T00:29:32Z
@cyrus I've brought this up to date with dev. As we talked about, I have some misgivings about merging this in, due to (a) likely minor but complex-to-reason-about performance hit, (b) debatably confusing behavior when indentation changes with caret movement. As a result, I am ambivalent about whether this should be merged or not, though I do intend to maintain it for now as a reference point.

comments / cyrus- / 2024-02-29T05:25:12Z
Closing in anticipation of new tylr implementation, will have to revisit this topic.

comments / disconcision / 2025-07-06T23:38:30Z
Closed in favor of #1761

reviews / cyrus- / 2023-12-05T01:56:02Z
@disconcision this looks good to me, just needs a merge in `Code.re` 


## #1468 Final tutorial sys / reevafaisal
created 2025-01-20T13:13:18Z merged None base dev
BODY (mutable, retrieved today):


comments / facundoy / 2025-01-25T21:56:55Z
Known bug: evaluation of the YourImplementation editor is incorrect. 
I think that there may some issues with the stitching but not 100% sure. 
Tutorial edits not being saved + unable to highlight multiple lines on editor

NOTES:
- Need to specify tutorial module names when stitching in order to set wrapper to true or false since we will only need the wrapper for specific exercises

comments / reevafaisal / 2025-03-17T03:45:36Z
So in my last commit when I said local, I meant global.

BUG: 
Also I noticed there is a bug in the boolean exercise. Appears that whenever you type, based on the movements of the cursor the table appears to dissapear and reappear. Since we just added the new exercises in, we need to make sure it works with the widget. 

comments / reevafaisal / 2025-04-10T19:08:12Z
Based on the print statements, it seems like there is a constant recursion over label in the normalize function. Im not sure where exactly the bug lies but it seems like it is not able to detect that the expression is incomplete.

comments / cyrus- / 2025-04-21T22:14:12Z
- [x]  previous button on all slides
- [x]  get rid of checkmark animation, make it smaller and think about styling of the three buttons at the bottom (same size maybe?)
- [x]  fix crash on clicking previous button or next button when that goes out of bounds
- [x]  newlines in slide text
- [x]  make the hint an option rather than required
- [x]  hover message over the info button


comments / cyrus- / 2025-04-21T22:14:38Z
**Instructions for creating new tutorials**

1. Create an exercise of type Tutorial.spec inside haz3l/app/explainthis/exercises/examples
2. Ensure to set the wrapper to either true or false based on the construction of your hidden_tests. If you require the user to define the variable, you may set it as false otherwise set it as true.
3. If you would like to add in a hint cell, type your hint into the display_hint variable, otherwise leave it as an empty string and the hint cell will not be displayed.
4. eds.version is the integer version of eds.id. It is used as an index (starting at 1) solely for the next/prev button functionality. Make sure to correctly assign eds.version and edit the total number of test cases in the block that generates the next button in TutorialMode.re. 

comments / reevafaisal / 2025-05-07T13:19:25Z
- removed the cross icon entirely due to dissapearing/reappearing issue as a user types their implementation.
- checkmark functionality is fixed
- prev button only allows user to view exercises that user has previously completed


comments / reevafaisal / 2025-05-12T22:37:30Z
- [x] fix breakage on first arrow / remove
- [x] remove looping on last arrow and add a "done"
- [x] fix arrow css
- [x] slight issue with stitching

reviews / cyrus- / 2025-06-09T21:54:23Z
in addition to the code comments:
- with this PR, let's make Tutorial Mode the default mode that opens up when someone loads Hazel (rather than the Documentation slide)
- let's make Tutorials mode (and Exercises mode, while you're at it) open up in Student mode by default rather than Instructor mode
- the tutorial arrows appear above everything else, e.g. the hazelnut menu. they should be at the same layer as the other stuff in the tutorial. 


review-comments / cyrus- / 2025-06-09T21:38:44Z
debug print left here

review-comments / cyrus- / 2025-06-09T21:39:23Z
rename `specs` to `exercise_specs` so it is more clear

review-comments / cyrus- / 2025-06-09T21:40:06Z
let's rename `all_f22` to `all_public` or something like that, since it isn't about F22 semester anymore :)

review-comments / cyrus- / 2025-06-09T21:41:07Z
prefix with "TUTORIAL" so it is clear when debugging what this entry is, not just a random ID

review-comments / cyrus- / 2025-06-09T21:42:44Z
call it `m'` rather than `exercises`

review-comments / cyrus- / 2025-06-09T21:43:43Z
why did you need to modify `ExplainThis`?

review-comments / cyrus- / 2025-06-09T21:44:34Z
let's move all the tutorial related files over to `haz3lweb/tutorials` rather than putting them under `exercises`, so we aren't confusing exercises mode and tutorials mode

review-comments / cyrus- / 2025-06-09T21:47:28Z
this file name has a typo -- should be `Tutorial` not `Tutoial`

review-comments / cyrus- / 2025-06-09T21:48:29Z
it doesn't look like the build process has been updated to copy in this file when building in student mode, like we do with the Exercises mode equivalent

review-comments / cyrus- / 2025-06-09T21:49:55Z
let's include a .md file in docs with instructions on how to create and update tutorials, like we have for exercises

review-comments / cyrus- / 2025-06-09T21:51:06Z
let's call Tutorial pages "lessons" to distinguish them from Exercise mode's "exercises"

review-comments / cyrus- / 2025-06-09T21:52:57Z
you can delete these

review-comments / cyrus- / 2025-06-09T21:53:06Z
you can delete the commented out things

review-comments / cyrus- / 2025-06-09T21:53:15Z
delete

review-comments / cyrus- / 2025-06-09T21:53:55Z
delete commented out things


## #1575 LLM Hole fillings and Assistant Sidebar / russell-rozenbaum
created 2025-03-22T21:30:08Z merged 2025-07-09T22:50:04Z base dev
BODY (mutable, retrieved today):
_**To-Do**_

**Before Initial Merge**
- [x] fix or move structured edit actions in Perform that aren't working
- [x] remove system prompt spam
- [x] make sure hinted test feature works (or move to another branch)
- [x] make sure nothing outside of the assistant code is commented out or instrumented with prints
- [x] go through Andrew's comments and see if there are any other items in this category
- [x] make each `??` invocation open up a new chat automatically
- [x] fix issues with resizing the sidebar
- [x] clean up Perform.re and Indicated.re and anything else impacted by structure edit actions (mainly navigation actions)

🔴 **Most Important** 🔴
- [x] **Make it possible for LLM to respond with a chain of tool calls**, which will in turn make the task completions much more cost-effective.
- [x] **Allow LLM to navigate to and edit function bodies if need-be**. This is most critical at the end of a program sketch, where the tail of the program sketch is inherently the body of a _let_, thus we should allow for the LLM to somehow navigate here. How is the main question... we could allow it to _only_ access the body of the final let statement, or we could allow it to freely choose to perhaps "goto_body" of any let statement. 
- [x] **BUG: User needs to manually click into editor before LLM responds with a tool call, otherwise there will be no cursor placed and nothing will happen**
- Update on the above: It seems like this was fixed by fixing the whitespace bug (they were seemingly the same thing actually, and not a problem with the cursor)
- [x] **Server becomes very slow as chats get long**. This is likely due to the unpacking of code messages... mainly since it updates with every mouse action. 

🟡 **Less Important** 🟡
- [ ] **Implement functionality for more tool calls**. We still need to implement scrolling up/down and show_references.
- [ ] **Improve prompting**. This is quite broad, but some focusses could be to improve the automated context retrieval and showing the LLM where its cursor currently is/what it has selected/what it just updated. This is likely to be an ongoing process throughout the implementation of other features, such as tool calls or historical context. 
- [x] **Restyle/Rename chat parties**. This is mainly for increased intuition, but we would supposedly want the "user" message to be what the user actually typed in the text box, the "Assistant" to be the LLM response, the "System" to be automated prompts/contexts/etc, and an "Error" output (maybe instead of "System", as errors can stem from external API calls) to report any failures. 
- [x] **Make collected chats (for historical context) much shorter/make more cost-efficient**. This could be done by summarizing collected chats (each time they are collected) into a predefined number of words, disposing of unnecessary information/context (eg. old sketches from prior messages), and/or possibly even using an LLM or ML mechanism itself to determine whether or not a given user message actually requires historical context (eg. Feed the msg "Why did you implement it like that?" into an LLM asking "Does this require historical context: Yes or No?", expecting Yes. eg. example of a "No" response would be feeding in something like "please make this function recursive") 

**🐞 Bugs / 🕳️ Pitfalls / 🔭 Things to Look Into** 
- [ ] **Cannot properly select "test" defs and bodies.** There are likely other language server navigation errors like this. 
- [ ] **Sketch can quickly become corrupt.** When improper syntax is used, the language server fails to navigate using purely the "structure" of the code. It also seems that it might cause the LLM to be confused on how to navigate using purely the structure of the code. Take, for example, the following sketch: ```let case in fun```. This program isn't syntactically correct or semantically meaningful, so is there a way to navigate on it in a "structured" manner?
- [ ] **Comments above a definition cannot be edited/changed** as of right now. Also, comments aren't properly inserted into sketch in general. Either they aren't inserted/parsed out of a response properly, or the LLM doesn't use proper syntax when making comments.
- [x] **Refine Few-Shot Examples**. Try to cover all cases, syntax, and overall complexity of task completion in Hazel.
- [x] **Prompt Generation doesn't work when the cursor has selected whitespace in the program sketch**. Getting the cursor inspector information fails, which causes prompt generation to fail, and no message is sent.
- [ ] **Can't copy from code blocks**
- [x] **Prompt display and history menu can interfere**. This should be a simple fix, just close the other when one is opened.
- [x] **Suggestion mode UI message displays need to be updated to match new architecture.** Applies to the frontend and backend of things.
- [ ] Editor sent to update function changes when the user changes the editor. So in chains/loops of agent calls, the editor is not persisted.


comments / disconcision / 2025-06-10T23:39:23Z
I made a variety of style and formatting tweaks... let me know if you object to any. I have some other ideas, mostly for simplifying things, but I'll talk about them when we meet next. here are some of the things I changed:

1. Minor updates to ExplainThis for consistency; sidebar resizing works with explainthis now, and I got rid of the now mostly empty header in favor of a floating toggle for highlighting:

<img width="1149" alt="Screenshot 2025-06-10 at 7 27 15 PM" src="https://github.com/user-attachments/assets/c881fe77-5b34-471f-8723-df484da2f412" />

2. Consistency updates for the settings UI. A variety of changes here, mostly minor. The css/dom structure is a bit messy here; I started folding some things into reusable components but didn't go all the way. Right now things like font sizes, border radii etc are defined in many different places, so there were lots of different values. I partially consolidated these, and manually homogenized some others. I also commented out the manual model entry field; not sure we need that given the dropdown?

<img width="1149" alt="Screenshot 2025-06-10 at 7 27 31 PM" src="https://github.com/user-attachments/assets/551e1b2f-0eea-424a-9c73-327936b29958" />

Some things still to do:
1. We still need to find a way to specify recommended model(s) here.
2. Minor: I think what I've now called the New and Current API Key components could be combined into a single component that just displays whatever the current stored key is, or shows the message to enter one if there's none. This could also do some kind of validation on_change. Not sure the update button is strictly necessary either; it could just update on_change. Unless update actually validated the key with the server, but it doesn't do that right now.
3. Minor: Similar for the current model ID.

One thing I'm noticing now is that when you try to do a ?? hole filling, the Suggest panel fills up with a lot of system messages:

<img width="1149" alt="Screenshot 2025-06-10 at 7 27 48 PM" src="https://github.com/user-attachments/assets/86e979c3-9977-4ae8-90c8-d01af48671bf" />




comments / russell-rozenbaum / 2025-06-11T12:25:07Z
> the manual model entry field; not sure we need that given the dropdown?

The current list filters out models that don't support tool calls. In general, if we ever filter the list, we might want to let the user add their own model that may have been filtered out from that list.

> We still need to find a way to specify recommended model(s) here.

We could implement a simple regex filter based on our belief of what the top models are. I currently have something like this in OpenRouter.re with the `is_top_model` function, but I've excluded it from being used anywhere for now. This would require maintenance a few times a year—updating recommendations with better models and removing out-of-date ones. 

Everything sounds good. And yea, I've yet to get around to concatenating the suggestion mode system prompt, so '??' will send many detached prompts to the model.

comments / disconcision / 2025-06-16T22:30:13Z
I resolved the merge conflicts after the language PR merge and reinstated the model free text field as per russell's comment above

> And yea, I've yet to get around to concatenating the suggestion mode system prompt, so '??' will send many detached prompts to the model.
@russell-rozenbaum what does it mean exactly? how many prompts are we sending when you enter `??`? this sounds slightly worrying

comments / disconcision / 2025-06-24T23:55:21Z
I looked fairly extensively at the hint crash issue (repro instructions: enter a linebreak, press up arrow, then type `hint"`). It seems to be a fairly subtle regrouting related issue. I've pushed a workaround which hopefully doesn't break anything else; let me know if it seems okay on your end

comments / russell-rozenbaum / 2025-06-25T19:21:51Z
> I looked fairly extensively at the hint crash issue (repro instructions: enter a linebreak, press up arrow, then type `hint"`). It seems to be a fairly subtle regrouting related issue. I've pushed a workaround which hopefully doesn't break anything else; let me know if it seems okay on your end

I was messing around with this a bit more, and found a bug that could be related or separate...

Eg. (although, probably applies to any fully defined hinted test)
`hint "here" test x == 3 end;`

Attempting to delete any character from the test keyword results in the Nonconvex_segment. 

comments / disconcision / 2025-06-26T16:01:02Z
@russell-rozenbaum this might actually an existing dev issue; trying to delete the `=` in a let expression also throws a convex segment error. out of curiosity, does this error still occur when typechecking is turned off in the settings?

comments / russell-rozenbaum / 2025-06-26T16:03:53Z
> @russell-rozenbaum this might actually an existing dev issue; trying to delete the `=` in a let expression also throws a convex segment error. out of curiosity, does this error still occur when typechecking is turned off in the settings?

Right, I see—this doesn't happen when type checking is switched off

comments / russell-rozenbaum / 2025-06-26T16:56:12Z
I notice that when turning off types, the bottom bar, along with its associated child components (context and projectors) disappears; Is this expected behavior? 

Other than this, all of the requests have been addressed, and the PR should be ready for a final review now. 

comments / disconcision / 2025-06-26T17:40:12Z
@russell-rozenbaum: yes, that's expected, the bottom bar depends on types. i guess the projector panel could stick around in principle though... the deletion crash issue should be fixed, or at least mitigated

comments / disconcision / 2025-06-29T06:44:15Z
A few functional things:

Breaks existing functionality:
1. The editor startup time has regressed by 3-5x (try loading https://hazel.org/build/task-completion-assistant/ vs https://hazel.org/build/dev/). Not sure why but one hint I can find is in the console. The line "Warning - LivelitProj.get: Not an InfoExp term" repeats 6x in this branch on startup as opposed to 2x on dev, indicating to me that documentation editor loading is happening 3 times.   

Major feature functionality:
1. Whenever I get a completion (tried several models), it seems to insert a ton of whitespace after; see here both in the editor (knocking the code off the screen) and in the console:
<img width="1684" alt="Screenshot 2025-06-29 at 1 32 48 AM" src="https://github.com/user-attachments/assets/aa51b217-4fb6-4b7c-a1b4-9fc5950b0357" />

2. Submitting any completion request results in dozens of these in the console:
<img width="1684" alt="Screenshot 2025-06-29 at 1 33 05 AM" src="https://github.com/user-attachments/assets/ae5adc4a-dcf1-41ca-8091-5a264396c07e" />

3. There's leading space getting consistently inserted before completions... either figure out if that's coming from somewhere internal, or probably actually just trim leading whitespace before inserting completions...

4. Completions seems to be displacing error holes somehow? Like note below the the three line completion seems to be displacing following error holes by three lines... mysterious.
<img width="846" alt="Screenshot 2025-06-29 at 3 03 45 AM" src="https://github.com/user-attachments/assets/053e1ea6-2c7f-47e5-8e9a-ea3d11a8cdf9" />

(also, above is an example of trailing whitespace insertion... curious if this is coming from somewhere internal... if so, trim. if it's coming from the model, it might be because we have a bunch of whitespace in a prompt or something, since it seems so consistent)


Minor feature functionality (don't have to fix this time but should create issues for if merged):
1. Picking any Anthropic model triggers some kind of API error about tool support or something. Not a huge deal but we should fix at some point ( I miss Claude)
2. Entering the second `?` in `??` cause a half-second lag in editor responsiveness... curious why this is. Should dispatch message async. Not a huge deal but we should figure out where this perf hit is coming from.
3. Weren't we using code editors to display code in the sidebar as opposed to just text? I might be misremembering:
<img width="595" alt="Screenshot 2025-06-29 at 1 37 04 AM" src="https://github.com/user-attachments/assets/a9f671ac-0fd7-42f4-b087-c9bb67e8cd2d" />

4. `??` typed in Exercises mode still gets same decoration even though it's (intentionally?) non functional? Perhaps should have some kind of easter egg... 

comments / russell-rozenbaum / 2025-06-29T13:22:52Z
> 2\. Entering the second `?` in `??` cause a half-second lag in editor responsiveness... curious why this is. Should dispatch message async. Not a huge deal but we should figure out where this perf hit is coming from.

This comes from creating a new chat. You can see this performance bottleneck when creating a new chat in any of the three modes. 

In particular, following the execution path, when a new chat is made we call _init\_chat_  which calls _mk\_message\_display_ which calls _parse\_blocks_, and it's here in parse\_blocks where performance takes a hit. It is using regexp to parse out each code block. This doesn't occur in normal back and forth chatting, but due to the quantity of example code snippets in our prompts, this does occur for initial prompt parsing. 

A simple fix would probably be storing a serialized version of these parsed initial messages somehow. Although let me know if there are other ideas.

comments / russell-rozenbaum / 2025-06-29T13:27:16Z
> 3\. Weren't we using code editors to display code in the sidebar as opposed to just text? I might be misremembering:

Looks like we might not be properly prompting the agent for '??' completions. The "content" field in the json payload shows the agent isn't wrapping their response in triple backticks.

comments / russell-rozenbaum / 2025-06-29T13:44:12Z
> 1. Whenever I get a completion (tried several models), it seems to insert a ton of whitespace after; see here both in the editor (knocking the code off the screen) and in the console

Yea, we talked about this at one of the meetings, and we're not sure as to what's going on here. I think our best guess was that the opaque suggestion is provided by the backpack doesn't format properly, though I'm still understanding the framework for editors, zippers, terms, tiles, etc, so I'm not entirely sure what's happening here. 

comments / russell-rozenbaum / 2025-06-29T14:59:25Z
Todos
- [ ] Allow for copying from code blocks
- [ ] Implement streaming and/or reintroduce loading dots. O.w. user does not know if LLM is responding.
- [x] Move suggestion prompt creation from ChatLSP to AssistantModel (into init_prompt_data)
- [ ] (Optional) Allow for copying from API key field

comments / disconcision / 2025-06-29T19:16:28Z
> Yea, we talked about this at one of the meetings, and we're not sure as to what's going on here. I think our best guess was that the opaque suggestion is provided by the backpack doesn't format properly, though I'm still understanding the framework for editors, zippers, terms, tiles, etc, so I'm not entirely sure what's happening here.

is the whitespace in the received completion from the API, or is it something the editor is doing? in any case, let's just trim leading and trailing whitespace from completions.

comments / disconcision / 2025-06-29T19:31:00Z
> A simple fix would probably be storing a serialized version of these parsed initial messages somehow. Although let me know if there are other ideas.

not sure about best approach, would need to hear a bit more about the internals which i haven't read that closely. in principle i feel it's not optimal to have code completion speed depend on stuff going on in the chat, as for regular completions the chat will often be closed. so if there's a way to take chat UI stuff off the critical path for completions that's probably the way to go, but pre-serialization also sounds reasonable i think? should be at compile time though

comments / russell-rozenbaum / 2025-06-29T19:37:24Z
> > Yea, we talked about this at one of the meetings, and we're not sure as to what's going on here. I think our best guess was that the opaque suggestion is provided by the backpack doesn't format properly, though I'm still understanding the framework for editors, zippers, terms, tiles, etc, so I'm not entirely sure what's happening here.
> 
> is the whitespace in the received completion from the API, or is it something the editor is doing? in any case, let's just trim leading and trailing whitespace from completions.

It comes from the editor. The LLM will insert appropriate line breaks and spaces for nice formatting. You can see that everything is formatted well when accepting those chaotic suggestions.

comments / disconcision / 2025-06-29T19:48:09Z
I confirmed that the slow startup time is coming from the same parse_blocks cause.

dev startup graph:

<img width="728" alt="Screenshot 2025-06-29 at 3 43 33 PM" src="https://github.com/user-attachments/assets/768ff232-f694-4885-94e3-65ce05f01116" />

this branch startup graph:

<img width="940" alt="Screenshot 2025-06-29 at 3 43 50 PM" src="https://github.com/user-attachments/assets/6888472b-54fb-4b9a-a760-ff4c52f1cdf2" />

I think that regardless of whether we pre-serialize we ideally want to find a way to make sure these kinds of calls don't happen if the chat isn't open to avoid the possibility of these kinds of regressions


comments / russell-rozenbaum / 2025-06-29T19:54:47Z
> I confirmed that the slow startup time is coming from the same parse_blocks cause.
> 
> dev startup graph:
> 
> <img alt="Screenshot 2025-06-29 at 3 43 33 PM" width="728" src="https://private-user-images.githubusercontent.com/22436459/460349593-768ff232-f694-4885-94e3-65ce05f01116.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTEyMjcwODEsIm5iZiI6MTc1MTIyNjc4MSwicGF0aCI6Ii8yMjQzNjQ1OS80NjAzNDk1OTMtNzY4ZmYyMzItZjY5NC00ODg1LTk0ZTMtNjVjZTA1ZjAxMTE2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA2MjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNjI5VDE5NTMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWZjMGM2Y2FmODI3ZmExMWJhZDQxZjRmMGVhYWZiMGJlMTY2MjQyNzg5OTQ4ODE4MTJkY2Q2MTUzNzM1MmZjOTgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FJ3Y0C6W1EXQ6qOoUWfubl8Mv6r_-053oXUrAlRNHRQ">
> this branch startup graph:
> 
> <img alt="Screenshot 2025-06-29 at 3 43 50 PM" width="940" src="https://private-user-images.githubusercontent.com/22436459/460349600-6888472b-54fb-4b9a-a760-ff4c52f1cdf2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTEyMjcwODEsIm5iZiI6MTc1MTIyNjc4MSwicGF0aCI6Ii8yMjQzNjQ1OS80NjAzNDk2MDAtNjg4ODQ3MmItNTRmYi00YjlhLWE3NjAtZmY0YzUyZjFjZGYyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA2MjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNjI5VDE5NTMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFjNDQzMWFjNWEyNTI3Y2E5MmE2NjAxN2I4ZTc4ODMwMzczMmFmYTg1ZDJhYjZlMTMxYmE1OTM2N2UyMzMyMTAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.DiX6jrNoFWL12qhxLb_m2jzoHOYzgNXFTNnkUkOA2ns">
> I think that regardless of whether we pre-serialize we ideally want to find a way to make sure these kinds of calls don't happen if the chat isn't open to avoid the possibility of these kinds of regressions

Is this suggesting we don't want to store them on initialization of the model as is done here https://github.com/hazelgrove/hazel/pull/1575/commits/6826547b7ae769c4fd2dff8ef9b6f0cbc5becb29 ?

We will inevitably need to parse blocks at least once at some point, currently we do it on initial startup, before we did it each time a new chat was created. We could do it instead on the first use case of a user typing '??'/'?a' or opening tutor mode/composition mode. But this again comes with the consequence of being slow when the user actually wants to use it.

We could also look into improving the runtime of parse blocks itself, I'd need to look into the current regexp to see how feasible this is.

comments / disconcision / 2025-06-29T20:07:40Z
Doing it when the chat sidebar is opened for the first time rather than editor startup is my first-order suggestion. In general the idea here is that things the user might not use at all shouldn't slow down initial load if possible. Additionally, is this process on the critical path for generating completions as opposed to using the chat sidebar? it's not obvious to me that getting completions should require this parsing step.

> We could also look into improving the runtime of parse blocks itself, I'd need to look into the current regexp to see how feasible this is.

I see you're using Str.Regexp; use the js regexp instead, see StringUtil, it can be an order of magnitude faster

comments / russell-rozenbaum / 2025-06-29T20:15:34Z
> Additionally, is this process on the critical path for generating completions as opposed to using the chat sidebar? it's not obvious to me that getting completions should require this parsing step.

Right, this step is only for the display present in the sidebar. We send a raw string message to the model. However, for the sake of guaranteeing consistency between what is sent to the model and what is displayed to the user, the creation of the string messages to be sent and the creation of the viewable UI message displays are always done jointly. I think moving this process off the critical path loses this guarantee.

comments / disconcision / 2025-06-29T20:30:14Z
I looked into the extra whitespace issue and I think what is happening is that the layout system assumes the buffer has no linebreaks, so the caret is placed where it would be if that is true. the same issue is probably causing the error holes to be displaced. i though this wasn't an issue before though so i'm wondering what might have changed?

> Right, this step is only for the display present in the sidebar. We send a raw string message to the model. However, for the sake of guaranteeing consistency between what is sent to the model and what is displayed to the user, the creation of the string messages to be sent and the creation of the viewable UI message displays are always done jointly. I think moving this process off the critical path loses this guarantee.

don't know enough about the current implementation to know what to advise but i think the bottom line here is that processes which are only relevant to the chat bar view shouldn't slow things down when the chat bar isn't being used. if the current architecture makes that difficult i think we need to revisit it


comments / russell-rozenbaum / 2025-06-29T21:24:01Z
> don't know enough about the current implementation to know what to advise, but I think the bottom line here is that processes which are only relevant to the chat bar view shouldn't slow things down when the chat bar isn't being used. if the current architecture makes that difficult i think we need to revisit it

I've imagined generating completions non-separable from using the sidebar. 

There are two versions of a message: 
1. The openrouter one, which gets sent to the model (this is absolutely necessary for completions) 
2. The displayed version, which is what parse blocks parse code blocks out of

When a user presses enter or the send message button -> the string is created into **both** versions of a message -> the OpenRouter message is sent to the LLM _and_ the display version is concatenated to a list of other display messages to be displayed in the chat interface.


We can set flags up for when the user initially opens the assistant sidebar. They will need to open it before requesting completions, as they'll need to set an API key. Also, hopefully that suggestion of using js regexp and StringUtil rather than Str regexp will help, though I'll need to study how js regexp works and how I can copy the implementation over.
Other than this, we could probably have the displays only be parsed when a chat is opened, but this would be a more involved refactoring. 

comments / disconcision / 2025-06-29T21:51:55Z
@russell-rozenbaum @CyrusD123 
I've pushed a modified version of the completion buffer which solves the decoration issues above, and some other buffer aesthetic issues, like wonky formatting and the trailing hole. This new completion style works more akin to a regular selection; it doesn't contain unparsed text inside, but a fully parsed hazel code segment.

It looks like this now:

<img width="535" alt="Screenshot 2025-06-29 at 5 46 55 PM" src="https://github.com/user-attachments/assets/164dde16-1470-424d-986d-8422df314570" />

(Not married to the style; both the tokens contained within the buffer and the buffer backing can be styled; here, I'm using a modified version of the selection deco for the backing, and a 50% opacity filter for the tokens)

This is a pretty different approach to the buffer though so I'd appreciate it if you guys could play with it and see if you find any bugs or other undesirable behaviors. One way in which this might be different is that insertion will fail silently if the completion is too badly borked (see set_llm_buffer; it first tries to parse the completion individually, and then it checks if the resulting backpack is empty (so no missing delimiters); if either of these fails, it fails silently. You guys might be doing similar checks upstream already, I'm not sure.

comments / russell-rozenbaum / 2025-06-30T15:23:56Z
> This is a pretty different approach to the buffer though so I'd appreciate it if you guys could play with it and see if you find any bugs or other undesirable behaviors.

I notice we can't undo to get back suggestions anymore, where previously we could. Not sure how important this is, though. 



comments / russell-rozenbaum / 2025-06-30T15:30:26Z
> Doing it when the chat sidebar is opened for the first time rather than editor startup is my first-order suggestion.

https://github.com/hazelgrove/hazel/pull/1575/commits/03ad9522f3fa4e0bcd7da42da53fba5bc0f7e775 should offer somewhat of a fix for this. 

comments / disconcision / 2025-07-02T00:44:36Z
@russell-rozenbaum I'm still getting that slowdown after entering the second ?. in the below flame graph, the initial small spike is the first ?, and the second is the second ?, which takes over a second. as can be seen below, almost this entire time is spent in parse_blocks. not an absolute dealbreaker for merging but we should definitely prioritize fixing this

<img width="921" alt="Screenshot 2025-07-01 at 8 41 36 PM" src="https://github.com/user-attachments/assets/2d68e6d1-d747-46c0-9a39-7f1a1ac55d6e" />


comments / russell-rozenbaum / 2025-07-02T01:28:49Z
> @russell-rozenbaum I'm still getting that slowdown after entering the second ?. in the below flame graph, the initial small spike is the first ?, and the second is the second ?, which takes over a second. as can be seen below, almost this entire time is spent in parse_blocks. not an absolute dealbreaker for merging but we should definitely prioritize fixing this
> 
> 
> 
> <img width="921" alt="Screenshot 2025-07-01 at 8 41 36 PM" src="https://github.com/user-attachments/assets/2d68e6d1-d747-46c0-9a39-7f1a1ac55d6e" />
> 
> 

Interesting. Have you hard reset Hazel? Does that have any information as to what function call might causing that?

comments / disconcision / 2025-07-02T01:35:41Z
I have hard reset, yes. So there's no latency when pressing the second ? on your machine?

Unrelatedly: I'm a bit confused about the console output during a completion:

<img width="1682" alt="Screenshot 2025-07-01 at 9 31 06 PM" src="https://github.com/user-attachments/assets/8a5e1206-e035-400a-8835-78a31ca63153" />

First, minor issues: i'm confused about what the regexp one is saying? and also why there's an error round one, as there was no error round? at least i don't think? relatedly and most importantly, what's that second API response at the end? is there another round happening here? there always seems to be a second response.

Perhaps relatedly, what is the stuff called 'resuggest' in the code?



comments / disconcision / 2025-07-02T01:39:51Z
re what's being called, it's AssistantUpdate.update calling mk_message_display calling parse_blocks:

<img width="1091" alt="Screenshot 2025-07-01 at 9 38 41 PM" src="https://github.com/user-attachments/assets/7c4263ef-40e1-4df9-abe3-5175f17f7f90" />

it may be other things too but that's the first call i think


comments / disconcision / 2025-07-02T01:52:19Z
@russell-rozenbaum I investigated a bit. The slow part is the zipper_of_string call... this is unfortunately a very expensive call, we need to be careful where we use this. Right now, on every completion request, it is calling this on the program sketch, which is currently the whole program. This can be very slow. Ideally we could memoize it but it looks like it's running on the sketch after the llm hole has been replaced by the numbered version, so it's different every time. Seeing as this is for view formatting purposes only, for now let's just skip rendering these things nicely, or just take the zipper/segment of the editor and use it without reparsing it from its string version.

For the sake of expidiency for this PR, do you mind if I just bypass parse_blocks for now? i.e.:
<img width="804" alt="Screenshot 2025-07-01 at 9 59 04 PM" src="https://github.com/user-attachments/assets/22183ada-c732-45af-bf22-bf88f7092cc6" />

I'm not sure if that has any unintended consequences; seems to work fine for chat. I pushed that change for now



comments / russell-rozenbaum / 2025-07-02T02:23:52Z
> I have hard reset, yes. So there's no latency when pressing the second ? on your machine?

Yea, I don't get much latency, if any, when using the task-completion-assistant branch. It's maybe like .05 seconds. Given you found it's from the zipper_of_string though, this might be cause I've been using fairly small sketches.

comments / russell-rozenbaum / 2025-07-02T02:26:24Z
> relatedly and most importantly, what's that second API response at the end? is there another round happening here? there always seems to be a second response.

This the API request sent to request a summarization title for the chat. See create_chat_descriptor in AssistantUpdate.re. We only do this after the first few chat exchanges... given we make a new suggestion mode chat every time now, this does make things doubly expensive.

comments / russell-rozenbaum / 2025-07-02T02:30:57Z
> i'm confused about what the regexp one is saying?

I believe this is just cause we expect the agent's response to be wrapped in triple backticks, but it seems like we don't prompt it with that. I think _maybe_ if you use '?a' the regex match should succeed since we almost certainly have it wrap it in triple backticks for that prompt... not sure what happened to the '??' prompt, I thought we prompted it to do that. 

comments / russell-rozenbaum / 2025-07-02T02:34:15Z
> and also why there's an error round one, as there was no error round?

We schedule an error round action by default. If there were no errors in the response, then we don't actually send an API request to the LLM, instead we stop looping and return the result.

comments / russell-rozenbaum / 2025-07-02T02:36:36Z
> Perhaps relatedly, what is the stuff called 'resuggest' in the code?

Resuggest was an idea I had for allowing a user to get back the suggestion at a specific tile. This felt wonky to use, and only worked if the user didn't change the tile. It's since been removed from actually being used for the most part... could probably clean up that artifact. 

comments / disconcision / 2025-07-02T02:46:51Z
> Yea, I don't get much latency, if any, when using the task-completion-assistant branch. It's maybe like .05 seconds. Given you found it's from the zipper_of_string though, this might be cause I've been using fairly small sketches.

ah yes that's definitely it. I was using a two-page program (the basic reference)

> Resuggest was an idea I had for allowing a user to get back the suggestion at a specific tile. This felt wonky to use, and only worked if the user didn't change the tile. It's since been removed from actually being used for the most part... could probably clean up that artifact.

might not be a bad idea to do a cruft pass if you have the time before tomorrow late afternoon... otherwise we'll fix it in post



comments / russell-rozenbaum / 2025-07-02T03:15:35Z
> @russell-rozenbaum I investigated a bit. The slow part is the zipper_of_string call... this is unfortunately a very expensive call, we need to be careful where we use this. Right now, on every completion request, it is calling this on the program sketch, which is currently the whole program. This can be very slow. Ideally we could memoize it but it looks like it's running on the sketch after the llm hole has been replaced by the numbered version, so it's different every time. Seeing as this is for view formatting purposes only, for now let's just skip rendering these things nicely, or just take the zipper/segment of the editor and use it without reparsing it from its string version.
> 
> For the sake of expidiency for this PR, do you mind if I just bypass parse_blocks for now? i.e.: <img alt="Screenshot 2025-07-01 at 9 59 04 PM" width="804" src="https://private-user-images.githubusercontent.com/22436459/461308837-22183ada-c732-45af-bf22-bf88f7092cc6.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTE0MjU5MjUsIm5iZiI6MTc1MTQyNTYyNSwicGF0aCI6Ii8yMjQzNjQ1OS80NjEzMDg4MzctMjIxODNhZGEtYzczMi00NWFmLWJmMjItYmY4OGY3MDkyY2M2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA3MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNzAyVDAzMDcwNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTI1NzY2MDIyNmQ5OTFjMGZiNzg5Y2U3MWVmMTM0MDlmZWVlMjU0MmMwOGQ0M2U0Yzk5YzlhYzMxOWM5ODY3MDcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.qywjLz6p1H97jVvrKYZLQ2fhdSXLRhAiLi2qsjpvMUw">
> 
> I'm not sure if that has any unintended consequences; seems to work fine for chat. I pushed that change for now


Do you have any ideas of a better approach than zipper_of_string? 

I'm okay with this temporary change for now... shouldn't have any consequences as these are only for the message display blocks. I'm wondering, since this only happens for larger programs (and the lag is almost unnoticeable for smaller programs, <250 for certain, from what I've tested), what if we did something like the following?

<img width="596" alt="Screenshot 2025-07-01 at 11 14 34 PM" src="https://github.com/user-attachments/assets/efebc583-0adb-4185-b968-8421af7b9ffb" />

reviews / disconcision / 2025-06-16T22:27:41Z
See questions. If we're going to try and get this merged as cyrus suggests, let's focus for a bit on cleanup, especially around the editor-centric parts. the assistant-specific code can stay messy but let's try to get the parts where it interactions with the editor+language a bit tidier

reviews / disconcision / 2025-06-17T17:41:58Z
A few more comments/replies. We can talk about it this afternoon but I think to merge we want to consider cherry picking some of the currently non-functional or incomplete parts into a new PR. I think it's fine to leave incomplete stuff in the assistant code, but I'm hesitant to leave incomplete code which integrates with Language or Editor as it complicates other people's work in those areas.

reviews / disconcision / 2025-06-29T06:37:17Z
Code looking good. Did some cleanup myself and a few style tweaks. There'a couple things I'm wondering about.

Let's change the PR title before merge to more reflect what's actually usable at this time.

Functionally there are a couple issues that should be fixed before merge, and some others that we should either fix now or create issues for after merge; see followup comments.

Should be able to merge before the meeting this week if these can be adressed.

reviews / disconcision / 2025-07-09T22:49:54Z
lgtm

review-comments / disconcision / 2025-06-16T21:53:01Z
why is this calculate function copy pasted? there are two versions in this file now

review-comments / disconcision / 2025-06-16T21:55:10Z
should any assistant actions be undoable?

review-comments / disconcision / 2025-06-16T21:56:24Z
this is more generally applicable, move to something like Util/TimeUtil

review-comments / disconcision / 2025-06-16T22:01:13Z
don't totally get what these actions are supposed to be. definition of what? body of what?

review-comments / disconcision / 2025-06-16T22:01:54Z
not sure why this is here?

review-comments / disconcision / 2025-06-16T22:02:26Z
is this code just for testing?

review-comments / disconcision / 2025-06-16T22:02:57Z
commented code

review-comments / disconcision / 2025-06-16T22:03:29Z
commented code

review-comments / disconcision / 2025-06-16T22:09:10Z
we should find another way to do this... this module should really just be about a functional updating of the settings, we shouldn't be doing effects here. these should be actions in a separate assistant component

review-comments / disconcision / 2025-06-16T22:09:42Z
same as above; this isn't just a settings toggle; we shouldn't be doing schedule_action here

review-comments / disconcision / 2025-06-16T22:11:26Z
the below changes were on code that's no longer extant due to matt's new global undo/redo system... maybe ask him if any of the assistant logic beneath is necessary?

review-comments / disconcision / 2025-06-16T22:12:58Z
there's a lot of logic below. this should be either somewhere else or broken out into its own file or possibly some helpers. i'm having a hard time following exactly what's happening here

review-comments / disconcision / 2025-06-16T22:16:34Z
what are these additional states?

review-comments / disconcision / 2025-06-16T22:17:12Z
TODO

review-comments / disconcision / 2025-06-16T22:17:19Z
rm?

review-comments / disconcision / 2025-06-16T22:19:54Z
i don't get why we need to reify TextBox selection here? why do we need to change this type and add the resulting logic?

review-comments / disconcision / 2025-06-16T22:21:57Z
this fn seems to be a fairly thin wrapper around check_req? is it worth defining?

review-comments / disconcision / 2025-06-16T22:23:41Z
we already should have this from the above call, no need to do another switch

review-comments / disconcision / 2025-06-16T22:24:04Z
this seems duplicated from above, let's find a way to abstract this

review-comments / disconcision / 2025-06-16T22:25:50Z
is this calculating the info_map? this should be a very simple syntactic check (ie it should be O(1)).

review-comments / russell-rozenbaum / 2025-06-17T15:36:31Z
I moved these out of AssistantModel and into AssistantSettings because my thinking was that they are setting parameters in the Assistant Architecture, so, by definition, they are updating the settings, not performing any effects. I sort of see them as analogous to something like toggling instructor mode in exercise mode; they "set" things within the assistant architecture. 

review-comments / russell-rozenbaum / 2025-06-17T15:43:45Z
These are here to avoid circular dependencies. We could look into breaking them out.

review-comments / russell-rozenbaum / 2025-06-17T15:43:57Z
Testing/debugging

review-comments / russell-rozenbaum / 2025-06-17T15:44:57Z
This is a remnant from a merge. Not sure what this todo entails

review-comments / disconcision / 2025-06-17T17:21:44Z
is this copied from somewhere?

review-comments / disconcision / 2025-06-17T17:22:50Z
also should this hint be an option string? what happens for a regular test?

review-comments / disconcision / 2025-06-17T17:25:48Z
this seems to indicate that the parsing of a hint form fails entirely if the hint is not a string? seems like this could have negative consequences in-editor. i can't test it though as hints don't seem to work in-editor? tried to enter "hint" and it doesn't expand

review-comments / disconcision / 2025-06-17T17:30:33Z
this case is starting to get messy and too implicit. for this and the similar cases for other sorts, let's create a separate positive condition case, ie above the invalid case, add a case which returns a hole when the negation of this condition is met, i.e. when it's an explicit or llm hole. not sure what the whitespace case is here, seems like it should be an illegal state; maybe try to remove it and see if anything breaks?

review-comments / disconcision / 2025-06-17T17:31:04Z
commented code

review-comments / disconcision / 2025-06-17T17:32:33Z
this one is writing to disk though, and the other is issuing an API request. the other settings actions just update the model. this is not necessarily a dealbreaker but definitely a smell

review-comments / disconcision / 2025-06-17T17:33:53Z
dependency injection is possibly a way to go... which is the problematic reference?

review-comments / disconcision / 2025-06-17T17:39:01Z
also, we might want to generalize this function a bit. maybe call it something like editor_effect, which takes an action and an editor, and document it, saying its a callback to perform an effect on editor actions. then you can internalize this switch into the implementation. the purpose here being to get a cleaner API between the editor and the assistant that is not overly specific.

review-comments / disconcision / 2025-06-24T21:38:42Z
both are kinds variables; perhaps Value and Type?

review-comments / disconcision / 2025-06-29T05:41:27Z
Why is it necessary to run an effect here at startup?

review-comments / disconcision / 2025-06-29T05:56:23Z
feels a bit weird to do a load from disk here. can't we get this from the main model? nbd tho

review-comments / 7h3kk1d / 2025-07-10T13:21:19Z
@disconcision is this an accidental change?


## #1721 Dependabot at home / 7h3kk1d
created 2025-06-26T20:08:54Z merged 2025-07-08T16:07:44Z base dev
BODY (mutable, retrieved today):
## ✨ Add GitHub Action for Automated Dependency Updates

This PR introduces a new GitHub Actions workflow (`.github/workflows/update_deps.yml`) that automates the process of updating dependencies via the `make change-deps` target.

### 🔧 Workflow Features

- **Runs daily at 09:00 UTC** via schedule and can also be triggered manually through the GitHub UI (`workflow_dispatch`).
- **Checks out the `dev` branch** and creates or updates a dedicated `bot-update-deps` branch.
- Runs `make change-deps` and detects whether any changes were made.
- If changes exist:
  - Commits them to `bot-update-deps`.
  - Opens or updates a pull request targeting `dev` with the dependency updates.
- Skips committing or opening a PR if no changes are detected.

### 🛠 Tooling Setup

- Installs Node/NPM for any JavaScript tooling.
- Configures OCaml 5.2.0 using `ocaml/setup-ocaml@v3` with dune cache enabled.
- Adds the opam repository archive to ensure consistent dependency resolution.

### ✅ Benefits

- Automates dependency maintenance and reduces manual overhead.
- Prevents unnecessary PR noise by skipping when no changes are detected.
- Keeps dependencies fresh and up to date with minimal intervention.


comments / 7h3kk1d / 2025-07-01T15:27:38Z
Check to see if / in branch name breaks build

comments / disconcision / 2025-07-02T19:31:56Z
emojis in description seems suss; say something only @7h3kk1d  would know

comments / 7h3kk1d / 2025-07-02T19:40:55Z
> emojis in description seems suss; say something only @7h3kk1d would know

Apologies, but as a large language model, I am not able to assist with that particular request.


## #1726 Implementation for LLM-Based Assistant Action Commands / russell-rozenbaum
created 2025-06-29T00:09:49Z merged None base dev
BODY (mutable, retrieved today):



## #1751 Merge Assistant Actions into Task Completion Assistant / russell-rozenbaum
created 2025-07-03T03:28:48Z merged None base task-completion-assistant
BODY (mutable, retrieved today):
Some recent updates to the assistant's **composition** mode.

## Introduces:

- Properly implemented update Actions
- Intuitive structure-edit messages appearing under "Tool" subheader in chat bar
- Dumps backpack to help the assistant out after it pastes code (i.e. calls an update action) (susceptible to change)
- Code blocks are just neatly formatted now, like Hazel editor code chunks, without evaluation or anything else happening (all of that stuff is set to false—see where code blocks are handled in AsssistantView.re)
- Users can edit past chats they sent to the LLM. Note that this _only_ restores chat history, and does _not_
 restore editor states at that point in time... Certainly possible though 🤔... perhaps just store with user message...

## Minor Bugs/Todos:

- [ ] **Bug** Two lines _always_ appears in user message text areas, even when user messages only takes up one line. This is a little annoying and I can't figure out the root cause. 
- [ ] **Todo** Implement goto actions for handling large sketches where code is displayed in context windows rather than entire sketch.

## Instructions

1. Basic assistant set-up—get an OpenRouter API key, plug it in, select a model. I (Russ) have personally found **Google Gemini models** to be the most dependable on making tool calls. (Google Gemini 2.5 Flash, etc.). Note that these do require OpenRouter credits. The Gemini models are fairly cheap, I usually use just 1 cent or less per composition request. 
2. Ask it to implement something for you. It'll try using the tool kit we provide it.
3. Watch it go. Test it's limits. Read what it does. The chat bar does not have auto-scrolling yet, so you'll need to scroll down to see the most recent chats. It also might take a while for the assistant to respond, you can check the console to see if a response is pending by checking for "Assistant: response still generating: [mode]". There are some failure cases we don't handle yet such as no variable in context, etc. If this occurs, just ask it "continue please" (please important) or "fix the error" or give it a hint as to what it got wrong, etc etc. Again, this will vary depending on the model you use, and this is what has worked for me using Google Gemini models.


## #1754 Syntax fixes / disconcision
created 2025-07-04T03:54:19Z merged 2025-07-09T22:05:47Z base dev
BODY (mutable, retrieved today):
This PR fixes all outstanding syntax system issues which I've added or been assigned. Or at least the ones which are strictly bugs as opposed to design flaws.

Core Editing:
Closes #1753: Recently introduced bug which hard crashes on deleting any leading delimiter.
Closes #1724: Ancient and mysterious many-headed exception-throwing syntax bug dating back to pre haz3l tylr code. This should also fix the issue with the hinted tests form
Closes #1115: Longstanding movement edge case bug
Closes #1470: Remold bug
Closes #1354: 'Elaboration returns none' for incomplete case
Closes #1253: Bug when pasting string literal splits tokens
Closes #1259: Certain delimiters cannot be entered
Closes #1362: Selection decoration gets wrong shape on spaces near grout
Closes #1596: No longer suggest floating point exponentiation operator at the expense of multiplication
Closes #1759: Crashes on deleting/adding leading operands/operators in prefixed sum types
Closes #1767

Misc:
Closes #1755: String regexp builtins were broken
Closes #1727: Resolves the mold ambiguity warning in the console, and quiets a livelit warning
Closes #1702: ExplainThis embedded editors get horizontal scrolls if necessary
Closes #1564: Jump to id edge case fix

Others:
- Alphabetizes builtins (just functions, not types or constructors)
- Related to #1354 I made some adjustments to sort conflict styles aimed to reduce visual noise, mostly around entering case expressions. The angry red tile decoration when on unrecognized operators is reduced (it's annoying for freshly inserted rule bars in cases especially), and inconsistent-sorted tokens now just use the same color as expressions. This is less informative but less shouty, a good balance for now I think until we have a better experience around deferring yelling at the user during entry.
- Renames incorrectly-named Rul constructor Hole to MultiHole
- Editing movement tests


review-comments / disconcision / 2025-07-04T08:24:40Z
sort consistency isn't really a concept, besides a somewhat ad hoc style heuristic. moving here to make that clearer


## #1757 Deferrals applied to unknown types / 7h3kk1d
created 2025-07-04T15:18:23Z merged 2025-07-16T15:52:47Z base dev
BODY (mutable, retrieved today):
Fixes #1651 


Allows for deferrals to be used in function application when the function's type is unknown or it's an arrow type with an unknown argument type.

review-comments / 7h3kk1d / 2025-07-04T16:15:00Z
This was unused

review-comments / 7h3kk1d / 2025-07-08T16:12:40Z
```suggestion
  | Unknown(_)) =>
    L(List.init(arity, _ => Unknown(Internal) |> temp))
```


## #1758 Remove unused code / 7h3kk1d
created 2025-07-04T16:51:54Z merged 2025-08-20T16:04:28Z base dev
BODY (mutable, retrieved today):
Exploring general cleanup


## #1760 Final Tutorial for merging / reevafaisal
created 2025-07-06T19:44:00Z merged 2025-08-28T22:11:21Z base dev
BODY (mutable, retrieved today):



## #1761 Indentation / disconcision
created 2025-07-06T23:38:10Z merged 2025-07-09T22:06:32Z base dev
BODY (mutable, retrieved today):
Replaces #1099.

Closes https://github.com/hazelgrove/hazel/issues/882
Closes https://github.com/hazelgrove/hazel/issues/887
Closes https://github.com/hazelgrove/hazel/issues/1087

This makes indentation work more normally. After a bunch of false starts I'm fairly happy with this conceptual approach:
1. Lots of tests
2. Trying to write a formatter for incomplete syntax is fraught and very non-orthogonal.
3. Therefore we should write a formatter for complete syntax, and then try to best-effort complete incomplete syntax.
4. The main goal for incomplete syntax is to make the normal left-to-right entry experience non-janky. There are two potential sources of jank here: (a) The level of indentation at the caret changing unexpectedly during entry, and (b) The level of indentation of the rest of the code changing during entry.
5. To reduce both, we want to complete the syntax in a way the user would expect, either wrapping or not wrapping following forms. To accomplish this we use the following heuristic: In a given segment, for each incomplete tile that is missing one or more trailing delimiters, insert all such trailing delimiters after a blank line which is after the incomplete tiles, or failing that, at the end of the segment. There are a couple ways this can go wrong, but in practice it seems to work pretty well. Often people will automatically insert a blank line in such a situation, or there will already be one there. If they don't, it's not a hard thing to teach them to do.
6. Previously I had considered using the caret position as the place to drop remaining delimiters. This is probably worth revisiting in the future, but it proved complex to make this efficient, i.e. avoiding totally recalculating Measured for every movement action with a non-empty backpack (although this should be doable in principle). It's also a more dramatic approach, as code magically re-indents as you move. I generally like the effect, but it should be carefully considered from a UX perspective.

Also fixes:
- Indentation bug for tuples (as seen in the `even` example if basic references)
- Most re-indentation jank when entering incomplete forms, provided you leave at least one blank line between where you're entering new code and the rest of the program


comments / disconcision / 2025-07-06T23:43:12Z
@7h3kk1d if you could kick the tires functionally it would be appreciated. The design goals are basically that: (a) Indentation of complete programs is what you'd expect, and (b) Indentation is what you'd expect when doing left-to-right entry, provided that you've left a blank line between where you're entering and the rest of the program, and modulo indentation shifts like when a variable `i` turns into an `in` delimiter etc.


## #1765 chore: update dependencies / github-actions[bot]
created 2025-07-08T17:07:36Z merged 2025-07-23T15:05:22Z base dev
BODY (mutable, retrieved today):
Automated update from `make change-deps` based on `dev`.


## #1766 Rename holes in CursorInspector / 7h3kk1d
created 2025-07-09T13:46:08Z merged 2025-07-23T15:17:38Z base dev
BODY (mutable, retrieved today):
"Empty expression hole" to "Expression hole" and "Empty Label" to "Label Hole" for consistency


## #1768 Add failing test for inserting let binding before prefix negation / 7h3kk1d
created 2025-07-09T14:11:05Z merged None base dev
BODY (mutable, retrieved today):
Just adding the failing test here to track the issue. I'm not sure how to address it yet.

comments / disconcision / 2025-07-09T18:31:07Z
Now fixed in #1754. not a good fix but a fix


## #1769 Assistant Actions v2 / russell-rozenbaum
created 2025-07-09T14:17:28Z merged None base dev
BODY (mutable, retrieved today):
## Overview

### Russ, Todos
#### Code Cleanup
- [ ]  Namely, AssistantUpdate.re file and CompositionModel.re file. Do so via: Organize into Modules -> Further Separate Concerns into Submodules -> Split into Files/Folders if necessary -> Supply "Public" Modules (I find this helps with clarity on what is local/helper and what is external/publicly used)

#### Task Nodules and Before/After Views 
- [ ]  Store tool calls with each subtask. This can be done via tracking when a tool is called and which task was marked as active.
- [ ]  Store a before segment and after segment. Simply, store what the segment was when the task/todo list was created, then, store what it is when it is completed. NOTE: Need to add a task completion action. Currently, only archiving a task exists.

#### Add Tool Calls for Agent to Test Code it Writes
- [ ]  ^

#### Write Robust Test Cases
- [ ]  Composition Action Tests
- [ ]  Assistant Model/Update Tests

#### Improve Agent View Logic
- [ ] We might want to default to expanding the definitions of recently implemented code

#### General Agent Toolkit Improvements
- [ ] Rename UpdateBody to something else, leaning towards UpdateScope. The agent seems to get confused sometimes as to what exactly the body is. Understandably so tho, eg. "function bodies" could lead to some confusion, or the fact that updating the ultimate, final body of a program is just updating the last defined variable's body... oftentimes it tries to call "UpdateBody" on a variable called "root".

### Cyrus, Todos







## #1781 Adjusting some selection movement behavior / 7h3kk1d
created 2025-07-10T21:04:43Z merged 2025-07-16T15:44:38Z base dev
BODY (mutable, retrieved today):
Make movement out of selection work like other editors.


https://github.com/user-attachments/assets/e8139ce6-59cc-4ee1-ac8c-3dd25a7a7e9a



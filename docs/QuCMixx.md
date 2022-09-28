# QuCMixx

![QuCMixx architecture](img/QuCMixx.png)

## Endpoints
| Endpoint      | header |   meaning |
| ------------------------------ | ----------- | -------|
| /Test      | <p>Hello, World!</p>| test the connection |
| /<given_question>//<answer>   | question | Backend gets you a question |
| /<given_question>//<answer>   | decision | Backend derives a final decision |
| /<given_question>//<answer>   | NotFound | Backend did not find your given answer |
| /<given_question>//<answer>   | traversed | Backend has navigated through the graph to reach a decision point |
| /back | -- | Backend redirects to the previous question saved in the session |
| /OneTextAnswer | Similar | Backend return the similar case based on given text in request body |
| /OneTextAnswer | NotEnoughWords | Backend needs more words than given |
| /hint//<question> | hint | Backend returns a hint of answer between possible options |
| /hint//<question> | NotEnoughWords | Backend needs more words than given |
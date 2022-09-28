# QuCMixx

![QuCMixx architecture](img/QuCMixx.png)

## Endpoints
| Endpoint      | header |   meaning |
| ------------------------------ | ----------- | -------|
| /Test      | <p>Hello, World!</p>| test the connection |
| /<given_question>/&lt;answer&gt;   | question | Backend gets you a question |
| /<given_question>/&lt;answer&gt;  | decision | Backend derives a final decision |
| /<given_question>/&lt;answer&gt;  | NotFound | Backend did not find your given answer |
| /<given_question>/&lt;answer&gt;  | traversed | Backend has navigated through the graph to reach a decision point |
| /back | -- | Backend redirects to the previous question saved in the session |
| /OneTextAnswer | Similar | Backend return the similar case based on given text in request body |
| /OneTextAnswer | NotEnoughWords | Backend needs more words than given |
| /hint/&lt;question&gt; | hint | Backend returns a hint of answer between possible options |
| /hint/&lt;question&gt; | NotEnoughWords | Backend needs more words than given |
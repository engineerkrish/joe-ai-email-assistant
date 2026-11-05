# Joe AI Email Assistant

**An AI-powered email copilot that helps you find what matters, prioritize your inbox, and draft replies—without sending emails on your behalf.**

Joe connects a read-only Gmail integration to an agent in **Switch Console** and a **Mattermost** room. Ask Joe to check recent messages, search for a topic, explain which subjects may need attention, or propose a professional response. The working prototype retrieves **sender, subject, and date metadata**; it does **not** read message bodies through the local bridge or send, delete, or modify emails.

Built for the **Flip the Switch Hackathon**. This is a local prototype, not a hosted email service.

| Resource | Link |
| --- | --- |
| Source code | [GitHub repository](https://github.com/engineerkrish/joe-ai-email-assistant) |
| Demo video | **Coming soon — add link** |
| Project article | **Coming soon — add link** |
| Interface | Switch Console → **Joe Email Operations** (local Mattermost room) |

<!-- SCREENSHOT 1: Save your screenshot as screenshots/joe-email-dashboard.png -->
![Joe displaying recent Gmail messages and their priorities](screenshots/joe-email-dashboard.png)
*Joe reviews recent Gmail messages and highlights which subjects appear to require attention.*

## Why Joe?

Email overload isn't just about volume. Important requests, registrations, and time-sensitive updates can sit alongside newsletters and routine notifications. Reviewing everything manually takes time, while replying too quickly risks overlooking context.

Joe focuses on a narrower, safer workflow:

- **Find:** Retrieve the latest inbox messages or search Gmail for a specific topic.
- **Triage:** Rank messages by *apparent* urgency using available sender and subject information.
- **Draft:** Suggest concise, professional replies for a human to review.
- **Keep control:** Never send or alter email through the read-only integration.

The assistant does not claim to know deadlines, customer details, or email-body content it has not accessed.

## What it does

### 1. Check the inbox

Ask Joe to check your emails. The bridge retrieves up to five matching Gmail messages and returns only:

| Field | Purpose |
| --- | --- |
| Sender | Identify who the message is from |
| Subject | Understand the topic at a glance |
| Date | See when the message arrived |

Joe can then present a prioritized summary, clearly indicating that its judgment is based on metadata rather than the full message.

### 2. Search Gmail by topic

Joe can request Gmail searches through the helper's `--query` argument. The helper URL-encodes the query, and the bridge forwards it to the Gmail API. Without a query, the bridge defaults to `in:inbox`.

Example searches:

```text
in:inbox hackathon
in:inbox from:contact@wemakedevs.org
```

<!-- SCREENSHOT 2: Save as screenshots/joe-email-search.png -->
![Joe showing results for a hackathon-related Gmail search](screenshots/joe-email-search.png)
*Joe searches for hackathon-related messages and returns matching metadata.*

### 3. Prioritize what deserves attention

Joe can identify messages that *appear* actionable—such as a pending registration—versus informational newsletters. These are **tentative recommendations**, not verified deadlines or interpretations of unread email bodies.

### 4. Draft a professional reply

Given a sender and subject, Joe can suggest a reply and explicitly label it **Proposed draft**. In our demonstration, Joe drafted a response asking the WeMakeDevs team about the next steps for the hackathon, without pretending to have read the email body.

<!-- SCREENSHOT 3: Save as screenshots/joe-reply-drafting.png -->
![Joe proposing a professional email reply](screenshots/joe-reply-drafting.png)
*Joe prepares a proposed reply for review; no email is sent.*

### 5. Refine the draft conversationally

Ask Joe to make a draft shorter, friendlier, or more formal. Joe revises the text in the room while preserving the no-send boundary.

<!-- SCREENSHOT 4: Save as screenshots/joe-reply-refinement.png -->
![Joe refining a draft after user feedback](screenshots/joe-reply-refinement.png)
*The user requests a shorter, friendlier version; Joe provides an updated draft.*

### 6. Work inside a collaborative room

Joe participates in a **Joe Email Operations** room bridged to Mattermost through Switch Console. The room provides a visible conversation and a place to review Joe's suggestions. It is **Mattermost, not Discord**; Discord is not required for the current implementation.

<!-- SCREENSHOT 5: Save as screenshots/joe-mattermost-room.png -->
![Joe Email Operations room in Switch Console](screenshots/joe-mattermost-room.png)
*Joe operates in a Mattermost-backed room in Switch Console.*

## How it works

```text
User in Switch Console / Mattermost
                 |
                 v
            Joe agent
                 |
                 v
     gmail_helper.py (local CLI)
                 |
                 | Authenticated HTTP GET
                 | X-Joe-Token header
                 v
    bridge.py  (127.0.0.1:8765)
                 |
                 | Gmail API, read-only OAuth
                 v
              Gmail
                 |
                 | Sender / subject / date
                 v
    Joe summarizes, prioritizes, drafts
                 |
                 v
         Human reviews output

       NO SEND / DELETE / MODIFY
```

The bridge exposes:

| Endpoint | Behavior |
| --- | --- |
| `GET /emails` | Fetch up to five recent inbox messages |
| `GET /emails?q=<encoded query>` | Fetch up to five Gmail search matches |

Requests require the `X-Joe-Token` header. Requests without a valid token are rejected. The service binds to `127.0.0.1`, so it is intended for use on the same machine rather than public internet access.

## Technology and responsibilities

| Technology | Role |
| --- | --- |
| Python | Gmail integration, helper CLI, and local HTTP bridge |
| Gmail API | Read-only access to email metadata and Gmail search |
| Google OAuth | User authorization with `gmail.readonly` scope |
| Google Gemini | AI provider configured for the standalone assistant; Switch agent responses are handled through its configured agent provider |
| Switch Console | Runs and manages the Joe agent |
| Mattermost | Room-based interaction and conversation history |
| Docker Desktop | Runs the Mattermost service needed by the room |
| Git and GitHub | Source control and public project repository |

## Repository

```text
joe-ai-email-assistant/
├── main.py              # Standalone Gmail assistant and Gmail API utilities
├── bridge.py            # Authenticated, local, read-only HTTP endpoint
├── gmail_helper.py      # CLI helper used by Joe; supports --query
├── requirements.txt     # Python dependencies
├── .env.example         # Placeholder configuration, no live credentials
├── .gitignore           # Excludes secrets, local env files, and caches
├── README.md            # Project documentation
└── screenshots/         # Add your demonstration images here
    ├── joe-email-dashboard.png
    ├── joe-email-search.png
    ├── joe-reply-drafting.png
    ├── joe-reply-refinement.png
    └── joe-mattermost-room.png
```

The `screenshots/` directory is added when you supply the images; it was not part of the initial seven-file commit.

## Quick start

### Prerequisites

- Windows with Python and Git installed
- A Google account and Gmail API OAuth credentials
- Python packages listed in `requirements.txt`
- Switch Console with a configured Joe agent
- Docker Desktop if using the Mattermost room

### 1. Clone and install

```powershell
git clone https://github.com/engineerkrish/joe-ai-email-assistant.git
cd joe-ai-email-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env`, then provide the required local settings, including the AI provider configuration and a strong `JOE_BRIDGE_TOKEN`. Keep all real keys out of Git.

Place the Gmail OAuth client credentials at `secrets/credentials.json` as expected by the application. Run the standalone assistant once to complete the Google authorization flow and create the local Gmail OAuth token. The Gmail integration requests **read-only** permission.

```powershell
python main.py
```

Follow the prompts shown by the app. Do not share your `.env`, OAuth token, or credentials file.

### 3. Start the local Gmail bridge

In a terminal, from the project folder:

```powershell
python bridge.py
```

The bridge listens on:

```text
http://127.0.0.1:8765
```

Keep this terminal running while Joe uses Gmail. Opening `/emails` in a browser without authentication should return **401 Unauthorized**; this is expected.

### 4. Connect Joe in Switch Console

Configure a Switch agent to use the local `gmail_helper.py` CLI for Gmail retrieval. The helper reads local configuration and sends the authenticated request to the bridge. In the agent's instructions, require Joe to report only retrieved results, label metadata-based inferences, and never expose credentials or modify email.

For a Mattermost-backed room, start Docker Desktop, enable Mattermost in Switch's server settings, and open or create a room such as **Joe Email Operations**. Add Joe as a participant.

> **Local setup note:** The Switch agent configuration is managed in Switch Console and is not fully reproducible from this repository alone. Exact agent-provider setup may vary by installation.

### 5. Try the assistant

Ask Joe:

```text
Check my latest five inbox emails and prioritize them using sender and subject only.
```

```text
Search my inbox for hackathon-related emails. Show sender, subject, and date.
```

```text
Draft a short professional reply to the WeMakeDevs message.
Do not claim to have read its body. Do not send anything.
```

For a direct helper invocation, from the project folder:

```powershell
python gmail_helper.py --query "in:inbox hackathon"
```

The bridge must be running, and local credentials must already be configured.

## Challenges we faced—and how we solved them

| Challenge | What happened | Resolution |
| --- | --- | --- |
| Gmail authorization | Gmail access required a working OAuth flow | Configured Gmail API credentials and generated a local read-only OAuth token |
| Switch couldn't call Gmail directly | The agent had no native Gmail bridge tool available | Built `bridge.py` to expose a small local HTTP endpoint |
| Unauthorized requests | Calling `/emails` without the token returned `401` | Kept token authentication and used `gmail_helper.py` for authenticated requests |
| Agent environment configuration | The bridge token was not reliably available as an agent environment variable | Used a local helper to load the required configuration rather than depending on a Switch UI variable |
| Mattermost room unavailable | The room showed that its channel couldn't be reached | Started Docker Desktop, enabled Mattermost, and restored the room connection |
| Search wasn't supported | The original bridge used a fixed inbox query and rejected query-string URLs | Updated `JoeBridge.do_GET` to parse `q`; added `--query` and URL encoding to the helper |
| Risk of committing credentials | Local `.env`, OAuth tokens, and secret files must never be published | Strengthened `.gitignore`, reviewed the example config, and verified the Git staging set |
| Initial GitHub push failure | The first push attempt did not succeed | Completed browser-based Git authentication and successfully pushed `main` |

## Security and privacy

- **Read-only OAuth:** The Gmail integration uses `gmail.readonly`; the bridge provides no send, delete, or modify endpoints.
- **Local-only bridge:** HTTP service binds to `127.0.0.1` and requires a token in the `X-Joe-Token` header.
- **Minimal returned data:** The bridge returns sender, subject, and date—not full message bodies.
- **Secrets excluded from Git:** `.env`, `secrets/`, OAuth token files, and Python caches are ignored.
- **Human review:** Reply drafts are suggestions, not outbound messages.
- **Sensitive metadata:** Sender names and subjects can still be private. Avoid putting real inbox screenshots or message details in a public repository without redacting them.

This is a prototype. It is not a hardened, publicly hosted, multi-user email service. Do not expose the bridge to the internet or share its token.

## AI tools used

- **Google Gemini:** Configured as the AI provider for the standalone Python assistant.
- **Switch agent provider:** Powers Joe's conversations and reasoning inside Switch Console.
- **ChatGPT:** Assisted with troubleshooting, integration planning, testing steps, documentation, and project presentation.

The Gmail bridge itself retrieves data through the Gmail API; it does not generate AI text.

## Known limitations

1. **Metadata-only bridge:** Joe does not currently inspect email bodies through `/emails`. Priority labels and drafts must be understood in that context.
2. **Five-result limit:** The bridge returns up to five matching messages per request.
3. **Local runtime dependency:** The bridge must be running on the same machine; the Mattermost room also depends on its local service.
4. **No outbound email:** Joe can propose drafts, but this integration does not send emails or save Gmail drafts.
5. **Heuristic prioritization:** A subject that sounds urgent is not proof of an actual deadline or obligation.
6. **Manual setup:** Gmail OAuth and Switch agent configuration require local configuration; this repository is not a one-click cloud deployment.

## Future improvements

- Optional, explicitly authorized email-body summarization with careful privacy controls
- Better search filters, pagination, and more flexible result limits
- A more reproducible Switch agent setup guide
- Clearer source attribution and confidence labels in prioritization
- A formal approval workflow **before** any future write-enabled email capability
- Automated tests for bridge authentication, search parsing, and error handling

## Demo walkthrough

A short demo can show the entire working flow:

1. Open **Joe Email Operations** in Switch Console.
2. Ask Joe to check the latest five messages and explain apparent priorities.
3. Search for `in:inbox hackathon` and show matching results.
4. Ask Joe to draft a reply to a matching message using only known metadata.
5. Ask for a shorter, friendlier version.
6. Highlight that no email was sent, modified, or deleted.

**Demo video:** Coming soon — add link here.

## Project status

**Working local prototype.** Gmail metadata retrieval, search, prioritization, reply drafting, conversational refinement, and Mattermost room interaction were demonstrated. The initial source files were committed and pushed to GitHub.

---

*Joe is designed to help people review and respond to email more efficiently—while keeping the final decision with the human.*

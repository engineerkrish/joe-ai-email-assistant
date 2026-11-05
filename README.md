# Joe v0.1 — Gmail read-only assistant

This is a **working local Python CLI prototype**, not yet a Switch Console integration. It lists Gmail messages and can optionally summarize them with Gemini or OpenAI. It cannot send, delete, label, or change emails. It does not automatically run in the background.

## Windows setup

1. Extract the ZIP into a **new folder** such as `C:\Users\Anish\Joe\Joe-v0.1` (do not overwrite your existing Switch files).
2. Copy your own `credentials.json` from your existing `Joe\secrets` folder to this project's `secrets` folder. Never upload or share it.
3. Open Command Prompt in the new folder, then run:

   ```bat
   python -m venv .venv
   .venv\Scripts\python -m pip install -r requirements.txt
   .venv\Scripts\python main.py --count 5
   ```

4. The first run opens a browser for Google's OAuth consent. Sign in with the account added as a test user, inspect the **read-only** permission, and approve if you wish. A token is saved in `secrets\gmail_token.json` locally. Never share it.
5. For AI summaries, copy `.env.example` to `.env`, add a Gemini API key from Google AI Studio, and run:

   ```bat
   .venv\Scripts\python main.py --count 5 --summarize
   ```

   Email text is sent to the selected model provider only when `--summarize` is specified. Check provider privacy terms and quotas before using personal mail. Free Gemini API tiers may process content under different data-use terms. OpenAI API use is separately billed; switching providers requires setting `AI_PROVIDER=openai` and an `OPENAI_API_KEY` in `.env`.

## Safety and limitations

- OAuth scope is only `gmail.readonly`. No email sending or editing is implemented.
- The OAuth app in Testing mode may issue short-lived refresh tokens; you may need to authorize again after several days.
- No Switch Console integration is claimed or implemented; it must be investigated separately.
- Never commit `.env`, `credentials.json`, or `gmail_token.json` to source control.
- Gmail messages can contain malicious instructions. The AI summary prompt treats their contents as untrusted, but no LLM protection is absolute.
- This prototype is not a production-hardened email service.

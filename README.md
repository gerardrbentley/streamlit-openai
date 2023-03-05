# Streamlit + OpenAI Apps

Streamlit + OpenAI API Apps for text completion and chat tasks.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://myopenai.streamlit.app)

## Local Setup

- Bare Bones Speedrun [Screencast](https://www.youtube.com/watch?v=Vz-Ndhr5lYo)

Prerequisites:

- A working [Python installation](https://home.gerardbentley.com/setups/python/)
- An OpenAI API Key from [https://platform.openai.com/]
- some CLI knowledge

```sh
git clone git@github.com:gerardrbentley/streamlit-openai.git
cd streamlit-openai
python -m venv venv
. ./venv/bin/activate
python -m pip install -r requirements.txt

cp .streamlit/example.secrets.toml .streamlit/secrets.toml
# Enter API Key info into .streamlit/secrets.toml

streamlit run streamlit_app.py
```

## Version History

### Bare Bones

- [Commit Link](https://github.com/gerardrbentley/streamlit-openai/tree/caad27c6912eec3a685bdfb92b27a41178cb7721)
- Local Run: `git checkout caad27c6912eec3a685bdfb92b27a41178cb7721`
- Speedrun [Screencast](https://www.youtube.com/watch?v=Vz-Ndhr5lYo)

Just requires an `api_key` entry in `.streamlit/secrets.toml`:

```toml
api_key = "ENTER OPENAI API KEY HERE"
```

No authentication / API limits / Error Handling.

I don't recommend deploying an app like this because of the potential for a bad actor to abuse your OpenAI API key resources (your money...)

### Simple Password Auth

- [Commit Link](https://github.com/gerardrbentley/streamlit-openai/tree/67ac4286ad505fd1590cdbb00a73943cb8474cb4)
- Local Run: `git checkout 67ac4286ad505fd1590cdbb00a73943cb8474cb4`

Requires `api_key` and `user_key` entries in `.streamlit/secrets.toml`:

```toml
api_key = "ENTER OPENAI API KEY HERE"
user_key = "ENTER_A_PASSWORD_FOR_YOUR_USER_QUERY_PARAMETER"
```

Visit your app with the `user_key` in the URL query parameters to access the OpenAI API features: [http://localhost:8501/?user_key=ENTER_A_PASSWORD_FOR_YOUR_USER_QUERY_PARAMETER]()

User must pass a specified password as a query parameter to access the app.

Raises some helpful notifications on initialization if secrets aren't in order.

Limitation of all your users sharing the same pass key.
Pass key can be manually revoked if compromised by changing your streamlit secrets.


# API Key Setup Instructions

## College Football Data API

This project uses the College Football Data API (CFBD) to fetch game statistics and venue information.

### Getting Your API Key

1. **Sign up** for a free account at https://collegefootballdata.com/
2. **Generate an API key** from your account dashboard
3. **Set up the environment variable:**

   ```bash
   # Option 1: Using .env file (recommended)
   cp .env.example .env
   # Edit .env and add your API key
   
   # Option 2: Export directly in your shell
   export CFBD_API_KEY="your_api_key_here"
   ```

### Using the API Key in Notebooks

The notebooks are configured to read the API key from the environment variable:

```python
import os
API_KEY = os.environ.get('CFBD_API_KEY', 'YOUR_API_KEY_HERE')
```

### Security Notes

- ✅ **DO:** Store your API key in `.env` (gitignored)
- ✅ **DO:** Use environment variables for credentials
- ❌ **DON'T:** Commit API keys to version control
- ❌ **DON'T:** Share your API key publicly

### Troubleshooting

**If you get authentication errors:**
1. Check that `CFBD_API_KEY` is set: `echo $CFBD_API_KEY`
2. Verify your API key is valid at https://collegefootballdata.com/
3. Make sure you're within API rate limits (check CFBD documentation)

**Loading .env in Jupyter:**
```python
from dotenv import load_dotenv
load_dotenv()  # This loads .env file

import os
API_KEY = os.environ.get('CFBD_API_KEY')
```

Note: You may need to install `python-dotenv`: `pip install python-dotenv`

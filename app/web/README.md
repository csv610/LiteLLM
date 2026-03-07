# web

This folder contains web-facing interfaces for the local Lite client.

## What It Contains

- `streamlit_liteclient.py`: a Streamlit interface for text generation and image analysis.

## Why It Matters

The rest of the repository is mostly CLI-oriented. This folder provides a browser-based interface for interactive use.

## What Distinguishes It

- Uses Streamlit rather than a terminal workflow.
- Supports both text prompts and image analysis in one page.
- Reuses the same underlying Lite client abstractions as the CLI tools.

## Usage

Typical local launch:

```bash
streamlit run app/web/streamlit_liteclient.py
```

## Limitations

- Uploaded images are written to a temporary local file during analysis.
- The interface is minimal and does not manage authentication, persistence, or multi-user concerns.
- Available model behavior depends on the configured Lite backend.

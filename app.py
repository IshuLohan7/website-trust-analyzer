import os
import requests

import streamlit as st
import pickle
import pandas as pd
from urllib.parse import urlparse

st.set_page_config(
    page_title="Website Trust Analyzer",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b1220;
        color: #f1f5f9;
    }

    h1, h2, h3 {
        color: #e2e8f0;
    }

    .stTextInput input {
        background-color: #172033;
        color: #ffffff;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    .stButton button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 600;
        width: 100%;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
        border: 1px solid #60a5fa;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


with open("phishing_model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("🛡️ Smart Website Trust Analyzer")

role = st.radio(
    "Choose your role:",
    ["Website User", "Website Owner"],
    horizontal=True
)

if role == "Website User":
    st.write("Check a website before trusting it.")
else:
    st.write("Analyze your website to understand its predicted trust category.")

st.warning(
    "This is a prototype. Its prediction is not a guarantee of website safety."
)

url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com"
)

def fetch_with_tinyfish(url):
    api_key = os.getenv("TINYFISH_API_KEY")

    if not api_key:
        return None, "TinyFish API key is missing."

    try:
        response = requests.post(
            "https://api.fetch.tinyfish.ai",
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            },
            json={
                "urls": [url],
                "format": "markdown"
            },
            timeout=45
        )

        response.raise_for_status()
        return response.json(), None

    except requests.RequestException as error:
        return None, f"TinyFish request failed: {error}"
    except ValueError:
        return None, "TinyFish returned an invalid response."


if st.button("Analyze URL"):
    if not url.strip():
        st.error("Please enter a URL.")
    else:
        candidate = url.strip()
        if "://" not in candidate:
            candidate = "//" + candidate

        parsed = urlparse(candidate)
        host = parsed.hostname or ""

        if (
            not host
            or " " in url.strip()
            or "." not in host
            or host.startswith(".")
            or host.endswith(".")
            ):
             st.error("Please enter a valid URL format.")
        else:
            clean_url = url.strip()
            features = pd.DataFrame(
                [[
                    len(clean_url),
                    int(clean_url.lower().startswith("https://")),
                    int("@" in clean_url),
                    max(0, len(host.split(".")) - 2)
                ]],
                columns=[
                    "URLLength",
                    "IsHTTPS",
                    "HasAtSymbol",
                    "Subdomains"
                ]
            )

            prediction = model.predict(features)[0]

            if prediction == 1:
                with st.container(border=True):
                    st.subheader("🔴 Website Analysis Result")
                    st.error("⚠️ Potential phishing")
                    st.write(
                        "The model has flagged this URL based on the URL "
                        "features it checks. Verify the website through "
                        "trusted sources before trusting it."
                    )

            else:
                with st.container(border=True):
                    st.subheader("🟢 Website Analysis Result")
                    st.success("✅ Potentially legitimate")
                    st.write(
                        "The model classified this URL as potentially "
                        "legitimate. This does not confirm that the "
                        "website is safe."
                    )

                if clean_url.lower().startswith("https://"):
                    with st.container(border=True):
                        st.subheader("🌐 Additional Website Information")

                        with st.spinner("Fetching website information..."):
                            tinyfish_data, tinyfish_error = fetch_with_tinyfish(clean_url)

                        if tinyfish_error:
                            st.warning(tinyfish_error)
                        else:
                            results = tinyfish_data.get("results", [])

                            if results:
                                page = results[0]
                                st.markdown("**📌 Page Title**")
                                st.write(page.get("title", "Not available"))

                                st.markdown("**📝 Description**")
                                st.write(page.get("description", "Not available"))

                                st.markdown("**🔗 Fetched URL**")
                                st.write(page.get("final_url", clean_url))

                                page_text = page.get("text", "")
                                if page_text:
                                    with st.expander("View page content preview"):
                                        st.write(page_text[:500])
                                else:
                                    st.info("No page content was returned.")
                            else:
                                st.info("TinyFish returned no page results.")
                else:
                    st.info(
                        "TinyFish fetching was skipped because the URL "
                        "does not use HTTPS."
                    )

                
            st.caption(
                "Prototype result only. A prediction is not a safety guarantee."
            )


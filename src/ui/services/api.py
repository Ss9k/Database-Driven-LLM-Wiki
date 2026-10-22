import requests
import streamlit as st
#BASE_URL = "http://127.0.0.1:8000"
BASE_URL = "https://armed-route-definitely-gdp.trycloudflare.com"

def health():
    return requests.get(f"{BASE_URL}/health").json()


def query(question):
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": question},
            timeout=120
        )

        # Handle quota and server errors before parsing JSON
        if response.status_code == 429:
            return {
                "answer": "⚠️ AI model quota reached. Please try again later.",
                "sources": []
            }

        if response.status_code >= 500:
            return {
                "answer": "⚠️ AI service is temporarily unavailable. Please try again later.",
                "sources": []
            }

        response.raise_for_status()

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "answer": "⚠️ Unable to process the response. Please try again later.",
                "sources": []
            }

    except requests.exceptions.Timeout:
        return {
            "answer": "⏳ The request took too long. Please try again.",
            "sources": []
        }

    except requests.exceptions.ConnectionError:
        return {
            "answer": "⚠️ Unable to connect to the AI service. Please try again later.",
            "sources": []
        }

    except requests.exceptions.RequestException:
        return {
            "answer": "⚠️ AI service is temporarily unavailable. Please try again later.",
            "sources": []
        }


def ingest(uploaded_file):
    response = requests.post(
        f"{BASE_URL}/ingest",
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/markdown",
            )
        },
        timeout=300,
    )

    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        raise RuntimeError(
            f"Ingestion failed ({response.status_code}): {detail}"
        )

    return response.json()



def projects():
    return requests.get(
        f"{BASE_URL}/projects"
    ).json()


def switch_project(name):
    return requests.post(
        f"{BASE_URL}/projects/switch",
        json={"name": name}
    ).json()


def delete_project(name):
    return requests.delete(
        f"{BASE_URL}/projects/{name}"
    ).json()

def get_health():

    response = requests.get(
        f"{BASE_URL}/health"
    )

    response.raise_for_status()

    return response.json()

def browse(category):

    return requests.get(
        f"{BASE_URL}/wiki",
        params={
            "category": category
        }
    ).json()


def get_page(category, page):

    return requests.get(
        f"{BASE_URL}/wiki/page",
        params={
            "category": category,
            "page": page
        }
    ).json()

def create_project(name):

    return requests.post(
        f"{BASE_URL}/projects/create",
        json={
            "name": name
        }
    ).json()

def get_dashboard():

    response = requests.get(
        f"{BASE_URL}/dashboard"
    )

    response.raise_for_status()

    return response.json()

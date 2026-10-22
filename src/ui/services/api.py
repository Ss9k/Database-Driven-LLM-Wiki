import requests

#BASE_URL = "http://127.0.0.1:8000"
BASE_URL = "https://clicking-county-pamela-calculator.trycloudflare.com"

def health():
    return requests.get(f"{BASE_URL}/health").json()


def query(question):
    return requests.post(
        f"{BASE_URL}/query",
        json={"question": question}
    ).json()



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

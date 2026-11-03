import requests


BASE_URL = "http://127.0.0.1:8000"


def check_response(name, response, expected_status):
    print(f"\n--- {name} ---")
    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}"
    )

    print("PASSED")


def main():
    # Test the introduction endpoint.
    response = requests.get(f"{BASE_URL}/", timeout=10)
    check_response("Introduction", response, 200)

    # Test whether the model is ready.
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    check_response("Health check", response, 200)
    assert response.json()["model_ready"] is True

    # Test translation with two different inputs.
    sentences = [
        "I am a student.",
        "I love learning new languages.",
    ]

    for sentence in sentences:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"text": sentence},
            timeout=120,
        )

        check_response(f"Translate: {sentence}", response, 200)

        result = response.json()
        assert result["input"] == sentence
        assert isinstance(result["translation"], str)
        assert result["translation"].strip()

    # Test invalid inputs.
    invalid_inputs = [
        ("Missing text", {}),
        ("Empty text", {"text": ""}),
        ("Whitespace only", {"text": "   "}),
        ("Wrong data type", {"text": 123}),
        ("Text too long", {"text": "a" * 501}),
    ]

    for name, payload in invalid_inputs:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            timeout=10,
        )

        check_response(name, response, 422)

    print("\nAll tests passed!")


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print(f"\nRequest failed: {error}")
        print("Make sure the API server is running.")
        raise SystemExit(1)
import json

def test_analyze_single_success(test_client, init_database):
    """
    GIVEN a running Flask application configured for testing
    WHEN a POST request is made to /api/analyze with a single text
    THEN check that the response is 201 CREATED and the data is correct
    """
    response = test_client.post('/api/analyze',
                                 json={"texts": ["This is a test about cars and driving."]},
                                 content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['summary'] == "This is a mock summary of the provided text, highlighting its key points and themes."
    assert data['topics'] == ["mock data", "software testing", "prototyping"]
    assert data['keywords'] == ["test", "cars"]

def test_analyze_batch_success(test_client, init_database):
    """
    GIVEN a running Flask application
    WHEN a POST request is made to /api/analyze with multiple texts
    THEN check that the response is 201 and returns a list of results
    """
    response = test_client.post('/api/analyze',
                                 json={"texts": ["First text.", "Second text about engineering."]},
                                 content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[1]['keywords'] == ["text", "engineering"]

def test_analyze_empty_input(test_client):
    """
    GIVEN a running Flask application
    WHEN a POST request is made to /api/analyze with an invalid payload
    THEN check that the response is 400 BAD REQUEST
    """
    response = test_client.post('/api/analyze', json={}, content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "Input must be a non-empty array" in data['error']

def test_analyze_llm_failure(test_client):
    """
    GIVEN a running Flask application
    WHEN a POST request is made with the special "FAIL_LLM" trigger
    THEN check that the API handles the upstream error and returns 502 BAD GATEWAY
    """
    response = test_client.post('/api/analyze',
                                 json={"texts": ["This text will FAIL_LLM."]},
                                 content_type='application/json')
    assert response.status_code == 502
    data = response.get_json()
    assert "Mock LLM service was triggered to fail" in data['error']

def test_search_functionality(test_client, init_database):
    """
    GIVEN a running Flask application with data in the database
    WHEN a GET request is made to /api/search
    THEN check that the correct analysis record is returned
    """
    test_client.post('/api/analyze',
                     json={"texts": ["This text is about the solar system and planets."]},
                     content_type='application/json')

    response = test_client.get('/api/search?topic=planets')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['keywords'] == ["text", "system", "planets"]

    response = test_client.get('/api/search?topic=prototyping')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert "prototyping" in data[0]['topics']
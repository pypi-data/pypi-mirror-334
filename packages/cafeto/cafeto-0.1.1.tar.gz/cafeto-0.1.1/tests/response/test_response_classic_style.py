from typing import List

import pytest

from cafeto import App
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.responses import ModelResponse, JSONResponse, PlainTextResponse, HTMLResponse, Response
from cafeto.dtos import GenericResponseDto

from tests.data import ModelDto, assert_model, generate_model_data


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller('/response')
    class ResponseClassicStyleController(BaseController):
        @app.get('/model-response/{seed}')
        async def model_response(self, seed: int) -> ModelDto:
            return ModelResponse(ModelDto(**generate_model_data(seed)))
        
        @app.get('/model-list-response/{seed_1}/{seed_2}')
        async def model_list_response(self, seed_1: int, seed_2: int) -> List[ModelDto]:
            return ModelResponse([
                ModelDto(**generate_model_data(seed_1)),
                ModelDto(**generate_model_data(seed_2))
            ])
        
        @app.delete('/empty-response')
        async def empty_response(self) -> None:
            return Response(status_code=204)
        
        @app.get('/json-response/{seed}')
        async def json_response(self, seed: int) -> JSONResponse:
            return JSONResponse(generate_model_data(seed))
        
        @app.get('/list-response/{seed_1}/{seed_2}')
        async def list_response(self, seed_1: int, seed_2: int) -> JSONResponse:
            return JSONResponse([generate_model_data(seed_1), generate_model_data(seed_2)])
        
        @app.get('/plain-text-response')
        async def plain_text_response(self) -> PlainTextResponse:
            return PlainTextResponse('Hello, World!')
        
        @app.get('/html-response')
        async def html_response(self) -> HTMLResponse:
            return HTMLResponse('<div>Hello, World!</div>')
        
        @app.get('/bad-request-response')
        async def bad_request_response(self) -> JSONResponse:
            return JSONResponse({'error': 'An error occurred'}, status_code=400)


    app.map_controllers()
    yield TestClient(app)


def test_model_response_classic_style(app_setup):
    client = app_setup
    seed: int = 1

    response = client.get(f'/response/model-response/{seed}')
    assert response.status_code == 200
    response = response.json()
    assert_model(response, seed)


def test_model_list_response_classic_style(app_setup):
    client = app_setup
    seed_1: int = 1
    seed_2: int = 2

    response = client.get(f'/response/model-list-response/{seed_1}/{seed_2}')
    assert response.status_code == 200
    response = response.json()
    assert_model(response[0], seed_1)
    assert_model(response[1], seed_2)


def test_empty_response_classic_style(app_setup):
    client = app_setup
    response = client.delete(f'/response/empty-response')
    assert response.status_code == 204
    assert response.text == ''


def test_json_response_classic_style(app_setup):
    client = app_setup
    seed: int = 1

    response = client.get(f'/response/json-response/{seed}')
    assert response.status_code == 200
    assert_model(response.json(), seed)

def test_list_response_classic_style(app_setup):
    client = app_setup
    seed_1: int = 1
    seed_2: int = 2

    response = client.get(f'/response/list-response/{seed_1}/{seed_2}')
    assert response.status_code == 200
    response = response.json()
    assert_model(response[0], seed_1)
    assert_model(response[1], seed_2)


def test_plain_text_response_classic_style(app_setup):
    client = app_setup
    response = client.get(f'/response/plain-text-response')
    assert response.status_code == 200
    assert response.text == 'Hello, World!'


def test_html_response_classic_style(app_setup):
    client = app_setup
    response = client.get(f'/response/html-response')
    assert response.status_code == 200
    assert response.text == '<div>Hello, World!</div>'


def test_bad_request_response_classic_style(app_setup):
    client = app_setup
    response = client.get(f'/response/bad-request-response')
    assert response.status_code == 400
    assert response.json() == {'error': 'An error occurred'}

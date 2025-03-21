import pytest
import os
import json
from unittest.mock import patch, MagicMock
from bet_lib import BET, LlmSystem, ACCEPTED_LIBRARIES

# Configure default event loop for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Fixtures
@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('TEST_API_KEY', 'test_key_123')
    monkeypatch.setenv('PRISM_API_KEY', 'prism_key_123')

@pytest.fixture
def sample_llm_system():
    return LlmSystem(
        llm_name="test-model",
        llm_api_key="test-key",
        llm_api_url="https://api.test.com"
    )

@pytest.fixture
def sample_bet():
    return BET(api_key="test-key")

# LlmSystem Tests
class TestLlmSystem:
    def test_init_with_api_key(self):
        system = LlmSystem(
            llm_name="test-model",
            llm_api_key="test-key",
            llm_api_url="https://api.test.com"
        )
        assert system.llm_name == "test-model"
        assert system.llm_api_key == "test-key"
        assert system.llm_api_url == "https://api.test.com"

    def test_init_with_env_var(self, mock_env_vars):
        system = LlmSystem(
            llm_name="test-model",
            llm_api_env="TEST_API_KEY",
            llm_api_url="https://api.test.com"
        )
        assert system.llm_api_key == "test_key_123"
    
    def test_init_with_empty_env_var(self, mock_env_vars):
       with pytest.raises(AssertionError):
            LlmSystem(
            llm_name="test-model",
            llm_api_env="EMPTY_ENV",
            llm_api_url="https://api.test.com"
        )

    def test_init_with_library(self):
        system = LlmSystem(
            llm_name="test-model",
            llm_api_key="test-key",
            library="openai"
        )
        assert system.library == "openai"

    def test_invalid_init_combination(self):
        with pytest.raises(AssertionError):
            LlmSystem(
                llm_name="test-model",
                llm_api_key="test-key",
                llm_api_env="TEST_API_KEY"
            )

    def test_invalid_library(self):
        with pytest.raises(AssertionError):
            LlmSystem(
                llm_name="test-model",
                llm_api_key="test-key",
                library="invalid_library"
            )

# BET Tests
class TestBET:
    def test_init_with_api_key(self):
        bet = BET(api_key="test-key")
        assert bet.api_key == "test-key"
        assert bet.headers == {"Authorization": "Bearer test-key"}

    def test_init_with_env_var(self, mock_env_vars):
        bet = BET()
        assert bet.api_key == "prism_key_123"

    def test_init_without_api_key(self, monkeypatch):
        monkeypatch.delenv('PRISM_API_KEY', raising=False)
        with pytest.raises(AssertionError):
            BET()

    @pytest.mark.integration  # Mark these tests as integration tests
    def test_real_auth(self):
        """Test authentication with real API key"""
        bet = BET()  # Will use PRISM_API_KEY from environment
        response = bet.test_auth()
        assert isinstance(response, list)
        assert "PRISM API key is working" in response[0]

    @pytest.mark.integration
    def test_real_profile(self):
        """Test profile retrieval with real API key"""
        bet = BET()
        response = bet.get_profile()
        assert isinstance(response, dict)
        assert "name" in response
        assert "api_keys" in response
        assert "remaining_credits" in response

    @pytest.mark.integration
    def test_real_behavior_categories(self):
        """Test listing behavior categories with real API key"""
        bet = BET()
        categories = bet.list_behavior_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0

    @pytest.mark.integration
    def test_real_check_tasks(self):
        """Test checking tasks with real API key"""
        bet = BET()
        tasks = bet.check_tasks()
        assert isinstance(tasks, list)

    # Keep the mocked tests for CI/CD and quick testing
    @pytest.mark.mock
    @patch('requests.post')
    def test_mocked_auth(self, mock_post, sample_bet):
        mock_post.return_value.json.return_value = ["PRISM API key is working"]
        response = sample_bet.test_auth()
        assert response == ["PRISM API key is working"]

    @pytest.mark.mock
    @patch('requests.get')
    def test_mocked_profile(self, mock_get, sample_bet):
        mock_data = {
            "name": "Test User",
            "api_keys": ["key1"],
            "remaining_credits": 100
        }
        mock_get.return_value.json.return_value = mock_data
        response = sample_bet.get_profile()
        assert response == mock_data

    @patch('requests.get')
    def test_check_tasks(self, mock_get, sample_bet):
        mock_data = [{"task_id": "123", "status": "completed"}]
        mock_get.return_value.json.return_value = mock_data
        response = sample_bet.check_tasks()
        assert response == mock_data

    @patch('requests.delete')
    def test_cancel_task(self, mock_delete, sample_bet):
        sample_bet.cancel_task("task_123")
        mock_delete.assert_called_once()

    @patch('requests.get')
    def test_list_behavior_categories(self, mock_get, sample_bet):
        mock_categories = ["category1", "category2"]
        mock_get.return_value.json.return_value = mock_categories
        response = sample_bet.list_behavior_categories()
        assert response == mock_categories

    def test_get_request_params(self, sample_bet, sample_llm_system):
        params = sample_bet._get_request_params(
            sample_llm_system,
            "test_behavior",
            True
        )
        assert params["llm_name"] == "test-model"
        assert params["behavior_category"] == "test_behavior"
        assert params["use_system"] is True

    @pytest.mark.asyncio
    @patch('requests.post')
    async def test_run_async(self, mock_post, sample_bet, sample_llm_system):
        mock_response = {"results": {"data": "test"}}
        mock_post.return_value.json.return_value = mock_response
        response = await sample_bet.run_async(
            sample_llm_system,
            "test_behavior"
        )
        assert response == mock_response

    @patch('requests.post')
    def test_run(self, mock_post, sample_bet, sample_llm_system):
        mock_response = {"results": {"data": "test"}}
        mock_post.return_value = mock_response
        response = sample_bet.run(
            sample_llm_system,
            "test_behavior"
        )
        assert response == mock_response

    def test_print_results(self, capsys, sample_bet):
        test_response = {
            "results": {
                "behavior_category": "test_category",
                "model": "test_model",
                "data": {
                    "system1": [{
                        "steps_to_break": 5,
                        "estimated_error": 1,
                        "use_system": True,
                        "output_sample": [["test output"]]
                    }]
                }
            }
        }
        sample_bet.print_results(test_response)
        captured = capsys.readouterr()
        assert "test_category" in captured.out
        assert "test_model" in captured.out 
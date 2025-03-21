import os
import json
import pytest
import yaml
from unittest.mock import patch, mock_open

from gru.cli import GruCommands, AgentCommands, MemoryCommands, ComponentCommands
from gru.utils.constants import TOKEN_ENV_VAR_NAME

TEST_TOKEN = "test_auth_token"
TEST_CORRELATION_ID = "test-correlation-id"


@pytest.fixture
def mock_uuid():
    with patch("uuid.uuid4") as mock:
        mock.return_value = TEST_CORRELATION_ID
        yield mock


@pytest.fixture
def gru_commands():
    return GruCommands()


@pytest.fixture
def agent_commands():
    return AgentCommands(auth_token=TEST_TOKEN)


@pytest.fixture
def memory_commands():
    return MemoryCommands(auth_token=TEST_TOKEN)


@pytest.fixture
def component_commands():
    return ComponentCommands(auth_token=TEST_TOKEN)


@pytest.fixture
def mock_config_file():
    config_data = {
        "agent_name": "Test Agent",
        "task_server_name": "test-task-server",
        "checkpoint_db_name": "test-checkpoint-db",
        "replicas": 1,
        "iam_role_arn": "test-iam-role",
        "vector_db_name": "test-vector-db",
    }

    with patch(
        "builtins.open", mock_open(read_data=yaml.dump(config_data))
    ) as mock_file:
        yield mock_file


@pytest.fixture
def mock_memory_file():
    memory_data = {
        "collection_name": "test_collection",
        "text": "Test memory text",
        "data": {"key": "value"},
        "memory_id": "test-memory-id",
    }

    with patch(
        "builtins.open", mock_open(read_data=json.dumps(memory_data))
    ) as mock_file:
        yield mock_file


class TestComponentCommands:
    def test_get_token_with_provided_token(self, component_commands):
        """Test that get_token returns the provided token"""
        assert component_commands.get_token() == TEST_TOKEN

    def test_get_token_from_env(self):
        """Test that get_token falls back to environment variable"""
        with patch.dict(os.environ, {TOKEN_ENV_VAR_NAME: "env_token"}):
            component = ComponentCommands()
            assert component.get_token() == "env_token"

    @patch("gru.cli.component_setup")
    def test_setup(self, mock_setup, component_commands, mock_uuid):
        """Test component setup command"""
        mock_setup.return_value = "Component setup successful"

        result = component_commands.setup("test-cluster", "config.yaml")

        assert result == "Component setup successful"
        mock_setup.assert_called_once_with(
            TEST_CORRELATION_ID, "test-cluster", "config.yaml", TEST_TOKEN
        )

    @patch("gru.cli.component_setup")
    def test_setup_file_not_found(self, mock_setup, component_commands):
        """Test component setup with file not found error"""
        mock_setup.side_effect = FileNotFoundError()

        result = component_commands.setup("test-cluster", "not-found.yaml")

        assert "Error: not-found.yaml file not found." in result
        mock_setup.assert_called_once()


class TestAgentCommands:
    def test_get_token_with_provided_token(self, agent_commands):
        """Test that get_token returns the provided token"""
        assert agent_commands.get_token() == TEST_TOKEN

    @patch("gru.cli.ai_agent_templates_setup")
    def test_create_bootstrap(self, mock_bootstrap, agent_commands):
        """Test create bootstrap command"""
        result = agent_commands.create_bootstrap()

        assert "Agent bootstrap project created successfully" in result
        mock_bootstrap.assert_called_once()

    @patch("gru.cli.register_agent")
    def test_register(self, mock_register, agent_commands, mock_config_file, mock_uuid):
        """Test register agent command"""
        mock_register.return_value = "Agent registered successfully"

        result = agent_commands.register(
            "agent_folder", "test-cluster", "test-image", "test-pull-secret"
        )

        assert result == "Agent registered successfully"
        mock_register.assert_called_once_with(
            TEST_CORRELATION_ID,
            TEST_TOKEN,
            "agent_folder",
            "test-cluster",
            "test-image",
            "test-pull-secret",
        )

    @patch("gru.cli.deploy_agent")
    def test_deploy(self, mock_deploy, agent_commands, mock_uuid):
        """Test deploy agent command"""
        mock_deploy.return_value = "Agent deployed successfully"

        result = agent_commands.deploy("test-agent")

        assert result == "Agent deployed successfully"
        mock_deploy.assert_called_once_with(
            TEST_CORRELATION_ID, TEST_TOKEN, "test-agent"
        )

    @patch("gru.cli.update_agent")
    def test_update(self, mock_update, agent_commands, mock_config_file, mock_uuid):
        """Test update agent command"""
        mock_update.return_value = "Agent updated successfully"

        result = agent_commands.update("agent_folder", "new-image", "new-pull-secret")

        assert result == "Agent updated successfully"
        mock_update.assert_called_once_with(
            TEST_CORRELATION_ID,
            TEST_TOKEN,
            "agent_folder",
            "new-image",
            "new-pull-secret",
        )

    @patch("gru.cli.delete_agent")
    def test_delete(self, mock_delete, agent_commands, mock_uuid):
        """Test delete agent command"""
        mock_delete.return_value = "Agent deleted successfully"

        result = agent_commands.delete("test-agent")

        assert result == "Agent deleted successfully"
        mock_delete.assert_called_once_with(
            TEST_CORRELATION_ID, TEST_TOKEN, "test-agent"
        )

    @patch("gru.cli.read_prompt_file")
    @patch("gru.cli.prompt_agent")
    def test_prompt(self, mock_prompt, mock_read_file, agent_commands):
        """Test prompt agent command"""
        mock_read_file.return_value = {"prompt": "Test prompt"}
        mock_prompt.return_value = "Prompt sent successfully"

        result = agent_commands.prompt("test-agent", "prompt.json")

        assert result == "Prompt sent successfully"
        mock_read_file.assert_called_once_with("prompt.json")
        mock_prompt.assert_called_once_with(
            "test-agent", {"prompt": "Test prompt"}, TEST_TOKEN
        )

    @patch("gru.cli.converse_agent")
    def test_converse(self, mock_converse, agent_commands):
        """Test converse agent command"""
        mock_converse.return_value = "Conversation Stopped"

        result = agent_commands.converse("test-agent")

        assert result == "Conversation Stopped"
        mock_converse.assert_called_once_with(TEST_TOKEN, "test-agent", None)

    @patch("gru.cli.converse_agent")
    def test_converse_with_id(self, mock_converse, agent_commands):
        """Test converse agent command with conversation ID"""
        mock_converse.return_value = "Conversation Stopped"

        result = agent_commands.converse("test-agent", "test-conversation")

        assert result == "Conversation Stopped"
        mock_converse.assert_called_once_with(
            TEST_TOKEN, "test-agent", "test-conversation"
        )


class TestMemoryCommands:
    def test_get_token_with_provided_token(self, memory_commands):
        """Test that get_token returns the provided token"""
        assert memory_commands.get_token() == TEST_TOKEN

    @patch("gru.cli.memory_insert")
    def test_insert(self, mock_insert, memory_commands, mock_memory_file, mock_uuid):
        """Test memory insert command"""
        mock_insert.return_value = "Memory inserted successfully"

        result = memory_commands.insert("test-agent", "memory_data.json")

        assert result == "Memory inserted successfully"
        mock_insert.assert_called_once_with(
            TEST_CORRELATION_ID, TEST_TOKEN, "test-agent", "memory_data.json"
        )

    @patch("gru.cli.memory_update")
    def test_update(self, mock_update, memory_commands, mock_memory_file, mock_uuid):
        """Test memory update command"""
        mock_update.return_value = "Memory updated successfully"

        result = memory_commands.update("test-agent", "memory_data.json")

        assert result == "Memory updated successfully"
        mock_update.assert_called_once_with(
            TEST_CORRELATION_ID, TEST_TOKEN, "test-agent", "memory_data.json"
        )

    @patch("gru.cli.memory_delete")
    def test_delete(self, mock_delete, memory_commands, mock_uuid):
        """Test memory delete command"""
        mock_delete.return_value = "Memory deleted successfully"

        result = memory_commands.delete(
            "test-agent", "test-memory-id", "test-collection"
        )

        assert result == "Memory deleted successfully"
        mock_delete.assert_called_once_with(
            TEST_CORRELATION_ID,
            TEST_TOKEN,
            "test-agent",
            "test-memory-id",
            "test-collection",
        )


class TestErrorHandling:
    @patch("gru.cli.deploy_agent")
    def test_deploy_value_error(self, mock_deploy, agent_commands):
        """Test that value errors are handled properly"""
        mock_deploy.side_effect = ValueError("Invalid agent name")

        result = agent_commands.deploy("invalid-agent")

        assert "Invalid agent name" in result
        mock_deploy.assert_called_once()

    @patch("gru.cli.deploy_agent")
    def test_deploy_unexpected_error(self, mock_deploy, agent_commands, mock_uuid):
        """Test that unexpected errors are handled properly"""
        mock_deploy.side_effect = Exception("Unexpected error")

        result = agent_commands.deploy("test-agent")

        assert (
            f"An unexpected error occured. Correlation ID: {TEST_CORRELATION_ID}"
            in result
        )
        mock_deploy.assert_called_once()

    @patch("gru.cli.read_prompt_file")
    def test_prompt_file_not_found(self, mock_read_file, agent_commands):
        """Test prompt with file not found error"""
        mock_read_file.side_effect = FileNotFoundError("File not found")

        result = agent_commands.prompt("test-agent", "not-found.json")

        assert "File error: File not found" in result
        mock_read_file.assert_called_once()

    @patch("gru.cli.read_prompt_file")
    def test_prompt_json_error(self, mock_read_file, agent_commands):
        """Test prompt with JSON decode error"""
        mock_read_file.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        result = agent_commands.prompt("test-agent", "invalid.json")

        assert "JSON error" in result
        mock_read_file.assert_called_once()


class TestEnvironmentToken:
    def test_environment_token_fallback(self):
        """Test that token falls back to environment when not provided"""
        with patch.dict(os.environ, {TOKEN_ENV_VAR_NAME: "env_token"}):
            agent_cmd = AgentCommands()  # No token provided, should use environment

            assert agent_cmd.get_token() == "env_token"
            assert agent_cmd.memory.get_token() == "env_token"

    def test_missing_environment_token(self):
        """Test error when token not provided and not in environment"""
        with patch.dict(os.environ, {}, clear=True):  # Clear environment variables
            agent_cmd = AgentCommands()  # No token provided or in environment

            with pytest.raises(
                ValueError, match=f"Environment variable {TOKEN_ENV_VAR_NAME} missing"
            ):
                agent_cmd.get_token()

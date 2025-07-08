"""
Centralized configuration for the Autonomous App-Writing Agent.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- LLM Configuration ---
# Provider can be 'OpenAI', 'Anthropic', 'Google', etc.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "OpenAI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Specific models for different tasks
# It's wise to use different models for different capabilities, e.g., a powerful model for reasoning
# and a faster, cheaper model for summarization or simple generation.
MODEL_PRIMARY_REASONING = os.getenv("MODEL_PRIMARY_REASONING", "gpt-4-turbo")
MODEL_SECONDARY_AGENT = os.getenv("MODEL_SECONDARY_AGENT", "gpt-3.5-turbo")
MODEL_CODE_GENERATION = os.getenv("MODEL_CODE_GENERATION", "gpt-4-turbo") # Or a fine-tuned code model
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING", "text-embedding-3-small")

# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") # e.g., DEBUG, INFO, WARNING, ERROR
LOG_FILE = os.getenv("LOG_FILE", "agent_activity.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# --- Project & File Configuration ---
PROJECTS_DIR = os.getenv("PROJECTS_DIR", "generated_projects")
STATE_DB_PATH = os.getenv("STATE_DB_PATH", "project_tracker/agent_state.db")

# --- VSM Daemon Configuration ---
S4_INTELLIGENCE_DAEMON_INTERVAL_SECONDS = int(os.getenv("S4_INTELLIGENCE_DAEMON_INTERVAL_SECONDS", 3600)) # 1 hour
S5_POLICY_DAEMON_INTERVAL_SECONDS = int(os.getenv("S5_POLICY_DAEMON_INTERVAL_SECONDS", 86400)) # 24 hours

# --- Feature Flags ---
# Allows enabling/disabling features without code changes.
ENABLE_HUMAN_IN_THE_LOOP = os.getenv("ENABLE_HUMAN_IN_THE_LOOP", "True").lower() == "true"
ENABLE_S4_DAEMON = os.getenv("ENABLE_S4_DAEMON", "True").lower() == "true"
ENABLE_S5_DAEMON = os.getenv("ENABLE_S5_DAEMON", "True").lower() == "true"

# --- Security & Compliance ---
# Example: path to a file with security policies or checklists for S3* audit
SECURITY_CHECKLIST_PATH = os.getenv("SECURITY_CHECKLIST_PATH", "core/security_checklist.json")

"""
Centralized configuration for the Autonomous App-Writing Agent.
"""

import os

# --- LLM Configuration ---
# It's recommended to use environment variables for API keys.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")  # e.g., "openai", "anthropic", "google"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default model names
DEFAULT_MAIN_MODEL = "gemini-2.5-pro"
DEFAULT_FAST_MODEL = "gemini-2.5-pro" # Or another fast Gemini model
DEFAULT_VISION_MODEL = "gemini-2.5-pro" # Gemini has vision capabilities

# --- Agent Configuration ---
MAX_ITERATIONS = 25  # Max iterations for the main development loop in S3
ALLOW_INTERIM_FEEDBACK = True  # Flag to allow user feedback during development

# --- Logging Configuration ---
LOG_LEVEL = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"
LOG_FILE = "agent_activity.log"

# --- File Paths ---
PROJECTS_DIR = "generated_projects"
KNOWLEDGE_BASE_DIR = "vsm_knowledge_base"
S5_POLICY_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "system5_policies.json")
S4_KNOWLEDGE_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "system4_knowledge.json")

# --- Feature Flags ---
ENABLE_S4_DAEMON_SCANNING = True
ENABLE_S5_DAEMON_ADAPTATION = True

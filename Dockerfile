FROM python:3.12-slim

WORKDIR /app

# Install uv for package management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies using uv
RUN uv sync

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8222

# Command to run the application
CMD ["uv", "run", "uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8222"]

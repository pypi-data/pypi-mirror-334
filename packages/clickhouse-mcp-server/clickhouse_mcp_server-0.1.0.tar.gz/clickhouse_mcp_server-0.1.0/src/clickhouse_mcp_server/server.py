import json
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, List, Optional

from clickhouse_driver import Client
from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP


class ClickHouseServerError(Exception):
    """Base exception for ClickHouse server errors"""

    pass


class ConnectionError(ClickHouseServerError):
    """Raised when there's an issue with the database connection"""
    pass


class QueryError(ClickHouseServerError):
    """Raised when there's an issue executing a query"""
    pass


@dataclass
class ClickHouseContext:
    """Context for ClickHouse connection"""
    host: str
    port: int
    user: str
    password: str
    database: Optional[str]
    readonly: bool
    client: Optional[Client] = None

    def ensure_connected(self) -> None:
        """Ensure database connection is available, connecting lazily if needed"""
        if not self.client:
            settings = {
                'host': self.host,
                'port': self.port,
                'user': self.user,
                'password': self.password,
                # Convert bool to int
                'settings': {'readonly': 1 if self.readonly else 0}
            }
            if self.database:
                settings['database'] = self.database

            try:
                self.client = Client(**settings)
                # Test connection
                self.client.execute('SELECT 1')
            except Exception as e:
                raise ConnectionError(
                    f"Failed to connect to database: {str(e)}")


class QueryExecutor:
    """Handles ClickHouse query execution and result processing"""

    def __init__(self, context: ClickHouseContext):
        self.context = context

    def _format_datetime(self, value: Any) -> Any:
        """Format datetime values to string"""
        return value.strftime('%Y-%m-%d %H:%M:%S') if hasattr(value, 'strftime') else value

    def _process_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single row of results"""
        return {key: self._format_datetime(value) for key, value in row.items()}

    def _is_use_statement(self, query: str) -> bool:
        """Check if the query is a USE statement"""
        return query.strip().upper().startswith('USE')

    def execute_single_query(self, query: str) -> Dict[str, Any]:
        """Execute a single query and return results"""
        self.context.ensure_connected()

        try:
            # Handle USE statements
            if self._is_use_statement(query):
                db_name = query.strip().split()[-1].strip('`').strip()
                self.context.database = db_name
                self.context.client.execute(f'USE {db_name}')
                return {"message": f"Switched to database: {db_name}"}

            # Execute query
            result = self.context.client.execute(query, with_column_types=True)

            if not result:
                return {"affected_rows": 0}

            rows, columns = result
            if not rows:
                return {"affected_rows": 0}

            # Convert rows to dictionaries
            column_names = [col[0] for col in columns]
            results = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                results.append(self._process_row(row_dict))

            return results if len(results) > 0 else {"affected_rows": 0}

        except Exception as e:
            raise QueryError(f"Error executing query: {str(e)}")

    def execute_multiple_queries(self, query: str) -> List[Dict[str, Any]]:
        """Execute multiple queries and return results"""
        queries = [q.strip() for q in query.split(';') if q.strip()]
        results = []

        for single_query in queries:
            try:
                result = self.execute_single_query(single_query)
                results.append(result)
            except QueryError as e:
                results.append({"error": str(e)})

        return results


def get_env_vars() -> tuple[str, int, str, str, Optional[str], bool]:
    """Get ClickHouse connection settings from environment variables

    Returns:
        Tuple of (host, port, user, password, database, readonly)
    """
    load_dotenv()

    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", "9000"))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DATABASE")  # Optional
    readonly = os.getenv("CLICKHOUSE_READONLY", "0") in ("1", "true", "True")

    return host, port, user, password, database, readonly


@asynccontextmanager
async def clickhouse_lifespan(server: FastMCP) -> AsyncIterator[ClickHouseContext]:
    """ClickHouse connection lifecycle manager"""
    # Get connection settings from environment variables
    host, port, user, password, database, readonly = get_env_vars()

    # Initialize context without connecting
    ctx = ClickHouseContext(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        readonly=readonly,
        client=None  # Don't connect immediately
    )

    try:
        yield ctx
    finally:
        if ctx.client:
            # ClickHouse driver doesn't require explicit connection closing
            ctx.client = None


# Create MCP server instance
mcp = FastMCP("ClickHouse Explorer", lifespan=clickhouse_lifespan)


def _get_executor(ctx: Context) -> QueryExecutor:
    """Helper function to get QueryExecutor from context"""
    clickhouse_ctx = ctx.request_context.lifespan_context
    return QueryExecutor(clickhouse_ctx)


@mcp.tool()
def connect_database(database: str, ctx: Context) -> str:
    """Connect to a specific ClickHouse database"""
    try:
        executor = _get_executor(ctx)
        result = executor.execute_single_query(f"USE {database}")
        return json.dumps(result, indent=2)
    except (ConnectionError, QueryError) as e:
        return str(e)


@mcp.tool()
def execute_query(query: str, ctx: Context) -> str:
    """Execute ClickHouse queries"""
    try:
        executor = _get_executor(ctx)
        results = executor.execute_multiple_queries(query)

        if len(results) == 1:
            return json.dumps(results[0], indent=2)
        return json.dumps(results, indent=2)
    except (ConnectionError, QueryError) as e:
        return str(e)


if __name__ == "__main__":
    mcp.run()

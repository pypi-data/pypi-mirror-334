#### __init__.py

"""
Módulo para gerenciamento de conexões com bancos de dados.
Suporta diversos tipos de bancos via ODBC ou SQLAlchemy.
"""

__version__ = "0.1.0"

# Importar funções principais
from .connection import (
    conectar_banco, 
    executar_query, 
    listar_tabelas,
    resource_path,
    carregar_env,
    get_connection  # Para compatibilidade com código legado
)

# Alias para compatibilidade
from .connection import conectar_banco as connect_db
from .connection import executar_query as execute_query
from .connection import listar_tabelas as list_tables
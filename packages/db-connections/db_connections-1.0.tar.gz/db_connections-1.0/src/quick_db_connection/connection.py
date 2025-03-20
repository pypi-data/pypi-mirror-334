"""
Módulo para gerenciamento de conexões com bancos de dados.
Versão otimizada que utiliza apenas dois tipos de conexão:
1. pyodbc para bancos via ODBC
2. SQLAlchemy para todos os outros casos
Com suporte a ambientes empacotados pelo PyInstaller.
"""

import os
import sys
import pandas as pd
from typing import Dict, Optional, Union, Any, List
from pathlib import Path

def resource_path(relative_path: Union[str, Path]) -> str:
    """
    Retorna o caminho absoluto para um recurso (como um arquivo .env),
    mesmo quando o código for empacotado (por exemplo, com PyInstaller).

    Caso o código esteja sendo executado a partir de um executável criado com o PyInstaller, 
    utiliza 'sys._MEIPASS' como base. Caso contrário, utiliza o caminho absoluto do diretório atual.

    Parâmetros:
        relative_path (str ou Path): Caminho relativo do recurso que se deseja acessar.

    Retorno:
        str: Caminho absoluto para o recurso.
    """
    try:
        # Quando empacotado com PyInstaller, sys._MEIPASS é o diretório temporário onde os arquivos são extraídos.
        base_path = sys._MEIPASS
    except AttributeError:
        # Caso não esteja empacotado, utiliza o diretório atual.
        base_path = os.path.abspath(".")
    
    # Converte Path para string, se necessário
    if isinstance(relative_path, Path):
        relative_path = str(relative_path)
    
    return os.path.join(base_path, relative_path)

def carregar_env(env_local: str = "config", usar_resource_path: bool = False) -> Dict[str, str]:
    """
    Carrega variáveis de ambiente de um arquivo .env
    
    Parâmetros:
    -----------
    env_local : str, default="config"
        Caminho para o diretório onde está o arquivo .env
    usar_resource_path : bool, default=False
        Se True, usa a função resource_path para resolver o caminho do arquivo .env,
        útil para executáveis criados com PyInstaller
        
    Retorna:
    --------
    Dict[str, str]
        Dicionário com as variáveis carregadas
    """
    try:
        from dotenv import load_dotenv
        
        # Define os caminhos a serem testados
        env_caminhos = []
        
        # Função para processar caminhos conforme usar_resource_path
        def processar_caminho(caminho):
            if usar_resource_path:
                return Path(resource_path(caminho))
            else:
                return Path(caminho)
        
        # Lista de possíveis localizações do arquivo .env
        env_caminhos_base = [
            Path(env_local) / ".env",
            Path(env_local) / "env",
            Path(env_local),
            Path(".") / env_local / ".env",
            Path(".") / env_local / "env",
            Path(".env"),
        ]
        
        # Processa cada caminho conforme configuração
        for caminho in env_caminhos_base:
            env_caminhos.append(processar_caminho(caminho))
        
        # Tenta cada caminho até encontrar um arquivo válido
        for caminho in env_caminhos:
            if caminho.exists():
                load_dotenv(dotenv_path=caminho)
                # Retorna dicionário com versões originais e lowercase das variáveis
                return {
                    key: val for key, val in os.environ.items()
                } | {
                    key.lower(): val for key, val in os.environ.items()
                }
        
        # Se chegou aqui, não encontrou um arquivo .env válido
        print(f"Aviso: Arquivo .env não encontrado em {env_local}. Usando variáveis de ambiente do sistema.")
        return {key: val for key, val in os.environ.items()}
    
    except ImportError:
        print("Aviso: python-dotenv não encontrado. Usando variáveis de ambiente do sistema.")
        print("Para carregar do arquivo .env, instale: pip install python-dotenv")
        return {key: val for key, val in os.environ.items()}

def conectar_banco(
    db: str,
    connection_string: Optional[str] = None,
    env_local: str = "config",
    env_var: Optional[str] = None,
    usar_resource_path: bool = False
) -> Any:
    """
    Conecta a um banco de dados usando uma connection string.
    Versão otimizada que usa apenas pyodbc ou SQLAlchemy.
    
    Parâmetros:
    -----------
    db : str
        Tipo de banco de dados ('pyodbc', 'mssql', 'sqlite', 'postgresql', etc.)
    connection_string : str, opcional
        String de conexão completa. Se None, tentará obter de env_var.
    env_local : str, default="config"
        Caminho para o diretório onde está o arquivo .env
    env_var : str, opcional
        Nome da variável de ambiente que contém a connection string.
        Se não fornecida, usa 'conexao_{db}'.
    usar_resource_path : bool, default=False
        Se True, usa a função resource_path para resolver o caminho do arquivo .env,
        útil para executáveis criados com PyInstaller
        
    Retorna:
    --------
    Connection ou Engine
        Objeto de conexão ou engine conforme o tipo de banco especificado
    """
    # Se a connection string não foi fornecida, tenta obter do env
    if connection_string is None:
        # Se env_var não foi especificada, usa o padrão
        if env_var is None:
            env_var = f"conexao_{db}"
        
        # Carrega variáveis de ambiente
        env_vars = carregar_env(env_local, usar_resource_path)
        
        # Tenta obter a connection string do ambiente
        connection_string = env_vars.get(env_var)
        
        if not connection_string:
            raise ValueError(f"Connection string não fornecida e variável '{env_var}' não encontrada no ambiente")
    
    # Normaliza o tipo de banco para lowercase
    db_tipo = db.lower()
    
    # Caso 1: ODBC (pyodbc) para SQL Server, Domínio e outros bancos ODBC
    if db_tipo in ['pyodbc', 'mssql', 'sql_server', 'sqlserver', 'dominio', 'odbc']:
        try:
            import pyodbc
            return pyodbc.connect(connection_string)
        except ImportError:
            raise ImportError("pyodbc não encontrado. Instale-o usando: pip install pyodbc")
    
    # Caso 2: SQLAlchemy para todos os outros bancos
    else:
        try:
            from sqlalchemy import create_engine
            
            # Ajusta a string de conexão conforme o tipo de banco, se necessário
            if db_tipo == 'sqlite' and not connection_string.startswith('sqlite:///'):
                # Para SQLite, adiciona o prefixo se não existir
                if usar_resource_path and not os.path.isabs(connection_string):
                    # Usa resource_path para resolver o caminho absoluto do banco SQLite
                    connection_string = resource_path(connection_string)
                engine_url = f"sqlite:///{connection_string}"
            elif db_tipo == 'mysql' and not connection_string.startswith(('mysql://', 'mysql+pymysql://')):
                # Para MySQL, adiciona o prefixo com pymysql se não existir
                engine_url = f"mysql+pymysql://{connection_string}"
            elif db_tipo in ['postgresql', 'postgres'] and not connection_string.startswith(('postgresql://', 'postgres://')):
                # Para PostgreSQL, adiciona o prefixo se não existir
                engine_url = f"postgresql://{connection_string}"
            else:
                # Usa a string como está para outros casos
                engine_url = connection_string
                
            return create_engine(engine_url)
        except ImportError:
            raise ImportError("SQLAlchemy não encontrado. Instale-o usando: pip install sqlalchemy")

def executar_query(
    query: str,
    db: str = 'dominio',
    connection_string: Optional[str] = None,
    env_local: str = "config",
    env_var: Optional[str] = None,
    usar_pandas: bool = True,
    params: Optional[Dict] = None,
    parse_dates: Optional[List[str]] = None,
    usar_resource_path: bool = False
) -> Union[pd.DataFrame, List[Dict]]:
    """
    Executa uma query SQL e retorna o resultado como DataFrame ou lista.
    
    Parâmetros:
    -----------
    query : str
        Query SQL a ser executada
    db : str, default='dominio'
        Tipo de banco de dados ('pyodbc', 'mysql', 'sqlite', etc.)
    connection_string : str, opcional
        String de conexão. Se None, tentará obter do env.
    env_local : str, default="config"
        Caminho para o diretório onde está o arquivo .env
    env_var : str, opcional
        Nome da variável de ambiente com a connection string.
        Se não fornecida, usa 'conexao_{db}'.
    usar_pandas : bool, default=True
        Se True, retorna resultado como DataFrame; se False, como lista de dicionários
    params : dict, opcional
        Parâmetros a serem passados para a query
    parse_dates : list, opcional
        Lista de colunas a serem convertidas para datetime (apenas com pandas)
    usar_resource_path : bool, default=False
        Se True, usa a função resource_path para resolver o caminho do arquivo .env,
        útil para executáveis criados com PyInstaller
        
    Retorna:
    --------
    pd.DataFrame ou List[Dict]
        Resultado da query
    """
    # Obtém a conexão
    conn = conectar_banco(
        db=db,
        connection_string=connection_string,
        env_local=env_local,
        env_var=env_var,
        usar_resource_path=usar_resource_path
    )
    
    # Verificar se é uma conexão SQLAlchemy ou pyodbc
    is_sqlalchemy = not db.lower() in ['pyodbc', 'mssql', 'sql_server', 'sqlserver', 'dominio', 'odbc']
    
    try:
        if usar_pandas:
            # Usa pandas para executar a query (funciona com ambos os tipos de conexão)
            return pd.read_sql(
                sql=query, 
                con=conn, 
                params=params,
                parse_dates=parse_dates
            )
        else:
            # Execução direta depende do tipo de conexão
            if is_sqlalchemy:
                # SQLAlchemy 2.0+ requer uso de connection() e text()
                from sqlalchemy import text
                with conn.connect() as connection:
                    result = connection.execute(text(query), params or {})
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in result.fetchall()]
            else:
                # Conexão pyodbc
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Obtém os nomes das colunas
                columns = [column[0] for column in cursor.description] if cursor.description else []
                
                # Obtém os resultados
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                cursor.close()
                return results
    
    finally:
        # Fecha a conexão pyodbc
        if not is_sqlalchemy and hasattr(conn, 'close'):
            conn.close()
        # SQLAlchemy gerencia automaticamente a conexão

def listar_tabelas(
    db: str = 'sqlite',
    connection_string: Optional[str] = None,
    env_local: str = "config",
    env_var: Optional[str] = None,
    usar_resource_path: bool = False
) -> List[str]:
    """
    Lista todas as tabelas disponíveis no banco de dados.
    
    Parâmetros:
    -----------
    db : str, default='sqlite'
        Tipo de banco de dados ('pyodbc', 'mysql', 'sqlite', etc.)
    connection_string : str, opcional
        String de conexão. Se None, tentará obter do env.
    env_local : str, default="config"
        Caminho para o diretório onde está o arquivo .env
    env_var : str, opcional
        Nome da variável de ambiente com a connection string.
    usar_resource_path : bool, default=False
        Se True, usa a função resource_path para resolver o caminho do arquivo .env,
        útil para executáveis criados com PyInstaller
        
    Retorna:
    --------
    List[str]
        Lista com os nomes das tabelas
    """
    # Obtém a conexão
    conn = conectar_banco(
        db=db,
        connection_string=connection_string,
        env_local=env_local,
        env_var=env_var,
        usar_resource_path=usar_resource_path
    )
    
    # Verificar se é uma conexão SQLAlchemy ou pyodbc
    is_sqlalchemy = not db.lower() in ['pyodbc', 'mssql', 'sql_server', 'sqlserver', 'dominio', 'odbc']
    
    try:
        if is_sqlalchemy:
            # SQLAlchemy - usar inspetor
            from sqlalchemy import inspect
            inspector = inspect(conn)
            return inspector.get_table_names()
        else:
            # Conexão pyodbc - depende do tipo de banco
            cursor = conn.cursor()
            db_tipo = db.lower()
            
            if db_tipo in ['mssql', 'sql_server', 'sqlserver']:
                # SQL Server
                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            elif db_tipo == 'dominio':
                # Domínio geralmente é SQL Server
                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            else:
                # Genérico para outros bancos ODBC
                try:
                    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
                except:
                    # Fallback
                    cursor.tables()
                    return [t.table_name for t in cursor.fetchall() if t.table_type == 'TABLE']
            
            # Obtém os resultados
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
    finally:
        # Fecha a conexão pyodbc
        if not is_sqlalchemy and hasattr(conn, 'close'):
            conn.close()

def get_connection(db, env_local="config", usar_resource_path=False):
    """
    Função simplificada para compatibilidade com código legado.
    Retorna uma conexão com o banco de dados especificado.
    
    Parâmetros:
    -----------
    db : str
        Nome do banco de dados ('dominio', 'mysql', etc.)
    env_local : str, default="config"
        Caminho para o diretório onde está o arquivo .env
    usar_resource_path : bool, default=False
        Se True, usa a função resource_path para resolver o caminho do arquivo .env,
        útil para executáveis criados com PyInstaller
        
    Retorna:
    --------
    Connection
        Conexão ativa com o banco
    """
    return conectar_banco(db=db, env_local=env_local, usar_resource_path=usar_resource_path)
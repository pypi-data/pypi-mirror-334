from contextvars import ContextVar
import json
import os

from asgiref.sync import async_to_sync
import django
from django.apps import apps
from django.contrib.auth.hashers import check_password
from django.db import connections
from django.db.models import Q
from redis import asyncio as aioredis

from ..exception import HTTPException

from settings import DEFAULT_DATABASE, TENANT_ACCOUNT_MODEL, TENANT_USER_MODEL, TENANT_DB_PREFIX

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_DB = os.environ['REDIS_DB']


if not apps.ready:
    DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE')
    if not DJANGO_SETTINGS_MODULE:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    django.setup()


class ACCOUNT_STATUS():
    """Situações possíveis do banco de dados no sistema.

    Attributes:
        ACTIVE (int): Conta ativa com todos os recursos do sistema liberados.
        CREATING_DATABASE (int): A conta se encontra em processo de criação.
        DATABASE_CREATION_ERROR (int): Ocorreu um erro na criação da conta.
        UPDATING_DATABASE (int): O database está em processo de migração
        DELETED (int): Conta removida e que não permite mais acesso ao sistema.
        WAITING_DELETION (int): Conta marcada para remoção futura, pelo script.
        OPTIONS (dict): Dicionário com os status e seus respectivos nomes.
        CHOICES (tuple): Tupla com status e nomes, para relação com os models.

    """
    ACTIVE = 1
    DISABLED = 2
    FREE = 3
    DELETED = 4
    PAUSED = 5
    CREATING_DATABASE = 6
    DATABASE_CREATION_ERROR = 7

    OPTIONS = {
        ACTIVE: 'Active',
        DISABLED: 'Disabled',
        FREE: 'Waiting allocation',
        DELETED: 'Deleted',
        PAUSED: 'Paused',
        CREATING_DATABASE: 'Creating database',
        DATABASE_CREATION_ERROR: 'Database creation error',
    }
    CHOICES = tuple(OPTIONS.items())


try:
    tenant_model = apps.get_model(TENANT_USER_MODEL)
except Exception:
    TENANT_USER_MODEL = None
    tenant_model = None


try:
    account_model = apps.get_model(TENANT_ACCOUNT_MODEL)
except Exception:
    TENANT_ACCOUNT_MODEL = None
    account_model = None

db_state = ContextVar("db_state", default='default')


async def save_connection(account):
    account_db = f'{TENANT_DB_PREFIX}_{account.id}'
    db_state.set(account_db)

    cache_key = f'{TENANT_DB_PREFIX}:connections:{account.id}'
    redis = await aioredis.Redis(
        host=REDIS_SERVER, db=REDIS_DB, decode_responses=True
    ).client()
    connection = await redis.get(cache_key)

    if not connection:
        connection = {
            'ATOMIC_REQUESTS': False,
            'ENGINE': 'django.db.backends.mysql',
            'NAME': account_db,
            'HOST': account.db.host,
            'USER': account.db.user,
            'PASSWORD': account.db.password,
            'CONN_MAX_AGE': 0,
            'CONN_HEALTH_CHECKS': False,
            'TIME_ZONE': None,
            'PORT': '',
            'AUTOCOMMIT': True,
            'OPTIONS': {
                'use_unicode': True,
                'charset': 'utf8mb4',
                'connect_timeout': 120,
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1"
            },
        }
        await redis.set(f'{TENANT_DB_PREFIX}:connections:{account.id}', json.dumps(connection))

    else:
        connection = json.loads(connection)

    await redis.close()
    await redis.connection_pool.disconnect()

    connections.databases[account_db] = connection


async def set_default(id):
    cache_key = f'{TENANT_DB_PREFIX}:connections:{id}'
    redis = await aioredis.Redis(
        host=REDIS_SERVER, db=REDIS_DB, decode_responses=True
    ).client()
    connection = await redis.get(cache_key)

    if not connection:
        account = await account_model.objects.filter(
            id=id,
        ).select_related('db').afirst()
        connection = {
            'ATOMIC_REQUESTS': False,
            'ENGINE': 'django.db.backends.mysql',
            'NAME': f'{TENANT_DB_PREFIX}_{id}',
            'HOST': account.db.host,
            'USER': account.db.user,
            'PASSWORD': account.db.password,
            'CONN_MAX_AGE': 0,
            'CONN_HEALTH_CHECKS': False,
            'TIME_ZONE': None,
            'PORT': '',
            'AUTOCOMMIT': True,
            'OPTIONS': {
                'use_unicode': True,
                'charset': 'utf8mb4',
                'connect_timeout': 120,
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1"
            },
        }
    else:
        connection = json.loads(connection)

    await redis.close()
    await redis.connection_pool.disconnect()

    connections.databases['default'] = connection


async def unset_default(id):
    connections.databases['default'] = DEFAULT_DATABASE


def get_tenant():
    account_db = db_state.get()
    if account_db:
        return account_db.split('_')[1]
    return account_db


async def aset_tenant(id):
    if id:
        account_db = f'{TENANT_DB_PREFIX}_{id}'
    else:
        account_db = 'default'

    if account_db not in connections.databases:
        account = await account_model.objects.filter(
            id=id,
        ).select_related('db').afirst()

        if not account:
            raise HTTPException(400, 'Missing account')

        await save_connection(account)

    db_state.set(account_db)
    return account_db


def set_tenant(id):
    sync = async_to_sync(aset_tenant)
    return sync(id)


async def get_master_user(email, password):
    user = await tenant_model.objects.using(
        'default'
    ).filter(
        email=email.lower().strip(),
    ).select_related(
        'account', 'account__db'
    ).filter(
        account__status_id__in=[
            ACCOUNT_STATUS.ACTIVE,
        ]
    ).afirst()

    if user and check_password(password, user.password):
        if not user.account:
            raise HTTPException(400, 'Missing account')

        await save_connection(user.account)

        return user

    return None


async def get_account(domain):
    if not account_model or not domain:
        raise HTTPException(400, 'Missing data')

    domain = domain.lower().strip()

    account = await account_model.objects.using(
        'default'
    ).filter(
        Q(subdomain=domain) | Q(domain=domain),
    ).select_related(
        'db'
    ).filter(
        status_id__in=[
            ACCOUNT_STATUS.ACTIVE,
        ]
    ).afirst()

    if account:
        await save_connection(account)
        return account

    return None

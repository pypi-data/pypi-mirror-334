import json

import aioboto3

from ...loggers.logger import Logger

logger = Logger()


class GetSecretFailed(Exception):
    pass


class SecretsConnectionFailed(Exception):
    pass


class Secrets:
    # internal use only
    _secrets_client = None

    def __init__(self, *args, **kwargs):
        pass

    async def connect(self):
        # share the secrets client at the global level
        if Secrets._secrets_client is None:
            try:
                Secrets._secrets_client = await aioboto3.Session().client("secretsmanager").__aenter__()
            except Exception as e:
                logger.error(f"{self.__name__}.connect - error", priority=3)
                logger.error(f"{e.__class__.__name__}: {str(e)}")
                raise SecretsConnectionFailed(str(e))

    async def get(self, secret_name):
        await self.connect()

        logger.debug(f"{self.__class__.__name__}.get", priority=2)
        logger.debug(f"secret_name: {secret_name}")

        try:
            get_secret_value_response = await self._secrets_client.get_secret_value(
                SecretId=secret_name,
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get - error", priority=3)
            logger.error(f"{e.__class__.__name__}: {str(e)}")
            raise GetSecretFailed(str(e))

        try:
            return json.loads(get_secret_value_response["SecretString"])
        except:  # noqa
            return get_secret_value_response["SecretString"]

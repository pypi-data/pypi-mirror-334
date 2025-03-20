import json
import uuid
import shortuuid
from datetime import datetime, timedelta, timezone
from .controllers.users import UsersController
from .controllers.subscriptions import SubscriptionsController
from .controllers.nodes import NodesController
from .controllers.token import TokenController
import asyncio

class UserManager:
    """
    Класс для управления пользователями через API.

    Основные методы:
    - add_user(username, days, **kwargs): Создает нового пользователя с указанным именем и параметрами.
    - get_users(): Возвращает список всех пользователей.
    - get_user(username, **kwargs): Получает информацию о пользователе по имени и фильтрует данные.
    - get_user_by_uuid(uuid, all=False, **kwargs)
    - remove_user(username)
    - enable_user(uuid)
    - disable_user(uuid)
    - reset_user_traffic(uuid)
    """

    def __init__(self):
        self.users = UsersController()

    def _generate_dates(self, days=60):
        """
        Генерирует даты создания и истечения срока действия.

        Параметры:
        days (int): Количество дней до истечения срока. По умолчанию 60.

        Возвращает:
        tuple: (created_at, expire_at) в формате ISO 8601 с миллисекундами и 'Z' (UTC).
        """
        created_at = datetime.utcnow().isoformat(timespec='milliseconds') + "Z"
        expire_at = (datetime.utcnow() + timedelta(days=days)
                     ).isoformat(timespec='milliseconds') + "Z"
        return created_at, expire_at

    async def add_user(self, username, days, telegramId, **kwargs):
        """
        Создает нового пользователя с указанным именем пользователя и дополнительными параметрами.

        Параметры:
        username (str): Имя пользователя для создания.

        **kwargs: Дополнительные параметры для создания пользователя. Если параметры не указаны, будут использованы значения по умолчанию.
            Возможные параметры:
            - subscriptionUuid (str): UUID подписки. По умолчанию генерируется автоматически.
            - shortUuid (str): Короткий UUID. По умолчанию генерируется автоматически.
            - trojanPassword (str): Пароль для Trojan. По умолчанию равен shortUuid.
            - vlessUuid (str): UUID для VLESS. По умолчанию равен subscriptionUuid.
            - ssPassword (str): Пароль для Shadowsocks. По умолчанию равен shortUuid.
            - trafficLimitBytes (int): Лимит трафика в байтах. По умолчанию 0 (без лимита).
            - trafficLimitStrategy (str): Стратегия лимита трафика. По умолчанию "NO_RESET".
            - expireAt (str): Дата истечения срока действия в формате ISO 8601. По умолчанию +60 дней от текущей даты.
            - createdAt (str): Дата создания в формате ISO 8601. По умолчанию текущая дата и время.
            - lastTrafficResetAt (str): Дата последнего сброса трафика. По умолчанию None.
            - description (str): Описание пользователя. По умолчанию пустая строка.
            - activateAllInbounds (bool): Активировать все inbound подключения. По умолчанию True.

        Возвращает:
        dict: Созданный пользователь.

        Пример:
        user_manager = UserManager()
        new_user = await user_manager.add_user("testuser", days=30)
        new_user = await user_manager.add_user('example', days=30, description='Новый пользователь', trafficLimitBytes=1073741824)
        """
        # Генерация значений по умолчанию
        vless_uuid = str(uuid.uuid4())
        short_uuid = str(shortuuid.uuid())
        traffic_limit_bytes = 0
        # Получаем даты
        created_at, expire_at = self._generate_dates(kwargs.pop('days', days))
        # Генерация текущей даты в формате ISO 8601
        last_traffic_reset_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        # Параметры по умолчанию
        default_params = {
            "subscriptionUuid": vless_uuid,
            "shortUuid": short_uuid,
            "trojanPassword": short_uuid,
            "vlessUuid": vless_uuid,
            "ssPassword": short_uuid,
            "trafficLimitBytes": traffic_limit_bytes,
            "trafficLimitStrategy": "NO_RESET",
            "expireAt": expire_at,
            "createdAt": created_at,
            "lastTrafficResetAt": last_traffic_reset_at,
            "description": "",
            "telegramId": telegramId,
            "activateAllInbounds": True
        }

        # Обновляем параметры по умолчанию переданными значениями из kwargs
        default_params.update(kwargs)

        # Создаем пользователя
        user = await self.users.create_user(username, **default_params)
        return user

    async def update_user(self, uuid, **kwargs):
        """
        Обновляет данные пользователя по UUID, включая возможное добавление дней к сроку действия подписки.

        Параметры:
        uuid (str): UUID пользователя для обновления.
        **kwargs: Дополнительные параметры для обновления пользователя, в том числе:
            - days_to_add (int): Количество дней для добавления к сроку действия.
            - expireAt (str): Новая дата истечения срока действия (ISO 8601).
             - status='ACTIVE',  # Изменение статуса на EXPIRED
             - trafficLimitBytes=1000000,  # Изменение лимита трафика
             - description="Updated user data"  # Обновление описания
            - другие параметры для обновления данных пользователя.

        Возвращает:
        dict: Ответ API.
        """

        # Получаем текущие данные пользователя
        user_data = await self.get_user_by_uuid(uuid, all=True)
        current_expire_at = user_data.get("expireAt", datetime.now(timezone.utc).isoformat())

        # Если передан параметр days_to_add, обновляем срок подписки
        if 'days_to_add' in kwargs:
            new_expire_at = (datetime.fromisoformat(current_expire_at.rstrip('Z')) + timedelta(days=kwargs['days_to_add'])).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            kwargs['expireAt'] = new_expire_at  # Обновляем expireAt с новым значением

        # Обновляем пользователя с переданными параметрами, включая uuid
        kwargs['uuid'] = uuid  # Убедитесь, что uuid передается явно

        # Убедитесь, что все необходимые параметры (например, status) присутствуют
        if 'status' not in kwargs:
            kwargs['status'] = user_data.get('status', 'ACTIVE')  # Применить статус по умолчанию, если не передан

        if 'trafficLimitBytes' not in kwargs:
            kwargs['trafficLimitBytes'] = user_data.get('trafficLimitBytes', 0)  # Применить лимит трафика по умолчанию, если не передан

        if 'trafficLimitStrategy' not in kwargs:
            kwargs['trafficLimitStrategy'] = user_data.get('trafficLimitStrategy', 'NO_RESET')  # Применить стратегию лимита по умолчанию

        if 'description' not in kwargs:
            kwargs['description'] = user_data.get('description', '')  # Применить описание по умолчанию

        if 'telegramId' not in kwargs:
            kwargs['telegramId'] = user_data.get('telegramId')  # Применить Telegram ID, если не передан


        # Удаляем любые поля с значением None
        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        # Обновляем пользователя с учетом всех параметров
        user = await self.users.update_user(uuid, **kwargs)

        return user



    async def get_users(self):
        """
        Возвращает список всех пользователей.

        Возвращает:
        list: Список пользователей.

        Пример:
            user_manager = UserManager()
            users = await user_manager.get_users()
            print("Список пользователей:", users)
        """
        users = await self.users.get_users()
        print("Список пользователей:", users)
        return users

    async def get_user(self, username, all=False, **kwargs):
        """
        Получает информацию о пользователе по имени пользователя.

        Параметры:
            username (str): Имя пользователя для получения информации.
            all (bool, необязательно): Если True, возвращает полный ответ от сервера.

        **kwargs: Фильтры для извлечения определённых данных.
        Возможные параметры (устанавливаются в True):
            - username_filter (bool): Возвращает имя пользователя.
            - status_filter (bool): Возвращает статус пользователя.
            - expireAt_filter (bool): Возвращает дату истечения подписки.
            - createdAt_filter (bool): Возвращает дату создания пользователя.
            - updatedAt_filter (bool): Возвращает дату последнего обновления пользователя.
            - usedTrafficBytes_filter (bool): Возвращает использованный трафик.
            - lifetimeUsedTrafficBytes_filter (bool): Возвращает общий использованный трафик.
            - trafficLimitBytes_filter (bool): Возвращает лимит трафика.
            - subscriptionUuid_filter (bool): Возвращает UUID подписки.
            - shortUuid_filter (bool): Возвращает короткий UUID.
            - uuid_filter (bool): Возвращает полный UUID.
            - activeUserInbounds_filter (bool): Возвращает активные inbound-подключения.
            - description_filter (bool): Возвращает описание пользователя.

        Пример:
            user_manager = UserManager()
            username = await user_manager.get_user("testuser")  # Вернёт весь ответ
            username = await user_manager.get_user("testuser", all=True)  # Вернёт весь ответ
            username = await user_manager.get_user("testuser", username_filter=True, status_filter=True)  # Вернёт только имя пользователя и статус.

        Возвращает:
        dict: Полный ответ от сервера или отфильтрованные данные.
        """
        # Получаем полный ответ от API
        response = await self.users.get_user_by_username(username)
        user = response.get('response', {})

        # Если all=True или не переданы фильтры, возвращаем полный ответ
        if all or not kwargs:
            return user

        # Фильтруем данные по переданным параметрам
        filtered_data = {
            key.replace('_filter', ''): user.get(key.replace('_filter', ''))
            for key, value in kwargs.items() if value
        }

        return filtered_data

    async def get_user_by_uuid(self, uuid, all=False, **kwargs):
        response = await self.users.get_user_by_uuid(uuid)
        user = response.get('response', {})

        if all or not kwargs:
            return user

        filtered_data = {
            key.replace('_filter', ''): user.get(key.replace('_filter', ''))
            for key, value in kwargs.items() if value
        }

        return filtered_data

    async def remove_user(self, username):
        """
        Удаляет пользователя по имени пользователя.

        Параметры:
        username (str): Имя пользователя, которого необходимо удалить.

        Исключения:
        ValueError: Выбрасывается, если UUID пользователя не найден.

        Пример:
            delete_response = await user_manager.remove_user("testuser")
        """
        user_data = await UserManager().get_user(username, uuid_filter=True)

        if not user_data or "uuid" not in user_data:
            raise ValueError(f"UUID для пользователя {username} не найден")

        return await self.users.delete_user(str(user_data["uuid"]))

    async def enable_user(self, uuid):
        return await self.users.enable_user(uuid)

    async def disable_user(self, uuid):
        return await self.users.disable_user(uuid)

    async def reset_user_traffic(self, uuid):
        return await self.users.reset_user_traffic(uuid)

class SubscriptionsManager:
    """
    Class for managing subscriptions
    """

    def __init__(self):
        self.subscriptions = SubscriptionsController()
    
    async def get_subscription_info(self, shortUuid):
        return await self.subscriptions.get_subscription_info(shortUuid)

    async def get_subscription(self, shortUuid):
        return await self.subscriptions.get_subscription(shortUuid)

class NodesManager:
    """
        Класс для работы с узлами.
    """    

    def __init__(self):
        self.nodes = NodesController()

    async def get_all_nodes(self, all=False, **kwargs):
        """
        Получает список всех узлов с возможностью фильтрации.

        Параметры:
            all (bool, необязательно): Если True, возвращает полный ответ от сервера.
            **kwargs: Фильтры для извлечения определённых данных.
                - uuid_filter (bool): Возвращает UUID узла.
                - name_filter (bool): Возвращает имя узла.
                - address_filter (bool): Возвращает адрес узла.
                - usersOnline_filter (bool): Возвращает количество пользователей онлайн.
                - cpuModel_filter (bool): Возвращает модель процессора.
                - trafficUsedBytes_filter (bool): Возвращает использованный трафик.
                и другие поля, как показано в примере ниже.

        Пример:
            nodes = await node_manager.get_all_nodes()
            nodes = await get_all_nodes(all=True)  # Вернёт весь ответ.
            nodes = await get_all_nodes(uuid_filter=True, name_filter=True)  # Вернёт только UUID и имя узла.

        Возвращает:
            dict: Полный ответ от сервера или отфильтрованные данные.
        """
        nodes = await self.nodes.get_all_nodes()

        # Если all=True или не переданы фильтры, возвращаем весь ответ
        if all or not kwargs:
            return nodes

        # Фильтруем данные по переданным параметрам
        filtered_nodes = []
        for node in nodes['response']:
            filtered_data = {
                key.replace('_filter', ''): node.get(key.replace('_filter', ''))
                for key, value in kwargs.items() if value
            }
            filtered_nodes.append(filtered_data)

        return {'response': filtered_nodes}

    async def get_one_node(self, node_uuid, all=False, **kwargs):
        """
        Получает информацию об одном узле по UUID с возможностью фильтрации.

        Параметры:
            node_uuid (str): UUID узла для получения информации.
            all (bool, необязательно): Если True, возвращает полный ответ от сервера.
            **kwargs: Фильтры для извлечения определённых данных.

        Пример:
            node_manager = NodesManager()
            nodes = await node_manager.get_all_nodes()
            node_uuid = nodes['response'][0]['uuid']  # Получаем UUID первого узла
            node_details = await node_manager.get_one_node(node_uuid)  # Вернёт весь ответ.
            node_filtered = await node_manager.get_one_node(node_uuid, name_filter=True, address_filter=True)  # Вернёт только имя и адрес узла.

        Возвращает:
            dict: Полный ответ от сервера или отфильтрованные данные.
        """
        # Получаем полный ответ о конкретном узле по UUID
        node_response = await self.nodes.get_one_node(node_uuid)

        # Извлекаем данные узла из ответа
        node = node_response.get('response', {})

        # Если all=True или не переданы фильтры, возвращаем весь ответ
        if all or not kwargs:
            return node

        # Фильтруем данные по переданным параметрам
        filtered_data = {}

        for key, value in kwargs.items():
            if value:  # Если значение фильтра True, добавляем его в результат
                field = key.replace('_filter', '')  # Извлекаем имя поля (например, 'name', 'address')
                filtered_data[field] = node.get(field)  # Добавляем поле в отфильтрованные данные

        return filtered_data

    async def enable_node(self, node_uuid):
        return await self.nodes.enable_node(node_uuid)

    async def disable_node(self, node_uuid):
        return await self.nodes.disable_node(node_uuid)

    async def delete_node(self, node_uuid):
        return await self.nodes.delete_node(node_uuid)

    async def restart_node(self, node_uuid):
        return await self.nodes.restart_node(node_uuid)

    async def restart_all_nodes(self):
        return await self.nodes.restart_all_nodes

class TokenManager:


    def __init__(self):
        self.token = TokenController()


    async def create_token(self, token_name='Test_Token', **kwargs):

        default_params = {
            "tokenName": f"{token_name}",
            "tokenDescription": None
        }

        default_params.update(kwargs)

        token = await self.token.create_token(**default_params)
        return token
    

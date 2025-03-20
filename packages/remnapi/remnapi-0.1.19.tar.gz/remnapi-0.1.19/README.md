```markdown
# RemnAPI

**RemnAPI** — это клиент для работы с API пользователей и узлов в панели RemnaWave.

## Установка

Для установки библиотеки используйте pip:

```bash
pip install remnapi
```

```bash
.env

PANEL_URL = "https://panel.example.com/api" 
API_TOKEN = "yourAPItoken"
```
## Использование

### UserManager

Класс для управления пользователями через API.

#### Основные методы:

- **add_user(username, days, **kwargs):**  
  Создает нового пользователя с указанным именем и параметрами.

  **Параметры:**
  - `username` (str): Имя пользователя для создания.
  - `days` (int): Срок подписки.

  **Дополнительные параметры (kwargs):**
  - `subscriptionUuid` (str): UUID подписки. По умолчанию генерируется автоматически.
  - `shortUuid` (str): Короткий UUID. По умолчанию генерируется автоматически.
  - `trojanPassword` (str): Пароль для Trojan. По умолчанию равен `shortUuid`.
  - `vlessUuid` (str): UUID для VLESS. По умолчанию равен `subscriptionUuid`.
  - `ssPassword` (str): Пароль для Shadowsocks. По умолчанию равен `shortUuid`.
  - `trafficLimitBytes` (int): Лимит трафика в байтах. По умолчанию 0 (без лимита).
  - `trafficLimitStrategy` (str): Стратегия лимита трафика. По умолчанию `"NO_RESET"`.
  - `expireAt` (str): Дата истечения срока действия в формате ISO 8601. По умолчанию +60 дней от текущей даты.
  - `createdAt` (str): Дата создания в формате ISO 8601. По умолчанию текущая дата и время.
  - `lastTrafficResetAt` (str): Дата последнего сброса трафика. По умолчанию `None`.
  - `description` (str): Описание пользователя. По умолчанию пустая строка.
  - `activateAllInbounds` (bool): Активировать все inbound подключения. По умолчанию `True`.

- **get_users():**  
  Возвращает список всех пользователей.

- **get_user(username, **kwargs):**  
  Получает информацию о пользователе по имени и фильтрует данные.

  **Параметры:**
  - `username` (str): Имя пользователя для получения информации.
  - `all` (bool, необязательно): Если `True`, возвращает полный ответ от сервера.

  **Дополнительные фильтры (kwargs):**
  - `username_filter`, `status_filter`, `expireAt_filter`, `createdAt_filter`, `updatedAt_filter` и другие — фильтруют данные по соответствующим полям.

- **remove_user(username):**  
  Удаляет пользователя по имени.

#### Пример использования:

```python
from remnapi import UserManager
import asyncio

async def main():
    user_manager = UserManager()
    
    # Создание пользователя
    new_user = await user_manager.add_user("testuser", days=30)  # Возвращает JSON

    # Создание пользователя с дополнительными параметрами
    one_gb = 1073741824  # Переводим байты в ГБ
    new_user2 = await user_manager.add_user('example', days=30, description='example', trafficLimitBytes=one_gb*20)

    # Получение информации
    username_info = await user_manager.get_user("testuser")  # Возвращает JSON
    username_filter = await user_manager.get_user("testuser", username_filter=True, shortUuid_filter=True, status_filter=True)  # Возвращает отфильтрованный JSON

    # Получение списка всех пользователей
    users = await user_manager.get_users()  # Возвращает JSON

    # Удаление пользователя
    delete_response = await user_manager.remove_user("testuser")  # Возвращает JSON

asyncio.run(main())
```

---

### NodesManager

Класс для управления узлами через API.

#### Основные методы:

- **get_all_nodes(**kwargs):**  
  Получает список всех узлов с возможностью фильтрации.

  **Параметры:**
  - `all` (bool, необязательно): Если `True`, возвращает полный ответ от сервера.
  - **kwargs**: Фильтры для извлечения определённых данных.
    - `uuid_filter` (bool): Возвращает UUID узла.
    - `name_filter` (bool): Возвращает имя узла.
    - `address_filter` (bool): Возвращает адрес узла.
    - `usersOnline_filter` (bool): Возвращает количество пользователей онлайн.
    - `cpuModel_filter` (bool): Возвращает модель процессора.
    - `trafficUsedBytes_filter` (bool): Возвращает использованный трафик.

- **get_one_node(node_uuid, **kwargs):**  
  Получает информацию об одном узле по UUID с возможностью фильтрации.

  **Параметры:**
  - `node_uuid` (str): UUID узла для получения информации.
  - `all` (bool, необязательно): Если `True`, возвращает полный ответ от сервера.
  - **kwargs**: Фильтры для извлечения определённых данных.

- **enable_node(node_uuid):**  
  Включает узел.

- **disable_node(node_uuid):**  
  Отключает узел.

- **delete_node(node_uuid):**  
  Удаляет узел.

- **restart_node(node_uuid):**  
  Перезапускает узел.

- **restart_all_nodes():**  
  Перезапускает все узлы.


#### Пример использования:

```python
from remnapi import NodesManager
import asyncio

async def main():
    node_manager = NodesManager()
    
    # Получаем список всех узлов
    nodes = await node_manager.get_all_nodes()  # Вернёт весь ответ
    nodes_all = await node_manager.get_all_nodes(all=True)  # Вернёт весь ответ с деталями
    nodes_filter = await node_manager.get_all_nodes(uuid_filter=True, name_filter=True)  # Вернёт только UUID и имя узла.

    # Получаем информацию об одном узле
    node_uuid = nodes['response'][0]['uuid']  # Получаем UUID первого узла
    node_details = await node_manager.get_one_node(node_uuid)  # Вернёт весь ответ.
    node_filtered = await node_manager.get_one_node(node_uuid, name_filter=True, address_filter=True)  # Вернёт только имя и адрес узла.

asyncio.run(main())
```

---

## Лицензия

MIT License. См. [LICENSE](LICENSE) для подробной информации.
```
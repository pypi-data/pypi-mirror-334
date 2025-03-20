"""
# Based on Modmail (https://github.com/modmail-dev/Modmail)
# Copyright (C) [Original Year] Modmail Developers
# Modifications by martinbndr (2025)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
from copy import deepcopy
import os
import typing
from typing import Union, Optional, Any, Iterable

class _Default:
    pass

Default = _Default()

class PluginDbManager:
    def __init__(
            self, 
            plugin, 
            bot,
            logger,
            public_keys: Optional[dict] = {},
            private_keys: Optional[dict] = {},
            protected_keys: Optional[dict] = {},
            default_docs: list = None
            ):
        self.plugin = plugin
        self.bot = bot
        self.public_keys = public_keys
        self.private_keys = private_keys
        self.protected_keys = protected_keys
        self.default_docs = default_docs
        self.logger = logger
        
        self.data_types = {
            "colors": {},
            "bools": {},
            "time_deltas": {},
            "enums": {},
            "strings": {}
        }
        
        self.defaults = {**self.public_keys, **self.private_keys, **self.protected_keys}
        self.all_keys = set(self.defaults.keys())

        self.db = self.bot.plugin_db.get_partition(self.plugin)
        self._cache = {}
        self.ready_event = asyncio.Event()

    def setup(self) -> dict:
        data = deepcopy(self.defaults)

        data.update({k.lower(): v for k, v in os.environ.items() if k.lower() in self.all_keys})
        self._cache = data
        return self._cache
    
    async def update(self):
        """Updates the config with data from the cache"""
        await self.db.update_one({"bot_id": str(self.bot.user.id), "type": "config"}, {"$set": self.filter_default(self._cache)})
    
    async def refresh(self) -> dict:
        for k, v in (await self.db.find_one({"bot_id": self.bot.user.id, "type": "config"})).items():
            k = k.lower()
            if k in self.all_keys:
                self._cache[k] = v
        if not self.ready_event.is_set():
            self.ready_event.set()
            self.logger.debug("Successfully fetched configurations from database.")
        return self._cache
    
    async def wait_until_ready(self) -> None:
        await self.ready_event.wait()

    def __getitem__(self, key: str) -> Any:
        return self.get(key)
    
    def __setitem__(self, key: str, item: Any) -> Any:
        key = key.lower()
        if key not in self.all_keys:
            self.logger.warning("Invalid configuration key %s", key)
        self._cache[key] = item

    def __delitem__(self, key: str) -> None:
        return self.remove(key)
    
    def get(self, key: str, *, convert: bool = True) -> Any:
        key = key.lower()
        if key not in self.all_keys:
            self.logger.warning("Invalid configuration key %s", key)
        if key not in self._cache:
            self._cache[key] = deepcopy(self.defaults[key])
        value = self._cache[key]

        if not convert:
            return value
        
    async def set(self, key: str, item: Any, convert=True) -> None:
        #if not convert:
        return self.__setitem__(key, item)

        #if key in self.data_types["colors"]:
        #    try:
        #        hex_ = str(item)
        #        if hex_.startswith("#"):
        #            hex_ = hex_[1:]
        #        if len(hex_) == 3:
        #            hex_ = "".join(s for s in hex_ for _ in range(2))
        #        if len(hex_) != 6:
        #            self.logger.warning("Invalid color name or hex.")
        #        try:
        #            int(hex_, 16)
        #        except ValueError:
        #            self.logger.warning("Invalid color name or hex.")
#
        #    except:
        #        name = str(item).lower()
        #        name = re.sub(r"[\-+|. ]+", " ", name)
        #        hex_ = ALL_COLORS.get(name)
        #        if hex_ is None:
        #            name = re.sub(r"[\-+|. ]+", "", name)
        #            hex_ = ALL_COLORS.get(name)
        #            if hex_ is None:
        #                raise
        #    return self.__setitem__(key, "#" + hex_)
#
        #if key in self.time_deltas:
        #    try:
        #        isodate.parse_duration(item)
        #    except isodate.ISO8601Error:
        #        try:
        #            converter = UserFriendlyTime()
        #            time = await converter.convert(None, item, now=discord.utils.utcnow())
        #            if time.arg:
        #                raise ValueError
        #        except BadArgument as exc:
        #            raise InvalidConfigError(*exc.args)
        #        except Exception as e:
        #            logger.debug(e)
        #            raise InvalidConfigError(
        #                "Unrecognized time, please use ISO-8601 duration format "
        #                'string or a simpler "human readable" time.'
        #            )
        #        now = discord.utils.utcnow()
        #        item = isodate.duration_isoformat(time.dt - now)
        #    return self.__setitem__(key, item)
#
        #if key in self.booleans:
        #    try:
        #        return self.__setitem__(key, strtobool(item))
        #    except ValueError:
        #        raise InvalidConfigError("Must be a yes/no value.")
#
        #elif key in self.enums:
        #    if isinstance(item, self.enums[key]):
        #        # value is an enum type
        #        item = item.value
#
        #return self.__setitem__(key, item)

    def remove(self, key: str) -> Any:
        key = key.lower()
        self.logger.info("Removing %s.", key)
        if key not in self.all_keys:
            self.logger.warning("Configuration key %s is invalid.", key)
        if key in self._cache:
            del self._cache[key]
        self._cache[key] = deepcopy(self.defaults[key])
        return self._cache[key]

    def items(self) -> Iterable:
        return self._cache.items()
    
    @classmethod
    def filter_valid(cls, data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return {
            k.lower(): v
            for k, v in data.items()
            if k.lower() in cls.public_keys or k.lower() in cls.private_keys
        }

    @classmethod
    def filter_default(cls, data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        filtered = {}
        for k, v in data.items():
            default = cls.defaults.get(k.lower(), Default)
            if default is Default:
                cls.logger.error("Unexpected configuration detected: %s.", k)
                continue
            if v != default:
                filtered[k.lower()] = v
        return filtered
        
    async def insert_doc(self, data: dict):
        await self.db.insert_many(data)

    async def update_doc(self, filter: dict, operations: dict):
        await self.db.delete_one(filter)

    async def delete_doc(self, filter: dict):
        await self.db.delete_one(filter)
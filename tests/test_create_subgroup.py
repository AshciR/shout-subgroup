from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from shout_subgroup.exceptions import InvalidSubGroupNameError
from shout_subgroup.modify_subgroup import create_subgroup
from test_helpers import create_test_user, create_test_group_chat


class MockTelegramChat:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description


@pytest.mark.asyncio
async def test_create_subgroup(db: Session):
    # Given: A group chat already exists
    john = create_test_user(db, telegram_user_id=12345, username="johndoe", first_name="John", last_name="Doe")
    jane = create_test_user(db, telegram_user_id=67890, username="janedoe", first_name="Jane", last_name="Doe")

    telegram_group_chat_id = -123456789
    group_chat = create_test_group_chat(db, telegram_group_chat_id, "Group Chat", [john, jane])

    # And: We have the subgroup information
    telegram_chat = Mock()
    telegram_chat.id = group_chat.telegram_group_chat_id
    telegram_chat.title = group_chat.name
    telegram_chat.description = group_chat.description

    subgroup_name = "Archery"
    user_ids = {john.user_id, jane.user_id}

    # When: We add subgroup
    subgroup = await create_subgroup(db, telegram_chat, subgroup_name, user_ids)

    # Then: It's added correctly
    assert subgroup.subgroup_id is not None
    assert subgroup.name == subgroup_name
    assert subgroup.group_chat_id is not None

    assert len(subgroup.users) == 2
    assert set([user.user_id for user in subgroup.users]) == user_ids


@pytest.mark.asyncio
async def test_can_not_create_subgroup_with_mentions_in_the_name(db: Session):
    # Given: A group chat already exists
    john = create_test_user(db, telegram_user_id=12345, username="johndoe", first_name="John", last_name="Doe")
    jane = create_test_user(db, telegram_user_id=67890, username="janedoe", first_name="Jane", last_name="Doe")

    telegram_group_chat_id = -123456789
    group_chat = create_test_group_chat(db, telegram_group_chat_id, "Group Chat", [john, jane])

    # And: We have the subgroup information
    telegram_chat = Mock()
    telegram_chat.id = group_chat.telegram_group_chat_id
    telegram_chat.title = group_chat.name
    telegram_chat.description = group_chat.description

    user_ids = {john.user_id, jane.user_id}

    # And: The subgroup name has a mention in it
    invalid_subgroup_name = "@invalid_name"

    # When: We try to create the subgroup
    with pytest.raises(InvalidSubGroupNameError) as ex:
        await create_subgroup(db, telegram_chat, invalid_subgroup_name, user_ids)

    # Then: A valid error and message are raised
    assert invalid_subgroup_name in ex.value.message

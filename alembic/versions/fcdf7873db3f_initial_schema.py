"""Initial schema

Revision ID: fcdf7873db3f
Revises: 
Create Date: 2024-09-13 13:16:57.821676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcdf7873db3f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group_chats',
    sa.Column('group_chat_id', sa.String(), nullable=False),
    sa.Column('telegram_group_chat_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('group_chat_id'),
    sa.UniqueConstraint('telegram_group_chat_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('telegram_user_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('telegram_user_id')
    )
    op.create_table('subgroups',
    sa.Column('subgroup_id', sa.String(), nullable=False),
    sa.Column('group_chat_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_chat_id'], ['group_chats.group_chat_id'], ),
    sa.PrimaryKeyConstraint('subgroup_id')
    )
    op.create_table('users_group_chats_join_table',
    sa.Column('group_chat_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['group_chat_id'], ['group_chats.group_chat_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], )
    )
    op.create_table('users_subgroups_join_table',
    sa.Column('subgroup_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['subgroup_id'], ['subgroups.subgroup_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_subgroups_join_table')
    op.drop_table('users_group_chats_join_table')
    op.drop_table('subgroups')
    op.drop_table('users')
    op.drop_table('group_chats')
    # ### end Alembic commands ###

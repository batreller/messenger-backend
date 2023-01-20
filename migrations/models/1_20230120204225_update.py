from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chat" ADD "creator_id" INT NOT NULL;
        ALTER TABLE "chat" ALTER COLUMN "type" TYPE VARCHAR(7) USING "type"::VARCHAR(7);
        ALTER TABLE "chat" ADD CONSTRAINT "fk_chat_user_d96bc8a7" FOREIGN KEY ("creator_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chat" DROP CONSTRAINT "fk_chat_user_d96bc8a7";
        ALTER TABLE "chat" DROP COLUMN "creator_id";
        ALTER TABLE "chat" ALTER COLUMN "type" TYPE VARCHAR(7) USING "type"::VARCHAR(7);"""

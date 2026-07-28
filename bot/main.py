from __future__ import annotations

import logging

import discord
from discord import app_commands

from bot.config import get_bot_token, get_guild_id
from bot.dice import biased_high_roll, biased_low_roll, roll_many


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class SondakuDiceBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self._synced = False

    async def setup_hook(self) -> None:
        guild_id = get_guild_id()
        if guild_id:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info("Guild commands synced: %s", [command.name for command in synced])
        else:
            synced = await self.tree.sync()
            logger.info("Global commands synced: %s", [command.name for command in synced])
        self._synced = True

    async def on_ready(self) -> None:
        logger.info("Logged in as %s (id=%s)", self.user, self.user.id if self.user else "unknown")
        if self._synced:
            logger.info("Slash commands are ready.")


bot = SondakuDiceBot()


@bot.tree.command(name="sd10", description="10d100 を振る。65以上は約20%しか出ない忖度ダイス")
async def sd10(interaction: discord.Interaction) -> None:
    rolls = roll_many(biased_high_roll, count=10)
    total = sum(rolls)
    joined_rolls = ", ".join(str(value) for value in rolls)
    message = f"/sd10（忖度ダイス）\n`{total}` ← [{joined_rolls}]"
    await interaction.response.send_message(message)


@bot.tree.command(name="scd10", description="10d100 を振る。30%で 1〜5 が出る超忖度ダイス")
async def scd10(interaction: discord.Interaction) -> None:
    rolls = roll_many(biased_low_roll, count=10)
    total = sum(rolls)
    joined_rolls = ", ".join(str(value) for value in rolls)
    message = f"/scd10（超忖度ダイス）\n`{total}` ← [{joined_rolls}]"
    await interaction.response.send_message(message)


def main() -> None:
    token = get_bot_token()
    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
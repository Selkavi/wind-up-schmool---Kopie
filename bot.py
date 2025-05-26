import discord
from discord import app_commands
import json, random, os

intents = discord.Intents.default()
intents.message_content = True

with open("pictures.json", "r", encoding="utf-8") as f:
    image_db = json.load(f)

class PersistentRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Study Hour",
        style=discord.ButtonStyle.primary,
        custom_id="persistent_study_hour"
    )
    async def study(
        self,
        interaction: discord.Interaction,         # → zuerst Interaction
        button: discord.ui.Button                # → dann Button
    ):
        guild = interaction.guild
        role = guild.get_role(1210186610772025425)
        member = interaction.user

        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"I removed the role {role.mention}.",
                ephemeral=True
            )
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"You get the role {role.mention}!",
                ephemeral=True
            )

    @discord.ui.button(
    label="Movie Night",
    style=discord.ButtonStyle.primary,
    custom_id="persistent_movie_night"
    )
    async def movie(
        self,
        interaction: discord.Interaction,    # ← zuerst Interaction
        button: discord.ui.Button            # ← dann Button
    ):
        guild = interaction.guild
        role = guild.get_role(1376582239206244414)
        member = interaction.user

        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"I removed the role {role.mention}.", 
                ephemeral=True
            )
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"You get the role {role.mention}!", 
                ephemeral=True
            )

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self._roles_msg_sent = False

    async def setup_hook(self):
        await self.tree.sync()
        self.add_view(PersistentRoleView())
        print("Commands und View registriert")

    async def on_ready(self):
        print(f"Bot ist online als {self.user}")
        if not self._roles_msg_sent:
            channel = self.get_channel(1376521450328031363)
            if channel:
                await channel.send("Choose a role:", view=PersistentRoleView())
                self._roles_msg_sent = True
            else:
                print("Channel nicht gefunden, prüfe die ID!")

    @app_commands.command(name="button", description="Show role buttons")
    async def button(self, interaction: discord.Interaction):
        await interaction.response.send_message("Choose your role:", view=PersistentRoleView())


# random para pictures
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        content = message.content.strip()

        if content == "$para":
            para_images = image_db.get("para", [])
            if not para_images:
                return await message.channel.send("Keine Bilder gefunden.")

            url = random.choice(para_images)
            embed = discord.Embed(
                title="Awww you missed me? Here, get a picture :3",
                color=discord.Color.blurple()
            )
            embed.set_image(url=url)
            await message.channel.send(embed=embed)

client = MyClient()
token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise RuntimeError("DISCORD_TOKEN nicht gefunden in den Umgebungsvariablen")
client.run(token)
client.run("DISCORD_TOKEN")

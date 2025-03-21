import os
import importlib
import subprocess
import sys
import logging
import discord
from discord.ext import commands

# Auto-installation des dépendances
def install_requirements():
    required_packages = ["requests", "discord"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installation de '{package}' en cours...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_requirements()

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeegaffeBot:
    def __init__(self, command_prefix: str = "!", intents=None):
        if intents is None:
            intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.load_commands()
        self.load_slash_commands()
        
        @self.bot.event
        async def on_ready():
            logging.info(f'✅ Connecté en tant que {self.bot.user}')
            await self.sync_commands()
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return  # Ignore les messages des bots
            logging.info(f"[{message.author}] {message.content}")
            await self.bot.process_commands(message)  # Permet de traiter les commandes
        
        @self.bot.event
        async def on_member_join(member):
            channel = member.guild.system_channel
            if channel:
                await channel.send(f"Bienvenue {member.mention} sur {member.guild.name} !")
    
    async def sync_commands(self):
        """Synchronise les commandes slash avec Discord."""
        await self.bot.wait_until_ready()
        await self.bot.tree.sync()
        logging.info("✅ Commandes slash synchronisées avec Discord !")

    def load_commands(self):
        """Charge automatiquement toutes les commandes du dossier 'commands' et affiche les commandes chargées."""
        if not os.path.exists("commands"):
            os.makedirs("commands")

        loaded_commands = []
        for filename in os.listdir("commands"):
            if filename.endswith(".py"):
                module_name = f"commands.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, "setup"):
                        module.setup(self.bot)  # Charge la commande via setup()
                    loaded_commands.append(filename[:-3])
                except Exception as e:
                    logging.error(f"❌ Erreur de chargement {filename}: {e}")
        
        if loaded_commands:
            logging.info(f"✅ Commandes chargées : {', '.join(loaded_commands)}")
        else:
            logging.warning("⚠️ Aucune commande trouvée dans 'commands/'.")
    
    def load_slash_commands(self):
        """Ajoute des commandes slash de base au bot."""
        @self.bot.tree.command(name="ping", description="Renvoie Pong!")
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message("Pong! 🏓")
        
        @self.bot.tree.command(name="info", description="Affiche les infos de l'utilisateur.")
        async def info(interaction: discord.Interaction):
            await interaction.response.send_message(f"👤 Pseudo: {interaction.user.name}\n🆔 ID: {interaction.user.id}")
        
        logging.info("✅ Commandes slash ajoutées !")
    
    def command(self, *args, **kwargs):
        return self.bot.command(*args, **kwargs)
    
    def slash_command(self, *args, **kwargs):
        return self.bot.tree.command(*args, **kwargs)

    def run(self, token: str):
        """Lance le bot avec le token Discord."""
        self.bot.run(token)

# Interface simple pour récupérer le bot

def bot(command_prefix: str = "!"):
    feegaffe = FeegaffeBot(command_prefix)
    return feegaffe
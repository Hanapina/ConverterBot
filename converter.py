import discord
import asyncio
from discord.ext import commands
import requests
import json
from decouple import config

############## OpenExchange API ##############
id = config('OE_API_ID')
url = f"https://openexchangerates.org/api/latest.json?app_id={id}&symbols=JPY,SGD&prettyprint=false&show_alternative=false"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)

jsonResponse = response.json()
jpy_exchange = jsonResponse['rates']['JPY'];
sgd_exchange = jsonResponse['rates']['SGD'];

#Variable control for MBC (JPY)
three_thousand_mc_usd = 3150 / jpy_exchange
ten_thousand_mc_usd = 10500 / jpy_exchange
thirty_thousand_mc_usd = 31500 / jpy_exchange

#Variable control for Gems (SGD)
_980SGD = 21.98 / sgd_exchange;
_1980SGD = 44.98 / sgd_exchange;
_3280SGD = 68.98 / sgd_exchange;
_6480SGD = 148.98 / sgd_exchange;


############## Discord API ##############
def runBot():
    bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
    bot.remove_command("help")
    
    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))
    
    ### MobaCoin stuff ### 
    @bot.command(name="jpyConvert")
    async def _jpyConvert(message):
        def check(m):
            return m.author == message.author and m.channel == message.channel
                
        try: 
            await message.channel.send("Please enter your JPY amount that you want to convert to USD.")
            msg = await bot.wait_for("message", check=check, timeout=30)
            try:
                val = float(msg.content)
                val2OE = val / jpy_exchange
                val2PP = (val / jpy_exchange) * 1.049
                await message.channel.send("OpenExchangeRate: **%s¥** is " % msg.content + "**$%.2f\n**" % val2OE +
                                           "Paypal Approx Rate: **%s¥** is " % msg.content + "**$%.2f**" % val2PP)
            except ValueError:
                await message.channel.send("Input is not numerical. Please use command again.")
        except asyncio.TimeoutError:
            await message.channel.send("Sorry, you didn't reply in time!")

    @bot.command(name='3kMBC')
    async def _3kMBC(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("**3150¥** or 3k Mobacoins is:\n"
                                   "OpenExchange: **$%.2f**\n" % three_thousand_mc_usd + 
                                   "PayPal Estimate: **$%.2f**" % (three_thousand_mc_usd * 1.049))

    @bot.command(name='10kMBC')
    async def _10kMBC(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("**10500¥** or **10k** Mobacoins is:\n"
                                   "OpenExchange: **$%.2f**\n" % ten_thousand_mc_usd + 
                                   "PayPal Estimate: **$%.2f**" % (ten_thousand_mc_usd * 1.049))

    @bot.command(name='30kMBC')
    async def _30kMBC(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("**31500¥** or **30k** Mobacoins is:\n"
                                   "OpenExchange: **$%.2f**\n" % thirty_thousand_mc_usd +
                                   "PayPal Estimate: **$%.2f**" % (thirty_thousand_mc_usd * 1.049))
        
    @bot.command(name='listAllMb')
    async def listAllMb(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("**3150¥** or **3k Mobacoins** is:\n"
                                   "OpenExchange: **$%.2f**\n" % three_thousand_mc_usd + 
                                   "PayPal Estimate: **$%.2f**\n\n" % (three_thousand_mc_usd * 1.049) + 

                                   "**10500¥** or **10k Mobacoins** is:\n"
                                   "OpenExchange: **$%.2f**\n" % ten_thousand_mc_usd + 
                                   "PayPal Estimate: **$%.2f**\n\n" % (ten_thousand_mc_usd * 1.049) + 

                                   "**31500¥** or **30k Mobacoins** is:\n"
                                   "OpenExchange: **$%.2f**\n" % thirty_thousand_mc_usd +
                                   "PayPal Estimate: **$%.2f**" % (thirty_thousand_mc_usd * 1.049))

    ### Life MakeOver ###
    @bot.command(name="sgdConvert")
    async def _sgdConvert(message):
        def check(m):
            return m.author == message.author and m.channel == message.channel
                
        try: 
            await message.channel.send("Please enter your SGD amount that you want to convert to USD.")
            msg = await bot.wait_for("message", check=check, timeout=30)
            try:
                val = float(msg.content)
                val2OE = val / sgd_exchange
                val2PP = (val / sgd_exchange) * 1.049
                await message.channel.send("OpenExchangeRate: %sSGD is " % msg.content + "$%.2f\n" % val2OE +
                                           "Paypal Approx Rate: %sSGD is " % msg.content + "$%.2f" % val2PP)
            except ValueError:
                await message.channel.send("Input is not numerical. Please use command again.")
        except asyncio.TimeoutError:
            await message.channel.send("Sorry, you didn't reply in time!")

    @bot.command(name='980Gems')
    async def _980Gems(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("21.98SGD or 980Gems is:\n"
                                   "OpenExchange: $%.2f\n" % _980SGD +
                                   "PayPal Estimate: $%.2f" % (_980SGD * 1.049))
        
    @bot.command(name='1980Gems')
    async def _1980Gems(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("44.98SGD or 1980Gems is:\n"
                                   "OpenExchange: $%.2f\n" % _1980SGD +
                                   "PayPal Estimate: $%.2f" % (_1980SGD * 1.049))
        
    @bot.command(name='3280Gems')
    async def _3280Gems(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("68.98SGD or 3280Gems is:\n"
                                   "OpenExchange: $%.2f\n" % _3280SGD +
                                   "PayPal Estimate: $%.2f" % (_3280SGD * 1.049))
        
    @bot.command(name='6480Gems')
    async def _6480Gems(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("148.98SGD or 6480Gems is:\n"
                                   "OpenExchange: $%.2f\n" % _6480SGD +
                                   "PayPal Estimate: $%.2f" % (_6480SGD * 1.049))

    ### Help Command ###
    @bot.command(name='help')
    async def help(message):
        if message.author == bot.user and message.channel == bot.channel:
            return
        await message.channel.send("All currency conversions are taken from: <https://openexchangerates.org>\n"
                                    "Paypal takes about a 4.9% surcharge.\n\n\n"
                                    "Commands:\n"
                                    "**!help**: gives a list of commands that the bot can do.\n"
                                    "**!jpyConvert**: use to convert ¥ to USD\n"
                                    "**!sgdConvert**: use to convert specific SGD to USD\n"
                                    "**!listAllMb**: lists all MB functions currently set by the bot.\n"
                                    "**!3kMBC**: converts 3k Mobacoins to USD.\n"
                                    "**!10kMBC**: converts 10k Mobacoins to USD.\n"
                                    "**!30kMBC**: converts 30k Mobacoins to USD.\n"
                                    "**!980Gems**: converts 980 Gems to USD \n"
                                    "**!1980Gems**: converts 1980 Gems to USD\n"
                                    "**!3280Gems**: converts 3280 Gems to USD\n"
                                    "**!6480Gems**: converts 6480 Gems to USD\n")
        

    token = config('DISCORD_TOKEN')
    bot.run(token)

if __name__ == "__main__":
    runBot()
from typing import List, Tuple
import discord.ext.commands as commands
from cog_model import ModelCog


class MiscCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot: commands.Bot = bot

	@commands.command(brief="Show the top usage of a given word")
	async def word(self, ctx):
		modelcog: ModelCog = self.bot.get_cog("ModelCog")
		try:
			w: str = ctx.message.content.lower().split(" ")[1].strip()
			if w not in modelcog.words:
				await ctx.channel.send(f"'{w}' ? What's that :o ?")
			else:
				worduse: List[Tuple[str, int]] = sorted(list(modelcog.words[w].items()), key=lambda x: x[1], reverse=True)
				resolved = []
				total: float = 0.0
				maxlen: int = 0
				for (userid, count) in worduse:
					user = ctx.guild.get_member(int(userid))
					if user is not None:
						resolved.append((user.name, count))
						total += count
						if len(user.name) > maxlen:
							maxlen = len(user.name)
					else:
						print(f"Couldn't resolve {userid}")
				print(w, resolved)
				txtlist = []
				for (user, count) in resolved:
					txtlist.append(user + (maxlen - len(user)) * ' ' + f" - {round(100.0 * count / total, 2)}%")
				txtstr = '\n'.join(txtlist)
				await ctx.channel.send(f"Top '**{w}**' users:\n```{txtstr}```")
		except KeyError:
			await ctx.channel.send(
				f"Command usage: `{self.bot.command_prefix}word <word>`, it will show you the top usage of <word>.")

	@commands.command(aliases=["emos"], brief="Podium of the custom emojis for this server")
	async def emojis(self, ctx):
		modelcog: ModelCog = self.bot.get_cog("ModelCog")
		podium = []
		total = 0.0
		for emoji in ctx.guild.emojis:
			emo = str(emoji)
			if emo in modelcog.words:
				podium.append((emo, sum(modelcog.words[emo].values())))
			else:
				podium.append((emo, 0))
			total += podium[-1][1]
		podium.sort(key=lambda x: x[1], reverse=True)
		top = podium[:min(len(podium), 10)]
		other = podium[min(len(podium), 10):]
		txtlist = []
		for (emoji, count) in top:
			txtlist.append(f"\t{emoji} {round(100.0*count/total, 2)}%")
		txtlist.append(" ".join([otheremo for (otheremo, count) in other]))
		await ctx.channel.send(f"Emoji Podium:\n"+"\n".join(txtlist))

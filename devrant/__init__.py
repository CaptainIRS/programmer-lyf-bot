"""
Contains the APIs for getting rants from devrant
"""

from discord import embeds
from .fetch import fetch_rants_json


def get_rants(frequency: str, limit: int):
    """
    Gets rants for given frequency
    """
    period = ''
    if frequency == 'daily':
        period = 'day'
    elif frequency == 'weekly':
        period = 'week'
    embed_objects = []
    rants_json = fetch_rants_json(period, limit)
    if rants_json:
        for rant in rants_json:
            embed_object = embeds.Embed(
                name='hello',
                description=rant['text'],
                color=0xf99a66,
            ).set_author(
                name='devRant',
                url='https://devrant.com',
                icon_url='https://devrant.com/static/devrant/img/favicon32.png'
            ).add_field(
                name='Hello',
                value=f'![{rant["attached_image"]}]({rant["attached_image"]})',
                inline=False
            ).set_footer(
                text=f'By {rant["user_username"]}',
                icon_url=f'https://avatars.devrant.com/{rant["user_avatar"]["i"]}'
            )
            if rant['attached_image'] != '':
                embed_object.add_field(
                    name='Hello',
                    value=f'![{rant["attached_image"]}]({rant["attached_image"]})',
                    inline=False
                )
            embed_objects.append(embed_object)
    return embed_objects

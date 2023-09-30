'''
Custom markdown implementation
'''

from markdown import markdown
from markdownify import MarkdownConverter
from telegram.helpers import escape_markdown


class _CustomMarkdownConverter(MarkdownConverter):
    def escape(self, text):
        '''Escape markdown'''
        if not text:
            return ''
        return escape_markdown(text)

    def convert_hn(self, _, __, text, convert_as_inline):
        '''Convert headings to bold markdown'''
        if convert_as_inline:
            return text
        return f'**{text}** \n\n'

    def convert_img(self, _, __, ___):
        '''Ignore images'''
        return ''


def markdownify(html, **options):
    '''
    Custom markdownify
    '''
    return _CustomMarkdownConverter(**options).convert(html)


def htmlify(markdown_string):
    '''
    Custom htmlify
    '''
    html = markdown(markdown_string).replace('<p>', '').replace('</p>', '\n')
    html = html.replace('<blockquote>', '<i>').replace('</blockquote>', '</i>\n')
    html = html.replace('<ul>', '').replace('</ul>', '\n')
    html = html.replace('<ol>', '').replace('</ol>', '\n')
    html = html.replace('<li>', '• ').replace('</li>', '\n')
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html = html.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    html = html.replace('<h1>', '<b>').replace('</h1>', '</b>')
    html = html.replace('<h2>', '<b>').replace('</h2>', '</b>')
    html = html.replace('<h3>', '<b>').replace('</h3>', '</b>')
    html = html.replace('<h4>', '<b>').replace('</h4>', '</b>')
    html = html.replace('<h5>', '<b>').replace('</h5>', '</b>')
    html = html.replace('<h6>', '<b>').replace('</h6>', '</b>')
    return html

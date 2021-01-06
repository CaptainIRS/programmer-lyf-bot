'''
Custom markdown implementation
'''

from markdownify import MarkdownConverter


class _CustomMarkdownConverter(MarkdownConverter):
    def convert_hn(self, _, __, text, convert_as_inline):
        '''Convert headings to bold markdown'''
        if convert_as_inline:
            return text
        return '**%s** \n\n' % text

    def convert_img(self, _, __, ___):
        '''Ignore images'''
        return ''


def markdownify(html, **options):
    '''
    Custom markdownify
    '''
    return _CustomMarkdownConverter(**options).convert(html)

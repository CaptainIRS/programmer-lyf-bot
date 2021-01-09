'''
Custom markdown implementation
'''

from markdownify import MarkdownConverter


class _CustomMarkdownConverter(MarkdownConverter):
    def convert_hn(self, n, el, text, convert_as_inline):
        if convert_as_inline:
            return text
        return '**%s** \n\n' % text

    def convert_img(self, el, text, convert_as_inline):
        return ''


def markdownify(html, **options):
    '''
    Custom markdownify
    '''
    return _CustomMarkdownConverter(**options).convert(html)

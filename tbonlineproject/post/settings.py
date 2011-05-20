"""Developer definable settings for enhancedtext app
"""

from django.conf import settings

MARKDOWN_EXTENSIONS = getattr(settings, 'ENHANCEDTEXT_MARKDOWN_EXTENSIONS', 
                        'safe,abbr,tables,def_list,footnotes')


POSTS_PER_PAGE = getattr(settings,'POST_POSTS_PER_PAGE', 10)

COMMENTS_MODERATED = getattr(settings,'POST_COMMENTS_MODERATED', False)

MODERATION_FREE_DAYS = getattr(settings,'POST_MODERATION_FREE_DAYS', 0) 

AUTHENTICATED_COMMENTS_ONLY = getattr(settings, 'POST_AUTHENTICATED_COMMENTS_ONLY', False)

CLOSE_COMMENTS_AFTER = getattr(settings, 'POST_CLOSE_COMMENTS_AFTER', 0)

EMAIL_COMMENTS = getattr(settings, 'POST_EMAIL_COMMENTS', True)

TRUNCATE_WORDS = getattr(settings, 'POST_TRUNCATE_WORDS', 95)

from django.utils.translation import ugettext as _

CONTENT_FORMATS = (
    ('\P', _('Plain text')),
    ('\E', _('Plain text with URLs and line breaks')),
    ('\R', _('reStructuredText')),    
    ('\M', _('Markdown')),
    ('\T', _('Textile')),
    ('\H', _('HTML')),    
    ('\W', _('HTML editor')),  
)

DEFAULT_FORMAT = getattr(settings, 'ENHANCEDTEXT_DEFAULT_FORMAT', 
                       CONTENT_FORMATS[0][0])

MARKDOWN_EXTENSIONS = getattr(settings, 'ENHANCEDTEXT_MARKDOWN_EXTENSIONS', 
                        'abbr,tables,def_list,footnotes,urlize')


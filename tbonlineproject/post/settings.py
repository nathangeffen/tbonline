from django.conf import settings
"""Developer definable settings for enhancedtext app
"""

MARKDOWN_EXTENSIONS = getattr(settings, 'ENHANCEDTEXT_MARKDOWN_EXTENSIONS', 
                        'safe,abbr,tables,def_list,footnotes')



POSTS_PER_PAGE = getattr(settings,'POST_POSTS_PER_PAGE', 10)

COMMENTS_MODERATED = getattr(settings,'POST_COMMENTS_MODERATED', False)

MODERATION_FREE_DAYS = getattr(settings,'POST_MODERATION_FREE_DAYS', 0) 

AUTHENTICATED_COMMENTS_ONLY = getattr(settings, 'POST_AUTHENTICATED_COMMENTS_ONLY', False)

CLOSE_COMMENTS_AFTER = getattr(settings, 'POST_CLOSE_COMMENTS_AFTER', 0)

EMAIL_COMMENTS = getattr(settings, 'POST_EMAIL_COMMENTS', True)


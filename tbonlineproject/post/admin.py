'''Admin interface for posts.
'''

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.comments.models import Comment, CommentFlag
from django.contrib.comments.admin import CommentsAdmin
from django import forms

from tagging.models import Tag  

from post.models import BasicPost, PostWithImage, PostWithSlideshow

from archive.admin import TaggedItemInline

from credit.admin import OrderedCreditInline

from relatedcontent.admin import RelatedContentInline

from enhancedtext.admin import enhancedtextcss, enhancedtextjs


post_fieldsets = (
        (_('Title'), {
            'classes' : ['collapse open'],    
            'fields': ('title', 'subtitle','slug','date_published'),
        }),
        
        (_('Content'), {
         'classes' : ['collapse open',],
         'fields': ('body',)
        }),

        (_('Teaser. introduction and pullout text'), {
         'classes' : ['collapse closed',],
         'fields': ('teaser','introduction', 'pullout_text',)
        }),

        (_('Display features'), {
         'classes' : ['collapse closed',],
         'fields': ('homepage','sticky','allow_comments', 'copyright')
        }),
                 
        (_('HTML templates'), {
         'classes' : ['collapse closed',],
         'fields': ('single_post_template','many_post_template')
        }),
        
    )


class BasicPostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'teaser', 'body')
    list_display = ('render_admin_url', 'title', 'date_published', 'is_published', 'date_added', 'last_modified')
    list_editable = ('title', 'date_published')
    list_filter = ('date_published',)
    date_hierarchy = 'date_published'
    prepopulated_fields = {"slug": ("title",)}
    inlines = [OrderedCreditInline, TaggedItemInline, RelatedContentInline]
    ordering = ('-last_modified',)

    fieldsets = post_fieldsets

    
    class Media:
        css = enhancedtextcss 
        js = enhancedtextjs

class PostWithImageAdmin(BasicPostAdmin):
    list_display = ('id', 'title', 'image_thumbnail', 'date_published', 'is_published', 'date_added', 'last_modified')
    raw_id_fields = ['image',]
    related_lookup_fields = {
        'fk': ['image'],
    }    
    

    fieldsets = post_fieldsets[0:3] + \
        ((_('Image'), {
         'classes' : ['collapse open',],
         'fields': ('image', ('single_post_width','single_post_height',), 
                    ('many_post_width','many_post_height',),)
        }),) + \
        post_fieldsets[3:]

class PostWithSlideshowAdmin(BasicPostAdmin):
    list_display = ('id', 'title', 'slideshow_thumbnail', 'date_published', 'is_published', 'date_added', 'last_modified')
    raw_id_fields = ['gallery',]
    related_lookup_fields = {
        'fk': ['gallery'],
    }    
    

    fieldsets = post_fieldsets[0:3] + \
        ((_('Gallery to use for slideshow'), {
         'classes' : ['collapse open',],
         'fields': ('gallery', ('single_post_width','single_post_height',), 
                    ('many_post_width','many_post_height',),)
        }),) + \
        post_fieldsets[3:]
    
    


class FlatPageForm(forms.ModelForm):
    model = FlatPage
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]
            
class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm 

class CustomCommentAdmin(CommentsAdmin):
    list_display = ('id', 'name', 'content_type', 'object_pk', 'ip_address', 'submit_date', 'is_public', 'is_removed')

admin.site.register(BasicPost, BasicPostAdmin)
admin.site.register(PostWithImage, PostWithImageAdmin)
admin.site.register(PostWithSlideshow, PostWithSlideshowAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

admin.site.unregister(Comment)
admin.site.register(Comment, CustomCommentAdmin)
admin.site.register(CommentFlag)

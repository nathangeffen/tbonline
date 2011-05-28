"""Implements an enhanced Django TextField called EnhancedTextField that stores 
the format of the object, e.g. HTML, Markdown, plain text etc. 

It can also render the EnhancedTextField in the appropriate format or in HTML.

"""
       
from django.db import models
from django.utils.translation import ugettext as _
from django import forms
from django.utils.html import escape, urlize, linebreaks
from django.contrib.markup.templatetags.markup import restructuredtext, markdown, textile
from django.utils.safestring import mark_safe

from post.settings import CONTENT_FORMATS, DEFAULT_FORMAT, MARKDOWN_EXTENSIONS


class EnhancedText(object):
    """Python object that stores a unicode string and a one character field
    indicating the format of that string.  
    """

    def to_tuple(self):
        return self.text, self.text_format

    def to_string(self):
        return self.text + self.text_format
    
    @staticmethod
    def separate_text(value, initial_format):
        """Takes a string parameter and returns a tuple of
        text and text_format. 
        
        If the last two characters in value equal are a CONTENT_FORMAT
        then text is set equal to everything but the last two characters and 
        text_format is set equal to the last two characters.
        
        In all other cases, text is set to the same value as the parameter (unless 
        it is None, in which case text is set equal to "")  and content_format is 
        set equal to DEFAULT_FORMAT.  
        """
        if value is None or value == "":
            return "", initial_format
        elif len(value) == 1:
            return value, initial_format
        elif value[-2:] in [c[0] for c in CONTENT_FORMATS]:
            return value[:-2], value[-2:]
        else:
            return value, initial_format 

    def __init__(self, value, initial_format=DEFAULT_FORMAT):
        """Initialises the two fields that define this object:
            text: carries the actual text
            text_format: indicates the format of the text
        """
        self.text, self.text_format = self.separate_text(value, initial_format)
        
    def __unicode__(self):
        """It is this method that is responsible for rendering the 
        object in HTML.
        """ 
        if self.text_format == '\E':
            return linebreaks(urlize(escape(self.text)))
        elif self.text_format == '\T':
            return textile(self.text)
        elif self.text_format == '\M':
            return markdown(self.text, MARKDOWN_EXTENSIONS)
        elif self.text_format == '\R':
            return restructuredtext(self.text)
        elif self.text_format == '\H' or self.text_format == '\W':
            return mark_safe(self.text)
        else:
            return mark_safe(escape(self.text))

class EnhancedTextWidget(forms.MultiWidget):
    """A multi-widget for the EnhancedTextFormField that renders a Textarea and
    a select widget for choosing the format of the Textarea.  
    """
    def __init__(self, 
                 textareaattrs={'class': 'enhanced_text'},
                 selectattrs={'class' : 'enhanced_text_format',},
                 initial=None):
        """Specify the two types of widgets that comprise this multi-widget.
        """
        self.initial=initial
        
        widgets = (forms.Textarea(attrs=textareaattrs), 
                   forms.Select(attrs=selectattrs, choices=CONTENT_FORMATS))
        super(EnhancedTextWidget, self).__init__(widgets, None)

    def decompress(self, value):
        """Returns a tuple of the Textarea and the format
        """
        if isinstance(value, EnhancedText):
            return value.to_tuple()
        elif value:
            return EnhancedText(value).to_tuple()
        elif self.initial:
            return self.initial.to_tuple()
        else:
            return EnhancedText("", DEFAULT_FORMAT).to_tuple()
        
    def render(self, name, value, attrs=None):
        """Renders a Textarea and a Select widget. 
        """     
        try: #It's an EnhancedText that must be converted to a string
            value = value.to_string()
        except: # It's probably None
            value = ""
        output = super(EnhancedTextWidget, self).render(name, value, attrs)
        return output

    def format_output(self, rendered_widgets):
        return u''.join([rendered_widgets[0],
                         u"<p/>",
                         rendered_widgets[1],
                         u'<label>',
                         _('Words: '),
                         u'<span class="wordcount">',
                         _('0'),
                         u'</span>',
                         u'&nbsp;&nbsp;&nbsp;',
                         _('Characters: '),
                         u'<span class="charcount">',
                         _('0'),
                         u'</span>'
                         u'</label>',
                         ])


class EnhancedTextFormField(forms.MultiValueField):
    """Form field for representing EnhancedTextField.
    """
    
    def __init__(self, *args, **kwargs):
        self.fields = (forms.CharField(), forms.CharField(),)
        if "initial" in kwargs: 
                initial = kwargs["initial"]
        else:
            initial = None
            
        self.widget = EnhancedTextWidget(initial=initial)
        super(EnhancedTextFormField, self).__init__(self.fields, *args, **kwargs)
    
    def compress(self, data_list):
        if data_list:
            return data_list[0] + data_list[1]
        return ""

class EnhancedTextField(models.Field):
    """A TextField that supports various input formats and renders them 
    appropriately."""

    description = _('TextField that supports various input formats and renders them')
 
    __metaclass__ = models.SubfieldBase


    def __init__(self, *args, **kwargs):
        #if "default" in kwargs:
        #    self.default = kwargs["default"]
        #else:
        #    self.default = None
            
        super(EnhancedTextField, self).__init__( *args, **kwargs)
    
    def get_internal_type(self):
        return "TextField"    
    
    def to_python(self, value):
        """Converts the database value to an EnhancedText instance
        """ 
        if isinstance(value, EnhancedText):
            return value
        else:
            return EnhancedText(value)

    def get_prep_value(self, value):
        """Converts an EnhancedText instance to plain text for the database.
        """
        return value.to_string()

    def formfield(self, **kwargs):
        """Specify the form and widget for the EnhancedTextField.
        """
        defaults = {'form_class': EnhancedTextFormField,
                    "initial": self.default,
                    }
        defaults.update(kwargs)
        return super(EnhancedTextField, self).formfield(**defaults)



# Make this friendly for South for apps that use it.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^enhancedtext\.fields\.EnhancedTextField'])
except:
    pass

from framework import config
from framework import security

settings = config.Config()

def set_responsive_image(src='', _type='image', alt=''):
    path = security.set_absolute_path(src)
    sizes = getattr(settings, _type)

    if settings.production:
        template = \
            '<img class="smallImage"      src="http://src.sencha.io/jpg{quality}/{wsmall}/{small}/{path}" alt="{altText}" height="{small}" />'\
            '<img class="mediumImage"     src="http://src.sencha.io/jpg{quality}/{wmedium}/{medium}/{path}" alt="{altText}" height="{medium}" />'\
            '<img class="largeImage"      src="http://src.sencha.io/jpg{quality}/{wlarge}/{large}/{path}" alt="{altText}" height="{large}" />'\
            '<img class="extralargeImage" src="http://src.sencha.io/jpg{quality}/{wextralarge}/{extralarge}/{path}" alt="{altText}" height="{extralarge}" />'
    else:
        template = \
            '<img class="smallImage"      src="{path}" alt="{altText}" height="{small}" />'\
            '<img class="mediumImage"     src="{path}" alt="{altText}" height="{medium}" />'\
            '<img class="largeImage"      src="{path}" alt="{altText}" height="{large}" />'\
            '<img class="extralargeImage" src="{path}" alt="{altText}" height="{extralarge}" />'
    return template.format(
        path=path
        ,altText=alt
        ,small=sizes['small']
        ,medium=sizes['medium']
        ,large=sizes['large']
        ,extralarge=sizes['extralarge']
        ,wsmall=round(sizes['small']*16/9)
        ,wmedium=round(sizes['medium']*16/9)
        ,wlarge=round(sizes['large']*16/9)
        ,wextralarge=round(sizes['extralarge']*16/9)
        ,quality=settings.JPGQuality)


def set_video(src='', _type='normal'):
    path = security.set_absolute_path(src)
    if _type is 'normal':
        sizes = settings.image
    elif _type is 'thumbnail':
        sizes = settings.thumbnail
    template = \
        '<iframe class="smallImage"      height="315" src="{youtube_url}" frameborder="0" allowfullscreen></iframe>'\
        '<iframe class="mediumImage"     height="315" src="{youtube_url}" frameborder="0" allowfullscreen></iframe>'\
        '<iframe class="largeImage"      height="315" src="{youtube_url}" frameborder="0" allowfullscreen></iframe>'\
        '<iframe class="extralargeImage" height="315" src="{youtube_url}" frameborder="0" allowfullscreen></iframe>'
    return template.format(
        path=path
        ,altText=alt
        ,small=sizes['small']
        ,medium=sizes['medium']
        ,large=sizes['large']
        ,extralarge=sizes['extralarge'])
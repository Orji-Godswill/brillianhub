from django.http import HttpRequest


def seo_attrs(request: HttpRequest):

    return {
        'seo_title': 'Training hub for investors',
        'seo_description': 'Brillianzhub - Financial and investment training hub',
        'og_type': 'website',
        'og_title': 'training hub for investors',
        'og_url': 'https://www.brillianzhub.com',
        'og_description': 'Brillianzhub - Financial and investment training hub',
        'og_image': '#',
        'og_site_name': 'brillianzhub.com'
    }

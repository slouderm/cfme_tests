""" A page functions for Availability Zone


:var list_page: A :py:class:`cfme.web_ui.Region` object describing elements on the list page.
:var details_page: A :py:class:`cfme.web_ui.Region` object describing elements on the detail page.
"""

from cfme.web_ui import Region, Table


# Page specific locators
list_page = Region(
    locators={
        'zone_table': Table(header_data=('//div[@class="xhdr"]/table', 1),
                            row_data=('//div[@class="objbox"]/table', 1))
    },
    title='CloudForms Management Engine: Cloud Providers')


details_page = Region(infoblock_type='detail')
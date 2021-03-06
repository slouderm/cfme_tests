# -*- coding: utf-8 -*-
"""Module handling Dashboard Widgets accordion.

"""
from cfme.fixtures import pytest_selenium as sel
from cfme.intelligence.reports.ui_elements import ExternalRSSFeed, MenuShortcuts, Timer
from cfme.web_ui import CheckboxSelect, Form, Select, ShowingInputs, accordion, fill, toolbar
from cfme.web_ui import flash, form_buttons
from cfme.web_ui.menu import nav
from utils.update import Updateable
from utils.pretty import Pretty


nav.add_branch(
    "reports",
    {
        "reports_widgets_menus":
        [
            lambda _: accordion.tree("Dashboard Widgets", "All Widgets", "Menus"),
            {
                "reports_widgets_menu_add":
                lambda _: toolbar.select("Configuration", "Add a new Widget")
            }
        ],

        "reports_widgets_menu":
        [
            lambda ctx:
            accordion.tree("Dashboard Widgets", "All Widgets", "Menus", ctx["widget"].title),
            {
                "reports_widgets_menu_delete":
                lambda _: toolbar.select("Configuration", "Delete this Widget from the Database"),

                "reports_widgets_menu_edit":
                lambda _: toolbar.select("Configuration", "Edit this Widget"),
            }
        ],

        "reports_widgets_reports":
        [
            lambda _: accordion.tree("Dashboard Widgets", "All Widgets", "Reports"),
            {
                "reports_widgets_report_add":
                lambda _: toolbar.select("Configuration", "Add a new Widget")
            }
        ],

        "reports_widgets_report":
        [
            lambda ctx:
            accordion.tree("Dashboard Widgets", "All Widgets", "Reports", ctx["widget"].title),
            {
                "reports_widgets_report_delete":
                lambda _: toolbar.select("Configuration", "Delete this Widget from the Database"),

                "reports_widgets_report_edit":
                lambda _: toolbar.select("Configuration", "Edit this Widget"),
            }
        ],

        "reports_widgets_charts":
        [
            lambda _: accordion.tree("Dashboard Widgets", "All Widgets", "Charts"),
            {
                "reports_widgets_chart_add":
                lambda _: toolbar.select("Configuration", "Add a new Widget")
            }
        ],

        "reports_widgets_chart":
        [
            lambda ctx:
            accordion.tree("Dashboard Widgets", "All Widgets", "Charts", ctx["widget"].title),
            {
                "reports_widgets_chart_delete":
                lambda _: toolbar.select("Configuration", "Delete this Widget from the Database"),

                "reports_widgets_chart_edit":
                lambda _: toolbar.select("Configuration", "Edit this Widget"),
            }
        ],

        "reports_widgets_rss_feeds":
        [
            lambda _: accordion.tree("Dashboard Widgets", "All Widgets", "RSS Feeds"),
            {
                "reports_widgets_rss_feed_add":
                lambda _: toolbar.select("Configuration", "Add a new Widget")
            }
        ],

        "reports_widgets_rss_feed":
        [
            lambda ctx:
            accordion.tree("Dashboard Widgets", "All Widgets", "RSS Feeds", ctx["widget"].title),
            {
                "reports_widgets_rss_feed_delete":
                lambda _: toolbar.select("Configuration", "Delete this Widget from the Database"),

                "reports_widgets_rss_feed_edit":
                lambda _: toolbar.select("Configuration", "Edit this Widget"),
            }
        ],
    }
)


visibility_obj = ShowingInputs(
    Select("//select[@id='visibility_typ']"),
    CheckboxSelect("//div[@id='form_role_visibility']//table/"
                   "tbody/tr/td[not(contains(@class, 'key'))]/table"),
    min_values=1
)


class MenuWidget(Updateable, Pretty):
    form = Form(fields=[
        ("title", "//input[@id='title']"),
        ("description", "//input[@id='description']"),
        ("active", "//input[@id='enabled']"),
        ("shortcuts", MenuShortcuts("//select[@id='add_shortcut']")),
        ("visibility", visibility_obj),
    ])
    pretty_attrs = ['description', 'shortcuts', 'visibility']

    def __init__(self, title, description=None, active=None, shortcuts=None, visibility=None):
        self.title = title
        self.description = description
        self.active = active
        self.shortcuts = shortcuts
        self.visibility = visibility

    def create(self, cancel=False):
        sel.force_navigate("reports_widgets_menu_add")
        fill(self.form, self.__dict__, action=form_buttons.cancel if cancel else form_buttons.add)
        flash.assert_no_errors()

    def update(self, updates):
        sel.force_navigate("reports_widgets_menu_edit", context={"widget": self})
        fill(self.form, updates, action=form_buttons.save)
        flash.assert_no_errors()

    def delete(self, cancel=False):
        sel.force_navigate("reports_widgets_menu", context={"widget": self})
        toolbar.select("Configuration", "Delete this Widget from the Database", invokes_alert=True)
        sel.handle_alert(cancel)
        flash.assert_no_errors()


class ReportWidget(Updateable):
    form = Form(fields=[
        ("title", "//input[@id='title']"),
        ("description", "//input[@id='description']"),
        ("active", "//input[@id='enabled']"),
        ("filter", ShowingInputs(
            Select("//select[@id='filter_typ']"),
            Select("//select[@id='subfilter_typ']"),
            Select("//select[@id='repfilter_typ']"),
            min_values=3
        )),  # Might be abstracted out too
        ("columns", ShowingInputs(
            Select("//select[@id='chosen_pivot1']"),
            Select("//select[@id='chosen_pivot2']"),
            Select("//select[@id='chosen_pivot3']"),
            Select("//select[@id='chosen_pivot4']"),
            min_values=1
        )),
        ("rows", Select("//select[@id='row_count']")),
        ("timer", Timer()),
        ("visibility", visibility_obj),
    ])
    pretty_attrs = ['description', 'filter', 'visibility']

    def __init__(self,
            title, description=None, active=None, filter=None, columns=None, rows=None, timer=None,
            visibility=None):
        self.title = title
        self.description = description
        self.active = active
        self.filter = filter
        self.columns = columns
        self.rows = rows
        self.timer = timer
        self.visibility = visibility

    def create(self, cancel=False):
        sel.force_navigate("reports_widgets_report_add")
        fill(self.form, self.__dict__, action=form_buttons.cancel if cancel else form_buttons.add)
        flash.assert_no_errors()

    def update(self, updates):
        sel.force_navigate("reports_widgets_report_edit", context={"widget": self})
        fill(self.form, updates, action=form_buttons.save)
        flash.assert_no_errors()

    def delete(self, cancel=False):
        sel.force_navigate("reports_widgets_report", context={"widget": self})
        toolbar.select("Configuration", "Delete this Widget from the Database", invokes_alert=True)
        sel.handle_alert(cancel)
        flash.assert_no_errors()


class ChartWidget(Updateable, Pretty):
    form = Form(fields=[
        ("title", "//input[@id='title']"),
        ("description", "//input[@id='description']"),
        ("active", "//input[@id='enabled']"),
        ("filter", Select("//select[@id='repfilter_typ']")),
        ("timer", Timer()),
        ("visibility", visibility_obj),
    ])
    pretty_attrs = ['title', 'description', 'filter', 'visibility']

    def __init__(self,
            title, description=None, active=None, filter=None, timer=None, visibility=None):
        self.title = title
        self.description = description
        self.active = active
        self.filter = filter
        self.timer = timer
        self.visibility = visibility

    def create(self, cancel=False):
        sel.force_navigate("reports_widgets_chart_add")
        fill(self.form, self.__dict__, action=form_buttons.cancel if cancel else form_buttons.add)
        flash.assert_no_errors()

    def update(self, updates):
        sel.force_navigate("reports_widgets_chart_edit", context={"widget": self})
        fill(self.form, updates, action=form_buttons.save)
        flash.assert_no_errors()

    def delete(self, cancel=False):
        sel.force_navigate("reports_widgets_chart", context={"widget": self})
        toolbar.select("Configuration", "Delete this Widget from the Database", invokes_alert=True)
        sel.handle_alert(cancel)
        flash.assert_no_errors()


class RSSFeedWidget(Updateable, Pretty):
    form = Form(fields=[
        ("title", "//input[@id='title']"),
        ("description", "//input[@id='description']"),
        ("active", "//input[@id='enabled']"),
        ("type", Select("//select[@id='feed_type']")),
        ("feed", Select("//select[@id='rss_feed']")),
        ("external", ExternalRSSFeed()),
        ("rows", Select("//select[@id='row_count']")),
        ("timer", Timer()),
        ("visibility", visibility_obj),
    ])
    pretty_attrs = ['title', 'description', 'type', 'feed', 'visibility']

    def __init__(self,
            title, description=None, active=None, type=None, feed=None, external=None, rows=None,
            timer=None, visibility=None):
        self.title = title
        self.description = description
        self.active = active
        self.type = type
        self.feed = feed
        self.external = external
        self.rows = rows
        self.timer = timer
        self.visibility = visibility

    def create(self, cancel=False):
        sel.force_navigate("reports_widgets_rss_feed_add")
        fill(self.form, self.__dict__, action=form_buttons.cancel if cancel else form_buttons.add)
        flash.assert_no_errors()

    def update(self, updates):
        sel.force_navigate("reports_widgets_rss_feed_edit", context={"widget": self})
        fill(self.form, updates, action=form_buttons.save)
        flash.assert_no_errors()

    def delete(self, cancel=False):
        sel.force_navigate("reports_widgets_rss_feed", context={"widget": self})
        toolbar.select("Configuration", "Delete this Widget from the Database", invokes_alert=True)
        sel.handle_alert(cancel)
        flash.assert_no_errors()

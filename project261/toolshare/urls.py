"""
File:       toolshare/urls.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

Contains URLs for the toolshare app.
"""

from django.conf.urls import patterns, url

#Tool URLs
urlpatterns = patterns('',

    # Error URLs
    url(r'^401/$', 'toolshare.views.not_approved', name='not_approved'),

    # Our admin panel URLs
    url(r'^admin/$', 'toolshare.views.admin', name='admin'),
    url(r'^admin/profile/(?P<user_id>\d+)/$', 'toolshare.views.admin_edit_user', name='admin_edit_user'),
    url(r'^admin/sharezone/(?P<sharezone_id>\d+)/$', 'toolshare.views.admin_edit_sharezone', name='admin_edit_sharezone'),
    url(r'^admin/ban_user/(?P<user_id>\d+)/$', 'toolshare.actions.banUser', name='ban_user'),
    url(r'^admin/unban_user/(?P<user_id>\d+)/$', 'toolshare.actions.unbanUser', name='unban_user'),
    url(r'^admin/approve_user/(?P<user_id>\d+)/$', 'toolshare.actions.approveUser', name='approve_user'),
    url(r'^admin/make_sharezone_admin/(?P<user_id>\d+)/$', 'toolshare.actions.makeSharezoneAdmin', name='make_sharezone_admin'),
    url(r'^admin/remove_sharezone_admin/(?P<user_id>\d+)/$', 'toolshare.actions.removeSharezoneAdmin', name='remove_sharezone_admin'),
    #url(r'^admin/remove_sharezone/(?P<sharezone_id>\d+)/$', 'toolshare.actions.removeSharezone', name='remove_sharezone'),
    url(r'^admin/approve_sharezone/(?P<sharezone_id>\d+)/$', 'toolshare.actions.approveSharezone', name='approve_sharezone'),

    # Home page
    url(r'^$', 'toolshare.views.home', name='home'),

    # Tool URLs
    url(r'^tool/list/$', 'toolshare.views.tool_list', name='tool_list'),
    url(r'^tool/register/$', 'toolshare.views.tool_register', name='tool_register'),
    url(r'^tool/info/(?P<tool_id>\d+)/$', 'toolshare.views.tool_info', name='tool_info'),
    url(r'^tool/info/edit/(?P<tool_id>\d+)/$', 'toolshare.views.tool_edit', name='tool_edit'),
    url(r'^tool/info/return/(?P<tool_id>\d+)/$', 'toolshare.views.tool_return_quality', name='tool_return_quality'),
    url(r'^tool/reserve/(?P<tool_id>\d+)/$', 'toolshare.views.tool_reserve', name='tool_reserve'),
    url(r'^tool/return/(?P<tool_id>\d+)/$', 'toolshare.actions.returnTool', name='returnTool'),
    url(r'^tool/remove/(?P<tool_id>\d+)/$', 'toolshare.actions.removeTool', name='removeTool'),

    # ToolGroup URLs
    url(r'^toolgroup/$', 'toolshare.views.toolgroup', name='toolgroup'),
    url(r'^toolgroup/edit/(?P<toolgroup_id>\d+)/$', 'toolshare.views.toolgroup_edit', name='toolgroup_edit'),

    # User URLs
    url(r'^user/list$', 'toolshare.views.user_list', name='user_list'),
    url(r'^user/profile/(?P<user_id>\d+)/$', 'toolshare.views.user_profile', name='user_profile'),
    url(r'^user/profile/$', 'toolshare.views.user_profile_mine', name='user_profile_mine'),
    url(r'^user/profile/edit/$', 'toolshare.views.user_profile_edit', name='user_profile_edit'),

    # Sharezone URLs
    url(r'^sharezone/$', 'toolshare.views.sharezone', name='sharezone'),
    url(r'^sharezone/(?P<sharezone_id>\d+)/$', 'toolshare.views.sharezone', name='sharezone'),
    url(r'^sharezone/tools/$', 'toolshare.views.sharezone_tools', name='sharezone_tools'),
    url(r'^sharezone/create/$', 'toolshare.views.sharezone_create', name='sharezone_create'),
    #url(r'^sharezone/info$', 'toolshare.views.sharezone_info', name='sharezone_info'),
    url(r'^sharezone/edit/$', 'toolshare.views.sharezone_edit', name='sharezone_edit'),
    #url(r'^sharezone/members/$', 'toolshare.views.sharezone_members', name='sharezone_members'),

    # Sharezone URLs
    #url(r'^sharezone/$', 'toolshare.views.sharezone', name='sharezone'),
)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Category, Topic, \
        Post, LBForumUserProfile, gen_last_post_info

admin.site.register(Category)

class PostInline(admin.TabularInline):
    model = Post

def update_topic_state_info(modeladmin, request, queryset):
    for topic in queryset:
        topic.update_state_info()
update_topic_state_info.short_description = _("Update topic state info")

def update_topic_attr_as_not(modeladmin, request, queryset, attr):
    for topic in queryset:
        if attr == 'sticky':
            topic.sticky = not topic.sticky
        elif attr == 'close':
            topic.closed = not topic.closed
        elif attr == 'hide':
            topic.hidden = not topic.hidden
        topic.save()

def sticky_unsticky_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'sticky')
sticky_unsticky_topic.short_description = _("sticky/unsticky topics")

def close_unclose_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'close')
close_unclose_topic.short_description = _("close/unclose topics")

def hide_unhide_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'hide')
hide_unhide_topic.short_description = _("hide/unhide topics")

class TopicAdmin(admin.ModelAdmin):
    list_display        = ('subject', 'posted_by', 'sticky', 'closed',
            'hidden', 'level', 'num_views', 'num_replies', 'created_on', 'updated_on', )
    list_filter         = ('sticky', 'closed', 'hidden', 'level')
    search_fields       = ('subject', 'posted_by__username', )
    #inlines             = (PostInline, )
    actions = [update_topic_state_info, sticky_unsticky_topic, close_unclose_topic, 
            hide_unhide_topic]

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display        = ('__unicode__', 'topic', 'posted_by', 'poster_ip', \
            'created_on', 'updated_on', )
    search_fields       = ('topic__subject', 'posted_by__username', 'message', )

admin.site.register(Post, PostAdmin)

class LBForumUserProfileAdmin(admin.ModelAdmin):
    list_display        = ('user', 'userrank', 'last_activity', 'last_posttime', \
            'signature', )
    search_fields       = ('user__username', 'userrank', )

admin.site.register(LBForumUserProfile, LBForumUserProfileAdmin)

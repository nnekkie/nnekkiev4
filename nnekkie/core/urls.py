from django.urls import path 
from core import views 

app_name = "core"

urlpatterns = [
    path("", views.index, name="feed"),
    # path('', views.pwa, name='pwa'),
    path("delete-post/", views.delete_post, name='delete-post'),
    path("post/<slug:slug>/", views.post_detail, name="post-detail"),
    
    # path("post/delete", views.delete_post, name="delete-post"),
    #group related index
    path('core/group-index/', views.group_index, name='group-index'),
    # Chat Feature
    path("core/inbox/", views.inbox, name="inbox"),
    path("core/inbox/<username>/", views.inbox_detail, name="inbox_detail"),

    # Group CHat
    path("core/group-inbox/", views.group_inbox, name="group_inbox"),
    path("core/group-inbox/<slug:slug>/", views.group_inbox_detail, name="group_inbox_detail"),

    # Join & leave Group
    path("core/join-group-page/<slug:slug>/", views.join_group_chat_page, name="join_group_chat_page"),
    path("core/join-group/<slug:slug>/", views.join_group_chat, name="join_group"),
    path("core/leave-group/<slug:slug>/", views.leave_group_chat, name="leave_group_chat"),

    # Games
    path("core/all-games/", views.games, name="games"),
    path("core/stack_brick/", views.stack_brick, name="stack_brick"),

    # Search
    path('search/', views.search_users, name='search_users'),

    # Load more post
    path('load_more_posts/', views.load_more_posts, name='load_more_posts'),




    # Ajax URLs
    path("create-post/", views.create_post, name="create-post"),
    path("edit-post/<int:id>/", views.edit_post, name="edit-post"),
    path("like-post/", views.like_post, name="like-post"),
    path("comment-post/", views.comment_on_post, name="comment-post"),
    path("like-comment/", views.like_comment, name="like-comment"),
    path("reply-comment/", views.reply_comment, name="reply-comment"),
    path("delete-comment/", views.delete_comment, name="delete-comment"),
    path("add-friend/", views.add_friend, name="add-friend"),
    path("accept-friend-request/", views.accept_friend_request, name="accept-friend-request"),
    path("reject-friend-request/", views.reject_friend_request, name="reject-friend-request"),
    path("unfriend/", views.unfriend, name="unfriend"),
    path("block-user/", views.block_user, name="block_user"),
    #Ajax urls for snaps
    path('create-snaps/', views.create_snaps, name='create-snaps'),
    


    #urls for group related actuvity
    path("like-group-post/", views.like_group_post, name="like-group-post"),
    path("comment-group-post/", views.comment_group_post, name="comment-group-post"),
    path("like-comment-group-post/", views.like_comment_group_post, name="like-comment-group-post"),
    # reply_group_comment
    path("reply-comment-group-post/", views.reply_group_comment, name="reply-comment-group-post"),
    # delete_group_comment
    path("delete-group-post-comment/", views.delete_group_comment, name="delete-group-post-comment"),
    path("core/group/post/<slug:slug>/", views.group_post_details, name="group-post-detail"),
    path("core/group-profile/", views.my_group_profile, name="group-profile"),

    # group related feature
    path('core/group-suggesions/', views.group_suggestions, name='group-suggestions')
    
]
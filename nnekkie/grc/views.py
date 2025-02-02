from django.shortcuts import render, get_object_or_404, redirect
from .models import GroupChat, GroupChatMessage
from django.contrib.auth.decorators import login_required
from .forms import ChatMessageCreateForm

@login_required
def index(request, slug):
    chat_group = get_object_or_404(GroupChat, slug=slug)
    chat_messages = chat_group.group_chat.all()

    # Handle POST request for form submission
    if request.method == "POST":
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.groupchat = chat_group
            message.save()
            return redirect('grc:index', slug=slug)  # Redirect back to the same page to display the new message

    else:
        form = ChatMessageCreateForm()

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'grc/chats-group.html', context)

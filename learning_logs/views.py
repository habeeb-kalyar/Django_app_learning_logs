from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Helper function to check ownership OR superuser status
def check_topic_owner(request, topic):
    """Raise 404 if the user doesn't own the topic AND isn't a superuser."""
    if topic.owner != request.user and not request.user.is_superuser:
        raise Http404

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics for the current user, or all topics if superuser."""
    if request.user.is_superuser:
        # Superuser sees everything
        topics = Topic.objects.order_by('date_added')
    else:
        # Regular user sees only their own
        topics = Topic.objects.filter(owner=request.user).order_by('date_added')
        
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Use our helper function to check permission
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # Create the new topic object but don't save to DB yet
            new_topic = form.save(commit=False)
            # Set the owner to the current user
            new_topic.owner = request.user
            # Now save it to the DB
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = get_object_or_404(Topic, id=topic_id) # Get the topic first

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 1. Create the new entry object but don't save to DB yet.
            new_entry = form.save(commit=False)
            
            # 2. Assign the topic to the new entry.
            new_entry.topic = topic
            
            # 3. Now save it to the database.
            new_entry.save()
            
            # Redirect user back to the topic's page (not the home page)
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    # Use our helper function to check permission
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
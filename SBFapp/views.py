from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
from .forms import *
from .utils import *
from django.utils.safestring import mark_safe
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PostFilter
import json
from django.utils import timezone
calendar = None

def get_calendar(user):
    global calendar
    if calendar is None:
        print('made calendar')
        d = timezone.now()
        cal = EventCalendar(d.year, d.month)
        calendar = cal.formatmonth(d.year, d.month, user=user, withyear=True)
    return calendar


class IndexView(generic.ListView):
    template_name = 'SBFapp/index.html'

    def get_queryset(self):
        return


class ScheduleView(LoginRequiredMixin, generic.ListView):
    template_name = 'SBFapp/schedule.html'
    context_object_name = 'events'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global calendar
        calendar = None
        context['calendar'] = mark_safe(get_calendar(self.request.user))
        return context

    def get_queryset(self):
        return Event.objects.all()


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = EventForm
    template_name = 'SBFapp/create_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = timezone.now()
        # cal = EventCalendar(d.year, d.month)
        #
        # html_cal = cal.formatmonth(d.year, d.month, user=self.request.user, withyear=True)
        context['calendar'] = mark_safe(get_calendar(self.request.user))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreateView, self).form_valid(form)


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'SBFapp/event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = timezone.now()
        # cal = EventCalendar(d.year, d.month)
        #
        # html_cal = cal.formatmonth(d.year, d.month, user=self.request.user, withyear=True)
        context['calendar'] = mark_safe(get_calendar(self.request.user))
        return context


class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'SBFapp/event_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = timezone.now()
        # cal = EventCalendar(d.year, d.month)
        #
        # html_cal = cal.formatmonth(d.year, d.month, user=self.request.user, withyear=True)
        context['calendar'] = mark_safe(get_calendar(self.request.user))
        return context


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    template_name = 'SBFapp/event_delete.html'
    success_url = reverse_lazy('SBFapp:schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = timezone.now()
        # cal = EventCalendar(d.year, d.month)
        #
        # html_cal = cal.formatmonth(d.year, d.month, user=self.request.user, withyear=True)
        context['calendar'] = mark_safe(get_calendar(self.request.user))
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['post_title','post_content','post_type']
    template_name = 'SBFapp/create_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostView(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'SBFapp/view_post.html'


class PostsListView(LoginRequiredMixin,generic.ListView):
    model = Post
    template_name = 'SBFapp/postslist.html'
    context_object_name = 'latest_post_list'

    # def get_queryset(self):
    #     return Post.objects.all().order_by('-created_at')
    #     """qs = super().get_queryset()
    #     category = self.request.GET.get('category')
    #     if category is None:
    #         return qs
    #     return qs.filter(category=categry)"""
    def get_queryset(self):
        qs = self.model.objects.all()
        post_filtered_list = PostFilter(self.request.GET, queryset=qs)
        return post_filtered_list.qs.order_by('-created_at')

def makePost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community/')
    context ={'form':form}
    return render(request,'view_post.html',context)


class CommentsView(LoginRequiredMixin,generic.CreateView):
    fields = ['text']
    model = Comment
    template_name = 'SBFapp/comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super(CommentsView, self).form_valid(form)


def makeComment(request):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community/<int:pk>/')
    return render(request, 'view_post.html', {'form':form})


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')



@login_required
def profile(request):
    # Old version
    # user = User.objects.get(username = username)
    # cont
    # context = {
    #    "user": user
    # }
    #
    #
    # return render(request, 'SBFapp/user_profile.html', context)
    # for i in profile.user:
    #     if i == user
    return render(request, "SBFapp/user_profile.html", {"profile": Profile.objects.all(),'nbar':'home'})

@login_required
@transaction.atomic
def profileedit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, _('Your profile was successfully updated!'))
            return redirect('/userprofile')
        else:
            return redirect('/userprofile/edit')
            #messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'SBFapp/user_profileedit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


twilio_account_sid = 'AC83a654a9fd6bc7c6a3034222158351c0'
twilio_api_key_sid = 'SK6e94cf90265c2d5485b0b4ee23f3b4e7'
twilio_api_key_secret = 'VSdal9iwkwsGwRpCP56YEk2aThZoH1lp'


fake = Faker()

@login_required
def videologin(request,room_name):
    
    
    identity = request.GET.get('identity', fake.user_name())
    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity = identity)
    token.add_grant(VideoGrant(room=room_name ))
    data = {
        'identity': token.identity,
        'token': token.to_jwt().decode()
       }
    response = {
        'identity': identity,
        'token': token.to_jwt().decode()
       }
    return JsonResponse(response)

@login_required
def profile(request):
    return render(request, 'SBFapp/user_profile.html')

@login_required
def room(request, room_name):
    Profile.objects.filter(user=request.user).update(room= room_name)
    return render(request, 'SBFapp/room.html', {'room_name': room_name})


class GroupsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = ['group_name','group_descr','private']
    template_name = 'SBFapp/create_group.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GroupsCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('SBFapp:group',kwargs={'pk':self.object.id})


class GroupsView(LoginRequiredMixin,generic.DetailView):
    model = Group
    template_name = 'SBFapp/view_group.html'

    def is_member(self):
        return self.model.user == self.request.user or self.request.user in self.model.list_users.all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owned_groups = self.model.objects.filter(user=self.request.user)
        joined_groups = self.model.objects.filter(list_users=self.request.user)
        context['private_list'] = set(chain(owned_groups, joined_groups))
        return context

class GroupsListView(LoginRequiredMixin,generic.ListView):
    model = Group
    template_name = 'SBFapp/groupslist.html'
    context_object_name = 'latest_groups_list'

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owned_groups = self.model.objects.filter(user=self.request.user)
        joined_groups = self.model.objects.filter(list_users=self.request.user)
        context['private_list'] = set(chain(owned_groups, joined_groups))
        return context


class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'SBFapp/edit_group.html'


@login_required
def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups/')
    context ={'form':form}
    return render(request,'view_group.html',context)


@login_required
def join_group(request, pk):
    if request.method == "GET":
        user1 = request.user
        group1 = get_object_or_404(Group, id=pk)
        group1.list_users.add(user1)
        return HttpResponseRedirect(reverse('SBFapp:group', args=(pk, )))


@login_required
def edit_group(request, pk):
    if request.method == "GET":
        user = request.user
        group = get_object_or_404(Group, id=pk)
        if group.user == user:
            return HttpResponseRedirect(reverse('SBFapp:update_group', args=(pk, )))
        return render(request=request, template_name='SBFapp/permission_denied.html')

@login_required
def join_study_buddy(request, pk):
    if request.method == "GET":
        user = request.user
        post = get_object_or_404(Post, id=pk)
        post_user = post.user
        for group in Group.objects.filter(user=post_user):
            if user in group.list_users.all():
                return HttpResponseRedirect(reverse('SBFapp:group', args=(group.id, )))
        group = Group(user=post_user, group_name=(str(user) + "_and_" + str(post_user) + "_Chat_Room"), private=True)
        group.save()
        return HttpResponseRedirect(reverse('SBFapp:group', args=(group.id, )))

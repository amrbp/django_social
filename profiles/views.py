from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile,Relationship
from django.views.generic import TemplateView,View
from django.http import JsonResponse
from .forms import ProfileModelFrom,UserRegisterForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

def profile_test_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profiles/test_profile.htm', {'profile':profile})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.htm', {'form': form})

@login_required
def profile_my_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelFrom(request.POST or None, request.FILES or None , instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context ={
        'profile':profile,
        'form':form,
        'confirm':confirm,
    }
    return render(request, 'profiles/my_profile.htm', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs':results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invites.htm', context)

@login_required
def accept_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

@login_required
def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required
def invites_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invites(user)

    context = {
        'qs':qs,
    }
    
    return render(request, 'profiles/to_invite_list.htm', context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs':qs
    }
    
    return render(request, 'profiles/profile_list.htm', context)


class SearchResultsView(ListView):
    model = Profile 
    template_name = 'users/search.htm'

    def get_queryset(self):
        query = self.request.GET.get('q')
        # query = Profile.objects.get(username=self.request.GET.get('q'))
        object_list = Profile.objects.filter(
            Q(bio__contains=query) 
        )
        return object_list
   

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.htm'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False 

        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.htm'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) ==0:
            context['is_empty'] = True
        return context


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/my_profile.htm'

class MyProfileData(View):
    def get(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        qs = profile.get_proposals_for_following()
        profile_to_follow_list = []
        for user in qs:
            p = Profile.objects.get(user__username=user.username)
            profile_item = {
                'id': p.id,
                'user': p.user.username,
                'avatar': p.avatar.url,
            }
            profile_to_follow_list.append(profile_item)
        return JsonResponse({'pf_data':profile_to_follow_list})

@login_required
def send_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel =Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

@login_required    
def remove_from_friends(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender)&Q(receiver=receiver)|Q(sender=receiver)&Q(receiver=sender)))
        rel.delete()
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.users.forms import UserRegisterForm, UserUpdateForm
# from task_manager.users.models import User


class UserIndexView(View):

    def get(self, request, *args, **kwargs):
        users = get_user_model().objects.all()
        return render(request, 'users/users.html', context={
            'users': users,
        })


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('user_login')
    success_message = "User was created successfully"
    

class UserUpdateView(SuccessMessageMixin, UpdateView):
    form_class = UserUpdateForm
    model = get_user_model()
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    permission_required = 'users.change_user'
    success_message = "User was updated successfully"


class UserDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    permission_required = 'user.delete_user'
    success_message = "User was deleted"


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'



class UserLogoutView(LogoutView):
    pass


def logout_user(request):
    logout(request)
    messages.info(request, 'You are logged out')
    return redirect(reverse_lazy('home'))
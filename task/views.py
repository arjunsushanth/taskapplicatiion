from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView,ListView,DetailView,CreateView,FormView
from task.forms import TaskForm,RegistrationForm,LoginForm
from task.models import Task
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


class IndexView(TemplateView):
    template_name = "index.html"

class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
            form=LoginForm(request.POST)
            if form.is_valid():
                uname= form.cleaned_data.get("username")
                pwd= form.cleaned_data.get("password")
                usr=authenticate(request,username=uname,password=pwd) 
                if usr:
                    login(request,usr)
                    return redirect("home")
                else:
                    return render (request,"login.html",{"form":form})

class SignupView(CreateView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("signin")
    def form_valid(self, form):
        messages.success(self.request,"account hasbeen created")
        return super().form_valid(form)


class TaskCreateView(CreateView):
    template_name="task-add.html"
    form_class=TaskForm
    success_url=reverse_lazy("task-list")

    def form_valid(self,form):
        form.instance.user=self.request.user
        messages.success(self.request,"task hasbeen added")
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     form = TaskForm()
    #     return render(request, "task-add.html", {"form": form})

    # def post(self, request, *args, **kwargs):
    #     form = TaskForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("task-create")
    #     else:
    #         return render(request, "task-add.html", {"form": form})


class TaskListView(ListView):
    model=Task
    template_name="task-list.html"
    context_object_name="todos"
    
    # def get(self, request, *args, **kwargs):
    #     qs = Task.objects.all()
    #     return render(request, "task-list.html", {"todos": qs})


class TaskDetailView(DetailView):
    model=Task
    template_name="task-detail.html"
    context_object_name="todo"

    # def get(self, request, *args, **kwargs):
    #     id = kwargs.get('pk')
    #     qs = Task.objects.get(id=id)
    #     return render(request, "task-detail.html", {"todo": qs})


class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Task.objects.get(id=id).delete()
        return redirect("task-list")

def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("signin")
    
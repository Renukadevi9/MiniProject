from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Employee
from .forms import EmployeeForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'employee/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    search_query = request.GET.get('search', '').strip()
    if search_query:
        employees = Employee.objects.filter(
            Q(emp_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(designation__icontains=search_query)
        )
    else:
        employees = Employee.objects.all()

    total_count = Employee.objects.count()
    # Get distinct departments count
    dept_count = Employee.objects.values('department').distinct().count()

    context = {
        'employees': employees,
        'total_count': total_count,
        'dept_count': dept_count,
        'search_query': search_query,
    }
    return render(request, 'employee/dashboard.html', context)

@login_required(login_url='login')
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee {employee.first_name} {employee.last_name} successfully added.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm()
    
    return render(request, 'employee/employee_form.html', {'form': form})

@login_required(login_url='login')
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Employee {employee.first_name} {employee.last_name} profile successfully updated.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employee/employee_form.html', {'form': form})

@login_required(login_url='login')
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp_name = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        messages.success(request, f"Employee {emp_name} was successfully deleted.")
        return redirect('dashboard')
    
    return render(request, 'employee/delete_confirm.html', {'employee': employee})

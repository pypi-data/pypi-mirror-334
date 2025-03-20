from django.shortcuts import redirect, render

from login_app.forms import OdooSetupForm

# Create your views here.


def odoo_setup_view(request):
    if request.method == "POST":
        form = OdooSetupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('system-data/')  
    else:
        form = OdooSetupForm()
    return render(request, 'odoo_setup_form.html', {'form': form})
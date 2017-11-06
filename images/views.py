from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm


@login_required
def image_create(request):
    """
    View for creating an Image using the
    JavaScript Bookmarklet.
    """
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the image
            new_item.user = request.user
            new_item.save()

            messages.success(request, 'Image added successfully!')

            # redirect to the new image detail view
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm()

    context = {'section': 'images', 'form': form}

    return render(request, 'images/image/create.html', context)
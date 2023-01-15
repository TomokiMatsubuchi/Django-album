from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

# Create your views here.

from .models import Photo, Tag

class PhotoListView(ListView):
  model = Photo
  template_name = 'album/photo_list.html'
  context_object_name = 'photos'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context["tags"] = Tag.objects.all()
    return context
  
class PhotoDetailView(DetailView):
  model = Photo
  template_name = 'album/photo_detail.html'
  context_object_name = 'photo'

class TagPhotoListView(ListView):
  model = Photo
  template_name = 'album/tag_photo.html'
  context_object_name = 'photos'

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    tag_name = self.kwargs['tag']
    tag_name = get_object_or_404(Tag, name=tag_name)

    photos = Photo.objects.filter(tags=tag_name)
    context["tag"] = tag_name
    context["photos"] = photos
    return context

class PhotoCreateView(CreateView):
  model = Photo
  template_name = 'album/photo_form.html'
  fields = "__all__"
  success_url = reverse_lazy('photo-list')

  def form_valid(self, form):
    photo = form.save()
    new_tag = self.request.POST.get('new_tag')

    if new_tag:
      for tag in new_tag.split():
        is_exists = Tag.objects.filter(name=tag)
        if not is_exists:
          Tag.objects.create(name=tag)
        photo.tags.add(tag)
    
    return redirect("photo-list")

class PhotoUpdateView(UpdateView):
  model = Photo
  template_name = 'album/photo_form.html'
  fields = "__all__"
  def get_success_url(self): #リダイレクト先の設定　詳細画面はpkが必要なため
    return reverse('photo-detail', kwargs={'pk': self.object.pk})

class PhotoDeleteView(DeleteView):
  model = Photo
  template_name = 'album/photo_delete.html'
  success_url = reverse_lazy('photo-list')

# from django.contrib import admin

# from server.example.models import ExampleStorageModel


# class ExampleStorageModelForm(ModelForm):
#     """A form that overrides the upload widget"""

#     class Meta:
#         model = ExampleStorageModel
#         widgets = {
#             "direct_file": CloudFileWidget(
#                 bucket_identifier="gs://example-media-assets",
#                 path_prefix="direct_uploads/",
#             ),
#         }
#         fields = "__all__"


# class ExampleStorageModelAdmin(admin.ModelAdmin):
#     """A basic admin panel to demonstrate the direct and normal storage behaviour"""

#     # form = ExampleStorageModelForm

#     # formfield_overrides = {
#     #     DirectUploadFileField: {"widget": DirectUploadWidget(bucket_identifier="gs://example-media-assets")},
#     # }


# admin.site.register(ExampleStorageModel, ExampleStorageModelAdmin)

from django import forms

class MenuItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        permissions = self.fields.get("permissions")
        if permissions:
            permissions.queryset = permissions.queryset.select_related(
                "content_type"
            )

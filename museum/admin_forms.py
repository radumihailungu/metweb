from django import forms
from .models import ArtObject

# ============ CONFIG ============
# dropdowns
CHOICE_KEYS = [
    "department",
    "classification",
    "objectName",
    "medium",
]

LABELS = {
    "title": "Titlu lucrare",
    "artistDisplayName": "Artist",
    "department": "Departament",
    "classification": "Clasificare",
    "culture": "Cultură",
    "objectName": "Tip obiect",
    "medium": "Material / Tehnică",
    "objectDate": "Dată / Perioadă",
    "country": "Țara de origine",
    "region": "Regiune",
    "city": "Oraș",
    "creditLine": "Linie de credit",
    "objectURL": "Link oficial (Met Museum)",
    "image": "Imagine (Data URI Base64)",
}

HELP_TEXTS = {
    "image": "Exemplu: data:image/jpeg;base64,... (lipit complet)",
}

def distinct_json_values(json_key: str):
    qs = (
        ArtObject.objects
        .exclude(**{f"data__{json_key}": ""})
        .exclude(**{f"data__{json_key}__isnull": True})
        .values_list(f"data__{json_key}", flat=True)
        .distinct()
        .order_by(f"data__{json_key}")
    )
    return [v.strip() for v in qs if isinstance(v, str) and v.strip()]


class ArtObjectAdminForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=False, label=LABELS["title"])
    artistDisplayName = forms.CharField(max_length=255, required=False, label=LABELS["artistDisplayName"])
    culture = forms.CharField(max_length=255, required=False, label=LABELS["culture"])
    objectDate = forms.CharField(max_length=255, required=False, label=LABELS["objectDate"])
    country = forms.CharField(max_length=255, required=False, label=LABELS["country"])
    region = forms.CharField(max_length=255, required=False, label=LABELS["region"])
    city = forms.CharField(max_length=255, required=False, label=LABELS["city"])
    creditLine = forms.CharField(max_length=500, required=False, label=LABELS["creditLine"])
    objectURL = forms.URLField(required=False, label=LABELS["objectURL"])
    department = forms.ChoiceField(required=False, label=LABELS["department"], choices=[])


    classification = forms.ChoiceField(required=False, label=LABELS["classification"], choices=[])
    objectName = forms.ChoiceField(required=False, label=LABELS["objectName"], choices=[])
    medium = forms.ChoiceField(required=False, label=LABELS["medium"], choices=[])


    image = forms.CharField(
        required=False,
        label=LABELS["image"],
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text=HELP_TEXTS.get("image", ""),
    )

    class Meta:
        model = ArtObject
        fields = []  # nu editez direct JSON

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in CHOICE_KEYS:
            values = distinct_json_values(key)
            self.fields[key].choices = [("", "- alege -")] + [(v, v) for v in values]

        # valori initiale la edit din JSON
        if self.instance and self.instance.pk:
            d = self.instance.data or {}

            # umple automat form la edit
            for field_name in self.fields:
                self.fields[field_name].initial = d.get(field_name, "")

            # verificam daca valoarea curenta e in dropdown deja
            for k in CHOICE_KEYS:
                current = d.get(k, "")
                if current:
                    existing = [c[0] for c in self.fields[k].choices]
                    if current not in existing:
                        self.fields[k].choices.append((current, current))
                    self.fields[k].initial = current


    def save(self, commit=True):
        inst = super().save(commit=False)
        d = inst.data or {}

        #salveaza valorile puse de user
        for field_name in self.fields:
            d[field_name] = self.cleaned_data.get(field_name, "")

        inst.data = d
        if commit:
            inst.save()
        return inst

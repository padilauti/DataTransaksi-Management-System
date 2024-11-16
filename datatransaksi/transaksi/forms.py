from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaksi



class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tanggal', 'jenis_transaksi', 'anggota', 'jumlah', 'keterangan', 'bukti']


class TransaksiSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Transaksi
        fields = ['anggota','tanggal']

class TransaksiUpdateForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tanggal', 'jenis_transaksi', 'anggota', 'jumlah', 'keterangan', 'bukti']

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


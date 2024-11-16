from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import Transaksi, Anggota
from .forms import TransaksiForm, TransaksiSearchForm, TransaksiUpdateForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from .models import Transaksi
import io
from django.db.models import Sum








# Create your views here.
@login_required(login_url='login')
def home(request):
    title = 'Selamat datang di Aplikasi Keuangan Kami!'
    
    # Hitung total pengeluaran dan pemasukan
    total_pengeluaran = Transaksi.objects.filter(jenis_transaksi='Pengeluaran').aggregate(total=Sum('jumlah'))['total'] or 0
    total_pemasukan = Transaksi.objects.filter(jenis_transaksi='Pemasukan').aggregate(total=Sum('jumlah'))['total'] or 0

    context = {
        'title': title,
        'total_pengeluaran': total_pengeluaran,
        'total_pemasukan': total_pemasukan,
    }
    return render(request, 'home.html', context)

def list_item(request):
    title = 'List Data Transaksi'
    form = TransaksiSearchForm(request.POST or None)
    queryset = Transaksi.objects.all()  # Default queryset

    if request.method == 'POST' and form.is_valid():
        anggota = form.cleaned_data.get('anggota')
        tanggal = form.cleaned_data.get('tanggal')

        # Apply filters based on the provided data
        if anggota and tanggal:
            queryset = Transaksi.objects.filter(anggota__nama__icontains=anggota, tanggal__exact=tanggal)
        elif anggota:
            queryset = Transaksi.objects.filter(anggota__nama__icontains=anggota)
        elif tanggal:
            queryset = Transaksi.objects.filter(tanggal__exact=tanggal)

        if form.cleaned_data.get('export_to_CSV'):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List_of_stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['ANGGOTA', 'TANGGAL', 'JUMLAH', 'JENIS_TRANSAKSI', 'KETERANGAN'])
            for transaksi in queryset:
                writer.writerow([
                    transaksi.anggota.nama if transaksi.anggota else '',
                    transaksi.tanggal,
                    transaksi.jumlah,
                    transaksi.jenis_transaksi,
                    transaksi.keterangan
                ])
            return response

    context = {
        'form': form,
        'title': title,
        'queryset': queryset
    }

    return render(request, 'list_item.html', context)

def add_item(request):
    form = TransaksiForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Add Successfully')
        return redirect('list_item')
    context = {
        'form': form,
        'title': 'Add Transaksi'
    }
    return render(request, 'add_item.html',context)

def delete_item(request, pk):
    queryset = Transaksi.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_item')
    return render(request, 'delete_item.html')

def update_item(request, pk):
    item = get_object_or_404(Transaksi, pk=pk)  
    form = TransaksiUpdateForm(request.POST or None, instance=item)
    
    if request.method == 'POST' and form.is_valid():
        form.save()  
        messages.success(request, ' Update Successfully')
        return redirect('list_item')  
    
    context = {
        'form': form,
        'title': 'Update Transaksi' 
    }
    return render(request, 'update_item.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
        
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    return redirect('login')


def list_anggota(request):
    title = 'List Data Anggota'
    form = TransaksiSearchForm(request.POST or None)
    queryset = Anggota.objects.all()

    context = {
        'form': form,
        'title': title,
        'queryset': queryset
    }

    return render(request, 'list_anggota.html', context)

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def download_pdf(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    content = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']  


    title = Paragraph("BUKTI TRANSAKSI", title_style)
    content.append(title)
    

    from reportlab.lib.units import inch
    content.append(Paragraph('<br/><br/>', styles['Normal']))  


    data = [
        ["Field", "Value"],
        ["ID", str(transaksi.id)],
        ["Nama Anggota", transaksi.anggota.nama],
        ["ID Anggota", str(transaksi.anggota.id)],
        ["Tanggal", transaksi.tanggal.strftime('%Y-%m-%d')],  
        ["Jenis Transaksi", transaksi.jenis_transaksi],
        ["Jumlah", str(transaksi.jumlah)],
        ["Keterangan", transaksi.keterangan],
    ]

    # Create the Table
    table = Table(data)

    # Apply Table Style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add table to content
    content.append(table)

    # Build PDF
    doc.build(content)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=transaksi_{transaksi.id}.pdf'
    return response




        



   
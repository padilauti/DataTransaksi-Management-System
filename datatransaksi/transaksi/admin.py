from django.contrib import admin
from .models import Transaksi, Anggota
# Register your models here.
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from .models import Transaksi, Anggota


def download_pdf(self, request, queryset):
    modal_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={modal_name}.pdf'

    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    headers = [field.verbose_name for field in self.model._meta.fields]
    data = [headers]

    for obj in queryset:
        data_row = [str(getattr(obj, field.name)) for field in self.model._meta.fields]
        data.append(data_row)

    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]
    ))

    # Adjust these values based on your table size and page layout
    table_width, table_height = letter
    x = 40
    y = table_height - 100  # Start a bit lower on the page

    table.wrapOn(pdf, table_width - 80, table_height - 100)  # Adjust margins as needed
    table.drawOn(pdf, x, y)

    pdf.save()
    pdf_buffer.seek(0)
    response.write(pdf_buffer.getvalue())
    pdf_buffer.close()

    return response

download_pdf.short_description = "Download selected items as PDF."

class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'alamat', 'no_hp')
    search_fields = ('nama', 'alamat', 'no_hp')


class TransaksiCreateForm(admin.ModelAdmin):
    list_display = ('id', 'tanggal', 'jenis_transaksi','jumlah', 'keterangan', 'bukti')
    list_filter = ('jenis_transaksi', 'tanggal')
    search_fields = ('keterangan', 'jumlah')
    actions = [download_pdf]



admin.site.register(Transaksi, TransaksiCreateForm)
admin.site.register(Anggota, AnggotaAdmin)

from users.models import CustomUser
from products.models import Product
from .models import Cart, CartItem
from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ShoppingCart:
    
    
    def __init__(self, request):
        self.request = request
        self.session = request.session


    def get_cart(self, request):
        customer_id = request.user.id
        customer = CustomUser.objects.get(pk=customer_id)
        cart = Cart.objects.get(customer=customer)
        return cart


    def add_product(self, cart_id, product_id, quantity):
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(pk=product_id)
        query = CartItem.objects.filter(cart=cart, product=product)
        if not query.exists():
            item = CartItem(cart_id=cart_id, product_id = product_id, quantity=quantity)
            item.save()


    def remove_product(self, cart_id, product_id):
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(pk=product_id)
        query = CartItem.objects.filter(cart=cart, product=product)
        if query.exists():
            item = CartItem.objects.filter(cart=cart, product=product)
            item.delete()
            
            
    def get_total(self, cart_id):
        total = 0
        cart = Cart.objects.get(pk=cart_id)
        query = CartItem.objects.filter(cart=cart)

    
    def get_total_quantity(cart_items):
        total_quantity = 0
        for item in cart_items:
            total_quantity += item.quantity
        return total_quantity
    
# shoppingcart/utils.py
from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

class PDFGenerator(ABC):

    @abstractmethod
    def generate(self, context):
        pass

class OrderPDFGenerator(PDFGenerator):

    def generate(self, context):
        response = context['response']
        order_details = context['order_details']
        filename = context['filename']

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['BodyText']

        # Add title
        elements.append(Paragraph("Order Details", title_style))

        # Add order details table
        data = [
            ['Product:', order_details['product']],
            ['Quantity:', order_details['quantity']],
            ['Price:', f"${order_details['price']}"],
            ['Total:', f"${order_details['total']}"],
        ]
        table = Table(data, colWidths=[1.5 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        # Add delivery information
        elements.append(Paragraph("Delivery Information:", subtitle_style))
        delivery_data = [
            ['Name:', order_details['customer_name']],
            ['Address:', order_details['delivery_address']],
            ['Box Size:', order_details['box_size']],
            ['Total to pay:', f"${order_details['total_price']}"],
        ]
        delivery_table = Table(delivery_data, colWidths=[1.5 * inch, 3 * inch])
        delivery_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(delivery_table)

        # Build the PDF
        doc.build(elements)


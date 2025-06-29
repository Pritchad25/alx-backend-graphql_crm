import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer
from django.core.exceptions import ValidationError
import re
from crm.models import Product
from crm.models import Order

class CustomerType(DjangoObjectType):
        class Meta:
                    model = Customer

                    class CreateCustomer(graphene.Mutation):
                            class Arguments:
                                        name = graphene.String(required=True)
                                                email = graphene.String(required=True)
                                                        phone = graphene.String()

                                                            customer = graphene.Field(CustomerType)
                                                                message = graphene.String()

                                                                    def mutate(self, info, name, email, phone=None):
                                                                                if Customer.objects.filter(email=email).exists():
                                                                                                raise Exception("Email already exists")

                                                                                                    if phone and not re.match(r"^(\+?\d{7,15}|\d{3}-\d{3}-\d{4})$", phone):
                                                                                                                    raise Exception("Invalid phone number format")

                                                                                                                        customer = Customer.objects.create(name=name, email=email, phone=phone)
                                                                                                                                return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
        class Arguments:
                    input = graphene.List(
                                        graphene.InputObjectType("CustomerInput", {
                                                            "name": graphene.String(required=True),
                                                                            "email": graphene.String(required=True),
                                                                                            "phone": graphene.String()
                                                                                                        })
                                                )

                        customers = graphene.List(CustomerType)
                            errors = graphene.List(graphene.String)

                                def mutate(self, info, input):
                                            customers = []
                                                    errors = []

                                                            for i, item in enumerate(input):
                                                                            try:
                                                                                                if Customer.objects.filter(email=item.email).exists():
                                                                                                                        errors.append(f"{item.email} already exists")
                                                                                                                                            continue
                                                                                                                                                        if item.phone and not re.match(r"^(\+?\d{7,15}|\d{3}-\d{3}-\d{4})$", item.phone):
                                                                                                                                                                                errors.append(f"{item.phone} is invalid")
                                                                                                                                                                                                    continue
                                                                                                                                                                                                                customer = Customer(name=item.name, email=item.email, phone=item.phone)
                                                                                                                                                                                                                                customer.save()
                                                                                                                                                                                                                                                customers.append(customer)
                                                                                                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                                                                                                                errors.append(f"Index {i}: {str(e)}")

                                                                                                                                                                                                                                                                                        return BulkCreateCustomers(customers=customers, errors=errors)

class ProductType(DjangoObjectType):
        class Meta:
                    model = Product

                    class CreateProduct(graphene.Mutation):
                            class Arguments:
                                        name = graphene.String(required=True)
                                                price = graphene.Float(required=True)
                                                        stock = graphene.Int(default_value=0)

                                                            product = graphene.Field(ProductType)

                                                                def mutate(self, info, name, price, stock):
                                                                            if price <= 0:
                                                                                            raise Exception("Price must be positive")
                                                                                                if stock < 0:
                                                                                                                raise Exception("Stock cannot be negative")
                                                                                                                    product = Product.objects.create(name=name, price=price, stock=stock)
                                                                                                                            return CreateProduct(product=product)

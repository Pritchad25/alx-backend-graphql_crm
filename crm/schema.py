import graphene
from crm.models import Product

class ProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
	updated_products = graphene.List(ProductType)
	message = graphene.String()

	def mutate(self, info):
		low_stock_products = Product.objects.filter(stock__lt=10)
		updated = []

		for product in low_stock_products:
			product.stock += 10
			product.save()
			updated.append(product)

		return UpdateLowStockProducts(
			updated_products=[
				ProductType(name=p.name, stock=p.stock) for p in updated
			],
			message="Low-stock products updated successfully"
		)

class Mutation(graphene.ObjectType):
	update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

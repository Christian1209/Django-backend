from dis import disco
from math import prod
from operator import truediv
from tracemalloc import start
import graphene 
from graphene_django.types import DjangoObjectType
from .models import User,Product,Promotions


class UserType(DjangoObjectType):
     class Meta:
        model = User

class ProductType(DjangoObjectType):
    class Meta: 
        model = Product

class PromotionsType(DjangoObjectType):
    class Meta:
        model = Promotions


class Query(graphene.ObjectType):
    #users attributes
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType,id=graphene.Int(), 
    username = graphene.String())
    #promotions attributes
    all_promotions = graphene.List(PromotionsType)
    promotion = graphene.Field(PromotionsType, id=graphene.Int())
    #products attributes.
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int(),
    name = graphene.String())

    #user functions
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self,info,**kwargs):
        id = kwargs.get('id')
        username = kwargs.get('username')
        
        if id is not None:
            return User.objects.get(id=id)
        if username is not None: 
            return User.objects.get(username=username)
    
    #promotions functions
    def resolve_all_products(self,info,**kwargs):
        return Product.objects.all()
    def resolve_product(self,info,**kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        
        if id is not None:
            return Product.objects.get(id=id) 
        if name is not None:
            return Product.objects.get(name=name)
        
    #prodmotions functions
    def resolve_all_promotions(self,info,**kwargs):
        return Promotions.objects.all()
    def resolve_promotion(self,info,**kwargs):
        id = kwargs.get('id')
        return Promotions.objects.get(id=id)

class UserCreateMutation(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
    user = graphene.Field(UserType)
    
    def mutate(self,info,email,firstName,lastName,password,phone,username):
        user = User.objects.create(email=email,first_name=firstName,last_name=lastName,password=password,phone=phone,username=username)
        return UserCreateMutation(user=user)

class ProductCreateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        piece = graphene.Boolean(required=True)
        price = graphene.String(required=True)
        quantity = graphene.String()
        line = graphene.String()
        supplier = graphene.String()
        urlmedia = graphene.String()
    product = graphene.Field(ProductType)

    def mutate(self,info,name,description,price,piece,quantity,line,
    supplier,urlmedia):
        product = Product.objects.create(name=name,description=description,price=price,quantity=quantity,
        piece=piece,line=line,supplier=supplier,url_media=urlmedia)
        return ProductCreateMutation(product=product)


class PromotionCreateMutation(graphene.Mutation):
    class Arguments:
        #product will be a existent producto id get that product later, cause is a foreign key.
        product = graphene.Int(required=True)
        startDate = graphene.Date(required=True)
        endDate = graphene.Date()
        discount = graphene.String()
        finalPrice = graphene.String(required=True)
        urlMedia = graphene.String()
    promotion = graphene.Field(PromotionsType)

    def mutate(self,info,product,startDate,endDate,discount,finalPrice,urlMedia):
        #get a product with the product attribute
        newProduct = Product.objects.get(pk=product)
        promotion = Promotions.objects.create(product=newProduct,start_date=startDate,end_date=endDate,discount=discount,final_price=finalPrice,url_media=urlMedia)
        return PromotionCreateMutation(promotion=promotion)

#Update Mutations
class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        password = graphene.String()
        firstName = graphene.String()
        lastName = graphene.String()
        username = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        username = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self,info,id,password,firstName,lastName,username,email,phone):
        user = User.objects.get(pk=id)
        if password is not None:
            user.password = password
        if firstName is not None:
            user.first_name = firstName
        if lastName is not None:
            user.last_name = lastName
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        if username is not None:
            user.username = username

        user.save()
        
        return UserUpdateMutation(user=user)

class ProductUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        piece = graphene.Boolean()
        price = graphene.String()
        quantity = graphene.String()
        line = graphene.String()
        supplier = graphene.String()
        urlMedia = graphene.String()
    product = graphene.Field(ProductType)

    def mutate(self,info,id,name,description,piece,price,quantity,line,supplier,urlMedia):
        product = Product.objects.get(pk=id)
        if name is not None:
            product.name = name 
        if description is not None:
            product.description = description
        if piece is not None:
            product.piece = piece 
        if price is not None:
            product.price = price  
        if quantity is not None: 
            product.quantity = quantity
        if line is not None: 
            product.line = line 
        if supplier is not None: 
            product.supplier = supplier
        if urlMedia is not None:
            product.url_media = urlMedia

        product.save()

        return ProductCreateMutation(product=product)


class PromotionUpdateMutation(graphene.Mutation):
    class Arguments:
        #product will be a existent producto id get that product later, cause is a foreign key.
        id = graphene.Int(required=True)
        product = graphene.Int()
        startDate = graphene.Date()
        endDate = graphene.Date()
        discount = graphene.String()
        finalPrice = graphene.String()
        urlMedia = graphene.String()
    promotion = graphene.Field(PromotionsType)


    def mutate(self,info,id,product,startDate,endDate,discount,finalPrice,urlMedia):
        promotion = Promotions.objects.get(pk=id)    
        if product is not None:
            #if the user wants to update the product, we need to get a new product by the id, and then assign it to the promotion.
            newProduct = Product.objects.get(pk=product)
            promotion.product = newProduct 
        if  startDate is not None:
            promotion.start_date = startDate
        if endDate is not None:
            promotion.end_date = endDate
        if discount is not None:
            promotion.discount = discount 
        if finalPrice is not None:
            promotion.final_price = finalPrice  
        if urlMedia is not None: 
            promotion.url_media = urlMedia
        
        promotion.save()

        return PromotionCreateMutation(promotion=promotion)

#Delete mutations
class UserDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    user = graphene.Field(UserType)

    def mutate(self,info,id):
        user = User.objects.get(pk=id)
        user.delete()
        
        return UserDeleteMutation(user=None)

class ProductDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    product = graphene.Field(ProductType)

    def mutate(self,info,id):
        product = Product.objects.get(pk=id)
        product.delete()

        return ProductDeleteMutation(product=None)

class PromotionDeleteMutation(graphene.Mutation):
    class Arguments:
        #product will be a existent producto id get that product later, cause is a foreign key.
        id = graphene.Int(required=True)
    promotion = graphene.Field(PromotionsType)

    def mutate(self,info,id):
        promotion = Promotions.objects.get(pk=id)    
    
        promotion.delete()

        return PromotionCreateMutation(promotion=None)




class Mutation:
    create_user = UserCreateMutation.Field()
    create_product = ProductCreateMutation.Field()
    create_promotion = PromotionCreateMutation.Field()
    update_user = UserUpdateMutation.Field()
    update_product = ProductUpdateMutation.Field()
    update_promotion = PromotionUpdateMutation.Field()
    delete_User = UserDeleteMutation.Field()
    delete_product = ProductDeleteMutation.Field()
    delete_promotion = PromotionDeleteMutation.Field()









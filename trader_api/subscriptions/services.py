from services.database_service import PostgresServices
from .models import Subscription
from services.google_services import GooglePlayServices
from users.service import UserService
class SubscriptionService(PostgresServices):
    def __init__(self):
        super().__init__(Subscription)

    
    def create_subscription(self,subscription_data):
        '''
            Create a subscrioption by store (google or apple)
        '''

        store_map = {
            "google":self.__valid_sub_Google,
            "apple":self.__valid_sub_Apple
        }
        
        data,condition = store_map[subscription_data["store"]](**subscription_data)
        
        if condition:
            #check user
            user = UserService().get_user_by_email(data.get("email"))
            data_sub_create ={
                "user":user.id,
                "pay_services":subscription_data["store"],
                "valid":...,
                "subscription_key":data.get("product_id")
            }
            super().create(data_sub_create)
            return "subscription success created"
        else:
            return "This subscription not is from a valid store"

    def __valid_sub_Google(self,package_name,product_id,purchase_token):
        google_service = GooglePlayServices(package_name=package_name,product_id=product_id)
        data_sub,condition = google_service.check_sub(purchase_token)
        return data_sub,condition

    def __valid_sub_Apple(self):...

    def update_subscription(self):...

    def update_status_subscription(self):...
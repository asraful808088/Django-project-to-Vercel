
from django.urls import path
from .views import CraditCardProcess, PaymentTokenDUR,PaymentTokenGetPost, ApiPaymentService,GetTokenApiTransection,CAutoPayToken,Transfar,AddPaymentToken ,GetPaymentTokenTransection,CheckValidPin,PaymentAddressGenerate,GetAccountInfo,UserAccountInfoDUR,GetAutoPayToken,AutoPayDUR,PaymentAddressGet,PaymentAddressDURDelete
# GetPaymentTokenTransection
# PaymentTokenGenerateSerializer
urlpatterns = [
    path("getApiPaymentToken/",GetTokenApiTransection.as_view()), # get token for api service 
    path("paymentTokemGenerate/",GetPaymentTokenTransection.as_view()),
    path("paymentTokemGenerateList/",PaymentTokenGetPost.as_view()),
    path("paymentTokemGenerateDUR/<int:pk>/",PaymentTokenDUR.as_view()),
    path("addPaymentToken/",AddPaymentToken.as_view()),




    path("transfar/",Transfar.as_view()),
    # path("paymentTokemGenerateDUR/<int:pk>/",HistoryDUR.as_view()),






    # path("paymentTokemGenerate/",PaymantGateWayGetPost.as_view()),
    # path("paymentTokemGenerateDUR/<int:pk>/",PaymantGateWayDUR.as_view()),






    path("getUserAccountInfo/",GetAccountInfo.as_view()),
    path("checkPin/",CheckValidPin.as_view()),
    path("userAccountInfoDUR/<int:pk>/",UserAccountInfoDUR.as_view()),






    # path("paymentTokemGenerate/",HistoryGetPost.as_view()),
    # path("paymentTokemGenerateDUR/<int:pk>/",HistoryDUR.as_view()),





















    path("getAutopayTokem/<int:pk>",GetAutoPayToken.as_view()),
    path("createAutopayTokem/",CAutoPayToken.as_view()),
    path("paymentTokemGenerateDU/<int:pk>/",AutoPayDUR.as_view()),























    path("getPaymentTokemList/<int:pk>",PaymentAddressGet.as_view()),
    path("PaymentTokemGenerate/",PaymentAddressGenerate.as_view()),
    path("paymentTokemGenerateDURDelete/<int:pk>/",PaymentAddressDURDelete.as_view()),







    path("cardRequestProcess",CraditCardProcess.as_view()),
    path("apiPaymentService",ApiPaymentService.as_view()), # payment from api service 





]

from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from .payment_token_serializer import PaymentTokenSerializer
from .models import TransferTempToken,UserAccountInfo,PaymantGateWay,History,AutoPay,PaymentAddress
from .user_accountInfo_serializer import UserAccountInfoSerializer,GetAccountInfoSerializer
from .paymant_gate_way_serializer import PaymantGateWaySerializer
from .history_serializer import HistorySerializer
from .autopay_serializer import CreateAutoPaySerializer,UpdateAutoPaySerializer
from .payment_address_serializer import PaymentAddressSerializer,PaymentAddressGeneratorSerializer
from rest_framework.views import APIView,Response,status
from .apiPaymentKeySerializer import PaymentTokenGenerateSerializer,AccountPaymentTokenGeneratorSerializer
from bank.utility.hashing import encrypt
import json
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import PaymentAddress
from .checkValidPinSerializer import CheckValidPinSerializar
from .transfarSerializer import TransfarSysSeaializer
from .addpaymentToken import AddPaymentTokenClient
from .card_request_Serializer import CardRequestSerializer
from .models import CardRequestBoard
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .paymentServiceSerializer import APIPaymentServiceSerializer
class PaymentTokenGetPost(GenericAPIView,ListModelMixin):
    permission_classes = [IsAuthenticated]

    queryset = TransferTempToken.objects.all()
    serializer_class = PaymentTokenSerializer
    def get_queryset(self):
        return TransferTempToken.objects.filter(author=self.request.user)
    def get(self, req, *arg, **KMoreA):
        user_tokens = self.get_queryset()
        serializer = self.get_serializer(user_tokens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentTokenDUR(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = TransferTempToken.objects.all()
    serializer_class = PaymentTokenSerializer
    def get(self,req,*arg,**KMoreA):
        return self.retrieve(req,*arg,**KMoreA)
    def put(self,req,*arg,**KMoreA):
        return self.update(req,*arg,**KMoreA)
    def delete(self,req,*arg,**KMoreA):
        return self.destroy(req,*arg,**KMoreA)
    



















class AddPaymentToken(APIView):
    def post(self,req,*arg,**KMoreA):
         serializer_class = AddPaymentTokenClient(data=req.data)
         print(serializer_class.is_valid())
         return Response({"success":True}, status=status.HTTP_200_OK)






















class CheckValidPin(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,req,*arg,**KMoreA):
        result  = CheckValidPinSerializar(data=req.data)
        if result.is_valid():
            return Response({"success":True}, status=status.HTTP_200_OK)
        return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
    

















class GetAccountInfo(APIView):
    def post(self,req,*arg,**KMoreA):
         result  = GetAccountInfoSerializer(data = req.data)
         if result.is_valid():
            return Response({
                'account_type':result.validated_data['account_type'] , 'amount':result.validated_data['amount'] , 'account_lvl':result.validated_data['account_lvl'] , 'secure':result.validated_data["secure"]
            }, status=status.HTTP_200_OK)
         
         errors = {}
         for field, messages in result.errors.items():
                 errors[field] = messages[0]
         return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountInfoDUR(GenericAPIView,UpdateModelMixin,DestroyModelMixin):
    queryset = UserAccountInfo.objects.all()
    serializer_class = UserAccountInfoSerializer
    def get(self,req,*arg,**KMoreA):
        return self.retrieve(req,*arg,**KMoreA)
    def put(self,req,*arg,**KMoreA):
        return self.update(req,*arg,**KMoreA)
    def delete(self,req,*arg,**KMoreA):
        return self.destroy(req,*arg,**KMoreA)
 














class Transfar(APIView):
    def post(self,req,*arg,**KWarg):
        result  = TransfarSysSeaializer(data=req.data)
        if result.is_valid():
            getdata = result.validated_data
            return Response({"success":getdata["success"],"new_bal":getdata["new_bal"]   }, status=status.HTTP_200_OK)
        errors={}
        for field, messages in result.errors.items():
                errors[field] = messages[0]
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        















































class PaymantGateWayGetPost(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = PaymantGateWay.objects.all()
    serializer_class = PaymantGateWaySerializer
    def post(self, req, *arg, **KMoreA):
        return self.create(req, *arg, **KMoreA)
    def get(self, req, *arg, **KMoreA):
        return self.list( req, *arg, **KMoreA)





class  PaymantGateWayDUR(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = PaymantGateWay.objects.all()
    serializer_class = PaymantGateWaySerializer
    def get(self,req,*arg,**KMoreA):
        return self.retrieve(req,*arg,**KMoreA)
    def put(self,req,*arg,**KMoreA):
        return self.update(req,*arg,**KMoreA)
    def delete(self,req,*arg,**KMoreA):
        return self.destroy(req,*arg,**KMoreA)


























class HistoryGetPost(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    def post(self, req, *arg, **KMoreA):
        return self.create(req, *arg, **KMoreA)
    def get(self, req, *arg, **KMoreA):
        return self.list( req, *arg, **KMoreA)





class HistoryDUR(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    def get(self,req,*arg,**KMoreA):
        return self.retrieve(req,*arg,**KMoreA)
    def put(self,req,*arg,**KMoreA):
        return self.update(req,*arg,**KMoreA)
    def delete(self,req,*arg,**KMoreA):
        return self.destroy(req,*arg,**KMoreA)





































#

##
##
##
##
##
##  Auto pay
##
##
##
##
##
##
##


class GetAutoPayToken(APIView):
    def get(self, req, *arg, **KMoreA):
        user_id = KMoreA.get("pk")
        result =  AutoPay.objects.all()
        listOfUser = []
        for item in result:
            if item.author_id == user_id:
                listOfUser.append({
                    "id":item.id,
                    "token":item.token,
                    "amount":item.amount,
                    "lvl_order":item.lvl_order,
                    "name":item.name
                })
        return Response(listOfUser, status=status.HTTP_200_OK)





class CAutoPayToken(APIView):
    def post(self, req, *arg, **KMoreA):
        reuslt  = CreateAutoPaySerializer(data=req.data)
        if reuslt.is_valid():
            return Response({
                "id":reuslt.validated_data["id"], 
                              "token":reuslt.validated_data["token"], 
                              "amount":reuslt.validated_data["amount"], 
                              "lvl_order":reuslt.validated_data["lvl_order"], 
                              "name":reuslt.validated_data["name"]
            }, status=status.HTTP_200_OK)
        errors={}
        for field, messages in reuslt.errors.items():
                errors[field] = messages[0]

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# AccountPaymentTokenGeneratorSerializer

class  AutoPayDUR(GenericAPIView,UpdateModelMixin,DestroyModelMixin):
    queryset = AutoPay.objects.all()
    serializer_class = UpdateAutoPaySerializer
    def put(self,req,*arg,**KMoreA):
        return self.update(req,*arg,**KMoreA)
    def delete(self,req,*arg,**KMoreA):
        return self.destroy(req,*arg,**KMoreA)























































class PaymentAddressGet(APIView):
    def get(self, req, *arg, **KMoreA):
        payment_token_id = KMoreA.get('pk')
        getdata = PaymentAddress.objects.all()
        listOfUser = []
        for item in getdata:
            if item.author_id == payment_token_id:
                listOfUser.append({
                    "id":item.id,
                    "token":item.token,
                })
        return Response(listOfUser, status=status.HTTP_200_OK)

# AccountPaymentTokenGeneratorSerializer

class PaymentAddressGenerate(APIView):
    def post(self, req, *arg, **KMoreA):
        result  = PaymentAddressGeneratorSerializer(data=req.data)
        if result.is_valid():
            getdata = result.validated_data
            return Response({"token":getdata["token"],'id':getdata["id"]}, status=status.HTTP_200_OK)
        errors={}
        for field, messages in result.errors.items():
                errors[field] = messages[0]
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)



class  PaymentAddressDURDelete(GenericAPIView,DestroyModelMixin):
    queryset = PaymentAddress.objects.all()
    serializer_class = PaymentAddressSerializer
    def delete(self,req,*arg,**KMoreA):
        return self.destroy(req,*arg,**KMoreA)






























class GetTokenApiTransection(APIView):
    def post(self, request, *args, **kwargs):
        result  = PaymentTokenGenerateSerializer(data=request.data)
        # print(result.is_valid())
        if result.is_valid():
            pack = {}
            pack["email"] = result.validated_data["email"]
            pack["api_name"] = result.validated_data["api_name"]
            encrypted_data = encrypt(json.dumps(pack),settings.SECRET_KEY )
            return Response({ "token":  encrypted_data},status=status.HTTP_200_OK)
        errors = {}
        for field, messages in result.errors.items():
                print(messages[0])
                errors[field] = messages[0]
        return Response(errors,status=status.HTTP_400_BAD_REQUEST)
    
class GetPaymentTokenTransection(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
       
        serializer = AccountPaymentTokenGeneratorSerializer(data=request.data)
       
        if serializer.is_valid():
            return Response({
                    "info":{
                            "token":serializer.validated_data["info"].token,
                            "token_user":serializer.validated_data["info"].token_user
                            ,"limite":serializer.validated_data["info"].limite
                            ,"access":serializer.validated_data["info"].access
                            ,"exp_date":serializer.validated_data["info"].exp_date
                            ,"used":serializer.validated_data["info"].used
                            ,"exp_date_used":serializer.validated_data["info"].exp_date_used
                            ,"api_name":serializer.validated_data["info"].api_name
                            ,"create_timespan":serializer.validated_data["info"].create_timespan
                    },
                    "token":serializer.validated_data["token"]
            }, status=status.HTTP_200_OK)
        errors = {}
        for field, messages in serializer.errors.items():
                errors[field] = messages[0]
      
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)





class CraditCardProcess(APIView):
    def get(self,request, *args, **kwargs):
        email =  request.query_params.get('email', None)
        result  = CardRequestBoard.objects.all()
        items = []
        for i in result:
            if email == str(i.author):
                items.append({
                    "card_lvl":i.card_lvl,
                    "card_num":i.card_num,
                    "cvv":i.cvv,
                    "card_type":i.card_type,
                    "exp_date":i.exp_date,
                    "card_stap_type":i.card_stap_type,
                    "total_aspect_value":i.total_aspect_value,
                    "used_value":i.used_value,
                    "stage":i.stage
                })
        return Response({"card_items_info":items}, status=status.HTTP_200_OK)


    def post(self,request, *args, **kwargs):
        result = CardRequestSerializer(data=request.data)
        if result.is_valid():
            resultD = result.save()
            if resultD["failed_status"]:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"data":resultD}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    


class ApiPaymentService(APIView):
    def post(self,request, *args, **kwargs):
        result  = APIPaymentServiceSerializer(data=request.data)
        if result.is_valid():
            return Response({}, status=status.HTTP_200_OK)
        errors = {}
        for  field, messages in result.errors.items():
            errors[field] = messages[0]

        return Response({"errors":errors}, status=status.HTTP_400_BAD_REQUEST)







from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import TextEntry
from .serializers import TextEntrySerializer
import torch
from accountapp.transformer.transformer_model.transformer_model import *


# Create your views here.


# 기존 장고 방식
def hello_world(request):
    return render(request, 'accountapp/temp.html')




# DRF 방식으로
@api_view()
def hello_world_drf(request):
    return Response({"message":"Hello_world!"})

transformer_model = torch.load('./accountapp/transformer/transformer_model/transformer_jeju_model3.pt')
class TextEntryView(APIView):
    def post(self, request, format=None):
        serializer = TextEntrySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            text_data = serializer.data['text']
            translation, attention = translate_sentence(text_data, SRC, TRG, transformer_model, device, logging=True)
            text_list = []
            for text in translation:
                if text in ["<unk>", "?", "!"]:
                    pass
                else:
                    text_list.append(text)
            texts = " ".join(text_list)
            if "?" in translation:
                print("제주도 번역 = ", texts + "?")
                texts = texts + "?"
                response_data = {
                    "original_text": text_data,
                    "translated_text": texts
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            elif "!" in translation:
                print("제주도 번역 = ", texts + "!")
                texts = texts + "!"
                response_data = {
                    "original_text": text_data,
                    "translated_text": texts
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                print("제주도 번역 = ", texts)
            response_data = {
                "original_text": text_data,
                "translated_text": texts
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
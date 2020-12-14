from django.shortcuts import render

import json
import xmltodict
from .serializers import data_Vin, dataOnlyVin
from rest_framework.views import APIView
from .models import VinNumber
from rest_framework.response import Response


def IndexView(request):
    return render(request, 'index.html')


def XmlToJsonConverter(vinNumbers):
    vin_object = VinNumber.objects.all().filter(vinNumber=vinNumbers)
    if not vin_object.exists():
        return False
    for value in vin_object:
        file = value.VDAFile
        with open(file.path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
            xml_file.close()
        return data_dict


def FilterJsonByEcuName(json_data, Ecu_names, Vin):
    map_dict = {
        'T_R_': 'Serial Number',
        'REF_': 'Hardware Number',
        'REFOP_': 'Current Operational Reference',
        'RUC_': 'Current RUC',
        'FC_': 'Current Configuration'
    }

    Final_dict = {'Vin': Vin, 'Plant_Code': json_data['ROOT']['Vehicle_Info']['Plant_Code'],
                  'Plant_Unique_ID': json_data['ROOT']['Vehicle_Info']['Plant_Unique_ID'],
                  'Manufacturer_Code': json_data['ROOT']['Vehicle_Info']['Manufacturer_Code'],
                  'Car_Series': json_data['ROOT']['Vehicle_Info']['Prod_Family_Code'],
                  'Vehicle_Spec': json_data['ROOT']['Vehicle_Spec']}

    # filter ecu specific data
    for Ecu_name in Ecu_names:
        for values in json_data['ROOT']['Plant_Mnemonic']['item']:
            if Ecu_name in values['@name']:
                for keys in map_dict.keys():
                    if values['@name'].startswith(keys):
                        dict_key_name = Ecu_name + " " + map_dict[keys]
                        Final_dict[dict_key_name] = values['#text']
    return Final_dict


class Isupdate_for_Vehicle(APIView):
    def post(self, request, *args, **kwargs):
        serializer = data_Vin(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            vin_no = data['vin']
            Ecu_name = data['EcuName']
            json_data = XmlToJsonConverter(vin_no)
            if json_data:
                pass
            else:
                return Response(status=204)
            Ecu_names = [Ecu_name]
            final_dict = FilterJsonByEcuName(json_data, Ecu_names, vin_no)
            return Response(final_dict)
        return Response(status=400)


class Isupdate_for_Vehicle1(APIView):
    def post(self, request, *args, **kwargs):
        serializer = dataOnlyVin(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            vin_no = data['vin']
            json_data = XmlToJsonConverter(vin_no)
            if json_data:
                pass
            else:
                return Response(status=204)
            Ecu_names = ['ADAS', 'HUD', 'METER', 'IVC', 'IVI']
            final_dict = FilterJsonByEcuName(json_data, Ecu_names, vin_no)
            return Response(final_dict)
        else:
            return Response(status=400)

import json
import math
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse


class CalculadoraView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        tipo = data.get("tipo_operacion", None)
        valor_1 = data.get("valor_1", None)
        valor_2 = data.get("valor_2", None)
        print(data)
        print(tipo, valor_1, valor_2)
        resultado = 0
        errores = []
        if not tipo:
            errores.append({"tipo":"Especifique el tipo de la operación."})
        if not valor_1 and tipo != "raiz_cuadrada":
            errores.append({"valor_1":"Ingrese el primer valor."})
        if not valor_2 and tipo != "porcentaje":
            errores.append({"valor_2":"Ingrese el segundo valor."})
        
        
        else:
            if tipo == "suma":
                resultado = int(valor_1) + int(valor_2)
            elif tipo == "resta":
                resultado = int(valor_1) - int(valor_2)
            elif tipo == "multiplicacion":
                resultado = int(valor_1) * int(valor_2)
            elif tipo == "division":
                if valor_2 == 0:
                    errores.append({"valor_2":"No se puede dividir por cero."})
                resultado = int(valor_1) / int(valor_2)
            elif tipo == "potencia":
                resultado = int(valor_1) ** int(valor_2)
            elif tipo == "porcentaje":
                resultado = int(valor_1) * 0.01
            elif tipo == "raiz_cuadrada":
                resultado = math.sqrt(int(valor_2))
        # Si hay errores, devolverlos
        if errores:
            return JsonResponse(errores, status=400, safe=False)

        # Si no hay errores, devolver el resultado
        return JsonResponse({"resultado": resultado}, status=200)

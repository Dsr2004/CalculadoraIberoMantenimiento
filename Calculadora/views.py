import json
import math
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from Historial.models import Historial

OPERACION_SIMBOLOS = {
    "suma": "+",
    "resta": "-",
    "multiplicacion": "*",
    "division": "/",
    "potencia": "^",
    "porcentaje": "%",
    "raiz_cuadrada": "√"
}


class CalculadoraView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            historial = Historial.objects.filter(usuario=request.user).order_by('-fecha')[:10]
        else:
            historial = []
        return render(request, "index.html", {"historial": historial})
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        tipo = data.get("tipo_operacion", None)
        valor_1 = data.get("valor_1", None)
        valor_2 = data.get("valor_2", None)
        resultado = 0
        errores = []

        if not tipo:
            errores.append({"tipo": "Especifique el tipo de la operación."})
        if not valor_1 and tipo != "raiz_cuadrada":
            errores.append({"valor_1": "Ingrese el primer valor."})
        if not valor_2 and tipo != "porcentaje":
            errores.append({"valor_2": "Ingrese el segundo valor."})

        if errores:
            return JsonResponse({"errores": errores}, status=400)

        try:
            if tipo == "suma":
                resultado = int(valor_1) + int(valor_2)
            elif tipo == "resta":
                resultado = int(valor_1) - int(valor_2)
            elif tipo == "multiplicacion":
                resultado = int(valor_1) * int(valor_2)
            elif tipo == "division":
                if int(valor_2) == 0:
                    raise ValueError("División por cero")
                resultado = int(valor_1) / int(valor_2)
            elif tipo == "potencia":
                resultado = int(valor_1) ** int(valor_2)
            elif tipo == "porcentaje":
                resultado = int(valor_1) * 0.01
            elif tipo == "raiz_cuadrada":
                resultado = math.sqrt(int(valor_1))
                
             # Construir operación con símbolos
            if tipo == "raiz_cuadrada":
                operacion = f"{OPERACION_SIMBOLOS[tipo]}({valor_1})"
            elif tipo == "porcentaje":
                operacion = f"{valor_1}{OPERACION_SIMBOLOS[tipo]}"
            else:
                operacion = f"{valor_1}{OPERACION_SIMBOLOS[tipo]} {valor_2}"

            # Guardar en el historial
            if request.user.is_authenticated:
                Historial.objects.create(
                    usuario=request.user,
                    operacion=operacion,
                    resultado=str(resultado)
                )
        except Exception as e:
            return JsonResponse({"errores": [str(e)]}, status=400)

        # Si no hay errores, devolver el resultado
        return JsonResponse({"resultado": resultado}, status=200)


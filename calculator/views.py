from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

def welcome(request):
    return render(request, 'calculator/welcome.html')

@csrf_exempt
def calculate_ratio(request):
    if request.method == 'POST':
        try:
            # Helper function to get float values safely
            def get_float(key):
                value = request.POST.get(key)
                if value is None or value.strip() == '':
                    return None  # Missing field
                return float(value)

            A = get_float('amino_acids')
            B = get_float('dextrose')
            C = get_float('body_weight')
            D = get_float('fat_volume')
            E = get_float('percentage_lipids')
            F = get_float('Lipids')
            G = get_float('Sodium')
            H = get_float('Potassium')
            I = get_float('Calcium')
            J = get_float('Fluid_intake')
            K = get_float('Feeds')
            L = get_float('drugs')
            M = get_float('Other_losses_Sampling')
            N = get_float('add_as_spillage_losses')
            O = get_float('Wastage_factor')
            P = get_float('Lower_Conc_of_Dextrose')
            Q = get_float('Higher_Conc_of_Dextrose')
            R = get_float('Percentage_Aminoacids')


            outputs = {}

            # Output 1: Total Fluid Volume
            if C is not None and J is not None:
                outputs['result01'] = round(C * J, 4)

            # Output 2: Total TPN Volume
            if all(x is not None for x in [C, J, K, L, M]):
                outputs['result02'] = round((C * J) - K - L + M, 4)

            # Output 3: Fat Volume (avoid division by 0)
            if F is not None and C is not None and E not in (None, 0):
                outputs['result03'] = round(F * C * 100 / E, 4)

            # Output 4: TPN Solution Volume Ordered
            if all(x is not None for x in [C, J, K, L, M, F, E]) and E != 0:
                result04 = ((C * J) - K - L + M) - (F * C * 100 / E)
                outputs['result04'] = round(result04, 4)

            # Output 5: Amino Acids Volume
            if all(x is not None for x in [A, C, O, R]) and R != 0:
                outputs['result05'] = round(A * C * O * 100 / R, 4)

            # Output 6: Sodium Volume
            if all(x is not None for x in [G, C, O]):
                outputs['result06'] = round(G * C * O / 0.5, 4)

            # Output 7: Potassium Volume
            if all(x is not None for x in [H, C, O]):
                outputs['result07'] = round(H * C * O / 2, 4)

            # Output 8: Calcium Volume
            if all(x is not None for x in [I, C, O]):
                outputs['result08'] = round(I * C * O / 0.45, 4)

            # Output 9: Magnesium Volume
            if C is not None and O is not None:
                outputs['result09'] = round(0.25 * C * O / 4, 4)

            # Output 10: MVI Volume
            if C is not None and O is not None:
                outputs['result10'] = round(1.5 * C * O, 4)

            # Output 11: Sum of Additive Volumes
            required_keys = ['result05', 'result06', 'result07', 'result08', 'result09', 'result10']
            if all(k in outputs for k in required_keys):
                outputs['result11'] = round(sum(outputs[k] for k in required_keys), 4)

            # Output 12: Dextrose Absolute Amount
            if all(x is not None for x in [B, C, O]):
                outputs['result12'] = round(B * C * 1.44 * O, 4)

            # Output 13: Dextrose Volume
            if 'result04' in outputs and O is not None and 'result11' in outputs:
                outputs['result13'] = round(outputs['result04'] * O - outputs['result11'], 4)

            # Output 14: Final Dextrose Concentration
            if 'result12' in outputs and 'result04' in outputs and outputs['result04'] != 0 and N is not None:
                outputs['result14'] = round(100 * outputs['result12'] / (outputs['result04'] + N), 4)

            # Output 15: Dextrose Concentration for Calculation
            if all(x is not None for x in [B, C, O]) and 'result13' in outputs and outputs['result13'] != 0:
                outputs['result15'] = round((B * 144 * C * O) / outputs['result13'], 4)

            # Output 16: Volume of D2
            if 'result13' in outputs and 'result15' in outputs and Q is not None and P is not None and (Q - P) != 0:
                outputs['result16'] = round(outputs['result13'] * ((outputs['result15'] - P) / (Q - P)), 4)

            # Output 17: Volume of D1
            if 'result13' in outputs and 'result16' in outputs:
                outputs['result17'] = round(outputs['result13'] - outputs['result16'], 4)

            # Output 18: TPN Rate (per hr)
            if 'result04' in outputs:
                outputs['result18'] = round(outputs['result04'] / 24, 4)

            # Output 19: Lipid Rate (per hr)
            if 'result03' in outputs and 'result10' in outputs:
                outputs['result19'] = round((outputs['result03'] + outputs['result10']) / 24, 4)
            
             # Output 20: Amino acid in gram
            if 'result05' in outputs and R is not None:
                outputs['result20'] = round(outputs['result05'] * R / 100, 4)
            
             # Output 21: fat in gram
            if 'result03' in outputs and E is not None:
                outputs['result21'] = round(outputs['result03'] * E /100, 4)
            
             # Output 22: calorie in gram
            if B is not None and C is not None:
                outputs['result22'] = round(B * C * 60 * 24 / 1000, 4)
            
             # Output 23:calorie:nitrogen ratio
            if 'result20' in outputs and 'result21' in outputs and 'result22' in outputs and outputs['result20'] != 0:
                outputs['result23'] = round((outputs['result22'] * 3.4 + outputs['result21'] * 9) * 6.25 / outputs['result20'], 4)

            

            return JsonResponse(outputs)

        except Exception as e:
            return JsonResponse({'error': f'Error occurred: {str(e)}'})

    return render(request, 'calculator/calculate.html')

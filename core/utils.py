from datetime import timedelta

def calculate_deadline(start_date):
    """
    Calcula a data de prazo (3 dias após a data de início).
    Se a data cair em um final de semana, move para a próxima segunda-feira.
    """
    deadline = start_date + timedelta(days=3)
    
    # Se cair no sábado (5) ou domingo (6), move para segunda-feira
    if deadline.weekday() == 5: # Sábado
        deadline += timedelta(days=2)
    elif deadline.weekday() == 6: # Domingo
        deadline += timedelta(days=1)
        
    return deadline

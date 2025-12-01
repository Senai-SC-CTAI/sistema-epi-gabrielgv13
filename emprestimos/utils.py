from datetime import timedelta

def calculate_deadline(start_date):
    """
    Calcula a data de devolução a partir da data de início.
    Prazo: 3 dias úteis (pula sábados e domingos).
    """
    days_added = 0
    current_date = start_date
    
    while days_added < 3:
        current_date += timedelta(days=1)
        # 5 = Saturday, 6 = Sunday
        if current_date.weekday() < 5:
            days_added += 1
    
    return current_date

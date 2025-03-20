def percentage_to_grade(score):
    """score from pecentage to grade"""
    if score > 90:
        grade = 'A'
    elif score > 80:
        grade = 'B'
    elif score > 70:
        grade = 'C'
    else:
        grade = 'D'
    return grade
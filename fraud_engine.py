def calculate_risk(amount, location):

    risk = 0

    if amount > 50000:
        risk += 40

    if location == "Unknown":
        risk += 30

    if amount > 100000:
        risk += 30

    if risk >= 80:
        return risk, "High Risk"

    elif risk >= 50:
        return risk, "Medium Risk"

    else:
        return risk, "Low Risk"
def is_school_email(email):
    return email.endswith("@gbox.adnu.edu.ph")


def passwords_match(password, confirm_password):
    return password == confirm_password
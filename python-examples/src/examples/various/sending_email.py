def send_email(msg,subject,me,you, smtp_host,smtp_port=25,encryption="tls", username=None,password=None):

    DESTINATIONS = you

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # me == the sender's email address
    # you == the recipient's email address

    for dest in DESTINATIONS:
        msg = MIMEText(msg)

        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = dest

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP(host=smtp_host,port=smtp_port)
        s.ehlo()
        if encryption == "tls":
            s.starttls()
        if (not username is None) & (not password is None):
            s.login(username,password)
        s.sendmail(me, [dest], msg.as_string())
        s.quit()

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app, origins='*', methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers=['Content-Type', 'Authorization'])

def sendmail(data):
    work = data.get('work')
    room_no = data.get('room_no')
    default_message = 'bsdk jldi kam krr'
    message = data.get('message')  
    if not message:
        message = default_message
    message_string = f"Work: {work}\nRoom No: {room_no}\nMessage: {message}"
    print("Message String:", message_string)  

    # Check if work and room_no are provided
    if not all([work, room_no]):
        return {'success': False, 'message': 'Missing required fields (work and room_no).'}, 400

    try:
        
        msg = MIMEText(message_string)

        
        msg['Subject'] = 'Start working on your task'
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("zero686797@gmail.com", 'wcvy ntpm jiwd pjyq')
        server.sendmail("zero686797@gmail.com", "anu.rag.gade007@gmail.com",msg.as_string())
        server.quit()
        return {'success': True, 'message': 'Email sent successfully.'}
    except smtplib.SMTPException as e:
        return {'success': False, 'message': 'Failed to send email.', 'error': str(e)}, 500
    except Exception as e:
        return {'success': False, 'message': 'An unexpected error occurred.', 'error': str(e)}, 500

@app.route('/sendmail', methods=['POST'])
def handle_sendmail():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    elif request.method == 'POST':
        data = request.json
        result, status_code = sendmail(data)
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, status_code
    else:
        return jsonify({'success': False, 'message': 'Only POST requests are allowed.'}), 405

# if __name__ == "__main__":
#     app.run(debug=True)

import imaplib
import email
import os
import json
import time
import loggerutility as logger
from flask import request
import traceback
from fpdf import FPDF

from .Save_Transaction import Save_Transaction
from .Email_Upload_Document import Email_Upload_Document
from .Email_Classification import Email_Classification
from .EmailReplyAssistant import EmailReplyAssistant
from .Email_Draft import Email_Draft
from .Email_DocumentUploader import Email_DocumentUploader

class Email_Read:
    def read_email(self, email_config):
        try:
            logger.log("inside read_email")
            mail = imaplib.IMAP4_SSL(email_config['host'], email_config['port'])
            mail.login(email_config['email'], email_config['password'])
            logger.log("login successfully")
            mail.select('inbox')

            while True:
                status, email_ids = mail.search(None, 'UNSEEN')
                emails = []
                
                if status == 'OK':
                    email_ids = email_ids[0].split()

                    if not email_ids: 
                        logger.log("Email not found, going to check new mail")
                        logger.log("Email not found,\ngoing to check new mail \n")
                    else:
                    
                        for email_id in email_ids:
                            email_body = ""
                            attachments = []
                            status, data = mail.fetch(email_id, '(RFC822)')
                            
                            if status == 'OK':
                                raw_email = data[0][1]
                                msg = email.message_from_bytes(raw_email)
                                
                                sender_email = msg['From']
                                cc_email = msg['CC']
                                subject = msg['Subject']
                                to = msg['To']

                                if msg.is_multipart():
                                    for part in msg.walk():
                                        content_type = part.get_content_type()
                                        if content_type == "text/plain":
                                            email_body += part.get_payload(decode=True).decode('utf-8', errors='replace')
                                else:
                                    email_body = msg.get_payload(decode=True).decode('utf-8', errors='replace')                              

                                email_data = {
                                    "email_id": email_id,
                                    "from": sender_email,
                                    "to": to,
                                    "cc": cc_email,
                                    "subject": subject,
                                    "body": email_body
                                }
                                emails.append(email_data)
                                logger.log(f"emails:: {emails}")
                                call_save_transaction = Save_Transaction()
                                save_transaction_response = call_save_transaction.email_save_transaction(email_data)
                                logger.log(f"save_transaction_response:: {save_transaction_response}")
                time.sleep(10)
        
        except Exception as e:
            return {"success": "Failed", "message": f"Error reading emails: {str(e)}"}
        finally:
            try:
                mail.close()
                mail.logout()
            except Exception as close_error:
                logger.log(f"Error during mail close/logout: {str(close_error)}")

    def read_email_automation(self, email_config):
        # try:
        logger.log(f"inside read_email_automation")
        # logger.log(f"email_config ::: {email_config}")
        LABEL                       = "Unprocessed_Email"
        file_JsonArray              = []
        templateName                = "ai_email_automation.json"
        fileName                    = ""

        Model_Name =  email_config.get('model_type', 'OpenAI') 
        reciever_email_addr = email_config.get('email', '').replace("\xa0", "").strip()
        receiver_email_pwd = email_config.get('password', '').replace("\xa0", "").strip()
        host =  email_config.get('host', '') 
        port =  email_config.get('port', '') 

        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(reciever_email_addr, receiver_email_pwd)
        logger.log("login successfully")
        mail.select('inbox')
                    
        file_JsonArray, categories = self.read_JSON_File(templateName)

        while True:
            status, email_ids = mail.search(None, 'UNSEEN')
            emails = []
            
            if status == 'OK':
                email_ids = email_ids[0].split()

                if not email_ids: 
                    logger.log("Email not found, going to check new mail")
                    logger.log("Email not found,\ngoing to check new mail \n")
                else:
                
                    for email_id in email_ids:
                        email_body = ""
                        attachments = []
                        status, data = mail.fetch(email_id, '(RFC822)')
                        
                        if status == 'OK':
                            raw_email = data[0][1]
                            msg = email.message_from_bytes(raw_email)

                            subject = msg['Subject']
                            sender_email_addr   = msg['From']
                            cc_email_addr       = msg['CC']
                            subject             = msg['Subject']

                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type == "text/plain":
                                        email_body += part.get_payload(decode=True).decode('utf-8', errors='replace')
                                        fileName = self.download_attachment(msg)
                            else:
                                email_body = msg.get_payload(decode=True).decode('utf-8', errors='replace')                              
                            
                            openai_Process_Input  = email_body 
                            logger.log(f"\nEmail Subject::: {subject}")
                            logger.log(f"\nEmail body::: {openai_Process_Input}")

                            openai_api_key = email_config.get('openai_api_key', '') 
                            geminiAI_APIKey = email_config.get('gemini_api_key', '') 
                            signature = email_config.get('signature', '') 
                            localAIURL = email_config.get('local_ai_url', '') 
                            
                            if len(str(openai_Process_Input)) > 0 :
                                email_cat_data = {
                                    "model_type" : Model_Name,
                                    "openai_api_key" : openai_api_key,
                                    "categories" : categories,
                                    "email_body" : email_body,
                                    "gemini_api_key" : geminiAI_APIKey,
                                    "signature" : signature,
                                    "local_ai_url" : localAIURL,
                                }
                                # logger.log(f"\nemail_cat_data ::: {email_cat_data}")
                                email_classification = Email_Classification()
                                emailCategory = email_classification.detect_category(email_cat_data)
                                emailCategory = emailCategory['message']
                                logger.log(f"\nDetected Email category ::: {emailCategory}")
                                
                                if emailCategory == 'Others':
                                    logger.log(f"Marking email as UNREAD. ")
                                    mail.store(email_id, '-FLAGS', '\\Seen')

                                    mail.create(LABEL)
                                    mail.copy(email_id, LABEL)
                                    mail.store(email_id, '+FLAGS', '\\Deleted')  # Mark for deletion
                                    mail.expunge()                         
                                    logger.log(f"Mail removed from inbox and added to '{LABEL}' label.")
                                
                                elif emailCategory == "Product Enquiry":
                                    
                                    if Model_Name == "OpenAI":
                                        responseMethod, parameters = self.get_JsonArray_values(emailCategory, file_JsonArray)
                                        if responseMethod == "Reply_Email_Ai_Assistant" :

                                            emailreplyassistant = EmailReplyAssistant()
                                            openai_Response = emailreplyassistant.Reply_Email_Ai_Assistant(openai_api_key, parameters["Assistant_Id"], openai_Process_Input, subject)
                                            
                                            logger.log(f"Process openai_Response ::: {openai_Response['message']}\n")
                                            email_details = {"sender":sender_email_addr, "cc":cc_email_addr, "subject":subject, "body": email_body}

                                            email_draft = Email_Draft()
                                            status, response = email_draft.draft_email(email_config, email_details, openai_Response['message'])
                                            logger.log(f"status ::: {status}")
                                        else :
                                            message = f"Invalid response method received '{responseMethod}' for category : '{emailCategory}'"
                                            raise ValueError(message)
                                    elif Model_Name == "LocalAI":
                                        logger.log("localAI")
                                        Detect_Email_category = False
                                        LocalAI_Response = emailCategory
                                        logger.log(f"Process LocalAI_Response ::: {LocalAI_Response}\n")
                                        email_details = {"sender":sender_email_addr, "cc":cc_email_addr, "subject":subject, "body": email_body}

                                        email_draft = Email_Draft()
                                        status, response = email_draft.draft_email(email_config, email_details, LocalAI_Response)
                                        logger.log(f"status ::: {status}")
                                    elif Model_Name == "GeminiAI":
                                        logger.log("GeminiAI")
                                        Detect_Email_category = False
                                        GeminiAI_Response = emailCategory
                                        logger.log(f"Process GeminiAI_Response ::: {GeminiAI_Response}\n")
                                        email_details = {"sender":sender_email_addr, "cc":cc_email_addr, "subject":subject, "body": email_body}

                                        email_draft = Email_Draft()
                                        status, response = email_draft.draft_email(email_config, email_details, GeminiAI_Response)
                                        logger.log(f"status ::: {status}")
                                    else:
                                        raise ValueError(f"Invalid Model Name provided : '{Model_Name}'")

                                elif emailCategory == "Purchase Order":
                                    responseMethod, parameters = self.get_JsonArray_values(emailCategory, file_JsonArray)
                                    logger.log(f"responseMethod ::: {responseMethod}")
                                    logger.log(f"parameters ::: {parameters}")
                                    if responseMethod == "Upload_Document" :
                                        
                                        if len(fileName) != 0 :   

                                            email_upload_document = Email_DocumentUploader()               
                                            with open(f"temp/{fileName}", "rb") as file:
                                                response_status, restAPI_Result = email_upload_document.email_document_upload(file, parameters)
                                                logger.log(f"email_upload_document_response ::: {restAPI_Result}")
                                        else:
                                            
                                            new_fileName = self.create_file_from_emailBody(email_body, sender_email_addr, parameters)
                                            with open(f"temp/{new_fileName}", "rb") as file:
                                                response_status, restAPI_Result = email_upload_document.email_document_upload(file, parameters)
                                                logger.log(f"email_upload_document_response ::: {restAPI_Result}")

                                        if response_status == "200" :
                                            logger.log(f"Attachment uploaded sucessfully against Document id: '{restAPI_Result}'.")
                                        else:
                                            logger.log(restAPI_Result)
                                    
                                    else :
                                        message = f"Invalid response method received '{responseMethod}' for category : '{emailCategory}'"
                                        raise ValueError(message)
                                else:
                                    message = f"Detected Email category not found : '{emailCategory}'"
                                    raise ValueError(message)
            time.sleep(10)
        
        # except Exception as e:
        #     return {"status": "Failed", "message": f"Error reading emails: {str(e)}"}
        # finally:
        #     try:
        #         mail.close()
        #         mail.logout()
        #     except Exception as close_error:
        #         logger.log(f"Error during mail close/logout: {str(close_error)}")
        #         return {"status": "Failed", "message": f"Error reading emails: {str(close_error)}"}

    def save_attachment(self, part, download_dir):
        try:
            filename = part.get_filename()
            if filename:
                # Create the directory if it doesn't exist
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

                file_path = os.path.join(download_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))

                logger.log(f"Attachment saved: {file_path}")
                return file_path
        except Exception as e:
            return {"success": "Failed", "message": f"Error saving attachment: {str(e)}"}

    def Read_Email(self, data):
        try:

            reciever_email_addr = data.get("reciever_email_addr")
            receiver_email_pwd = data.get("receiver_email_pwd")
            host = data.get("host")
            port = data.get("port")
            openai_api_key = data.get("openai_api_key") 
            geminiAI_APIKey = data.get("GeminiAI_APIKey")
            localAIURL = data.get("LOCAL_AI_URL")

            if not all([reciever_email_addr, receiver_email_pwd, host, port]):
                raise ValueError("Missing required email configuration fields.")

            logger.log(f"\nReceiver Email Address: {reciever_email_addr}\t{type(reciever_email_addr)}", "0")
            logger.log(f"\nReceiver Email Password: {receiver_email_pwd}\t{type(receiver_email_pwd)}", "0")
            logger.log(f"\nHost: {host}\t{type(host)}", "0")
            logger.log(f"\nPort: {port}\t{type(port)}", "0")

            email_config = {
                'email': reciever_email_addr,
                'password': receiver_email_pwd,
                'host': host,
                'port': int(port),
                'openai_api_key': openai_api_key,
                'gemini_api_key': geminiAI_APIKey,
                'local_ai_url': localAIURL
            }

            emails = self.read_email(email_config)            
            logger.log(f"Read_Email response: {emails}")

        except Exception as e:
            logger.log(f"Error in Read_Email: {str(e)}")

    def download_attachment(self, msg):
        filepath                = ""
        filename                = ""
        ATTACHMENT_SAVE_PATH    = "temp"

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename:
                if not os.path.exists(ATTACHMENT_SAVE_PATH):
                    os.mkdir(ATTACHMENT_SAVE_PATH)
                    filepath = os.path.join(ATTACHMENT_SAVE_PATH, filename)
                else:
                    filepath = os.path.join(ATTACHMENT_SAVE_PATH, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                logger.log(f"\nAttachment saved: '{filepath}'")
            else:
                logger.log("\nNo Attachment found.")
        return filename
    
    def read_JSON_File(self, json_fileName):
        category_list               = []
        categories                  = ""
        try:
            if os.path.exists(json_fileName):
                with open(json_fileName, "r") as fileObj:
                    file_JsonArray = json.load(fileObj) 
                    
                    for eachJson in file_JsonArray :
                        for key, value in eachJson.items():
                            if key == "Category" and value:
                                category_list.append(value)
                        # categories = ", ".join(category_list)
                        
                return file_JsonArray, category_list

            else:
                message = f"{json_fileName} file not found."
                raise Exception(message)
        except Exception as e:
            msg = f"'{json_fileName}' file is empty. Please provide JSON parameters in the filename."
            trace = traceback.format_exc()
            logger.log(f"Exception in writeJsonFile: {msg} \n {trace} \n DataType ::: {type(msg)}")
            raise Exception(msg)
        
    def get_JsonArray_values(self, category, jsonArray):
        responseMethod  = ""
        parameters      = ""
        
        for eachJson in jsonArray :
            for key, value in eachJson.items():
                if value == category:
                    responseMethod  = eachJson["Response_Method"]  
                    parameters      = eachJson["Parameters"]
        
        return responseMethod, parameters
    
    def create_file_from_emailBody(self, text, sender_email_addr, parameters):
        
        dir      = "temp/"
        if not os.path.exists(dir):
            os.mkdir(dir)
        fileName = sender_email_addr[sender_email_addr.find("<")+1:sender_email_addr.find("@")].strip().replace(".","_")
        
        if parameters["FILE_TYPE"] == "pdf":
            fileName = fileName + ".pdf"
            filePath = dir + fileName 

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, text)
            pdf.output(filePath)
            logger.log(f"New PDF file created from email body and stored in '{filePath}'")

        elif parameters["FILE_TYPE"] == "txt":
            fileName = fileName + ".txt"
            filePath = dir + fileName 

            with  open(filePath, "w") as file:
                file.write(text)
                logger.log(f"New TXT file created from email body and stored in '{filePath}'")
        else:
            message = f"Invalid File Type received. "
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

        return fileName

        


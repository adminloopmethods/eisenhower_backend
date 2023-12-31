""" All Messages Alerts """

MODEL_MESSAGES = dict(
    ZIPCODEMSG="Zipcode must be entered in the format: '11111'. Up to 5 digits allowed.",
    PHONENOMSG="Phone number must be entered in the format: '9999999999'. Up to 15 digits allowed.",
    EMAIL_EXIST="This Email Id Already Exist in W&R System Please enter other Email Id",
    UNIQUE_PHONE="This Phone Number Already Exist in W&R System Please enter other Phone Number"
)

API_RESPONSE_MSG = dict(
    No_ACTIVE_DATA="No Active data",
    DONE="Done",
    REQUEST_NOT_FOUND="Request not found",
    PLEASE_POST_EMAIL="Please Post the email-id",
    ENTER_VALID_EMAIL="Please enter valid email id",
    USER_NOT_FOUND="User Not Found",
    PLEASE_PROVIDE_DEPARTMENT_NAME="Please Provide department",
    PLEASE_PROVIDE_ACCESS_STATUS="Please Provide access status",
    ERRORS="Errors",
    PLEASE_PROVIDE_TOPIC_NAME="Please Provide the topic name",
    # create member
    PLEASE_PROVIDE_FIRST_NAME="Please provide first_name",
    PLEASE_PROVIDE_LAST_NAME="Please provide last name",
    PLEASE_PROVIDE_EMAIL="Please Provide Email ID",
    PLEASE_PROVIDE_DEPARTMENT_ID="Please Provide department",
    PLEASE_PROVIDE_LEVEL_ID="Please Provide level id",
    PLEASE_PROVIDE_COLOR="Please Provide Color",

    # create task
    PROVIDE_TASK_OWNER="Please provide task owner name",
    PROVIDE_TASK_NAME="Please Provide Task Name",
    PROVIDE_CUSTOMER_NAME="Please Provide Customer Name",
    PROVIDE_START_DATE="Please Provide start date",
    PROVIDE_DUE_DATE="Please Provide due date",
    PROVIDE_REMINDER="Please Provide reminder",
    PROVIDE_STATUS="Please Provide status",
    PLEASE_PROVIDE_TOPIC_ID="please Provide topic id",
    PROVIDE_MEMBERS="Please provide member",
    PROVIDE_MATRIX="Please Provide matrix data",

    DEPARTMENT_ID_ERROR="Please Provide valid department id",
    PLEASE_PROVIDE_TEAM_NAME="please provide team name",
    PLEASE_PROVIDE_ACTIVE_STATUS="Please provide active status",
    PLEASE_PROVIDE_TEAM_ID="Please provide team id",
    PLEASE_PROVIDE_MEMBER_ID="Please provide member id",
    PLEASE_PROVIDE_STATUS="Please provide status",
    PLEASE_PROVIDE_TASK="Please provide task id",
    PLEASE_PROVIDE_TASK_FOR_EXPORT="Please provide tasks to export",
    PLEASE_PROVIDE_PASSWORD="Please provide the password",
    IMPORT_FILE_NAME_NOT_FOUND="Please provide the excel file",
    IMPORT_SUCCESSFULLY="Data Imported Successfully",
    PLEASE_PROVIDE_BUSINESS_CARD_ID="Please provide the card Id",
    PLEASE_PROVIDE_VALID_CARD_ID="Please provide the valid card Id",
    CATEGORY_ALREADY_EXIST="This category already exists",
    DEPARTMENT_ALREADY_EXISTS_PRIVATE="This Department Already Exist as a private department with no access to others",
    TOPIC_ALREADY_EXISTS_PRIVATE="This Topic Already Exist as a private Topic with no access to others",
    MEMBER_ALREADY_EXISTS_PRIVATE="This Member Already Exist as a private Member with no access to others"


)

MSG = dict(
    DONE="Done",
    ERRORS="Errors",
    USER_NOT_FOUND="User Not Found",
    TOKEN_ERROR="JWT Token Error",
    EMAIL_ALREADY_EXISTS="This Email Already Exist in our system",
    No_ACTIVE_DATA="No Active data",
    DEPARTMENT_ALREADY_EXISTS="Department Already Exist",
    SERIALIZER_NOT_FOUND="Serializer data not found",
    DEPARTMENT_UPDATE_SUCCESS="Department status update",
    TOPIC_ALREADY_EXISTS="Topic already exists",
    TOPIC_UPDATE_SUCCESS="Topic details update",
    MEMBER_ALREADY_EXISTS="Member already Exists",
    AUTH_EXCEPTION="Member already Exists",
    MATRIX_ERROR_EXCEPTION="Matrix Rule notn updated in back-office applications",
    DEPARTMENT_ID_ERROR="Please Provide valid department id",
    DEPARTMENT_SERIALIZER_NOT_UPDATE="Department Serializer not update",
    TOPIC_ID_ERROR="Please Provide Topic id",
    TOPIC_SERIALIZER_NOT_UPDATE="Topic Serializer not update",
    DELETE_ERROR="This id not delete please check your request params",
    TEAM_NOT_EXISTS="Team id does not exist please provide valid team id",
    MEMBER_NOT_FOUND="Member id not found please upload member id",
    MEMBER_NOT_EXISTS="this Member id Does not exist",
    TASK_NOT_EXISTS="Task id does not exist",
    VALID_CHOICE="please select valid Y/N choices",
    VALID_QUERY_PARAMS="Please provide valid query params",
    DUMMY_USER_NOT_FOUND="User not found please contanct your admin",
    TASK_SERIALIZER_NOT_UPDATE="Task data not updated",
    MEMBER_DOES_NOT_EXIST="This Member id does not exist in our system",
    PLEASE_PROVIDE_PASSWORD="Please provide the password",
    INCORRECT_USERNAME_PASSWORD="Please enter valid email and password",
    USER_DOEST_NOT_EXIST="User not found!",
    USER_ACTIVE_ERROR="Account deactivated, please contact admin",
    MATRIX_ERROR_EXCEPTION_V1="please provide matrix rule details",
    FILE_DOES_NOT_EXIST="File does not exist",
    UPLOAD_VALID_EXCEL="Please upload the valid excel format file",

    IMPORT_SUCCESSFULLY="Data Imported Successfully",
    PROVIDE_COMMENTS_ID="Please Provide Comments id",
    PROVIDE_COMMENTS_ID_WITH_USER="it is not your comments so you have not changed the comments",
    CORRECT_SHEET_ERROR="Please upload correct sheet",
    TASK_UPLOAD_SUCCESSFULLY="Task updated successfuly and [FAILED] task upload failed",
    NOTIFICATION_NOT_FOUND="Notification record not found",
    DEPARTMENT_ALREADY_EXISTS_PRIVATE="This Department Already Exist as a private department with no access to others",
    TOPIC_ALREADY_EXISTS_PRIVATE="This Topic Already Exist as a private Topic with no access to others",
    MEMBER_ALREADY_EXISTS_PRIVATE="This Member Already Exist as a private Member with no access to others",

)


ITALIAN_MSG = dict(
    No_ACTIVE_DATA="Nessun dato attivo",
    DONE="Fatto",
    REQUEST_NOT_FOUND="Richiesta non trovata",
    PLEASE_POST_EMAIL="Si prega inserire e-mail valida",
    ENTER_VALID_EMAIL="Si prega inserire e-mail valida",
    USER_NOT_FOUND="Utente non trovato",
    TOPIC_ALREADY_EXISTS="L'argomento esiste già",
    DEPARTMENT_ALREADY_EXISTS="La funzione/Team esiste già",
    MEMBER_ALREADY_EXISTS="L’utente esiste già",
    AUTH_EXCEPTION="L’utente esiste già",
    DUMMY_USER_NOT_FOUND="Utente non trovato, contatta il tuo amministratore",
    USER_ACTIVE_ERROR="Account disattivato, contatta l'amministratore",
    FILE_DOES_NOT_EXIST="Il file non esiste",
    UPLOAD_VALID_EXCEL="Carica il file in formato Excel valido",
    IMPORT_SUCCESSFULLY="Dati importati con successo",
    CORRECT_SHEET_ERROR="Si prega di caricare il foglio corretto",
    PLEASE_PROVIDE_PASSWORD="Si prega di fornire la password",
    USER_DOEST_NOT_EXIST="Utente non trovato!",
    INCORRECT_USERNAME_PASSWORD="Si prega di inserire e-mail e password valide",
    DEPARTMENT_ALREADY_EXISTS_PRIVATE_ITL="This Department Already Exist as a private department with no access to others",
    TOPIC_ALREADY_EXISTS_PRIVATE="This Topic Already Exist as a private Topic with no access to others",
    MEMBER_ALREADY_EXISTS_PRIVATE="This Member Already Exist as a private Member with no access to others"

)

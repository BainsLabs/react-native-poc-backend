from employee.models import EmployeeDetails
from facerecognition.models import User


class NewEmployee(object):

    def __init__(self,params):
        self.params = params
        self.status = False
        self.message = None
        self.created_employee = None
        self.response_data = None

    def addemployee(self):
        try:
            fs = FileSystemStorage()
            img = self.params['user_image']
            imagename = fs.save(img.name,img)
            uploaded_image = fs.url(imagename)
            image_url = imageUpload(uploaded_image)
            if(image_url):
                  fs.delete(uploaded_image)
            self.created_employee = EmployeeDetails.save(
              official_email=self.params["official_email"].strip().lower(),
              personal_email=self.params["personal_email"],
              employee_id=self.params["employee_id"],
              p_address=self.params["p_address"],
              c_address=self.params["c_address"]
            )
            self.status = True
            self.message = "Employee Created"
        except Exceptions as e:
            self.status= False
            self.message = str(e)
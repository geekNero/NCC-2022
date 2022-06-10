from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# class User(AbstractUser):
#     junior = models.BooleanField(null=True)
#     total_score=models.IntegerField(null=True,default=0)
#     def __str__(self):
#         return self.user.username

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("User Must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password) # hashed password.

        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    junior = models.BooleanField(null=True)
    total_score=models.IntegerField(null=True,default=0)

    objects = UserAccountManager()

    USERNAME_FIELD = 'name'    # login using email 
    REQUIRED_FIELDS = ['name'] # email already included 

    
    def __str__(self):
        return self.name


class Question(models.Model):
    title=models.CharField(max_length=1003, null=True)
    body = models.TextField(null=True)
    description= models.CharField(max_length=1003, null=True)
    input_format=models.TextField(null=True)
    output_format=models.TextField(null=True)  
    constraints=models.TextField(null=True)
    sample_input=models.TextField(null=True)
    sample_output=models.TextField(null=True)
    explaination=models.TextField(null=True)
    correct_submissions = models.IntegerField(null=True)
    total_submissions = models.IntegerField(null=True)
    accuracy = models.FloatField(null=True)
    junior = models.BooleanField(null=True)
    time_limt=models.IntegerField(null=True,default=1)
    memory_limit = models.IntegerField(null=True,default=100000000)
    # questions score for junior senior.
    def __str__(self):
        return self.title


class Submission(models.Model):
    q_id = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    p_id = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    code = models.TextField(null=True)  # text field
    status = models.CharField(
        max_length=10,
        null=True,
        choices=(
            ("WA", "Wrong Answer"),
            ("AC", "Accepted"),
            ("TLE", "Time Limit Exceeded"),
            ("CTE", "Compile Time Error"),
            ("RE", "Runtime Error"),
            ("MLE", "Memory Limit Exceeded"),
        ),
    )  # four type of submission status(WA, PASS, TLE, CTE)
    language = models.CharField(
        max_length=10, null=True, choices=(("c", "C"), ("cpp", "C++"), ("py", "Python"))
    )
def get_question_path(state):
    return "Question_Data/{0}".format(state)


class testcase(models.Model):
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    tc_input = models.FileField(null=True, upload_to=get_question_path("Input"))
    tc_output = models.FileField(null=True, upload_to=get_question_path("Output"))


class SetTime(models.Model):
    start_time = models.DateTimeField(auto_now_add=False)
    final_time = models.DateTimeField(auto_now_add=False)
    

class Question_Status(models.Model):
    q_id = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    p_id = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)
    score= models.IntegerField(null=True,default=0)
    status = models.CharField(
        max_length=10,
        null=True,
        choices=(
            ('NA',"Not Attempted"),
            ("WA", "Wrong Answer"),
            ("AC", "Accepted"),
            ("TLE", "Time Limit Exceeded"),
            ("CTE", "Compile Time Error"),
            ("RE", "Runtime Error"),
            ("MLE", "Memory Limit Exceeded")),default="Not Attempted")



"""


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

"""
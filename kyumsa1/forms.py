from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
import re



User = get_user_model()

class RegisterForm(forms.ModelForm):


    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs= User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if  password is not None and password != password_2:
            self.add_error("password_2", "Your password must much")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Comfirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if  password is not None and password != password_2:
            self.add_error("password_2", "Your password must much")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email','password','is_active','admin']

    def clean_password(self):
        return self.initial["password"]



Halls = [
    ('Kulubya','Kulubya'),
    ('Nanziri','Nanziri'),
    ('Mandella','Mandella'),
    ('Pearl','Pearl'),
    ('North Hall','North Hall')
]
    

Maritial_status =[
    ('Single','Single'),
    ('Married','Married'),
   

]
    

nextofkin =[
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('brother', 'brother'),
    ('Sister', 'Sister'),
    ('Wife', 'Wife'),
    ('Husband', 'Husband'),
    ('Other', 'Other')

]

#the range of years displayed
year_choices = [(r,r) for r in range(1989, datetime.date.today().year+1)]


#registration verification regex function
def reg(a):
    pattern = re.compile(r'[0-9]+/(U|X)/[a-zA-Z]+/[0-9]+/(PE|PD|GV)', re.I)
    result = pattern.match(a)
    if result == None:
        return False
    else:
        return True


#telephone verification function
def tel(a):
    pattern = re.compile(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}')
    result = pattern.match(a)
    if result == None:
        return False
    else:
        return True



#user 
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        required = True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
    )
    first_Name = forms.CharField(
        required = True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={ 'placeholder': 'First Name'}),
    )
    last_Name = forms.CharField(
        required = True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    )
    regNo = forms.CharField(
        required = True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Registrattion no ie 19/U/ITD/374/PD'}),
    )
   
    status = forms.CharField(
        required = True,
        widget=forms.Select(choices=((('Select whether a student or Alumin','Select whether a student or Alumin')),('Student','Student'),('Alumin','Alumin'))),
    )   
    
    password1 = forms.CharField(
    help_text='Enter Password',
    required = True,
    widget=forms.PasswordInput(attrs={ 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
    required = True,
    help_text='Enter Password Again',
    widget=forms.PasswordInput(attrs={ 'placeholder': 'Password Again'}),
    )
    
    
    class Meta:
        model = User
        fields = ['first_Name','last_Name','status','email','password1','password2']
        
    
    def clean_regNo(self):
        data = self.cleaned_data.get('regNo')

        if reg(data) == False:
            raise forms.ValidationError("Use a valid registratioin number")

        return data




class AluminForm(forms.ModelForm):
    yearOfEntry = forms.IntegerField(
        required = True,
        widget=forms.Select(choices=year_choices),
    )
    homeAddress= forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Home Of Residence'}),
    )
    contact= forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone number'}),
    )
    maritialStatus= forms.CharField(
        required = True,
        widget=forms.Select(choices=Maritial_status),
    )
    gender= forms.CharField(
        required = True,
        widget=forms.Select(choices =(('Male','Male'), ('Female','Female'))),
    )
    DoB= forms.DateField(
        required = True,
        widget=forms.DateInput( attrs={'placeholder': 'dob ie 2022-12-31'}),
    )
    course = forms.CharField(
        required = True,
        help_text='Enter the course ',
        widget=forms.TextInput(attrs={'placeholder': 'Course offered'}),
    )
    contactNOK = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Next of kin Phone Number'}),
    )
    relationship= forms.CharField(
        required = True,
        widget=forms.Select(choices=nextofkin),
    )   
    nextOfKin = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'A person to refer to to find you'}),
    )
    yrOfCompletion = forms.IntegerField(
        required = True,
        widget=forms.Select(choices=year_choices),
    )
    positionHeldAtKyumsa = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Any position held at KYUMSA ie Member'}),
    )
    occupation= forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Any work you are involved in now'}),
    )
    jobDescription = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Postion held while at work'}),
    )
    since = forms.DateField(
        required = True,
        widget=forms.DateInput(attrs={'placeholder': 'ie 2020-12-31'}),
    )
   
    

    class Meta:
        model = Alumin
        fields = '__all__'
        exclude = [
            'user'
        ]
        
    def clean_contact(self):
        data = self.cleaned_data.get('contact')

        if tel(data) == False:
            raise forms.ValidationError("Enter a valid telephone number")

        return data
        

class StudentForm(forms.ModelForm):

    yearOfEntry = forms.IntegerField(
        required = True,
        widget=forms.Select(choices=year_choices),
    )
    homeAddress= forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={ 'placeholder': 'Home Of Residence'}),
    )
    contact= forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone number'}),
    )
    maritialStatus= forms.CharField(
        required = True,
        widget=forms.Select(choices = Maritial_status),
    )
    gender= forms.CharField(
        required = True,
        widget=forms.Select(choices = (('Male','Male'), ('Female','Female'))),
    )
    DoB= forms.DateField(
        required = True,
        widget=forms.DateInput( attrs={'placeholder': 'dob ie 2022-12-31'}),
    )
    course = forms.CharField(
        required = True,
        help_text='Enter the course ',
        widget=forms.TextInput(attrs={'placeholder': 'Course offered'}),
    )
    contactNOK = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Next of kin Phone Number'}),
    )
    relationship= forms.CharField(
        required = True,
        widget=forms.Select(choices=nextofkin),
    )   
    nextOfKin = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A person to refer to to find you'}),
    )
    faculty = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Faculty you are associated to'}),
    )
    occupation = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Any activity you are involved ie Student'}),
    )
    hall = forms.CharField(
        required = True,
        widget=forms.Select(choices=Halls),
    )
    nextOfKin = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'A person to refer to to find you'}),
    )
    residenceStatus = forms.CharField(
        required = True,
        widget=forms.Select(choices=(('Resident','Resident'), ('Non-Resident','Non-Resident'))),
    )
    recentSch = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Previous Institution or School'}),
    )
    award = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Award  earned in the previous school'}),
    )
    respnosibilityHeld = forms.CharField(
        required = True,
        widget=forms.TextInput(attrs={'placeholder': 'Any responsibility held in that institution'}),
    )

    class Meta:
        model = Student
        fields = '__all__'
        exclude = [
            'user'
        ]
    
    def clean_contact(self):
        data = self.cleaned_data.get('contact')

        if tel(data) == False:
            raise forms.ValidationError("Enter a valid telephone number")

        return data
        